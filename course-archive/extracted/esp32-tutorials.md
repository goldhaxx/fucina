# ESP32 TTGO T-Display Tutorials

Extracted from `Getting_Started/ESP32_TTGO_T-Display/`.

---

## Board Overview

The LilyGo TTGO T-Display ESP32 is a compact IoT development board with:
- ESP32 microcontroller (240MHz dual-core Xtensa LX6)
- Built-in 1.14" IPS TFT display (135x240 px, ST7789V driver)
- WiFi 802.11 b/g/n + Bluetooth 4.2/BLE
- USB-C for power and programming
- JST 1.25 battery connector with built-in charger
- 2 programmable buttons (GPIO 0, GPIO 35)
- 4MB Flash, 520KB SRAM

### Specifications

| Spec | Value |
|------|-------|
| Working voltage | 2.7V-4.2V |
| Working current | ~67mA |
| Sleep current | ~350uA |
| Size | 51.49mm x 25.09mm (7.81g) |
| WiFi range | ~300m |
| WiFi transmit power | 22dBm |
| Display resolution | 135x240 pixels |

### Arduino IDE Setup

1. Add ESP32 board manager URL: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
2. Install "esp32 by Espressif Systems" from Boards Manager
3. Select "ESP32 Dev Module" as the board
4. Connect via USB-C, select correct port

### Important Pin Notes

- **All GPIO is 3.3V** -- do NOT connect 5V signals without logic level converter
- Pins 36-39 are INPUT ONLY (no internal pull-up/pull-down)
- Pins 21-22 are for I2C -- avoid for general use
- Display consumes SPI pins 18, 19, 5, 16, 23, and GPIO 4 (backlight)

---

## 002 — Light Emitting Diode (ESP32 version)

**Pin:** GPIO 32
**Wiring:**
| ESP32 | LED |
|-------|-----|
| GND | 220 ohm resistor then negative (shorter) lead |
| 32 | Positive (longer) LED lead |

**Notes:** Uses GPIO 32 instead of pin 2 (HERO XL). Avoids pins 36-39 (input only) and 21-22 (I2C).

```cpp
#include <Arduino.h>

const int Light = 32;

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

## 004 — RGB Light Emitting Diode (ESP32 version)

**Pins:** redPin=13, greenPin=15, bluePin=2
**Wiring:**
| ESP32 | LED |
|-------|-----|
| 13 | RED lead |
| GND | Common pin (longest) |
| 15 | GREEN lead |
| 2 | BLUE lead |

```cpp
#import <Arduino.h>

constexpr int redPin   = 13;
constexpr int greenPin = 15;
constexpr int bluePin  = 2;

void setup() {
  pinMode(redPin,   OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin,  OUTPUT);
}

void loop() {
  setColor(255, 0, 0); // Red
  delay(1000);
  setColor(0, 255, 0); // Green
  delay(1000);
  setColor(0, 0, 255); // Blue
  delay(1000);
  setColor(255, 255, 255); // White
  delay(1000);
  setColor(170, 0, 255); // Purple
  delay(1000);
}

void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(redPin,   redValue);
  analogWrite(greenPin, greenValue);
  analogWrite(bluePin,  blueValue);
}
```

---

## TTGO Simple Test (Button + Display Test)

**Libraries:** TFT_eSPI (must configure for Setup25_TTGO_T_Display)
**Buttons:** GPIO 0 (bottom/left), GPIO 35 (top/right) -- both INPUT_PULLUP, active LOW
**Board setting:** ESP32 Dev Module

**Important:** Edit `libraries/TFT_eSPI/User_Setup_Select.h` and uncomment the `#include` for `Setup25_TTGO_T_Display.h`.

If upload errors occur, try lowering the upload speed in Tools > Upload Speed.

```cpp
#include <TFT_eSPI.h>
#if USER_SETUP_ID != 25
#error "This sketch is for TFT_eSPI config 25 (TTGO_T_Display)."
#error "Edit libraries/TFT_eSPI/User_Setup_Select.h"
#endif

TFT_eSPI tft = TFT_eSPI(135, 240);

void setup() {
  tft.init();
  tft.fillScreen(TFT_BLUE);
  tft.setCursor(3, 2);
  tft.setTextColor(TFT_GREEN, TFT_BLUE);
  tft.setTextSize(2);
  tft.println("Button Test");
  tft.println("   Push a");
  tft.println("   button");
  tft.println("  to Start");
  Serial.begin(9600);
  pinMode(0, INPUT_PULLUP);
  pinMode(35, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(0) == 0) {
    Serial.println("Button 2 Pressed");
    delay(500);
    tft.setCursor(3, 2);
    tft.fillScreen(TFT_RED);
    tft.setTextColor(TFT_GREEN, TFT_RED);
    tft.setTextSize(3);
    tft.println("Left");
    tft.println("button");
    tft.println("pressed");
  }
  if (digitalRead(35) == 0) {
    Serial.println("Button 1 Pressed");
    delay(500);
    tft.setCursor(3, 2);
    tft.fillScreen(TFT_GREEN);
    tft.setTextColor(TFT_BLACK, TFT_GREEN);
    tft.setTextSize(3);
    tft.println("Right");
    tft.println("button");
    tft.println("pressed");
  }
}
```

---

## Sample Sketches (Display Demos)

### Mandelbrot
Renders Mandelbrot fractal on the built-in display.

### Matrix
Matrix-style falling text animation.

### Starfield
Star field simulation on the display.

---

## Volos Projects (Games and Utilities)

Originally from Volos Projects YouTube channel, adapted by David Schmidt.

| Project | Description |
|---------|-------------|
| Resistor | Decode resistor color codes on display |
| EspGauge | Semicircular 0-100% rotating gauge |
| Color Picker | Adjust RGB values with external potentiometers |
| Car Dodge Game | Dodge oncoming cars |
| Tetris | Two-button classic Tetris (reportedly works well) |
| Alien Attack | Space Invaders-style game |
| Internet Weather | Local weather/time from internet API |
| Breakout | Classic Breakout game |
| T-Rex | Chrome dinosaur jump game |
| Space Wars | Space combat game |
| HowAndWhenToUseSprites | Tutorial on TFT sprite usage |
| RotateSpritesTutorial | Tutorial on rotating sprites |
