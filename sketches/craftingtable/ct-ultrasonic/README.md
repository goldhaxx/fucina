# Ultrasonic Sensor — Distance Measurement

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 070

Measures distance using the HC-SR04 ultrasonic sensor and prints readings in centimeters and inches to the serial monitor at 115200 baud. The sensor sends a 10-microsecond trigger pulse, then measures the echo return time to calculate distance (range: 2 cm to 400 cm).

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-ultrasonic/wiring.yaml -o sketches/craftingtable/ct-ultrasonic/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x HC-SR04 ultrasonic distance sensor (4-pin module)
- 4x jumper wires

## Step-by-Step Wiring

### 1. Identify the HC-SR04 pins

The HC-SR04 has 4 pins in a row. Looking at the front (the side with the two silver transducers):

```
VCC — Trig — Echo — GND
```

### 2. Place the sensor

Insert the 4 pins into consecutive rows on the left bank of the breadboard:
- **VCC** into **a10**
- **Trig** into **a11**
- **Echo** into **a12**
- **GND** into **a13**

### 3. Connect jumper wires

- **Wire 1 (red):** From **a10** to **5V** on the HERO XL (power)
- **Wire 2 (orange):** From **a11** to **Pin 13** on the HERO XL (trigger)
- **Wire 3 (blue):** From **a12** to **Pin 12** on the HERO XL (echo)
- **Wire 4 (black):** From **a13** to **GND** on the HERO XL (ground)

### 4. Electrical path

```
HERO XL 5V  → VCC (powers the sensor)
HERO XL Pin 13 → Trig (sends 10us pulse to start measurement)
HERO XL Pin 12 ← Echo (returns HIGH for duration proportional to distance)
HERO XL GND → GND
```

## Build and Upload

```bash
cd sketches/craftingtable/ct-ultrasonic
pio run -e mega -t upload
pio device monitor -b 115200
```

You should see distance readings updating approximately 5 times per second:
```
Distance: 15 cm, 5 inch
```

## What to Try Next

- Add an LED or buzzer that triggers when an object is within a threshold distance
- Map the distance to a servo angle to create a radar-like sweep
- Use the LCD1602 display to show distance readings without a computer
