import os
import tempfile
import unittest

from probes import Probe, parse_w1_slave

GOOD = (
    "d8 01 4b 46 7f ff 0c 10 2e : crc=2e YES\n"
    "d8 01 4b 46 7f ff 0c 10 2e t=29500\n"
)
BAD_CRC = (
    "d8 01 4b 46 7f ff 0c 10 2e : crc=2e NO\n"
    "d8 01 4b 46 7f ff 0c 10 2e t=29500\n"
)


class TestParseW1Slave(unittest.TestCase):
    def test_reads_degrees_from_millidegrees(self):
        self.assertAlmostEqual(parse_w1_slave(GOOD), 29.5)

    def test_rejects_a_failed_crc(self):
        self.assertIsNone(parse_w1_slave(BAD_CRC))

    def test_rejects_output_without_a_temperature(self):
        self.assertIsNone(parse_w1_slave("nonsense\n"))


class TestProbe(unittest.TestCase):
    def _device_file(self, text):
        d = tempfile.mkdtemp()
        path = os.path.join(d, "w1_slave")
        with open(path, "w") as fh:
            fh.write(text)
        return path

    def test_applies_the_calibration_offset(self):
        p = Probe(role="core", device_path=self._device_file(GOOD), offset_c=-0.25)
        self.assertAlmostEqual(p.read(), 29.25)

    def test_keeps_the_raw_value_alongside_the_corrected_one(self):
        p = Probe(role="core", device_path=self._device_file(GOOD), offset_c=-0.25)
        p.read()
        self.assertAlmostEqual(p.raw_c, 29.5)

    def test_rejects_an_implausible_reading(self):
        power_on_reset = GOOD.replace("t=29500", "t=85000")
        p = Probe(role="air", device_path=self._device_file(power_on_reset))
        self.assertIsNone(p.read())

    def test_returns_none_when_the_device_has_gone_away(self):
        p = Probe(role="air", device_path="/nonexistent/w1_slave")
        self.assertIsNone(p.read())


if __name__ == "__main__":
    unittest.main()
