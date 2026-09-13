#!/usr/bin/env python3
"""Stage 0 fermentation chamber: hold a setpoint, log what actually happened.

    ./chamber.py --list-probes           # find probe ids for chamber.toml
    ./chamber.py --config chamber.toml   # start a run
    ./chamber.py --config chamber.toml --dry-run   # no plug, logs only

The heater is switched off on every exit path, including a crash.
"""

import argparse
import glob
import os
import signal
import sys
import time

from config import W1_DEVICES, load_config_file
from controller import Hysteresis
from loop import ControlLoop
from probes import Probe, parse_w1_slave
from run import Run
from switch import HttpSwitch, NullSwitch


def list_probes():
    """Print every probe the kernel can see, with its current reading."""
    found = sorted(glob.glob(os.path.join(W1_DEVICES, "28-*")))
    if not found:
        print("No DS18B20 found. Is 'dtoverlay=w1-gpio' set and the Pi rebooted?")
        return 1
    for device in found:
        path = os.path.join(device, "w1_slave")
        try:
            with open(path) as fh:
                celsius = parse_w1_slave(fh.read())
        except OSError:
            celsius = None
        print("{}  {}".format(
            os.path.basename(device),
            "unreadable" if celsius is None else "{:.2f} C".format(celsius),
        ))
    return 0


def build(cfg, dry_run):
    probes = [
        Probe(role=p["role"], device_path=p["device_path"], offset_c=p["offset_c"])
        for p in cfg["probes"]
    ]
    controller = Hysteresis(
        setpoint_c=cfg["setpoint_c"],
        band_c=cfg["band_c"],
        min_dwell_s=cfg["min_dwell_s"],
        max_temp_c=cfg["max_temp_c"],
    )
    switch = NullSwitch() if dry_run else HttpSwitch(
        on_url=cfg["switch"]["on_url"], off_url=cfg["switch"]["off_url"]
    )
    run = Run(
        root_dir=os.path.expanduser(cfg["data_dir"]),
        setpoint_c=cfg["setpoint_c"],
        probe_roles=[p["role"] for p in cfg["probes"]],
        probes_meta=cfg["probes"],
        load=cfg.get("load", {}),
        control={
            "band_c": cfg["band_c"],
            "min_dwell_s": cfg["min_dwell_s"],
            "max_temp_c": cfg["max_temp_c"],
            "interval_s": cfg["interval_s"],
            "control_role": cfg["control_role"],
        },
    )
    loop = ControlLoop(
        probes=probes,
        controller=controller,
        switch=switch,
        run=run,
        control_role=cfg["control_role"],
        interval_s=cfg["interval_s"],
    )
    return run, loop


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="chamber.toml")
    parser.add_argument("--list-probes", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="run the loop and log, but never touch the plug")
    args = parser.parse_args(argv)

    if args.list_probes:
        return list_probes()

    cfg = load_config_file(args.config)
    run, loop = build(cfg, args.dry_run)

    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))

    print("run {} -> {}".format(run.run_id, run.path))
    seq = 0
    try:
        while True:
            temps = loop.tick(seq)
            print("{:5d}  {}  heater {}".format(
                seq,
                "  ".join(
                    "{} {}".format(role, "--" if v is None else "{:5.2f}".format(v))
                    for role, v in temps.items()
                ),
                "ON " if loop.controller.heating else "off",
            ), flush=True)
            seq += 1
            time.sleep(cfg["interval_s"])
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.shutdown()
        run.close()
        print("\nheater off, run closed: {}".format(run.path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
