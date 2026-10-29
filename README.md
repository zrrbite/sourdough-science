# Sourdough Science

A working reference on preferment selection and fermentation science, developed around a
single applied question: **how to make the best possible pizza in a domestic oven and a
12" Ooni** — and, latterly, how the same mechanisms apply to bread.

The document moves from preferment taxonomy and microbiology through gluten chemistry,
thermal management of fermentation, and oven-spring mechanics, to concrete formulas.
Empirical observations from my own experiments are presented alongside the published
literature, and **flagged as such wherever the two diverge**.

---

## Contents

Read in order if you are reading it whole — the chapters are a chain, and most
open by building on the one before. Jump straight in if you are looking
something up; every chapter carries prev/next links back to this page.

### Part I — Foundations

What a preferment is, and the two axes that distinguish them.

| # | Chapter |
|---|---|
| 01 | [What Is a Preferment?](docs/01-what-is-a-preferment.md) |
| 02 | [The Four Quadrants](docs/02-the-four-quadrants.md) |
| 03 | [Microbiology: Monoculture vs. Mixed Consortium](docs/03-microbiology-monoculture-vs-mixed-consortium.md) |
| 04 | [Acidity: Lactic vs. Acetic and the Hydration Effect](docs/04-acidity-lactic-vs-acetic-and-the-hydration-effect.md) |

### Part II — The Science

Mechanism: what acid, enzymes and heat actually do to a dough and a culture.

**Gluten**

| # | Chapter |
|---|---|
| 05 | [Gluten: Structure, Modification, and Why It Matters](docs/05-gluten-structure-modification-and-why-it-matters.md) |
| 06 | [Time-Dependent Gluten Development](docs/06-time-dependent-gluten-development.md) |

**Thermal**

| # | Chapter |
|---|---|
| 07 | [Thermal Management: Heat-Stressed Fermentation as a Flavour Tool](docs/07-thermal-management-heat-stressed-fermentation.md) |
| 08 | [Empirical Evidence: Pure Sourdough at 40°C+](docs/08-empirical-evidence-pure-sourdough-at-40c.md) |
| 09 | [The Kveik Parallel: Domestication Through Selective Pressure](docs/09-the-kveik-parallel-domestication-through-selective-pressure.md) |
| 10 | [Thermal Lag: The Oven Setpoint Is Not the Dough Temperature](docs/10-thermal-lag-the-oven-setpoint-is-not-the-dough-temperature.md) |
| 11 | [Thermal Death Kinetics and Culture Recovery](docs/11-thermal-death-kinetics-and-culture-recovery.md) |

### Part III — Application

Turning the mechanism into a strategy, then into a bake.

**Strategy and flavour chemistry**

| # | Chapter |
|---|---|
| 12 | [The Hybrid Approach: Commercial Yeast + Sourdough Levain](docs/12-the-hybrid-approach-commercial-yeast-sourdough-levain.md) |
| 13 | [Ester Chemistry: Where Brewing Meets Baking](docs/13-ester-chemistry-where-brewing-meets-baking.md) |
| 14 | [Why Cold Ferment With Commercial Yeast at All?](docs/14-why-cold-ferment-with-commercial-yeast-at-all.md) |

**Pizza and bread**

| # | Chapter |
|---|---|
| 15 | [Application: Pizza Dough](docs/15-application-pizza-dough.md) |
| 16 | [The Long Fermentation Problem in Pizza](docs/16-the-long-fermentation-problem-in-pizza.md) |
| 17 | [Controlled Proteolysis for Bread: Degradation as a Tool](docs/17-controlled-proteolysis-for-bread-degradation-as-a-tool.md) |
| 18 | [High-Heat Baking: Sugar, Hydration, and the Ooni Problem](docs/18-high-heat-baking-sugar-hydration-and-the-ooni-problem.md) |
| 19 | [Post-Retard Handling: CO₂ Nucleation and the Gentle Pull](docs/19-post-retard-handling-co2-nucleation-and-the-gentle-pull.md) |
| 20 | [Oven Spring Mechanics: What Actually Determines Rise](docs/20-oven-spring-mechanics-what-actually-determines-rise.md) |

### Part IV — Practical and Formulas

The lookup end of the document: what to buy, what to weigh, what to check.

| # | Chapter |
|---|---|
| 21 | [Flour Selection: Why Protein Percentage Is Not Enough](docs/21-flour-selection-why-protein-percentage-is-not-enough.md) |
| 22 | [Practical Ratios and Formulas](docs/22-practical-ratios-and-formulas.md) |
| 23 | [Quick Reference: Home Oven vs. Ooni 12"](docs/23-quick-reference-home-oven-vs-ooni-12.md) |
| 24 | [Quick Reference: Preferment Comparison](docs/24-quick-reference-preferment-comparison.md) |
| 25 | [References](docs/25-references.md) |

### Notes

- [Starting a Starter From Scratch](notes/starter-from-scratch.md) — the step before every
  chapter: Full Proof Baking's 14-day method day by day, in grams and hours, alongside the
  microbial succession it follows (the early rise is bacteria, the day-5 lull is the hand-over),
  and the culture it ends in: who lives there, how one-sided the partnership is, and when it is
  settled, ready and at its best.
  Also why to start warm but not hot, what changes for this kitchen, and how to dry a backup
  and revive it (a pinch, not a spoonful). The schedule on one printable A4 page: [cheat
  sheet](notes/starter-cheatsheet.pdf).
- [Accelerating Proteolysis: pH, Heat, and Salt](notes/proteolysis-ph-heat.md) — working notes on
  whether a heat boost can substitute for long fermentation in driving protease activity.
- [The Heat-Driven Levain Bank](notes/heat-driven-levain-bank.md) — the protocol as currently
  run: levains built hot and banked cold for days, refed hot with wholegrain on bake day, a hot
  pulse after mixing, then an overnight cold rest *before* bulk. Mechanism hypotheses and open tests.
- [The Levain Doubling Test](notes/levain-doubling-test.md) — bench protocol for the
  experiment that would settle ch. 08's open question, with the correction that doubling shows
  gas production rather than cell division, and serial hot passage as the decisive version.
- [Why the Hot Protocol Works](notes/why-the-hot-protocol-works.md) — why fermenting above
  conventional guidance keeps working. Argues the 28°C question dissolves (nothing is stressed
  there, and the norm is a scheduling convention), and that the 40–50°C case is six ordinary
  effects compounding rather than an unusual culture. Takes a position on ch. 08's open question.

### Slides

One Beamer deck per part, for bakers who like science: practical points first, each with
its mechanism and source. [Foundations](slides/01-foundations.pdf) ·
[The Science](slides/02-the-science.pdf) · [Application](slides/03-application.pdf) ·
[Practical](slides/04-practical.pdf) · [Starters](slides/05-starters.pdf). Sources are in
[`slides/`](slides/); `make` there rebuilds them with [Tectonic](https://tectonic-typesetting.github.io/).

---

## Equipment and materials this is written around

- **Ovens:** domestic oven to 300°C; Ooni 12" gas
- **Flour:** Caputo Oro Manitoba (W 350–380+) as the reference; comparisons to generic
  "Manitoba" at ~13% protein
- **Culture:** pure sourdough, maintained warm, repeatedly built at 40°C+
- **Retard:** domestic fridge at 3–5°C
- **Measurement:** oven air measured at ~45°C on the usual setting (2026-09-13).
  A logging chamber is designed and its first stage built — see
  [`chamber/`](chamber/) — but nothing is instrumented yet, so every temperature
  in this document is still a setpoint rather than a reading.

Formulas and temperatures assume this setup. Adjust accordingly.

---

## Conventions

- **Empirical vs. literature.** Where my own results contradict published findings, both are
  stated and the conflict is left open rather than resolved. See chapter 08 in particular.
- **Contested evidence is flagged inline**, not hidden. Chapter 07 carries a note on
  conflicting ester/temperature findings; chapter 25 carries one on chemical vs. biological
  acidification.
- **Baker's percentages** throughout, on total flour including levain flour unless stated.
- **Temperatures in °C.** Hydration figures state whether they include levain contribution.

---

## Format

**The document** is markdown and nothing else. There is no build step and no
generated PDF or DOCX — it is meant to be browsed and searched a chapter at a
time, on GitHub or in an editor, which is how it actually gets used. The
consequence to be aware of: **chapter order is load-bearing.** Most chapters
open by referring to the one before, so moving a file means rewriting its first
paragraph.

**[`slides/`](slides/) is derived from the document, not part of it.** Each deck
summarises one part, and its PDF is built with Tectonic from the `.tex` source next
to it. A deck can lag behind a chapter that changes after it was written; where
they disagree, the chapter wins.

**[`chamber/`](chamber/) is a project, not prose**, and has its own toolchain —
Python, tests, a systemd unit. It is kept here rather than in its own repository
because its whole purpose is to answer questions chapters 08, 10 and 11 leave
open, and the run data belongs next to the argument it settles.

---

## Status and open threads

This is a live document, not a finished text. Things currently unresolved:

- **Thermotolerance vs. temporal escape** (ch. 08) — is the culture genuinely heat-adapted, or
  merely escaping via short exposure and thermal lag? [Why the Hot Protocol
  Works](notes/why-the-hot-protocol-works.md) now argues for the second, as one term in a
  six-effect stack — but that is a stated bet, not a result. The decisive test is whether a
  levain **doubles** during a hot build; the extended-bulk test in ch. 08 is the confirmatory
  one. Neither has been run, and [`chamber/`](chamber/) exists to run them.
- **Post-recovery culture assessment** (ch. 11) — the recovered culture has not yet been
  compared against a control on thermotolerance, flavour, and vigour.
- **Ester/temperature direction** (ch. 07) — the literature genuinely conflicts. Needs a
  side-by-side taste test against a room-temperature control.
- **Strecker/pyrazine crust claim** (ch. 17) — the least directly evidenced claim in the
  document. Wants a sensory comparison.
- **Structural reorganisation** — partly settled. The contents above are now grouped
  Foundations → science → application → formulas, which is what this wanted. What was *not*
  done is renumbering the files, and there is a reason: the chapters are welded into a chain
  by their opening sentences — 04→05→06, 07→08→09→10→11, 12→13→14, 16→17, 19→20 each
  back-reference the chapter before, and ch. 25 groups its references "by the section of this
  document". Only 01, 02, 03, 15, 18 and 21–24 could move freely. A physical reorder is
  therefore a prose edit, not a file rename, and is still open if it ever seems worth it.
