# Sound Sensor — Clap Detection

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 130

Reads both the digital threshold output and analog raw sound level from a KY-037/KY-038 sound sensor module and prints the values to serial. The digital pin goes HIGH when the sound exceeds the threshold set by the onboard potentiometer. The analog pin outputs a raw sound level reading (0-1023). A running peak level is tracked to help visualize the loudest sound detected.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-sound-sensor/wiring.yaml -o sketches/craftingtable/ct-sound-sensor/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x KY-037 or KY-038 sound sensor module
- 4x jumper wires

## Step-by-Step Wiring

The KY-037/KY-038 module has 4 pins. Pin labels vary by manufacturer — look for VCC/+, GND/G, A0/AO (analog out), and D0/DO/S (digital out).

### 1. Connect power

- **Wire 1 (power — red):** From sensor **VCC/+** pin through row **a10** to **5V** on the HERO XL

### 2. Connect ground

- **Wire 2 (ground — black):** From sensor **GND/G** pin through row **a11** to **GND** on the HERO XL

### 3. Connect analog output

- **Wire 3 (analog — green):** From sensor **A0** pin through row **a12** to **A0** on the HERO XL analog header

### 4. Connect digital output

- **Wire 4 (digital — orange):** From sensor **D0/S** pin through row **a13** to **Pin 2** on the HERO XL

### 5. Adjust the threshold

The module has a small potentiometer (blue knob) on the PCB. Turn it with a small screwdriver to set the digital trigger threshold:
- **Clockwise:** less sensitive (louder sounds needed to trigger)
- **Counter-clockwise:** more sensitive (quieter sounds trigger)

The onboard LED on the module lights up when the digital output goes HIGH.

## Build and Upload

```bash
cd sketches/craftingtable/ct-sound-sensor
pio run -e mega -t upload
pio device monitor -b 115200
```

Serial output format: `digital, analog, peak`
- **digital:** 0 or 1 (1 = sound exceeded threshold)
- **analog:** raw sound level (0-1023)
- **peak:** highest analog value seen so far (capped at 100)

Clap near the sensor — you should see the digital value spike to 1 and the analog value jump. Speak, snap, or tap the table to see how different sounds register.

## What to Try Next

- Add an LED that toggles on/off with each clap (clap-switch)
- Build a sound-level meter using multiple LEDs as a bar graph
- Use the analog value to control servo position — louder sound = more rotation
