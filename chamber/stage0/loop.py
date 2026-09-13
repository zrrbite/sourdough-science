"""The sense -> decide -> switch -> log cycle.

Everything it touches is injected, so the whole loop runs in a test with real
probe files, a real Run on disk and a stand-in switch, and no chamber.
"""

import time


class ControlLoop:
    def __init__(
        self,
        probes,
        controller,
        switch,
        run,
        control_role="air",
        interval_s=10.0,
        clock=time.monotonic,
    ):
        self.probes = list(probes)
        self.controller = controller
        self.switch = switch
        self.run = run
        self.control_role = control_role
        self.interval_s = interval_s
        self.clock = clock
        self._t0 = clock()

    def tick(self, seq):
        """One cycle. Returns the temperatures read, for the caller to display."""
        now = self.clock()
        t_s = now - self._t0

        temps = {probe.role: probe.read() for probe in self.probes}
        heating = self.controller.update(now_s=now, temp_c=temps.get(self.control_role))

        flags = list(self.controller.flags)
        if not self.switch.set(heating):
            flags.append("switch_fault")

        self.run.append(seq=seq, t_s=t_s, temps=temps, heating=heating, flags=flags)
        return temps

    def shutdown(self):
        """Leave the heater off. Called on every exit path, including crashes."""
        self.switch.set(False)
