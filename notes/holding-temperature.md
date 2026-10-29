# Holding a Temperature at Home

> **Context.** The chapters and notes ask for specific temperatures: 24–27°C for a starter,
> 35–38°C for a hot levain, 38–42°C for a warm autolyse, 3–5°C for a retard. This note is
> how to get them in a home kitchen, from the oven light to dedicated boxes. One rule
> applies to all of them, and matters more than the choice of device: the air temperature
> is not the dough temperature.

---

## The targets

| What | Temperature | From |
| --- | --- | --- |
| New starter, first two weeks | 24–27°C; her target is measured at 27°C | [Starter note](starter-from-scratch.md), *Temperature* |
| Optional warm start | About 30°C *(hypothesis)* | Starter note, open tests 1–2 |
| Reviving a dried starter | 24–26°C | Starter note, *Reviving it* |
| Tripling test ("done") | 27°C | [Cheat sheet](starter-cheatsheet.md) |
| Hot levain build | 35–38°C; the levain bank runs its oven at a 40–50°C setpoint | Ch. 07; [levain bank](heat-driven-levain-bank.md) |
| Warm autolyse | 38–42°C for 60–90 min | Ch. 17 |
| Bulk, hybrid formulas | About 22°C | Ch. 22 |
| Cold retard | 3–5°C | Ch. 14, 22 |

No hot build until the starter passes the tripling test (starter note).

## The rule: measure the dough, not the air

- **Air is a poor conductor.** A jar or a tub of dough lags the air around it, and the larger
  the mass, the longer the lag (ch. 10). Here, the oven air has been measured at about
  45°C; the levain core never has (levain bank, *The temperature caveat*).
- **Put a probe in the core.** A dual-probe thermometer, one probe in the air and one in the
  dough, is the single most useful purchase. The gap between the two is the number that
  matters (`chamber/ORDER.md`, group A).
- **The ramp matters as well as the level.** A slow ramp is protective. Dropping a small
  levain into an already-hot water bath is harsher than it looks (ch. 11).

## The options

| Method | Range | Holds a setpoint? | Best for |
| --- | --- | --- | --- |
| Oven, light on | Whatever the lamp gives: 27°C in the video | No | A starter at about 27°C |
| Oven, low setting or residual heat | About 45°C air here, on the usual setting | No | Hot builds, with a core probe |
| Water bath | Anything up to hot tap water; a sous-vide stick holds it exactly | Only with a circulator | Gentle, steady starter temperatures |
| Improvised warm spots | A few degrees above the room | No | A starter on a cold day |
| Inkbird-style controller in a box | Whatever the heater and box can reach | Yes | A starter, levain or dough at a set temperature |
| Chamber Stage 0 (this repo) | Up to about 45°C | Yes, and it logs | Any run you want to measure |
| Brød & Taylor Folding Proofer | 21–35°C humid, 21–49°C dry | Yes | Whole doughs, warm autolyse, levain builds |
| Brød & Taylor Sourdough Home | 5–50°C, heats and cools | Yes | A starter jar |
| Fridge | Usually 3–5°C; measure yours | Roughly | Retards |

### The oven

- **Light on.** The heat comes from the lamp, so it depends on the bulb: incandescent and
  halogen oven lamps warm the cavity, LED lamps barely do. The video's oven held 27°C (80°F)
  with the light on (starter note, *Day by day*). Measure yours before trusting it.
- **Lowest setting.** Domestic oven dials are unreliable at low settings. Here the usual
  setting gave about 45°C air, a spot reading, so whether it holds 45°C or cycles around a
  lower mean is still open (levain bank). 45°C air is thermal-kill territory for the
  surface of a wet culture (ch. 07), which is why the core reading matters.
- **Residual heat.** Heating briefly and switching off gives a falling temperature with no
  control, and it overshoots easily. Use it only with a thermometer inside.
- **Leave a note on the oven** when something is proving in it. A preheat with a jar of
  starter inside is the most common way to lose one.

### Water

A jar in warm water reaches the water's temperature far faster than it would in air, which
is the point and the risk. For holding a starter at 24–27°C it is the steadiest cheap
method, if the water is topped up or a sous-vide circulator holds it. For a hot build it
removes the slow ramp that may be protecting the culture (ch. 11), so warm the water with
the jar in it rather than dropping the jar into hot water.

### Improvised warm spots

A closed microwave or cupboard with a mug of just-boiled water, the top of the fridge, a
spot near a radiator. All unregulated: put a thermometer next to the jar and refresh the
water every hour or so.

### An Inkbird-style controller in a box

The cheapest way to *hold* a temperature. A plug-in controller such as the Inkbird ITC-308
switches a heater on and off against its probe. It has separate heating and cooling
outlets, each rated 10 A, a range of −50 to 99°C, and high and low temperature alarms
(manufacturer and retailer specifications).

- **Heater:** a 40–60 W ceramic heat emitter in a ceramic socket, as in chamber Stage 0, or a
  seedling heat mat under a tile. An LED bulb makes almost no heat (`chamber/stage0`).
- **Box:** a cooler box, a styrofoam box or a dead fridge. Insulation does the work: holding
  45°C in about 35 L takes roughly 16 W (`chamber/stage0`).
- **Cooling:** the second outlet on a mini fridge or wine fridge gives a controlled 10–15°C,
  or a retard you can trust.
- **Probe placement:** in the air, or taped to a water-filled jar the size of the dough, as a
  stand-in. *(Reasoning:)* not in the dough itself for a hot build, because the controller
  would keep heating the air far past the target while the core catches up.
- **Safety:** a ceramic emitter runs hot enough to scorch foam or cardboard. Ceramic socket,
  wire guard, a real air gap, and aim it along a wall, never at the dough
  (`chamber/stage0`).
- **No log** on its own. The chamber's collector can read an Inkbird Bluetooth
  thermometer's broadcasts, so one of those adds the record (`chamber/README`).

### Chamber Stage 0

This repository's own build: a Raspberry Pi, a ceramic heat emitter, a smart plug and an
insulated box, about €45. It holds a setpoint with hysteresis and writes air and dough-core
temperatures to a CSV, which makes it the only option here that records what the dough
actually did. See [`chamber/stage0`](../chamber/stage0/).

### Brød & Taylor

Two products, figures from the manufacturer:

- **Folding Proofer.** Humid mode, with the water tray and an open container, runs
  21–35°C. Dry mode, for a closed container, runs 21–49°C. The thermostat sits in the base
  and reads the aluminium heating plate. It is calibrated to keep the *food* at the setpoint,
  and a covered dough may run 1–3°C warmer. It suits whole doughs, a covered warm autolyse at
  38–42°C, and levain builds up to 49°C. *(Reasoning:)* it heats from below, so the jar's
  bottom warms first, a different ramp from oven air. It does not cool.
- **Sourdough Home.** 5–50°C, heating and cooling, holding a starter within 1–3°F (about
  0.5–1.5°C) of the setpoint. Takes up to a 1 L jar. Made for keeping a starter at a fixed
  temperature, or cool between bakes; not for doughs.

## What to use for what

- **The starter, day to day:** the oven light if it really gives 24–27°C; otherwise a water
  bath, the Sourdough Home, or a controller box.
- **Hot levain builds:** the oven, as now, but with a probe in the core. Stage 0 when you want
  a record; the Folding Proofer if you want it held, up to 49°C.
- **Warm autolyse:** the Folding Proofer in dry mode, covered, or a water bath.
- **Retards:** the fridge, measured, or the controller's cooling outlet for anything warmer
  than 5°C.

---

## Related

- [Thermal lag](../docs/10-thermal-lag-the-oven-setpoint-is-not-the-dough-temperature.md) — why
  the air is not the dough.
- [The Heat-Driven Levain Bank](heat-driven-levain-bank.md) — the protocol these temperatures
  serve, and its temperature caveat.
- [`chamber/`](../chamber/) — the logging chamber, Stage 0 and the full design.

## Sources

- Brød & Taylor. FAQ: Folding Proofer and Sourdough Home. https://brodandtaylor.com/pages/faq —
  Proof-mode ranges, base-plate thermostat, food-temperature calibration, Sourdough Home
  range and tolerance. Manufacturer's figures.
- Inkbird. ITC-308 temperature controller. https://inkbird.com/products/itc-308s and
  https://au.inkbird.com/products/temperature-controller-itc-308 — Two 10 A outlets, range,
  alarms. Manufacturer's figures; some variants list a range to 120°C.
- Brouwland. Inkbird ITC-308 listing.
  https://brouwland.com/en/temperature-controllers/10512-inkbird-itc-308-temperature-controller.html
  — ±1°C accuracy, 0.1°C resolution.

---

<!-- nav -->
[Contents](../README.md)
