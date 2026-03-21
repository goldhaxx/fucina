# Build Journal

Chronological log of what was built, what worked, and open questions.

---

<!-- Format:
## YYYY-MM-DD — Sketch name or topic

**Component(s):** what you used
**Board:** HERO XL / TTGO ESP32
**Result:** worked / partially / failed

Notes, observations, gotchas, ideas for next time.
-->

## 2026-03-20 — 001-blink

**Component(s):** LED (red), 220Ω resistor
**Board:** HERO XL (Mega 2560)
**Result:** worked

First sketch. LED blinks on pin 9 at 1 Hz. Setup milestones along the way:
- Fixed PlatformIO TLS errors caused by Cloudflare WARP — appended gateway CA to certifi bundle
- Built `tools/breadboard.py` — custom SVG diagram generator for the 830-point breadboard
- Added `~/.platformio/penv/bin` to PATH so `pio` works from terminal
- Established sketch scaffold: wiring.yaml → wiring.svg → code → upload
