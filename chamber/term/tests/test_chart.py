import unittest

from chart import render

AIR = (42, 120, 214)
CORE = (235, 104, 52)


def ramp(n=40, start=20.0, end=40.0):
    return [(i, start + (end - start) * i / (n - 1)) for i in range(n)]


def series(points, colour=AIR, label="air"):
    return [{"points": points, "colour": colour, "label": label}]


class TestShape(unittest.TestCase):
    def test_line_count_is_the_plot_plus_an_axis_and_a_label_row(self):
        lines = render(series(ramp()), width=40, height=8, ansi=False)
        self.assertEqual(len(lines), 10)

    def test_every_line_is_the_same_width(self):
        lines = render(series(ramp()), width=40, height=8, ansi=False)
        self.assertEqual(len({len(line) for line in lines}), 1)

    def test_an_empty_series_still_renders_a_frame(self):
        lines = render([], width=30, height=6, ansi=False)
        self.assertEqual(len(lines), 8)


class TestAxes(unittest.TestCase):
    def test_the_y_axis_labels_span_the_data(self):
        text = "\n".join(render(series(ramp(start=20.0, end=40.0)),
                                width=40, height=8, ansi=False))
        self.assertIn("40", text)
        self.assertIn("20", text)

    def test_the_x_axis_carries_elapsed_labels(self):
        lines = render(series([(i * 600.0, 30.0) for i in range(20)]),
                       width=50, height=6, ansi=False, x_is_seconds=True)
        self.assertIn("h", lines[-1])

    def test_an_explicit_y_range_is_honoured(self):
        text = "\n".join(render(series(ramp()), width=40, height=8,
                                ansi=False, y_min=0.0, y_max=100.0))
        self.assertIn("100", text)


class TestPlotting(unittest.TestCase):
    def test_a_flat_series_draws_ink(self):
        lines = render(series([(i, 30.0) for i in range(40)]),
                       width=40, height=8, ansi=False)
        body = "".join(lines[:8])
        self.assertTrue(any(ch not in " ⠀│┤└─0123456789." for ch in body))

    def test_a_rising_series_ends_higher_than_it_starts(self):
        lines = render(series(ramp()), width=40, height=8, ansi=False)
        rows_with_ink = [i for i, line in enumerate(lines[:8]) if _has_dots(line)]
        first, last = _ink_columns(lines, rows_with_ink)
        self.assertGreater(first, last)  # row index falls as value rises

    def test_two_series_both_appear(self):
        lines = render(
            [{"points": ramp(end=40.0), "colour": AIR, "label": "air"},
             {"points": ramp(end=30.0), "colour": CORE, "label": "core"}],
            width=40, height=8, ansi=False)
        self.assertGreaterEqual(sum(1 for line in lines[:8] if _has_dots(line)), 3)


class TestReferenceLine(unittest.TestCase):
    def test_a_reference_line_is_drawn_and_labelled(self):
        lines = render(series(ramp()), width=40, height=8, ansi=False,
                       reference={"y": 40.0, "label": "setpoint"})
        self.assertIn("setpoint", "\n".join(lines))


class TestColour(unittest.TestCase):
    def test_ansi_output_carries_the_series_colour(self):
        text = "\n".join(render(series(ramp()), width=40, height=8, ansi=True))
        self.assertIn("[38;2;42;120;214m", text)

    def test_plain_output_carries_no_escapes(self):
        text = "\n".join(render(series(ramp()), width=40, height=8, ansi=False))
        self.assertNotIn("\x1b", text)


def _has_dots(line):
    return any(0x2801 <= ord(ch) <= 0x28FF for ch in line)


def _ink_columns(lines, rows):
    """Row index of the leftmost and rightmost ink, to check slope direction."""
    left = right = None
    for row in rows:
        for col, ch in enumerate(lines[row]):
            if 0x2801 <= ord(ch) <= 0x28FF:
                if left is None or col < left[1]:
                    left = (row, col)
                if right is None or col > right[1]:
                    right = (row, col)
    return left[0], right[0]


if __name__ == "__main__":
    unittest.main()


class TestElapsedLabels(unittest.TestCase):
    def test_a_ninety_minute_run_is_not_rounded_to_two_hours(self):
        lines = render(series([(i * 60.0, 30.0) for i in range(91)]),
                       width=60, height=6, ansi=False, x_is_seconds=True)
        self.assertIn("1.5h", lines[-1])
        self.assertNotIn("2h", lines[-1])

    def test_a_whole_hour_stays_whole(self):
        lines = render(series([(i * 60.0, 30.0) for i in range(121)]),
                       width=60, height=6, ansi=False, x_is_seconds=True)
        self.assertIn("2h", lines[-1])

    def test_a_short_run_is_labelled_in_minutes(self):
        lines = render(series([(i * 60.0, 30.0) for i in range(31)]),
                       width=60, height=6, ansi=False, x_is_seconds=True)
        self.assertIn("30m", lines[-1])
