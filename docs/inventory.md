# Component Inventory

> **Kit:** Adventure Kit: Pandora's Box  
> **Vendor:** inventr.io (now craftingtable.com)  
> **Purchased:** May 24, 2023 — Order #49962  
> **Kit URL:** https://craftingtable.com/products/adventure-kit-2

## Status Legend

| Symbol | Meaning |
|--------|---------|
| `[ ]` | Unused — still in bag/box |
| `[~]` | Tested — confirmed working, used in at least one sketch |
| `[x]` | In active use — currently wired into a project |
| `[!]` | Damaged or suspect — needs investigation |

---

## Boards

### HERO XL (Mega 2560 Rev3 compatible)
- **Status:** `[x]`
- **MCU:** ATmega2560 (8-bit AVR, 16 MHz)
- **Digital I/O:** 54 pins (15 PWM)
- **Analog Inputs:** 16
- **UARTs:** 4 hardware serial ports
- **Memory:** 256 KB Flash, 8 KB SRAM, 4 KB EEPROM
- **Operating Voltage:** 5V
- **Input Voltage:** 7–12V recommended (6–20V limits)
- **Pin Current:** 20 mA per I/O pin (40 mA absolute max)
- **USB:** Type-B connector
- **PlatformIO board:** `megaatmega2560`
- **Arduino IDE board:** `Arduino Mega or Mega 2560`
- **Notes:** This is the primary board for most sketches. Compatible with standard Arduino Mega shields. The HERO XL is inventr.io's branded clone of the Arduino Mega 2560 Rev3 open-source design.
- **Datasheet:** https://ww1.microchip.com/downloads/en/devicedoc/atmel-2549-8-bit-avr-microcontroller-atmega640-1280-1281-2560-2561_datasheet.pdf

### LilyGo TTGO T-Display ESP32
- **Status:** `[ ]`
- **MCU:** ESP32-D0WD-Q6 (dual-core Xtensa LX6, 240 MHz)
- **Wireless:** WiFi 802.11 b/g/n, Bluetooth 4.2 + BLE
- **Display:** 1.14" IPS TFT (ST7789V driver, 135×240 px, 64K colors)
- **Memory:** 4 MB Flash (some versions 16 MB), 520 KB SRAM
- **Operating Voltage:** 3.3V logic (5V via USB or VIN)
- **USB:** USB-C
- **Buttons:** 2 programmable (GPIO 0, GPIO 35) + 1 reset
- **Battery:** JST 1.25 connector for LiPo/LiIon, built-in charger
- **PlatformIO board:** `esp32dev`
- **Arduino IDE board:** `ESP32 Dev Module` or `LilyGo T-Display`
- **Display pins (internal SPI, not exposed):** MOSI=19, CLK=18, CS=5, DC=16, RST=23, Backlight=GPIO 4
- **Notes:** All GPIO is 3.3V. Do NOT connect 5V signals directly — use the logic level converter. Primary SPI is consumed by the display and not available for external SPI devices. The TFT_eSPI library is required for the built-in display.
- **GitHub:** https://github.com/Xinyuan-LilyGO/TTGO-T-Display

#### TTGO Available GPIO
```
Left side (top to bottom):  3V3, GND, 36, 37, 38, 39, 32, 33, 25, 26, 27, GND
Right side (top to bottom): GND, 21, 22, 17, 2, 15, 13, 12, GND, GND, 3V3, 5V
```

---

## Shields & Power

### 2.4" LCD Touchscreen Shield (320×240)
- **Status:** `[ ]`
- **Controller:** ILI9341
- **Display:** 2.4" TFT LCD, 240×320 resolution
- **Touch:** Resistive touch panel
- **Interface:** Plugs directly onto HERO XL headers
- **Libraries:** `MCUFRIEND_kbv`, `Adafruit TouchScreen`
- **Rotations:** 0–3 (0 = portrait with white button on top, clockwise)
- **Notes:** Designed to stack on top of any Mega-compatible board. Useful for interactive UI projects — menus, dashboards, simple games. Requires touch calibration before use — run calibration sketch to obtain constexpr values for your specific panel.

### HERO XL Prototype Shield + 170-point Mini Breadboard
- **Status:** `[ ]`
- **Notes:** Plugs onto top of the HERO XL (Mega 2560) board for compact prototyping. The mini breadboard sits on top of the shield.

### Breadboard Power Supply Module
- **Status:** `[ ]`
- **Output:** 3.3V and 5V selectable per rail
- **Input:** 6.5–12V DC barrel jack or USB
- **Notes:** Plugs directly into the 830-point breadboard power rails. Useful when you need isolated power for motor/sensor circuits separate from the board's USB power.

---

## Displays

### LCD1602 (16×2 Character Display, Blue Backlight)
- **Status:** `[ ]`
- **Display:** 16 characters × 2 lines
- **Interface:** Parallel (requires 6+ pins) or I2C if backpack is soldered
- **Operating Voltage:** 5V
- **Library:** `LiquidCrystal` (parallel) or `LiquidCrystal_I2C`
- **Parallel pin mapping:** RS=12, E=11, D4=2, D5=3, D6=4, D7=5 (simplified 4-bit wiring without contrast potentiometer)
- **Notes:** Classic character display for showing text, readings, status messages. Can use 3.3V pin for backlight anode — dimmer but works without a current-limiting resistor.

### 1-Digit 7-Segment Display (5161AS)
- **Status:** `[ ]`
- **Type:** Common cathode
- **Pin mapping:** 7 segment pins (A–G) — no decimal point in basic wiring
- **Library:** `SevSeg` by Dean Reading
- **Notes:** Good for learning multiplexing and segment control basics.

### 4-Digit 7-Segment Display (5641AS)
- **Status:** `[ ]`
- **Type:** Common cathode (red)
- **Pin count:** 12 pins (4 digit commons + 8 segment lines)
- **Resistance:** At least 800Ω on each segment pin
- **Library:** `SevSeg` by Dean Reading
- **Datasheet:** http://www.xlitx.com/datasheet/5641AS.pdf
- **Notes:** Ideal for clocks, counters, timers. Multiplexed — only one digit is lit at a time, cycled rapidly by the library.

---

## Sensors

### HC-SR501 PIR Motion Sensor
- **Status:** `[ ]`
- **Detection Range:** Up to 7 meters, 120° cone
- **Output:** Digital HIGH/LOW
- **Operating Voltage:** 5V–20V (3.3V logic output)
- **Adjustments:** Sensitivity potentiometer, delay potentiometer
- **Notes:** Has a ~1 minute warm-up period after power-on. Jumper selects single-trigger vs. repeatable-trigger mode.

### HC-SR04 Ultrasonic Distance Sensor
- **Status:** `[ ]`
- **Range:** 2 cm – 400 cm
- **Pins:** VCC, Trig, Echo, GND
- **Operating Voltage:** 5V
- **Library:** `NewPing` or manual `pulseIn()`
- **Notes:** Trig pin sends 10μs pulse, Echo pin returns HIGH for duration proportional to distance. Distance (cm) = duration × 0.034 / 2. Distance (inches) = duration × 0.0133 / 2.

### KY-037 / KY-038 Sound Sensor Module
- **Status:** `[ ]`
- **Output:** Digital (threshold via potentiometer) + Analog
- **Operating Voltage:** 5V
- **Notes:** Has both digital out (D0) for threshold detection and analog out (A0) for raw sound level readings. Sensitivity is adjustable via onboard potentiometer. The KY-037 and KY-038 variants have the same interface — either can be used interchangeably.

### Rain/Water Level Detection Sensor (HW-038)
- **Status:** `[ ]`
- **Output:** Analog (varies with water contact area)
- **Operating Voltage:** 3.3V–5V
- **Sensing traces:** 10 exposed copper traces (5 power, 5 sense)
- **Notes:** The sensor board and the control board are separate — connect with included cable. Analog reading increases with more water on the sensing pad. Best practice: power the sensor only during reads (use a digital pin for VCC) to prevent corrosion and degradation of the sensing traces.

### MPU-6050 Accelerometer/Gyroscope (GY-521 Module)
- **Status:** `[ ]`
- **Axes:** 3-axis accelerometer + 3-axis gyroscope
- **Interface:** I2C (SDA, SCL)
- **Operating Voltage:** 3.3V–5V (onboard regulator)
- **I2C Address:** 0x68 (default) or 0x69 (AD0 pin HIGH)
- **Library:** `MPU6050` by Electronic Cats, or `Adafruit_MPU6050`
- **Notes:** Requires soldering header pins. Capable of detecting tilt, orientation, motion, and vibration.

### DHT11 Temperature & Humidity Sensor (KY-015)
- **Status:** `[ ]`
- **Interface:** Single-wire digital (data pin)
- **Operating Voltage:** 3.3V–5V
- **Accuracy:** ±2°C temperature, ±5% humidity
- **Library:** `DHT Sensor Library` by Adafruit + `Adafruit Unified Sensor`
- **Notes:** Readings take ~250ms. Allow 2 seconds between reads. Connect 10KΩ pull-up resistor from data pin to VCC. Anti-static precautions recommended.

### Photoresistor (LDR / Light Dependent Resistor)
- **Status:** `[~]`
- **Interface:** Analog (voltage divider with 10KΩ pull-down)
- **Notes:** Included in the Circuits Essentials Kit. Pair with a 10KΩ pull-down resistor to form a voltage divider. Connect one lead to 5V, other lead to analog pin AND through 10KΩ to GND. `analogRead()` returns 0–1023 based on light intensity.

---

## Input Devices

### KY-040 Rotary Encoder
- **Status:** `[ ]`
- **Outputs:** CLK, DT (quadrature), SW (push button)
- **Operating Voltage:** 5V
- **Library:** `BasicEncoder`
- **Notes:** Not a potentiometer — it outputs pulses for rotation direction and clicks. Requires debouncing in software or hardware. Good for menu navigation and value adjustment. Uses interrupts — connect CLK and DT to interrupt-capable pins (2, 3, 18 on Mega). SW requires `INPUT_PULLUP`.

### KY-023 Joystick Module
- **Status:** `[ ]`
- **Interface:** 2× analog (X, Y axes) + 1 digital (button)
- **Operating Voltage:** 5V
- **Pins:** VRx (analog), VRy (analog), SW (digital button)
- **Notes:** Each axis outputs 0–1023 via `analogRead()`. Center position reads ~512. Button is active LOW — use `INPUT_PULLUP`.

### 4×4 Membrane Keypad
- **Status:** `[ ]`
- **Keys:** 16 keys (0-9, A-D, *, #)
- **Interface:** 8 pins (4 rows + 4 columns), matrix scanning
- **Library:** `Keypad` by Mark Stanley and Alexander Brevig
- **Notes:** Thin and flexible. Connects via 8-pin ribbon header. Uses matrix scanning so only 8 pins are needed for 16 keys.

### IR Remote Control + Receiver
- **Status:** `[ ]`
- **Remote:** Standard NEC protocol remote (black, 21 buttons)
- **Receiver:** 38 KHz IR receiver module (3 pins: OUT, GND, VCC)
- **Operating Voltage:** 5V
- **Library:** `IRremote`
- **Notes:** Each button sends a unique hex code. You'll need to map the codes by reading them with the receiver first.

### RFID Reader (MFRC-522 RC522) + S50 Card + Keychain Tag
- **Status:** `[ ]`
- **Frequency:** 13.56 MHz
- **Interface:** SPI
- **Operating Voltage:** 3.3V (do NOT connect to 5V)
- **Library:** `MFRC522` by miguelbalboa (or `MFRC522-spi-i2c-uart-async`)
- **SPI Pins on Mega:** SS=53, SCK=52, MOSI=51, MISO=50
- **RST Pin:** Configurable — commonly pin 26 or pin 8
- **Notes:** Reads and writes to MIFARE Classic 1K cards/tags. Each card has a unique UID. Requires 3.3V power — the HERO XL has a 3.3V output pin. The RST and SDA (SS) pins are configurable.

---

## Output Devices

### Servo SG90 (Micro Servo, 180°)
- **Status:** `[ ]`
- **Rotation:** 0°–180°
- **Operating Voltage:** 4.8V–6V
- **Signal:** PWM
- **Library:** `Servo` (built-in)
- **Datasheet:** http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf
- **Notes:** Three wires — brown (GND), red (VCC), orange (signal/PWM). Can be powered from the board's 5V pin for light loads. For multiple servos, use external power.

### 28BYJ-48 Stepper Motor + ULN2003 Driver Board
- **Status:** `[ ]`
- **Type:** Unipolar, 4-phase
- **Step Angle:** 5.625°/64 (gear ratio), so 2048 steps per full revolution in half-step mode
- **Steps per revolution:** 2038 (full step mode, per course calibration)
- **Operating Voltage:** 5V
- **Library:** `Stepper` (built-in) or `AccelStepper`
- **ULN2003 pin order:** IN1–IN3–IN2–IN4 (not sequential — required for proper step sequence)
- **Notes:** The ULN2003 driver connects between the board and the motor. 4 digital pins → driver board IN1–IN4. The motor is slow but precise — good for positioning, not speed.

### DC Motor + 3-Leaf Fan Blade
- **Status:** `[ ]`
- **Operating Voltage:** 3V–6V
- **Notes:** Cannot be driven directly from a GPIO pin — use a transistor (NPN like 2N2222) or the relay module. The fan blade press-fits onto the motor shaft.

### Active Buzzer
- **Status:** `[ ]`
- **Operating Voltage:** 5V
- **Variants:** KY-012 (2-pin bare component), HW-512 (3-pin PCB module — third pin not connected)
- **Identification:** Sealed/closed bottom. Makes a continuous tone when tested with a 9V battery.
- **Notes:** Produces a fixed-frequency tone when powered. Just apply voltage — no `tone()` function needed. Has a built-in oscillator. Usually has a white sticker or `+` marking on top.

### Passive Buzzer (KY-006)
- **Status:** `[ ]`
- **Operating Voltage:** 3.3V–5V
- **Variants:** KY-006 (bare component), HW-508 (3-pin PCB module)
- **Identification:** Open bottom / exposed circuit board. Makes a clicking sound when tested with a 9V battery.
- **Library:** `tone()` (built-in)
- **Notes:** Requires a PWM signal to produce sound. You control the frequency, so you can play melodies. No built-in oscillator — silent unless driven.

### Relay Module (5V, Single Channel)
- **Status:** `[ ]`
- **Trigger:** Active LOW or Active HIGH (check your module)
- **Switching:** Up to 10A @ 250VAC or 10A @ 30VDC (rated)
- **Notes:** Used to switch higher-power devices (lamps, fans, motors) using a low-power signal from the board. Has indicator LED and opto-isolation on some models. Listen for the click — if it clicks, it's switching.

### RGB LED (Common Cathode)
- **Status:** `[ ]`
- **Pins:** 4 pins — Red, Common GND (longest leg), Green, Blue
- **Notes:** Requires 220Ω resistor on each color pin. Use `analogWrite()` for PWM color mixing (0–255 per channel). Common cathode type — longest pin goes to GND.

### L293D Motor Driver IC
- **Status:** `[ ]`
- **Type:** Dual H-bridge motor driver IC
- **Max Voltage:** 36V
- **Max Current:** 600mA per channel
- **Notes:** Used for DC motors that draw more than GPIO can supply. Alternative to using a relay or transistor driver. Supports bidirectional motor control and speed control via PWM enable pins.

---

## Communication & Timing

### HC-06 Bluetooth Module (4-pin)
- **Status:** `[ ]`
- **Bluetooth:** Classic Bluetooth 2.0 SPP (Serial Port Profile)
- **Interface:** UART (TX, RX) at 9600 baud default
- **Operating Voltage:** 3.3V–6V input, but RX pin is 3.3V logic
- **Notes:** Pairs with a phone or computer as a serial Bluetooth device. Default name is usually "HC-06", default PIN is "1234". The RX pin needs a voltage divider or the logic level converter when connected to a 5V board's TX pin.

### DS3231 Real-Time Clock Module (ZS-042, AT24C32 EEPROM)
- **Status:** `[ ]`
- **Module model:** ZS-042
- **Interface:** I2C (SDA, SCL)
- **Accuracy:** ±2 ppm (very accurate — drifts ~1 minute per year)
- **Battery:** CR2032 coin cell backup (maintains time when unpowered)
- **EEPROM:** 32 Kbit (4 KB) AT24C32 onboard for data logging
- **I2C Address:** 0x68 (RTC), 0x57 (EEPROM)
- **Library:** `RTClib` by Adafruit, or `DS3231` by Andrew Wickert (+ `LibPrintf` for formatted output)
- **Notes:** Shares I2C address 0x68 with the MPU-6050 — do not use both on the same I2C bus without changing the MPU-6050's address (set AD0 pin HIGH to switch it to 0x69). Also includes a temperature sensor (±3°C accuracy).

### IIC/I2C Logic Level Converter (Bi-Directional, 5V ↔ 3.3V)
- **Status:** `[ ]`
- **Channels:** Typically 4 bidirectional channels
- **Notes:** Essential for connecting 3.3V devices (ESP32, RFID reader, Bluetooth RX) to 5V boards. HV side connects to 5V, LV side to 3.3V. Each channel converts one signal line.

---

## Fundamentals & Passive Components

### 830-Point Breadboard
- **Status:** `[x]`
- **Notes:** Full-size solderless breadboard. Two power rail strips on each side, 63 rows of 5-hole terminal strips. Center channel separates the two halves.

### 400-Point Solderless Breadboard
- **Status:** `[ ]`
- **Notes:** Half-size breadboard. Good for smaller sub-circuits or use alongside the 830-point board.

### Jumper Wire Kit (65× Breadboard Jumpers)
- **Status:** `[~]`
- **Notes:** Pre-cut, rigid jumper wires in assorted lengths. Color-coded. Used for breadboard connections.

### 20-Pin Male-to-Female Jumper Wires
- **Status:** `[ ]`
- **Notes:** Flexible Dupont wires. Used for connecting modules (sensors, displays) to the board or breadboard.

### USB A-B Cable
- **Status:** `[~]`
- **Notes:** Connects HERO XL to computer for power and programming.

### USB-C Cable
- **Status:** `[ ]`
- **Notes:** Connects TTGO T-Display ESP32 to computer for power and programming.

### 9V Battery Connector
- **Status:** `[ ]`
- **Notes:** Snap connector with barrel plug. Powers the HERO XL via the DC jack for portable/untethered operation.

### Resistor Kit (Assorted Values)
- **Status:** `[~]`
- **Typical values included:** 220Ω, 330Ω, 1KΩ, 4.7KΩ, 10KΩ, 100KΩ
- **Notes:** Used for current limiting (LEDs), pull-up/pull-down resistors, and voltage dividers. Color bands indicate value — use a multimeter if unsure.

### Circuits Essentials Kit
- **Status:** `[~]`
- **Typically includes:** Assorted LEDs (red, green, yellow, blue), push buttons with colored caps, photoresistors (LDRs), and possibly additional passive components
- **Notes:** This is the grab bag of small parts. Inventory yours and update this section with exact quantities.

### Storage Crate
- **Notes:** The box everything ships in. Doubles as parts organization.

---

## I2C Address Map

Multiple components share the I2C bus. Keep track of addresses to avoid conflicts.

| Address | Device | Notes |
|---------|--------|-------|
| 0x27 or 0x3F | LCD1602 (with I2C backpack) | Common addresses — scan to confirm |
| 0x57 | AT24C32 EEPROM (on DS3231 module) | |
| 0x68 | DS3231 RTC | Conflicts with MPU-6050 default |
| 0x68 | MPU-6050 (default) | Set AD0 HIGH → 0x69 to avoid conflict with DS3231 |

Use the I2C scanner sketch to detect all connected devices:
```cpp
#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
  Serial.println("I2C Scanner");
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.print("Found device at 0x");
      Serial.println(addr, HEX);
    }
  }
}

void loop() {}
```

---

## SPI Pin Reference

| Pin Function | HERO XL (Mega) | ESP32 (TTGO) |
|-------------|----------------|---------------|
| SCK | 52 | 18 (used by display) |
| MOSI | 51 | 19 (used by display) |
| MISO | 50 | N/A (not exposed) |
| SS (default) | 53 | 5 (used by display) |

**Note:** The TTGO T-Display's primary SPI bus is consumed by the built-in screen. External SPI devices (like the RFID reader) should be used with the HERO XL.

---

## Useful Links

- **Kit product page:** https://craftingtable.com/products/adventure-kit-2
- **HERO XL product page:** https://craftingtable.com/products/hero-xl-board-2560-rev3-usb-cable
- **TTGO T-Display GitHub:** https://github.com/Xinyuan-LilyGO/TTGO-T-Display
- **Arduino language reference:** https://www.arduino.cc/reference/en/
- **PlatformIO docs:** https://docs.platformio.org/en/latest/
- **ATmega2560 datasheet:** https://ww1.microchip.com/downloads/en/devicedoc/atmel-2549-8-bit-avr-microcontroller-atmega640-1280-1281-2560-2561_datasheet.pdf
- **ESP32 technical reference:** https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf
- **TFT_eSPI library:** https://github.com/Bodmer/TFT_eSPI

---

## Library Reference

| Library | Component | Install via |
|---------|-----------|-------------|
| SevSeg | 7-segment displays | PlatformIO: `dean/SevSeg` |
| BasicEncoder | Rotary encoder | PlatformIO: `BasicEncoder` |
| IRremote | IR receiver/remote | PlatformIO: `z3t0/IRremote` (v3.8.0+) |
| DHT Sensor Library | DHT11/DHT22 | PlatformIO: `adafruit/DHT sensor library` |
| Adafruit Unified Sensor | (required by DHT) | PlatformIO: `adafruit/Adafruit Unified Sensor` |
| DS3231 | Real-time clock | PlatformIO: `andrew-wickert/DS3231` |
| MFRC522 | RFID reader | PlatformIO: `miguelbalboa/MFRC522` |
| Keypad | 4×4 membrane keypad | PlatformIO: `chris--a/Keypad` |
| MCUFRIEND_kbv | LCD touchscreen shield | PlatformIO: `prenticedavid/MCUFRIEND_kbv` |
| Adafruit TouchScreen | Touch panel | PlatformIO: `adafruit/Adafruit TouchScreen` |
| TFT_eSPI | TTGO T-Display screen | PlatformIO: `bodmer/TFT_eSPI` |
| LiquidCrystal | LCD1602 (parallel) | Built-in |
| Servo | SG90 servo motor | Built-in |
| Stepper | 28BYJ-48 stepper | Built-in |
| Wire | I2C communication | Built-in |
