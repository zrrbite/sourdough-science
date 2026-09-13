"""Naming the transports, so the hardware decision stays a command-line flag.

    open_source("simulated")                       # no hardware
    open_source("serial", port="/dev/tty.usbmodem") # USB device printing lines
    open_source("ble")                             # our broadcast probe
    open_source("ble", decoder="inkbird")          # somebody else's probe
    open_source("w1", ids={"air": "28-...", "core": "28-..."})
"""

from ble import BleSource
from decoders import DECODERS
from onewire import OneWireSource
from serial_line import SerialLineSource
from simulated import ProbeSimulator
from simulated_source import SimulatedSource


def _simulated(interval_s=10.0, speed=1.0, limit=None, setpoint_c=40.0,
               dough_probe=True, **_ignored):
    return SimulatedSource(
        ProbeSimulator(setpoint_c=setpoint_c, dough_probe=dough_probe),
        interval_s=interval_s, speed=speed, limit=limit)


def _ble(interval_s=10.0, limit=None, decoder="chamber", **_ignored):
    return BleSource(decoder=_decoder(decoder), interval_s=interval_s, limit=limit)


def _serial(port=None, baud=115200, stream=None, limit=None, **_ignored):
    return SerialLineSource(stream=stream, port=port, baud=baud, limit=limit)


def _w1(paths=None, ids=None, offsets=None, interval_s=10.0, limit=None, **_ignored):
    return OneWireSource(paths=paths, ids=ids, offsets=offsets,
                         interval_s=interval_s, limit=limit)


SOURCES = {
    "simulated": _simulated,
    "ble": _ble,
    "serial": _serial,
    "w1": _w1,
}


def open_source(name, **opts):
    if name not in SOURCES:
        raise ValueError("unknown source {!r}; available: {}".format(
            name, ", ".join(sorted(SOURCES))))
    return SOURCES[name](**opts)


def _decoder(name):
    if name not in DECODERS:
        raise ValueError("unknown decoder {!r}; available: {}".format(
            name, ", ".join(sorted(DECODERS))))
    return DECODERS[name]
