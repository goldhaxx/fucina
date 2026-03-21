# Wiring Patterns

Common circuit building blocks used across fucina sketches.

---

## LED with Current-Limiting Resistor

```
GPIO pin ---[ 220Ω ]---[LED+]---[LED-]--- GND
```

- 220Ω is safe for most standard LEDs at 5V (~15 mA).
- At 3.3V (ESP32), 100Ω–150Ω works. 220Ω is still fine but dimmer.
- Long leg = anode (+), short leg = cathode (−).

---

## Pull-Down Resistor (Button)

```
        5V (or 3.3V)
         |
       [BUTTON]
         |
         +-----> GPIO pin (reads HIGH when pressed)
         |
       [10KΩ]
         |
        GND
```

- Without the resistor, the pin floats when the button is open.
- 10KΩ is the standard pull-down value.
- Alternative: use `INPUT_PULLUP` mode and wire button between pin and GND (inverted logic — LOW when pressed).

---

## Pull-Up Resistor (I2C bus)

```
        3.3V (or 5V)
         |
       [4.7KΩ]
         |
SDA -----+-----> to device(s)
```

- I2C requires pull-ups on both SDA and SCL.
- 4.7KΩ is standard. Use 2.2KΩ for long wires or many devices.
- Many breakout modules (DS3231, MPU-6050) have onboard pull-ups. If using multiple modules, you may need to desolder extras to avoid too-strong pull-up.

---

## Voltage Divider (5V → 3.3V signal)

```
5V signal ---[ 1KΩ ]---+---[ 2KΩ ]--- GND
                        |
                        +-----> 3.3V output to ESP32 GPIO
```

- Vout = Vin × R2 / (R1 + R2) = 5 × 2K / 3K = 3.33V
- Use for one-way level shifting (e.g., HERO XL TX → HC-06 RX).
- For bidirectional signals, use the logic level converter module instead.

---

## NPN Transistor Motor/Relay Driver

```
GPIO pin ---[ 1KΩ ]--- Base
                        |
               Collector|
        Load ──────────┘
         |
     +5V/+12V
                        |
               Emitter──┘
                        |
                       GND
```

- Use for loads that draw more than 20 mA (motors, relays, LED strips).
- 2N2222 or BC547 for loads up to ~500 mA.
- Add a flyback diode (1N4007) across inductive loads (motors, relays): cathode to +V, anode to collector.

---

## Flyback Diode (Inductive Load Protection)

```
       +V ──────────── Load+ (motor/relay coil)
         |                    |
    [1N4007]              Load−
     cathode↑                 |
      anode ──────────────────+──── to transistor collector or driver
```

- Inductive loads generate voltage spikes when switched off.
- The diode shorts the spike back through the coil instead of through your transistor or board.
- Always use with motors, relays, solenoids.

---

## Breadboard Power Supply Module

```
[Barrel Jack or USB] → [Module] → Breadboard power rails

Module jumpers select output per rail:
  - 3.3V position → that rail gets 3.3V
  - 5V position → that rail gets 5V
  - OFF → rail disconnected
```

- Input: 6.5–12V DC via barrel jack, or USB.
- Orientation matters — the module's +/− pins must align with the breadboard's +/− rails.
- Useful when the USB port can't supply enough current for motors + board simultaneously.

---

## Logic Level Converter (Bidirectional)

```
        5V side                3.3V side
        -------                ---------
  HV ── 5V power         LV ── 3.3V power
 GND ── Ground           GND ── Ground
 HV1 ── 5V signal 1      LV1 ── 3.3V signal 1
 HV2 ── 5V signal 2      LV2 ── 3.3V signal 2
 HV3 ── 5V signal 3      LV3 ── 3.3V signal 3
 HV4 ── 5V signal 4      LV4 ── 3.3V signal 4
```

- Required for I2C/SPI/UART between HERO XL (5V) and ESP32 (3.3V).
- Each channel is one signal line. 4 channels available.
- Connect reference voltages first (HV to 5V, LV to 3.3V), then signal lines.

---

## Photoresistor Voltage Divider

```
5V ──── [Photoresistor] ──+── Analog Pin (A0)
                           |
                        [10KΩ]
                           |
                          GND
```

- Forms a voltage divider where light changes the resistance of the LDR.
- `analogRead()` returns 0-1023. Higher values = more light (lower LDR resistance).
- 10KΩ pull-down resistor is required — without it, the analog pin floats.
- Same circuit pattern as any variable-resistance sensor (thermistor, FSR, etc.).

---

## DHT11/DHT22 Temperature & Humidity Sensor

```
       5V
        |
     [10KΩ] (pull-up)
        |
Data ---+----> GPIO pin 7

VCC ────────── 5V
GND ────────── GND
```

- Single-wire digital protocol — only one data pin needed.
- 10K pull-up resistor from data pin to VCC is recommended.
- Allow at least 2 seconds between reads (sensor is slow).
- Library: `DHT Sensor Library` by Adafruit.

---

## 7-Segment Display (Direct Drive, Common Cathode)

```
                    ┌─── A (seg) ───── GPIO + 220Ω
    ┌──────┐       ├─── B (seg) ───── GPIO + 220Ω
    │ 8.8. │       ├─── C (seg) ───── GPIO + 220Ω
    └──────┘       ├─── D (seg) ───── GPIO + 220Ω
                    ├─── E (seg) ───── GPIO + 220Ω
                    ├─── F (seg) ───── GPIO + 220Ω
                    ├─── G (seg) ───── GPIO + 220Ω
                    └─── COM ────────── GND
```

- Common cathode: COM pin to GND. Set segment GPIO HIGH to light it.
- 1-digit uses 7 GPIO pins + GND (8 with decimal point).
- 4-digit multiplexes 4 digit-select pins + 8 segment pins = 12 GPIO total.
- Each segment pin needs a current-limiting resistor (220Ω–800Ω).
- Library: `SevSeg` by Dean Reading handles multiplexing automatically.

---

## 4x4 Membrane Keypad (Matrix Scanning)

```
Keypad Pin:  1    2    3    4    5    6    7    8
             C4   C3   C2   C1   R4   R3   R2   R1
Arduino:     2    3    4    5    6    7    8    9
```

- 16 keys scanned with only 8 pins using row/column matrix.
- 4 row pins + 4 column pins. Library scans rows while reading columns.
- No external resistors or pull-ups needed — library handles it.
- Library: `Keypad` by Mark Stanley & Alexander Brevig.

---

## Rotary Encoder with Interrupts

```
        5V ──── + (VCC)
       GND ──── GND
  Pin 2 (INT0) ──── CLK
  Pin 3 (INT1) ──── DT
 Pin 18 (INT5) ──── SW
```

- CLK and DT must be on interrupt-capable pins (2, 3, 18, 19, 20, 21 on Mega).
- SW (push button) uses INPUT_PULLUP — reads LOW when pressed.
- Not a potentiometer — outputs quadrature pulses for rotation direction.
- Library: `BasicEncoder` — call `encoder.service()` from interrupt handler.

---

## Water Level Sensor (Power-Gated)

```
GPIO 7 (power) ──── + (sensor power)
         GND  ──── - (sensor ground)
          A0  ──── S (analog signal)
```

- Power the sensor ONLY during reads to prevent corrosion.
- Use a digital pin to gate power: HIGH before read, LOW after.
- `analogRead()` returns higher values with more water contact.
- Same pattern works for any corrosion-prone sensor.

---

## IR Receiver Module (KY-022)

```
GPIO 11 ──── S (signal)
     5V ──── VCC (center pin)
    GND ──── -
```

- 38 KHz demodulated output — just `digitalRead()` or use IRremote library.
- Point remote directly at receiver, 1-5 meter range.
- Each remote button sends a unique hex code — read codes with `IrReceiver.decode()`.
- Library: `IRremote` by shirriff/z3t0/ArminJo (v3.8.0+).

---

## Joystick Module (KY-023)

```
  5V ──── 5V
 GND ──── GND
  A0 ──── VRx (X axis)
  A1 ──── VRy (Y axis)
   2 ──── SW  (button)
```

- Two analog axes (0-1023, center ~512) + one digital button.
- Button is active LOW — use `INPUT_PULLUP` and `digitalWrite(pin, HIGH)`.
- Same analog read pattern as a potentiometer on each axis.

---

## LCD1602 (Parallel Mode, Simplified)

```
LCD Pin:  VSS  VDD  V0   RS   RW   E    D4   D5   D6   D7   A    K
Arduino:  GND  5V   (*)  12   GND  11   2    3    4    5    3.3V GND

(*) V0 = contrast. Connect to GND for max contrast, or use potentiometer.
```

- 4-bit mode: only D4-D7 used (saves 4 pins vs 8-bit mode).
- RW tied to GND (write-only mode).
- Backlight: A (anode) to 3.3V works without resistor for dimmer but safe operation.
- Library: `LiquidCrystal` (built-in).

---

## Stepper Motor (28BYJ-48 via ULN2003)

```
Arduino:        ULN2003 Driver:
   8  ─────────── IN1
   10 ─────────── IN3    ← Note: NOT sequential!
   9  ─────────── IN2
   11 ─────────── IN4

External Power:
   5V ─────────── +
  GND ─────────── -
```

- Pin order is IN1-IN3-IN2-IN4 (not IN1-IN2-IN3-IN4) for correct step sequence.
- 2038 steps per full revolution (full-step mode).
- External 5V power recommended — motor draws too much for USB alone.
- Library: `Stepper` (built-in). Constructor: `Stepper(2038, 8, 10, 9, 11)`.

---

## RFID Reader (RC522 via SPI)

```
Arduino Mega:     RC522:
      53 ─────── SDA (SS)
      52 ─────── SCK
      51 ─────── MOSI
      50 ─────── MISO
      26 ─────── RST    (configurable)
    3.3V ─────── VCC    ← MUST be 3.3V, NOT 5V
     GND ─────── GND
```

- MUST use 3.3V power — 5V will damage the module.
- RST and SS pins are configurable in software.
- SPI interface — uses hardware SPI pins on Mega (50-53).
- Library: `MFRC522` by miguelbalboa.

---

## Accelerometer/Gyroscope (MPU-6050 via I2C)

```
Arduino Mega:     GY-521:
      20 ─────── SDA
      21 ─────── SCL
      5V ─────── VCC
     GND ─────── GND
```

- I2C address 0x68 (default). Conflicts with DS3231 — set AD0 HIGH for 0x69.
- Onboard voltage regulator accepts 3.3V or 5V.
- Initialize by writing 0 to register 0x6B (wake up from sleep).
- Raw data: 7 registers × 2 bytes = 14 bytes per read (accel XYZ, temp, gyro XYZ).
