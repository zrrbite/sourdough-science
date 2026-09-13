import os
import tempfile
import unittest
from datetime import datetime, timezone

from controller import Hysteresis
from loop import ControlLoop
from probes import Probe
from run import Run
from switch import NullSwitch

STARTED = datetime(2026, 9, 13, 18, 4, 12, tzinfo=timezone.utc)


def probe_at(role, celsius, offset_c=0.0):
    body = (
        "d8 01 4b 46 7f ff 0c 10 2e : crc=2e YES\n"
        "d8 01 4b 46 7f ff 0c 10 2e t={}\n".format(int(celsius * 1000))
    )
    path = os.path.join(tempfile.mkdtemp(), "w1_slave")
    with open(path, "w") as fh:
        fh.write(body)
    return Probe(role=role, device_path=path, offset_c=offset_c)


class RefusingSwitch(NullSwitch):
    def set(self, on):
        super().set(on)
        return False


class TestControlLoop(unittest.TestCase):
    def _loop(self, probes, switch=None, setpoint_c=40.0):
        self.run_obj = Run(
            root_dir=tempfile.mkdtemp(),
            run_id="r",
            started_utc=STARTED,
            setpoint_c=setpoint_c,
            probe_roles=[p.role for p in probes],
        )
        self.clock = [0.0]
        return ControlLoop(
            probes=probes,
            controller=Hysteresis(setpoint_c=setpoint_c, min_dwell_s=0),
            switch=switch or NullSwitch(),
            run=self.run_obj,
            control_role="air",
            clock=lambda: self.clock[0],
        )

    def _rows(self):
        with open(os.path.join(self.run_obj.path, "samples.csv")) as fh:
            return fh.read().splitlines()

    def test_a_tick_logs_one_row_per_probe_reading(self):
        loop = self._loop([probe_at("air", 24.0), probe_at("core", 22.5)])
        loop.tick(seq=0)
        self.assertEqual(self._rows()[1], "0,0.0,2026-09-13T18:04:12Z,40.0,24.0,22.5,1,")

    def test_a_cold_chamber_switches_the_heater_on(self):
        switch = NullSwitch()
        loop = self._loop([probe_at("air", 24.0)], switch=switch)
        loop.tick(seq=0)
        self.assertEqual(switch.calls, [True])

    def test_a_hot_chamber_leaves_the_heater_off(self):
        switch = NullSwitch()
        loop = self._loop([probe_at("air", 44.0)], switch=switch)
        loop.tick(seq=0)
        self.assertEqual(switch.calls, [False])

    def test_the_controlling_probe_is_the_named_role(self):
        switch = NullSwitch()
        loop = self._loop([probe_at("air", 44.0), probe_at("core", 20.0)], switch=switch)
        loop.tick(seq=0)
        self.assertEqual(switch.calls, [False])

    def test_a_plug_that_refuses_is_flagged_in_the_log(self):
        loop = self._loop([probe_at("air", 24.0)], switch=RefusingSwitch())
        loop.tick(seq=0)
        self.assertTrue(self._rows()[1].endswith("switch_fault"))

    def test_shutdown_turns_the_heater_off(self):
        switch = NullSwitch()
        loop = self._loop([probe_at("air", 24.0)], switch=switch)
        loop.tick(seq=0)
        loop.shutdown()
        self.assertEqual(switch.calls[-1], False)

    def test_elapsed_time_comes_from_the_clock(self):
        loop = self._loop([probe_at("air", 24.0)])
        loop.tick(seq=0)
        self.clock[0] = 30.0
        loop.tick(seq=1)
        self.assertTrue(self._rows()[2].startswith("1,30.0,2026-09-13T18:04:42Z"))


if __name__ == "__main__":
    unittest.main()
