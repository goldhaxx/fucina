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

## 2026-03-21 — Part Tutorial Sketches (Phase 3a)

**Topic:** Create all Individual Part Tutorial sketches from course content
**Result:** Complete — 23 sketches, all compile clean

Converted all course Part Tutorials into PlatformIO sketches at `sketches/craftingtable/ct-*/`. Each has wiring.yaml, wiring.svg, platformio.ini, src/main.cpp, and README.md.

Sketches created (23 total):
- **No-library basics:** potentiometer, push-button, active-buzzer, passive-buzzer, photoresistor, rgb-led
- **Sensor modules:** ultrasonic, pir-motion, joystick, sound-sensor, gyroscope, rain-sensor, dht-sensor
- **Actuator/output:** servo, stepper, lcd1602, 7seg-1digit, 7seg-4digit
- **Communication/input:** ir-receiver, rotary-encoder, keypad, rtc, rfid

Gotchas:
- PlatformIO registry names differ from Arduino IDE: `arduino-libraries/Servo`, `deanisme/SevSeg`, `z3t0/IRremote`, `micromouseonline/BasicEncoder`, etc. Must use `pio pkg search` to find correct names.
- Built-in Arduino libraries (Servo, Stepper, LiquidCrystal) are NOT automatically available in PlatformIO — need explicit `lib_deps` entries
- RFID module (MFRC522) MUST use 3.3V — 5V damages it

Next: Chapter projects (multi-component integration builds)

## 2026-03-21 — Chapter Project Sketches (Phase 3b)

**Topic:** Create multi-component Chapter Project sketches from course content
**Result:** Complete — 7 sketches, all compile clean

Created integration projects that combine multiple components:
- **ct-security-motion** — PIR + LED flood lights (Ch.02 L01)
- **ct-keypad-lock** — 4x4 keypad secret code entry (Ch.02 L02)
- **ct-rfid-lock** — RFID reader + LCD1602 access control (Ch.02 L03)
- **ct-rtttl-alarm** — RTTTL melody player through passive buzzer (Ch.02 L04)
- **ct-plant-monitor** — water sensor + PWM LED brightness mapping (Ch.03 L01)
- **ct-alarm-clock** — DS3231 RTC + 4-digit 7-seg + buzzer alarm (Ch.04 L01)
- **ct-clap-lights** — sound sensor toggle for onboard LED (Ch.04 L04)

The alarm clock is the most complex — combines 3 components on different interfaces (I2C for RTC, 12 GPIO pins for 7-seg, 1 pin for buzzer).

Skipped from plan: ct-fan-control (course warns it can burn the board), ct-relay-fan (concept only), ct-radar-sweep (requires touchscreen shield — save for later), ct-wifi-lights (ESP32 — different board).

**Total sketch count: 30** (3 original + 23 part tutorials + 7 chapter projects, with some plan items deferred)

## 2026-03-21 — Deferred Sketches, Phase 4, Scaffold & Renderers (Session 3)

**Topic:** Complete all deferred work, enhance scaffold, add breadboard component renderers
**Result:** Mostly complete — 7-segment digit overflow still unresolved

What was done:
- 2 deferred sketches (ct-radar-sweep, ct-wifi-lights) — total now 32
- `docs/course-map.md` — lesson-to-sketch mapping
- `/new-component` command + `components.md` rule + `docs/renderers.md`
- 8 new breadboard.py renderers (button, buzzer, sensor, potentiometer, rgb_led, seven_segment, module)
- All 32 wiring.yaml files updated with component declarations, all SVGs regenerated
- Pin pills anchored to correct side of diagram, sized to avoid overlap
- 7-segment DIP wiring corrected (both banks), body widened to e→i, digits rotated + italicized + decimal points

Unresolved:
- 7-segment digit glyphs overflow the DIP body — constraint math doesn't account for SVG transform composition correctly. Need to use clipPath or nested SVG viewBox for structural containment instead of trying to solve it algebraically.

Key learnings documented in checkpoint:
1. Need visual test fixtures for renderers (not just crash tests)
2. SVG containment should be structural (clipPath), not mathematical
3. Physical component dimensions should come from datasheets, not guesswork
4. wiring.yaml must reflect physical breadboard positions (both banks for DIPs)
5. PlatformIO library names need a reference mapping document

## 2026-03-22 — 004-joystick-lights

**Component(s):** HW-504 joystick, 5× LEDs (red, green, blue, white, yellow), 5× 220Ω resistors
**Board:** HERO XL (Mega 2560)
**Result:** worked

First multi-component original sketch. Joystick position selects LED animation effects in real time:
- Center: sync pulse (all LEDs breathe together)
- Left/Right: sequential chase in that direction, speed scales with deflection
- Up: random twinkle, cubic intensity curve — goes chaotic at full throw
- Down: ripple wave expanding outward from center LED

Gotchas and fixes:
- **Joystick calibration is mandatory.** Hardcoded center of 512 was completely wrong — the HW-504 read X=0, Y=0 at rest because the 5V bus wire was missing. After adding 5V, it calibrated to X=509, Y=518. Auto-calibration at startup (32 samples averaged) is the right approach for any analog joystick.
- **X-axis was inverted.** Physical right = high analog on this unit. Swapped in code. Would vary by manufacturer — could add a serial command to flip axes.
- **Zone flicker at axis boundaries.** Without hysteresis, the joystick flickered between UP and LEFT when near a diagonal. Fixed with 20-unit hysteresis (need more deflection to enter a zone than to stay in it).
- **Forgot the 5V bus wire.** Sketch 003 only used GND bus. Adding the joystick required a new wire from HERO XL 5V to the + rail. Without it, potentiometers have no reference voltage and read 0.
- **Cubic intensity curve feels right.** Linear deflection-to-speed mapping felt flat. `deflection³` makes small movements gentle and full throw severe — much more satisfying on twinkle and ripple.

Also overhauled the module renderer in breadboard.py:
- New `to:` pin format for direct module-to-destination wiring (no intermediate breadboard holes)
- Module cards now render fully separated from the breadboard
- Onboarded HW-504 through `/new-component` workflow (specs, inventory, wiring patterns)

**Sketch count: 33** (4 original + 29 craftingtable)
