import unittest

from controller import Hysteresis


class TestHysteresis(unittest.TestCase):
    def test_starts_off(self):
        c = Hysteresis(setpoint_c=40.0)
        self.assertFalse(c.heating)

    def test_turns_on_when_below_the_band(self):
        c = Hysteresis(setpoint_c=40.0, band_c=0.25)
        self.assertTrue(c.update(now_s=0.0, temp_c=39.5))

    def test_stays_off_inside_the_band(self):
        c = Hysteresis(setpoint_c=40.0, band_c=0.25)
        self.assertFalse(c.update(now_s=0.0, temp_c=39.9))

    def test_stays_on_until_above_the_band(self):
        c = Hysteresis(setpoint_c=40.0, band_c=0.25, min_dwell_s=0)
        c.update(now_s=0.0, temp_c=39.5)
        self.assertTrue(c.update(now_s=10.0, temp_c=40.1))

    def test_turns_off_above_the_band(self):
        c = Hysteresis(setpoint_c=40.0, band_c=0.25, min_dwell_s=0)
        c.update(now_s=0.0, temp_c=39.5)
        self.assertFalse(c.update(now_s=10.0, temp_c=40.3))

    def test_min_dwell_blocks_switching_off_too_soon(self):
        c = Hysteresis(setpoint_c=40.0, band_c=0.25, min_dwell_s=60)
        c.update(now_s=0.0, temp_c=39.5)
        self.assertTrue(c.update(now_s=30.0, temp_c=40.3))

    def test_min_dwell_expires(self):
        c = Hysteresis(setpoint_c=40.0, band_c=0.25, min_dwell_s=60)
        c.update(now_s=0.0, temp_c=39.5)
        self.assertFalse(c.update(now_s=61.0, temp_c=40.3))

    def test_probe_fault_cuts_heat_ignoring_dwell(self):
        c = Hysteresis(setpoint_c=40.0, min_dwell_s=600)
        c.update(now_s=0.0, temp_c=39.0)
        self.assertFalse(c.update(now_s=1.0, temp_c=None))

    def test_over_temperature_cuts_heat_ignoring_dwell(self):
        c = Hysteresis(setpoint_c=40.0, min_dwell_s=600, max_temp_c=55.0)
        c.update(now_s=0.0, temp_c=39.0)
        self.assertFalse(c.update(now_s=1.0, temp_c=55.0))

    def test_records_why_heat_was_cut(self):
        c = Hysteresis(setpoint_c=40.0, min_dwell_s=600, max_temp_c=55.0)
        c.update(now_s=0.0, temp_c=39.0)
        c.update(now_s=1.0, temp_c=56.0)
        self.assertIn("over_temperature", c.flags)


if __name__ == "__main__":
    unittest.main()
