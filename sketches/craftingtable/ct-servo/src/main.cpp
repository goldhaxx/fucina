#include <Arduino.h>
#include <Servo.h>

// Pin assignments — must match wiring.yaml
constexpr int SERVO_PIN = 9;

Servo myServo;

void setup() {
  myServo.attach(SERVO_PIN);
}

void loop() {
  // Sweep from 0° to 180°
  for (int angle = 0; angle < 180; angle++) {
    myServo.write(angle);
    delay(15);
  }
  // Sweep back from 180° to 0°
  for (int angle = 180; angle > 0; angle--) {
    myServo.write(angle);
    delay(15);
  }
}
