# Alarm Clock — RTC + 7-Segment + Buzzer

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Chapter 04, Lesson 01

Displays the current time on a 4-digit 7-segment display using a DS3231 real-time clock module, and sounds an active buzzer alarm when the configured alarm time is reached. Time can be set via serial by sending a `YYMMDDwHHMMSS` string. This is a multi-component integration project combining 3 devices: RTC (I2C), 7-segment display (12 GPIO pins), and buzzer.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

```bash
python3 tools/breadboard.py sketches/craftingtable/ct-alarm-clock/wiring.yaml -o sketches/craftingtable/ct-alarm-clock/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x DS3231 RTC module (ZS-042)
- 1x 4-digit 7-segment display (5641AS, common cathode)
- 1x active buzzer
- 18x jumper wires

## Wiring

### 4-Digit 7-Segment Display
- **Pin 2** → digit 1 common
- **Pin 3** → digit 2 common
- **Pin 4** → digit 3 common
- **Pin 5** → digit 4 common
- **Pin 6** → segment A
- **Pin 7** → segment B
- **Pin 8** → segment C
- **Pin 9** → segment D
- **Pin 10** → segment E
- **Pin 11** → segment F
- **Pin 12** → segment G
- **Pin 13** → segment DP (decimal point)

### DS3231 RTC
- **Pin 20 (SDA)** → RTC SDA
- **Pin 21 (SCL)** → RTC SCL
- **5V** → RTC VCC
- **GND** → RTC GND

### Active Buzzer
- **Pin 45** → buzzer signal (+)
- **GND** → buzzer ground (-)

## Build and Upload

```bash
cd sketches/craftingtable/ct-alarm-clock
pio run -e mega -t upload
```

Open the serial monitor at 115200 baud. The display shows the current time in HHMM format. To set the time, send a 13-character string in `YYMMDDwHHMMSS` format (e.g., `2603211143000` for 2026-03-21, Saturday, 14:30:00).

## What to Try Next

- Add a push button to snooze or dismiss the alarm
- Use the decimal point to blink as a seconds indicator
- Add multiple alarm times stored in the DS3231's EEPROM
- Display seconds by alternating between HH:MM and MM:SS every few seconds
