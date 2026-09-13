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
- **[`ble/`](ble/)** — a broadcast-only Bluetooth probe: wire format, a simulator that runs
  the chamber's own physics, and a listener. Simulated end to end, no hardware needed. It
  exists because a wired dough-core probe means a cable through the chamber seal; a probe that
  advertises does not.
- **Full instrument** — designed, not built:
  [`../docs/superpowers/specs/2026-09-13-fermentation-chamber-design.md`](../docs/superpowers/specs/2026-09-13-fermentation-chamber-design.md).
  ESP32, PID over a PTC heater, four probes, three independent safety layers,
  and a seam for programmable profiles.

- **[`viewer/`](viewer/)** — a single page that reads a run's `samples.csv` and
  plots chamber air against dough core, with lag-to-setpoint, time-weighted mean
  core temperature and peak gradient computed from the data. Published at
  <https://claude.ai/code/artifact/2865cdf4-1ac0-433d-b3c8-a8f6e1c0c05d>; the
  source here is the same file, so it runs offline from any browser too. Opens
  on a simulated run derived from the chamber's own constants, so it shows
  something before the first real bake.

Stage 0 is a subset of that design, not a detour: the file schema, the run
manifest and the calibration discipline are identical, so runs recorded now stay
comparable with runs recorded later.
