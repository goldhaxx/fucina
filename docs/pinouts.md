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
  + rail (red)   ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
  - rail (blue)  ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●

  a  ● ● ● ● ● | ● ● ● ● ●     Rows 1-63
  b  ● ● ● ● ● | ● ● ● ● ●     5 holes per side, connected horizontally
  c  ● ● ● ● ● | ● ● ● ● ●     Center channel breaks the connection
  d  ● ● ● ● ● | ● ● ● ● ●
  e  ● ● ● ● ● | ● ● ● ● ●
     - - - - - GAP - - - - -
  f  ● ● ● ● ● | ● ● ● ● ●
  g  ● ● ● ● ● | ● ● ● ● ●
  h  ● ● ● ● ● | ● ● ● ● ●
  i  ● ● ● ● ● | ● ● ● ● ●
  j  ● ● ● ● ● | ● ● ● ● ●

  + rail (red)   ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
  - rail (blue)  ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
```

Power rails run the full length of the board. Some 830-point boards have a split in the middle of each rail — bridge with a jumper wire if continuity is needed across the full length.
