# Course Map

Maps Crafting Table Pandora's Box course lessons to local fucina sketches.

**Course:** [Adventure Kit: Pandora's Box](https://craftingtable.com/products/adventure-kit-2)
**GitHub:** [inventrdotio/AdventureKit2](https://github.com/inventrdotio/AdventureKit2)

---

## Individual Part Tutorials

| GitHub # | Component | Local Sketch | Status |
|----------|-----------|-------------|--------|
| 000 | Blink (built-in LED) | `sketches/001-blink/` | Done (original) |
| 002 | External LED | `sketches/001-blink/` | Covered |
| 004 | RGB LED | `ct-rgb-led/` | Done |
| 006 | Photoresistor (LDR) | `ct-photoresistor/` | Done |
| 010 | Active Buzzer | `ct-active-buzzer/` | Done |
| 020 | Passive Buzzer (KY-006) | `ct-passive-buzzer/` | Done |
| 030 | Potentiometer | `ct-potentiometer/` | Done |
| 035 | Rotary Encoder (KY-040) | `ct-rotary-encoder/` | Done |
| 040 | Push Button | `ct-push-button/` | Done |
| 050 | Water Level Sensor (HW-038) | `ct-rain-sensor/` | Done |
| 060 | IR Receiver (KY-022) | `ct-ir-receiver/` | Done |
| 070 | Ultrasonic Sensor (HC-SR04) | `ct-ultrasonic/` | Done |
| 080 | 1-Digit 7-Segment (5161AS) | `ct-7seg-1digit/` | Done |
| 085 | 4-Digit 7-Segment (5641AS) | `ct-7seg-4digit/` | Done |
| 090 | PIR Motion Sensor (HC-SR501) | `ct-pir-motion/` | Done |
| 100 | 4x4 Membrane Keypad | `ct-keypad/` | Done |
| 110 | Joystick (KY-023) | `ct-joystick/` | Done |
| 120 | DHT11 Temp/Humidity (KY-015) | `ct-dht-sensor/` | Done |
| 130 | Sound Sensor (KY-038) | `ct-sound-sensor/` | Done |
| 140 | Real-Time Clock (DS3231) | `ct-rtc/` | Done |
| 150 | RFID Reader (MFRC-522) | `ct-rfid/` | Done |
| 160 | Accelerometer/Gyroscope (MPU-6050) | `ct-gyroscope/` | Done |
| 170 | Servo Motor (SG90) | `ct-servo/` | Done |
| 200 | LCD1602 (16x2 Character) | `ct-lcd1602/` | Done |
| 210 | Stepper Motor (28BYJ-48) | `ct-stepper/` | Done |
| 220 | L293D Motor Driver IC | — | Skipped (concept only) |
| 240 | Touchscreen Shield (ILI9341) | `ct-radar-sweep/` | Used in radar |

---

## Chapter Projects (AI Apocalypse Storyline)

### Chapter 01 — Moving In

| Lesson | Topic | Local Sketch | Notes |
|--------|-------|-------------|-------|
| 01 | Blink | `sketches/001-blink/` | Original sketch |
| 02 | External LED | `sketches/001-blink/` | Same concept |
| 03 | Push Button (4 versions) | `ct-push-button/` | Uses INPUT_PULLUP version |
| 04 | Photoresistor + Analog | `ct-photoresistor/` | Basic version |
| 05 | Buzzer + millis() | `ct-active-buzzer/`, `ct-passive-buzzer/` | Split into two sketches |
| 06 | Potentiometer + PWM | `ct-potentiometer/` | Basic version |

### Chapter 02 — Base Security

| Lesson | Topic | Local Sketch | Notes |
|--------|-------|-------------|-------|
| 01 | PIR Motion + LED | `ct-security-motion/` | Done — multi-component |
| 02 | Keypad Door Lock | `ct-keypad-lock/` | Done — secret code entry |
| 03 | RFID Door Lock | `ct-rfid-lock/` | Done — RFID + LCD |
| 04 | RTTTL Alarm | `ct-rtttl-alarm/` | Done — melody player |

### Chapter 03 — Green House

| Lesson | Topic | Local Sketch | Notes |
|--------|-------|-------------|-------|
| 01 | Dry Plant Alert | `ct-plant-monitor/` | Done — water sensor + LED |
| 02 | Weather Station | `ct-dht-sensor/` | Covered by part tutorial |
| 03 | Fan Ventilation | — | Skipped — course warns direct motor drive can burn GPIO |
| 04 | Relay Fan | — | Skipped — concept only, no complete code |

### Chapter 04 — Daily Life

| Lesson | Topic | Local Sketch | Notes |
|--------|-------|-------------|-------|
| 01 | Alarm Clock | `ct-alarm-clock/` | Done — RTC + 7-seg + buzzer |
| 02 | Auto Summer Fan | — | Skipped — similar to Ch.03 fan |
| 03 | IR Smart Lights | `ct-ir-receiver/` | Covered by part tutorial |
| 04 | Clap Lights | `ct-clap-lights/` | Done — sound sensor toggle |
| 05 | Party Time | — | Placeholder in course |
| 06 | Paint Clone | — | Placeholder in course |

### Chapter 05 — Spy vs Spy (ESP32)

| Lesson | Topic | Local Sketch | Notes |
|--------|-------|-------------|-------|
| 10 | WiFi Light AP | `ct-wifi-lights/` | Done — ESP32 access point |
| 20 | WiFi Async AP | — | Same concept, async version |
| 30 | WiFi Station | — | Connects to existing network |

### Chapter 06 — Base Security++ (Radar)

| Lesson | Topic | Local Sketch | Notes |
|--------|-------|-------------|-------|
| 20 | 180° Sonar | `ct-radar-sweep/` | Done — servo + ultrasonic + TFT |
| 30 | RGB Turret Gun | — | Advanced — touchscreen + encoder + fan |
| 40 | T-Display Turret | — | ESP32 version |

### Chapter 07–08

Placeholder/concept chapters — no sketches created.

---

## Coverage Summary

| Category | Total in Course | Sketches Created | Coverage |
|----------|----------------|-----------------|----------|
| Part Tutorials | 25 components | 23 sketches | 92% |
| Chapter Projects | ~20 lessons | 9 integration sketches | 45% |
| ESP32 Projects | 3 lessons | 1 sketch | 33% |
| **Total** | | **32 sketches** | |

Skipped items are either placeholders in the course, duplicate concepts, or would require hardware not suitable for GPIO-direct drive.
