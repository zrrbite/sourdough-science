"""Reading and validating chamber.toml.

Validation is deliberately strict about the two things that burn dough or a
house: a setpoint outside the envelope the chamber was designed for, and a
cut-out that sits at or below the setpoint (which would make it fire constantly,
or never).
"""

import tomllib

W1_DEVICES = "/sys/bus/w1/devices"

SETPOINT_MIN_C = 15.0
SETPOINT_MAX_C = 55.0

DEFAULTS = {
    "band_c": 0.25,
    "min_dwell_s": 60.0,
    "max_temp_c": 55.0,
    "interval_s": 10.0,
    "control_role": "air",
    "data_dir": "runs",
}


def load_config(text):
    raw = tomllib.loads(text)
    cfg = dict(DEFAULTS)
    cfg.update(raw)

    if "setpoint_c" not in cfg:
        raise ValueError("setpoint_c is required")
    setpoint = float(cfg["setpoint_c"])
    if not (SETPOINT_MIN_C <= setpoint <= SETPOINT_MAX_C):
        raise ValueError(
            "setpoint_c {} is outside the {}-{} C envelope".format(
                setpoint, SETPOINT_MIN_C, SETPOINT_MAX_C
            )
        )
    if float(cfg["max_temp_c"]) <= setpoint:
        raise ValueError("max_temp_c must sit above setpoint_c")

    probes = cfg.get("probes") or []
    if not probes:
        raise ValueError("at least one probe must be configured")

    cfg["probes"] = [
        {
            "role": p["role"],
            "id": p["id"],
            "offset_c": float(p.get("offset_c", 0.0)),
            "device_path": p.get(
                "path", "{}/{}/w1_slave".format(W1_DEVICES, p["id"])
            ),
        }
        for p in probes
    ]

    roles = [p["role"] for p in cfg["probes"]]
    if cfg["control_role"] not in roles:
        raise ValueError(
            "control_role {!r} has no probe; configured roles are {}".format(
                cfg["control_role"], ", ".join(roles)
            )
        )

    cfg["setpoint_c"] = setpoint
    return cfg


def load_config_file(path):
    with open(path) as fh:
        return load_config(fh.read())
