#!/usr/bin/env python3
"""A terminal view of a fermentation run. Braille graphs, no dependencies.

    ./top.py                                   # follow the local listener
    ./top.py --once                            # one frame, then exit
    ./top.py --csv ~/chamber-runs/<run>/samples.csv   # replay a recorded run
    ./top.py --url http://pi.local:8787/telemetry.json

Reads the same telemetry `chamber/ble/listen.py --serve` publishes, and the same
CSV `chamber/stage0` records, so it is a third view of one dataset rather than a
parallel implementation.
"""

import argparse
import json
import shutil
import signal
import sys
import time
import urllib.error
import urllib.request

from screen import render

ALT_SCREEN_ON = "\x1b[?1049h\x1b[?25l"
ALT_SCREEN_OFF = "\x1b[?25h\x1b[?1049l"
HOME = "\x1b[H"
CLEAR_LINE = "\x1b[K"

DEFAULT_URL = "http://127.0.0.1:8787/telemetry.json"


def fetch(url, timeout=2.0):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode())


def from_csv(path):
    """Turn a recorded run into the same document shape the listener serves."""
    with open(path) as fh:
        lines = [line.rstrip("\n") for line in fh if line.strip()]
    if len(lines) < 2:
        raise SystemExit("{}: no data rows".format(path))

    head = [h.strip() for h in lines[0].split(",")]
    index = {name: i for i, name in enumerate(head)}
    air_key = "air_c" if "air_c" in index else None
    core_key = "core_c" if "core_c" in index else None
    if air_key is None:
        raise SystemExit("{}: no air_c column - is this a chamber samples.csv?".format(path))

    def number(row, key):
        if key is None or index.get(key) is None:
            return None
        try:
            return float(row[index[key]])
        except (ValueError, IndexError):
            return None

    samples, setpoint = [], None
    for line in lines[1:]:
        row = line.split(",")
        setpoint = setpoint or number(row, "setpoint_c")
        samples.append([
            number(row, "t_s") or 0.0,
            number(row, air_key),
            number(row, core_key),
            1 if index.get("heating") is not None
            and row[index["heating"]].strip() == "1" else 0,
        ])

    last = samples[-1]
    return {
        "current": {
            "run_id": path.rsplit("/", 2)[-2] if "/" in path else path,
            "source": "recorded run",
            "stale": False,
            "t_s": last[0], "air_c": last[1], "core_c": last[2],
            "setpoint_c": setpoint or 40.0, "heating": bool(last[3]),
        },
        "series": {"setpoint_c": setpoint or 40.0,
                   "columns": ["t_s", "air_c", "core_c", "heating"],
                   "samples": samples},
    }


def draw(docs, status, ansi):
    width, height = shutil.get_terminal_size((80, 24))
    lines = render(docs, width=width, height=height - 1, ansi=ansi, status=status)
    sys.stdout.write(HOME + "\n".join(line + CLEAR_LINE for line in lines) + "\x1b[J")
    sys.stdout.flush()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url", default=DEFAULT_URL)
    p.add_argument("--csv", default=None, help="replay a recorded run instead")
    p.add_argument("--interval", type=float, default=2.0)
    p.add_argument("--once", action="store_true", help="one frame to stdout, then exit")
    p.add_argument("--no-colour", action="store_true")
    args = p.parse_args(argv)

    ansi = not args.no_colour and sys.stdout.isatty()

    if args.csv:
        docs = from_csv(args.csv)
        if args.once:
            print("\n".join(render(docs, *_size(), ansi=ansi, status=args.csv)))
            return 0
        status = args.csv
    else:
        docs, status = None, "waiting for {}".format(args.url)

    if args.once:
        try:
            docs = fetch(args.url)
            status = args.url
        except (urllib.error.URLError, OSError, ValueError) as err:
            status = "{} unreachable: {}".format(args.url, err)
        print("\n".join(render(docs, *_size(), ansi=ansi, status=status)))
        return 0

    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    sys.stdout.write(ALT_SCREEN_ON)
    misses = 0
    try:
        while True:
            if not args.csv:
                try:
                    docs = fetch(args.url)
                    misses = 0
                    status = "{}   updated {}".format(
                        args.url, time.strftime("%H:%M:%S"))
                except (urllib.error.URLError, OSError, ValueError) as err:
                    misses += 1
                    status = "{}  unreachable ({} tries): {}".format(
                        args.url, misses, err)
            draw(docs, status, ansi)
            time.sleep(args.interval)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        sys.stdout.write(ALT_SCREEN_OFF)
        sys.stdout.flush()
    return 0


def _size():
    width, height = shutil.get_terminal_size((80, 24))
    return width, height - 1


if __name__ == "__main__":
    raise SystemExit(main())
