"""What every source has to be, and nothing more.

A source yields reading dicts. That is the entire contract, and it is what lets
the hardware question stay open: BLE, USB serial, a wired DS18B20 and a
simulator are four sources, and everything downstream - the telemetry buffer,
the server, the terminal app, the viewer - has never heard of any of them.

A reading:

    {"t_s": 120.0, "air_c": 40.29, "core_c": 36.71, "heating": False,
     "seq": 14, "battery_pct": 97, "setpoint_c": 40.0}

`t_s` and `air_c` are required; everything else is optional and may be None.
"""


class Source:
    name = "source"

    def readings(self):
        """Yield reading dicts until exhausted or stopped."""
        raise NotImplementedError

    def close(self):
        pass

    def __iter__(self):
        return iter(self.readings())


def reading(t_s, air_c, core_c=None, heating=False, **extra):
    """Build a reading, so every source produces the same shape."""
    out = {"t_s": t_s, "air_c": air_c, "core_c": core_c, "heating": bool(heating)}
    out.update({k: v for k, v in extra.items() if v is not None})
    return out
