import io
import os
import tempfile
import unittest

from onewire import OneWireSource
from registry import SOURCES, open_source
from serial_line import SerialLineSource
from simulated import ProbeSimulator
from simulated_source import SimulatedSource

W1_BODY = ("d8 01 4b 46 7f ff 0c 10 2e : crc=2e YES\n"
           "d8 01 4b 46 7f ff 0c 10 2e t={}\n")


def w1_file(celsius):
    path = os.path.join(tempfile.mkdtemp(), "w1_slave")
    with open(path, "w") as fh:
        fh.write(W1_BODY.format(int(celsius * 1000)))
    return path


class TestSimulatedSource(unittest.TestCase):
    def test_it_yields_readings_with_advancing_time(self):
        src = SimulatedSource(ProbeSimulator(), interval_s=20, speed=0, limit=3)
        times = [r["t_s"] for r in src.readings()]
        self.assertEqual(times, [20.0, 40.0, 60.0])

    def test_it_stops_at_the_limit(self):
        src = SimulatedSource(ProbeSimulator(), interval_s=20, speed=0, limit=5)
        self.assertEqual(len(list(src.readings())), 5)

    def test_readings_round_trip_through_the_real_wire_format(self):
        src = SimulatedSource(ProbeSimulator(), interval_s=20, speed=0, limit=1)
        reading = next(iter(src.readings()))
        # centidegree resolution is the wire format's, not the model's
        self.assertEqual(round(reading["air_c"], 2), reading["air_c"])

    def test_it_carries_the_setpoint_through(self):
        src = SimulatedSource(ProbeSimulator(setpoint_c=42.0), interval_s=20,
                              speed=0, limit=1)
        self.assertEqual(next(iter(src.readings()))["setpoint_c"], 42.0)


class TestSerialLineSource(unittest.TestCase):
    def test_it_reads_readings_from_a_stream(self):
        stream = io.StringIO("air=24.0,core=22.0\nair=25.0,core=22.5\n")
        readings = list(SerialLineSource(stream=stream, limit=2).readings())
        self.assertAlmostEqual(readings[1]["air_c"], 25.0)

    def test_it_skips_lines_it_cannot_read(self):
        stream = io.StringIO("booting...\nair=24.0,core=22.0\n")
        readings = list(SerialLineSource(stream=stream, limit=1).readings())
        self.assertEqual(len(readings), 1)
        self.assertAlmostEqual(readings[0]["air_c"], 24.0)

    def test_it_stamps_elapsed_time_on_arrival(self):
        stream = io.StringIO("air=24.0\nair=25.0\n")
        readings = list(SerialLineSource(stream=stream, limit=2).readings())
        self.assertGreaterEqual(readings[1]["t_s"], readings[0]["t_s"])

    def test_it_ends_when_the_stream_does(self):
        stream = io.StringIO("air=24.0\n")
        self.assertEqual(len(list(SerialLineSource(stream=stream).readings())), 1)


class TestOneWireSource(unittest.TestCase):
    def test_it_reads_the_configured_probes(self):
        src = OneWireSource(paths={"air": w1_file(40.0), "core": w1_file(33.5)},
                            interval_s=0, limit=1)
        reading = next(iter(src.readings()))
        self.assertAlmostEqual(reading["air_c"], 40.0)
        self.assertAlmostEqual(reading["core_c"], 33.5)

    def test_a_missing_probe_reads_as_none(self):
        src = OneWireSource(paths={"air": w1_file(40.0), "core": "/nope/w1_slave"},
                            interval_s=0, limit=1)
        self.assertIsNone(next(iter(src.readings()))["core_c"])

    def test_it_applies_calibration_offsets(self):
        src = OneWireSource(paths={"air": w1_file(40.0)},
                            offsets={"air": -0.25}, interval_s=0, limit=1)
        self.assertAlmostEqual(next(iter(src.readings()))["air_c"], 39.75)


class TestRegistry(unittest.TestCase):
    def test_every_transport_is_registered(self):
        for name in ("simulated", "ble", "serial", "w1"):
            self.assertIn(name, SOURCES)

    def test_it_builds_a_simulated_source(self):
        src = open_source("simulated", limit=1, speed=0)
        self.assertIsInstance(src, SimulatedSource)

    def test_an_unknown_source_names_the_ones_that_exist(self):
        with self.assertRaises(ValueError) as caught:
            open_source("carrier-pigeon")
        self.assertIn("simulated", str(caught.exception))

class TestSerialFromAFile(unittest.TestCase):
    """A plain file or FIFO stands in for a serial device, so the USB line
    protocol can be exercised before any hardware exists."""

    def test_it_reads_a_plain_file_as_if_it_were_a_port(self):
        path = os.path.join(tempfile.mkdtemp(), "probe")
        with open(path, "w") as fh:
            fh.write("booting\nair=40.1,core=36.2\nair=40.3,core=36.4\n")
        readings = list(SerialLineSource(port=path).readings())
        self.assertEqual(len(readings), 2)
        self.assertAlmostEqual(readings[1]["core_c"], 36.4)

    def test_a_port_that_does_not_exist_is_reported_clearly(self):
        with self.assertRaises(Exception) as caught:
            SerialLineSource(port="/dev/nonexistent-probe")
        self.assertIn("nonexistent-probe", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
