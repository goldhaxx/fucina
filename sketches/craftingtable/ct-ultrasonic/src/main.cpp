#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr uint8_t TRIG_PIN = 13;
constexpr uint8_t ECHO_PIN = 12;

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  Serial.begin(115200);
  Serial.println("Ultrasonic Sensor HC-SR04 Test");
}

void loop() {
  // Send 10us trigger pulse
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Measure echo duration
  long duration = pulseIn(ECHO_PIN, HIGH);

  // Convert to distance
  int distance_cm   = duration * 0.034 / 2;
  int distance_inch = duration * 0.0133 / 2;

  Serial.print("Distance: ");
  Serial.print(distance_cm);
  Serial.print(" cm, ");
  Serial.print(distance_inch);
  Serial.println(" inch");
  delay(200);
}
