# LCD1602 — Character Display

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 200

Displays text on a 16x2 character LCD using the built-in `LiquidCrystal` library. Shows a full-screen test pattern, then a scanning cursor demo.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-lcd1602/wiring.yaml -o sketches/craftingtable/ct-lcd1602/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x LCD1602 display (the blue 16x2 character display with 16 header pins)
- 9x jumper wires

## Step-by-Step Wiring

This uses 4-bit parallel mode (saves pins). No contrast potentiometer — connect V0 to GND for maximum contrast.

### LCD pin connections

| LCD Pin | Name | Connect to |
|---------|------|------------|
| 1 (VSS) | GND | HERO XL GND |
| 2 (VDD) | +5V | HERO XL 5V |
| 3 (V0) | Contrast | GND (max contrast) |
| 4 (RS) | Register Select | HERO XL Pin 12 |
| 5 (RW) | Read/Write | GND (write-only) |
| 6 (E) | Enable | HERO XL Pin 11 |
| 7-10 | D0-D3 | Not connected (4-bit mode) |
| 11 (D4) | Data 4 | HERO XL Pin 2 |
| 12 (D5) | Data 5 | HERO XL Pin 3 |
| 13 (D6) | Data 6 | HERO XL Pin 4 |
| 14 (D7) | Data 7 | HERO XL Pin 5 |
| 15 (A) | Backlight + | HERO XL 3.3V (dimmer but safe without resistor) |
| 16 (K) | Backlight - | GND |

## Build and Upload

```bash
cd sketches/craftingtable/ct-lcd1602
pio run -e mega -t upload
```

The display shows "0123456789ABCDEF" on both lines for 2 seconds, then a scanning "0" cursor moves across the display.

## What to Try Next

- Display sensor readings (temperature, distance, light level)
- Create a scrolling message marquee with `lcd.scrollDisplayLeft()`
- Build a countdown timer or stopwatch
