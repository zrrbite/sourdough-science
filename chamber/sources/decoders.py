"""Turning whatever a device emits into a reading.

The transport says how bytes arrive; a decoder says what they mean. Keeping
them apart is what makes an Inkbird a decoder swap rather than a rewrite - it
broadcasts BLE advertisements exactly as our own probe does, just with somebody
else's bytes inside.
"""

import json

from protocol import decode as _decode_chamber

# Field names accepted on a text line. `ambient` is deliberately absent: it
# means the ROOM elsewhere in this project, and accepting it as chamber air
# would put two different quantities under one column name.
_LINE_FIELDS = {
    "air": "air_c", "air_c": "air_c",
    "core": "core_c", "core_c": "core_c", "dough": "core_c",
    "heating": "heating", "heater": "heating",
    "setpoint": "setpoint_c", "setpoint_c": "setpoint_c",
    "battery": "battery_pct", "battery_pct": "battery_pct",
    "seq": "seq",
}


def decode_chamber(payload):
    """Our own 8-byte advertisement."""
    return _decode_chamber(payload)


def decode_inkbird(payload):
    """Not implemented, on purpose.

    An Inkbird IBS-TH broadcasts temperature in manufacturer data, so it fits
    this seam exactly - but its byte layout has not been observed here, and a
    guessed wire format silently produces confident wrong numbers, which is the
    worst failure this project could have. Capture real advertisements with
    `collector/listen.py --scan-raw`, then write this from the evidence.
    """
    return None


decode_inkbird.unimplemented_because = (
    "payload layout unverified - capture real advertisements with --scan-raw first"
)


def decode_line(line):
    """A text line from a USB serial device.

    Two accepted shapes, both deliberately trivial so that ten lines of Arduino
    sketch can feed the whole system:

        air=40.29,core=36.71,heating=1
        {"air_c": 40.29, "core_c": 36.71, "heating": true}
    """
    text = (line or "").strip()
    if not text:
        return None

    if text.startswith("{"):
        try:
            raw = json.loads(text)
        except ValueError:
            return None
        fields = {_LINE_FIELDS[k]: v for k, v in raw.items() if k in _LINE_FIELDS}
    else:
        fields = {}
        for pair in text.split(","):
            if "=" not in pair:
                continue
            key, _, value = pair.partition("=")
            key = key.strip().lower()
            if key in _LINE_FIELDS:
                fields[_LINE_FIELDS[key]] = value.strip()

    if "air_c" not in fields and "core_c" not in fields:
        return None

    return {
        "air_c": _number(fields.get("air_c")),
        "core_c": _number(fields.get("core_c")),
        "heating": _flag(fields.get("heating")),
        "setpoint_c": _number(fields.get("setpoint_c")),
        "battery_pct": _number(fields.get("battery_pct")),
        "seq": _number(fields.get("seq")),
    }


def _number(value):
    if value is None or value is False or value is True:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _flag(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in ("1", "true", "on", "yes")


DECODERS = {
    "chamber": decode_chamber,
    "inkbird": decode_inkbird,
    "line": decode_line,
}
