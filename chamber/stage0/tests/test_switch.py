import http.server
import threading
import unittest

from switch import HttpSwitch, NullSwitch


class _Server:
    """A real HTTP server on a throwaway port, so nothing here is mocked."""

    def __init__(self, status=200):
        requested = self.requested = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                requested.append(self.path)
                self.send_response(status)
                self.end_headers()
                self.wfile.write(b"ok")

            def log_message(self, *args):
                pass

        self.httpd = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def url(self, path):
        return "http://127.0.0.1:{}{}".format(self.port, path)

    def stop(self):
        self.httpd.shutdown()


class TestHttpSwitch(unittest.TestCase):
    def _switch(self, server):
        return HttpSwitch(
            on_url=server.url("/relay/0?turn=on"),
            off_url=server.url("/relay/0?turn=off"),
        )

    def test_turning_on_requests_the_on_url(self):
        s = _Server()
        self.addCleanup(s.stop)
        self._switch(s).set(True)
        self.assertEqual(s.requested, ["/relay/0?turn=on"])

    def test_turning_off_requests_the_off_url(self):
        s = _Server()
        self.addCleanup(s.stop)
        self._switch(s).set(False)
        self.assertEqual(s.requested, ["/relay/0?turn=off"])

    def test_reports_success(self):
        s = _Server()
        self.addCleanup(s.stop)
        self.assertTrue(self._switch(s).set(True))

    def test_a_server_error_is_reported_not_raised(self):
        s = _Server(status=500)
        self.addCleanup(s.stop)
        self.assertFalse(self._switch(s).set(True))

    def test_an_unreachable_plug_is_reported_not_raised(self):
        s = _Server()
        port = s.port
        s.stop()
        s.httpd.server_close()
        sw = HttpSwitch(
            on_url="http://127.0.0.1:{}/on".format(port),
            off_url="http://127.0.0.1:{}/off".format(port),
            timeout=0.5,
        )
        self.assertFalse(sw.set(True))


class TestNullSwitch(unittest.TestCase):
    def test_records_the_requested_state(self):
        sw = NullSwitch()
        sw.set(True)
        sw.set(False)
        self.assertEqual(sw.calls, [True, False])

    def test_always_succeeds(self):
        self.assertTrue(NullSwitch().set(True))


if __name__ == "__main__":
    unittest.main()
