# IR Receiver — Remote Control Decoder

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 060

Receives and decodes infrared signals from the included NEC-protocol remote control. Each button press prints the hex code and protocol details to the serial monitor. Use this to map button codes for your own IR-controlled projects.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-ir-receiver/wiring.yaml -o sketches/craftingtable/ct-ir-receiver/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x IR receiver module (KY-022 — the small dark bulb on a board, 3 pins)
- 1x IR remote control (the black remote with 21 buttons)
- 3x jumper wires

## Step-by-Step Wiring

The KY-022 IR receiver module has 3 pins:
- **S** (signal) — data output
- **Middle pin** — VCC (5V)
- **-** (minus) — GND

### Connect the module

- **Signal (S)** via row 10 → **Pin 11** on the HERO XL
- **VCC (middle)** via row 11 → **5V** on the HERO XL
- **GND (-)** via row 12 → **GND** on the HERO XL

## Build and Upload

```bash
cd sketches/craftingtable/ct-ir-receiver
pio run -e mega -t upload
pio device monitor -b 115200
```

Point the remote at the receiver (within ~5 meters) and press buttons. Each press prints the raw hex code and decoded protocol info.

## What to Try Next

- Write down the hex code for each button to build a lookup table
- Use specific button codes to control LEDs, a servo, or a buzzer
- Build an IR-controlled robot or light show
