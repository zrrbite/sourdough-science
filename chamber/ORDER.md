# Parts to order

**Decided 2026-09-13. Nothing bought yet.** Roughly €70–85 plus ~235 DKK for the Pi, in three
groups.

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

  Better still, buy the emitter **in a reflector dome** rated for ceramic emitters — that is how
  the vivarium trade mounts these, and it keeps the element away from every surface. In a foam
  box that stops being a nicety. See the warning in the Denmark section.

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

- [ ] **Cable seal — glands *or* silicone** — ~€3

  Probe leads pass through the chamber wall. Unsealed, humid air wicks out and condensation
  tracks down the cable toward whatever is on the other end.

  **A threaded gland only works on a thin panel.** Through 20–40 mm of foam there is no way to
  land the locking nut, so on a flamingokasse the answer is a drilled hole sealed with silicone
  on both faces. Size glands to the *cable* (M12 for a 3–4 mm probe lead) and use one per cable
  — a gland with three leads through it is not sealed. See the Denmark section.

- [ ] **Insulated box, ~35 L** — €0–25

  **Check the house first.** A cooler box works; a styrofoam fish box from a fishmonger is
  often free and better insulated than most coolers. PU walls beat EPS. Only buy if nothing
  suitable turns up.

---

## Group C — the Pi

Stage 0 needs a small always-on computer to read the probes, decide, and call the plug. It does
almost nothing: **two file reads and one HTTP request every ten seconds.** Performance is
irrelevant here, and that is worth knowing before overbuying.

**The Pi already in the house is not a candidate.** It has been unreachable since 2026-09-08
with its address unknown (see `todo`), and it is the Bullet roaster's deployment target
regardless — a chamber holding temperature unattended overnight would collide with that.

- [ ] **Raspberry Pi Zero WH + power supply + microSD** — ~235 DKK as a bundle

| check | why |
|---|---|
| **Pre-soldered header (the "H" in WH)** | The 1-Wire bus needs GPIO4, 3.3 V and GND. A bare Zero ships with no header, and the alternative is soldering 40 pins. This is the single spec most likely to be got wrong. |
| **Micro-USB power supply, 5 V 2.5 A** | The Zero takes micro-USB, not USB-C. A phone charger usually works but an official supply avoids brownout weirdness on a box that must not stop. |
| **microSD, 16 GB is plenty** | Raspberry Pi OS Lite plus a Python script. |

**An original Zero W is ample.** Single-core ARMv6 sounds antique, and for a loop that samples
at 0.1 Hz it makes no difference. A Zero 2 W is quad-core and 64-bit and nicer to live with —
worth it only if the board will later do BLE scanning as well. Both have Bluetooth, so either
can grow into the broadcast-probe path.

**Plan for headless setup.** The Zero has *mini*-HDMI, so unless that cable is already in a
drawer, do not plan to plug in a monitor. Use Raspberry Pi Imager on the Mac to preconfigure
Wi-Fi, SSH and the hostname before first boot — then the Pi is reachable the moment it powers
up, which is how it will be used anyway.

---

## Where to buy — Denmark

Searched 2026-09-13. **Prices seen at the time, not quotes**, and product pages move — treat
these as "this shop stocks this category" rather than as links to click blindly.

The non-obvious part is which *kind* of shop sells what: a ceramic heat emitter is a reptile
item, a dual-probe thermometer is a BBQ item, and neither is where you would start looking.

### Dual-probe thermometer — kitchen / BBQ shops

[Lomax](https://www.lomax.dk/flere-produkter/udendoers/grill-og-grilludstyr/grilltilbehoer/termometerfabriken-digitalt-ovn-stegetermometer-70158490/)
(Termometerfabriken) · [AV-Cables](https://www.av-cables.dk/stegetermometer/) ·
[AvXperten](https://www.avxperten.dk/stegetermometre/) ·
[Damborg](https://damborg.dk/conzept-stegetermometer-tradlost-m-2-temperaturfolere-sort) ·
[Davidsen](https://www.davidsen.dk/stegetermometre-c-id2000056)

**One distinction worth getting right before buying.** Two different things are sold as
"dual probe":

- **Two sensors on one spit** (the Termometerfabriken style — tip reads the core, a second
  sensor near the handle reads the oven air, ~1 m cable, both shown at once). Elegant for a
  **dough tub**: push it in and you get core and air from one insertion.
- **Two independent cabled probes.** More flexible, and what you want for a **75 g levain
  jar**, where a single spit would put the "air" sensor at the jar mouth rather than in free
  chamber air.

Given the plan is to measure jar *and* tub, two independent probes is the safer buy.

### Ceramic heat emitter + ceramic socket — reptile / terrarium suppliers

[Centrum Dyrehandel](https://centrumdyrehandel.dk/vare/repti-zoo-100w-reptile-ceramic-heat-emitter/) ·
[CDON's terrarium heating section](https://cdon.dk/dyretilbehor/tilbehor-til-krybdyr/radiatorer-lamper-til-terrarier-til-krybdyr/)

Listings skew toward 100–200 W for large vivaria — **look specifically for 40–60 W**, which is
right for a 35 L box and is often the least prominent option. The trade reinforces two things
already in this document: a CHE should always run through a thermostat, and it wants a guard,
because the element gets hot enough to burn anything touching it.

### Shelly smart plug — home-automation shops

[Let-Elektronik](https://let-elektronik.dk/smart-socket-shelly-plug-wifi) ·
[Smart.dk](https://www.smart.dk/maerker/shelly.html) ·
[AvXperten](https://www.avxperten.dk/smart-home-stikkontakt/shelly-plus-plug-s-wi-fi-stikkontakt-energimaaler-1-udtag-2500w-12a.asp)
(Plus Plug S, 229 DKK seen) · [Gadgethuset](https://www.gadgethuset.dk/shop/438-shelly-smarthome/7123-shelly-plus-plug-s-wifi-stikkontakt-med-energimaaling/) ·
[SoluNOiD](https://www.solunoid.dk/shelly) · [WATTOO](https://www.wattoo.dk/shelly-plug-s-gen3-hvid-matter-wifi-smartplug-12a-7822623419)

**This resolves the buying trap in our favour.** Shelly ships a built-in web server with a
local HTTP/RPC API, MQTT and webhooks, and **the cloud can be switched off entirely** —
operation is fully local and does not depend on an internet connection. That is exactly the
property Stage 0's safety argument needs. Type F (Schuko) is the Danish-compatible variant.

### DS18B20 waterproof probes — electronics shops

[Elektronik Lavpris](https://elektronik-lavpris.dk/p140343/sens0025-temperaturfoeler-probe-ds18b20-vandtaet/) ·
[Let-Elektronik](https://let-elektronik.dk/ds18b20-waterproof-temperature-probe-sensor) (1 m, 2 m
and 5 m leads) · [ELEXTRA](https://www.elextra.dk/p/temperatursensor-ds18b20-vandt%C3%A6t-m-ledn-55-125c-1m/H15942) ·
[eBits](https://ebits.dk/products/vandtaet-temperatur-sensor-ds18b20) ·
[Svane-El](https://svane-el.dk/temperatur-alarm-843/temperatursensor-vandtaet-ds18b20-1-meter-p617) ·
[Elektro Shoppen](https://elektroshoppen.dk/produkt/keyestudio-ds18b20-temperatursensor-1m-vandtaet-roer-med-connect-module/)
(Keyestudio, **sold with the connect module** — that is the adapter-board variant, so no
resistor needed)

Longer leads are worth it: the electronics live outside the box, so a 1 m lead is the minimum
and 2 m is more comfortable.

### Insulated box — packaging suppliers and builders' merchants

[Harald Nyborg](https://www.harald-nyborg.dk/flamingokasse-med-laag) (flamingokasse with lid,
40 L and 50 L; the 40 L is H27 × W39,5 × L59,5 cm externally) ·
[jem & fix](https://www.jemogfix.dk/flamingokasse-med-laag-16-liter/1191/9069265/) (16 L, too
small) · [Lomax](https://www.lomax.dk/lager/emballage/papkasser-og-aesker/termo-og-flamingokasser/)
(up to 52 L) · [DT Emballage](https://www.dtemballage.dk/shop/en/varekatalog/termo-og-kolekasser/termokasser-eps) ·
[Grafical](https://www.grafical.dk/termokasser-flamingokasser/)

EPS flamingo is the right material — thick-walled, moisture-resistant, food-approved, and it
holds heat in exactly as it holds cold in. **40 L is close enough to the 35 L the thermal
budget assumes**; the loss figure scales with surface area, so a 40 L box costs a couple of
watts more and nothing else changes. And a fishmonger will often hand over a used one free,
which is worth asking before ordering.

> ### ⚠ Do not put a ceramic emitter against polystyrene
>
> This is the one genuinely dangerous combination in this list, and it arises precisely because
> the best insulator here is foam and the best heater here runs hot. A CHE's element reaches
> several hundred degrees — far above the point where EPS melts, and then burns.
>
> The vivarium trade already solved this: **buy the emitter with a reflector dome / lamp
> fixture rated for ceramic emitters**, which is how a CHE is normally mounted. The dome holds
> the element away from any surface, stops line-of-sight to the walls, and directs the heat.
> Add real clearance on top of that, aim it along a wall rather than at the dough, and put
> something non-combustible — a ceramic tile, a piece of sheet metal — between the emitter and
> the nearest foam.
>
> If that feels like too much care for a proofing box, the alternative is a **seedling heat
> mat**: much lower surface temperature, designed for continuous use, no radiant hot spot. It
> gives up headroom and fast pull-up in exchange for removing this problem entirely.

### Cable glands — Biltema, or rethink the seal

[Biltema M16, 4–8 mm, 2-pack](https://www.biltema.dk/byggeri/elinstallationer/monteringsdetaljer/kabelforskruning-m16-4-8-mm-2-stk-2000064967)
(with nut and gasket) ·
[Biltema M-thread, 2-pack](https://www.biltema.dk/byggeri/elinstallationer/monteringsdetaljer/kabelforskruning-m-gevind-2-stk-2000051760) ·
[Biltema rubber grommets, 10-pack](https://www.biltema.dk/byggeri/elinstallationer/monteringsdetaljer/kabelgennemforing-10-pak-2000021896) ·
[MakerSupplies M12, 3–6,5 mm](https://makersupplies.dk/electrical-cnc-electronics/electrical/cable-management/cable-management-cable-gland-m12-3-65mm)

**Two things to get right here, and the second one may mean buying something else entirely.**

**Size to the cable, not to the hole.** A waterproof DS18B20 lead is typically 3–4 mm, so
**M12 (3–6,5 mm) fits it properly**; M16 (4–8 mm) is loose on a single thin probe lead. And a
gland seals *one* cable — running two or three leads through one gland does not seal, it just
looks like it does. One gland per cable, or a different approach.

**A cable gland assumes a thin panel.** Its thread is sized for a few millimetres of enclosure
wall plus a locking nut on the inside. A flamingokasse wall is 20–40 mm of foam, and a cooler
box is a liner plus foam plus a shell — **the thread will not reach through, and there is
nothing solid to tighten a nut against.** So for a foam box the practical seal is: drill
undersized, push the lead through, and seal both faces with silicone. Or mount a gland on a
thin plate fixed over a larger hole, if you want it demountable.

Buy the glands only if the box turns out to have a thin wall somewhere to mount them; buy
**silicone sealant** either way.

### Raspberry Pi — the bundle is the best buy

[AvXperten's Zero WH bundle](https://www.avxperten.dk/raspberry-pi/raspberry-pi-zero-wh-stroemforsyning-512mb-16gb-microsd.asp)
— **235 DKK for board with pre-soldered header, power supply and a 16 GB microSD**, as listed.
One order, nothing to solder, nothing missing. For this workload that is the whole Pi decision.

If you would rather have the faster board: the **Zero 2 WH** (pre-soldered) is listed at
[RaspberryPi.dk](https://raspberrypi.dk/en/product/raspberry-pi-zero-2-wh-with-presoldered-header/)
at €22,59 but was **out of stock** when checked, with a waitlist. The plain **Zero 2 W** without
a header is widely available from about 149 kr —
[Power](https://www.power.dk/computere-og-tablets/datakomponenter/mikrocontroller/raspberry-pi-zero-2-w-enkeltkortscomputer/p-3959181/),
[Dustin](https://www.dustin.dk/product/5020077561/zero-2-w),
[Farnell](https://dk.farnell.com/raspberry-pi/rpi-zero-w-v2/raspberry-pi-kit-64bit-arm-cortex/dp/3838499),
compared on [PriceRunner](https://www.pricerunner.dk/pl/10012-3208416724/Single-board-computere/Raspberry-Pi-Zero-2-W-Zero-2-Sammenlign-Priser) —
**but then you are soldering a header**, which is exactly the work the bundle avoids.

Power supplies and microSD separately, if buying a bare board:
[official micro-USB 5 V 2.5 A, EU](https://raspberrypi.dk/en/product/raspberry-pi-power-supply-eu-5v-25a/)
· [Zero accessories](https://raspberrypi.dk/en/shop/category/raspberry-pi-zero-and-accessories/).

### KSD9700 thermal cutoff — electronics shops

[BitByg](http://bitbyg.dk/shop/thermostat-switch-bimetal-ksd9700) — **verified**: 60 °C is
stocked, NC is the default variant, 27,50 kr. Also
[Fyndiq](https://fyndiq.dk/produkt/2-stk-ksd9700-temperaturafbryder-termostat-termisk-beskytter-nc-6277d69834c840fc/)
(2-pack) and [ampul.eu](https://ampul.eu/en/thermostats/4089-thermostat-ksd9700-250v-5a-nc).

**The tolerances matter here, and they constrain the setpoint.** The 60 °C part is
**60 ± 5 °C trip, 40 ± 10 °C reset**. So it may open as low as 55 °C — comfortably above a
45 °C working setpoint, but close enough that **setpoints above 50 °C risk nuisance trips**.
Either keep runs at or below 50 °C (which is the whole designed envelope anyway) or take the
70 °C variant for headroom and accept a higher failure temperature. The 5 A version is ample:
a 60 W emitter on 230 V draws about 0.26 A.

Being self-resetting, it will close again as the box cools — so a nuisance trip shows up as a
chamber that mysteriously will not hold temperature, not as a dead run. Worth remembering when
diagnosing.

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
- **A second computer, if you would rather not have one.** `listen.py --source serial` exists
  precisely so a USB device printing `air=40.29,core=36.71` can feed the whole system from the
  Mac, with no Pi at all. The catch is that the Mac then has to stay awake and plugged in for
  the length of a run, which is workable for an afternoon and awkward for an overnight retard.
  A 235 DKK Zero is the cheaper answer to that problem than a laptop that cannot sleep.
- **A reference thermometer for calibration.** Not required — relative agreement between probes
  is what the gradient rests on, and a stirred ice bath anchors the absolute scale at 0.00 °C
  by definition.

---

## What actually arrived

Fill in on receipt. Substitutions are fine; unrecorded substitutions are not.

| item | bought | actual spec | notes |
|---|---|---|---|
| Dual-probe thermometer | | | resolution? one spit or two probes? |
| Raspberry Pi | | | model, header pre-soldered? |
| PSU + microSD | | | |
| Ceramic heat emitter | | | W: |
| Ceramic socket | | | |
| Smart plug | | | local API verified with internet off? |
| DS18B20 ×n | | | adapter board included? |
| KSD9700 | | | NC confirmed? |
| Cable seal | | | glands or silicone? |
| Insulated box | | | wall type, wall thickness, internal volume |

---

## Before the first powered run

- [ ] Smart plug answers on the LAN **with the internet disconnected**
- [ ] KSD9700 wired **in series with the heater supply**, not merely present
- [ ] Emitter has clearance from anything combustible, aimed along a wall rather than at the dough
- [ ] Probes calibrated against a stirred ice bath, offsets recorded in `chamber.toml`
- [ ] `./chamber.py --config chamber.toml --dry-run` runs clean before the plug is ever switched
