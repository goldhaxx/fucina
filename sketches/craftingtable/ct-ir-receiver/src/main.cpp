#include <Arduino.h>
#include <IRremote.hpp>

// Pin assignments — must match wiring.yaml
constexpr int RECV_PIN = 11;

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("IR Receiver ready — point remote and press buttons");
  IrReceiver.begin(RECV_PIN, ENABLE_LED_FEEDBACK);
}

void loop() {
  if (IrReceiver.decode()) {
    Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX);
    IrReceiver.printIRResultShort(&Serial);
    IrReceiver.resume();
  }
}
