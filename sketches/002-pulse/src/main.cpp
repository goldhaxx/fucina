#include <Arduino.h>

constexpr uint8_t LED_PIN = 9;
constexpr uint8_t STEP_DELAY_MS = 10;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // Fade up: 0 → 255
  for (int brightness = 0; brightness <= 255; brightness++) {
    analogWrite(LED_PIN, brightness);
    delay(STEP_DELAY_MS);
  }

  // Fade down: 255 → 0
  for (int brightness = 255; brightness >= 0; brightness--) {
    analogWrite(LED_PIN, brightness);
    delay(STEP_DELAY_MS);
  }
}
