#include <Arduino.h>

// Pin assignments — must match wiring.yaml
constexpr int SOUND_ANALOG  = A0;
constexpr int SOUND_DIGITAL = 2;
constexpr int LED_PIN       = LED_BUILTIN;  // Pin 13, onboard LED

bool ledState = false;

void setup() {
  Serial.begin(9600);
  pinMode(SOUND_ANALOG, INPUT);
  pinMode(SOUND_DIGITAL, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int sensorData = analogRead(SOUND_ANALOG);
  Serial.print("Sound = ");
  Serial.println(sensorData);

  int sound = digitalRead(SOUND_DIGITAL);

  if (sound == HIGH) {
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState ? HIGH : LOW);
    delay(500);  // Debounce — ignore follow-up triggers
  }
}
