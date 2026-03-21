#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr int DIGITAL_PIN = 2;
constexpr int ANALOG_PIN  = A0;

int peakLevel = 0;

void setup() {
  pinMode(DIGITAL_PIN, INPUT);
  Serial.begin(115200);
}

void loop() {
  int digitalValue = digitalRead(DIGITAL_PIN);
  int analogValue  = analogRead(ANALOG_PIN);

  if (analogValue > peakLevel) {
    peakLevel = min(analogValue, 100);
  }

  Serial.print(digitalValue);
  Serial.print(", ");
  Serial.print(analogValue);
  Serial.print(", ");
  Serial.println(peakLevel);
  delay(1);
}
