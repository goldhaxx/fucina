# Plan: Integrate Crafting Table Course Content

## Context

The Pandora's Box course has 85 lessons across 12 modules:
- **Getting Started** (2 lessons) — setup, community
- **Chapter 01: Moving In** (6 lessons) — blink, LEDs, buttons, photoresistor, buzzers, PWM
- **Chapter 02: Base Security** (4 lessons) — PIR motion, keypad lock, RFID, RTTTL alarm
- **Chapter 03: GreenHouse** (3 lessons) — rain sensor, fan/motor, relay
- **Chapter 04: Daily Life** (3 lessons) — RTC alarm clock, clap lights (sound sensor), T-Display intro
- **Chapter 05: Phoenix Restoration** (2 lessons) — ESP32 WiFi networking, 180° radar sweep
- **Chapter 06: Base Security++** (2 lessons) — RGB turret with LCD touchscreen, T-Display variant
- **Chapter 07: Showdown** (3 lessons) — finale, what's next, board reference
- **Individual Part Tutorials** (27 lessons) — standalone component guides
- **Spies vs Spies** (15 lessons) — alternative projects using same components
- **Reincarnated** (15 lessons) — fantasy-themed alternative projects

Source material:
- `course-archive/raw-html/` — 85 crawled lesson pages (mix of text content and embedded images)
- `course-archive/github-repo/` — cloned inventrdotio/AdventureKit2 repo with ALL source code (.ino files) and READMEs
- `course-archive/lesson-metadata.json` — API data for all lessons
- `course-archive/lesson-index.txt` — lesson number → title mapping

## Phase 1: Extract & Organize (current)

Extraction agents are producing:
- [ ] `course-archive/extracted/parts-tutorials.md` — component tutorials from GitHub repo
- [ ] `course-archive/extracted/chapters.md` — chapter project code from GitHub repo
- [ ] `course-archive/extracted/device-docs.md` — component datasheets from GitHub repo
- [ ] `course-archive/extracted/esp32-tutorials.md` — ESP32/T-Display specific content
- [ ] `course-archive/extracted/lesson-text.md` — narrative/concept text from crawled HTML
- [ ] `course-archive/extracted/spies-vs-spies.md` — spy alternative storyline
- [ ] `course-archive/extracted/reincarnated.md` — isekai alternative storyline

## Phase 2: Enhance Existing Docs

### 2a. Enhance `docs/inventory.md`
- Add components discovered in course but missing from inventory:
  - Temperature & Humidity sensor (DHT11/DHT22 — referenced in lessons 43, 69, 120)
  - Joystick module (lesson 44, 110)
  - RGB LED (lesson 45, 67)
  - Photoresistor/LDR (lesson 30, 68)
  - L293D Motor Driver IC (lesson 220 in GitHub)
- Update status markers for components used in course projects
- Add library dependencies per component (from GitHub README files)

### 2b. Enhance `docs/wiring-patterns.md`
- Add patterns discovered in course:
  - Photoresistor voltage divider circuit
  - DHT sensor single-wire connection
  - 7-segment display multiplexing
  - Keypad matrix scanning wiring
  - RTTTL buzzer melody pattern
  - Stepper motor ULN2003 driver wiring
  - LCD touchscreen shield pin mapping
  - Relay module with flyback diode (expanded)
  - Joystick analog + button wiring

### 2c. Enhance `docs/pinouts.md`
- Add LCD touchscreen shield pin consumption map
- Add L293D motor driver IC pinout
- Add common multi-component pin allocation plans (avoid conflicts)

### 2d. Enhance `tools/breadboard.py`
- Add new component renderers based on course projects:
  - Push button renderer
  - Potentiometer renderer
  - 7-segment display renderer
  - Buzzer renderer
  - Sensor module renderer (generic 3-pin: VCC/OUT/GND)
- These will allow generating wiring diagrams for course-derived sketches

## Phase 3: Create Course-Derived Sketches

Store in `sketches/` with a `ct-` prefix to indicate Crafting Table origin:

### From Individual Part Tutorials (highest priority — standalone component learning)
- `sketches/craftingtable/ct-potentiometer/` — analog read + serial output (lesson 18 / GitHub 030)
- `sketches/craftingtable/ct-push-button/` — pull-down, pull-up, toggle (lesson 33 / GitHub 040)
- `sketches/craftingtable/ct-photoresistor/` — light level detection (lesson 30 / GitHub 006)
- `sketches/craftingtable/ct-active-buzzer/` — simple alarm tone (lesson 46 / GitHub 010)
- `sketches/craftingtable/ct-passive-buzzer/` — melody playback (lesson 46 / GitHub 020)
- `sketches/craftingtable/ct-rotary-encoder/` — rotation + click input (lesson 38 / GitHub 035)
- `sketches/craftingtable/ct-ir-receiver/` — decode remote codes (lesson 35 / GitHub 060)
- `sketches/craftingtable/ct-ultrasonic/` — distance measurement (lesson 23 / GitHub 070)
- `sketches/craftingtable/ct-7seg-1digit/` — single digit display (lesson 20 / GitHub 080)
- `sketches/craftingtable/ct-7seg-4digit/` — 4-digit counter (lesson 39 / GitHub 085)
- `sketches/craftingtable/ct-pir-motion/` — motion detection (lesson 28 / GitHub 090)
- `sketches/craftingtable/ct-keypad/` — 4x4 matrix scanning (lesson 50 / GitHub 100)
- `sketches/craftingtable/ct-joystick/` — analog X/Y + button (lesson 44 / GitHub 110)
- `sketches/craftingtable/ct-dht-sensor/` — temperature & humidity (lesson 43 / GitHub 120)
- `sketches/craftingtable/ct-sound-sensor/` — clap detection (lesson 41 / GitHub 130)
- `sketches/craftingtable/ct-rtc/` — real-time clock read/set (lesson 22 / GitHub 140)
- `sketches/craftingtable/ct-rfid/` — card UID reader (lesson 37 / GitHub 150)
- `sketches/craftingtable/ct-gyroscope/` — accelerometer/gyro data (lesson 40 / GitHub 160)
- `sketches/craftingtable/ct-servo/` — sweep 0-180° (lesson 25 / GitHub 170)
- `sketches/craftingtable/ct-lcd1602/` — character display output (lesson 49 / GitHub 200)
- `sketches/craftingtable/ct-stepper/` — stepper motor control (lesson 48 / GitHub 210)
- `sketches/craftingtable/ct-rgb-led/` — color cycling (lesson 45)
- `sketches/craftingtable/ct-rain-sensor/` — water level detection (lesson 32 / GitHub 050)
- `sketches/craftingtable/ct-touchscreen/` — LCD shield basics (lesson 27 / GitHub 240)

### From Chapter Projects (integrated multi-component builds)
- `sketches/craftingtable/ct-security-motion/` — PIR + LED + buzzer alarm (Ch.02 lesson 1)
- `sketches/craftingtable/ct-keypad-lock/` — keypad + servo door lock (Ch.02 lesson 2)
- `sketches/craftingtable/ct-rfid-lock/` — RFID + servo access control (Ch.02 lesson 3)
- `sketches/craftingtable/ct-rtttl-alarm/` — melody alarm system (Ch.02 lesson 4)
- `sketches/craftingtable/ct-plant-monitor/` — rain sensor + buzzer alert (Ch.03 lesson 5)
- `sketches/craftingtable/ct-fan-control/` — DC motor + temp sensor (Ch.03 lesson 6)
- `sketches/craftingtable/ct-relay-fan/` — relay-driven fan (Ch.03 lesson 7)
- `sketches/craftingtable/ct-alarm-clock/` — RTC + LCD + buzzer (Ch.04 lesson 8)
- `sketches/craftingtable/ct-clap-lights/` — sound sensor + LED (Ch.04 lesson 9)
- `sketches/craftingtable/ct-radar-sweep/` — servo + ultrasonic scanner (Ch.06 lesson 12)
- `sketches/craftingtable/ct-wifi-lights/` — ESP32 WiFi LED control (Ch.05)

### From Alternative Storylines (unique project ideas)
- `sketches/craftingtable/ct-morse-transmitter/` — LED morse code (Spies #1)
- `sketches/craftingtable/ct-ir-alarm/` — IR remote stealth alarm (Spies #2)
- `sketches/craftingtable/ct-encrypted-lcd/` — encrypted message display (Spies #3)
- `sketches/craftingtable/ct-weather-station/` — multi-sensor weather (Spies #10)

## Phase 4: Cleanup & Documentation

- [ ] Add `course-archive/` to `.claudeignore` (large, reference-only)
- [ ] Update `docs/journal.md` with course integration notes
- [ ] Create `docs/course-map.md` — maps course lessons to local sketches
- [ ] Update CLAUDE.md if new conventions emerge

## Execution Order

1. **Now:** Wait for extraction agents to finish
2. **Next session:** Enhance existing docs (Phase 2) using extracted content
3. **Following sessions:** Create sketches in batches (Phase 3), starting with part tutorials
4. **Each sketch:** wiring.yaml → wiring.svg → platformio.ini → src/main.cpp → README.md

## Decisions (Resolved)

1. **Sketch location:** `sketches/craftingtable/ct-{name}/` — dedicated subdirectory with `ct-` prefix
2. **Scope:** All component tutorials and chapter projects — full coverage
3. **Code style:** Rewrite all `.ino` code to PlatformIO conventions:
   - `src/main.cpp` with `#include <Arduino.h>`
   - `constexpr` for pin definitions (no `#define` or bare `int`)
   - Forward declarations where needed
   - Our standard sketch structure (wiring.yaml, wiring.svg, platformio.ini, README.md)
4. **ESP32 content:** Include now
