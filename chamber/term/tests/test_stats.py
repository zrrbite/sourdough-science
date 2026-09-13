import unittest

from stats import summarise

# [t_s, air_c, core_c, heating]
RAMP = [[i * 60.0, 40.0, 20.0 + i * 0.5, 1 if i % 4 else 0] for i in range(41)]


class TestSummarise(unittest.TestCase):
    def test_no_samples_gives_empty_figures(self):
        s = summarise([], setpoint=40.0)
        self.assertIsNone(s["lag_s"])
        self.assertIsNone(s["mean_core"])

    def test_lag_is_when_the_core_first_comes_within_half_a_degree(self):
        s = summarise(RAMP, setpoint=40.0)
        self.assertEqual(s["lag_s"], 39 * 60.0)  # core hits 39.5 at i=39

    def test_lag_is_none_when_the_core_never_arrives(self):
        cool = [[i * 60.0, 40.0, 25.0, 1] for i in range(10)]
        self.assertIsNone(summarise(cool, setpoint=40.0)["lag_s"])

    def test_mean_core_is_time_weighted(self):
        flat = [[0.0, 40.0, 30.0, 1], [10.0, 40.0, 30.0, 1], [1000.0, 40.0, 36.0, 1]]
        # the 36 C sample covers 990 s of the 1000 s, so the mean sits near 36
        self.assertGreater(summarise(flat, setpoint=40.0)["mean_core"], 35.0)

    def test_peak_gradient_is_the_widest_air_to_core_gap(self):
        s = summarise(RAMP, setpoint=40.0)
        self.assertAlmostEqual(s["peak_gap"], 20.0)
        self.assertEqual(s["peak_gap_at"], 0.0)

    def test_duty_is_the_fraction_of_time_heating(self):
        half = [[0.0, 40.0, 30.0, 0], [10.0, 40.0, 30.0, 1], [20.0, 40.0, 30.0, 1]]
        self.assertAlmostEqual(summarise(half, setpoint=40.0)["duty"], 1.0)

    def test_a_missing_core_reading_does_not_break_the_figures(self):
        gappy = [[0.0, 40.0, None, 1], [60.0, 40.0, 30.0, 1]]
        self.assertIsNotNone(summarise(gappy, setpoint=40.0)["mean_core"])

    def test_total_is_the_span_of_the_run(self):
        self.assertEqual(summarise(RAMP, setpoint=40.0)["total_s"], 40 * 60.0)


if __name__ == "__main__":
    unittest.main()
