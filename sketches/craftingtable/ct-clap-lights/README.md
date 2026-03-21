# Clap Lights — Sound Sensor Toggle

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Chapter 04, Lesson 04

Toggles the onboard LED on/off when a loud sound (clap) is detected by the KY-038 sound sensor. The digital output threshold is set by the potentiometer on the sensor module.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

```bash
python3 tools/breadboard.py sketches/craftingtable/ct-clap-lights/wiring.yaml -o sketches/craftingtable/ct-clap-lights/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x KY-037 or KY-038 sound sensor module
- 4x jumper wires

## Wiring

- **A0** ← sensor analog output (raw sound level)
- **Pin 2** ← sensor digital output (threshold trigger)
- **5V** → sensor VCC
- **GND** → sensor GND

## Setup

**Important:** Adjust the potentiometer on the sensor module before use. Turn it until the digital LED on the module just goes off in a quiet room. Then a clap should trigger it.

## Build and Upload

```bash
cd sketches/craftingtable/ct-clap-lights
pio run -e mega -t upload
pio device monitor
```

Clap near the sensor — the onboard LED toggles. The serial monitor shows the raw analog sound level.

## What to Try Next

- Replace the onboard LED with an external LED or relay for real lights
- Require two claps in quick succession (double-clap detection)
- Add a cooldown period to prevent accidental toggles from ambient noise
