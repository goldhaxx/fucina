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

## 2026-03-21 — Course Archive Integration

**Topic:** Crafting Table Pandora's Box course content extraction
**Result:** Complete

Crawled the entire Crafting Table course (85 lessons, 12 modules) and cloned the inventrdotio/AdventureKit2 GitHub repo. Key findings:
- Course has 3 storylines (Apocalypse, Spies vs Spies, Reincarnated) that teach the same components with different narratives
- GitHub repo at `inventrdotio/AdventureKit2` has all 88 `.ino` source files — the authoritative code source
- Course HTML content is mostly JavaScript-rendered; crawlable HTML has wiring/concept text but code was in images or JS
- Individual Part Tutorials section covers 27 components with standalone test sketches

What was produced:
- `course-archive/` — raw HTML (85 lessons), GitHub repo clone, extracted markdown (7 files, ~330KB)
- Enhanced `docs/inventory.md` — 5 new components, 13 updated entries, library reference table
- Enhanced `docs/wiring-patterns.md` — 13 new circuit patterns (photoresistor, DHT, 7-seg, keypad, encoder, etc.)
- Enhanced `docs/pinouts.md` — touchscreen shield pin map, multi-component allocation plans, ESP32 safe pin guide
- `docs/plan.md` — plan for creating `sketches/craftingtable/ct-*` directories from course projects

Next: Create PlatformIO sketches from course content (Phase 3 of plan)
