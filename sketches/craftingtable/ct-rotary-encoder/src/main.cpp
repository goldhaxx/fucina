#include <Arduino.h>
#include <BasicEncoder.h>

// Pin assignments — must match wiring.yaml
// CLK and DT must be on interrupt-capable pins
constexpr int CLK_PIN = 2;   // INT0
constexpr int DT_PIN  = 3;   // INT1
constexpr int SW_PIN  = 18;  // INT5

BasicEncoder encoder(CLK_PIN, DT_PIN);

void updateEncoder();
void updateSwitch();

void setup() {
  pinMode(SW_PIN, INPUT_PULLUP);
  Serial.begin(115200);
  delay(1000);
  Serial.println("Rotary Encoder ready");
  Serial.print("Counter: ");
  Serial.println(encoder.get_count());

  attachInterrupt(digitalPinToInterrupt(CLK_PIN), updateEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(DT_PIN), updateEncoder, CHANGE);
}

void loop() {
  if (encoder.get_change()) {
    Serial.print("Counter: ");
    Serial.println(encoder.get_count());
  }
}

void updateEncoder() {
  encoder.service();
}

void updateSwitch() {
  // Debounce handled by interrupt timing
  if (digitalRead(SW_PIN) == LOW) {
    Serial.println("SWITCH PRESSED");
  } else {
    Serial.println("SWITCH RELEASED");
  }
}
