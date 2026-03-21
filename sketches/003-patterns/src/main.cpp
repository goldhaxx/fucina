#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr uint8_t LED_RED    = 9;
constexpr uint8_t LED_GREEN  = 10;
constexpr uint8_t LED_BLUE   = 11;
constexpr uint8_t LED_WHITE  = 5;
constexpr uint8_t LED_YELLOW = 6;

constexpr uint8_t LED_PINS[] = {LED_RED, LED_GREEN, LED_BLUE, LED_WHITE, LED_YELLOW};
constexpr uint8_t NUM_LEDS   = sizeof(LED_PINS) / sizeof(LED_PINS[0]);

// Pattern IDs
constexpr uint8_t PAT_CHASE   = 1;
constexpr uint8_t PAT_BLINK   = 2;
constexpr uint8_t PAT_TWINKLE = 3;
constexpr uint8_t PAT_CYCLE   = 4;

uint8_t currentPattern = PAT_CHASE;

// ─── Helpers ─────────────────────────────────────────────────────

void allOff() {
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    digitalWrite(LED_PINS[i], LOW);
  }
}

void printMenu() {
  Serial.println();
  Serial.println(F("=== 003 - LED Patterns ==="));
  Serial.println(F("1: Sequential Chase"));
  Serial.println(F("2: All Blink"));
  Serial.println(F("3: Random Twinkle"));
  Serial.println(F("4: Pattern Cycle"));
  Serial.print(F("Active: "));
  Serial.println(currentPattern);
  Serial.println(F("Send 1-4 to switch."));
}

// Check serial for pattern switch. Returns true if pattern changed.
bool checkSerial() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c >= '1' && c <= '4') {
      allOff();
      currentPattern = c - '0';
      printMenu();
      return true;
    }
  }
  return false;
}

// ─── Pattern 1: Sequential Chase ─────────────────────────────────
// LEDs light one at a time, sweeping left-to-right then bouncing back.

void chase() {
  // Forward sweep
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    allOff();
    digitalWrite(LED_PINS[i], HIGH);
    delay(120);
    if (checkSerial()) return;
  }
  // Bounce back (skip endpoints to avoid double-flash)
  for (int8_t i = NUM_LEDS - 2; i > 0; i--) {
    allOff();
    digitalWrite(LED_PINS[i], HIGH);
    delay(120);
    if (checkSerial()) return;
  }
}

// ─── Pattern 2: All Blink ────────────────────────────────────────
// All 5 LEDs blink on and off together.

void blinkAll() {
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    digitalWrite(LED_PINS[i], HIGH);
  }
  delay(400);
  if (checkSerial()) return;

  allOff();
  delay(400);
  checkSerial();
}

// ─── Pattern 3: Random Twinkle ──────────────────────────────────
// Random LEDs flicker on and off like stars.

void twinkle() {
  uint8_t idx = random(NUM_LEDS);
  digitalWrite(LED_PINS[idx], HIGH);
  delay(50 + random(100));
  digitalWrite(LED_PINS[idx], LOW);
  delay(30 + random(80));
  checkSerial();
}

// ─── Pattern 4: Pattern Cycle ───────────────────────────────────
// Runs each of patterns 1-3 for 5 seconds, then rotates.

void patternCycle() {
  static uint8_t sub = PAT_CHASE;
  unsigned long start = millis();

  while (millis() - start < 5000) {
    switch (sub) {
      case PAT_CHASE:   chase();    break;
      case PAT_BLINK:   blinkAll(); break;
      case PAT_TWINKLE: twinkle();  break;
    }
    // Exit immediately if user switched away from cycle mode
    if (currentPattern != PAT_CYCLE) return;
  }

  sub = (sub % 3) + 1;  // rotate 1 → 2 → 3 → 1 ...
}

// ─── Setup & Loop ───────────────────────────────────────────────

void setup() {
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    pinMode(LED_PINS[i], OUTPUT);
  }
  Serial.begin(9600);
  randomSeed(analogRead(A0));  // seed from floating analog pin
  printMenu();
}

void loop() {
  switch (currentPattern) {
    case PAT_CHASE:   chase();        break;
    case PAT_BLINK:   blinkAll();     break;
    case PAT_TWINKLE: twinkle();      break;
    case PAT_CYCLE:   patternCycle(); break;
  }
}
