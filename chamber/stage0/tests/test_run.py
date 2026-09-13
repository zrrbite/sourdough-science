import json
import os
import tempfile
import unittest
from datetime import datetime, timezone

from run import Run

STARTED = datetime(2026, 9, 13, 18, 4, 12, tzinfo=timezone.utc)


class TestRun(unittest.TestCase):
    def _run(self, **kw):
        kw.setdefault("root_dir", tempfile.mkdtemp())
        kw.setdefault("run_id", "2026-09-13T18-04-12Z_test")
        kw.setdefault("started_utc", STARTED)
        kw.setdefault("setpoint_c", 40.0)
        kw.setdefault("probe_roles", ["air", "core"])
        return Run(**kw)

    def _read(self, run, name):
        with open(os.path.join(run.path, name)) as fh:
            return fh.read()

    def test_creates_the_run_directory_with_both_files(self):
        r = self._run()
        self.assertTrue(os.path.isfile(os.path.join(r.path, "samples.csv")))
        self.assertTrue(os.path.isfile(os.path.join(r.path, "manifest.json")))

    def test_header_carries_one_column_per_probe_role(self):
        r = self._run(probe_roles=["air", "core", "ambient"])
        header = self._read(r, "samples.csv").splitlines()[0]
        self.assertEqual(
            header,
            "seq,t_s,iso_utc,setpoint_c,air_c,core_c,ambient_c,heating,flags",
        )

    def test_append_writes_a_row_in_header_order(self):
        r = self._run()
        r.append(seq=7, t_s=70.0, temps={"air": 39.9, "core": 24.1}, heating=True)
        row = self._read(r, "samples.csv").splitlines()[1]
        self.assertEqual(row, "7,70.0,2026-09-13T18:05:22Z,40.0,39.9,24.1,1,")

    def test_append_is_flushed_immediately(self):
        r = self._run()
        r.append(seq=0, t_s=0.0, temps={"air": 39.9, "core": 24.1}, heating=False)
        self.assertEqual(len(self._read(r, "samples.csv").splitlines()), 2)

    def test_a_missing_probe_value_is_an_empty_field(self):
        r = self._run()
        r.append(seq=0, t_s=0.0, temps={"air": None, "core": 24.1}, heating=False)
        self.assertEqual(
            self._read(r, "samples.csv").splitlines()[1],
            "0,0.0,2026-09-13T18:04:12Z,40.0,,24.1,0,",
        )

    def test_flags_are_pipe_separated(self):
        r = self._run()
        r.append(
            seq=0,
            t_s=0.0,
            temps={"air": 39.9, "core": 24.1},
            heating=False,
            flags=["probe_fault", "dwell_hold"],
        )
        row = self._read(r, "samples.csv").splitlines()[1]
        self.assertTrue(row.endswith("probe_fault|dwell_hold"))

    def test_manifest_records_setpoint_probes_and_load(self):
        probes_meta = [{"role": "core", "offset_c": -0.25, "rom": "28-abc"}]
        r = self._run(probes_meta=probes_meta, load={"dough_mass_g": 1000})
        m = json.loads(self._read(r, "manifest.json"))
        self.assertEqual(m["setpoint"], {"type": "constant", "value_c": 40.0})
        self.assertEqual(m["probes"], probes_meta)
        self.assertEqual(m["load"], {"dough_mass_g": 1000})
        self.assertEqual(m["schema_version"], 1)

    def test_close_records_the_end_time(self):
        r = self._run()
        r.close(ended_utc=datetime(2026, 9, 14, 6, 0, 0, tzinfo=timezone.utc))
        m = json.loads(self._read(r, "manifest.json"))
        self.assertEqual(m["ended_utc"], "2026-09-14T06:00:00Z")


if __name__ == "__main__":
    unittest.main()


class TestRunControlBlock(unittest.TestCase):
    def test_manifest_records_the_control_parameters(self):
        r = Run(
            root_dir=tempfile.mkdtemp(),
            run_id="r",
            started_utc=STARTED,
            setpoint_c=40.0,
            probe_roles=["air"],
            control={"band_c": 0.25, "min_dwell_s": 60, "max_temp_c": 55.0},
        )
        with open(os.path.join(r.path, "manifest.json")) as fh:
            m = json.load(fh)
        self.assertEqual(m["control"]["band_c"], 0.25)
        self.assertEqual(m["control"]["law"], "hysteresis")
