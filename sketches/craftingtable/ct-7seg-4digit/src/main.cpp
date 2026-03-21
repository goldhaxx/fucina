#include <Arduino.h>
#include <SevSeg.h>

SevSeg sevseg;

void setup() {
  byte numDigits = 4;
  byte digitPins[] = {2, 3, 4, 5};
  byte segmentPins[] = {6, 7, 8, 9, 10, 11, 12, 13};
  sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins);
}

void loop() {
  static unsigned long timer = millis();
  static int deciSeconds = 0;

  if (millis() >= timer) {
    deciSeconds++;
    timer += 100;
    if (deciSeconds == 10000) deciSeconds = 0;
    sevseg.setNumber(deciSeconds, 1);
  }
  sevseg.refreshDisplay();
}
