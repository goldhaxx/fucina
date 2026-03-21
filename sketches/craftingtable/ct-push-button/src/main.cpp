#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr byte BUTTON_PIN = 12;

// Serial config
constexpr unsigned long BAUD_RATE = 9600;

// Plot bounds for Serial Plotter
constexpr int PLOT_MIN = -1;
constexpr int PLOT_MAX = 2;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(BAUD_RATE);
}

void loop() {
  Serial.print("button:");
  Serial.print(digitalRead(BUTTON_PIN));
  Serial.print(" minimum:");
  Serial.print(PLOT_MIN);
  Serial.print(" maximum:");
  Serial.println(PLOT_MAX);
}
