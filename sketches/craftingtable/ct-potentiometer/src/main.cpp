#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr byte ANALOG_PIN = A0;

// Serial config
constexpr unsigned long BAUD_RATE = 9600;

// Plot bounds for Serial Plotter
constexpr int PLOT_MIN = 0;
constexpr int PLOT_MAX = 1023;

void setup() {
  Serial.begin(BAUD_RATE);
}

void loop() {
  Serial.print("potentiometer:");
  Serial.print(analogRead(ANALOG_PIN));
  Serial.print(" minimum:");
  Serial.print(PLOT_MIN);
  Serial.print(" maximum:");
  Serial.println(PLOT_MAX);
}
