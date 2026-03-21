#include <Arduino.h>
#include <Wire.h>
#include <DS3231.h>
#include <LibPrintf.h>
#include <SevSeg.h>

// Pin assignments — must match wiring.yaml
constexpr int BUZZER_PIN = 45;

// Alarm time (24-hour format)
constexpr int ALARM_HOUR   = 10;
constexpr int ALARM_MINUTE = 11;

DS3231 setRTC;
RTClib myRTC;
SevSeg sevseg;

void alarmBuzzer();

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Wire.begin();
  delay(500);

  // Initialize 7-segment display
  byte numDigits = 4;
  byte digitPins[] = {2, 3, 4, 5};
  byte segmentPins[] = {6, 7, 8, 9, 10, 11, 12, 13};
  bool resistorsOnSegments = false;
  sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins, resistorsOnSegments, false, true);
  sevseg.setBrightness(100);

  pinMode(BUZZER_PIN, OUTPUT);

  printf("Alarm Clock — set to %02d:%02d\n", ALARM_HOUR, ALARM_MINUTE);
  printf("To set time, enter YYMMDDwHHMMSS via serial\n");
}

void loop() {
  // Handle serial time-setting
  if (Serial.available()) {
    String newDate = Serial.readStringUntil('\r');
    newDate.trim();
    if (newDate.length() == 13) {
      int year, month, day, dOW, hour, minute, second;
      sscanf(newDate.c_str(), "%2d%2d%2d%1d%2d%2d%2d",
             &year, &month, &day, &dOW, &hour, &minute, &second);
      if (month <= 12 && day <= 31 && hour <= 23 && minute <= 59 && second <= 59) {
        setRTC.setClockMode(false);
        setRTC.setYear(year);
        setRTC.setMonth(month);
        setRTC.setDate(day);
        setRTC.setDoW(dOW);
        setRTC.setHour(hour);
        setRTC.setMinute(minute);
        setRTC.setSecond(second);
        printf("Time set!\n");
      }
    }
  }

  // Read current time
  DateTime now = myRTC.now();
  int displayTime = (now.hour() * 100) + now.minute();
  sevseg.setNumber(displayTime);
  sevseg.refreshDisplay();

  // Check alarm
  if (now.hour() == ALARM_HOUR && now.minute() == ALARM_MINUTE) {
    alarmBuzzer();
  } else {
    digitalWrite(BUZZER_PIN, LOW);
  }
}

void alarmBuzzer() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);
    digitalWrite(BUZZER_PIN, LOW);
    delay(200);
  }
}
