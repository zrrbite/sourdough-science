"""A local HTTP server so the viewer updates itself, with nothing in the loop.

This is the relay that needs no agent and no credentials: `listen.py --serve`
holds the live buffer, serves the viewer at `/` and its telemetry at
`/telemetry.json`, and the page polls its own origin. Same machine, same
process, no bridge.

It exists because the published artifact cannot be fed this way. A page served
from claude.ai is blocked by CSP from fetching any host at all, localhost
included, and the artifact store has no endpoint an unauthenticated process can
write to. Locally, both problems vanish: the page and the data share an origin.
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def start_server(port, buffer, viewer_html, host="127.0.0.1"):
    """Start the server on a daemon thread and return it. Call shutdown() to stop."""

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = self.path.split("?", 1)[0]
            if path == "/telemetry.json":
                self._send(200, "application/json",
                           json.dumps(buffer.documents()).encode())
            elif path in ("/", "/index.html"):
                self._send(200, "text/html; charset=utf-8", viewer_html.encode())
            else:
                self._send(404, "text/plain; charset=utf-8", b"not found\n")

        def _send(self, status, content_type, body):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass  # the sampling loop owns stdout

    server = ThreadingHTTPServer((host, port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server
