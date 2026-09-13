# Stage 0 — Pi, bulb, box

The smallest thing that both **holds** a fermentation temperature and **records
what actually happened**. A Raspberry Pi reads DS18B20 probes, switches a heat
source through a smart plug, and writes a CSV you can plot.

It exists because every open question in this repository — ch. 08's
thermotolerance test, ch. 10's thermal-lag figures, the levain bank note's first
open test — is a *measurement* problem, not a heating problem. An oven already
heats. What it cannot do is tell you what temperature the dough actually reached.

Full design, and what this grows into, in
[`../../docs/superpowers/specs/2026-09-13-fermentation-chamber-design.md`](../../docs/superpowers/specs/2026-09-13-fermentation-chamber-design.md).

## What you need

| Item | Note | ~€ |
|---|---|---|
| Raspberry Pi | any model; it lives **outside** the box | — |
| Ceramic heat emitter, 40–60 W | screws into an E27 socket, gives heat and no light, rated for continuous humid duty. A 40 W *appliance* bulb also works; an LED bulb does not — it makes no heat | 12 |
| **Ceramic** lamp socket + wire guard | a CHE runs hot enough to scorch foam or cardboard | 8 |
| Smart plug with a local HTTP API | Shelly or Tasmota. This is what keeps mains wiring out of the project entirely | 15 |
| 2–3 waterproof DS18B20 probes | buy the kind sold *with* an adapter board — it carries the pull-up resistor, so there is nothing to solder | 9 |
| An insulated box | cooler box, styrofoam fish box, cupboard | — |

**~€45.** Holding 45 °C in a ~35 L insulated box costs roughly 16 W, so 40–60 W
is ample; insulation does the work, not the heater.

## Safety

Three things, in order of how much they matter:

1. **Clearance.** A ceramic emitter's surface gets hot enough to ignite foam or
   cardboard. Ceramic socket, wire guard, real air gap, and aim it *along* a wall
   — never at the dough, which would cook a hot face onto it.
2. **Use the smart plug, not a relay board.** The Pi's entire involvement with
   230 V then becomes one HTTP request, and nothing mains-side sits in a humid box.
3. `max_temp_c` in the config is a software cut-out and the *weakest* layer — it
   cannot help if the Pi hangs. The full design adds a hardware thermal cut-out
   in series with the heater; if you leave this running unattended overnight,
   add one.

The software switches the heater off on every exit path, including crashes and
`systemctl stop`.

## Setup

**1. Enable 1-Wire.** `sudo raspi-config` → Interface Options → 1-Wire, or add
`dtoverlay=w1-gpio` to `/boot/firmware/config.txt`. Reboot.

**2. Wire the probes.** All in parallel on one bus: data → GPIO4 (pin 7),
VCC → 3.3 V (pin 1), GND → pin 6. If your probes came without an adapter board,
add one 4.7 kΩ resistor between data and 3.3 V.

**3. Find the probe ids.**

    ./chamber.py --list-probes
    28-0000063d1f2a  22.31 C
    28-0000063d4b11  22.44 C

Warm one probe in your hand and re-run to tell them apart.

**4. Calibrate.** Bundle every probe together in a stirred water bath, hold it at
three or four points across 20–50 °C, take one probe as the reference, and put
the differences in `offset_c`. Anchor the absolute scale with a well-stirred
ice bath, which is 0.00 °C by definition — **no reference thermometer needed.**
Relative agreement between probes is what the surface-to-core gradient rests on,
and this gets it to about ±0.1 °C.

**5. Configure.** `cp config.example.toml chamber.toml` and edit. The `[load]`
block is free-form and lands verbatim in the run manifest — it is the experiment
log, and without it run two is not comparable with run one.

**6. Dry run first.** Logs everything, never touches the plug:

    ./chamber.py --config chamber.toml --dry-run

**7. Run it.**

    ./chamber.py --config chamber.toml

or install the service: `sudo cp chamber.service /etc/systemd/system/`,
`sudo systemctl daemon-reload && sudo systemctl enable --now chamber`.

## What you get

A directory per run under `data_dir`:

    2026-09-13T18-04-12Z_a3f1/
      manifest.json    setpoint, control settings, probe ids and offsets, the load block
      samples.csv      seq, t_s, iso_utc, setpoint_c, <role>_c per probe, heating, flags

    seq,t_s,iso_utc,setpoint_c,air_c,core_c,heating,flags
    0,0.0,2026-09-13T18:04:12Z,40.0,24.00,22.10,1,
    1,10.0,2026-09-13T18:04:22Z,40.0,24.31,22.10,1,

`heating` is 0/1 per sample, so duty over any window is just its mean. Readings
are calibrated; because offsets are additive and recorded in the manifest, the
raw value is exactly `logged − offset` and nothing is lost.

Keep a run by copying its directory into [`../data/runs/`](../data/) and
committing it.

## Why bang-bang and not PID

The dough's own thermal mass low-passes the air swing — a ±1 °C wobble in the
air barely reaches the core. That is ch. 10's thermal lag working in your
favour, and it is why this is adequate rather than a compromise. Swapping in PID
later touches one function, because the control law is isolated in
`controller.py`.

## Deliberately not here

Profiles, a web UI, humidity control, active cooling. The full design has a seam
for each; none are worth building before the logs say what is wanted.

## Tests

    python3 -m unittest discover -s tests -t .

50 tests, no dependencies beyond the standard library. The HTTP switch is tested
against a real local server rather than a mock, and the whole loop runs in a test
with real probe files and a real run directory.
