# Parts to order

**Decided 2026-09-13. Nothing bought yet.** Roughly €70–85 in two groups.

Prices are indicative, not quoted. Every line says what to *check*, because most of these are
commodity parts where the wrong variant looks identical and fails differently.

Tick as ordered, fill in what actually arrived — the chamber's own manifest discipline applies
to the chamber. Knowing you have a 60 W emitter rather than a 100 W one matters the first time
a run overshoots.

---

## Group A — the dual-probe thermometer

**Buy this first.** It is not a chamber part, and it unblocks more than the whole of Group B:
the [core-temperature measurement](../notes/levain-doubling-test.md) can run at the next bake
with nothing else at all, and that measurement is the largest open term in
[why the hot protocol works](../notes/why-the-hot-protocol-works.md).

- [ ] **Dual-probe cabled thermometer** — ~€25–40

| check | why |
|---|---|
| **Two channels** | Air and core simultaneously. The *gap* is the datum; either number alone says little. |
| **Probes rated 100 °C+** | Working range is 40–50 °C, but oven-safe ratings start high anyway. |
| **Wired probes, ~1 m leads** | The probe must stay in. Opening the door dumps the air and restarts the ramp being measured, so a reading-per-door-opening protocol reports a longer lag than the real one. |
| **Display sits outside** | Lead passes through the door seal — normal for this class. |

**Avoid:** instant-read pen thermometers (no cable, so no leaving it in) and wireless in-meat
probes (one channel, no air reading, and designed to be buried in a roast).

**Where to look:** kitchen and BBQ suppliers, not electronics. Search *"dual probe BBQ
thermometer oven safe"*. Inkbird and ThermoPro both make things in this class; check the
specification rather than trusting a model number from here.

**Known limitation, accepted:** 1 °C display resolution is common at this price. That is fine
for lag, where the effect is 5–15 °C. It is **not** enough for chapter 10's gradient numbers —
those wait for calibrated DS18B20s, which is what Group B is for.

---

## Group B — Stage 0 chamber

Full rationale in [`stage0/README.md`](stage0/README.md); thermal budget in the
[design spec](../docs/superpowers/specs/2026-09-13-fermentation-chamber-design.md) §5.

- [ ] **Ceramic heat emitter, E27, 40–60 W** — ~€12

  Not a bulb: LED bulbs make no heat and incandescents are being phased out. A CHE is
  self-limiting by physics, which is safety layer one of three. **40–60 W, not 100 W** —
  holding 45 °C in a 35 L box costs about 16 W, and an oversized emitter overshoots badly
  under bang-bang control.

  *Where:* reptile and vivarium suppliers. Search *"ceramic heat emitter 60W"*.

- [ ] **Ceramic lamp socket with wire guard, E27** — ~€8

  **Ceramic, not plastic.** A CHE's surface gets hot enough to deform a plastic holder and to
  scorch foam or cardboard. The guard stops the emitter touching anything.

  *Where:* same suppliers as the emitter, often sold together as a "ceramic heat lamp holder".

- [ ] **Smart plug with a local HTTP API** — ~€15

  **The one buying trap in this list.** Most cheap Wi-Fi plugs are cloud-only. Stage 0's entire
  safety argument is that the Pi's only contact with 230 V is one HTTP request to a *local*
  endpoint — no relay board in a humid box, no mains on a breadboard. A plug that only works
  through a vendor app collapses that, and you would be back to wiring mains yourself.

  Shelly exposes local HTTP out of the box. A Tasmota-flashable plug works too but has to be
  flashed first. Verify before buying that the device answers on your LAN with the internet
  off.

  *Where:* home-automation suppliers.

- [ ] **Waterproof DS18B20 probes ×2–3, with adapter board** — ~€9

  The adapter board carries the 4.7 kΩ pull-up, so there is nothing to solder. Without it, add
  one 4.7 kΩ resistor to the order.

  Two is the minimum (air + dough core). A third gives room ambient, which costs one config
  line and one CSV column.

  *Where:* electronics hobby suppliers. Search *"DS18B20 waterproof probe module"*.

- [ ] **KSD9700 thermal cutoff, 60 °C, normally closed** — ~€2

  **Verify NC (normally closed), not NO.** Wired in series with the heater supply, it opens the
  circuit if the chamber exceeds 60 °C regardless of what the software is doing. It is the only
  safety layer that works when the Pi has hung, and it is two euros. Do not let it fall out of
  the basket as a rounding error.

  Often sold in mixed-temperature packs — that is fine, use the 60 °C one.

  *Where:* electronics suppliers. Search *"KSD9700 60C NC thermal switch"*.

- [ ] **Cable gland / sealed grommet ×2** — ~€3

  Probe leads pass through the chamber wall. Unsealed, humid air wicks out and condensation
  tracks down the cable toward whatever is on the other end.

- [ ] **Insulated box, ~35 L** — €0–25

  **Check the house first.** A cooler box works; a styrofoam fish box from a fishmonger is
  often free and better insulated than most coolers. PU walls beat EPS. Only buy if nothing
  suitable turns up.

---

## Deliberately not ordering

- **Inkbird IBS-TH (~€20).** A broadcast probe that drops straight into the decoder seam in
  [`sources/`](sources/), so the software is ready for it — but `decode_inkbird` is a stub
  until real advertisements have been captured with `listen.py --scan-raw`, and its probe
  calibration is unknown. Revisit once a wired run shows whether the cable through the seal is
  actually a problem in practice.
- **ESP32, PTC heater, MOSFET, 24 V PSU.** The full instrument from the design spec. §15's
  argument is that a few Stage 0 runs tell you whether it is needed at all: if the box holds
  43 ± 2 °C, PID is a luxury.
- **A reference thermometer for calibration.** Not required — relative agreement between probes
  is what the gradient rests on, and a stirred ice bath anchors the absolute scale at 0.00 °C
  by definition.

---

## What actually arrived

Fill in on receipt. Substitutions are fine; unrecorded substitutions are not.

| item | bought | actual spec | notes |
|---|---|---|---|
| Dual-probe thermometer | | | resolution? |
| Ceramic heat emitter | | | W: |
| Ceramic socket | | | |
| Smart plug | | | local API verified with internet off? |
| DS18B20 ×n | | | adapter board included? |
| KSD9700 | | | NC confirmed? |
| Cable glands | | | |
| Insulated box | | | wall type, internal volume |

---

## Before the first powered run

- [ ] Smart plug answers on the LAN **with the internet disconnected**
- [ ] KSD9700 wired **in series with the heater supply**, not merely present
- [ ] Emitter has clearance from anything combustible, aimed along a wall rather than at the dough
- [ ] Probes calibrated against a stirred ice bath, offsets recorded in `chamber.toml`
- [ ] `./chamber.py --config chamber.toml --dry-run` runs clean before the plug is ever switched
