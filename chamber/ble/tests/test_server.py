import json
import unittest
import urllib.error
import urllib.request

from server import start_server
from telemetry import TelemetryBuffer


def reading(t_s=0.0, air=24.0, core=22.0):
    return {"seq": 1, "t_s": t_s, "air_c": air, "core_c": core,
            "heating": True, "battery_pct": 99, "setpoint_c": 40.0}


class TestLocalServer(unittest.TestCase):
    def setUp(self):
        self.buffer = TelemetryBuffer(run_id="srv")
        self.server = start_server(0, self.buffer, viewer_html="<title>viewer</title>")
        self.addCleanup(self.server.shutdown)
        self.port = self.server.server_address[1]

    def get(self, path):
        with urllib.request.urlopen("http://127.0.0.1:{}{}".format(self.port, path)) as r:
            return r.status, r.read().decode()

    def test_telemetry_endpoint_serves_the_current_documents(self):
        self.buffer.add(reading(air=33.5))
        _, body = self.get("/telemetry.json")
        self.assertAlmostEqual(json.loads(body)["current"]["air_c"], 33.5)

    def test_telemetry_reflects_later_readings_without_a_restart(self):
        self.buffer.add(reading(air=30.0))
        self.get("/telemetry.json")
        self.buffer.add(reading(air=35.0))
        _, body = self.get("/telemetry.json")
        self.assertAlmostEqual(json.loads(body)["current"]["air_c"], 35.0)

    def test_telemetry_is_served_as_json(self):
        with urllib.request.urlopen(
            "http://127.0.0.1:{}/telemetry.json".format(self.port)
        ) as r:
            self.assertEqual(r.headers["Content-Type"], "application/json")

    def test_root_serves_the_viewer(self):
        status, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn("<title>viewer</title>", body)

    def test_an_unknown_path_is_a_404(self):
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.get("/nope")
        self.assertEqual(caught.exception.code, 404)

    def test_it_serves_an_empty_buffer_without_failing(self):
        _, body = self.get("/telemetry.json")
        self.assertTrue(json.loads(body)["current"]["stale"])


if __name__ == "__main__":
    unittest.main()
