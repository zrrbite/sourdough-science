import unittest

from protocol import COMPANY_ID, VERSION, decode, encode


class TestEncodeDecodeRoundtrip(unittest.TestCase):
    def test_carries_both_temperatures(self):
        r = decode(encode(seq=7, air_c=21.5, core_c=33.25))
        self.assertAlmostEqual(r["air_c"], 21.5)
        self.assertAlmostEqual(r["core_c"], 33.25)

    def test_resolution_is_a_hundredth_of_a_degree(self):
        r = decode(encode(seq=0, air_c=44.44, core_c=38.07))
        self.assertAlmostEqual(r["air_c"], 44.44)
        self.assertAlmostEqual(r["core_c"], 38.07)

    def test_carries_negative_temperatures(self):
        r = decode(encode(seq=0, air_c=-4.5, core_c=3.0))
        self.assertAlmostEqual(r["air_c"], -4.5)

    def test_carries_sequence_battery_and_heater_state(self):
        r = decode(encode(seq=42, air_c=20.0, core_c=20.0,
                          battery_pct=88, heating=True))
        self.assertEqual(r["seq"], 42)
        self.assertEqual(r["battery_pct"], 88)
        self.assertTrue(r["heating"])

    def test_payload_is_eight_bytes(self):
        self.assertEqual(len(encode(seq=0, air_c=20.0, core_c=20.0)), 8)


class TestAbsentDoughProbe(unittest.TestCase):
    def test_absent_dough_probe_decodes_as_none(self):
        r = decode(encode(seq=1, air_c=40.0, core_c=None))
        self.assertIsNone(r["core_c"])

    def test_air_still_readable_without_a_dough_probe(self):
        r = decode(encode(seq=1, air_c=40.0, core_c=None))
        self.assertAlmostEqual(r["air_c"], 40.0)


class TestRejectsBadPayloads(unittest.TestCase):
    def test_rejects_a_short_payload(self):
        self.assertIsNone(decode(b"\x01\x00\x00"))

    def test_rejects_an_unknown_version(self):
        bad = bytes([0x7F]) + encode(seq=0, air_c=20.0, core_c=20.0)[1:]
        self.assertIsNone(decode(bad))

    def test_rejects_an_empty_payload(self):
        self.assertIsNone(decode(b""))


class TestAdvertisementShape(unittest.TestCase):
    def test_uses_the_reserved_for_testing_company_id(self):
        self.assertEqual(COMPANY_ID, 0xFFFF)

    def test_version_is_carried_in_the_first_byte(self):
        self.assertEqual(encode(seq=0, air_c=20.0, core_c=20.0)[0], VERSION)


if __name__ == "__main__":
    unittest.main()
