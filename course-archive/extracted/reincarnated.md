# Module 12: Reincarnated Into Another World with my HERO Board

Extracted from Crafting Table Pandora's Box course, lessons 66-81.
Board: HERO XL (Mega 2560).

> **Note:** The HTML crawl captured narrative text and wiring instructions but did not capture JavaScript-rendered code blocks. Code sections below are marked as unavailable where the source HTML contained no code. Pin connections and wiring instructions are fully extracted.

---

## Lesson 66 — Introduction

No technical content. Module overview and storyline setup only.

---

## Lesson 67 — RGB LED Color Cycling with Potentiometer

**Fantasy name:** Magical Color Wheel

### Components
- RGB LED module (common cathode)
- Potentiometer (10K)

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| RGB LED Red | D3 | PWM pin, 256 brightness levels |
| RGB LED Green | D5 | PWM pin |
| RGB LED Blue | D6 | PWM pin |
| RGB LED GND | GND | |
| Potentiometer center | A0 | Analog input, 0-1023 |
| Potentiometer outer 1 | 5V | |
| Potentiometer outer 2 | GND | |

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-2d5cDiAT.png`

### Key Concepts
- PWM (Pulse Width Modulation) for analog-like output on digital pins
- Analog input reading (0-1023) from potentiometer voltage divider
- RGB color mixing: independent control of red, green, blue intensity
- Modular arithmetic for cycling through the color spectrum from a single analog input
- Each color channel has 256 brightness levels (0-255), yielding 16 million+ combinations

### Libraries Required
- None (built-in `analogRead`, `analogWrite`)

### Warnings
- If the RGB LED gets hot or dims unexpectedly, add 220-330 ohm current-limiting resistors on each color pin. Some modules have these built in.

### Code
Not captured in HTML crawl.

---

## Lesson 68 — Light-Responsive LED Brightness (Photoresistor)

**Fantasy name:** Magic Sensor Light

### Components
- Photoresistor (LDR / light-dependent resistor)
- LED
- 10K ohm resistor (pull-down)
- 220 ohm resistor (LED current limiting, implied)

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| Photoresistor leg 1 | A0 | Analog input |
| Photoresistor leg 2 | 5V | |
| 10K resistor | A0 to GND | Pull-down, forms voltage divider with LDR |
| LED positive (long leg) | D9 | PWM pin for brightness control |
| LED negative (short leg) | GND | Via 220 ohm resistor (implied) |

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-7rn-5Vrn.png`

### Key Concepts
- Photoresistor behavior: low resistance in bright light, high resistance in dark
- Voltage divider circuit: photoresistor + fixed resistor creates variable voltage
- Inverse mapping: darker environment produces brighter LED output
- Analog-to-digital conversion: HERO XL reads 0-1023 from analog pins
- PWM output for smooth LED brightness control (not just on/off)

### Libraries Required
- None (built-in `analogRead`, `analogWrite`)

### Code
Not captured in HTML crawl.

---

## Lesson 69 — Temperature and Humidity Monitor with LCD

**Fantasy name:** Mystical Temperature Reader

### Components
- DHT11 temperature and humidity sensor
- LCD1602 (16x2 character display)
- Potentiometer (for LCD contrast, optional)

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| DHT11 VCC | 5V | |
| DHT11 GND | GND | |
| DHT11 DATA | D8 | Digital pin for sensor protocol |
| LCD VSS | GND | |
| LCD VDD | 5V | |
| LCD RW | GND | |
| LCD V0 (contrast) | Potentiometer center | Optional, for brightness/contrast control |
| LCD RS | D12 | Register select |
| LCD Enable | D11 | |
| LCD D4 | D2 | 4-bit mode |
| LCD D5 | D3 | |
| LCD D6 | D4 | |
| LCD D7 | D5 | |

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-hgDHd7yQ.png`

### Key Concepts
- DHT11 sensor: capacitive humidity element + thermistor in one package
- 4-bit LCD mode saves pins (uses D4-D7 only) while maintaining full functionality
- Dual sensor readings: temperature (Celsius) and humidity (%) displayed simultaneously
- Error handling for sensor read failures
- Timing intervals for sensor polling (DHT11 needs ~2 seconds between reads)

### Libraries Required
- `LiquidCrystal` (built-in)
- `DHT` (DHT sensor library, e.g., Adafruit DHT or SimpleDHT)

### Code
Not captured in HTML crawl.

---

## Lesson 70 — Ultrasonic Distance Tracker with Servo and LCD

**Fantasy name:** Mystical Object Tracker

### Components
- HC-SR04 ultrasonic distance sensor
- Servo motor (SG90, 180 degrees)
- LCD1602 (16x2 character display)

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| LCD RS | D12 | |
| LCD Enable | D11 | |
| LCD D4 | D5 | 4-bit mode data lines |
| LCD D5 | D4 | |
| LCD D6 | D3 | |
| LCD D7 | D2 | |
| Servo signal | D8 | PWM for position control |
| HC-SR04 Trig | D9 | Sends 10us ultrasonic pulse |
| HC-SR04 Echo | D10 | Returns pulse proportional to distance |
| All VCC | 5V | |
| All GND | GND | |

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-cOuRDtC_.png`

### Key Concepts
- Ultrasonic ranging: distance = (echo duration * 0.034) / 2 cm
- HC-SR04 sends 40 kHz pulses, measures echo return time
- Servo snaps to a preset angle when an object is detected within 15 cm threshold
- Combining sensor input + actuator output + display for a complete detection system
- `pulseIn()` for measuring echo duration with microsecond precision

### Libraries Required
- `LiquidCrystal` (built-in)
- `Servo` (built-in)

### Code
Not captured in HTML crawl.

---

## Lesson 71 — Tone Generator with Buttons and Potentiometer

**Fantasy name:** Magic Melody Machine

### Components
- Passive buzzer (KY-006)
- Potentiometer (10K)
- 4 push buttons

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| Buzzer positive | D9 | PWM pin for tone generation |
| Buzzer negative | GND | |
| Potentiometer center | A0 | Analog input for base frequency |
| Potentiometer outer 1 | 5V | |
| Potentiometer outer 2 | GND | |
| Button 1 | D2 | With INPUT_PULLUP |
| Button 2 | D3 | With INPUT_PULLUP |
| Button 3 | D4 | With INPUT_PULLUP |
| Button 4 | D5 | With INPUT_PULLUP |
| All button other leg | GND | Common ground |

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-2_LLrW2u.png`

### Key Concepts
- `tone()` function generates square waves at specified frequencies on PWM pins
- Potentiometer sweeps through a frequency range (mapped from 0-1023 to a musical range)
- Each button multiplies the base frequency: 1x, 2x, 3x, 4x (harmonic overtones)
- `INPUT_PULLUP` mode eliminates need for external pull-up resistors (active LOW)
- Frequency mapping: `map()` translates analog range to audible frequency range
- Harmonic series: overtones at integer multiples of fundamental frequency

### Libraries Required
- None (built-in `tone()`, `noTone()`, `analogRead`, `digitalRead`)

### Code
Not captured in HTML crawl.

---

## Lesson 72 — Temperature-Triggered Fan with Relay and LCD

**Fantasy name:** Mystical Climate Wind

### Components
- DHT11 temperature and humidity sensor
- Relay module (5V, single channel)
- DC motor with fan blade
- LCD1602 (16x2 character display)

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| DHT11 DATA | D8 | Digital communication |
| DHT11 VCC | 5V | |
| DHT11 GND | GND | |
| Relay signal (IN) | D9 | Controls relay coil |
| LCD connections | Same as lesson 69 | RS=12, EN=11, D4-D7=2-5 |
| Motor | Via relay NO/COM terminals | Switched by relay, not directly from GPIO |

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-NjpigEEm.png`

### Key Concepts
- Threshold-based automation: fan activates when temperature exceeds 31 degrees C
- Relay as an electronic switch for high-power loads (motor cannot be driven from GPIO)
- DHT11 provides both temperature and humidity readings
- LCD displays real-time temperature and fan status
- Automated decision-making: no human intervention required
- Relay module acts as electrical isolation between low-power control circuit and motor

### Libraries Required
- `LiquidCrystal` (built-in)
- `DHT` (DHT sensor library)

### Warnings
- Never drive motors directly from GPIO pins. Use relay module or transistor driver.
- Relay switching can be heard as a mechanical click.

### Code
Not captured in HTML crawl.

---

## Lesson 73 — Stepper Motor Random Position on Button Press

**Fantasy name:** Magic Stepper Oracle

### Components
- 28BYJ-48 stepper motor
- ULN2003 driver board
- Push button

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| ULN2003 IN1 | D8 | Coil control |
| ULN2003 IN2 | D10 | Coil control |
| ULN2003 IN3 | D9 | Coil control |
| ULN2003 IN4 | D11 | Coil control |
| ULN2003 VCC | 5V | Motor power |
| ULN2003 GND | GND | |
| Button | Digital pin (not specified in crawl) | With pull-up resistor |
| Stepper motor | 5-pin connector to ULN2003 | Direct plug-in |

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-E_w9ge26.png`

### Key Concepts
- Stepper motors move in discrete steps (2048 steps per revolution for 28BYJ-48 in half-step mode)
- Step angle: 5.625 degrees / 64 gear ratio
- ULN2003 driver translates 5V logic to motor coil drive signals
- Electromagnets energized in sequence create rotating magnetic field
- Random position generation on button press (simulates "oracle" divination)
- Precise positioning unlike DC motors: can hold exact angles

### Libraries Required
- `Stepper` (built-in) or `AccelStepper`

### Code
Not captured in HTML crawl.

---

## Lesson 74 — Number Guessing Game with Rotary Encoder and 7-Segment Display

**Fantasy name:** Magic Number Guesser

### Components
- 1-digit 7-segment display
- KY-040 rotary encoder
- Passive buzzer

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| 7-segment A-G, DP | D2-D8, D10 | Direct segment control |
| Rotary encoder CLK | D11 | Quadrature signal A |
| Rotary encoder DT | D10 | Quadrature signal B |
| Rotary encoder SW | D9 | Push button, use INPUT_PULLUP |
| Buzzer positive | D12 | Audio feedback |
| Buzzer negative | GND | |

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-2048MMPW.png`

### Key Concepts
- Rotary encoder: infinite rotation, outputs quadrature pulses for direction detection
- Debouncing encoder button presses in software
- 7-segment display: direct segment control (each segment individually addressed)
- Random number generation for game target
- Game state management: guess, compare, feedback loop
- Audio feedback via buzzer for correct/incorrect guesses

### Libraries Required
- None (built-in digital I/O, `tone()`, `random()`)

### Code
Not captured in HTML crawl.

---

## Lesson 75 — Joystick-Controlled LCD Cursor Navigation

**Fantasy name:** Magic Labyrinth Navigator

### Components
- LCD1602 (16x2 character display)
- Analog joystick module

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| LCD RS | D2 | Register select |
| LCD Enable | D3 | |
| LCD D4 | D4 | 4-bit mode |
| LCD D5 | D5 | |
| LCD D6 | D6 | |
| LCD D7 | D7 | |
| LCD VSS, RW | GND | |
| LCD VDD | 5V | |
| Joystick VRx | A0 | X-axis analog (0-1023) |
| Joystick VRy | A1 | Y-axis analog (0-1023) |
| Joystick VCC | 5V | |
| Joystick GND | GND | |

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-IjtxXjSe.png`

### Key Concepts
- Analog joystick uses two potentiometers (X and Y axes), each outputting 0-1023
- Center position reads approximately 512 on both axes
- `map()` function scales joystick range (0-1023) to LCD coordinates (0-15 columns, 0-1 rows)
- Real-time cursor movement on LCD based on joystick position
- Foundation for menu navigation and interactive UI systems

### Libraries Required
- `LiquidCrystal` (built-in)

### Code
Not captured in HTML crawl.

---

## Lesson 76 — LED Reflex Training Game (Whack-a-Mole Style)

**Fantasy name:** Magical Training System

### Components
- 5 LEDs (various colors)
- 5 push buttons
- Passive buzzer
- 5 current-limiting resistors (220 ohm, for LEDs)

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| LED 1 | D8 | Through current-limiting resistor |
| LED 2 | D9 | |
| LED 3 | D10 | |
| LED 4 | D11 | |
| LED 5 | D12 | |
| Button 1 | D2 | With internal pull-up/pull-down |
| Button 2 | D3 | |
| Button 3 | D4 | |
| Button 4 | D5 | |
| Button 5 | D6 | |
| Buzzer | D7 | PWM-capable for frequency control |

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-3Sz3D1Xk.png`

### Key Concepts
- Random target selection: system randomly lights one LED at a time
- Reaction time measurement with millisecond precision using `millis()`
- Multiple simultaneous input monitoring (5 buttons)
- Audio feedback for hits and misses
- Real-time interactive system: stimulus -> response -> feedback loop
- State management for game logic (active target, score tracking, timing)

### Libraries Required
- None (built-in `digitalRead`, `digitalWrite`, `tone()`, `millis()`, `random()`)

### Code
Not captured in HTML crawl.

---

## Lesson 77 — Clock Display with Rotary Encoder Time Adjustment

**Fantasy name:** Magical Rune Decoder

### Components
- LCD1602 (16x2 character display)
- KY-040 rotary encoder

### Pin Connections
Wiring details cut off in HTML crawl. Based on lesson context:

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| LCD connections | Standard 4-bit mode | RS, EN, D4-D7 |
| Rotary encoder CLK | Digital pin | Quadrature signal |
| Rotary encoder DT | Digital pin | Quadrature signal |
| Rotary encoder SW | Digital pin | Push button (reset) |

### Key Concepts
- Software clock displayed on LCD (no RTC module -- pure software timekeeping)
- Rotary encoder adjusts hours and minutes
- Quadrature decoding: two out-of-phase signals determine rotation direction
- Time overflow/wraparound: 59 minutes -> 0 minutes (increment hour), and reverse
- Button press resets time
- Debouncing for mechanical encoder contacts

### Libraries Required
- `LiquidCrystal` (built-in)

### Code
Not captured in HTML crawl.

---

## Lesson 78 — Time Adjuster with Rotary Encoder and 4-Digit Display

**Fantasy name:** Time Magic Adjuster

### Components
- KY-040 rotary encoder
- 4-digit 7-segment display (or LCD -- context suggests display for time)

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| Encoder CLK | D8 | Timing signal |
| Encoder DT | D9 | Direction signal |
| Encoder SW | D10 | Push button (reset to 12:00) |
| Encoder VCC | 5V | |
| Encoder GND | GND | |

Display connections not specified in crawl (likely 4-digit 7-segment or LCD).

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-F07sabQ_.png`

### Key Concepts
- Rotary encoder as infinite-rotation precision input (vs potentiometer with end stops)
- Quadrature encoding: two slightly out-of-phase digital pulses reveal direction
- Direction detection: which signal leads determines clockwise vs counterclockwise
- Time wraparound: 23:59 -> 00:00 and 00:00 -> 23:59 (24-hour cycle)
- Button debouncing for mechanical switches
- Professional-grade analog control interface principles

### Libraries Required
- Display library (depends on display type used)

### Code
Not captured in HTML crawl.

---

## Lesson 79 — Potentiometer-Controlled Servo Position

**Fantasy name:** Magic Servo Dial

### Components
- Servo motor (SG90, 180 degrees)
- Potentiometer (10K)

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| Servo red wire (VCC) | 5V | Needs steady 5V, not 3.3V |
| Servo brown/black (GND) | GND | |
| Servo orange/yellow (signal) | D9 | PWM position command |
| Potentiometer center | A0 | Analog input (assumed, standard pattern) |
| Potentiometer outer 1 | 5V | |
| Potentiometer outer 2 | GND | |

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-aLICkZfl.jpeg`

### Key Concepts
- Servo motors move to exact angles (0-180 degrees) and hold position
- Internal position feedback sensor: servo knows its current angle
- `map()` converts analog input (0-1023) to servo range (0-180 degrees)
- Direct tactile control: turning potentiometer immediately moves servo
- Difference between continuous rotation DC motors and position-controlled servos
- Servo signal is PWM-based pulse width encoding (not simple duty cycle)

### Libraries Required
- `Servo` (built-in)

### Code
Not captured in HTML crawl.

---

## Lesson 80 — RTC-Triggered Timed Event System with LCD

**Fantasy name:** Magic Timebomb

### Components
- DS3231 Real-Time Clock module (with AT24C32 EEPROM)
- LCD1602 (16x2 character display)
- LED
- 220 ohm resistor (for LED)
- 10K potentiometer (for LCD contrast)

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| DS3231 VCC | 5V | |
| DS3231 GND | GND | |
| DS3231 SDA | A4 | I2C data (dedicated pin) |
| DS3231 SCL | A5 | I2C clock (dedicated pin) |
| LCD VSS | GND | |
| LCD VDD | 5V | |
| LCD RW | GND | |
| LCD V0 | Potentiometer center | Contrast adjustment |
| LCD RS | D2 | |
| LCD Enable | D3 | |
| LCD D4 | D4 | 4-bit mode |
| LCD D5 | D5 | |
| LCD D6 | D6 | |
| LCD D7 | D7 | |
| LED | D13 | Through 220 ohm resistor to GND |

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-EwvJr1mf.png`

### Key Concepts
- DS3231 RTC maintains accurate time via CR2032 battery backup (survives power loss)
- Crystal oscillator at 32,768 Hz (2^15) for binary-friendly counting
- I2C communication: only 2 data wires (SDA, SCL) plus power
- RTC I2C address: 0x68
- Conditional time-based triggering: LED activates at a specific time
- Time displayed on LCD with proper formatting
- Automation without human intervention (works even during sleep/absence)
- Power loss recovery: RTC retains time, code re-reads on startup

### Libraries Required
- `RTClib` (by Adafruit)
- `Wire` (built-in, for I2C)
- `LiquidCrystal` (built-in)

### Code
Not captured in HTML crawl.

---

## Lesson 81 — Touchscreen Phone Interface (LCD Touchscreen Shield)

**Fantasy name:** Magical TouchScreen Rune Scribe

### Components
- 2.4" LCD Touchscreen Shield (320x240, resistive touch)

### Pin Connections

| Component Pin | HERO XL Pin | Notes |
|---------------|-------------|-------|
| Touch Y+ / Y- | A3, A2 | Analog pins read touch coordinates |
| Touch X+ / X- | D8, D9 | Digital pins provide drive current |
| Display control | A0, A1, A4 | LCD graphics rendering and color |
| Shield power | 3.3V and 5V | Both voltage rails required |
| Shield GND | GND | |

Note: The touchscreen shield plugs directly onto the HERO XL headers.

### Wiring Diagram
Image: `/uploads/course-images/pandoras-box-wiring-wltqQW51.jpeg`

### Key Concepts
- Resistive touchscreen: two conductive layers make contact under pressure
- Touch coordinate detection via analog voltage measurement
- Works with gloves, styluses, or any pressure-applying object (unlike capacitive)
- Button grid layout: mapping screen regions to virtual buttons
- Touch event handling: detect press, determine coordinates, match to button
- Visual feedback on press (button state change rendering)
- Phone-style keypad interface with numbers, letters, and icons
- Combining graphics library with touch library for interactive UI

### Libraries Required
- `MCUFRIEND_kbv` or `Adafruit_TFTLCD` (for display)
- `TouchScreen` (for touch input)
- `Adafruit_GFX` (graphics primitives)

### Code
Not captured in HTML crawl.

---

## Component Summary

All 15 projects (lessons 67-81) use the HERO XL (Mega 2560) board.

| Lesson | Project | Key Components |
|--------|---------|----------------|
| 67 | RGB LED Color Cycling | RGB LED, Potentiometer |
| 68 | Light-Responsive LED | Photoresistor, LED |
| 69 | Temp/Humidity Monitor | DHT11, LCD1602 |
| 70 | Ultrasonic Distance Tracker | HC-SR04, Servo, LCD1602 |
| 71 | Tone Generator | Passive buzzer, 4 buttons, Potentiometer |
| 72 | Temp-Triggered Fan | DHT11, Relay, DC motor, LCD1602 |
| 73 | Stepper Random Position | 28BYJ-48, ULN2003, Button |
| 74 | Number Guessing Game | Rotary encoder, 7-segment display, Buzzer |
| 75 | Joystick LCD Cursor | Joystick, LCD1602 |
| 76 | LED Reflex Trainer | 5 LEDs, 5 buttons, Buzzer |
| 77 | Clock with Encoder Adjust | Rotary encoder, LCD1602 |
| 78 | Time Adjuster | Rotary encoder, Display |
| 79 | Potentiometer Servo Control | Servo SG90, Potentiometer |
| 80 | RTC Timed Event Trigger | DS3231, LCD1602, LED |
| 81 | Touchscreen Phone UI | 2.4" LCD Touchscreen Shield |

## Unique Libraries Used Across Module

| Library | Lessons | Built-in? |
|---------|---------|-----------|
| `LiquidCrystal` | 69, 70, 72, 75, 77, 80 | Yes |
| `Servo` | 70, 79 | Yes |
| `DHT` | 69, 72 | No (install via PlatformIO) |
| `RTClib` | 80 | No (Adafruit, install via PlatformIO) |
| `Wire` | 80 | Yes |
| `Stepper` | 73 | Yes |
| `MCUFRIEND_kbv` / `Adafruit_TFTLCD` | 81 | No |
| `TouchScreen` | 81 | No |
| `Adafruit_GFX` | 81 | No |
