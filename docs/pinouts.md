# Pinout Reference

## HERO XL (Mega 2560)

| Function | Pins | Notes |
|----------|------|-------|
| Digital I/O | D0–D53 | 54 total, all 5V logic |
| PWM | D2–D13, D44–D46 | 15 pins, 8-bit resolution |
| Analog In | A0–A15 | 16 channels, 10-bit ADC |
| UART 0 (USB) | TX0=1, RX0=0 | Connected to USB-serial chip |
| UART 1 | TX1=18, RX1=19 | |
| UART 2 | TX2=16, RX2=17 | |
| UART 3 | TX3=14, RX3=15 | |
| I2C | SDA=20, SCL=21 | Shared bus — check address conflicts |
| SPI | MOSI=51, MISO=50, SCK=52, SS=53 | SS must be OUTPUT even if unused |
| Built-in LED | D13 | Shared with SCK — avoid SPI conflicts |
| External Interrupts | D2(INT0), D3(INT1), D18(INT5), D19(INT4), D20(INT3), D21(INT2) | |
| Power Out | 5V, 3.3V, GND | 3.3V pin max ~50 mA |

**USB:** Type-B  
**Power Jack:** 2.1 mm barrel, 7–12V recommended  
**Pin Current:** 20 mA per pin (40 mA absolute max)

---

## TTGO T-Display ESP32

**All GPIO is 3.3V. Do not connect 5V signals without the logic level converter.**

| Function | Pins | Notes |
|----------|------|-------|
| Safe GPIO | 21, 22, 17, 2, 15, 13, 12, 25, 26, 27, 32, 33 | General purpose, no boot conflicts |
| Input Only | 36, 37, 38, 39 | No internal pull-up/pull-down |
| ADC | Most GPIO pins | 12-bit, 0–3.3V range, noisy — use averaging |
| I2C (default) | SDA=21, SCL=22 | |
| Buttons | GPIO 0 (bottom), GPIO 35 (top) | Active LOW, built into the board |
| Display Backlight | GPIO 4 | PWM dimmable |
| Battery Voltage | GPIO 34 | Requires 12dB attenuation setting |

### Pins consumed by built-in display (not available for use)
| Function | Pin |
|----------|-----|
| SPI MOSI | 19 |
| SPI CLK | 18 |
| SPI CS | 5 |
| DC | 16 |
| RST | 23 |
| Backlight | 4 |

### Physical pin layout
```
         +-------------+
         | T T G O     |
    G    | +---------+  |
   3V  G | |         |  |
   36 21 | |  D I S  |  |
   37 22 | |  P L A  |  |
   38 17 | |  Y     |  |
   39  2 | |         |  |
   32 15 | |         |  |
   33 13 | |         |  |
   25 12 | |         |  |
   26  G | |         |  |
   27  G | |         |  |
    G 3V | |         |  |
   5V    | +---------+  |
         +-------------+
```

**USB:** USB-C  
**Battery:** JST 1.25 connector (LiPo/LiIon, built-in charger)

---

## Breadboard Layout (830-point)

```
      + -  a b c d e     f g h i j  + -

 1         ● ● ● ● ●     ● ● ● ● ●
 2         ● ● ● ● ●     ● ● ● ● ●
 3    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  ┐
 4    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  │
 5    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  │ group 1
 6    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  │
 7    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  ┘
 8         ● ● ● ● ●     ● ● ● ● ●
 9    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  ┐
10    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  │
11    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  │ group 2
12    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  │
13    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  ┘
14         ● ● ● ● ●     ● ● ● ● ●
           ·  ·  ·  ·     ·  ·  ·  ·          ...groups 3–9
57    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  ┐
58    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  │
59    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  │ group 10
60    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  │
61    ● ●  ● ● ● ● ●     ● ● ● ● ●  ● ●  ┘
62         ● ● ● ● ●     ● ● ● ● ●
63         ● ● ● ● ●     ● ● ● ● ●
```

**Terminal strips:** 63 rows × 10 columns. Left bank (a–e) and right bank (f–j) are each connected horizontally per row. The center channel breaks the connection between banks.

**Power rails:** + (red) and − (blue) on both left and right edges. Rail holes appear in 10 groups of 5, aligned to terminal rows 3–7, 9–13, 15–19, 21–25, 27–31, 33–37, 39–43, 45–49, 51–55, 57–61. Each rail is a continuous conductor internally. Some boards split at the midpoint — bridge with a jumper wire if continuity is needed across the full length.

---

## LCD Touchscreen Shield Pin Consumption

The 2.4" ILI9341 LCD Touchscreen Shield plugs directly onto the HERO XL headers and consumes many pins.

| Function | Pins | Notes |
|----------|------|-------|
| LCD Data | D2–D9 | 8-bit parallel data bus |
| LCD Control | A0 (RS), A1 (CS), A2 (RD), A3 (WR), A4 (RST) | |
| Touch Panel | D8 (XP), A2 (XM), A3 (YP), D9 (YM) | Shares with LCD — multiplex |
| SD Card | D10 (CS), D11 (MOSI), D12 (MISO), D13 (SCK) | Optional, uses SPI |

**Available pins when shield is mounted:** D22-D53, A5-A15, and SDA/SCL (20/21). Serial pins (0/1) remain available for USB communication.

**Libraries:** `MCUFRIEND_kbv` for LCD, `Adafruit TouchScreen` for touch input.

**Calibration:** Run calibration sketch to obtain touch coordinate mapping constants:
```
constexpr int XP=8, XM=A2, YP=A3, YM=9;
constexpr int TS_LEFT=109, TS_RT=914, TS_TOP=86, TS_BOT=905;
```

---

## Common Multi-Component Pin Allocations

These are tested pin assignments from Crafting Table course projects that avoid conflicts.

### Basic I/O Project (LEDs + Button + Buzzer + Potentiometer)
| Component | Pin(s) | Notes |
|-----------|--------|-------|
| LED (red) | D2 | With 220Ω resistor |
| LED (green) | D3 | PWM capable |
| Button | D12 | INPUT_PULLUP, no external resistor |
| Active Buzzer | D4 | digitalWrite only |
| Passive Buzzer | D5 | PWM for tone() |
| Potentiometer | A0 | analogRead 0-1023 |

### Sensor Array (PIR + Ultrasonic + Sound + Water)
| Component | Pin(s) | Notes |
|-----------|--------|-------|
| PIR Motion | D2 | Digital HIGH/LOW |
| Ultrasonic Trig | D13 | 10μs pulse output |
| Ultrasonic Echo | D12 | pulseIn() input |
| Sound Sensor (digital) | D3 | Threshold trigger |
| Sound Sensor (analog) | A0 | Raw audio level |
| Water Level (signal) | A1 | Analog 0-1023 |
| Water Level (power) | D7 | Gate power to prevent corrosion |

### Security System (Keypad + RFID + Servo + LCD)
| Component | Pin(s) | Notes |
|-----------|--------|-------|
| 4x4 Keypad | D2-D9 | 4 rows + 4 columns |
| Servo | D10 | PWM signal |
| RFID SS | D53 | SPI chip select |
| RFID RST | D26 | Configurable |
| RFID SPI | D50-D52 | MISO, MOSI, SCK (hardware SPI) |
| LCD RS | D12 | |
| LCD E | D11 | |
| LCD D4-D7 | D22-D25 | Shifted to avoid keypad conflict |

### I2C Bus Devices (RTC + Gyroscope)
| Component | Pin(s) | I2C Address |
|-----------|--------|-------------|
| DS3231 RTC | SDA=20, SCL=21 | 0x68 |
| MPU-6050 Gyroscope | SDA=20, SCL=21 | 0x69 (AD0 HIGH) |

**Note:** Both share the same I2C bus but use different addresses. Set MPU-6050 AD0 pin HIGH to shift from default 0x68 to 0x69.

### Rotary Encoder (Interrupt Pins Required)
| Component | Pin(s) | Notes |
|-----------|--------|-------|
| CLK | D2 (INT0) | Must be interrupt-capable |
| DT | D3 (INT1) | Must be interrupt-capable |
| SW (button) | D18 (INT5) | INPUT_PULLUP, optional interrupt |

---

## TTGO T-Display ESP32 — Safe Pin Quick Reference

Pins are listed in order of "safest to use first" for general projects.

| Priority | GPIO | Type | Notes |
|----------|------|------|-------|
| 1st | 32, 33 | I/O + ADC | No boot conflicts, fully general purpose |
| 2nd | 25, 26, 27 | I/O + ADC | Safe for most uses |
| 3rd | 13, 15, 2 | I/O | Work fine but may affect boot if pulled LOW |
| 4th | 12 | I/O | Must be LOW during boot (MTDI strapping pin) |
| 5th | 17 | I/O | TX2 — safe if not using UART2 |
| Input only | 36, 37, 38, 39 | Input | No pull-up/pull-down, ADC only |
| Reserved | 21, 22 | I2C | Default SDA/SCL — use for I2C only |
| Consumed | 4, 5, 16, 18, 19, 23 | Display | Used by built-in TFT — do not use |
| Buttons | 0, 35 | Input | Built-in buttons, active LOW |
