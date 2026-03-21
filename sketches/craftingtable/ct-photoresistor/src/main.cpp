#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr int SENSOR_PIN = A0;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  int sensorValue = analogRead(SENSOR_PIN);
  Serial.println(sensorValue);

  // Blink the onboard LED at a rate proportional to light level
  digitalWrite(LED_BUILTIN, HIGH);
  delay(sensorValue);
  digitalWrite(LED_BUILTIN, LOW);
  delay(sensorValue);
}
