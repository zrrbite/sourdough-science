# Terminal view

The same run, in a terminal, with braille graphs. No dependencies.

    ./top.py                                          # follow the local listener
    ./top.py --once                                   # one frame to stdout
    ./top.py --csv ~/chamber-runs/<run>/samples.csv    # replay a recorded run
    ./top.py --url http://pi.local:8787/telemetry.json

```
DOUGH CORE TRACE  ble-simulated  ·  setpoint 40.0 °C        2026-09-13T12-19Z_ble
────────────────────────────────────────────────────────────────────────────────
▌ chamber air  40.29 °C   ▌ dough core   36.71 °C
  gradient      3.58 °C     heater            off   duty 38%

  41 ┤⠂⠐⠀⠂⠐⠀⠂⠐⢀⠶⠑⠒⠦⠔⠉⠒⠲⠤⠚⠙⠒⠲⠴⠊⠓⠒⠢⠖⠙⠒⠒⠴⠚⠛⠒⠲⠖⠛⠓⠒⠶⠖⠋⠒⠒⠦⠚⠑⠒⠲⠔⠋
     │⠀⠀⠀⠀⠀⠀⠀⢀⠴⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⡤⠤⠤⠖⠒⠒
  35 ┤⠀⠀⠀⢀⡰⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡤⠤⠤⠒⠒⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
     └────────────────────────────────────────────────────────────────────────
      0m                        45m                                      1.5h

lag —  mean core 30.28 °C  peak gap 15.37 °C  run 1h 30m
```

## Why braille

The Unicode braille block encodes eight dots in the low bits of a code point, so one character
is a 2×4 pixel grid. An 80×20 terminal becomes a 160×80 plot — enough to *see* the curve rather
than infer it from a sparkline, which is the only reason a terminal chart is worth drawing.

The cost is that colour is per character, not per dot: where the air and core traces share a
cell, one colour wins. The core is drawn last, so it takes the cell.

## Pieces

| File | What it is |
|---|---|
| `braille.py` | the canvas — pixels in, braille rows out, optionally coloured |
| `chart.py` | scales a series onto a canvas, draws the gutter, axis and reference line |
| `stats.py` | lag to setpoint, time-weighted mean core, peak gradient, duty |
| `screen.py` | one frame as a list of strings |
| `top.py` | the loop: poll, draw, repeat |

`screen.render()` returns strings rather than writing to a terminal, so every layout decision
is testable and `--once` can pipe a frame into anything.

## Sources

It reads the telemetry `chamber/collector/listen.py --serve` publishes and the CSV `chamber/stage0`
records — a third view of one dataset, not a parallel implementation. `stats.py` computes the
same four figures the web viewer does, from the same rows.

## Tests

    python3 -m unittest discover -s tests -t .

51 tests, standard library only. The braille dot mapping is pinned character by character
(the block numbers dots down the left column then the right, with rows 4 appended last, so it
is worth asserting rather than trusting); the chart is checked for axis labels that name values
the data actually reaches, and for not rounding a 90-minute run up to "2h".
