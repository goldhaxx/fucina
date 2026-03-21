#include <Arduino.h>
#include <SevSeg.h>

SevSeg sevseg;

int counter = 0;

void setup() {
  byte numDigits = 1;
  byte digitPins[] = {};
  byte segmentPins[] = {2, 3, 4, 5, 6, 7, 8, 9};
  bool resistorsOnSegments = true;
  sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins, resistorsOnSegments);
  sevseg.setBrightness(90);
}

void loop() {
  if (++counter > 9) counter = 0;
  sevseg.setNumber(counter);
  sevseg.refreshDisplay();
  delay(1000);
}
