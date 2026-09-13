"""Reading DS18B20 probes through the kernel's 1-Wire driver.

Raspberry Pi OS exposes each probe as /sys/bus/w1/devices/28-*/w1_slave once
`dtoverlay=w1-gpio` is set, so there is nothing to install and no library to
depend on: a probe read is a file read.
"""

PLAUSIBLE_MIN_C = -10.0
PLAUSIBLE_MAX_C = 60.0


def parse_w1_slave(text):
    """Return degrees Celsius from a w1_slave dump, or None if it is not usable.

    The driver reports its own CRC check on the first line; a reading whose CRC
    failed is garbage that happens to look like a number.
    """
    lines = text.strip().splitlines()
    if len(lines) < 2 or not lines[0].rstrip().endswith("YES"):
        return None
    _, _, millidegrees = lines[1].partition("t=")
    try:
        return int(millidegrees) / 1000.0
    except ValueError:
        return None


class Probe:
    """One DS18B20, its calibration offset, and its last raw reading.

    The raw value is kept so a run stays interpretable if the offset later turns
    out to be wrong — see the spec's future-proofing contract.
    """

    def __init__(
        self,
        role,
        device_path,
        offset_c=0.0,
        min_c=PLAUSIBLE_MIN_C,
        max_c=PLAUSIBLE_MAX_C,
    ):
        self.role = role
        self.device_path = device_path
        self.offset_c = offset_c
        self.min_c = min_c
        self.max_c = max_c
        self.raw_c = None

    def read(self):
        """Return the calibrated temperature, or None if the reading is unusable."""
        try:
            with open(self.device_path) as fh:
                text = fh.read()
        except OSError:
            self.raw_c = None
            return None

        raw = parse_w1_slave(text)
        self.raw_c = raw
        if raw is None or not (self.min_c <= raw <= self.max_c):
            return None
        return raw + self.offset_c
