"""One frame of the terminal UI, as a list of strings.

Returning strings rather than writing to a terminal keeps the whole layout
testable, and lets the caller decide between a live loop and a one-shot dump.

Colours match the web viewer so the two read as one system: air blue, core
orange, everything else in the terminal's own ink.
"""

from chart import render as chart
from stats import clock, summarise

AIR = (42, 120, 214)
CORE = (235, 104, 52)
MUTED = (133, 141, 139)
RESET = "\x1b[0m"
BOLD = "\x1b[1m"

# header, rule, two readouts, blank, the chart's own axis rows, blank, figures,
# status. Counted rather than guessed: the status line is the one that falls off
# the bottom when this is wrong.
CHROME_ROWS = 10


def render(docs, width, height, ansi=True, status=""):
    current = (docs or {}).get("current") or {}
    series_doc = (docs or {}).get("series") or {}
    samples = series_doc.get("samples") or []
    setpoint = current.get("setpoint_c") or series_doc.get("setpoint_c") or 40.0

    paint, raw = _painters(ansi)
    figures = summarise(samples, setpoint)
    lines = []

    run_id = current.get("run_id", "—")
    source = current.get("source", "")
    lines.append(_row(width,
                      raw(BOLD + "DOUGH CORE TRACE" + RESET) +
                      paint(MUTED, "  " + source if source else "") +
                      paint(MUTED, "  ·  setpoint {:.1f} °C".format(setpoint)),
                      paint(MUTED, run_id)))
    lines.append(paint(MUTED, "─" * width))

    air = current.get("air_c")
    core = current.get("core_c")
    gap = (air - core) if (air is not None and core is not None) else None
    lines.append(_row(width,
                      _pair(paint, "chamber air", _deg(air), AIR) + "   " +
                      _pair(paint, "dough core", _deg(core), CORE)))
    lines.append(_row(width,
                      _pair(paint, "gradient", _deg(gap), None) + "   " +
                      _pair(paint, "heater",
                            "ON " if current.get("heating") else "off", None) +
                      paint(MUTED, "   duty {:.0f}%".format(figures["duty"] * 100))))
    lines.append("")

    plot_height = max(3, height - CHROME_ROWS)
    if samples:
        lines.extend(chart(
            [{"points": [(r[0], r[1]) for r in samples], "colour": AIR, "label": "air"},
             {"points": [(r[0], r[2]) for r in samples], "colour": CORE, "label": "core"}],
            width=width, height=plot_height, ansi=ansi,
            reference={"y": setpoint, "label": "setpoint"}, x_is_seconds=True))
    else:
        lines.extend([""] * (plot_height + 1))
        lines.append(paint(MUTED, "  no telemetry yet"))

    lines.append("")
    lines.append(_row(width, paint(MUTED, "  ".join([
        "lag " + clock(figures["lag_s"]),
        "mean core " + _deg(figures["mean_core"]),
        "peak gap " + _deg(figures["peak_gap"]),
        "run " + clock(figures["total_s"]),
    ]))))
    if status:
        lines.append(_row(width, paint(MUTED, status)))

    return [_clip(line, width) for line in lines[:height]]


def _painters(ansi):
    """`paint(colour, text)` colours text; `raw(text)` passes escapes through."""
    def paint(colour, text):
        if not ansi or colour is None:
            return text
        return "\x1b[38;2;{};{};{}m{}{}".format(*colour, text, RESET)

    def raw(text):
        return text if ansi else _strip(text)

    return paint, raw


def _pair(paint, label, value, colour):
    swatch = paint(colour, "▌") if colour else " "
    return "{} {} {}".format(swatch, paint(MUTED, label.ljust(11)), value.rjust(9))


def _deg(value):
    return "—" if value is None else "{:.2f} °C".format(value)


def _row(width, left, right=""):
    pad = width - _visible(left) - _visible(right)
    return left + " " * max(1, pad) + right if right else left


def _clip(line, width):
    if _visible(line) <= width:
        return line
    out, seen, i = [], 0, 0
    while i < len(line) and seen < width:
        if line[i] == "\x1b":
            end = line.find("m", i) + 1
            out.append(line[i:end])
            i = end
            continue
        out.append(line[i])
        seen += 1
        i += 1
    return "".join(out) + (RESET if "\x1b" in line else "")


def _visible(line):
    out, i = 0, 0
    while i < len(line):
        if line[i] == "\x1b":
            i = line.find("m", i) + 1
            continue
        out += 1
        i += 1
    return out


def _strip(line):
    out, i = [], 0
    while i < len(line):
        if line[i] == "\x1b":
            i = line.find("m", i) + 1
            continue
        out.append(line[i])
        i += 1
    return "".join(out)
