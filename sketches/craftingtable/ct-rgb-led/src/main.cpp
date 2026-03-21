#include <Arduino.h>

// Pin assignments — must match wiring.yaml
// RGB LED: 4 pins — Red, Common GND (longest), Green, Blue
constexpr int RED_PIN   = 7;
constexpr int GREEN_PIN = 6;
constexpr int BLUE_PIN  = 5;

void setColor(int r, int g, int b);

void setup() {
  pinMode(RED_PIN,   OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN,  OUTPUT);
}

void loop() {
  setColor(255, 0, 0);       // Red
  delay(1000);
  setColor(0, 255, 0);       // Green
  delay(1000);
  setColor(0, 0, 255);       // Blue
  delay(1000);
  setColor(255, 255, 255);   // White
  delay(1000);
  setColor(170, 0, 255);     // Purple
  delay(1000);
}

void setColor(int r, int g, int b) {
  analogWrite(RED_PIN,   r);
  analogWrite(GREEN_PIN, g);
  analogWrite(BLUE_PIN,  b);
}
