"""Shaping a stream of probe readings into the two documents the UI reads.

The artifact store holds at most 5,000 documents and explicitly warns against
mapping an unbounded stream to one document per item. A run at 10 s intervals
would blow that inside fourteen hours, so telemetry aggregates into exactly two
fixed documents that are overwritten rather than accumulated:

    telemetry/current   the latest reading, for the readout tiles
    telemetry/series    a rolling window of recent samples, for the chart

Series rows are compact arrays rather than objects - [t_s, air, core,
heating] - because the field names would otherwise be repeated on every row and
the document has a 256 KiB ceiling.
"""

from collections import deque

SCHEMA_VERSION = 1
SERIES_CAP = 720  # 2 h at 10 s, or 4 h at 20 s


class TelemetryBuffer:
    def __init__(self, run_id, setpoint_c=None, source="ble"):
        self.run_id = run_id
        self.setpoint_c = setpoint_c
        self.source = source
        self.samples = deque(maxlen=SERIES_CAP)
        self.latest = None

    def add(self, reading):
        self.latest = reading
        if self.setpoint_c is None:
            self.setpoint_c = reading.get("setpoint_c")
        self.samples.append([
            round(reading["t_s"], 1),
            _round(reading.get("air_c")),
            _round(reading.get("core_c")),
            1 if reading.get("heating") else 0,
        ])

    def documents(self):
        """The two document bodies, ready to write to the store."""
        r = self.latest or {}
        current = {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "source": self.source,
            "stale": self.latest is None,
            "seq": r.get("seq"),
            "t_s": r.get("t_s"),
            "air_c": _round(r.get("air_c")),
            "core_c": _round(r.get("core_c")),
            "setpoint_c": self.setpoint_c,
            "heating": bool(r.get("heating")),
            "battery_pct": r.get("battery_pct"),
        }
        series = {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "setpoint_c": self.setpoint_c,
            "columns": ["t_s", "air_c", "core_c", "heating"],
            "samples": list(self.samples),
        }
        return {"current": current, "series": series}


def _round(value):
    return None if value is None else round(value, 2)
