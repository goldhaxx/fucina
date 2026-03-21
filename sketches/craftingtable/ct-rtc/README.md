# Real-Time Clock — DS3231

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 140

Reads and displays the current date/time from a DS3231 RTC module (ZS-042) over I2C, printing to serial every 5 seconds. Time can be set by sending a 13-character string in `YYMMDDwHHMMSS` format via the serial monitor.

The DS3231 is one of the most accurate RTC chips available (drifts about 1 minute per year). The onboard CR2032 backup battery keeps time even when the board is unpowered or disconnected -- once you set the clock, it stays set.

**I2C note:** The DS3231 uses address `0x68`, which conflicts with the MPU-6050 accelerometer/gyroscope at its default address. If using both on the same I2C bus, set the MPU-6050's AD0 pin HIGH to shift it to `0x69`.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-rtc/wiring.yaml -o sketches/craftingtable/ct-rtc/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x DS3231 ZS-042 RTC module (with CR2032 battery installed)
- 4x jumper wires

## Step-by-Step Wiring

### 1. Place the DS3231 module on the breadboard

Insert the DS3231 ZS-042 module's header pins into the breadboard. The module has pins labeled **VCC**, **GND**, **SDA**, and **SCL**.

- **VCC** into hole **a10**
- **GND** into hole **a11**
- **SDA** into hole **a12**
- **SCL** into hole **a13**

### 2. Connect jumper wires

- **Wire 1 (power -- red):** From **a10** to **5V** on the HERO XL
- **Wire 2 (ground -- black):** From **a11** to **GND** on the HERO XL
- **Wire 3 (SDA -- blue):** From **a12** to **Pin 20** (SDA) on the HERO XL
- **Wire 4 (SCL -- green):** From **a13** to **Pin 21** (SCL) on the HERO XL

### 3. Circuit explanation

The DS3231 communicates over I2C, which only needs two data lines (SDA and SCL) plus power. The module has onboard pull-up resistors, so no external pull-ups are needed.

```
5V  → DS3231 VCC
GND → DS3231 GND
Pin 20 (SDA) ↔ DS3231 SDA
Pin 21 (SCL) ↔ DS3231 SCL
```

## Build and Upload

```bash
cd sketches/craftingtable/ct-rtc
pio run -e mega -t upload
pio device monitor -b 115200
```

## Setting the Time

Send a 13-character string via the serial monitor in this format:

```
YYMMDDwHHMMSS
```

Where `w` is the day of the week (1 = Monday, 7 = Sunday).

**Example:** To set **2026-03-21 Saturday 10:15:00**, send:

```
2603214101500
```

Make sure the serial monitor is set to send a carriage return (`\r`) at the end of the line.

## What to Try Next

- Build an alarm clock that triggers a buzzer at a set time
- Log sensor readings with timestamps to the onboard AT24C32 EEPROM
- Display the time on an LCD1602 or 7-segment display
- Read the DS3231's built-in temperature sensor (accurate to about 3 degrees C)
