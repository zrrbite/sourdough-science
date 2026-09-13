#!/usr/bin/env python3
"""Listen for chamber probe advertisements and shape them for the UI.

    ./listen.py --simulate --speed 120 --limit 720   # no hardware, fast
    ./listen.py --simulate                           # no hardware, real time
    ./listen.py                                      # real BLE scan (needs bleak)

Writes `telemetry.json` (the two document bodies the viewer reads) and, with
--record, a run directory in the same CSV + manifest format stage 0 produces.

In simulate mode the readings are round-tripped through the real advertisement
encoding before use, so the wire format is exercised rather than bypassed - the
simulated path and the radio path decode identically.
"""

import argparse
import json
import os
import sys
import time

from protocol import COMPANY_ID, decode
from simulate import ProbeSimulator
from telemetry import TelemetryBuffer

# stage 0 owns the run-directory writer. A third consumer would justify moving
# it to chamber/common/; with two, an explicit path is honest and cheaper.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stage0"))
from run import Run  # noqa: E402


def simulated_readings(sim, interval_s, speed, limit):
    """Yield decoded readings from the simulator, via the real wire format."""
    emitted = 0
    while limit is None or emitted < limit:
        sim.step(interval_s)
        reading = decode(sim.advertisement())
        if reading is not None:
            reading["t_s"] = sim.t_s
            reading["setpoint_c"] = sim.setpoint_c
            yield reading
            emitted += 1
        if speed:
            time.sleep(interval_s / speed)


def scanned_readings(interval_s, limit):
    """Yield decoded readings from real advertisements."""
    try:
        import asyncio

        from bleak import BleakScanner
    except ImportError:
        raise SystemExit("Real scanning needs bleak: pip install bleak "
                         "(or use --simulate)")

    queue = []

    def on_advert(_device, adv):
        payload = adv.manufacturer_data.get(COMPANY_ID)
        reading = decode(payload) if payload else None
        if reading is not None:
            reading["rssi"] = adv.rssi
            queue.append(reading)

    async def pump():
        scanner = BleakScanner(detection_callback=on_advert)
        await scanner.start()
        started = time.monotonic()
        try:
            emitted = 0
            while limit is None or emitted < limit:
                await asyncio.sleep(interval_s)
                while queue:
                    reading = queue.pop(0)
                    reading["t_s"] = time.monotonic() - started
                    results.append(reading)
                    emitted += 1
        finally:
            await scanner.stop()

    results = []
    asyncio.run(pump())
    return iter(results)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--simulate", action="store_true", help="no radio, run the physics")
    p.add_argument("--speed", type=float, default=1.0,
                   help="simulate faster than real time (0 = as fast as possible)")
    p.add_argument("--interval", type=float, default=10.0, help="seconds per sample")
    p.add_argument("--limit", type=int, default=None, help="stop after N samples")
    p.add_argument("--setpoint", type=float, default=40.0)
    p.add_argument("--out", default="telemetry.json")
    p.add_argument("--record", metavar="DIR", default=None,
                   help="also write a run directory (CSV + manifest) here")
    p.add_argument("--no-dough-probe", action="store_true",
                   help="simulate a probe with no dough sensor attached")
    args = p.parse_args(argv)

    run_id = time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime()) + "_ble"
    buffer = TelemetryBuffer(run_id=run_id, setpoint_c=args.setpoint,
                             source="ble-simulated" if args.simulate else "ble")

    recorder = None
    if args.record:
        recorder = Run(root_dir=os.path.expanduser(args.record), run_id=run_id,
                       setpoint_c=args.setpoint, probe_roles=["air", "core"],
                       control={"law": "reported-by-probe"},
                       load={"source": buffer.source})

    if args.simulate:
        sim = ProbeSimulator(setpoint_c=args.setpoint,
                             dough_probe=not args.no_dough_probe)
        readings = simulated_readings(sim, args.interval, args.speed, args.limit)
    else:
        readings = scanned_readings(args.interval, args.limit)

    print("run {}  ->  {}".format(run_id, args.out))
    count = 0
    try:
        for reading in readings:
            buffer.add(reading)
            if recorder:
                recorder.append(seq=reading["seq"], t_s=reading["t_s"],
                                temps={"air": reading["air_c"],
                                       "core": reading["core_c"]},
                                heating=reading["heating"])
            count += 1
            if count % 25 == 0 or count == 1:
                print("  {:5d}  air {:5.2f}  dough core {}  heater {}".format(
                    count, reading["air_c"],
                    "  --  " if reading["core_c"] is None
                    else "{:5.2f}".format(reading["core_c"]),
                    "ON " if reading["heating"] else "off"), flush=True)
            _write(args.out, buffer)
    except KeyboardInterrupt:
        pass
    finally:
        _write(args.out, buffer)
        if recorder:
            recorder.close()
        print("\n{} samples  ->  {}".format(count, args.out))
    return 0


def _write(path, buffer):
    with open(path, "w") as fh:
        json.dump(buffer.documents(), fh, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    raise SystemExit(main())
