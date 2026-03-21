#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr int LED_PIN    = 22;
constexpr int SENSOR_PIN = A8;

// Calibration: sensor reads ~540 when dry, ~800 when wet
constexpr int DRY_THRESHOLD = 540;
constexpr int WET_MAX       = 800;

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  unsigned int sensorValue = analogRead(SENSOR_PIN);

  if (sensorValue < DRY_THRESHOLD) return;

  // Map sensor range to LED brightness (0-255)
  uint8_t brightness = map(sensorValue, DRY_THRESHOLD, WET_MAX, 0, 255);

  Serial.print(sensorValue);
  Serial.print(" ");
  Serial.println(brightness);

  analogWrite(LED_PIN, brightness);
}
