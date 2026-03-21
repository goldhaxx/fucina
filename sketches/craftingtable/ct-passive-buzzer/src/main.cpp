#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr byte BUZZER_PIN = 2;

// Tone config
constexpr unsigned int  TONE_PITCH   = 440;   // Hz (A4 note)
constexpr unsigned long TONE_LENGTH  = 1000;   // ms
constexpr unsigned long CYCLE_LENGTH = 2000;   // ms (includes tone duration)

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  tone(BUZZER_PIN, TONE_PITCH, TONE_LENGTH);
  delay(CYCLE_LENGTH);
}
