"""Wired DS18B20 probes through the kernel's 1-Wire driver.

Wraps stage 0's `Probe` rather than reparsing sysfs, so there is one
implementation of the w1_slave format and one place calibration is applied.
"""

import os
import sys
import time

from base import Source, reading

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "stage0"))
from probes import Probe  # noqa: E402

W1_DEVICES = "/sys/bus/w1/devices"


class OneWireSource(Source):
    name = "w1"

    def __init__(self, paths=None, ids=None, offsets=None, interval_s=10.0,
                 limit=None):
        offsets = offsets or {}
        paths = dict(paths or {})
        for role, device_id in (ids or {}).items():
            paths.setdefault(role, "{}/{}/w1_slave".format(W1_DEVICES, device_id))
        self.probes = {
            role: Probe(role=role, device_path=path, offset_c=offsets.get(role, 0.0))
            for role, path in paths.items()
        }
        self.interval_s = interval_s
        self.limit = limit

    def readings(self):
        started = time.monotonic()
        emitted = 0
        while self.limit is None or emitted < self.limit:
            values = {role: probe.read() for role, probe in self.probes.items()}
            yield reading(
                t_s=time.monotonic() - started,
                air_c=values.get("air"),
                core_c=values.get("core"),
                heating=False,   # a wired probe reports temperature, not control
                **{k: v for k, v in values.items() if k not in ("air", "core")}
            )
            emitted += 1
            if self.interval_s:
                time.sleep(self.interval_s)
