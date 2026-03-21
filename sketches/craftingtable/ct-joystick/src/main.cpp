#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr int SW_PIN = 2;
constexpr int X_PIN  = A0;
constexpr int Y_PIN  = A1;

void setup() {
  pinMode(SW_PIN, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  Serial.print("Switch: ");
  Serial.print(digitalRead(SW_PIN));
  Serial.print("  X-axis: ");
  Serial.print(analogRead(X_PIN));
  Serial.print("  Y-axis: ");
  Serial.println(analogRead(Y_PIN));
  delay(500);
}
