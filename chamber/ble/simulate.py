"""A simulated chamber probe, for running the whole path without hardware.

The physics are the chamber's own, not invented for the demo: a lumped thermal
model of the box under a ceramic emitter, and the same hysteresis control law
`stage0/controller.py` runs. Constants come from the design spec - UA 0.63 W/K,
a 55 W emitter, and a dough time constant of 48 minutes.

That matters for a POC. A simulator with arbitrary curves proves the plumbing
works; one with the real constants also shows the thermal lag the whole project
exists to measure.
"""

from protocol import encode

UA_W_PER_K = 0.63       # box heat loss
HEATER_W = 55.0         # ceramic emitter
BOX_C_J_PER_K = 3000.0  # air plus liner plus probe
DOUGH_TAU_S = 48 * 60   # dough core time constant


class ProbeSimulator:
    def __init__(
        self,
        setpoint_c=40.0,
        air_start_c=21.5,
        dough_start_c=None,
        room_c=21.5,
        band_c=0.25,
        min_dwell_s=60.0,
        dough_probe=True,
        battery_pct=100,
    ):
        self.setpoint_c = setpoint_c
        self.room_c = room_c
        self.band_c = band_c
        self.min_dwell_s = min_dwell_s
        self.dough_probe = dough_probe
        self.battery_pct = battery_pct

        self.air_c = air_start_c
        self.core_c = air_start_c if dough_start_c is None else dough_start_c
        self.heating = False
        self.seq = 0
        self.t_s = 0.0
        self._last_change_s = -1e9

    def step(self, dt_s):
        """Advance the model by dt_s seconds and return the current reading."""
        wanted = (
            self.air_c <= self.setpoint_c + self.band_c
            if self.heating
            else self.air_c < self.setpoint_c - self.band_c
        )
        if wanted != self.heating and self.t_s - self._last_change_s >= self.min_dwell_s:
            self.heating = wanted
            self._last_change_s = self.t_s

        power = HEATER_W if self.heating else 0.0
        self.air_c += (
            (power - UA_W_PER_K * (self.air_c - self.room_c)) / BOX_C_J_PER_K
        ) * dt_s
        self.core_c += ((self.air_c - self.core_c) / DOUGH_TAU_S) * dt_s

        self.t_s += dt_s
        self.seq += 1
        return self.reading()

    def reading(self):
        return {
            "seq": self.seq % 256,
            "t_s": self.t_s,
            "air_c": self.air_c,
            "core_c": self.core_c if self.dough_probe else None,
            "heating": self.heating,
            "battery_pct": self.battery_pct,
            "setpoint_c": self.setpoint_c,
        }

    def advertisement(self):
        """The payload this probe would be broadcasting right now."""
        r = self.reading()
        return encode(
            seq=r["seq"],
            air_c=r["air_c"],
            core_c=r["core_c"],
            battery_pct=r["battery_pct"],
            heating=r["heating"],
        )
