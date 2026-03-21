# Parts Tutorials (HERO XL / Mega 2560)

Extracted from `Getting_Started/HERO_XL/` -- individual component test sketches.

---

## 000 — Blink (Built-in LED)

**Component:** Built-in LED (LED_BUILTIN, pin 13)
**Pin Connections:** LED_BUILTIN (pin 13)
**Libraries:** None
**Notes:** Verifies board connectivity. Uses `const uint8_t ON = HIGH; OFF = LOW;` pattern.

```cpp
#include <arduino.h>

const uint8_t OFF = LOW;
const uint8_t ON  = HIGH;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
   digitalWrite(LED_BUILTIN, ON);
   delay(1000);
   digitalWrite(LED_BUILTIN, OFF);
   delay(1000);
}
```

---

## 002 — Light Emitting Diode (LED)

**Component:** Standard LED (any color, two leads)
**Pin Connections:**
| Arduino | LED |
|---------|-----|
| GND | 220 ohm resistor then negative (shorter) lead |
| 2 (or 13) | Positive (longer) LED lead |

**Libraries:** None
**Notes:** 220 ohm resistor required for current limiting at 5V. Long leg = anode (+), short leg = cathode (-).

```cpp
int Light = 2;

void setup() {
  pinMode(Light, OUTPUT);
}

void loop() {
  digitalWrite(Light, HIGH);
  delay(1000);
  digitalWrite(Light, LOW);
  delay(1000);
}
```

---

## 004 — RGB Light Emitting Diode

**Component:** RGB LED (common cathode, 4 pins)
**Pin Connections:**
| Arduino | LED |
|---------|-----|
| 7 | RED lead (alone next to GND) |
| GND | Common pin (longest) |
| 6 | GREEN lead (between GND and BLUE) |
| 5 | BLUE lead (next to GREEN) |

**Libraries:** None
**Notes:** Uses `analogWrite()` for PWM color mixing. 220 ohm resistor on each color pin recommended.

```cpp
constexpr int redPin   = 7;
constexpr int greenPin = 6;
constexpr int bluePin  = 5;

void setup() {
  pinMode(redPin,   OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin,  OUTPUT);
}

void loop() {
  setColor(255, 0, 0); // Red Color
  delay(1000);
  setColor(0, 255, 0); // Green Color
  delay(1000);
  setColor(0, 0, 255); // Blue Color
  delay(1000);
  setColor(255, 255, 255); // White Color
  delay(1000);
  setColor(170, 0, 255); // Purple Color
  delay(1000);
}

void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(redPin,   redValue);
  analogWrite(greenPin, greenValue);
  analogWrite(bluePin,  blueValue);
}
```

---

## 006 — Photo Resistor (LDR)

**Component:** Photoresistor (light-dependent resistor)
**Pin Connections:**
| Arduino | Photoresistor |
|---------|---------------|
| A0 | First lead of photo resistor |
| GND | 10K ohm resistor then A0 lead |
| 5V | Other lead of photo resistor |

**Libraries:** None
**Notes:** Requires 10K pull-down resistor to form a voltage divider. `analogRead()` returns 0-1023 based on light intensity.

```cpp
int sensorPin  = A0;
int onboardLED = LED_BUILTIN;

void setup() {
  Serial.begin(115200);
  pinMode(onboardLED, OUTPUT);
}

void loop() {
  int sensorValue = analogRead(sensorPin);
  Serial.println(sensorValue);
  digitalWrite(onboardLED, HIGH);
  delay(sensorValue);
  digitalWrite(onboardLED, LOW);
  delay(sensorValue);
}
```

---

## 010 — Active Buzzer

**Component:** 2-pin active buzzer (fixed pitch)
**Pin Connections:**
| Arduino | Buzzer |
|---------|--------|
| 2 | + |
| GND | Other |

**Libraries:** None
**Notes:** Active buzzer has built-in oscillator -- just apply voltage for sound. Has a sealed back. No `tone()` needed -- just `digitalWrite()`.

```cpp
const byte          BUZZER_PIN =    2;
const unsigned long ON_LENGTH  = 1000;
const unsigned long OFF_LENGTH = 1000;

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  digitalWrite(BUZZER_PIN, HIGH);
  delay(ON_LENGTH);
  digitalWrite(BUZZER_PIN, LOW);
  delay(OFF_LENGTH);
}
```

---

## 020 — Passive Buzzer (KY-006)

**Component:** 2-pin passive buzzer (variable pitch)
**Pin Connections:**
| Arduino | Buzzer |
|---------|--------|
| 2 | + |
| GND | Other |

**Libraries:** None
**Notes:** Requires PWM signal via `tone()` to produce sound. You control the frequency. The passive buzzer has exposed metal on the back (vs. sealed on active). 3-pin version (KY-006/HW-508) is coded identically.

```cpp
constexpr byte          BUZZER_PIN   =    2;
constexpr unsigned int  TONE_PITCH   =  440;
constexpr unsigned long TONE_LENGTH  = 1000;
constexpr unsigned long CYCLE_LENGTH = 2000;

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  tone(BUZZER_PIN, TONE_PITCH, TONE_LENGTH);
  delay(CYCLE_LENGTH);
}
```

---

## 030 — Potentiometer

**Component:** Potentiometer (B103)
**Pin Connections (single pin = pin 1, proceeding clockwise):**
| Arduino | Potentiometer |
|---------|---------------|
| A0 | Pin 1 (single pin side) |
| 5V | Pin 2 |
| GND | Pin 3 |

**Libraries:** None
**Notes:** Returns 0-1023 via `analogRead()`. Use Serial Plotter for visualization.

```cpp
const byte          ANALOG_PIN =   A0;
const unsigned long BAUD_RATE  = 9600;
const int           PLOT_MIN   =    0;
const int           PLOT_MAX   = 1023;

void setup() {
  Serial.begin(BAUD_RATE);
}

void loop() {
  Serial.print("potentiometer:");
  Serial.print(analogRead(ANALOG_PIN));
  Serial.print(" minimum:");
  Serial.print(PLOT_MIN);
  Serial.print(" maximum:");
  Serial.println(PLOT_MAX);
}
```

---

## 035 — Rotary Encoder (KY-040)

**Component:** KY-040 Rotary Encoder
**Pin Connections:**
| Arduino | Encoder |
|---------|---------|
| GND | GND |
| 5V | + |
| 18 (SW) | SW |
| 3 (DT) | DT |
| 2 (CLK) | CLK |

**Libraries:** BasicEncoder
**Notes:** Uses interrupts (pins 2, 3, 18) for responsive rotation detection. Not a potentiometer -- outputs pulses. Requires debouncing for switch press.

```cpp
#include <BasicEncoder.h>

constexpr int CLK = 2;
constexpr int DT = 3;
constexpr int SW = 18;

int previousCounter = 0;
BasicEncoder encoder(CLK, DT);

void setup() {
  pinMode(SW, INPUT_PULLUP);
  Serial.begin(115200);
  delay(1000);
  Serial.print("Counter: ");
  Serial.println(encoder.get_count());
  attachInterrupt(digitalPinToInterrupt(CLK), updateEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(DT), updateEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(SW), updateSwitch, CHANGE);
}

void loop() {
  if (encoder.get_change()) {
    int counter = encoder.get_count();
    Serial.print("Counter: ");
    Serial.println(counter);
    if(previousCounter < 10 && counter >= 10) {
      Serial.println("---------->PASSED 10!");
    }
    if(previousCounter < 20 && counter >= 20) {
      Serial.println("---------->PASSED 20!");
    }
    if(previousCounter < 30 && counter >= 30) {
      Serial.println("---------->PASSED 30!");
    }
    previousCounter = counter;
  }
}

void updateEncoder() {
  encoder.service();
}

bool pressed = false;
void updateSwitch() {
  if (pressed && digitalRead(SW) == HIGH) {
    Serial.println("SWITCH RELEASED");
    pressed = false;
    delay(50);
  }
  if (!pressed && digitalRead(SW) == LOW) {
    Serial.println("SWITCH PRESSED");
    pressed = true;
    delay(50);
  }
}
```

---

## 040 — Push Button

**Component:** Momentary push button
**Pin Connections:**
| Arduino | Button |
|---------|--------|
| 12 | One side |
| 5V | Other side (via breadboard) |
| GND | (via pull-down resistor, or use INPUT_PULLUP) |

**Libraries:** None
**Notes:** Use `INPUT_PULLUP` mode to avoid needing external resistor. Button reads LOW when pressed with pull-up. Serial Plotter compatible.

```cpp
const byte          BUTTON_PIN =   12;
const unsigned long BAUD_RATE  = 9600;
const int           PLOT_MIN   =   -1;
const int           PLOT_MAX   =    2;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(BAUD_RATE);
}

void loop() {
  Serial.print("button:");
  Serial.print(digitalRead(BUTTON_PIN));
  Serial.print(" minimum:");
  Serial.print(PLOT_MIN);
  Serial.print(" maximum:");
  Serial.println(PLOT_MAX);
}
```

---

## 050 — Water Level Detector

**Component:** Water level detection sensor (HW-038)
**Pin Connections:**
| Arduino | Sensor |
|---------|--------|
| A0 | S (signal) |
| 7 | + (power) |
| GND | - |

**Libraries:** None
**Notes:** Power the sensor only during reads to prevent corrosion/degradation. Use a digital pin to toggle power.

```cpp
constexpr byte WATER_DETECTOR_PIN = A0;
constexpr byte POWER_PIN = 7;

void setup() {
  pinMode(WATER_DETECTOR_PIN, INPUT);
  pinMode(POWER_PIN, OUTPUT);
  digitalWrite(POWER_PIN, LOW);
  Serial.begin(115200);
}

void loop() {
  int waterLevel = readSensor();
  Serial.print("Water level: ");
  Serial.println(waterLevel);
  delay(1000);
}

int readSensor() {
  digitalWrite(POWER_PIN, HIGH);
  delay(10);
  int val = analogRead(WATER_DETECTOR_PIN);
  digitalWrite(POWER_PIN, LOW);
  return val;
}
```

---

## 060 — IR Receiver (KY-022)

**Component:** IR Receiver module + IR remote control
**Pin Connections:**
| Arduino | KY-022 |
|---------|--------|
| 11 | S (signal) |
| 5V | Center pin |
| GND | - |

**Libraries:** IRremote by shirriff, z3t0, ArminJo (v3.8.0+)
**Notes:** Remote uses NEC protocol. Map button hex codes by reading them first.

```cpp
#include <IRremote.hpp>

int RECV_PIN = 11;

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("Beginning IrReceiver...");
  IrReceiver.begin(RECV_PIN, ENABLE_LED_FEEDBACK);
  Serial.println("IrReceiver started...");
}

void loop() {
  if (IrReceiver.decode()) {
    Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX);
    IrReceiver.printIRResultShort(&Serial);
    IrReceiver.resume();
  }
}
```

---

## 070 — Ultrasonic Sensor (HC-SR04)

**Component:** HC-SR04 Ultrasonic Ranging Module
**Pin Connections:**
| Arduino | HC-SR04 |
|---------|---------|
| 5V | Vcc |
| GND | Gnd |
| 13 | Trig |
| 12 | Echo |

**Libraries:** None
**Notes:** Distance = (duration * 0.034) / 2 cm. Send 10us pulse on Trig, read pulse duration on Echo.

```cpp
constexpr uint8_t echoPin = 12;
constexpr uint8_t trigPin = 13;

long duration;
int distance_cm;
int distance_inch;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(115200);
  Serial.println("Ultrasonic Sensor HC-SR04 Test");
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance_cm = duration * 0.034 / 2;
  distance_inch = duration * 0.0133 / 2;
  Serial.print("Distance: ");
  Serial.print(distance_cm);
  Serial.print(" cm, ");
  Serial.print(distance_inch);
  Serial.println(" inch");
  delay(200);
}
```

---

## 080 — 1-Digit 7-Segment LED (5161AS)

**Component:** Single digit 7-segment display (common cathode)
**Pin Connections:**
| Arduino | 5161AS |
|---------|--------|
| 2 | 7 (A) |
| 3 | 6 (B) |
| 4 | 4 (C) |
| 5 | 2 (D) |
| 6 | 1 (E) |
| 7 | 9 (F) |
| 8 | 10 (G) |

**Libraries:** SevSeg by Dean Reading

```cpp
#include "SevSeg.h"
SevSeg sevseg;
int i = 0;

void setup() {
    byte numDigits = 1;
    byte digitPins[] = {};
    byte segmentPins[] = {2, 3, 4, 5, 6, 7, 8, 9};
    bool resistorsOnSegments = true;
    byte hardwareConfig = COMMON_CATHODE;
    sevseg.begin(hardwareConfig, numDigits, digitPins, segmentPins, resistorsOnSegments);
    sevseg.setBrightness(90);
}

void loop() {
    if (++i > 9) i=0;
    sevseg.setNumber(i);
    sevseg.refreshDisplay();
    delay(1000);
}
```

---

## 085 — 4-Digit 7-Segment LED

**Component:** 4-digit 7-segment display (common cathode)
**Pin Connections:**
| Arduino | Resistor | Display |
|---------|----------|---------|
| 2 | 220 ohm | D1 |
| 3 | 220 ohm | D2 |
| 4 | 220 ohm | D3 |
| 5 | 220 ohm | D4 |
| 6 | | A |
| 7 | | B |
| 8 | | C |
| 9 | | D |
| 10 | | E |
| 11 | | F |
| 12 | | G |
| 13 | | DP |

**Libraries:** SevSeg by Dean Reading

```cpp
#include "SevSeg.h"
SevSeg sevseg;

void setup() {
    byte numDigits = 4;
    byte digitPins[] = {2,3,4,5};
    byte segmentPins[] = {6, 7, 8, 9, 10, 11, 12, 13};
    sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins);
}

void loop() {
    static unsigned long timer = millis();
    static int deciSeconds = 0;
    if (millis() >= timer) {
        deciSeconds++;
        timer += 100;
        if (deciSeconds == 10000) { deciSeconds=0; }
        sevseg.setNumber(deciSeconds, 1);
    }
    sevseg.refreshDisplay();
}
```

---

## 090 — PIR Motion Sensor (HW-416-B / HC-SR501)

**Component:** PIR Motion Sensor Module
**Pin Connections:** Signal to pin 2, VCC to 5V, GND to GND
**Libraries:** None
**Notes:** ~1 minute warm-up period after power-on. Two adjustment potentiometers: sensitivity and delay time. Jumper selects single-trigger vs. repeatable-trigger mode.

```cpp
int pirPin = 2;
bool detected = false;

void setup() {
  Serial.begin(115200);
  pinMode(pirPin, INPUT);
}

int counter = 0;
void loop() {
  int pirStat = digitalRead(pirPin);
  if (pirStat == HIGH && !detected) {
    detected = true;
    counter = 0;
    Serial.println("\nMotion Detected!!!");
  }
  if (pirStat == LOW && detected) {
    detected = false;
    Serial.println("  All quiet now...");
  }
  if (detected) {
    Serial.print("status: ");
    Serial.print(pirStat);
    Serial.print(" at ");
    Serial.println(counter++);
  }
  delay(1000);
}
```

---

## 100 — 4x4 Membrane Keypad

**Component:** 4x4 membrane switch matrix keypad
**Pin Connections:**
| Arduino | Keypad |
|---------|--------|
| 2 | 8 |
| 3 | 7 |
| 4 | 6 |
| 5 | 5 |
| 6 | 4 |
| 7 | 3 |
| 8 | 2 |
| 9 | 1 |

**Libraries:** Keypad by Mark Stanley, Alexander Brevig

```cpp
#include <Keypad.h>

const byte ROWS = 4;
const byte COLS = 4;

char keys[ROWS][COLS] = {
  {'1','2','3', 'A'},
  {'4','5','6', 'B'},
  {'7','8','9', 'C'},
  {'*','0','#', 'D'}
};
byte rowPins[ROWS] = {9, 8, 7, 6};
byte colPins[COLS] = {5, 4, 3, 2};

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void setup(){
  Serial.begin(115200);
}

void loop(){
  char key = keypad.getKey();
  if (key){
    Serial.print("Key Pressed : ");
    Serial.println(key);
  }
}
```

---

## 110 — Game Joystick (KY-023)

**Component:** KY-023 Dual Axis Joystick Module
**Pin Connections:**
| Arduino | Joystick |
|---------|----------|
| 5V | 5V |
| GND | GND |
| A0 | VRx |
| A1 | VRy |
| 2 | SW |

**Libraries:** None

```cpp
#include "Arduino.h"

const int SW_pin = 2;
const int X_pin = A0;
const int Y_pin = A1;

void setup() {
  pinMode(SW_pin, INPUT);
  digitalWrite(SW_pin, HIGH);
  Serial.begin(115200);
}

void loop() {
  Serial.print("Switch:  ");
  Serial.print(digitalRead(SW_pin));
  Serial.print("\n");
  Serial.print("X-axis: ");
  Serial.print(analogRead(X_pin));
  Serial.print("\n");
  Serial.print("Y-axis: ");
  Serial.println(analogRead(Y_pin));
  Serial.print("\n\n");
  delay(500);
}
```

---

## 120 — Temperature & Humidity Sensor (KY-015 / DHT11)

**Component:** DHT11 Temperature and Humidity Sensor
**Pin Connections:**
| Arduino | DHT11 |
|---------|-------|
| 7 | S (data) |
| 5V | VCC |
| GND | - |

**Libraries:** DHT Sensor Library (Adafruit), Adafruit Unified Sensor
**Notes:** Anti-static precautions needed. Readings take ~250ms. Sensor is slow -- allow 2 seconds between reads. Connect 10K resistor from data pin to power pin.

```cpp
#include "DHT.h"

#define DHTPIN 7
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHTxx test!"));
  dht.begin();
}

void loop() {
  delay(2000);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);

  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  float hif = dht.computeHeatIndex(f, h);
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print("%  Temperature: ");
  Serial.print(t);
  Serial.print("C ");
  Serial.print(f);
  Serial.print("F  Heat index: ");
  Serial.print(hic);
  Serial.print("C ");
  Serial.print(hif);
  Serial.println("F");
}
```

---

## 130 — Sound Sensor (KY-038)

**Component:** KY-038 Sound Sensor Module
**Pin Connections:**
| Arduino | KY-038 |
|---------|--------|
| A0 | A0 |
| GND | GND |
| 5V | VCC |
| 2 | S (digital threshold) |

**Libraries:** None

```cpp
#include "Arduino.h"

void setup() {
  pinMode(2,INPUT);
  Serial.begin(115200);
}
int max = 0;
void loop() {
  int sensorDigitalValue= digitalRead(2);
  int sensorAnalogValue = analogRead(A0);
  if (sensorAnalogValue > max) max = sensorAnalogValue > 100 ? 100 : sensorAnalogValue;
  Serial.print(sensorDigitalValue);
  Serial.print(", ");
  Serial.print(sensorAnalogValue);
  Serial.print(", ");
  Serial.println(max);
  delay(1);
}
```

---

## 140 — Real Time Clock (DS3231 / ZS-042)

**Component:** DS3231 RTC Module
**Pin Connections:**
| Arduino | ZS-042 |
|---------|--------|
| 21 | SCL |
| 20 | SDA |
| 5V | VCC |
| GND | GND |

**Libraries:** DS3231 by Andrew Wickert, LibPrintf
**Notes:** I2C address 0x68 (conflicts with MPU-6050 default). CR2032 backup battery. Set time via serial input in format YYMMDDwHHMMSS.

```cpp
#include <Wire.h>
#include <DS3231.h>
#include <LibPrintf.h>

RTClib myRTC;
DS3231 setRTC;

void setup () {
    Serial.begin(115200);
    while(!Serial);
    Wire.begin();
    delay(500);
    printf("To set RTC enter time as YYMMDDwHHMMSS\n");
}

void loop () {
  if (Serial.available()) {
    String newDate = Serial.readStringUntil('\r');
    newDate.trim();
    if (newDate.length() == 13) {
      int year, month, day, dOW, hour, minute, second;
      sscanf(newDate.c_str(), "%2d%2d%2d%1d%2d%2d%2d",
             &year, &month, &day, &dOW, &hour, &minute, &second);
      if (month <= 12 && day <= 31 && hour <= 23 && minute <= 59 && second <= 59) {
        setRTC.setClockMode(false);
        setRTC.setYear(year);
        setRTC.setMonth(month);
        setRTC.setDate(day);
        setRTC.setDoW(dOW);
        setRTC.setHour(hour);
        setRTC.setMinute(minute);
        setRTC.setSecond(second);
      }
    }
  }

  DateTime now = myRTC.now();
  printf("%04d/%02d/%02d %02d:%02d:%02d\n", now.year(), now.month(),
    now.day(), now.hour(), now.minute(), now.second());
  delay(5000);
}
```

---

## 150 — RFID Reader (MFRC-522 / RC522)

**Component:** RFID-RC522 Reader + S50 Card + Keychain Tag
**Pin Connections:**
| Arduino | RFID-RC522 |
|---------|------------|
| 26 (or 8) | RST |
| 53 | SDA (SS) |
| 51 | MOSI |
| 50 | MISO |
| 52 | SCK |
| 3.3V | VCC |
| GND | GND |

**Libraries:** MFRC522-spi-i2c-uart-async
**Notes:** MUST use 3.3V power -- do NOT connect to 5V. SPI interface. Each card has a unique UID.

```cpp
#include <SPI.h>
#include <MFRC522.h>

constexpr uint8_t RST_PIN = 26;
constexpr uint8_t SS_PIN =  53;

MFRC522 mfrc522 = MFRC522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  while (!Serial);
  SPI.begin();
  mfrc522.PCD_Init();
  mfrc522.PCD_DumpVersionToSerial();
  Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));
}

void loop() {
  if ( ! mfrc522.PICC_IsNewCardPresent()) { return; }
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    Serial.println("Bad read");
    return;
  }
  if (mfrc522.uid.size == 0) {
    Serial.println("Bad card");
  } else {
    char tag[sizeof(mfrc522.uid.uidByte) * 4] = { 0 };
    for (int i = 0; i < mfrc522.uid.size; i++) {
      char buff[5];
      snprintf(buff, sizeof(buff), "%s%d", i ? "-" : "", mfrc522.uid.uidByte[i]);
      strncat(tag, buff, sizeof(tag));
    };
    Serial.println(tag);
  };
  mfrc522.PICC_HaltA();
}
```

---

## 160 — Accelerometer / Gyroscope (GY-521 / MPU-6050)

**Component:** GY-521 breakout board (MPU-6050)
**Pin Connections:**
| Arduino | GY-521 |
|---------|--------|
| 21 | SCL |
| 20 | SDA |
| 5V | VCC |
| GND | GND |

**Libraries:** Wire (built-in)
**Notes:** I2C address 0x68 (default) or 0x69 (AD0 HIGH). Conflicts with DS3231. 3-axis accelerometer + 3-axis gyroscope + temperature sensor.

```cpp
#include "Wire.h"

constexpr int MPU_ADDR = 0x68;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
}

void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 7*2, true);

  int16_t accelerometer_x = Wire.read()<<8 | Wire.read();
  int16_t accelerometer_y = Wire.read()<<8 | Wire.read();
  int16_t accelerometer_z = Wire.read()<<8 | Wire.read();
  int16_t temperature =     Wire.read()<<8 | Wire.read();
  int16_t gyro_x =          Wire.read()<<8 | Wire.read();
  int16_t gyro_y =          Wire.read()<<8 | Wire.read();
  int16_t gyro_z =          Wire.read()<<8 | Wire.read();

  Serial.print("aX = "); Serial.print(accelerometer_x);
  Serial.print(" | aY = "); Serial.print(accelerometer_y);
  Serial.print(" | aZ = "); Serial.print(accelerometer_z);
  Serial.print(" | tmp = "); Serial.print(temperature/340.00+36.53);
  Serial.print(" | gX = "); Serial.print(gyro_x);
  Serial.print(" | gY = "); Serial.print(gyro_y);
  Serial.print(" | gZ = "); Serial.print(gyro_z);
  Serial.println();
  delay(1000);
}
```

---

## 170 — Servo Motor (SG90, 180 degree sweep)

**Component:** SG90 Micro Servo Motor
**Pin Connections:**
| Arduino | SG90 |
|---------|------|
| 9 | Signal (orange/yellow) |
| 5V | VCC (red) |
| GND | GND (brown) |

**Libraries:** Servo (built-in)

```cpp
#include <Servo.h>
Servo myservo;

void setup() {
    myservo.attach(9);
}

void loop() {
    for (int i = 0; i < 180; i++) {
        myservo.write(i);
        delay(15);
    }
    for (int i = 180; i > 0; i--) {
        myservo.write(i);
        delay(15);
    }
}
```

---

## 200 — LCD Display (LCD1602, 16x2)

**Component:** LCD1602 16x2 character display
**Pin Connections:**
| Arduino | LCD1602 |
|---------|---------|
| GND | VSS |
| GND | RW |
| GND | K |
| 5V | VDD |
| 12 | RS |
| 11 | E |
| 2 | D4 |
| 3 | D5 |
| 4 | D6 |
| 5 | D7 |
| 3.3V | A (backlight) |

**Libraries:** LiquidCrystal (built-in)
**Notes:** Simplified wiring without potentiometer or resistor.

```cpp
#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 2, 3, 4, 5);

void setup() {
  lcd.begin(16, 2);
}

void loop() {
  lcd.setCursor(0, 0);
  lcd.print("0123456789ABCDEF");
  lcd.setCursor(0, 1);
  lcd.print("0123456789ABCDEF");
  delay(2000);
  for (int row = 0; row < 2; row++) {
    for (int col = 0; col < 16; col++) {
      lcd.setCursor(col, row);
      lcd.print("0");
      delay(100);
      lcd.clear();
    }
  }
}
```

---

## 210 — Stepper Motor (28BYJ-48 + ULN2003 Driver)

**Component:** 28BYJ-48 stepper motor + ULN2003 driver board
**Pin Connections:**
| Arduino | ULN2003 |
|---------|---------|
| GND | - |
| 8 | IN1 |
| 9 | IN2 |
| 10 | IN3 |
| 11 | IN4 |

External 5V supply: GND to -, 5V to + on ULN2003

**Libraries:** Stepper (built-in)
**Notes:** 2048 steps per revolution in half-step mode. Pins entered IN1-IN3-IN2-IN4 for proper step sequence.

```cpp
#include <Stepper.h>

const int stepsPerRevolution = 2038;
Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {}

void loop() {
  myStepper.setSpeed(5);
  myStepper.step(stepsPerRevolution);
  delay(1000);
  myStepper.setSpeed(10);
  myStepper.step(-stepsPerRevolution);
  delay(1000);
}
```

---

## 220 — L293D Motor Driver IC

**Component:** L293D dual H-bridge motor driver IC
**Pin Connections:** motorPin1 = 5 (Pin 14 of L293D), motorPin2 = 6 (Pin 10 of L293D)
**Libraries:** None
**Notes:** Up to 36V, 600mA per channel. Use for DC motors that draw more than GPIO can supply.

```cpp
const int motorPin1 = 5;
const int motorPin2 = 6;

void setup() {
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
}

void loop() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(motorPin1, HIGH);
    digitalWrite(motorPin2, LOW);
    delay(2000);
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, HIGH);
    delay(2000);
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, LOW);
    delay(1000);
  }
}
```

---

## 240 — Touch Screen (2.4" ILI9341 240x320 TFT LCD Shield)

**Component:** HiLetgo 2.4" ILI9341 TFT LCD Display with Touch Panel (shield)
**Pin Connections:** Shield -- plugs directly onto HERO XL headers. Match 3.3V and 5V pins.
**Libraries:** MCUFRIEND_kbv, Adafruit TouchScreen

**Notes:**
- Rotation 0-3 (0 = portrait with white button on top, proceeds clockwise)
- Touch panel requires calibration before use
- LCD and touch are separate systems with different libraries
- Four test programs provided:
  1. `1-ShowLCDRotations` -- tests LCD rotation
  2. `2-TouchScreenCalibrate` -- calibrates touch panel, outputs `constexpr` values
  3. `3-TouchSwitchWithRotation` -- on/off buttons with touch
  4. `4-GraphicsDemo` -- trig graphs, sine waves, color boxes

**Calibration output format:**
```
constexpr int XP=8,XM=A2,YP=A3,YM=9; //240x320 ID=0x9341
constexpr int TS_LEFT=109,TS_RT=914,TS_TOP=86,TS_BOT=905;
```
