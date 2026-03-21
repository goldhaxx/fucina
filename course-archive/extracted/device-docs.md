# Device Documentation

Extracted from `Devices/` -- component datasheets and identification guides.

---

## Buzzer Identification Guide

Adventure Kit 2 contains four buzzers: two active and two passive.

### Active vs Passive

| Property | Active Buzzer | Passive Buzzer |
|----------|---------------|----------------|
| Function | Fixed pitch, just needs power | Variable pitch, needs external signal |
| Code | `digitalWrite(pin, HIGH)` | `tone(pin, frequency)` |
| Sound when powered | Continuous tone | Click/tick sound |

### Form Factors

- **2-pin components:** Small, fragile, bare components
- **3-pin modules:** Correct pin spacing, mounted on small PCB (third pin is not connected)

### Identifying 2-pin buzzers
- **Active (KY-012):** Closed/sealed bottom
- **Passive:** Open bottom, exposed circuit board

### Identifying 3-pin modules by part number
- **Active:** KY-012, HW-512
- **Passive:** KY-006, HW-508

### 9V Battery Test
- **Active:** Makes continuous tone
- **Passive:** Makes clicking sound

---

## 5641AS — 4-Digit 7-Segment LED Display

Red, common cathode 4-digit display.

**Segment layout:** Standard 7-segment (A-G + DP)
**Resistance required:** At least 800 ohm on each segment pin to prevent current overload.
**Datasheet:** http://www.xlitx.com/datasheet/5641AS.pdf

---

## HW-038 — Water Level Detector

Analog water level sensor. Ten exposed copper traces (5 power, 5 sense) that are bridged by water. Power only during reads to prevent corrosion.

**Tutorial:** https://lastminuteengineers.com/water-level-sensor-arduino-tutorial/

---

## HW-512 — 3-Pin Active Buzzer

Active buzzer on PCB module. Fixed pitch when powered. Third pin is not connected.

---

## KY-012 — 2-Pin Active Buzzer

Bare 2-pin active buzzer. Sealed back. Fixed pitch when voltage applied.

---

## SG90 Micro Servo

Small servo motor for angular positioning (0-180 degrees).

**Wires:** Red (power), Brown (ground), Yellow/Orange (signal)
**Power:** Connect to ground and power on the microcontroller, signal to a digital pin
**Datasheet:** http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf
