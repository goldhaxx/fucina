#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr byte BUZZER_PIN = 2;

// Timing
constexpr unsigned long ON_LENGTH  = 1000;
constexpr unsigned long OFF_LENGTH = 1000;

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  digitalWrite(BUZZER_PIN, HIGH);
  delay(ON_LENGTH);
  digitalWrite(BUZZER_PIN, LOW);
  delay(OFF_LENGTH);
}
