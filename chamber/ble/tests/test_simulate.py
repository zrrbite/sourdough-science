import unittest

from protocol import decode
from simulate import ProbeSimulator


class TestProbeSimulator(unittest.TestCase):
    def test_starts_cold_at_room_temperature(self):
        s = ProbeSimulator(air_start_c=21.5)
        self.assertAlmostEqual(s.step(0)["air_c"], 21.5, places=2)

    def test_heating_raises_the_air_temperature(self):
        s = ProbeSimulator(setpoint_c=40.0, air_start_c=21.5)
        first = s.step(60)["air_c"]
        later = s.step(60)["air_c"]
        self.assertGreater(later, first)

    def test_the_dough_lags_behind_the_air(self):
        s = ProbeSimulator(setpoint_c=40.0, air_start_c=21.5)
        for _ in range(30):
            r = s.step(60)
        self.assertLess(r["core_c"], r["air_c"])

    def test_the_heater_stops_once_the_air_passes_the_band(self):
        s = ProbeSimulator(setpoint_c=40.0, air_start_c=21.5, min_dwell_s=0)
        for _ in range(400):
            r = s.step(30)
            if not r["heating"]:
                break
        self.assertFalse(r["heating"])
        self.assertGreater(r["air_c"], 40.0)

    def test_a_step_produces_a_decodable_advertisement(self):
        s = ProbeSimulator(setpoint_c=40.0, air_start_c=21.5)
        reading = s.step(60)
        decoded = decode(s.advertisement())
        self.assertAlmostEqual(decoded["air_c"], round(reading["air_c"], 2), places=2)
        self.assertAlmostEqual(decoded["core_c"], round(reading["core_c"], 2), places=2)

    def test_the_sequence_advances_and_wraps(self):
        s = ProbeSimulator()
        for _ in range(257):
            s.step(1)
        self.assertEqual(decode(s.advertisement())["seq"], 257 % 256)

    def test_a_probeless_simulator_reports_no_dough_reading(self):
        s = ProbeSimulator(dough_probe=False)
        s.step(60)
        self.assertIsNone(decode(s.advertisement())["core_c"])


if __name__ == "__main__":
    unittest.main()
