"""Driving the heater through a smart plug's local HTTP API.

A plug with a local endpoint keeps mains wiring out of the project entirely:
the Pi's whole involvement with 230 V is one HTTP request. URLs are supplied by
config rather than hard-coded, so Shelly, Tasmota and anything else with a local
API work without a code change:

    Shelly Gen1   http://IP/relay/0?turn=on            ...?turn=off
    Shelly Gen2   http://IP/rpc/Switch.Set?id=0&on=true   ...&on=false
    Tasmota       http://IP/cm?cmnd=Power%20On          ...Power%20Off
"""

import urllib.request


class HttpSwitch:
    def __init__(self, on_url, off_url, timeout=5.0):
        self.on_url = on_url
        self.off_url = off_url
        self.timeout = timeout

    def set(self, on):
        """Request the state. Returns whether the plug confirmed it.

        A failure is reported rather than raised: a blip on the network must not
        take down a control loop that has a heater running.
        """
        url = self.on_url if on else self.off_url
        try:
            with urllib.request.urlopen(url, timeout=self.timeout) as response:
                return 200 <= response.status < 300
        except Exception:
            return False


class NullSwitch:
    """Stands in for the plug during a dry run, so a chamber-less test is possible."""

    def __init__(self):
        self.calls = []

    def set(self, on):
        self.calls.append(on)
        return True
