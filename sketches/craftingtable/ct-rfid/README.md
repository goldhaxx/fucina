# RFID Reader — Card UID Scanner

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 150

Reads and displays the unique ID (UID) of RFID cards and tags using the MFRC-522 reader module via SPI. Each card/tag has a factory-assigned UID that is printed to the serial monitor when scanned.

> **WARNING: The MFRC-522 module MUST be powered from 3.3V, NOT 5V. Connecting 5V will damage the module.**

The SPI interface uses the hardware SPI pins on the Mega (50--53), which gives reliable high-speed communication with the reader.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-rfid/wiring.yaml -o sketches/craftingtable/ct-rfid/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x MFRC-522 RC522 RFID reader module
- 1x S50 RFID card
- 1x RFID keychain tag
- 7x jumper wires

## Step-by-Step Wiring

### 1. Place the RFID module on the breadboard

Insert the MFRC-522 module header pins into the breadboard. The module has 8 pins but only 7 are used (IRQ is not connected in this sketch).

### 2. Connect jumper wires

| MFRC-522 Pin | Breadboard Hole | HERO XL Pin | Wire Color |
|--------------|-----------------|-------------|------------|
| SDA (SS)     | a5              | Pin 53      | Red        |
| SCK          | a6              | Pin 52      | Orange     |
| MOSI         | a7              | Pin 51      | Green      |
| MISO         | a8              | Pin 50      | Blue       |
| RST          | a9              | Pin 26      | Purple     |
| VCC (3.3V)   | a10             | 3.3V        | Orange     |
| GND          | a11             | GND         | Black      |

### 3. Circuit explanation

The MFRC-522 communicates over SPI, a 4-wire protocol (SCK, MOSI, MISO, SS). The HERO XL's hardware SPI pins are fixed at 50--53 on the Mega 2560. The RST pin is configurable -- Pin 26 is used here to stay clear of other common pin assignments.

```
Pin 53 (SS)   → MFRC-522 SDA (chip select)
Pin 52 (SCK)  → MFRC-522 SCK (clock)
Pin 51 (MOSI) → MFRC-522 MOSI (data out)
Pin 50 (MISO) → MFRC-522 MISO (data in)
Pin 26        → MFRC-522 RST (reset)
3.3V          → MFRC-522 VCC (power — NOT 5V!)
GND           → MFRC-522 GND
```

## Build and Upload

```bash
cd sketches/craftingtable/ct-rfid
pio run -e mega -t upload
pio device monitor -b 9600
```

On startup, the firmware version of the MFRC-522 is printed. Hold an RFID card or keychain tag near the reader -- the UID bytes are printed as dash-separated decimal values.

## What to Try Next

- Store known UIDs in an array and print "Access Granted" or "Access Denied"
- Build an access control system that unlocks a servo when a valid card is scanned
- Combine with the LCD1602 to display the UID and access status on screen
- Read and write data to the card's memory sectors (MIFARE Classic 1K has 16 sectors)
