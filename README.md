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

### Foundations

| # | Chapter |
|---|---|
| 01 | [What Is a Preferment?](docs/01-what-is-a-preferment.md) |
| 02 | [The Four Quadrants](docs/02-the-four-quadrants.md) |
| 03 | [Microbiology: Monoculture vs. Mixed Consortium](docs/03-microbiology-monoculture-vs-mixed-consortium.md) |
| 04 | [Acidity: Lactic vs. Acetic and the Hydration Effect](docs/04-acidity-lactic-vs-acetic-and-the-hydration-effect.md) |

### Gluten

| # | Chapter |
|---|---|
| 05 | [Gluten: Structure, Modification, and Why It Matters](docs/05-gluten-structure-modification-and-why-it-matters.md) |
| 06 | [Time-Dependent Gluten Development](docs/06-time-dependent-gluten-development-why-folding-is-a-shortcut-.md) |

### Thermal

| # | Chapter |
|---|---|
| 07 | [Thermal Management: Heat-Stressed Fermentation as a Flavour Tool](docs/07-thermal-management-heat-stressed-fermentation-as-a-flavour-t.md) |
| 08 | [Empirical Evidence: Pure Sourdough at 40°C+](docs/08-empirical-evidence-pure-sourdough-at-40c.md) |
| 09 | [The Kveik Parallel: Domestication Through Selective Pressure](docs/09-the-kveik-parallel-domestication-through-selective-pressure.md) |
| 10 | [Thermal Lag: The Oven Setpoint Is Not the Dough Temperature](docs/10-thermal-lag-the-oven-setpoint-is-not-the-dough-temperature.md) |

### Flavour Chemistry

| # | Chapter |
|---|---|
| 12 | [The Hybrid Approach: Commercial Yeast + Sourdough Levain](docs/12-the-hybrid-approach-commercial-yeast-sourdough-levain.md) |
| 13 | [Ester Chemistry: Where Brewing Meets Baking](docs/13-ester-chemistry-where-brewing-meets-baking.md) |
| 14 | [Why Cold Ferment With Commercial Yeast at All?](docs/14-why-cold-ferment-with-commercial-yeast-at-all.md) |

### Application

| # | Chapter |
|---|---|
| 15 | [Application: Pizza Dough](docs/15-application-pizza-dough.md) |
| 16 | [The Long Fermentation Problem in Pizza](docs/16-the-long-fermentation-problem-in-pizza.md) |
| 17 | [Controlled Proteolysis for Bread: Degradation as a Tool](docs/17-controlled-proteolysis-for-bread-degradation-as-a-tool.md) |
| 18 | [High-Heat Baking: Sugar, Hydration, and the Ooni Problem](docs/18-high-heat-baking-sugar-hydration-and-the-ooni-problem.md) |
| 19 | [Post-Retard Handling: CO₂ Nucleation and the Gentle Pull](docs/19-post-retard-handling-co2-nucleation-and-the-gentle-pull.md) |
| 20 | [Oven Spring Mechanics: What Actually Determines Rise](docs/20-oven-spring-mechanics-what-actually-determines-rise.md) |

### Practical

| # | Chapter |
|---|---|
| 21 | [Flour Selection: Why Protein Percentage Is Not Enough](docs/21-flour-selection-why-protein-percentage-is-not-enough.md) |
| 22 | [Practical Ratios and Formulas](docs/22-practical-ratios-and-formulas.md) |
| 23 | [Quick Reference: Home Oven vs. Ooni 12"](docs/23-quick-reference-home-oven-vs-ooni-12.md) |
| 24 | [Quick Reference: Preferment Comparison](docs/24-quick-reference-preferment-comparison.md) |
| 25 | [References](docs/25-references.md) |

### Notes

- [Accelerating Proteolysis: pH, Heat, and Salt](notes/proteolysis-ph-heat.md) — working notes on
  whether a heat boost can substitute for long fermentation in driving protease activity.

---

## Equipment and materials this is written around

- **Ovens:** domestic oven to 300°C; Ooni 12" gas
- **Flour:** Caputo Oro Manitoba (W 350–380+) as the reference; comparisons to generic
  "Manitoba" at ~13% protein
- **Culture:** pure sourdough, maintained warm, repeatedly built at 40°C+
- **Retard:** domestic fridge at 3–5°C

Formulas and temperatures assume this setup. Adjust accordingly.

---

## Conventions

- **Empirical vs. literature.** Where my own results contradict published findings, both are
  stated and the conflict is left open rather than resolved. See chapter 08 in particular.
- **Contested evidence is flagged inline**, not hidden. Chapter 13 carries a note on
  conflicting ester/temperature findings; chapter 25 carries one on chemical vs. biological
  acidification.
- **Baker's percentages** throughout, on total flour including levain flour unless stated.
- **Temperatures in °C.** Hydration figures state whether they include levain contribution.

---

## Building

Markdown is the source of truth. To produce a single PDF or DOCX:

```sh
make pdf     # -> build/sourdough-science.pdf
make docx    # -> build/sourdough-science.docx
make single  # -> build/sourdough-science.md  (concatenated)
```

Requires `pandoc`; PDF additionally requires a LaTeX engine (`xelatex`).

---

## Status and open threads

This is a live document, not a finished text. Things currently unresolved:

- **Thermotolerance vs. temporal escape** (ch. 08) — is the culture genuinely heat-adapted, or
  merely escaping via short exposure and thermal lag? The extended-bulk test described in
  ch. 08 would distinguish these and has not been run.
- **Ester/temperature direction** (ch. 13) — the literature genuinely conflicts. Needs a
  side-by-side taste test against a room-temperature control.
- **Strecker/pyrazine crust claim** (ch. 17) — the least directly evidenced claim in the
  document. Wants a sensory comparison.
- **Structural reorganisation** — chapter order still reflects how the document grew rather
  than how it reads. Foundations → science → application → formulas would be better.
