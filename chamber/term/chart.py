"""Line charts drawn in braille, with a labelled gutter and an x axis.

Returns a list of strings, so the caller decides where they go and the whole
thing is testable without a terminal.

Layout, per call:

      45 ┤<--------------- braille canvas ---------------->
         │
      25 ┤
         └───────────────────────────────────────────────
          0h                1h                2h
"""

from braille import BLANK, RESET, Canvas, _fg

GUTTER = 6           # "  45 ┤"
MUTED = (133, 141, 139)


def render(series, width, height, ansi=True, y_min=None, y_max=None,
           reference=None, x_is_seconds=False):
    """Draw `series` into `width` x `height` characters, plus two axis rows.

    Each series is {"points": [(x, y)], "colour": (r, g, b), "label": str}.
    Points whose y is None are treated as gaps, not zeros.
    """
    plot_w = max(1, width - GUTTER)
    canvas = Canvas(plot_w, height)

    points = [p for s in series for p in s["points"] if p[1] is not None]
    if points:
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        x_lo, x_hi = min(xs), max(xs)
        lo = y_min if y_min is not None else min(ys)
        hi = y_max if y_max is not None else max(ys)
        if reference is not None and y_min is None and y_max is None:
            lo, hi = min(lo, reference["y"]), max(hi, reference["y"])
        if hi == lo:
            lo, hi = lo - 1.0, hi + 1.0
    else:
        x_lo, x_hi = 0.0, 1.0
        lo, hi = (y_min, y_max) if y_min is not None and y_max is not None else (0.0, 1.0)

    to_px_x = _mapper(x_lo, x_hi, canvas.width_px - 1)
    to_px_y = _mapper(lo, hi, canvas.height_px - 1, invert=True)

    if reference is not None:
        ry = to_px_y(reference["y"])
        for px in range(0, canvas.width_px, 3):   # dashed, so a series reads over it
            canvas.set(px, ry, MUTED)

    for s in series:                               # last series owns a shared cell
        _draw(canvas, s["points"], to_px_x, to_px_y, s["colour"])

    rows = canvas.rows_ansi() if ansi else canvas.rows()
    labels = _y_labels(lo, hi, height)
    out = [labels[i] + rows[i] for i in range(height)]
    out.append(" " * (GUTTER - 1) + "└" + "─" * plot_w)
    out.append(_x_labels(x_lo, x_hi, plot_w, x_is_seconds))

    if reference is not None:
        out[_row_of(to_px_y(reference["y"]))] += _tag(reference["label"], ansi, MUTED)
    return _pad_lines(out)


def _draw(canvas, points, to_px_x, to_px_y, colour):
    previous = None
    for x, y in points:
        if y is None:
            previous = None
            continue
        current = (to_px_x(x), to_px_y(y))
        if previous is not None:
            _line(canvas, previous, current, colour)
        else:
            canvas.set(current[0], current[1], colour)
        previous = current


def _line(canvas, a, b, colour):
    """Bresenham, so a steep segment is a line rather than a column of gaps."""
    x0, y0 = a
    x1, y1 = b
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        canvas.set(x0, y0, colour)
        if x0 == x1 and y0 == y1:
            return
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def _mapper(lo, hi, span, invert=False):
    if hi == lo:
        return lambda _value: span // 2
    def to_px(value):
        t = (value - lo) / (hi - lo)
        return int(round((1 - t) * span if invert else t * span))
    return to_px


def _y_labels(lo, hi, height, ticks=4):
    """Labels at evenly spaced rows, always including the top and bottom.

    Both ends are labelled on purpose: the axis is not padded beyond the data,
    so the first and last labels name values the chart actually reaches.
    """
    span = max(1, height - 1)
    rows = {round(i * span / max(1, ticks - 1)) for i in range(ticks)}
    rows |= {0, span}
    out = []
    for row in range(height):
        if row in rows:
            value = hi - (hi - lo) * (row / span)
            out.append("{:>4.0f} ┤".format(value))
        else:
            out.append(" " * (GUTTER - 1) + "│")
    return out


def _x_labels(x_lo, x_hi, plot_w, x_is_seconds):
    line = [" "] * (GUTTER + plot_w)
    for fraction in (0.0, 0.5, 1.0):
        value = x_lo + (x_hi - x_lo) * fraction
        text = _clock(value) if x_is_seconds else "{:g}".format(value)
        start = GUTTER + int(fraction * (plot_w - 1)) - (len(text) if fraction == 1.0 else 0)
        start = max(0, min(len(line) - len(text), start))
        line[start:start + len(text)] = list(text)
    return "".join(line)


def _clock(seconds):
    """Elapsed time, never rounded past the run: a 90 minute run reads 1.5h."""
    if seconds < 3600:
        return "{:.0f}m".format(seconds / 60)
    hours = seconds / 3600.0
    if abs(hours - round(hours)) < 0.05:
        return "{:.0f}h".format(hours)
    return "{:.1f}h".format(hours)


def _row_of(pixel_y):
    return pixel_y // 4


def _tag(label, ansi, colour):
    return (" " + _fg(colour) + label + RESET) if ansi else " " + label


def _pad_lines(lines):
    """Equal visible width, so the block sits square in a terminal."""
    widths = [_visible(line) for line in lines]
    target = max(widths)
    return [line + " " * (target - w) for line, w in zip(lines, widths)]


def _visible(line):
    out, i = 0, 0
    while i < len(line):
        if line[i] == "\x1b":
            i = line.find("m", i) + 1
            continue
        out += 1
        i += 1
    return out


__all__ = ["render", "BLANK"]
