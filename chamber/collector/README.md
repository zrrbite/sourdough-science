# Collector — buffer, serve, record

Takes readings from any [source](../sources/) and publishes them for the viewers.

    ./listen.py --simulate --serve            # live UI at http://127.0.0.1:8787
    ./listen.py --serve                       # the same, from our BLE probe
    ./listen.py --source serial --port /dev/tty.usbmodem1101 --serve
    ./listen.py --scan-raw                    # dump advertisements, write a decoder

    ./listen.py --simulate --speed 120 --limit 270    # fast, no server
    ./listen.py --simulate --record ~/chamber-runs    # also write CSV + manifest

**`--serve` is the whole live system.** One process holds the buffer, serves the viewer at `/`
and its telemetry at `/telemetry.json`, and the page polls its own origin. Nothing relays,
nothing authenticates, nothing is manual. It works with real hardware the moment there is any.

## Telemetry shape

Two fixed documents, overwritten rather than accumulated:

    telemetry/current   latest reading, for the readout tiles
    telemetry/series    rolling window of recent samples, for the chart

The artifact store holds at most 5,000 documents and warns against one document per item for a
growing stream — a run at 10 s intervals would exhaust that inside fourteen hours. Series rows
are compact arrays (`[t_s, air_c, core_c, heating]`) rather than objects, because field names
repeated on every row would eat the 256 KiB document ceiling.

With `--record`, samples also land in the same CSV + manifest format stage 0 writes, so a run
recorded through any source is comparable with any other.

## Two places the viewer can run, and why only one is automatic

**Locally (`--serve`) — fully automatic.** The page and its telemetry share an origin, so the
page just polls. No credentials, no relay, no agent. This is the one to use.

**The published artifact — needs something authenticated in the loop.** A page served from
claude.ai is blocked by CSP from fetching any host, localhost included, and the artifact store
has **no endpoint an unauthenticated process can write to** — the only documented writers are
the page itself and Claude Code's `write_db`. No code here changes that.

What closes that loop is a scheduled Claude Code session:

    ./listen.py --simulate --out-dir ~/chamber-live --serve

then `/loop 60s` uploading `telemetry-current.json` and `telemetry-series.json` to the
artifact's `telemetry/current` and `telemetry/series` documents. `--out-dir` writes exactly
the split files upload expects, so the loop is an upload rather than an editing job.
Automatic in that you do nothing, but a session must be running and each tick costs tokens.

The same viewer file does all three: inside the artifact it subscribes to the store, served
locally it polls, opened as a bare file it shows the sample run. It picks by whether
`window.claude` exists.

## Tests

    python3 -m unittest discover -s tests -t .

15 tests. The local server is tested by making real HTTP requests to it rather than by mocking.
