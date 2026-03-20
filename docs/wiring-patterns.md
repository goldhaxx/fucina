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
