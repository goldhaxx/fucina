# 7-Segment 1-Digit — Counter

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 080

Counts 0--9 on a single 7-segment display (5161AS, common cathode) using the SevSeg library by Dean Reading. Each digit displays for one second before advancing. After 9 it wraps back to 0.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-7seg-1digit/wiring.yaml -o sketches/craftingtable/ct-7seg-1digit/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x 5161AS 1-digit 7-segment display (common cathode)
- 8x jumper wires

## Pin Mapping

| Arduino Pin | Segment | Display Position |
|-------------|---------|------------------|
| 2           | A       | Top              |
| 3           | B       | Upper right      |
| 4           | C       | Lower right      |
| 5           | D       | Bottom           |
| 6           | E       | Lower left       |
| 7           | F       | Upper left       |
| 8           | G       | Middle           |
| 9           | DP      | Decimal point    |

The common cathode pin connects to GND. SevSeg handles driving the segments -- you just call `setNumber()`.

## Build and Upload

```bash
cd sketches/craftingtable/ct-7seg-1digit
pio run -e mega -t upload
pio device monitor -b 9600
```

The display counts from 0 to 9, one digit per second, then loops.

## What to Try Next

- Display letters (A--F) by using `setChars()` for a hex counter
- Add a push button to pause/resume counting
- Connect a second digit and build the 4-digit version (ct-7seg-4digit)
- Use a potentiometer to control the count speed
