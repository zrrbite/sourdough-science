import unittest

from braille import BLANK, Canvas

ESC = "\x1b"


class TestCanvasGeometry(unittest.TestCase):
    def test_pixel_grid_is_two_by_four_per_character(self):
        c = Canvas(10, 3)
        self.assertEqual((c.width_px, c.height_px), (20, 12))

    def test_an_empty_canvas_is_all_blank_braille(self):
        rows = Canvas(4, 2).rows()
        self.assertEqual(rows, [BLANK * 4, BLANK * 4])


class TestDotMapping(unittest.TestCase):
    """The Unicode braille block numbers dots down the left column then the
    right, with the fourth row appended last - so the mapping is worth pinning."""

    def _one(self, x, y):
        c = Canvas(1, 1)
        c.set(x, y)
        return c.rows()[0]

    def test_top_left_pixel(self):
        self.assertEqual(self._one(0, 0), "⠁")

    def test_top_right_pixel(self):
        self.assertEqual(self._one(1, 0), "⠈")

    def test_bottom_left_pixel(self):
        self.assertEqual(self._one(0, 3), "⡀")

    def test_bottom_right_pixel(self):
        self.assertEqual(self._one(1, 3), "⢀")

    def test_middle_left_pixels(self):
        self.assertEqual(self._one(0, 1), "⠂")
        self.assertEqual(self._one(0, 2), "⠄")

    def test_every_dot_set_is_a_full_cell(self):
        c = Canvas(1, 1)
        for x in range(2):
            for y in range(4):
                c.set(x, y)
        self.assertEqual(c.rows()[0], "⣿")


class TestBounds(unittest.TestCase):
    def test_pixels_outside_the_canvas_are_ignored(self):
        c = Canvas(2, 1)
        for point in [(-1, 0), (0, -1), (4, 0), (0, 4)]:
            c.set(*point)
        self.assertEqual(c.rows(), [BLANK * 2])

    def test_a_pixel_lands_in_the_right_cell(self):
        c = Canvas(3, 1)
        c.set(4, 0)  # third character cell, left column, top row
        self.assertEqual(c.rows()[0], BLANK + BLANK + "⠁")


class TestColour(unittest.TestCase):
    def test_plain_rows_carry_no_escape_codes(self):
        c = Canvas(2, 1)
        c.set(0, 0, colour=(1, 2, 3))
        self.assertNotIn(ESC, c.rows()[0])

    def test_ansi_rows_colour_the_cell(self):
        c = Canvas(2, 1)
        c.set(0, 0, colour=(10, 20, 30))
        self.assertIn(ESC + "[38;2;10;20;30m", c.rows_ansi()[0])

    def test_ansi_rows_reset_at_the_end_of_a_line(self):
        c = Canvas(2, 1)
        c.set(0, 0, colour=(10, 20, 30))
        self.assertTrue(c.rows_ansi()[0].endswith(ESC + "[0m"))

    def test_the_last_write_owns_a_shared_cell(self):
        c = Canvas(1, 1)
        c.set(0, 0, colour=(1, 1, 1))
        c.set(1, 3, colour=(9, 9, 9))
        self.assertIn(ESC + "[38;2;9;9;9m", c.rows_ansi()[0])


if __name__ == "__main__":
    unittest.main()
