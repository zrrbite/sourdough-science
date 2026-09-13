# BLE probe — protocol, simulator, listener

A broadcast-only Bluetooth probe for the chamber, and the listener that turns its
advertisements into the telemetry the viewer reads. **Simulated end to end** — there is no
hardware yet, and none is needed to run any of this.

## Why broadcast, not GATT

The same shape as a Tilt hydrometer: the probe advertises, anybody listens. No pairing, no
connection, no reconnection logic, any number of listeners at once.

The reason it matters for this project is physical. Stage 0 runs DS18B20 probes on wires, so
the dough-core probe needs a cable passing through the chamber seal — which is a humidity
leak, a condensation path down the cable, and a thing to snag every time the tub comes out.
A broadcast probe sitting in the dough removes all three.

## The payload

Eight bytes of manufacturer-specific data under company ID `0xFFFF` (reserved for testing —
never ship a product on it):

| byte | field |
|---|---|
| 0 | version |
| 1 | sequence, wraps at 256 |
| 2–3 | chamber air, int16 big-endian, centidegrees C |
| 4–5 | dough core, int16 big-endian, centidegrees C |
| 6 | battery percent |
| 7 | flags — bit 0 heater on, bit 1 dough probe present |

Centidegrees give 0.01 °C resolution, finer than a DS18B20 resolves and far finer than one is
accurate. `-32768` is the absent-reading sentinel, so a probe with no dough sensor attached
still reports air.

**Field names match stage 0's probe roles — `air` and `core` — deliberately.** Stage 0 already
uses `ambient` for the *room* temperature outside the box, so a payload calling the chamber
air "ambient" would put two different quantities under one column name across the dataset.

## Running it

    ./listen.py --simulate --speed 120 --limit 270   # 90 min of run in a few seconds
    ./listen.py --simulate                           # real time
    ./listen.py --simulate --record ~/chamber-runs   # also write a CSV + manifest
    ./listen.py                                      # real BLE scan (needs bleak)

The simulator is not arbitrary curves. It runs the chamber's own lumped thermal model and the
same hysteresis law `stage0/controller.py` uses, with the constants from the design spec —
UA 0.63 W/K, a 55 W emitter, dough τ 48 minutes. So the simulated run shows the real thermal
lag, not a decorative wiggle.

Simulated readings are **round-tripped through the actual advertisement encoding** before use,
so the simulated path and the radio path decode through identical code.

## Output

`telemetry.json` holds the two document bodies the viewer subscribes to:

    telemetry/current   latest reading, for the readout tiles
    telemetry/series    rolling window of recent samples, for the chart

Two fixed documents, overwritten rather than accumulated. The artifact store holds at most
5,000 documents and explicitly warns against one document per item for a growing stream — a
run at 10 s intervals would exhaust that inside fourteen hours. Series rows are compact arrays
(`[t_s, air_c, core_c, heating]`) rather than objects, because field names repeated on every
row would eat the 256 KiB document ceiling.

With `--record`, samples also land in the same CSV + manifest format stage 0 writes, so a
BLE-recorded run and a wired run are directly comparable.

## The gap between here and real hardware

The listener produces `telemetry.json`. Something has to put that in the artifact's store for
the published viewer to see it, and right now that is done by hand from a Claude Code session
(`write_db`). A Python process on a Pi cannot authenticate to it.

That is the one genuinely missing piece, and it is honest to name it: **this is a simulated
POC with a manual bridge, not an unattended live feed.** Everything on either side of that gap
is real — the wire format, the physics, the decoding, the document shapes, the subscription in
the page.

## Tests

    python3 -m unittest discover -s tests -t .

28 tests, standard library only. The protocol is tested for round-trip, resolution, negative
temperatures, the absent-probe sentinel and rejection of foreign advertisements; the simulator
for its physics and for producing decodable payloads; the telemetry buffer for the rolling
window, the compact row shape, and staying inside the document size limit at full capacity.
