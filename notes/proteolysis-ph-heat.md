# Accelerating Proteolysis: pH, Heat, and Salt

> **Context for a fresh session.** These are notes from a longer conversation about
> fermentation science, developed around sourdough/hybrid pizza and bread. There is a
> companion document (`preferments.docx` / `.tex` / `.pdf`) covering preferment taxonomy,
> gluten chemistry, thermal management, oven-spring mechanics, and formulas. This file
> captures one specific thread: **can a pH drop be induced fast enough (via heat) to
> boost protease activity, without a long fermentation?**
>
> Relevant background from the companion doc: the baker runs pure sourdough levain builds
> at 40°C+ for ~1h, hot bulk at 40°C+ for ~2h, then overnight cold retard. Flour is
> typically Caputo Oro Manitoba (W 350–380+). Ooni 12" and a 300°C home oven.

---

## The question

> What about pH drop to increase protease activity. Is that achievable with a heat boost
> like this, without a long fermentation?

---

## Part 1 — General answer

**Partially — but the limiting factor isn't what you'd expect. It's not the rate of acid
production; it's buffering and dilution.**

### Heat does accelerate acidification

Thermophilic LAB at 40–45°C produce acid several times faster than mesophilic LAB at 25°C.
A pH drop that takes 8 hours at room temperature might take 2–3 hours hot. That's a real
compression, but it's roughly **2–4×, not 20×**. You can't get there in 30 minutes.

### Why: buffering capacity is a molar requirement

To move dough from pH ~6.0 to ~4.0, you have to produce a fixed *quantity* of acid — enough
to overcome the flour's buffer from amphoteric proteins, phosphates, and minerals. That's a
molar requirement, and it doesn't shrink because you're producing acid faster. Heat gets you
there sooner; it doesn't reduce the amount needed.

Higher-ash flour buffers harder, so **the mineral content that activates the proteases also
resists the pH drop that activates them.**

### Then dilution kills it

This is the part that matters most for the hot-levain protocol. Even if the levain hits
pH 3.8, when it's mixed into the bulk at 10–15% of total flour, the final dough gets
buffered back up — realistically to somewhere around **pH 5.2–5.5**. That's well above the
~3.5–4.0 optimum for the endogenous wheat aspartic proteases.

So:

- The levain's own gluten is heavily degraded ✓
- A bolus of LAB proteases is introduced into the dough ✓
- **But the bulk flour's own proteases stay largely dormant** ✗

Getting the *final dough* to protease-optimum pH quickly is a much harder problem than
getting the levain there.

### Heat partially substitutes for pH

Enzyme rate roughly doubles per 10°C (Q₁₀ ≈ 2) up to the denaturation threshold. Wheat
proteases hold up fine to ~50°C. So:

> A dough at **pH 5.5 and 40°C** can have comparable total proteolytic throughput to a dough
> at **pH 4.5 and 25°C**.

You're trading position on the pH-activity curve for position on the temperature-activity
curve. **That's the mechanism actually doing the work in a hot bulk** — not a dramatic pH
drop, but ordinary proteases running hot.

### Effective levers, ranked

If you genuinely want fast, aggressive proteolysis:

1. **Raise levain percentage** — the big one; moves acid load and LAB protease load
   simultaneously
2. **Heat**
3. **Time**

Heat alone is the weakest of the three.

### Shortcut: direct acidification

A small addition of lactic acid drops pH to the protease optimum instantly, decoupling
"reach low pH" from "wait for LAB to make acid." Combine with 40°C and you get rapid
proteolysis without extended fermentation.

**Caveat** (from the Clarke / Wehrle literature): chemical acidification *firms* dough rather
than softening it. This applies on short timescales, before proteolysis has had time to act.
Hold it warm and the proteases catch up and overtake.

### ⚠️ Flag: this is probably wrong for pizza

The companion doc's *Long Fermentation Problem* chapter is about exactly this failure mode —
proteolysis past a threshold gives dough that tears during opening rather than stretching.

- **Soft sandwich loaf / ciabatta-style crumb** → makes sense
- **10–11" Ooni pie stretched by hand** → more proteolysis is moving in the wrong direction

---

## Part 2 — Bread-specific answer

*(after clarifying this is a bread question, not pizza)*

**There's a lever available that sidesteps the pH problem entirely.**

### Salt is the biggest inhibitor, and it's free to remove

Salt suppresses cereal protease activity through **ionic strength** and **reduced water
activity**, independent of pH. A no-salt autolyse therefore lets the flour's own proteases run
at a substantially higher rate than the same dough with salt already in.

This is the actual reason Calvel's autolyse works the way it does — it's usually explained as
passive hydration, but **a meaningful part of the softening is enzymatic**. Delaying salt to
the final mix is a bigger proteolytic lever than any realistic pH manipulation, and it costs
nothing.

### The warm autolyse

Stack salt removal with heat:

> **38–42°C, no salt, no levain, 60–90 minutes.**

Rapid, controlled proteolysis with no fermentation at all. There's no pH drop to wait for, no
acid to accumulate, no buffering to overcome. You're running ordinary wheat proteases at
pH ~6.0 but at 2–4× their room-temperature rate via Q₁₀. Add the levain and salt afterward.

This **decouples "degrade the protein" from "ferment the dough"** — the two become independent
control axes.

### Temperature ceiling

Stay below ~50°C. Starch gelatinisation onset is 55–60°C, and above that you're into
scald / *Brühstück* territory — a different technique with the **opposite** goal, since it
gelatinises starch *and* denatures the proteases you're trying to exploit.

### Why more proteolysis is good for bread

Things it buys that it doesn't buy for pizza:

- **Extensibility** for shaping
- **Softer crumb**
- **A larger free amino acid pool** going into the oven → feeds Strecker degradation and
  pyrazine formation in the crust

That last one is the underrated benefit. Bread's long bake (40–50 min) gives that chemistry
far more time to express than a 2-minute pizza bake does.

### Gentler risk profile

You're not stretching to 3mm by hand; the dough sits in a banneton with structural support.

| | Pizza | Bread |
|---|---|---|
| Failure mode | Tearing during hand-stretching | Loss of gas retention → flat, dense loaf |
| Threshold | Near | Much further out |
| Tolerable levain % | 10–15% | 20–30% |

### Lever ordering for bread

1. **No-salt warm autolyse** (largest effect, costs nothing, reversible by adding salt at
   final mix)
2. **Levain percentage**
3. **Bulk temperature**
4. *pH manipulation* — least efficient path; leave it alone unless the others aren't getting
   you there

---

## Suggested protocol

1. **Warm autolyse** — flour + all formula water at 40–42°C. No salt, no levain, no commercial
   yeast. Mix only until no dry flour remains. Hold at 38–42°C for 60–90 min.
   *Note: thermal lag applies — a large dough mass in a plastic container takes 30–45 min to
   reach setpoint at its core.*
2. **Assess** — should feel noticeably softer, slacker, more extensible than a
   room-temperature autolyse. A small piece should stretch thin without snapping back. Tight →
   extend 30 min. Slack to the point of structural loss → reduce time/temp next time.
3. **Final mix** — add levain and salt. Salt immediately begins suppressing further protease
   activity; the proteolysis window is now closed and the network can rebuild through
   time-dependent mechanisms.
4. **Bulk and shape as normal** — may need fewer folds and shorter bulk than the same formula
   without a warm autolyse. Watch the dough, not the clock.
5. **Expect a flavour dividend** — enlarged free amino acid pool feeds Strecker degradation
   during the bake: malty, nutty, roasted crust notes.

---

## References

- Calvel R, Wirtz RL, MacGuire JJ (2001). *The Taste of Bread*. Aspen Publishers.
  — origin of the autolyse; enzymatic contribution alongside hydration
- Bombara N, Añón MC, Pilosof AMR (1997). Functional properties of protease modified wheat
  flours. *LWT* 30(5):441–447.
- Beck M, Jekle M, Becker T (2012). Impact of sodium chloride on wheat flour dough for
  yeast-leavened products. *J Sci Food Agric* 92(2):299–306.
- Clarke CI, Schober TJ, Dockery P, O'Sullivan K, Arendt EK (2004). Wheat sourdough
  fermentation: effects of time and acidification on fundamental rheological properties.
  *Cereal Chemistry* 81(3):409–417.
- Wehrle K, Grau H, Arendt EK (1997). Effects of lactic acid, acetic acid, and table salt on
  fundamental rheological properties of wheat dough. *Cereal Chemistry* 74(6):739–744.
- Thiele C, Grassl S, Gänzle MG (2004). Gluten hydrolysis and depolymerization during
  sourdough fermentation. *J Agric Food Chem* 52(5):1307–1314.
- Eliasson AC (1980). Effect of water content on the gelatinization of wheat starch.
  *Starch/Stärke* 32(8):270–272. — basis for the 55–60°C ceiling
- Bloksma AH, Bushuk W (1988). Rheology and chemistry of dough. In *Wheat: Chemistry and
  Technology*, 3rd ed., AACC.

> **Caveat:** Q₁₀ ≈ 2 is a general biochemical approximation, not a bread-specific
> measurement. Treat it as an order-of-magnitude guide, not a precise predictor for any
> particular protease isoform.

---

## Open threads / possible next steps

- Test the warm autolyse against a room-temperature control on the same formula — assess
  extensibility by hand and crumb softness after bake
- Log core dough temperature with a probe during the warm autolyse to quantify the thermal lag
- Try direct lactic acid acidification + 40°C hold as a comparison arm (expect initial
  tightening before enzymatic softening overtakes)
- Compare crust aroma between warm-autolyse and control loaves — the Strecker/pyrazine claim
  is the least directly evidenced part of this and would benefit from a sensory check

---

<!-- nav -->
[Contents](../README.md)
