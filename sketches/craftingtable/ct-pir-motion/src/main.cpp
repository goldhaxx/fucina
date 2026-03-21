#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr int PIR_PIN = 2;

bool detected = false;

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  Serial.println("PIR Sensor warming up... (wait ~1 minute)");
}

void loop() {
  int pirState = digitalRead(PIR_PIN);

  if (pirState == HIGH && !detected) {
    detected = true;
    Serial.println("Motion Detected!");
  }

  if (pirState == LOW && detected) {
    detected = false;
    Serial.println("All quiet...");
  }
}
