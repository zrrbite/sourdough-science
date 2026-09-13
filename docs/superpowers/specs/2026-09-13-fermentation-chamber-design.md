# Fermentation Chamber — Design

**Date:** 2026-09-13
**Status:** design approved, awaiting implementation plan
**Scope:** a temperature-controlled, logging fermentation chamber, built as the
`chamber/` subtree of this repository.

---

## 1. Why

This document's Part II (chapters 07–11) argues about fermentation temperature
in terms the document cannot currently measure. Chapter 10 says the core of a
dough mass is *"probably 30–38°C"* against a 45°C setpoint and lags
*"30–45 minutes"*; chapter 08's extended-bulk thermotolerance test is described
and has never been run. The working note on the heat-driven levain bank states
the problem outright: *"the setpoint is above conventional guidance, the core
temperature is unknown, and the bread rises"*, and lists as its first open test
*"log core temperature with a probe in a banked levain jar and in the dough
during the hot pulse — this is the single measurement that would settle the
caveat."*

All three are blocked on the same missing thing: an environment whose
temperature is known, held, and recorded — together with the temperature
*inside the dough*, which is the quantity the argument is actually about.

A domestic oven on its lowest setting heats. It does not measure, does not
hold, and cannot be trusted to have been at the temperature its dial claims.
The point of this build is therefore **not** that it replaces the oven as a
heat source. It is that it turns several of this repository's open threads from
speculation into experiments.

## 2. Decisions

Locked during design, with the reasoning that produced them.

| Decision | Choice | Why |
|---|---|---|
| Temperature envelope | **Warm only, 25–50°C** | The 3–5°C retard is already covered by a domestic fridge. Adding cooling duplicates existing capability and costs a compressor, floor space and anti-short-cycle control. |
| Role | **Instrument: hold *and* log** | Holding alone is an appliance and leaves every open thread open. Logging air *and* dough-core temperature is what makes ch. 08/10/11 runnable. |
| Capacity | **~30–40 L** — one 1–2 kg bulk tub plus levain jars | Smallest box that covers every planned experiment. Small and well-insulated means thermally stable, and stability is what makes logged data worth anything. |
| Controller | **ESP32** | WiFi built in, drives a MOSFET, ample headroom for the profile engine and web UI later. Costs nothing extra now and does not need replacing then. |
| System shape | **Autonomous controller + host-side collector** | Live view during a run *and* a plain-CSV artifact readable by anything, forever. Transport sits behind a seam, so an MQTT/Grafana stack is a later swap rather than a rewrite. |
| Location | **Same repo, `chamber/` subtree** | The run data belongs next to the prose that interprets it. Separating them puts the evidence one repo away from the argument and invites link rot. |

### Non-goals for v1

- **Cooling.** Warm-only, by decision above. See §13 for what this costs the
  profile version.
- **Humidity control.** RH is logged, not controlled. A water tray and the
  circulation fan are the whole humidity story.
- **Programmable profiles.** Wanted, and explicitly designed *for* (§13), but
  not built. You do not know which profile you want until the logs tell you.
- **Web UI, phone alerts, cloud anything.**

## 3. Architecture

Four units, each understandable and testable alone.

| Unit | Job | Depends on |
|---|---|---|
| **Chamber** | Insulated box, PTC heater + fan, hardware thermal cutoff | nothing — physics |
| **Controller** (ESP32) | Reads probes, runs PID, drives heater, emits samples | a *setpoint source* |
| **Collector** (Python, host) | Receives the stream, writes one CSV + one manifest per run | the wire schema |
| **Analysis** (Python, in repo) | Lag-to-setpoint, time-weighted mean core temp, gradient | the *file* schema only |

The load-bearing property: **analysis never talks to hardware.** It reads
files. It therefore runs against a run recorded years ago, a run recorded by
someone else, or a hand-written CSV in a test — and the chamber can be rebuilt
from scratch without touching a line of it.

## 4. The future-proofing contract

The principle: **future-proof the data and the interfaces; treat the firmware
and the box as replaceable.** Data is forever, code is not. No plugin
architecture, no hardware abstraction layer for sensors that will never be
bought.

- **Plain text is the source of truth.** CSV for samples, JSON for the run
  manifest, both carrying `schema_version`. Columns are self-describing, so
  adding a probe adds a column and readers that select by name keep working.
  Never a database or binary format as the primary artifact.
- **Calibration travels with the run.** Per-probe offsets are written into
  every manifest, not only held in device NVS, and both raw and corrected
  values are logged. Recalibrate or swap a probe and earlier runs stay
  interpretable; get a calibration wrong and it is recoverable rather than
  baked in.
- **No cloud, no account, no vendor service.** Everything works on the LAN with
  the internet down, and nothing in the stack can be discontinued.
- **Three seams, because these are the changes actually expected:** setpoint
  source (constant → profile), transport (line-to-file → MQTT), probe set
  (1-Wire bus takes more probes on the same pin, no schema change).
- **Explicitly not future-proofed:** firmware internals and the enclosure.

## 5. Hardware

### Thermal budget

A ~35 L cooler box presents roughly 0.7 m² of wall at U ≈ 0.9 W/m²K, so
UA ≈ 0.63 W/K. Holding 45°C in a 20°C kitchen costs about **16 W**
steady-state; about 20 W at 50°C in a cold room. Insulation does the work, not
the heater.

### Heat

A **24 V, 80–120 W PTC fan-heater module**, landing steady-state duty around
20% — margin enough to recover from a lid opening or a cold 2 kg tub, without
being so oversized that the loop gets twitchy.

**Two separate channels: the heater is PWM'd, the fan runs continuously.** This
matters more than it looks. If fan speed tracked heater duty, the surface
heat-transfer coefficient would vary with heater duty, contaminating the exact
surface-to-core gradient the instrument exists to measure. Constant airflow
fixes the convection boundary condition.

Mount the heater in a baffled corner blowing *along* a wall, never impinging on
the tub — direct impingement makes a hot face on the dough and destroys the
symmetry of the gradient.

### Sensing

Four waterproof DS18B20 probes on one 1-Wire bus — **chamber air, dough core,
dough sub-surface, room ambient** — plus an SHT31 for RH.

- The air probe sits in the return path, **shielded from line-of-sight to the
  heater**, or it reads radiant heat and lies to the controller.
- The core/sub-surface pair is what makes ch. 10 measurable rather than argued.
- Both dough probes need a **depth collar on the tub lid** so insertion
  geometry repeats between runs. Two centimetres of depth error swamps the
  effect being measured; reproducible placement is a measurement requirement,
  not a nicety.
- **Two load cases, two fixtures.** The bulk tub is one; a 75 g levain jar per
  the heat-driven levain bank note is the other, and its thermal behaviour is
  very different — far less mass, far shorter lag, so its core plausibly *does*
  approach the setpoint where a 1 kg tub's does not. The jar needs its own
  fixture: a lid or silicone plug holding the probe at the jar's geometric
  centre, clear of the glass wall.

### Calibration

DS18B20s are ±0.5°C absolute, which is mediocre — but gradient work needs
*relative* agreement, not absolute truth. Bundle all four probes in a stirred
water bath at three or four points across 20–50°C, take one as reference, and
record pairwise offsets; that gets relative agreement to roughly ±0.1°C. Anchor
absolute accuracy with an ice bath. Offsets go to NVS *and* into every run
manifest.

### Safety — three independent layers, no mains inside the box

1. **Physics.** A PTC element is self-limiting: its resistance climbs steeply at
   its Curie point, so it cannot exceed its rated surface temperature even at
   100% duty with dead firmware. Choose a module rated ≤110°C.
2. **Hardware.** A KSD9700-type 60°C normally-closed thermal switch bonded
   inside the chamber, wired in series with the heater supply — independent of
   the MOSFET and of any code. Plus an inline fuse on the 24 V line.
3. **Firmware.** Watchdog and plausibility checks: any probe failing, reading
   out of range, or air exceeding setpoint + 5°C forces duty to zero and flags
   the run. Maximum-duty clamp and maximum-runtime limit.

Everything inside the chamber is low-voltage DC. The PSU brick lives outside,
and cables pass through a sealed grommet so humid air cannot wick out and
condensation cannot track down a cable. Electronics are mounted outside the
box, which also keeps the ESP32's self-heating out of the measurement.

## 6. Bill of materials

Prices indicative, not quoted. Check availability before ordering.

| # | Item | Spec | Qty | ~€ |
|---|---|---|---|---|
| 1 | Insulated cooler box | ~35 L, PU walls preferred over EPS | 1 | 20–30 |
| 2 | PTC fan-heater module | 24 V, 80–120 W, element rated ≤110°C | 1 | 10–15 |
| 3 | PSU | 24 V, 150 W sealed brick — lives outside | 1 | 15 |
| 4 | ESP32 devkit | ESP32 or ESP32-S3 | 1 | 6 |
| 5 | DS18B20 probes | waterproof stainless, silicone lead 1–2 m | 4 | 12 |
| 6 | Resistor | 4.7 kΩ, 1-Wire pull-up | 1 | — |
| 7 | SHT31 breakout | I²C, ±2% RH | 1 | 6 |
| 8 | MOSFET module | logic-level N-channel, ≥10 A, heatsinked | 1 | 3 |
| 9 | Thermal cutoff | KSD9700 60°C NC, in series with heater | 1 | 2 |
| 10 | Fuse + holder | ~6.3 A slow-blow, inline on 24 V | 1 | 3 |
| 11 | Project enclosure | small ABS box, mounted outside the chamber | 1 | 5 |
| 12 | Cable gland / grommet | sealed pass-through | 2 | 3 |
| 13 | Water tray | shallow, for humidity | 1 | — |
| 14 | Probe depth collars | printed or silicone, on the tub lid | 2 | — |
| 15 | Wire, ferrules, heatshrink | 18–20 AWG for the 24 V run | — | 5 |

**Roughly €90 all in**, less if the cooler box is one already owned.

## 7. Firmware

**Toolchain:** PlatformIO with the Arduino-ESP32 framework — chosen for library
ergonomics (OneWire, SHT31, ArduinoJson) and because it provides a `native`
host test environment for free. ESP-IDF is a viable swap.

| Module | Job | Notes |
|---|---|---|
| `probes` | 1-Wire + I²C read, apply offsets | returns raw **and** corrected per channel, with a validity flag |
| `setpoint_source` | `float setpointAt(elapsed_ms)` | **the profile seam.** v1 `ConstantSetpoint`; later `ProfileSetpoint` walks segments |
| `control` | PID: setpoint + air → duty | anti-windup clamp; **derivative on measurement, not on error** — otherwise profiles kick the output at every segment change |
| `safety` | plausibility + watchdog, can veto the heater | deliberately separate from `control`, so a control bug cannot disable it |
| `heater` | PWM out, duty clamp, hard-off | LEDC, ~1 kHz, 10-bit |
| `telemetry` | `publish(Sample&)` | **the transport seam.** v1 NDJSON over TCP; later MQTT |
| `buffer` | ring buffer, replay on reconnect | a WiFi dropout must not put a hole in a 12-hour record |
| `run` | run id, manifest emission, lifecycle | |

### Timing

One broadcast 1-Wire conversion per second, then read four scratchpads — so
12-bit resolution (0.0625°C) costs one 750 ms conversion rather than four. PID
updates at 1 Hz. Telemetry emits every 10 s as the **mean over the interval**,
with duty as mean duty, which is the physically meaningful quantity (energy
in). That is 8,640 rows/day, about 700 KB raw and 100 KB gzipped —
committable. A `samples_n` column records how many raw samples backed each row,
so a degraded stretch is visible rather than silently smoothed.

### Tuning, and the first experiment

Do not hand-tune blind. Run an open-loop step test: fix duty, record the
response, fit first-order-plus-dead-time, derive initial gains, refine. That
characterisation *is data worth committing* — it gives the chamber's time
constant and dead time, which is precisely what determines how fast a profile
can ramp later. **The first run of the instrument characterises the
instrument.**

## 8. Schemas

### Wire (NDJSON, one object per emit)

```json
{"schema_version":1,"run_id":"2026-09-13T18-04-12Z_a3f1","seq":417,"t_s":4170.0,
 "setpoint_c":40.00,"air_c":39.96,"core_c":33.12,"subsurf_c":37.80,"ambient_c":21.4,
 "rh_pct":74.2,"duty":0.187,"samples_n":10,"flags":[]}
```

`flags` carries values such as `probe_fault:core`, `safety_cutoff` and
`backfill`, so replayed samples stay distinguishable from live ones forever.

### Files

```
chamber/data/runs/2026-09-13T18-04-12Z_a3f1/
  manifest.json
  samples.csv     # header = the JSON keys; add a probe, add a column
  notes.md        # optional, free text
```

`manifest.json` carries `schema_version`, start/end timestamps, firmware
version and git sha, the setpoint spec, control gains, **per-probe ROM id,
offset and placement**, calibration method and date, and a `load` block —
dough mass, container, flour, hydration, levain percentage. The `load` block is
the experiment log, and it is the difference between a pile of runs and a
comparable series. The collector prompts for it, or accepts `--load load.yaml`.

The setpoint is stored as a typed spec object (`{"type":"constant","value_c":40.0}`)
specifically so that `{"type":"profile","segments":[...]}` needs no schema bump.

## 9. Host side (`chamber/host/`)

- **`collect.py`** — listens, validates each line against the schema, appends to
  `samples.csv` flushing per line (a crash loses at most one sample), dedupes
  backfilled samples by `seq`, writes the manifest at start and patches
  `ended_utc` at stop.
- **`analyse.py`** — reads a run *directory*, never a device. Produces
  lag-to-setpoint, time-weighted mean core temperature, mean and peak
  surface-to-core gradient, duty integral, and the plot. **Those four numbers
  are chapter 10's unrun measurement.**

This follows the shape already established in `tilt-hydrometer-analysis`:
BLE/network sensor → logged time series → Python fit and plot.

## 10. Testing

- **Firmware.** `control`, `safety` and `setpoint_source` are plain C++ with no
  hardware in them, unit-testable under PlatformIO's `native` environment. A
  simulated first-order plant regression-tests that the loop settles without
  overshoot.
- **Host.** Golden CSV fixtures, deliberately including a probe fault, a gap,
  and backfilled rows, asserted against expected analysis output.
- **Integration.** The chamber characterisation run (§7) doubles as the
  end-to-end acceptance test: if it produces a clean first-order response and a
  complete CSV, the whole chain works.

## 11. Repo integration

```
chamber/
  README.md                       what the instrument is, how to run a build
  docs/01-build.md                enclosure, wiring, assembly, BOM
      02-calibration.md           the bath procedure, recording offsets
      03-running-an-experiment.md protocol: manifest, probe placement, start/stop
      04-characterisation.md      the step test and the chamber's measured constants
  firmware/                       PlatformIO project
  host/                           collect.py, analyse.py, tests
  data/runs/                      committed run directories
```

Changes to the existing document, kept minimal:

- **Format section** scoped: the document is markdown with no build step;
  `chamber/` is a project with its own toolchain.
- **Equipment and materials** gains the chamber.
- **Chapters 08, 10 and 11** each gain a link out to the relevant build or
  experiment doc. Chapter 10's "Verifying Actual Dough Temperature" section is
  effectively this instrument's specification and should point at it.
- **Status and open threads** notes which threads the chamber now unblocks.

The chamber docs are build-and-procedure voice; the chapters remain
interpretation. Keeping that seam clean is what stops the two drifting.

## 12. Experiment programme

1. **Characterisation** — the step test. Calibrates the instrument before
   anything it says is trusted.
2. **Levain jar core (levain bank note, open test 1)** — a 75 g jar at a 45°C
   setpoint, probe at the jar's centre. The note names this as *the single
   measurement* that would settle its temperature caveat, and it is cheap: one
   jar, one afternoon. It also tests the more interesting hypothesis, that jar
   and tub sit in genuinely different thermal regimes rather than differing by
   degree.
3. **Thermal lag (ch. 10)** — 1 kg tub, 45°C setpoint, 3 h. Replaces
   "probably 30–38°C" and "likely 30–45 minutes" with measurements. Run
   alongside 2 for the jar-versus-tub comparison.
4. **Stir vs. no-stir (ch. 10)** — two runs at one setpoint, one stirred twice;
   observe the gradient collapse and its effect on rise.
5. **Extended bulk / thermotolerance (ch. 08)** — the README's first open
   thread. It has been unrunnable because the core could not be *verified* at
   40°C+ rather than hiding in a cool refuge. Now it can be, and thermotolerance
   separates from temporal escape.
6. **Post-recovery culture (ch. 11)** — identical, verified thermal exposure for
   the recovered culture against a control.

Experiments 2 and 5 are unlocked by the measurement, not by the box. An oven
would have done the heating.

## 13. What v2 (profiles) inherits — and one honest limit

Inherited free from this design:

- `setpoint_source` makes `ProfileSetpoint` a new class, not a controller change.
- Derivative-on-measurement means no output kick at segment boundaries.
- The setpoint is already a typed spec object, so profiles need no schema bump.
- The transport seam carries profile push when MQTT arrives.
- Characterisation (§7) gives the measured ramp rate, so profiles get designed
  against physics rather than wishes.

**The limit, stated now so profiles are not designed on a false premise:**
warm-only means profiles ramp *up* fast and *down* only passively. With
UA ≈ 0.63 W/K against roughly 7.5 kJ/K of dough and liner, the time constant is
about 3.3 hours — so 45°C → 26°C in a 20°C kitchen takes on the order of
**four to five hours**. A vent fan would cool the air quickly and the dough core
barely faster, because the dough's own mass dominates. It is the same thermal
lag chapter 10 is about, running in reverse. Downward segments in any future
profile must be written around that, or the chamber needs active cooling.

In practice this bites less than it looks. The protocol in the levain bank note
alternates hot and cold repeatedly — hot build, fridge for days, hot refeed,
hot pulse, fridge overnight — but every cold step is done by **moving the jar or
tub to the fridge**, not by ramping the chamber down. Relocation is far faster
than passive cooldown and needs no hardware. A future profile engine should
therefore treat a downward step as a *prompt to move the load*, not as a
setpoint to chase.

## 14. Assumptions

- PlatformIO + Arduino-ESP32 rather than ESP-IDF (§7). Swappable.
- A host machine is available on the same LAN for the duration of a run; the
  device's ring buffer covers dropouts, not a host that is off all night.
- Run data is committed to the repository. At ~100 KB gzipped per run-day this
  is comfortable for the planned programme, and it is what makes the empirical
  claims checkable — consistent with the document's stated
  empirical-versus-literature convention.
