"""One run on disk: a directory holding samples.csv and manifest.json.

The file layout is the artifact that outlives this code, so it is deliberately
dull: plain CSV, plain JSON, a schema_version on both, and one column per probe
role so adding a probe adds a column rather than breaking a reader.

Raw readings are not stored separately. Every offset is recorded in the
manifest and applied additively, so raw = logged - offset exactly, and nothing
is lost by keeping one number per probe.
"""

import json
import os
import secrets
from datetime import datetime, timedelta, timezone

SCHEMA_VERSION = 1


def _iso(moment):
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _num(value):
    return "" if value is None else str(round(value, 3))


class Run:
    def __init__(
        self,
        root_dir,
        setpoint_c,
        probe_roles,
        run_id=None,
        started_utc=None,
        probes_meta=None,
        load=None,
        control=None,
    ):
        self.started_utc = started_utc or datetime.now(timezone.utc)
        self.run_id = run_id or "{}_{}".format(
            self.started_utc.strftime("%Y-%m-%dT%H-%M-%SZ"), secrets.token_hex(2)
        )
        self.probe_roles = list(probe_roles)
        self.setpoint_c = setpoint_c
        self.path = os.path.join(root_dir, self.run_id)
        os.makedirs(self.path, exist_ok=True)

        self._manifest = {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "started_utc": _iso(self.started_utc),
            "ended_utc": None,
            "setpoint": {"type": "constant", "value_c": setpoint_c},
            "control": dict({"law": "hysteresis"}, **(control or {})),
            "probes": probes_meta or [],
            "load": load or {},
        }
        self._write_manifest()

        self._samples = open(os.path.join(self.path, "samples.csv"), "a")
        self._write(
            ["seq", "t_s", "iso_utc", "setpoint_c"]
            + ["{}_c".format(role) for role in self.probe_roles]
            + ["heating", "flags"]
        )

    def append(self, seq, t_s, temps, heating, flags=None):
        """Write one sample. Flushed immediately: a crash costs one row, not a run."""
        stamp = self.started_utc + timedelta(seconds=t_s)
        self._write(
            [str(seq), _num(t_s), _iso(stamp), _num(self.setpoint_c)]
            + [_num(temps.get(role)) for role in self.probe_roles]
            + ["1" if heating else "0", "|".join(flags or [])]
        )

    def close(self, ended_utc=None):
        self._manifest["ended_utc"] = _iso(ended_utc or datetime.now(timezone.utc))
        self._write_manifest()
        self._samples.close()

    def _write(self, fields):
        self._samples.write(",".join(fields) + "\n")
        self._samples.flush()

    def _write_manifest(self):
        with open(os.path.join(self.path, "manifest.json"), "w") as fh:
            json.dump(self._manifest, fh, indent=2)
            fh.write("\n")
