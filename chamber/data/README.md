# Run data

One directory per run: `manifest.json` (setpoint, control settings, probe ids and
calibration offsets, and the load block describing the dough) and `samples.csv`
(one row per sample).

Committed on purpose. The document's convention is that empirical claims are
checkable, and a claim about dough temperature is only checkable if the curve
behind it is here. At roughly 100 KB gzipped per run-day, the cost is nil.

Schema and field meanings: [`../stage0/README.md`](../stage0/README.md).
