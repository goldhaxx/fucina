# Plant Monitor — Water Sensor + LED

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Chapter 03, Lesson 01

Monitors soil moisture using a water level sensor. The LED brightness increases proportionally with moisture level — brighter means wetter soil. Below the dry threshold, the LED stays off (plant needs water!).

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

```bash
python3 tools/breadboard.py sketches/craftingtable/ct-plant-monitor/wiring.yaml -o sketches/craftingtable/ct-plant-monitor/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x water level sensor (HW-038) + control board
- 1x LED (any color)
- 5x jumper wires

## Wiring

- **Pin 22** → LED anode (must be PWM-capable for `analogWrite`)
- **A8** ← water sensor signal
- **5V** → sensor VCC
- **GND** → sensor GND, LED cathode

## Build and Upload

```bash
cd sketches/craftingtable/ct-plant-monitor
pio run -e mega -t upload
pio device monitor
```

Touch the sensor with a wet finger — the LED brightens and the serial monitor shows the raw sensor value and mapped brightness.

## What to Try Next

- Add a buzzer that beeps when the soil is too dry
- Power-gate the sensor (like ct-rain-sensor) to prevent corrosion
- Display moisture level on the LCD1602
