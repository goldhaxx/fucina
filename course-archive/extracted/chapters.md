# Chapter Lessons

Extracted from `Lessons/` -- the "AI Apocalypse" storyline course by inventr.io.

**Story premise:** Year 2042. AI has gone rogue. Two survivors (Eric and Roomy) find an old inventr.io warehouse with pre-AI era electronics. They use Arduino components to rebuild systems for their new base.

---

## Chapter 01 — Moving In (Getting Started)

**Theme:** Set up the base -- lights, switches, power management.

### Lesson 01: Does It Still Work? (Blink)

**Parts:** HERO XL, USB cable, computer
**Concepts:** Arduino IDE setup, setup(), loop(), pinMode(), digitalWrite(), delay()

Standard blink sketch using LED_BUILTIN. Verifies board and IDE connectivity.

```cpp
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
```

### Lesson 02: Light Up This Place (External LED)

**Parts:** LED, 220 ohm resistor, breadboard, jumper wires
**Pins:** LIGHT_PIN = 22
**Concepts:** Constants (`const uint8_t`), named pins, breadboard wiring, #include, block/single-line comments, data types

Pin selection guidance: Use D22-D49 for fewest conflicts (avoids Serial, SPI, I2C, PWM, interrupts).

```cpp
#include "Arduino.h"

const uint8_t LIGHT_PIN = 22;
const uint8_t ON = HIGH;
const uint8_t OFF = LOW;

void setup() {
  pinMode(LIGHT_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LIGHT_PIN, ON);
  delay(1000);
  digitalWrite(LIGHT_PIN, OFF);
  delay(1000);
}
```

### Lesson 03: Add Light Switches (Push Button)

Four progressive versions:

**03.10 — Button No Resistor (Floating Pin Demo)**
- Pins: LIGHT_PIN=22, LIGHT_BUTTON=23
- Demonstrates floating pin problem (random HIGH/LOW when button not pressed)
- Concepts: digitalRead(), if statements, INPUT mode

```cpp
#include "Arduino.h"

const uint8_t LIGHT_PIN = 22;
const uint8_t LIGHT_BUTTON = 23;
const uint8_t ON = HIGH;
const uint8_t OFF = LOW;

void setup() {
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(LIGHT_BUTTON, INPUT);
}

void loop() {
  if (digitalRead(LIGHT_BUTTON) == HIGH) {
    digitalWrite(LIGHT_PIN, ON);
  }
  if (digitalRead(LIGHT_BUTTON) == LOW) {
    digitalWrite(LIGHT_PIN, OFF);
  }
  delay(50);
}
```

**03.20 — Button with Pull-Down Resistor**
- Adds external 10K pull-down resistor
- Concepts: if-else, pull-down resistors, stable inputs

```cpp
#include "Arduino.h"

const uint8_t LIGHT_PIN = 22;
const uint8_t LIGHT_BUTTON = 23;
const uint8_t ON = HIGH;
const uint8_t OFF = LOW;

void setup() {
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(LIGHT_BUTTON, INPUT);
}

void loop() {
  if (digitalRead(LIGHT_BUTTON) == HIGH) {
    digitalWrite(LIGHT_PIN, ON);
  } else {
    digitalWrite(LIGHT_PIN, OFF);
  }
  delay(50);
}
```

**03.30 — Button with INPUT_PULLUP**
- Uses built-in pull-up resistor (no external resistor needed)
- Inverted logic: PRESSED = LOW
- Concepts: INPUT_PULLUP, named constants for readability

```cpp
#include "Arduino.h"

const uint8_t LIGHT_PIN = 22;
const uint8_t LIGHT_BUTTON = 23;
const uint8_t ON = HIGH;
const uint8_t OFF = LOW;
const uint8_t PRESSED = LOW;

void setup() {
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(LIGHT_BUTTON, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(LIGHT_BUTTON) == PRESSED) {
    digitalWrite(LIGHT_PIN, ON);
  } else {
    digitalWrite(LIGHT_PIN, OFF);
  }
  delay(50);
}
```

**03.40 — Toggle Button (Light Switch)**
- Press once = on, press again = off
- Concepts: boolean variables, variable scope (global vs local), state tracking, toggle logic

```cpp
#include "Arduino.h"

const uint8_t LIGHT_PIN = 22;
const uint8_t LIGHT_BUTTON = 23;
const uint8_t ON = HIGH;
const uint8_t OFF = LOW;
const uint8_t PRESSED = LOW;
const uint8_t NOT_PRESSED = HIGH;

bool light_is_on = false;
bool previous_button_state = NOT_PRESSED;

void setup() {
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(LIGHT_BUTTON, INPUT_PULLUP);
}

void loop() {
  uint8_t button_state = digitalRead(LIGHT_BUTTON);
  if (button_state != previous_button_state) {
    if (button_state == PRESSED) {
      if (light_is_on) {
        digitalWrite(LIGHT_PIN, OFF);
        light_is_on = false;
      } else {
        digitalWrite(LIGHT_PIN, ON);
        light_is_on = true;
      }
    }
    previous_button_state = button_state;
  }
  delay(50);
}
```

### Lesson 04: Charging the Batteries (Photoresistor + Analog Input)

Four progressive versions using photoresistor to simulate solar panels.

**Pins:** LIGHT_PIN=22, LIGHT_BUTTON=23, CHARGING_RATE=A8
**Parts added:** Photoresistor, 10K resistor

**04.10** — Read photoresistor, display via Serial Monitor/Plotter
- Concepts: analogRead(), Serial.begin/print/println, Serial Plotter, uint16_t

**04.15** — Map values to percentage, add labels for Serial Plotter
- Concepts: map(), labeled Serial Plotter output, conditional compilation (#define, #if/#elif/#else/#endif)

**04.20** — Battery charging simulation
- Concepts: float data type, `+=` operator, calculated constants for simulation timing

**04.30** — Full simulation with battery limits and light power draw
- Concepts: `-=` operator, charge/discharge hysteresis, battery protection limits (LOW_BATTERY_LIMIT=10%, HIGH_BATTERY_LIMIT=90%), auto light shutoff

Key simulation constants:
```cpp
const float LOW_BATTERY_LIMIT = 10;
const float HIGH_BATTERY_LIMIT = 90;
const float RESUME_CHARGING_AT = HIGH_BATTERY_LIMIT - 5.0;
const uint8_t SECONDS_TO_FULL = 30;
const uint8_t LOOPS_PER_SECOND = 20;
const int AVERAGE_CHARGE_LEVEL = 420;
```

### Lesson 05: Low Battery Warning (Buzzer + millis())

Four progressive versions of low-battery alert.

**Pins added:** ALARM_PIN = 24
**Parts added:** Active buzzer (v1-3), passive buzzer (v4)

**v1** — Continuous buzzer when battery low (annoying!)
**v2** — Beep 3 times using delay() (freezes Serial Plotter)
**v3** — Beep 3 times using millis() (non-blocking)
**v4** — Play descending tone sequence using tone()/noTone() with passive buzzer

Key concepts: millis() for non-blocking timing, tone()/noTone(), arrays, array indexing, sizeof()

Tone array for v4:
```cpp
const int16_t TONES[] = { 880, 698, 587 };
```

### Lesson 06: Dimming the Lights (Potentiometer + PWM)

Four progressive versions.

**Pins added:** LIGHT_DIMMER = A9, LIGHT_PIN moved to 44 (PWM capable in v3+)
**Parts added:** Potentiometer for dimmer control

**v1** — Read potentiometer as percentage
**v2** — Reverse map() direction (clockwise = brighter)
**v3** — analogWrite() for PWM dimming on pin 44
**v4** — Battery drain proportional to dimmer setting

Key concepts: PWM (Pulse Width Modulation), analogWrite() (0-255), reverse map(), pins D2-D13 and D44-D46 support PWM

---

## Chapter 02 — Base Security

**Theme:** Secure the building with sensors and locks.

### Lesson 01: Motion Sensor Lights (PIR Sensor)

**Parts:** PIR motion sensor (HC-SR501), LED
**Pins:** FLOOD_LIGHTS=22, MOTION_SENSOR=23

```cpp
#include "Arduino.h"

const int FLOOD_LIGHTS = 22;
const int MOTION_SENSOR = 23;
const uint8_t ON = HIGH;
const uint8_t OFF = LOW;

void setup() {
  pinMode(MOTION_SENSOR, INPUT);
  pinMode(FLOOD_LIGHTS, OUTPUT);
}

void loop() {
  bool motion_detected = digitalRead(MOTION_SENSOR);
  if (motion_detected) {
    digitalWrite(FLOOD_LIGHTS, ON);
  } else {
    digitalWrite(FLOOD_LIGHTS, OFF);
  }
}
```

### Lesson 02: Keypad Door Lock (4x4 Keypad)

**Parts:** 4x4 membrane keypad
**Pins:** ROW_PINS={23,25,27,29}, COL_PINS={31,33,35,37}
**Libraries:** Keypad

Secret code entry with `*` to reset, `#` to delete last character.

```cpp
#include "Arduino.h"
#include <Keypad.h>

const byte ROWS = 4;
const byte COLS = 4;
const byte ROW_PINS[ROWS] = { 23, 25, 27, 29 };
const byte COL_PINS[COLS] = { 31, 33, 35, 37 };
const char BUTTONS[ROWS][COLS] = {
  { '1', '2', '3', 'A' },
  { '4', '5', '6', 'B' },
  { '7', '8', '9', 'C' },
  { '*', '0', '#', 'D' }
};

Keypad security_keypad = Keypad(makeKeymap(BUTTONS), ROW_PINS, COL_PINS, ROWS, COLS);
const String SECRET_CODE = "1234";
String entered_code = "";

void setup() { Serial.begin(9600); }

void loop() {
  char key = security_keypad.getKey();
  if (key) {
    if (key == '*') { entered_code = ""; return; }
    if (key == '#') {
      entered_code = entered_code.substring(0, entered_code.length() - 1);
      return;
    }
    entered_code += key;
    if (entered_code.length() == SECRET_CODE.length()) {
      if (entered_code == SECRET_CODE) {
        Serial.println("Entered code matches - unlock door for 2 seconds");
        delay(2000);
        Serial.println("Re-lock door");
      } else {
        Serial.println("Wrong combination entered");
      }
      entered_code = "";
    }
  }
}
```

### Lesson 03: RFID Door Locks

**Parts:** RFID-RC522 reader, NFC card/keychain tag, 4x4 keypad
**Concept:** NFC badge for authentication (brute-force resistant vs. keypad)

### Lesson 04: RTTTL Alarm (Ringtone Tunes)

**Parts:** Passive buzzer
**Pin:** tonePin = 24

Plays RTTTL (RingTone Text Transfer Language) songs using tone(). Includes many classic tunes (Never Gonna Give You Up, Star Wars, Indiana Jones, Mission Impossible, etc.) stored as RTTTL strings.

RTTTL format: `name:d=N,o=N,b=NNN:notes...`

Notes frequency table (C4-B6) built into the sketch. Parser handles duration, note, sharp, dotted notes, and octave.

---

## Chapter 03 — Green House

**Theme:** Grow food, monitor environment.

### Lesson 01: Dry Plant Alert System

**Parts:** Water level sensor, LED
**Pins:** ledPin=22, sensorPin=A8

```cpp
#define ledPin 22
#define sensorPin A8

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}

void loop() {
  unsigned int sensorValue = analogRead(sensorPin);
  if (sensorValue < 540) return;
  uint8_t outputValue = map(sensorValue, 540, 800, 0, 255);
  Serial.print(sensorValue);
  Serial.print(" ");
  Serial.println(outputValue);
  analogWrite(ledPin, outputValue);
}
```

### Lesson 02: Weather Station
**Parts:** Temperature and humidity sensor (DHT11)

### Lesson 03: Automatic Fan Ventilation System
**Parts:** Fan motor (direct drive attempt -- note: this fails/burns the board!)

### Lesson 04: Huge Fan (Relay Module)
**Parts:** Relay module for high-power fan control
**Lesson:** GPIO cannot power large loads directly. Use relay module.

---

## Chapter 04 — Daily Life

**Theme:** Quality of life improvements.

### Lesson 01: Accurate Alarm Clock

**Parts:** DS3231 RTC, 4-digit 7-segment display, buzzer
**Pins:** buzzerPin=45, digitPins={2,3,4,5}, segmentPins={6,7,8,9,10,11,12,13}
**Libraries:** Wire, DS3231, LibPrintf, SevSeg

Combines RTC for accurate time, 7-segment display for time readout, and buzzer for alarm. Set time via serial YYMMDDwHHMMSS format.

```cpp
#include <Wire.h>
#include <DS3231.h>
#include <LibPrintf.h>
#include "SevSeg.h"

const int buzzerPin = 45;
DS3231 rtc;
SevSeg sevseg;
RTClib myRTC;
int alarmHour = 10;
int alarmMinute = 11;

void setup () {
  Serial.begin(115200);
  while(!Serial);
  Wire.begin();
  delay(500);

  byte numDigits = 4;
  byte digitPins[] = {2,3,4,5};
  byte segmentPins[] = {6, 7, 8, 9, 10, 11, 12, 13};
  bool resistorsOnSegments = false;
  sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins, resistorsOnSegments, false, true);
  sevseg.setBrightness(100);
  pinMode(buzzerPin, OUTPUT);
}

void loop () {
  // Serial time-setting code omitted for brevity (same as 140-RealTimeClock)

  DateTime now = myRTC.now();
  int displayTime = (now.hour() * 100) + now.minute();
  sevseg.setNumber(displayTime);
  sevseg.refreshDisplay();

  if (now.hour() == alarmHour && now.minute() == alarmMinute) {
    alarmBuzzer();
  } else {
    digitalWrite(buzzerPin, LOW);
  }
}

void alarmBuzzer() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(buzzerPin, HIGH);
    delay(200);
    digitalWrite(buzzerPin, LOW);
    delay(200);
  }
}
```

### Lesson 02: Automatic Summer Fan
**Parts:** Temperature/humidity sensor + fan motor

### Lesson 03: IR Smart Lights (5 progressive versions)
**Parts:** IR remote + receiver
**Concept:** Control lights via IR remote

### Lesson 04: Clap Lights
**Parts:** Sound sensor (KY-038)
**Concept:** Toggle lights by clapping

### Lesson 05: Party Time (placeholder)
### Lesson 06: Microsoft Paint Clone (placeholder -- touchscreen drawing)

---

## Chapter 05 — Spy vs Spy (WiFi -- ESP32)

**Theme:** WiFi-controlled lights using ESP32 TTGO T-Display
**Note:** Marked as potentially being removed (placeholder)

Three progressive WiFi sketches:
- **10** — WiFi Light Control AP (access point mode)
- **20** — WiFi Light Control Async AP
- **30** — WiFi Light Control Async (connect to existing network)

---

## Chapter 06 — Base Security++ (Radar System)

**Theme:** Build a sonar/radar security system.

### Lesson 20: 180-Degree Sonar

**Parts:** HC-SR04 ultrasonic sensor, SG90 servo, 240x320 touch screen shield
**Pins:** TRIGGER_PIN=22, ECHO_PIN=23, SERVO_PIN=24
**Libraries:** Servo, MCUFRIEND_kbv

Sweeps servo 0-180 degrees in 2-degree steps, measures distance at each angle, plots results as dots on TFT display (radar-style). Includes servo calibration mode (set to 90 degrees for alignment).

```cpp
#include <Servo.h>
#include <MCUFRIEND_kbv.h>

MCUFRIEND_kbv tft;
const uint8_t TRIGGER_PIN = 22;
const uint8_t ECHO_PIN = 23;
const uint8_t SERVO_PIN = 24;

Servo myservo;

void setup() {
  Serial.begin(9600);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  myservo.attach(SERVO_PIN);
  tft.begin(tft.readID());
  tft.setRotation(0);
  drawRanges();
}

void loop() {
  for (int direction = 0; direction <= 180; direction += 2) {
    myservo.write(direction);
    delay(20);
    distanceCheck(direction);
  }
  for (int direction = 180; direction >= 0; direction -= 2) {
    myservo.write(direction);
    delay(20);
    distanceCheck(direction);
  }
  drawRanges();
}
```

### Lesson 30: RGB Turret Gun
**Parts:** Fan motor, touchscreen, rotary encoder, ultrasonic sensor

### Lesson 40: RGB Turret Gun (T-Display version)

---

## Chapter 07 — Battle the AI

**Theme:** Offensive projects (placeholder/concept only).
1. False Signals
2. Rick Roll 'Em
3. Space Invader Game
4. Attack Tanks

---

## Chapter 08 — Communications and Networking

**Theme:** I2C, SPI, WiFi with ESP32 T-Display

**Planned lessons:**
1. I2C and SPI Communications
2. Connect to WiFi (scanning APs, connecting, NTP time)
3. Send Virtual Signal Flare (IP geolocation to world map via external API)
