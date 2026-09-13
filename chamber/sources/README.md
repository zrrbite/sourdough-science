# Sources — where readings come from

Two seams, deliberately separate:

| | what it decides | implementations |
|---|---|---|
| **Transport** | how bytes arrive | `ble.py` · `serial_line.py` · `onewire.py` · `simulated_source.py` |
| **Decoder** | what the bytes mean | `chamber` · `inkbird` · `line` |

They are separate because an Inkbird is **not a different transport** — it broadcasts BLE
advertisements exactly as our own probe does, just with somebody else's bytes inside. Splitting
transport from payload is what turns "Bluetooth eventually, USB for starters, maybe an Inkbird"
into three `(transport, decoder)` pairs rather than three rewrites.

Everything downstream — the telemetry buffer, the local server, the terminal app, the web
viewer, the CSV schema — has never heard of any of them.

## The contract

A source yields reading dicts. That is all:

```python
{"t_s": 120.0, "air_c": 40.29, "core_c": 36.71, "heating": False,
 "seq": 14, "battery_pct": 97, "setpoint_c": 40.0}
```

`t_s` and `air_c` are required; the rest are optional and may be `None`. `base.reading()`
builds them so every source produces the same shape.

## Choosing one

    listen.py --simulate                                    # no hardware
    listen.py --source ble                                  # our probe
    listen.py --source ble --decoder inkbird                # somebody else's
    listen.py --source serial --port /dev/tty.usbmodem1101  # USB
    listen.py --source w1 --air 28-0000... --core 28-0000... # wired to a Pi

## The USB line protocol

Deliberately stupid, so a handful of lines of sketch feeds the whole system:

    air=40.29,core=36.71,heating=1
    {"air_c": 40.29, "core_c": 36.71, "heating": true}

Unparseable lines are skipped, because every device prints a boot banner. **You can exercise
this today without hardware** — a plain file or FIFO stands in for a serial device, since a
real port is a character device and anything else is opened directly:

    printf 'air=40.1,core=36.2\n' > /tmp/probe
    listen.py --source serial --port /tmp/probe

`ambient` is **not** an accepted field name. It means the *room* elsewhere in this project, and
accepting it as chamber air would put two different quantities under one column name.

## The Inkbird decoder is deliberately unimplemented

An IBS-TH broadcasts temperature in manufacturer data, so it fits this seam exactly. Its byte
layout has not been observed here, and **a guessed wire format produces confident wrong
numbers** — the worst failure a measurement project can have. So `decode_inkbird` returns
`None` and carries the reason.

To write it properly:

    listen.py --scan-raw 30

That prints every distinct advertisement with its company ID and hex payload. Put the Inkbird
next to the machine, warm it in your hand, watch which bytes move, and implement the decoder
against what you captured.

## Our own payload

`protocol.py` — eight bytes under company ID `0xFFFF` (reserved for testing):

| byte | field |
|---|---|
| 0 | version |
| 1 | sequence, wraps at 256 |
| 2–3 | chamber air, int16 big-endian, centidegrees C |
| 4–5 | dough core, int16 big-endian, centidegrees C |
| 6 | battery percent |
| 7 | flags — bit 0 heater on, bit 1 dough probe present |

`-32768` is the absent-reading sentinel, so a probe with no dough sensor still reports air.

## The simulator

`simulated.py` runs the chamber's own lumped thermal model and the same hysteresis law
`stage0/controller.py` uses, with the design spec's constants — UA 0.63 W/K, a 55 W emitter,
dough τ 48 minutes. Its readings are **round-tripped through the real advertisement encoding**
before use, so the simulated path and the radio path decode through identical code.

## Tests

    python3 -m unittest discover -s tests -t .

49 tests, standard library only. The serial source is tested against real streams and real
files, the 1-Wire source against real sysfs-shaped files, and the decoders against payloads
built by the encoder they mirror.
