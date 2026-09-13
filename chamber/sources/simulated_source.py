"""The simulator as a source, so no-hardware runs use the same path as hardware."""

import time

from base import Source, reading
from decoders import decode_chamber
from simulated import ProbeSimulator


class SimulatedSource(Source):
    name = "simulated"

    def __init__(self, simulator=None, interval_s=10.0, speed=1.0, limit=None):
        self.simulator = simulator or ProbeSimulator()
        self.interval_s = interval_s
        self.speed = speed
        self.limit = limit

    def readings(self):
        emitted = 0
        while self.limit is None or emitted < self.limit:
            self.simulator.step(self.interval_s)
            # through the real wire format, so the simulated path and the radio
            # path decode through identical code
            decoded = decode_chamber(self.simulator.advertisement())
            if decoded is not None:
                yield reading(
                    t_s=self.simulator.t_s,
                    air_c=decoded["air_c"],
                    core_c=decoded["core_c"],
                    heating=decoded["heating"],
                    seq=decoded["seq"],
                    battery_pct=decoded["battery_pct"],
                    setpoint_c=self.simulator.setpoint_c,
                )
                emitted += 1
            if self.speed:
                time.sleep(self.interval_s / self.speed)
