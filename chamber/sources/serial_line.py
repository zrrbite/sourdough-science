"""A USB device that prints readings, one per line.

The line format is deliberately stupid so that a handful of lines of Arduino or
ESP sketch feeds the whole system:

    air=40.29,core=36.71,heating=1

Unparseable lines are skipped rather than fatal, because every device in the
world prints a boot banner.
"""

import os
import stat
import time

from base import Source, reading
from decoders import decode_line


class SerialLineSource(Source):
    name = "serial"

    def __init__(self, stream=None, port=None, baud=115200, limit=None, timeout=2.0):
        self.limit = limit
        self._own_stream = stream is None
        if stream is not None:
            self.stream = stream
        else:
            self.stream = _open_port(port, baud, timeout)

    def readings(self):
        started = time.monotonic()
        emitted = 0
        for line in self.stream:
            if isinstance(line, bytes):
                line = line.decode("utf-8", "replace")
            decoded = decode_line(line)
            if decoded is None:
                continue
            yield reading(
                t_s=time.monotonic() - started,
                air_c=decoded["air_c"],
                core_c=decoded["core_c"],
                heating=decoded["heating"],
                seq=decoded["seq"],
                battery_pct=decoded["battery_pct"],
                setpoint_c=decoded["setpoint_c"],
            )
            emitted += 1
            if self.limit is not None and emitted >= self.limit:
                return

    def close(self):
        if self._own_stream and hasattr(self.stream, "close"):
            self.stream.close()


def _open_port(port, baud, timeout):
    """Open a real serial device, or a plain file standing in for one.

    A serial port is a character device. Anything else that exists - a regular
    file, a FIFO - is opened directly, which means the line protocol can be
    exercised with `printf` long before any hardware is chosen.
    """
    if not port:
        raise ValueError("serial source needs either a stream or a port")
    if os.path.exists(port) and not stat.S_ISCHR(os.stat(port).st_mode):
        return open(port)
    if not os.path.exists(port):
        raise FileNotFoundError("no such serial device: {}".format(port))
    try:
        import serial  # pyserial
    except ImportError:
        raise SystemExit("the serial source needs pyserial: pip install pyserial")
    return serial.Serial(port, baud, timeout=timeout)
