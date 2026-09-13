"""A braille canvas: 2x4 pixels per character cell.

The Unicode braille block (U+2800-U+28FF) encodes eight dots in the low eight
bits of the code point, which makes a terminal character into a 2x4 pixel grid -
so an 80x20 terminal is a 160x80 plot. That is enough resolution to see a curve
rather than infer one, which is the whole reason to draw in the terminal at all.

The dot numbering is historical, not raster order: dots 1-3 run down the left
column, 4-6 down the right, and 7-8 were appended underneath when the block was
extended from six dots to eight. Hence the bit table below rather than a formula.
"""

BLANK = "⠀"
RESET = "\x1b[0m"

# (column, row) -> bit. Left column top-to-bottom is dots 1,2,3,7; right is 4,5,6,8.
_BITS = {
    (0, 0): 0x01, (1, 0): 0x08,
    (0, 1): 0x02, (1, 1): 0x10,
    (0, 2): 0x04, (1, 2): 0x20,
    (0, 3): 0x40, (1, 3): 0x80,
}


class Canvas:
    """A grid of braille cells addressed in pixels.

    A cell carries one colour: braille gives sub-character resolution but not
    sub-character colour, so where two series share a cell the last write owns
    it. Draw the series you care most about last.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._bits = [[0] * width for _ in range(height)]
        self._colour = [[None] * width for _ in range(height)]

    @property
    def width_px(self):
        return self.width * 2

    @property
    def height_px(self):
        return self.height * 4

    def set(self, x, y, colour=None):
        """Light the pixel at (x, y). Out-of-range points are dropped silently,
        which keeps every caller from having to clip its own data."""
        if not (0 <= x < self.width_px and 0 <= y < self.height_px):
            return
        col, row = int(x) // 2, int(y) // 4
        self._bits[row][col] |= _BITS[(int(x) % 2, int(y) % 4)]
        if colour is not None:
            self._colour[row][col] = colour

    def rows(self):
        """Plain text, no escape codes."""
        return ["".join(chr(0x2800 + bits) for bits in row) for row in self._bits]

    def rows_ansi(self):
        """Truecolor text, emitting an escape only where the colour changes."""
        out = []
        for bits_row, colour_row in zip(self._bits, self._colour):
            parts, current = [], None
            for bits, colour in zip(bits_row, colour_row):
                if colour != current:
                    parts.append(RESET if colour is None else _fg(colour))
                    current = colour
                parts.append(chr(0x2800 + bits))
            parts.append(RESET)
            out.append("".join(parts))
        return out


def _fg(colour):
    return "\x1b[38;2;{};{};{}m".format(*colour)
