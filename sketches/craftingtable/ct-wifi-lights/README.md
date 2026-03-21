# WiFi Lights — ESP32 Access Point

**Board:** TTGO T-Display ESP32
**Source:** Crafting Table course — Chapter 05 (Spy vs Spy)

Creates a WiFi access point named "HomeLights" with a built-in web server. Connect from your phone or computer, browse to 192.168.4.1, and tap buttons to turn an LED on GPIO 2 on and off.

This is the first ESP32 sketch in the collection. All ESP32 GPIO is 3.3V — do not connect 5V signals directly.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-wifi-lights/wiring.yaml -o sketches/craftingtable/ct-wifi-lights/wiring.svg
```

## Parts

- TTGO T-Display ESP32 board + USB-C cable
- 830-point breadboard
- 2x jumper wires

## Step-by-Step

### 1. Connect jumper wires

- **Wire 1 (signal — green):** From **a10** to **GPIO 2** on the ESP32
- **Wire 2 (ground — black):** From **a11** to **GND** on the ESP32

GPIO 2 is safe to use on the ESP32 — no boot conflicts and it also drives the onboard LED on many ESP32 boards.

### 2. Upload the sketch

```bash
cd sketches/craftingtable/ct-wifi-lights
pio run -e esp32 -t upload
pio device monitor
```

### 3. Connect to the WiFi network

1. Open WiFi settings on your phone or computer
2. Connect to the network named **HomeLights** (open, no password)
3. Open a browser and go to **http://192.168.4.1**
4. Tap **Turn On** or **Turn Off** to control the LED

The serial monitor will show connection events and HTTP requests as they arrive.

### 4. How it works

The ESP32 creates a software access point (soft AP) — it acts as both the WiFi router and the web server. No external router or internet connection is needed. The default AP IP is always 192.168.4.1.

When a client requests `/H`, the LED turns on. When it requests `/L`, the LED turns off. The HTML page provides two buttons that link to those paths.

## Build and Upload

```bash
cd sketches/craftingtable/ct-wifi-lights
pio run -e esp32 -t upload
pio device monitor
```

## What to Try Next

- Add a password to the access point (`WiFi.softAP(ssid, "yourpassword")`)
- Control multiple pins — add more buttons for different GPIOs
- Show the current LED state on the web page (on/off indicator)
- Display connection status and IP address on the built-in TFT screen using TFT_eSPI
