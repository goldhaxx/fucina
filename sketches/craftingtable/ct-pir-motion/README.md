# PIR Motion Sensor — Motion Detection

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 090

Detects motion using the HC-SR501 PIR (Passive Infrared) sensor and prints status changes to the serial monitor. The sensor outputs a digital HIGH when motion is detected and LOW when the area is clear.

**Note:** The HC-SR501 has a ~1 minute warm-up period after power-on. During this time the sensor may trigger false readings. Wait for it to stabilize before testing.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-pir-motion/wiring.yaml -o sketches/craftingtable/ct-pir-motion/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x HC-SR501 PIR motion sensor module
- 3x jumper wires (male-to-female recommended for the PIR module header)

## Step-by-Step Wiring

### 1. Identify the PIR sensor pins

The HC-SR501 has 3 pins on its header. Looking at the module from the front (dome facing you), with the header at the bottom:

```
VCC — Signal (OUT) — GND
```

Check the silkscreen labels on your specific module — pin order can vary between manufacturers.

### 2. Connect the PIR sensor to the breadboard

Insert 3 jumper wires from the PIR module header into consecutive breadboard rows:
- **VCC** into **a10**
- **Signal (OUT)** into **a11**
- **GND** into **a12**

### 3. Connect jumper wires to the HERO XL

- **Wire 1 (red):** From **a10** to **5V** on the HERO XL
- **Wire 2 (orange):** From **a11** to **Pin 2** on the HERO XL
- **Wire 3 (black):** From **a12** to **GND** on the HERO XL

### 4. Electrical path

```
HERO XL 5V  → PIR VCC (power)
HERO XL Pin 2 ← PIR Signal OUT (digital HIGH/LOW)
HERO XL GND → PIR GND (ground)
```

### 5. Adjust the PIR module (optional)

The HC-SR501 has two potentiometers on the back:
- **Sensitivity:** Adjusts detection range (up to ~7 meters)
- **Delay:** Adjusts how long the output stays HIGH after detection (5 seconds to ~5 minutes)

There is also a jumper to select trigger mode:
- **Single trigger (H):** Output goes HIGH once, then LOW after delay, regardless of continued motion
- **Repeatable trigger (L):** Output stays HIGH as long as motion continues, delay resets with each detection

## Build and Upload

```bash
cd sketches/craftingtable/ct-pir-motion
pio run -e mega -t upload
pio device monitor
```

Open the serial monitor at 115200 baud. After the warm-up period, wave your hand in front of the sensor. You should see:

```
PIR Sensor warming up... (wait ~1 minute)
Motion Detected!
All quiet...
Motion Detected!
```

## What to Try Next

- Add an LED or active buzzer as a visual/audible alarm when motion is detected
- Count the number of motion events and print a running total
- Add a delay cooldown between detections to debounce rapid triggers
- Combine with the ultrasonic sensor for distance + motion awareness
