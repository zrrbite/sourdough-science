"""Bang-bang heat control with hysteresis, minimum dwell, and safety cut-outs.

Hysteresis rather than PID is a deliberate choice at this stage: the dough's own
thermal mass low-passes the air swing, so a band of a few tenths of a degree
barely reaches the core. See docs/10-thermal-lag-*.md.
"""


class Hysteresis:
    """Decide whether the heater should be on.

    Safety cut-outs (failed probe, over-temperature) bypass the dwell timer:
    refusing to switch off promptly is never the safe choice.
    """

    def __init__(self, setpoint_c, band_c=0.25, min_dwell_s=60.0, max_temp_c=55.0):
        self.setpoint_c = setpoint_c
        self.band_c = band_c
        self.min_dwell_s = min_dwell_s
        self.max_temp_c = max_temp_c
        self.heating = False
        self.flags = []
        self._last_change_s = None

    def update(self, now_s, temp_c):
        """Return the heater state wanted now, given the controlling temperature."""
        self.flags = []

        if temp_c is None:
            self.flags.append("probe_fault")
            return self._apply(now_s, False)
        if temp_c >= self.max_temp_c:
            self.flags.append("over_temperature")
            return self._apply(now_s, False)

        if self.heating:
            wanted = temp_c <= self.setpoint_c + self.band_c
        else:
            wanted = temp_c < self.setpoint_c - self.band_c

        if wanted != self.heating and not self._dwell_elapsed(now_s):
            self.flags.append("dwell_hold")
            return self.heating

        return self._apply(now_s, wanted)

    def _dwell_elapsed(self, now_s):
        if self._last_change_s is None:
            return True
        return (now_s - self._last_change_s) >= self.min_dwell_s

    def _apply(self, now_s, state):
        if state != self.heating:
            self.heating = state
            self._last_change_s = now_s
        return self.heating
