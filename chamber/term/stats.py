"""The four figures chapter 10 asks for, computed from a sample series.

The same arithmetic the web viewer does, kept here so the terminal app does not
depend on a browser having been open. Samples are the compact rows the telemetry
series carries: [t_s, air_c, core_c, heating].
"""


def summarise(samples, setpoint):
    """Lag to setpoint, time-weighted mean core, peak gradient, duty, total."""
    lag = None
    peak_gap = None
    peak_gap_at = None
    weighted = 0.0
    weighted_span = 0.0
    heating_span = 0.0
    total = 0.0

    previous_t = None
    for row in samples:
        t, air, core = row[0], row[1], row[2]
        heating = row[3] if len(row) > 3 else 0
        span = 0.0 if previous_t is None else t - previous_t
        previous_t = t
        total += span
        if heating:
            heating_span += span

        if core is not None:
            weighted += core * span
            weighted_span += span
            if lag is None and core >= setpoint - 0.5:
                lag = t
        if core is not None and air is not None:
            gap = air - core
            if peak_gap is None or gap > peak_gap:
                peak_gap, peak_gap_at = gap, t

    return {
        "lag_s": lag,
        # weighted_span excludes the first sample's zero span, so a run with a
        # single reading still reports that reading rather than dividing by zero
        "mean_core": (weighted / weighted_span) if weighted_span else _first_core(samples),
        "peak_gap": peak_gap,
        "peak_gap_at": peak_gap_at,
        "duty": (heating_span / total) if total else 0.0,
        "total_s": total,
    }


def _first_core(samples):
    for row in samples:
        if row[2] is not None:
            return row[2]
    return None


def clock(seconds):
    """`2h 50m`, the format the figures are read in."""
    if seconds is None:
        return "—"
    hours = int(seconds // 3600)
    minutes = int(round((seconds % 3600) / 60))
    if minutes == 60:
        hours, minutes = hours + 1, 0
    return "{}h {:02d}m".format(hours, minutes)
