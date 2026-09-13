#!/usr/bin/env python3
"""Collect readings from any source and publish them for the viewers.

    ./listen.py --simulate --serve            # live UI at http://127.0.0.1:8787
    ./listen.py --serve                       # the same, from our BLE probe
    ./listen.py --source serial --port /dev/tty.usbmodem1101 --serve
    ./listen.py --source w1 --air 28-0000063d1f2a --core 28-0000063d4b11
    ./listen.py --source ble --decoder inkbird --serve
    ./listen.py --scan-raw                    # dump advertisements, write a decoder

    ./listen.py --simulate --speed 120 --limit 270    # fast, no server
    ./listen.py --simulate --out-dir runs/live        # split docs for the relay

With --serve this is the whole live system: it holds the buffer, serves the
viewer and its telemetry from one origin, and the page polls it. Nothing else
runs, nothing authenticates, no bridge.

The source is a flag rather than a rewrite. Which transport the hardware ends up
using - Bluetooth, USB serial, wired 1-Wire, or somebody else's probe entirely -
changes this line and nothing downstream.
"""

import argparse
import json
import os
import sys
import time

from server import start_server
from telemetry import TelemetryBuffer

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "sources"))
sys.path.insert(0, os.path.join(_HERE, "..", "stage0"))

from ble import scan_raw  # noqa: E402
from registry import open_source  # noqa: E402
from run import Run  # noqa: E402

# Mirrors the wrapper claude.ai puts around a published artifact, so the page
# renders identically served locally and served there.
SKELETON = (
    '<!doctype html><html><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    "<style>:root{color-scheme:light}body{margin:0;font:14px system-ui,sans-serif;"
    "background:#faf9f7}img{max-width:100%}[hidden]{display:none!important}</style>"
    "</head><body>{body}</body></html>"
)
VIEWER = os.path.join(_HERE, "..", "viewer", "dough-core-trace.html")


def viewer_html():
    with open(VIEWER) as fh:
        return SKELETON.replace("{body}", fh.read())


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", default="ble",
                   help="simulated | ble | serial | w1  (default: ble)")
    p.add_argument("--simulate", action="store_true",
                   help="shorthand for --source simulated")
    p.add_argument("--decoder", default="chamber",
                   help="chamber | inkbird | line  (ble sources only)")
    p.add_argument("--port", default=None, help="serial device, for --source serial")
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--air", default=None, help="1-Wire id of the air probe")
    p.add_argument("--core", default=None, help="1-Wire id of the dough core probe")
    p.add_argument("--scan-raw", nargs="?", type=float, const=20.0, default=None,
                   metavar="SECONDS",
                   help="dump every BLE advertisement seen, then exit")
    p.add_argument("--speed", type=float, default=1.0,
                   help="simulate faster than real time (0 = as fast as possible)")
    p.add_argument("--interval", type=float, default=10.0, help="seconds per sample")
    p.add_argument("--limit", type=int, default=None, help="stop after N samples")
    p.add_argument("--setpoint", type=float, default=40.0)
    p.add_argument("--out", default="telemetry.json")
    p.add_argument("--out-dir", default=None, metavar="DIR",
                   help="also write telemetry-current.json and telemetry-series.json "
                        "there, the split form the artifact-store relay uploads")
    p.add_argument("--serve", nargs="?", type=int, const=8787, default=None,
                   metavar="PORT",
                   help="serve the viewer and its telemetry locally (default 8787)")
    p.add_argument("--record", metavar="DIR", default=None,
                   help="also write a run directory (CSV + manifest) here")
    p.add_argument("--no-dough-probe", action="store_true",
                   help="simulate a probe with no dough sensor attached")
    args = p.parse_args(argv)

    if args.scan_raw is not None:
        scan_raw(args.scan_raw)
        return 0

    name = "simulated" if args.simulate else args.source
    try:
        source = open_source(
            name,
            interval_s=args.interval, speed=args.speed, limit=args.limit,
            setpoint_c=args.setpoint, dough_probe=not args.no_dough_probe,
            decoder=args.decoder, port=args.port, baud=args.baud,
            ids=_ids(args.air, args.core),
        )
    except (ValueError, FileNotFoundError) as err:
        # a mistyped flag is a user error, not a stack trace
        p.error(str(err))

    run_id = time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime()) + "_" + name
    buffer = TelemetryBuffer(run_id=run_id, setpoint_c=args.setpoint, source=name)

    recorder = None
    if args.record:
        recorder = Run(root_dir=os.path.expanduser(args.record), run_id=run_id,
                       setpoint_c=args.setpoint, probe_roles=["air", "core"],
                       control={"law": "reported-by-source"},
                       load={"source": name, "decoder": args.decoder})

    server = None
    if args.serve is not None:
        server = start_server(args.serve, buffer, viewer_html())
        print("live UI  ->  http://127.0.0.1:{}".format(server.server_address[1]))

    print("run {}  source {}  ->  {}".format(run_id, name, args.out))
    count = 0
    try:
        for reading in source.readings():
            buffer.add(reading)
            if recorder:
                recorder.append(seq=reading.get("seq", count), t_s=reading["t_s"],
                                temps={"air": reading["air_c"],
                                       "core": reading["core_c"]},
                                heating=reading["heating"])
            count += 1
            if count % 25 == 0 or count == 1:
                print("  {:5d}  air {}  dough core {}  heater {}".format(
                    count, _fmt(reading["air_c"]), _fmt(reading["core_c"]),
                    "ON " if reading["heating"] else "off"), flush=True)
            _write(args.out, buffer)
            if args.out_dir:
                _write_split(args.out_dir, buffer)
    except KeyboardInterrupt:
        pass
    finally:
        _write(args.out, buffer)
        if args.out_dir:
            _write_split(args.out_dir, buffer)
        if recorder:
            recorder.close()
        source.close()
        if server:
            server.shutdown()
        print("\n{} samples  ->  {}".format(count, args.out))
    return 0


def _ids(air, core):
    ids = {}
    if air:
        ids["air"] = air
    if core:
        ids["core"] = core
    return ids or None


def _fmt(value):
    return "  --  " if value is None else "{:5.2f}".format(value)


def _write(path, buffer):
    with open(path, "w") as fh:
        json.dump(buffer.documents(), fh, indent=2)
        fh.write("\n")


def _write_split(directory, buffer):
    """One file per document, which is what the artifact-store relay uploads."""
    os.makedirs(os.path.expanduser(directory), exist_ok=True)
    for name, body in buffer.documents().items():
        path = os.path.join(os.path.expanduser(directory),
                            "telemetry-{}.json".format(name))
        with open(path, "w") as fh:
            json.dump(body, fh, indent=2)
            fh.write("\n")


if __name__ == "__main__":
    raise SystemExit(main())
