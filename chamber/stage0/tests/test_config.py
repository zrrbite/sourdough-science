import unittest

from config import load_config

MINIMAL = """
setpoint_c = 40.0

[switch]
on_url = "http://10.0.0.5/relay/0?turn=on"
off_url = "http://10.0.0.5/relay/0?turn=off"

[[probes]]
role = "air"
id = "28-0000063d1f2a"
"""


class TestLoadConfig(unittest.TestCase):
    def test_applies_defaults_for_everything_optional(self):
        c = load_config(MINIMAL)
        self.assertEqual(c["band_c"], 0.25)
        self.assertEqual(c["min_dwell_s"], 60.0)
        self.assertEqual(c["interval_s"], 10.0)
        self.assertEqual(c["control_role"], "air")

    def test_derives_the_sysfs_path_from_the_probe_id(self):
        c = load_config(MINIMAL)
        self.assertEqual(
            c["probes"][0]["device_path"],
            "/sys/bus/w1/devices/28-0000063d1f2a/w1_slave",
        )

    def test_probe_offset_defaults_to_zero(self):
        self.assertEqual(load_config(MINIMAL)["probes"][0]["offset_c"], 0.0)

    def test_rejects_a_config_with_no_probes(self):
        text = MINIMAL.split("[[probes]]")[0]
        with self.assertRaisesRegex(ValueError, "at least one probe"):
            load_config(text)

    def test_rejects_a_control_role_that_has_no_probe(self):
        with self.assertRaisesRegex(ValueError, "control_role"):
            load_config('control_role = "core"\n' + MINIMAL)

    def test_rejects_a_cutout_at_or_below_the_setpoint(self):
        with self.assertRaisesRegex(ValueError, "max_temp_c"):
            load_config("max_temp_c = 40.0\n" + MINIMAL)

    def test_rejects_a_missing_setpoint(self):
        text = MINIMAL.replace("setpoint_c = 40.0", "")
        with self.assertRaisesRegex(ValueError, "setpoint_c"):
            load_config(text)

    def test_rejects_a_setpoint_outside_the_designed_envelope(self):
        text = MINIMAL.replace("setpoint_c = 40.0", "setpoint_c = 70.0")
        with self.assertRaisesRegex(ValueError, "setpoint_c"):
            load_config(text)

    def test_keeps_the_switch_urls(self):
        c = load_config(MINIMAL)
        self.assertEqual(c["switch"]["off_url"], "http://10.0.0.5/relay/0?turn=off")


if __name__ == "__main__":
    unittest.main()


class TestExplicitProbePath(unittest.TestCase):
    def test_an_explicit_path_overrides_the_derived_one(self):
        text = MINIMAL + '\npath = "/tmp/fake/w1_slave"\n'
        self.assertEqual(
            load_config(text)["probes"][0]["device_path"], "/tmp/fake/w1_slave"
        )
