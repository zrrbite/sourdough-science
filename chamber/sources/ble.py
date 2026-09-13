"""Bluetooth advertisements, decoded by whichever decoder you hand it.

Broadcast-only: the probe advertises and anybody listens. No pairing, no
connection, any number of listeners - and no cable through the chamber seal.

The decoder is a parameter, which is the whole point of this module. Our probe
and an Inkbird are the same transport with different bytes inside.
"""

import time

from base import Source, reading
from decoders import decode_chamber
from protocol import COMPANY_ID


class BleSource(Source):
    name = "ble"

    def __init__(self, decoder=None, company_id=COMPANY_ID, interval_s=10.0,
                 limit=None):
        self.decoder = decoder or decode_chamber
        self.company_id = company_id
        self.interval_s = interval_s
        self.limit = limit

    def readings(self):
        import asyncio

        scanner_cls = _scanner()
        queue = []
        started = time.monotonic()

        def on_advert(_device, adv):
            payload = adv.manufacturer_data.get(self.company_id)
            decoded = self.decoder(payload) if payload else None
            if decoded is not None:
                queue.append((decoded, adv.rssi))

        async def pump(out):
            scanner = scanner_cls(detection_callback=on_advert)
            await scanner.start()
            try:
                emitted = 0
                while self.limit is None or emitted < self.limit:
                    await asyncio.sleep(self.interval_s)
                    while queue:
                        decoded, rssi = queue.pop(0)
                        out.append(reading(
                            t_s=time.monotonic() - started,
                            air_c=decoded.get("air_c"),
                            core_c=decoded.get("core_c"),
                            heating=decoded.get("heating"),
                            seq=decoded.get("seq"),
                            battery_pct=decoded.get("battery_pct"),
                            rssi=rssi,
                        ))
                        emitted += 1
            finally:
                await scanner.stop()

        collected = []
        asyncio.run(pump(collected))
        return iter(collected)


def scan_raw(seconds=20.0, printer=print):
    """Dump every advertisement seen, so a new decoder can be written from evidence.

    This is how the Inkbird decoder gets written: point it at the device, read
    the bytes it actually emits, then implement `decode_inkbird` against them.
    Guessing a third party's layout produces confident wrong numbers.
    """
    import asyncio

    scanner_cls = _scanner()
    seen = {}

    def on_advert(device, adv):
        for company_id, payload in (adv.manufacturer_data or {}).items():
            key = (device.address, company_id)
            if seen.get(key) == payload:
                continue
            seen[key] = payload
            printer("{}  company=0x{:04X}  len={:<3d} rssi={:<5} {}  {}".format(
                device.address, company_id, len(payload), adv.rssi,
                payload.hex(" "), device.name or ""))

    async def pump():
        scanner = scanner_cls(detection_callback=on_advert)
        await scanner.start()
        try:
            await asyncio.sleep(seconds)
        finally:
            await scanner.stop()

    printer("scanning {:.0f}s - every distinct advertisement, once".format(seconds))
    asyncio.run(pump())
    printer("{} distinct (address, company) payloads".format(len(seen)))


def _scanner():
    try:
        from bleak import BleakScanner
    except ImportError:
        raise SystemExit("Bluetooth needs bleak: pip install bleak "
                         "(or use --source simulated)")
    return BleakScanner
