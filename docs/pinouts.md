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
