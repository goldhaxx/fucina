# Photoresistor — Light Level

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 006

Reads ambient light level via a photoresistor (LDR) voltage divider and prints the analog value (0–1023) to serial. The onboard LED blinks at a rate proportional to the light level — brighter light = faster blinks.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-photoresistor/wiring.yaml -o sketches/craftingtable/ct-photoresistor/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x photoresistor (LDR — the small flat component with a squiggly pattern on top)
- 1x 10KΩ resistor (bands: brown, black, orange, gold)
- 3x jumper wires

## Step-by-Step Wiring

### 1. Place the photoresistor

The photoresistor has no polarity — either leg works in either direction.

- One leg into hole **e10**
- Other leg into hole **e12**

### 2. Place the 10KΩ pull-down resistor

- One leg into hole **d12** (same row as one photoresistor leg)
- Other leg into hole **d14**

### 3. Connect jumper wires

- **Wire 1 (signal — green):** From **a12** to **A0** on the HERO XL analog header
- **Wire 2 (power — red):** From **a10** to **5V** on the HERO XL
- **Wire 3 (ground — black):** From **a14** to **GND** on the HERO XL

### 4. Circuit explanation

This is a voltage divider. The photoresistor's resistance changes with light:
- **Bright light:** LDR resistance drops → voltage at A0 rises → higher reading
- **Dark:** LDR resistance rises → voltage at A0 drops → lower reading

```
5V → photoresistor → A0 junction → 10KΩ → GND
```

## Build and Upload

```bash
cd sketches/craftingtable/ct-photoresistor
pio run -e mega -t upload
pio device monitor -b 115200
```

Cover the photoresistor with your hand — the value drops. Shine a light on it — the value rises. The onboard LED blinks slower in darkness, faster in light.

## What to Try Next

- Use the light level to control an external LED brightness with `analogWrite()`
- Set a threshold to trigger a buzzer when it gets dark (nightlight alarm)
- Log values over time to see light patterns in a room
