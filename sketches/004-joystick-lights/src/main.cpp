#include <Arduino.h>

// ─── Pin assignments — must match wiring.yaml ───────────────────

// LEDs (all PWM-capable)
constexpr uint8_t LED_RED    = 9;
constexpr uint8_t LED_GREEN  = 10;
constexpr uint8_t LED_BLUE   = 11;
constexpr uint8_t LED_WHITE  = 5;
constexpr uint8_t LED_YELLOW = 6;

constexpr uint8_t LED_PINS[] = {LED_RED, LED_GREEN, LED_BLUE, LED_WHITE, LED_YELLOW};
constexpr uint8_t NUM_LEDS   = sizeof(LED_PINS) / sizeof(LED_PINS[0]);

// Joystick (HW-504)
constexpr uint8_t JOY_X_PIN  = A0;   // VRx — left/right
constexpr uint8_t JOY_Y_PIN  = A1;   // VRy — up/down
constexpr uint8_t JOY_SW_PIN = 2;    // push button

// ─── Joystick calibration ──────────────────────────────────────

// Calibrated at startup by reading resting position
int joyCenterX = 512;
int joyCenterY = 512;

constexpr int JOY_DEADZONE = 60;     // ±60 around calibrated center
constexpr int ZONE_HYSTERESIS = 20;  // extra margin to leave a zone

enum Zone { ZONE_CENTER, ZONE_RIGHT, ZONE_LEFT, ZONE_UP, ZONE_DOWN };

Zone currentZone    = ZONE_CENTER;
Zone previousZone   = ZONE_CENTER;
float deflection    = 0.0;          // 0.0–1.0 magnitude

// ─── Effect state ───────────────────────────────────────────────

unsigned long lastStep = 0;
int8_t chaseIndex = 0;
uint8_t twinkleBrightness[NUM_LEDS];
int8_t rippleRing   = 0;
uint8_t rippleFade  = 0;
uint16_t pulsePhase = 0;

// Debug timing
unsigned long lastDebugPrint = 0;

// ─── Helpers ────────────────────────────────────────────────────

void allOff() {
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    analogWrite(LED_PINS[i], 0);
  }
}

uint8_t triangleWave(uint16_t phase) {
  if (phase < 512) {
    return phase / 2;
  }
  return (1023 - phase) / 2;
}

// ─── Joystick Calibration ──────────────────────────────────────

void calibrateJoystick() {
  // Average 32 readings over ~500ms to find the resting center
  long sumX = 0, sumY = 0;
  constexpr int SAMPLES = 32;

  Serial.print(F("Calibrating joystick (don't touch)... "));

  for (int i = 0; i < SAMPLES; i++) {
    sumX += analogRead(JOY_X_PIN);
    sumY += analogRead(JOY_Y_PIN);
    delay(15);
  }

  joyCenterX = sumX / SAMPLES;
  joyCenterY = sumY / SAMPLES;

  Serial.print(F("center X="));
  Serial.print(joyCenterX);
  Serial.print(F(" Y="));
  Serial.println(joyCenterY);
}

// ─── Joystick Reading ───────────────────────────────────────────

void readJoystick() {
  int rawX = analogRead(JOY_X_PIN);
  int rawY = analogRead(JOY_Y_PIN);

  int dx = rawX - joyCenterX;
  int dy = rawY - joyCenterY;
  int absDx = abs(dx);
  int absDy = abs(dy);

  // Compute the max possible deflection from center to rail (0 or 1023)
  int maxRangeX = max(joyCenterX, 1023 - joyCenterX);
  int maxRangeY = max(joyCenterY, 1023 - joyCenterY);

  previousZone = currentZone;

  // Use hysteresis: need more deflection to ENTER a zone than to STAY in it
  int enterThreshold = JOY_DEADZONE + ZONE_HYSTERESIS;
  int exitThreshold  = JOY_DEADZONE;

  bool inDeadZone;
  if (currentZone == ZONE_CENTER) {
    // Must exceed enter threshold to leave center
    inDeadZone = (absDx <= enterThreshold && absDy <= enterThreshold);
  } else {
    // Only return to center if within exit threshold
    inDeadZone = (absDx <= exitThreshold && absDy <= exitThreshold);
  }

  if (inDeadZone) {
    currentZone = ZONE_CENTER;
    deflection = 0.0;
    return;
  }

  // Dominant axis wins
  if (absDx >= absDy) {
    currentZone = (dx > 0) ? ZONE_LEFT : ZONE_RIGHT;
    deflection = constrain((float)(absDx - JOY_DEADZONE) / (float)(maxRangeX - JOY_DEADZONE), 0.0, 1.0);
  } else {
    currentZone = (dy > 0) ? ZONE_DOWN : ZONE_UP;
    deflection = constrain((float)(absDy - JOY_DEADZONE) / (float)(maxRangeY - JOY_DEADZONE), 0.0, 1.0);
  }

  // Periodic raw value debug output
  unsigned long now = millis();
  if (now - lastDebugPrint >= 500) {
    lastDebugPrint = now;
    Serial.print(F("raw X="));
    Serial.print(rawX);
    Serial.print(F(" Y="));
    Serial.print(rawY);
    Serial.print(F("  dx="));
    Serial.print(dx);
    Serial.print(F(" dy="));
    Serial.print(dy);
    Serial.print(F("  zone="));
    const char* zoneNames[] = {"CENTER", "RIGHT", "LEFT", "UP", "DOWN"};
    Serial.print(zoneNames[currentZone]);
    Serial.print(F("  defl="));
    Serial.println(deflection, 2);
  }
}

// ─── Effect: Sync Pulse (center) ────────────────────────────────

void effectPulse() {
  unsigned long now = millis();
  if (now - lastStep >= 2) {
    lastStep = now;
    pulsePhase = (pulsePhase + 1) & 1023;
  }

  uint8_t brightness = triangleWave(pulsePhase);
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    analogWrite(LED_PINS[i], brightness);
  }
}

// ─── Effect: Sequential Chase (left/right) ──────────────────────

void effectChase() {
  unsigned long now = millis();
  unsigned long interval = 200 - (uint16_t)(deflection * 160);

  if (now - lastStep >= interval) {
    lastStep = now;
    analogWrite(LED_PINS[chaseIndex], 0);

    if (currentZone == ZONE_RIGHT) {
      chaseIndex++;
      if (chaseIndex >= NUM_LEDS) chaseIndex = 0;
    } else {
      chaseIndex--;
      if (chaseIndex < 0) chaseIndex = NUM_LEDS - 1;
    }

    analogWrite(LED_PINS[chaseIndex], 255);
  }
}

// ─── Effect: Random Twinkle (up) ────────────────────────────────

void effectTwinkle() {
  unsigned long now = millis();
  // Cubic curve: gentle at low deflection, severe at high
  float curve = deflection * deflection * deflection;
  unsigned long interval = 200 - (uint16_t)(curve * 192);  // 200ms → 8ms

  if (now - lastStep >= interval) {
    lastStep = now;

    // At high deflection, hit more LEDs per tick for frenetic effect
    uint8_t changes = 1 + (uint8_t)(curve * 4);  // 1 at low → 5 at max
    for (uint8_t c = 0; c < changes; c++) {
      uint8_t idx = random(NUM_LEDS);
      twinkleBrightness[idx] = random(256);
      analogWrite(LED_PINS[idx], twinkleBrightness[idx]);
    }

    // Rapid dimming at high intensity
    uint8_t dimIdx = random(NUM_LEDS);
    uint8_t dimAmount = 20 + (uint8_t)(curve * 80);  // 20 → 100
    if (twinkleBrightness[dimIdx] > dimAmount) {
      twinkleBrightness[dimIdx] -= dimAmount;
    } else {
      twinkleBrightness[dimIdx] = 0;
    }
    analogWrite(LED_PINS[dimIdx], twinkleBrightness[dimIdx]);
  }
}

// ─── Effect: Ripple (down) ──────────────────────────────────────

void effectRipple() {
  unsigned long now = millis();
  // Cubic curve: gentle at low deflection, severe at high
  float curve = deflection * deflection * deflection;
  unsigned long interval = 150 - (uint16_t)(curve * 142);  // 150ms → 8ms

  // Faster fade steps at high intensity (bigger jumps = faster waves)
  uint8_t fadeStep = 25 + (uint8_t)(curve * 60);  // 25 → 85

  if (now - lastStep >= interval) {
    lastStep = now;

    rippleFade += fadeStep;
    if (rippleFade < fadeStep) {  // overflow = next ring
      rippleFade = 0;
      rippleRing++;
      if (rippleRing > 2) {
        rippleRing = 0;
        allOff();
      }
    }

    uint8_t brightness = rippleFade;
    // At high deflection, boost brightness to full
    if (curve > 0.5) {
      brightness = (uint8_t)min(255, (int)rippleFade + (int)(curve * 100));
    }

    // Clear all then light the active ring
    for (uint8_t i = 0; i < NUM_LEDS; i++) {
      analogWrite(LED_PINS[i], 0);
    }

    constexpr uint8_t CENTER = 2;
    switch (rippleRing) {
      case 0:
        analogWrite(LED_PINS[CENTER], brightness);
        break;
      case 1:
        analogWrite(LED_PINS[CENTER - 1], brightness);
        analogWrite(LED_PINS[CENTER + 1], brightness);
        analogWrite(LED_PINS[CENTER], brightness / 3);
        break;
      case 2:
        analogWrite(LED_PINS[0], brightness);
        analogWrite(LED_PINS[4], brightness);
        analogWrite(LED_PINS[CENTER - 1], brightness / 3);
        analogWrite(LED_PINS[CENTER + 1], brightness / 3);
        break;
    }
  }
}

// ─── Zone Transition ────────────────────────────────────────────

void onZoneChange() {
  allOff();
  lastStep = millis();

  chaseIndex = 0;
  pulsePhase = 0;
  rippleRing = 0;
  rippleFade = 0;

  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    twinkleBrightness[i] = 0;
  }

  const char* zoneNames[] = {"CENTER", "RIGHT", "LEFT", "UP", "DOWN"};
  Serial.print(F(">> Zone: "));
  Serial.print(zoneNames[currentZone]);
  Serial.print(F("  deflection: "));
  Serial.println(deflection, 2);
}

// ─── Setup & Loop ───────────────────────────────────────────────

void setup() {
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    pinMode(LED_PINS[i], OUTPUT);
  }

  pinMode(JOY_SW_PIN, INPUT_PULLUP);

  Serial.begin(9600);
  randomSeed(analogRead(A2));

  Serial.println(F("=== 004 — Joystick Lights ==="));

  calibrateJoystick();

  Serial.println(F("Ready. Move joystick to control LEDs:"));
  Serial.println(F("  Center : sync pulse"));
  Serial.println(F("  Right  : chase right"));
  Serial.println(F("  Left   : chase left"));
  Serial.println(F("  Up     : random twinkle"));
  Serial.println(F("  Down   : ripple from center"));
}

void loop() {
  readJoystick();

  if (currentZone != previousZone) {
    onZoneChange();
  }

  switch (currentZone) {
    case ZONE_CENTER: effectPulse();   break;
    case ZONE_RIGHT:  effectChase();   break;
    case ZONE_LEFT:   effectChase();   break;
    case ZONE_UP:     effectTwinkle(); break;
    case ZONE_DOWN:   effectRipple();  break;
  }
}
