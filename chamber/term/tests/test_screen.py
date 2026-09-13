import unittest

from screen import render

DOCS = {
    "current": {
        "run_id": "2026-09-13T12-07-32Z_ble",
        "source": "ble-simulated",
        "stale": False,
        "t_s": 5400.0,
        "air_c": 40.29,
        "core_c": 36.71,
        "setpoint_c": 40.0,
        "heating": False,
        "battery_pct": 97,
    },
    "series": {
        "setpoint_c": 40.0,
        "columns": ["t_s", "air_c", "core_c", "heating"],
        "samples": [[i * 20.0, 21.5 + i * 0.07, 21.5 + i * 0.056, 1] for i in range(270)],
    },
}


def plain(docs=DOCS, width=80, height=24, status="polling"):
    return render(docs, width=width, height=height, ansi=False, status=status)


class TestFrame(unittest.TestCase):
    def test_it_fills_no_more_than_the_given_height(self):
        self.assertLessEqual(len(plain(height=24)), 24)

    def test_no_line_exceeds_the_given_width(self):
        self.assertTrue(all(len(line) <= 80 for line in plain(width=80)))

    def test_it_works_in_a_small_terminal(self):
        lines = plain(width=48, height=14)
        self.assertTrue(all(len(line) <= 48 for line in lines))
        self.assertLessEqual(len(lines), 14)


class TestContent(unittest.TestCase):
    def test_it_shows_both_temperatures(self):
        text = "\n".join(plain())
        self.assertIn("40.29", text)
        self.assertIn("36.71", text)

    def test_it_shows_the_gradient_between_them(self):
        self.assertIn("3.58", "\n".join(plain()))

    def test_it_names_the_run(self):
        self.assertIn("2026-09-13T12-07-32Z_ble", "\n".join(plain()))

    def test_it_shows_the_heater_state(self):
        self.assertIn("off", "\n".join(plain()))

    def test_it_draws_a_chart(self):
        text = "\n".join(plain())
        self.assertTrue(any(0x2801 <= ord(ch) <= 0x28FF for ch in text))

    def test_it_carries_the_status_line(self):
        self.assertIn("polling", "\n".join(plain(status="polling 127.0.0.1:8787")))


class TestDegraded(unittest.TestCase):
    def test_it_renders_before_any_telemetry_arrives(self):
        docs = {"current": {"stale": True}, "series": {"samples": []}}
        lines = render(docs, width=80, height=24, ansi=False, status="waiting")
        self.assertTrue(any("waiting" in line for line in lines))

    def test_it_renders_with_no_core_probe(self):
        docs = {
            "current": dict(DOCS["current"], core_c=None),
            "series": {"setpoint_c": 40.0,
                       "samples": [[i * 20.0, 30.0, None, 1] for i in range(20)]},
        }
        text = "\n".join(render(docs, width=80, height=24, ansi=False, status=""))
        self.assertIn("40.29", text)


class TestColour(unittest.TestCase):
    def test_ansi_output_carries_escapes(self):
        self.assertIn("\x1b[", "\n".join(render(DOCS, width=80, height=24, ansi=True)))

    def test_plain_output_carries_none(self):
        self.assertNotIn("\x1b", "\n".join(plain()))


class TestSetpoint(unittest.TestCase):
    def test_the_header_names_the_setpoint(self):
        self.assertIn("setpoint 40.0", "\n".join(plain()))


if __name__ == "__main__":
    unittest.main()

