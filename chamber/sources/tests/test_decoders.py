import unittest

from decoders import DECODERS, decode_chamber, decode_inkbird, decode_line
from protocol import encode


class TestChamberDecoder(unittest.TestCase):
    def test_it_decodes_our_own_payload(self):
        r = decode_chamber(encode(seq=3, air_c=40.25, core_c=36.5, heating=True))
        self.assertAlmostEqual(r["air_c"], 40.25)
        self.assertAlmostEqual(r["core_c"], 36.5)
        self.assertTrue(r["heating"])

    def test_it_ignores_somebody_elses_advertisement(self):
        self.assertIsNone(decode_chamber(b"\x99\x01\x02\x03"))


class TestInkbirdDecoder(unittest.TestCase):
    """Deliberately unimplemented: the payload layout has not been observed,
    and guessing a third party's wire format would be worse than nothing."""

    def test_it_decodes_nothing_until_a_real_payload_has_been_captured(self):
        self.assertIsNone(decode_inkbird(b"\x01\x02\x03\x04\x05\x06\x07"))

    def test_it_says_why_rather_than_failing_silently(self):
        self.assertIn("capture", decode_inkbird.unimplemented_because.lower())


class TestLineDecoder(unittest.TestCase):
    def test_it_reads_key_value_pairs(self):
        r = decode_line("air=40.29,core=36.71,heating=1")
        self.assertAlmostEqual(r["air_c"], 40.29)
        self.assertAlmostEqual(r["core_c"], 36.71)
        self.assertTrue(r["heating"])

    def test_it_reads_a_json_line(self):
        r = decode_line('{"air_c": 40.29, "core_c": 36.71, "heating": true}')
        self.assertAlmostEqual(r["air_c"], 40.29)
        self.assertTrue(r["heating"])

    def test_a_missing_core_reading_is_none_not_zero(self):
        self.assertIsNone(decode_line("air=40.29")["core_c"])

    def test_it_tolerates_spaces_and_trailing_commas(self):
        r = decode_line("  air = 40.29 , core = 36.71 ,  ")
        self.assertAlmostEqual(r["core_c"], 36.71)

    def test_unknown_keys_are_ignored_rather_than_fatal(self):
        r = decode_line("air=40.0,humidity=71,core=30.0")
        self.assertAlmostEqual(r["air_c"], 40.0)

    def test_a_line_with_no_recognised_field_is_rejected(self):
        self.assertIsNone(decode_line("hello there"))

    def test_an_empty_line_is_rejected(self):
        self.assertIsNone(decode_line("   "))

    def test_it_rejects_ambient_as_a_name_for_chamber_air(self):
        """`ambient` means the room elsewhere in this project. Accepting it here
        would put two quantities under one column name."""
        self.assertIsNone(decode_line("ambient=40.29"))


class TestRegistry(unittest.TestCase):
    def test_the_named_decoders_are_registered(self):
        self.assertIn("chamber", DECODERS)
        self.assertIn("inkbird", DECODERS)

    def test_a_registered_decoder_is_callable(self):
        self.assertTrue(callable(DECODERS["chamber"]))


if __name__ == "__main__":
    unittest.main()
