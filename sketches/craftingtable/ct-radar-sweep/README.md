# Radar Sweep — Servo + Ultrasonic + TFT

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Chapter 06, Lesson 20

Sweeps an HC-SR04 ultrasonic sensor mounted on an SG90 servo 180 degrees and plots distance readings as cyan dots on the 2.4" ILI9341 TFT LCD touchscreen shield, creating a radar-style display. The servo steps in 2-degree increments, taking a distance measurement at each position. Range rings are drawn at fixed intervals to help visualize distance.

The LCD touchscreen shield plugs directly onto the HERO XL headers and consumes many pins (D2-D9 for data, A0-A4 for control, D10-D13 for SD/SPI). The servo and ultrasonic sensor use pins 22-24 to avoid conflicts.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-radar-sweep/wiring.yaml -o sketches/craftingtable/ct-radar-sweep/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x 2.4" ILI9341 TFT LCD touchscreen shield (plugs onto HERO XL headers)
- 1x HC-SR04 ultrasonic distance sensor
- 1x SG90 micro servo motor
- 5x jumper wires

## Step-by-Step Wiring

### 1. Mount the LCD shield

Plug the 2.4" TFT LCD touchscreen shield directly onto the HERO XL headers. It will consume pins D2-D9, A0-A4, and D10-D13.

### 2. Place the ultrasonic sensor and servo on the breadboard

The HC-SR04 has 4 pins and the servo has 3 wires. Both share 5V power and GND.

### 3. Connect jumper wires

- **Wire 1 (orange):** From **a10** to **Pin 22** on the HERO XL (ultrasonic TRIG)
- **Wire 2 (blue):** From **a11** to **Pin 23** on the HERO XL (ultrasonic ECHO)
- **Wire 3 (purple):** From **a12** to **Pin 24** on the HERO XL (servo signal)
- **Wire 4 (red):** From **a13** to **5V** on the HERO XL (power for both)
- **Wire 5 (black):** From **a14** to **GND** on the HERO XL (ground for both)

### 4. Mount the ultrasonic sensor on the servo

Attach the HC-SR04 sensor to the servo horn so it rotates with the servo. You can use tape, hot glue, or a 3D-printed bracket.

## Servo Calibration

Before running the full radar sweep, you can calibrate the servo to ensure it points straight ahead at 90 degrees. In `src/main.cpp`, uncomment these two lines near the top of `loop()`:

```cpp
myServo.write(90);
return;
```

Upload with these lines uncommented. The servo will hold at 90 degrees so you can align the ultrasonic sensor to face straight ahead. Once aligned, comment the lines back out and re-upload for normal radar operation.

## Build and Upload

```bash
cd sketches/craftingtable/ct-radar-sweep
pio run -e mega -t upload
pio device monitor
```

The TFT display should show a radar-style view with cyan dots appearing as the servo sweeps back and forth. Range rings (blue circles) are drawn at fixed intervals. The display clears periodically to prevent dot buildup.

## What to Try Next

- Adjust the sweep step size (currently 2 degrees) for finer or coarser resolution
- Change the dot color based on distance (close = red, far = green)
- Add a sweep line that follows the current servo angle
- Display the closest detected object distance as text on the screen
