# The Levain Doubling Test: Bench Protocol

> **Context.** Chapter 08 poses two explanations for why a pure sourdough culture leavens
> bread after hot builds — genuine thermotolerance, or temporal escape — and names a test to
> separate them. [Why the Hot Protocol Works](why-the-hot-protocol-works.md) takes a position
> on that question and identifies this as the experiment that would falsify it. This note is
> the protocol, written to be followed at the bench rather than read.
>
> It needs a thermometer, two jars and a rubber band. **It does not need the chamber**, though
> a core probe removes its largest confound.

---

## What this actually tests — and the correction

Chapter 08 states that if the levain doubles during a hot build, *"the yeast are reproducing
at 40°C — definitive evidence of thermotolerance."*

**That is too strong.** Doubling demonstrates gas production, not cell division. A
heat-stressed, non-dividing yeast population is still metabolically active — it still
ferments sugar and still evolves CO₂. That is precisely what Hypothesis 2 (temporal escape)
predicts: a population on its way out can leaven a jar on the way.

So the test resolves as:

| Observation during a hot build | What it supports |
|---|---|
| Strong, prompt rise comparable to the control | Yeast metabolically active at temperature. **Consistent with either hypothesis.** |
| Acid and aroma develop, little or no expansion | LAB active, yeast not contributing gas. Points to temporal escape. |
| Rise markedly slower than the control | Yeast impaired but functional. Points to temporal escape. |

A negative result is therefore informative and a positive result is not decisive. For the
decisive version, see *Serial hot passage* below.

---

## Protocol

### Setup

- [ ] **Two jars, one feed.** Same mother, same ratio, mixed at the same moment, divided into
      two identical vessels. One goes hot, one is the control. **Weigh both** — equal mass
      matters more than a round number, because mass is what drives the thermal lag the hot
      jar is being tested for.
- [ ] **A control jar at room temperature.** Without it, "it doubled" has no scale — doubling
      in one hour and doubling in four mean opposite things, and only the control says which
      this culture does normally on this feed.

      The control does **not** need to sit at some particular warm temperature, and should not
      be made to: there is one oven, so manufacturing a second controlled warm spot introduces
      a variable rather than removing one. What the control must be is *un-stressed and
      recorded*. Room temperature qualifies. Put a thermometer beside it and write the number
      down — a control at 21°C with the figure noted is worth more than one at a nominal 26°C
      that was never measured.
- [ ] **Straight-sided, tall, narrow jars**, identical to each other. Height stands in for
      volume, so geometry must match.
- [ ] **Rubber band at the start line** on both.
- [ ] **Feed the mother the day before.** Chapter 11's first mitigation: a hot session lands
      best on a culture with full substrate and minimal accumulated acid and ethanol. It also
      makes the two jars comparable to anything run later.

### During

- [ ] **Height on both jars every 15 minutes.** A photo with a ruler in frame beats a written
      number and takes less time.
- [ ] **Oven air temperature at each check.** A domestic oven cycles; a single spot reading
      is not a hold.
- [ ] **Core temperature if a probe is available.** This is the largest confound in the whole
      experiment — see below.
- [ ] **Run until the hot jar peaks and begins to recede**, not to a fixed clock time. Peak
      timing is itself a result.

### Record before you start

Five things, or run two is not comparable with run one:

1. Mother source, and when it was last fed
2. Feed ratio and total mass per jar
3. Temperature of the mix as it goes in
4. Jar geometry — diameter and fill height, and the mass in each jar
5. Oven setting, and whether the cavity is otherwise empty
6. The control's actual temperature, measured rather than assumed

---

## The confound: the jar is not the oven

The jar is the *right* vessel for this test, which is a point in its favour. A 75 g levain
warms through in a small fraction of an hour, where a 1 kg tub does not (ch. 10) — so at jar
scale the culture really does spend most of a one-hour build near air temperature.

But "most" is the operative word, and it is unmeasured. If the jar takes 20 minutes to arrive
at 45°C, a third of a one-hour build happened on the ramp. That matters twice over: it
shortens the effective exposure, and the ramp itself is protective (ch. 11). A core probe in
the hot jar turns that from an assumption into a number, and it is the reason this test sits
first in the chamber's experiment programme.

---

## Serial hot passage — the decisive version

If the doubling test gives a positive result, it has not distinguished the hypotheses. This
does, and it is only arithmetic.

At a 1:1:1 feed the incoming starter is one third of the new mass. **If the yeast are not
dividing, cell count per gram falls to (⅓)ⁿ after n builds** — a twenty-seventh by the third,
under a two-hundredth by the fifth. Leavening power falls with it.

- [ ] Run **five consecutive hot builds**, backslopping each time **from the hot jar** — not
      from the fridge, not from the mother.
- [ ] Same ratio, same duration, same setpoint each cycle.
- [ ] Time each build to peak, and compare build five against build one.

If build five still rises like build one, the population is replenishing itself. There is no
way to survive that dilution otherwise, and that is reproduction at temperature.

### Do this on a split lineage

Chapter 08 is explicit that serial passage under thermal selection progressively reshapes a
culture, favouring thermotolerant organisms and narrowing diversity over 10–20 cycles. Five
cycles is milder than that, but the direction is the same, and chapter 11 makes the case for
a room-temperature backup precisely so an experiment like this is survivable.

**Split off a test jar. Do not run this on the only culture in the house.**

---

## Related

- Chapter 08 for the two hypotheses and the original framing of this test.
- Chapter 11 for why feeding before heat matters, and for the ramp effect that the jar's
  warm-up period invokes.
- Chapter 10 for the thermal lag that makes jar scale and tub scale different experiments.
- [Why the Hot Protocol Works](why-the-hot-protocol-works.md) for the position this test would
  falsify.
- [The Heat-Driven Levain Bank](heat-driven-levain-bank.md) for the protocol these jars are
  drawn from, and the 2026-09-13 oven-air measurement.
- [`chamber/`](../chamber/) for the instrument that removes the core-temperature confound.

---

<!-- nav -->
[Contents](../README.md)
