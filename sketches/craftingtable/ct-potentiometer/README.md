# Potentiometer — Analog Read

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 030

Reads a potentiometer's position via `analogRead()` and prints the value (0–1023) to the serial monitor. Compatible with Arduino Serial Plotter for live visualization.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-potentiometer/wiring.yaml -o sketches/craftingtable/ct-potentiometer/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x potentiometer (B103 — the small knob with 3 pins)
- 3x jumper wires

## Step-by-Step Wiring

### 1. Place the potentiometer

The potentiometer has 3 pins. Orient it so the single pin is on one side and two pins are on the other.

Push the 3 pins into the breadboard:
- **Pin 1** (single pin side) into hole **a10**
- **Pin 2** (middle) into hole **a11**
- **Pin 3** into hole **a12**

### 2. Connect jumper wires

- **Wire 1 (signal — green):** From **a10** (or same row) to **A0** on the HERO XL analog header
- **Wire 2 (power — red):** From **a11** (or same row) to **5V** on the HERO XL
- **Wire 3 (ground — black):** From **a12** (or same row) to **GND** on the HERO XL

### 3. Electrical path

```
HERO XL A0 ← potentiometer pin 1 (wiper output)
HERO XL 5V → potentiometer pin 2 (reference voltage)
HERO XL GND → potentiometer pin 3
```

## Build and Upload

```bash
cd sketches/craftingtable/ct-potentiometer
pio run -e mega -t upload
pio device monitor
```

Turn the knob — you should see values from 0 to 1023 scrolling in the serial monitor. Open **Serial Plotter** (Tools → Serial Plotter in Arduino IDE, or `pio device monitor --raw`) for a live graph.

## What to Try Next

- Use the potentiometer value to control an LED brightness with `analogWrite()`
- Map the 0–1023 range to a servo angle (0–180°) using `map()`
