# Chamber

A temperature-controlled, logging fermentation environment for the experiments
this repository keeps describing and not running.

The point is the measurement, not the heat. An oven heats perfectly well; what
it cannot do is tell you what temperature the dough actually reached — which is
the quantity ch. 07–11 and [`../notes/heat-driven-levain-bank.md`](../notes/heat-driven-levain-bank.md)
are all arguing about.

- **[`stage0/`](stage0/)** — built now. Pi + ceramic heat emitter + smart plug +
  an insulated box, ~€45. Holds a setpoint with hysteresis and logs air and
  dough-core temperature to CSV. Start here.
- **Full instrument** — designed, not built:
  [`../docs/superpowers/specs/2026-09-13-fermentation-chamber-design.md`](../docs/superpowers/specs/2026-09-13-fermentation-chamber-design.md).
  ESP32, PID over a PTC heater, four probes, three independent safety layers,
  and a seam for programmable profiles.

Stage 0 is a subset of that design, not a detour: the file schema, the run
manifest and the calibration discipline are identical, so runs recorded now stay
comparable with runs recorded later.
