# 7-Segment 4-Digit — Stopwatch

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 085

Displays a running stopwatch (0.0 to 999.9 seconds) on a 4-digit 7-segment display (5641AS, common cathode). The display uses multiplexing -- only one digit is lit at a time, cycled rapidly by the SevSeg library so all four digits appear to be on simultaneously. Uses 12 pins total: 4 digit select + 8 segment lines (A-G plus decimal point).

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-7seg-4digit/wiring.yaml -o sketches/craftingtable/ct-7seg-4digit/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x 5641AS 4-digit 7-segment display (common cathode, 12 pins)
- 12x jumper wires
- 4x 220-ohm resistors (on digit pins to limit current)

## Step-by-Step Wiring

### 1. Place the 4-digit 7-segment display on the breadboard

The 5641AS has 12 pins (6 on top, 6 on bottom). Place it spanning the center channel of the breadboard so the top pins land in rows 5--10 on one side and the bottom pins on the other.

### 2. Connect digit select pins (common cathode pins)

These pins select which digit is active. The SevSeg library rapidly cycles through them.

- **Digit 1:** From **a5** to **Pin 2** on the HERO XL (red wire)
- **Digit 2:** From **a6** to **Pin 3** on the HERO XL (orange wire)
- **Digit 3:** From **a7** to **Pin 4** on the HERO XL (yellow wire)
- **Digit 4:** From **a8** to **Pin 5** on the HERO XL (green wire)

### 3. Connect segment pins

These 8 pins control which segments (A-G + decimal point) light up.

- **Seg A:** From **a10** to **Pin 6** on the HERO XL (blue wire)
- **Seg B:** From **a11** to **Pin 7** on the HERO XL (purple wire)
- **Seg C:** From **a12** to **Pin 8** on the HERO XL (brown wire)
- **Seg D:** From **a13** to **Pin 9** on the HERO XL (gray wire)
- **Seg E:** From **a14** to **Pin 10** on the HERO XL (red wire)
- **Seg F:** From **a15** to **Pin 11** on the HERO XL (orange wire)
- **Seg G:** From **a16** to **Pin 12** on the HERO XL (green wire)
- **Seg DP:** From **a17** to **Pin 13** on the HERO XL (blue wire)

### 4. Circuit explanation

The 5641AS is a common cathode display, meaning the cathode (ground) of each digit is shared. The SevSeg library drives the digit select pins LOW one at a time while setting the segment pins HIGH for the desired pattern. It cycles through all 4 digits fast enough (~1 kHz) that persistence of vision makes them all appear lit.

```
Pin 2  → Digit 1 common cathode
Pin 3  → Digit 2 common cathode
Pin 4  → Digit 3 common cathode
Pin 5  → Digit 4 common cathode
Pin 6  → Segment A
Pin 7  → Segment B
Pin 8  → Segment C
Pin 9  → Segment D
Pin 10 → Segment E
Pin 11 → Segment F
Pin 12 → Segment G
Pin 13 → Decimal Point
```

Each segment should have a 220-ohm current-limiting resistor in series (on the segment pins, not the digit pins) to keep the LED current at a safe level.

## Build and Upload

```bash
cd sketches/craftingtable/ct-7seg-4digit
pio run -e mega -t upload
```

The display starts counting from 0.0 upward in tenths of a second. The decimal point appears between the third and fourth digits, showing seconds with one decimal place. The counter resets to 0.0 after reaching 999.9.

## What to Try Next

- Add a push button to start/stop/reset the stopwatch
- Display a countdown timer instead of counting up
- Use `sevseg.setChars()` to display text like "HELP" or "COOL"
- Connect two displays for an 8-digit readout
