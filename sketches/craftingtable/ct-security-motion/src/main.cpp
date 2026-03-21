#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr int FLOOD_LIGHTS  = 22;
constexpr int MOTION_SENSOR = 23;

void setup() {
  pinMode(MOTION_SENSOR, INPUT);
  pinMode(FLOOD_LIGHTS, OUTPUT);
  Serial.begin(9600);
  Serial.println("PIR warming up... (wait ~1 minute)");
}

void loop() {
  bool motion_detected = digitalRead(MOTION_SENSOR);
  if (motion_detected) {
    digitalWrite(FLOOD_LIGHTS, HIGH);
  } else {
    digitalWrite(FLOOD_LIGHTS, LOW);
  }
}
