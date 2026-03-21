# Accelerometer/Gyroscope — MPU-6050

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 160

Reads 3-axis accelerometer, 3-axis gyroscope, and temperature from the GY-521 (MPU-6050) module via I2C. Raw sensor values print to the serial monitor at 115200 baud once per second.

> **I2C address conflict:** The MPU-6050 defaults to address 0x68, which is the same as the DS3231 RTC module. If you need both on the same I2C bus, set the MPU-6050's AD0 pin HIGH to shift it to 0x69.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-gyroscope/wiring.yaml -o sketches/craftingtable/ct-gyroscope/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x GY-521 MPU-6050 accelerometer/gyroscope module
- 4x jumper wires (male-to-female or male-to-male depending on header)

## Step-by-Step Wiring

### 1. Place the GY-521 module

Insert the module's header pins into the breadboard starting at row 10. The module has pins labeled VCC, GND, SCL, SDA, XDA, XCL, AD0, and INT. Only the first four are needed for this sketch.

### 2. Connect jumper wires

- **Wire 1 (red — power):** From **a10** (VCC row) to **5V** on the HERO XL
- **Wire 2 (black — ground):** From **a11** (GND row) to **GND** on the HERO XL
- **Wire 3 (blue — SDA):** From **a12** (SDA row) to **Pin 20** on the HERO XL
- **Wire 4 (green — SCL):** From **a13** (SCL row) to **Pin 21** on the HERO XL

### 3. Electrical path

```
HERO XL 5V   → GY-521 VCC (onboard regulator handles 3.3V conversion)
HERO XL GND  → GY-521 GND
HERO XL Pin 20 (SDA) → GY-521 SDA
HERO XL Pin 21 (SCL) → GY-521 SCL
```

The GY-521 module has an onboard voltage regulator and level shifter, so it accepts 5V power and I2C signals from the Mega without an external logic level converter.

## Build and Upload

```bash
cd sketches/craftingtable/ct-gyroscope
pio run -e mega -t upload
```

Open the serial monitor at 115200 baud:
```bash
pio device monitor -b 115200
```

You should see lines like:
```
aX=1234 aY=-456 aZ=16384 tmp=25.12 gX=100 gY=-50 gZ=30
```

Tilt or rotate the module and watch the values change in real time.

## What to Try Next

- Calculate tilt angles from accelerometer data using `atan2()`
- Build a motion alarm that triggers a buzzer when movement exceeds a threshold
- Combine with the LCD1602 or TTGO T-Display to show orientation graphically
- Use a complementary filter to fuse accelerometer and gyroscope data for stable angle readings
