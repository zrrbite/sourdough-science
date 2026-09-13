"""The chamber probe's BLE advertisement payload.

Broadcast-only, in the manner of a Tilt hydrometer: the sensor advertises and
anybody may listen. No pairing, no connection, no GATT, any number of listeners
— and, the reason it matters here, **no cable through the chamber seal** to a
probe buried in a dough mass.

Field names match stage 0's probe roles - `air` for the chamber air, `core` for
the dough core - deliberately. Stage 0 already uses `ambient` for the ROOM
temperature outside the box, so a BLE payload calling the chamber air "ambient"
would put two different quantities in one column name across the dataset.

Eight bytes of manufacturer-specific data:

    byte 0   version
    byte 1   sequence, wraps at 256
    2..3     chamber air, int16 big-endian, centidegrees C
    4..5     dough core, int16 big-endian, centidegrees C
    byte 6   battery percent
    byte 7   flags - bit 0 heater on, bit 1 dough probe present

Centidegrees give 0.01 C resolution over a range no kitchen will exceed, which
is finer than a DS18B20 resolves and far finer than one is accurate.
"""

import struct

COMPANY_ID = 0xFFFF  # reserved for testing; never ship a real product on it
VERSION = 0x01
PAYLOAD_LEN = 8

_ABSENT = -32768  # int16 minimum, sentinel for "no reading"
FLAG_HEATING = 0x01
FLAG_DOUGH_PRESENT = 0x02


def _to_centi(celsius):
    if celsius is None:
        return _ABSENT
    return max(-32767, min(32767, int(round(celsius * 100))))


def encode(seq, air_c, core_c, battery_pct=100, heating=False):
    """Build one advertisement payload. `core_c` may be None (probe absent)."""
    flags = 0
    if heating:
        flags |= FLAG_HEATING
    if core_c is not None:
        flags |= FLAG_DOUGH_PRESENT
    return struct.pack(
        ">BBhhBB",
        VERSION,
        seq & 0xFF,
        _to_centi(air_c),
        _to_centi(core_c),
        max(0, min(100, int(battery_pct))),
        flags,
    )


def decode(payload):
    """Decode a payload, or return None if it is not one of ours.

    Returning None rather than raising is deliberate: a BLE scanner sees every
    advertisement in the room, and most of them are somebody else's.
    """
    if payload is None or len(payload) != PAYLOAD_LEN or payload[0] != VERSION:
        return None
    _, seq, air, core, battery, flags = struct.unpack(">BBhhBB", payload)
    return {
        "seq": seq,
        "air_c": None if air == _ABSENT else air / 100.0,
        "core_c": (
            None
            if core == _ABSENT or not (flags & FLAG_DOUGH_PRESENT)
            else core / 100.0
        ),
        "battery_pct": battery,
        "heating": bool(flags & FLAG_HEATING),
    }
