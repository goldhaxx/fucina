# Spies Vs Spies -- Module 11 Extraction

> **Source:** Crafting Table / inventr.io -- Adventure Kit: Pandora's Box
> **Module:** 11 -- Spies Vs Spies (Alternative Storyline)
> **Lessons:** 51--65
> **Board:** HERO XL (Mega 2560) unless otherwise noted
> **Note:** Code blocks were not fully captured by the scraper (JavaScript-rendered content). Only partial code snippets are included where available.

---

## Lesson 51 -- Basic LED Morse Code Transmitter

**Project:** Transmit text messages as Morse code light patterns via LED.

### Components
- 1x LED (any color)
- HERO XL

### Pin Connections
| Component | Pin |
|-----------|-----|
| LED anode (+) | Pin 13 |
| LED cathode (-) | GND |

### Wiring Notes
- Pin 13 has a built-in current-limiting resistor, so no external resistor is needed.
- Ground connection completes the circuit.

### Key Concepts
- Morse code timing: dot = 1 unit, dash = 3 units
- Intra-character gap = 1 unit, inter-character gap = 3 units, word gap = 7 units
- String manipulation to convert text characters to dot/dash sequences
- Loops to process character arrays for automated transmission
- Timing-critical applications with `delay()` or `millis()`

### Libraries
- None (built-in Arduino functions only)

### Code
Not captured by scraper.

---

## Lesson 52 -- IR Remote Control-based Stealth Alarm

**Project:** Decode IR remote button presses and use them to arm/trigger an alarm system.

### Components
- 1x IR receiver module (38 kHz, 3-pin: OUT, GND, VCC)
- 1x IR remote control (NEC protocol)
- HERO XL

### Pin Connections
| Component | Pin |
|-----------|-----|
| IR receiver VCC | 5V |
| IR receiver GND | GND |
| IR receiver OUT (data) | Digital pin (not specified -- likely pin 11 or similar) |

### Wiring Notes
- IR receiver needs clean, stable 5V power for internal amplification.
- The data output pin sends decoded digital signals to the HERO Board.
- IR communication is line-of-sight and does not pass through walls -- useful for stealth.

### Key Concepts
- Infrared communication: invisible light pulses encode button identities
- NEC protocol: each button sends a unique hex code pattern
- Receiver demodulates 38 kHz carrier signal into digital data
- IR is limited range, line-of-sight -- constraints become security features
- Must first scan and map each button's hex code before building logic

### Libraries
- `IRremote`

### Code
Not captured by scraper.

---

## Lesson 53 -- Encrypted Messages using LCD1602 Display

**Project:** Dual-message display that shows a cover message normally and reveals a hidden message when a button is pressed.

### Components
- 1x LCD1602 (16x2 character display, parallel mode)
- 1x Push button
- HERO XL

### Pin Connections
| Component | Pin |
|-----------|-----|
| LCD VSS | GND |
| LCD VDD | 5V |
| LCD V0 (contrast) | GND (max contrast) |
| LCD RS (register select) | Pin 12 |
| LCD Enable | Pin 11 |
| LCD D4 | Pin 2 |
| LCD D5 | Pin 3 |
| LCD D6 | Pin 4 |
| LCD D7 | Pin 5 |
| Button (one leg) | Pin 7 |
| Button (other leg) | 5V |

### Wiring Notes
- LCD runs in 4-bit mode (D4--D7 only), saving pins.
- V0 grounded gives maximum contrast. For adjustable contrast, use a 10K potentiometer between 5V and GND with wiper to V0.
- Button wired to 5V for active-HIGH reads. Consider using `INPUT_PULLUP` and wiring to GND for active-LOW instead (avoids floating pin if no pull-down resistor is used).

### Key Concepts
- HD44780 controller protocol (standard for 16x2 LCDs)
- 4-bit vs 8-bit communication modes
- Register Select (RS): command mode vs data mode
- Enable pin: data strobe signal
- Button state reading with `digitalRead()`
- Conditional display logic: different content based on button state

### Libraries
- `LiquidCrystal`

### Code
Not captured by scraper.

---

## Lesson 54 -- Motion Detection System using HC-SR501 PIR

**Project:** Detect human motion via passive infrared and report state changes over serial.

### Components
- 1x HC-SR501 PIR motion sensor
- HERO XL

### Pin Connections
| Component | Pin |
|-----------|-----|
| HC-SR501 VCC | 5V |
| HC-SR501 GND | GND |
| HC-SR501 OUT | Pin 2 |

### Wiring Notes
- Sensor outputs HIGH (5V) when motion detected, LOW (0V) when clear.
- ~1 minute warm-up period after power-on before readings are reliable.
- Two onboard potentiometers: sensitivity (range) and delay (hold time after trigger).
- 7-meter range, 110-degree field of view.

### Key Concepts
- Passive infrared detection: senses changes in infrared radiation, not steady heat
- State tracking: report only transitions (motion started / motion stopped), not continuous HIGH
- Debouncing / filtering false triggers
- `digitalRead()` for binary sensor input
- Adjustable sensitivity and hold-time via onboard pots

### Libraries
- None (built-in Arduino functions only)

### Code
Not captured by scraper.

---

## Lesson 55 -- RFID Message Decoder using MFRC-522

**Project:** Read unique identification codes (UIDs) from RFID cards and tags via SPI.

### Components
- 1x MFRC-522 RC522 RFID reader module
- 1x RFID card (S50, MIFARE Classic 1K)
- 1x RFID keychain tag
- HERO XL

### Pin Connections
| Component | HERO XL Pin |
|-----------|-------------|
| MFRC-522 VCC | 3.3V |
| MFRC-522 GND | GND |
| MFRC-522 MOSI | Pin 11 |
| MFRC-522 MISO | Pin 12 |
| MFRC-522 SCK | Pin 13 |
| MFRC-522 SS (SDA) | Pin 10 |
| MFRC-522 RST | Not specified (typically pin 9) |

### Wiring Notes
- **CRITICAL: Power at 3.3V only.** 5V will damage the MFRC-522 module.
- SPI pins on Mega: MOSI=51, MISO=50, SCK=52, SS=53. However, the lesson uses pins 11/12/13/10 (Uno-style SPI). On Mega 2560, the hardware SPI pins are 50--53. The lesson's pin assignments may be using software SPI or may be incorrect for Mega. Verify with the `MFRC522` library documentation.
- 13.56 MHz operating frequency.
- Each card/tag has a unique 4--10 byte UID.

### Key Concepts
- RFID: Radio Frequency Identification at 13.56 MHz
- SPI communication protocol (MOSI, MISO, SCK, SS)
- Passive RFID cards: powered by the reader's electromagnetic field (no battery)
- UID extraction and hex formatting
- Foundation for access control systems

### Libraries
- `MFRC522` (by miguelbalboa)

### Code
Not captured by scraper.

---

## Lesson 56 -- Sound Surveillance System using KY-037

**Project:** Sound-activated defense turret with stepper motor aiming and RGB LED output.

### Components
- 1x KY-037 sound sensor module
- 1x 28BYJ-48 stepper motor + ULN2003 driver board
- 1x Joystick module
- 1x RGB LED (common cathode)
- HERO XL

### Pin Connections
| Component | Pin |
|-----------|-----|
| KY-037 VCC | 5V |
| KY-037 GND | GND |
| KY-037 AO (analog out) | A0 |
| KY-037 DO (digital out) | Pin 2 |
| ULN2003 IN1 | Pin 22 |
| ULN2003 IN2 | Pin 24 |
| ULN2003 IN3 | Pin 26 |
| ULN2003 IN4 | Pin 28 |
| Joystick X-axis | A8 |
| Joystick button | Pin 30 (internal pullup) |
| RGB LED Red | Pin 44 (PWM) |
| RGB LED Green | Pin 45 (PWM) |
| RGB LED Blue | Pin 46 (PWM) |

### Wiring Notes
- KY-037 provides both analog (volume level) and digital (threshold trigger) outputs.
- Stepper motor draws significant current -- ensure adequate power supply.
- Joystick provides manual aiming override; button acts as fire control.
- RGB LED on PWM pins for variable intensity color control.
- All 5V and GND connections share common rails.

### Key Concepts
- Analog vs digital sensor outputs
- Sound threshold calibration via onboard potentiometer
- Stepper motor sequencing for directional aiming
- Joystick analog input for manual control
- PWM-based RGB color mixing
- Multi-component integration

### Libraries
- `Stepper` (built-in) or `AccelStepper`

### Code
Not captured by scraper.

---

## Lesson 57 -- Wireless Signal Detector using ESP32 T-Display

**Board:** LilyGo TTGO T-Display ESP32

**Project:** WiFi network scanner that displays detected SSIDs and signal strengths on the built-in TFT screen.

### Components
- 1x LilyGo TTGO T-Display ESP32 (no external wiring needed)
- USB-C cable for power/programming

### Pin Connections
No external wiring. Uses built-in:
- ESP32 WiFi radio (2.4 GHz)
- ST7789 TFT display (135x240 px)
- Two programmable buttons
- Built-in antenna

### Key Concepts
- WiFi scanning in station (STA) mode without connecting to any network
- Beacon frames: networks broadcast SSID, security type, signal strength every ~100 ms
- RSSI (Received Signal Strength Indicator) for distance estimation
- TFT graphics: text rendering, color management, screen refresh
- Standalone portable device (no computer needed after upload)

### Libraries
- `WiFi` (ESP32 built-in)
- `TFT_eSPI`

### Code (partial -- scraper captured opening only)
```cpp
#include <WiFi.h>
#include <TFT_eSPI.h>
TFT_eSPI tft = TFT_eSPI();
```

---

## Lesson 58 -- Two-Way Communication Device

**Project:** Two-way communication system (details not captured).

### Components
Not captured by scraper (page contained only the title).

### Pin Connections
Not available.

### Key Concepts
- Likely involves HC-06 Bluetooth module or ESP32 WiFi for bidirectional serial communication.

### Libraries
Not available.

### Code
Not captured by scraper.

---

## Lesson 59 -- Spy Motion Tracker

**Project:** Motion tracking system (details not captured).

### Components
Not captured by scraper (page contained only the title).

### Pin Connections
Not available.

### Key Concepts
- Likely involves MPU-6050 accelerometer/gyroscope for orientation and motion tracking.

### Libraries
Not available.

### Code
Not captured by scraper.

---

## Lesson 60 -- Weather Station

**Project:** Environmental monitoring station tracking temperature, humidity, and rain detection with serial output.

### Components
- 1x DHT11 temperature/humidity sensor
- 1x Rain/water level detection sensor
- HERO XL

### Pin Connections
| Component | Pin |
|-----------|-----|
| DHT11 data | Pin 2 |
| DHT11 VCC | 5V |
| DHT11 GND | GND |
| Rain sensor analog out | A0 (likely) |
| Rain sensor VCC | 5V |
| Rain sensor GND | GND |

### Wiring Notes
- DHT11 uses a single-wire digital protocol with precise timing.
- Pin 2 chosen for reliable digital communication without interfering with serial or PWM.
- Rain sensor: separate sensor board and control board connected via included cable.
- Analog reading from rain sensor increases with more water contact.

### Key Concepts
- DHT11 single-wire protocol: temperature and humidity in one data pin
- Analog rain sensing: resistance changes with water contact area
- Combining digital and analog sensor inputs
- Data formatting for human-readable serial output
- Continuous monitoring loops

### Libraries
- `DHT` (Adafruit DHT library or similar)

### Code
Not captured by scraper.

---

## Lesson 61 -- Trap Disarming Simulator (w/Servos)

**Project:** Button-activated servo motor that rotates to a target angle and resets -- simulating a mechanical lock disarm sequence.

### Components
- 1x SG90 micro servo (180 degree)
- 1x Push button
- HERO XL

### Pin Connections
| Component | Pin |
|-----------|-----|
| Servo signal (orange) | Pin 9 (PWM) |
| Servo power (red) | 5V |
| Servo ground (brown/black) | GND |
| Button | Pin 2 |
| Button ground | GND |

### Wiring Notes
- Pin 2 has interrupt capability for immediate button detection.
- Pin 9 provides PWM signals that the servo interprets as position commands.
- For multiple servos, use external power (not the board's 5V rail).

### Key Concepts
- Servo motor control: precise angle positioning (0--180 degrees)
- PWM signal interpretation: pulse width maps to angle
- Internal feedback loop: potentiometer + control circuit maintain position
- Button-triggered mechanical sequences
- Automated reset cycles

### Libraries
- `Servo` (built-in)

### Code (partial -- scraper captured opening only)
```cpp
#include <Servo.h>
Servo myservo; // create servo object to control a servo
```

---

## Lesson 62 -- Hacking Device (w/Keypad)

**Project:** Keystroke capture system using a 4x4 membrane keypad -- foundation for password/access control systems.

### Components
- 1x 4x4 membrane keypad
- HERO XL

### Pin Connections
| Keypad Pin | Function | HERO XL Pin |
|------------|----------|-------------|
| Pin 1 | Row 1 (1, 2, 3, A) | Pin 9 |
| Pin 2 | Row 2 (4, 5, 6, B) | Pin 8 |
| Pin 3 | Row 3 (7, 8, 9, C) | Pin 7 |
| Pin 4 | Row 4 (*, 0, #, D) | Pin 6 |
| Pin 5 | Col 1 (1, 4, 7, *) | Pin 5 |
| Pin 6 | Col 2 (2, 5, 8, 0) | Pin 4 |
| Pin 7 | Col 3 (3, 6, 9, #) | Pin 3 |
| Pin 8 | Col 4 (A, B, C, D) | Pin 2 |

### Wiring Notes
- 8 pins total: 4 rows + 4 columns for 16-key matrix.
- Row pins are driven HIGH during scanning; column pins are read as inputs.
- Keypad ribbon cable pin 1 is typically on the left when the keypad faces you.

### Key Concepts
- Matrix scanning: 16 keys with only 8 pins
- Row-column intersection detection
- Keypad library handles scanning automatically
- Foundation for password entry, access control, menu navigation

### Libraries
- `Keypad` (by Mark Stanley and Alexander Brevig)

### Code
Not captured by scraper.

---

## Lesson 63 -- Emergency Escape Gadget

**Project:** Precision stepper motor control for mechanical lock rotation -- bidirectional movement with exact step counting.

### Components
- 1x 28BYJ-48 stepper motor
- 1x ULN2003 driver board
- HERO XL

### Pin Connections
| Component | Pin |
|-----------|-----|
| ULN2003 IN1 | Pin 8 |
| ULN2003 IN2 | Pin 9 |
| ULN2003 IN3 | Pin 10 |
| ULN2003 IN4 | Pin 11 |
| ULN2003 power | 5V + GND (from board or external) |

### Wiring Notes
- **Never connect stepper motor directly to HERO Board pins.** Always use the ULN2003 driver board to handle current requirements.
- Motor requires 4 control pins for the two internal coils.
- Driver board handles the heavy current that would damage microcontroller pins.

### Key Concepts
- Stepper motor: discrete steps vs continuous rotation
- 2048 steps per full revolution (half-step mode), ~0.18 degrees per step
- Bidirectional control: positive and negative step counts
- No position feedback needed -- step counting is inherently self-tracking
- Two-coil energizing sequence: IN1-IN2 (coil A), IN3-IN4 (coil B)

### Libraries
- `Stepper` (built-in)

### Code (partial -- scraper captured opening only)
```cpp
#include <Stepper.h>
const int stepsPerRevolution = 2048;

Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);
```

---

## Lesson 64 -- Color Changing Camouflage Device

**Project:** RGB LED color cycling with PWM intensity control -- automatic color transitions through timed sequences.

### Components
- 1x RGB LED (common cathode)
- 3x Resistors (current limiting -- values not specified, use 220 ohm)
- HERO XL

### Pin Connections
| Component | Pin |
|-----------|-----|
| RGB Red channel | Pin 11 (PWM) |
| RGB Green channel | Pin 10 (PWM) |
| RGB Blue channel | Pin 9 (PWM) |
| RGB common cathode | GND |

### Wiring Notes
- All three channels on PWM-capable pins for `analogWrite()` intensity control.
- Common cathode connects to GND; each color channel is driven independently.
- Use current-limiting resistors (220 ohm) on each channel to protect the LED.

### Key Concepts
- `analogWrite()`: 0--255 intensity per channel (8-bit PWM)
- Additive color mixing: R+G = yellow, R+B = purple, G+B = cyan, R+G+B = white
- 16.7 million color combinations (256^3)
- Timed color cycling with `delay()` or `millis()`
- PWM frequency and duty cycle

### Libraries
- None (built-in Arduino functions only)

### Code
Not captured by scraper.

---

## Lesson 65 -- Multi-Function Spy Gadget

**Project:** Integrated environment monitor combining DHT11 sensor, LCD1602 display, and RGB LED for color-coded temperature alerts.

### Components
- 1x DHT11 temperature/humidity sensor
- 1x LCD1602 (16x2 character display, parallel mode)
- 1x RGB LED (common cathode)
- Resistors as needed
- HERO XL

### Pin Connections
| Component | Pin |
|-----------|-----|
| LCD RS | Pin 12 |
| LCD Enable | Pin 11 |
| LCD D4 | Pin 2 |
| LCD D5 | Pin 3 |
| LCD D6 | Pin 4 |
| LCD D7 | Pin 5 |
| DHT11 data | Not specified (likely pin 6 or 7) |
| DHT11 VCC | 5V |
| DHT11 GND | GND |
| RGB Red | PWM pin (not specified) |
| RGB Green | PWM pin (not specified) |
| RGB Blue | PWM pin (not specified) |
| RGB common cathode | GND |

### Wiring Notes
- LCD runs in 4-bit mode (D4--D7), using pins 2--5 for data.
- Each component needs its own VCC connection but all share common GND.
- RGB LED color-codes temperature: blue = cold, green = optimal, red = hot.
- DHT11 data pin must not conflict with LCD or RGB assignments.

### Key Concepts
- Multi-sensor system integration: combining inputs and outputs
- Conditional logic: temperature thresholds drive RGB color selection
- Custom functions for multi-pin component control
- Real-time LCD data display with formatted readings
- System architecture: central controller reads sensors, makes decisions, drives outputs

### Libraries
- `LiquidCrystal`
- `DHT` (Adafruit DHT library or similar)

### Code
Not captured by scraper.

---

## Summary: Components by Lesson

| # | Lesson | Key Components | Board |
|---|--------|---------------|-------|
| 51 | Morse Code Transmitter | LED | HERO XL |
| 52 | IR Stealth Alarm | IR receiver, IR remote | HERO XL |
| 53 | Encrypted Messages | LCD1602, push button | HERO XL |
| 54 | Motion Detection | HC-SR501 PIR | HERO XL |
| 55 | RFID Decoder | MFRC-522, RFID card/tag | HERO XL |
| 56 | Sound Surveillance | KY-037, stepper + ULN2003, joystick, RGB LED | HERO XL |
| 57 | Wireless Signal Detector | (built-in WiFi + TFT) | ESP32 T-Display |
| 58 | Two-Way Communication | Unknown (not captured) | Unknown |
| 59 | Spy Motion Tracker | Unknown (not captured) | Unknown |
| 60 | Weather Station | DHT11, rain sensor | HERO XL |
| 61 | Trap Disarming Simulator | SG90 servo, push button | HERO XL |
| 62 | Hacking Device | 4x4 membrane keypad | HERO XL |
| 63 | Emergency Escape Gadget | 28BYJ-48 stepper + ULN2003 | HERO XL |
| 64 | Color Camouflage | RGB LED | HERO XL |
| 65 | Multi-Function Spy Gadget | DHT11, LCD1602, RGB LED | HERO XL |

## Libraries Referenced

| Library | Lessons | Install |
|---------|---------|---------|
| `IRremote` | 52 | PlatformIO: `mxgxw/IRremote` |
| `LiquidCrystal` | 53, 65 | Built-in (Arduino framework) |
| `MFRC522` | 55 | PlatformIO: `miguelbalboa/MFRC522` |
| `Servo` | 61 | Built-in (Arduino framework) |
| `Stepper` | 56, 63 | Built-in (Arduino framework) |
| `Keypad` | 62 | PlatformIO: `chris--a/Keypad` |
| `DHT` | 60, 65 | PlatformIO: `adafruit/DHT sensor library` |
| `WiFi` | 57 | Built-in (ESP32 framework) |
| `TFT_eSPI` | 57 | PlatformIO: `bodmer/TFT_eSPI` |
