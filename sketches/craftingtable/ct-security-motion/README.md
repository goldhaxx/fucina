# Security Motion Lights — PIR + LED

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Chapter 02, Lesson 01

Turns on an LED "flood light" whenever the PIR sensor detects motion. The light stays on as long as motion is detected, then turns off when the area is clear.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

```bash
python3 tools/breadboard.py sketches/craftingtable/ct-security-motion/wiring.yaml -o sketches/craftingtable/ct-security-motion/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x HC-SR501 PIR motion sensor
- 1x LED (any color)
- 1x 220Ω resistor
- 5x jumper wires

## Wiring

- **Pin 22** → 220Ω resistor → LED anode → LED cathode → GND
- **Pin 23** ← PIR signal output
- **5V** → PIR VCC
- **GND** → PIR GND

## Build and Upload

```bash
cd sketches/craftingtable/ct-security-motion
pio run -e mega -t upload
```

Wait ~1 minute for the PIR sensor to warm up, then wave your hand in front of it — the LED lights up.

## What to Try Next

- Add a buzzer on another pin for an audible alarm
- Use `millis()` to keep the light on for a fixed duration after motion stops
- Add a second PIR sensor covering a different area
