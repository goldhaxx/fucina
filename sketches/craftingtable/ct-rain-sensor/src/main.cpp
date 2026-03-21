#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr byte WATER_PIN = A0;
constexpr byte POWER_PIN = 7;

int readSensor();

void setup() {
  pinMode(WATER_PIN, INPUT);
  pinMode(POWER_PIN, OUTPUT);
  digitalWrite(POWER_PIN, LOW);
  Serial.begin(115200);
}

void loop() {
  int waterLevel = readSensor();
  Serial.print("Water level: ");
  Serial.println(waterLevel);
  delay(1000);
}

// Power the sensor only during reads to prevent corrosion
int readSensor() {
  digitalWrite(POWER_PIN, HIGH);
  delay(10);
  int val = analogRead(WATER_PIN);
  digitalWrite(POWER_PIN, LOW);
  return val;
}
