import json
import unittest

from telemetry import SERIES_CAP, TelemetryBuffer


def reading(seq=0, t_s=0.0, air=24.0, core=22.0, heating=True):
    return {"seq": seq, "t_s": t_s, "air_c": air, "core_c": core,
            "heating": heating, "battery_pct": 97, "setpoint_c": 40.0}


class TestCurrent(unittest.TestCase):
    def test_current_reflects_the_latest_reading(self):
        b = TelemetryBuffer(run_id="r")
        b.add(reading(seq=1, air=30.0))
        b.add(reading(seq=2, air=31.5))
        self.assertAlmostEqual(b.documents()["current"]["air_c"], 31.5)

    def test_current_carries_the_run_id_and_schema_version(self):
        d = TelemetryBuffer(run_id="run-7").documents()["current"]
        self.assertEqual(d["run_id"], "run-7")
        self.assertEqual(d["schema_version"], 1)

    def test_current_before_any_reading_is_marked_stale(self):
        self.assertTrue(TelemetryBuffer(run_id="r").documents()["current"]["stale"])

    def test_current_after_a_reading_is_not_stale(self):
        b = TelemetryBuffer(run_id="r")
        b.add(reading())
        self.assertFalse(b.documents()["current"]["stale"])


class TestSeries(unittest.TestCase):
    def test_each_reading_adds_one_compact_row(self):
        b = TelemetryBuffer(run_id="r")
        b.add(reading(t_s=10.0, air=25.5, core=22.25, heating=True))
        self.assertEqual(b.documents()["series"]["samples"], [[10.0, 25.5, 22.25, 1]])

    def test_a_missing_core_reading_is_null_in_the_row(self):
        b = TelemetryBuffer(run_id="r")
        b.add(reading(core=None))
        self.assertIsNone(b.documents()["series"]["samples"][0][2])

    def test_the_series_is_capped_and_drops_the_oldest(self):
        b = TelemetryBuffer(run_id="r")
        for i in range(SERIES_CAP + 50):
            b.add(reading(t_s=float(i)))
        samples = b.documents()["series"]["samples"]
        self.assertEqual(len(samples), SERIES_CAP)
        self.assertEqual(samples[0][0], 50.0)

    def test_a_full_series_document_stays_well_inside_the_size_limit(self):
        b = TelemetryBuffer(run_id="r")
        for i in range(SERIES_CAP):
            b.add(reading(t_s=float(i), air=44.44, core=38.07))
        size = len(json.dumps(b.documents()["series"]).encode())
        self.assertLess(size, 256 * 1024)


class TestDocumentBodies(unittest.TestCase):
    def test_both_bodies_are_json_objects(self):
        docs = TelemetryBuffer(run_id="r").documents()
        for body in docs.values():
            self.assertIsInstance(body, dict)
            json.dumps(body)


if __name__ == "__main__":
    unittest.main()
