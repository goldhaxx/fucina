# Rotary Encoder — Rotation + Click

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 035

Tracks rotation of a KY-040 rotary encoder using hardware interrupts. Prints a running counter to the serial monitor — turn clockwise to increment, counter-clockwise to decrement. The built-in push button is also detected.

**Important:** The rotary encoder is NOT a potentiometer. It outputs digital pulses for rotation direction, not an analog value.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-rotary-encoder/wiring.yaml -o sketches/craftingtable/ct-rotary-encoder/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x KY-040 rotary encoder module (the knob with a click)
- 5x jumper wires

## Step-by-Step Wiring

The KY-040 has 5 pins: CLK, DT, SW, +, GND.

**CLK and DT must be on interrupt-capable pins** — on the Mega, that's pins 2, 3, 18, 19, 20, 21.

- **CLK** → **Pin 2** (INT0)
- **DT** → **Pin 3** (INT1)
- **SW** → **Pin 18** (INT5, uses INPUT_PULLUP)
- **+** → **5V**
- **GND** → **GND**

## Build and Upload

```bash
cd sketches/craftingtable/ct-rotary-encoder
pio run -e mega -t upload
pio device monitor -b 115200
```

Turn the knob — the counter increments and decrements. Press the knob to trigger the switch.

## What to Try Next

- Use the encoder to set a value (brightness, volume, servo angle)
- Add an LED whose brightness tracks the counter value
- Build a menu system navigated by rotation + click
