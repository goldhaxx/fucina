# DHT11 — Temperature & Humidity

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 120

Reads temperature (°C and °F), humidity (%), and computed heat index from a DHT11 sensor every 2 seconds. Prints results to the serial monitor.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-dht-sensor/wiring.yaml -o sketches/craftingtable/ct-dht-sensor/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x DHT11 temperature & humidity sensor (KY-015 — the blue module with grid holes)
- 1x 10KΩ resistor (bands: brown, black, orange, gold) — pull-up from data to VCC
- 3x jumper wires

## Step-by-Step Wiring

The DHT11 module (KY-015) has 3 pins: S (data), VCC (+), GND (-).

### 1. Place the sensor module

Insert the 3 pins into consecutive breadboard rows:
- **S (data)** into row 10
- **VCC** into row 12
- **GND** into row 14

### 2. Place the 10KΩ pull-up resistor

- From **d10** (data row) to **d12** (VCC row)

This pulls the data line high when the sensor isn't actively driving it.

### 3. Connect jumper wires

- **Data (green):** From **a10** to **Pin 7** on the HERO XL
- **VCC (red):** From **a12** to **5V** on the HERO XL
- **GND (black):** From **a14** to **GND** on the HERO XL

## Build and Upload

```bash
cd sketches/craftingtable/ct-dht-sensor
pio run -e mega -t upload
pio device monitor
```

Readings appear every 2 seconds. The DHT11 is accurate to ±2°C and ±5% humidity — good enough for room monitoring.

## What to Try Next

- Display the temperature on an LCD1602 character display
- Add a threshold to trigger a buzzer when temperature is too high
- Log readings over time to build a temperature graph
