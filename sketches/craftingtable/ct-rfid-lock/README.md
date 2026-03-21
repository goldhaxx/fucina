# RFID Door Lock — Card Access Control

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Chapter 02, Lesson 03

Scans RFID cards and tags with the MFRC-522 reader and displays "Come on in!" or "NO MATCH" on the LCD1602 display. On first run, scan your cards to capture their UID bytes from the serial monitor, then add them to the `APPROVED` array in `main.cpp` to grant access.

> **WARNING: The MFRC-522 module MUST be powered from 3.3V, NOT 5V. Connecting 5V will damage the module.**

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-rfid-lock/wiring.yaml -o sketches/craftingtable/ct-rfid-lock/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x MFRC-522 RC522 RFID reader module
- 1x S50 RFID card
- 1x RFID keychain tag
- 1x LCD1602 (16x2 character display)
- 16x jumper wires

## Step-by-Step Wiring

### 1. Place the RFID module on the breadboard

Insert the MFRC-522 module header pins into the breadboard at rows 5--11. The module has 8 pins but only 7 are used (IRQ is not connected).

### 2. Connect RFID jumper wires

| MFRC-522 Pin | Breadboard Hole | HERO XL Pin | Wire Color |
|--------------|-----------------|-------------|------------|
| SDA (SS)     | a5              | Pin 53      | Red        |
| SCK          | a6              | Pin 52      | Orange     |
| MOSI         | a7              | Pin 51      | Green      |
| MISO         | a8              | Pin 50      | Blue       |
| RST          | a9              | Pin 26      | Purple     |
| VCC (3.3V)   | a10             | 3.3V        | Orange     |
| GND          | a11             | GND         | Black      |

### 3. Place the LCD1602 on the breadboard

Insert the LCD1602 header pins into the breadboard starting at row 14. The LCD is wired in 4-bit parallel mode with contrast tied to GND for maximum contrast.

### 4. Connect LCD jumper wires

| LCD Pin  | Breadboard Hole | HERO XL Pin | Wire Color |
|----------|-----------------|-------------|------------|
| RS       | a14             | Pin 22      | Red        |
| E        | a15             | Pin 24      | Orange     |
| D4       | a16             | Pin 23      | Green      |
| D5       | a17             | Pin 25      | Blue       |
| D6       | a18             | Pin 27      | Purple     |
| D7       | a19             | Pin 29      | Brown      |
| VDD (5V) | a20             | 5V          | Red        |
| VSS (GND)| a21             | GND         | Black      |
| A (BL)   | a22             | 3.3V        | Orange     |

**Note:** LCD RW pin is tied to GND (write-only mode). V0 (contrast) is tied to GND for maximum contrast. Backlight anode uses 3.3V for safe operation without a current-limiting resistor.

### 5. Circuit explanation

The MFRC-522 communicates over SPI using the Mega's hardware SPI pins (50--53). The LCD1602 uses 4-bit parallel mode on digital pins 22--29 (high-numbered pins to avoid conflicts with SPI).

```
RFID (SPI):
Pin 53 (SS)   -> MFRC-522 SDA (chip select)
Pin 52 (SCK)  -> MFRC-522 SCK (clock)
Pin 51 (MOSI) -> MFRC-522 MOSI (data out)
Pin 50 (MISO) -> MFRC-522 MISO (data in)
Pin 26        -> MFRC-522 RST (reset)
3.3V          -> MFRC-522 VCC (power -- NOT 5V!)
GND           -> MFRC-522 GND

LCD (4-bit parallel):
Pin 22 (RS)   -> LCD RS (register select)
Pin 24 (E)    -> LCD E (enable)
Pin 23 (D4)   -> LCD D4
Pin 25 (D5)   -> LCD D5
Pin 27 (D6)   -> LCD D6
Pin 29 (D7)   -> LCD D7
5V            -> LCD VDD
GND           -> LCD VSS, RW, V0
3.3V          -> LCD backlight anode
```

### 6. How the lock works

1. On startup, the LCD displays "Tap to Enter"
2. Hold an RFID card or keychain tag near the reader
3. The card's UID bytes are printed to the serial monitor
4. If the UID matches an entry in the `APPROVED` array, the LCD shows "Come on in!"
5. If the UID does not match, the LCD shows "NO MATCH"
6. After 2 seconds the status clears and you can scan again

### 7. Adding your cards

1. Upload the sketch and open the serial monitor at 9600 baud
2. Scan each card/tag you want to approve
3. Copy the UID bytes from the serial output (e.g., `Card UID: 19, 162, 41, 43`)
4. Replace the placeholder in the `APPROVED` array:
   ```cpp
   const byte APPROVED[][10] = {
     {19, 162, 41, 43},    // My blue card
     {115, 200, 87, 12},   // Keychain tag
   };
   ```
5. Re-upload the sketch

## Build and Upload

```bash
cd sketches/craftingtable/ct-rfid-lock
pio run -e mega -t upload
pio device monitor -b 9600
```

Scan a card to see its UID in the serial monitor and the access status on the LCD.

## What to Try Next

- Add a servo motor to physically lock/unlock a latch on valid scan
- Add a piezo buzzer for audible feedback (beep on scan, tone on grant/deny)
- Store approved UIDs in EEPROM so they persist across power cycles
- Add a "learn mode" activated by a button that enrolls new cards without re-flashing
- Combine with the keypad for two-factor authentication (card + PIN)
