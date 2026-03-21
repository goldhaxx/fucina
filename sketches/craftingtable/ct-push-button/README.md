# Push Button — Digital Read

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 040

Reads a momentary push button using `INPUT_PULLUP` (no external resistor needed) and prints the state to the serial monitor. Compatible with Arduino Serial Plotter.

With `INPUT_PULLUP`, the pin reads **HIGH (1) when released** and **LOW (0) when pressed** — inverted logic.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-push-button/wiring.yaml -o sketches/craftingtable/ct-push-button/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x momentary push button (from the Circuits Essentials bag)
- 2x jumper wires

## Step-by-Step Wiring

### 1. Place the push button

Push buttons have 4 pins that straddle the center channel of the breadboard. Press the button into the breadboard so it spans the channel — legs in rows 10 and 11 across the gap.

- Two pins in **row 10** (one on each side of the channel)
- Two pins in **row 11** (one on each side of the channel)

### 2. Connect jumper wires

- **Wire 1 (signal — blue):** From **a10** to **Pin 12** on the HERO XL
- **Wire 2 (ground — black):** From **a11** to **GND** on the HERO XL

### 3. How it works

The code uses `INPUT_PULLUP`, which connects an internal resistor between the pin and 5V. When the button is pressed, it connects Pin 12 to GND through row 11, pulling the pin LOW.

```
Pin 12 ← internal pull-up → 5V (reads HIGH normally)
Pin 12 ← button pressed → GND (reads LOW)
```

## Build and Upload

```bash
cd sketches/craftingtable/ct-push-button
pio run -e mega -t upload
pio device monitor
```

Press the button — you should see the value toggle between 1 (released) and 0 (pressed).

## What to Try Next

- Add an LED that lights up when the button is pressed
- Implement a toggle: press once to turn on, press again to turn off (debouncing needed)
- Count button presses and display the count
