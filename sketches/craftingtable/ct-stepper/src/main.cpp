#include <Arduino.h>
#include <Stepper.h>

// Motor specs
constexpr int STEPS_PER_REV = 2038;

// Pin assignments — must match wiring.yaml
// IMPORTANT: Pin order is IN1-IN3-IN2-IN4 (not sequential!)
// This matches the ULN2003 driver's expected step sequence.
Stepper myStepper(STEPS_PER_REV, 8, 10, 9, 11);

void setup() {
  // Nothing to set up — Stepper library handles pin modes
}

void loop() {
  // Rotate one full revolution clockwise at 5 RPM
  myStepper.setSpeed(5);
  myStepper.step(STEPS_PER_REV);
  delay(1000);

  // Rotate one full revolution counter-clockwise at 10 RPM
  myStepper.setSpeed(10);
  myStepper.step(-STEPS_PER_REV);
  delay(1000);
}
