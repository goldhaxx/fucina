#include <Arduino.h>
#include <Wire.h>
#include <DS3231.h>
#include <LibPrintf.h>

RTClib myRTC;
DS3231 setRTC;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Wire.begin();
  delay(500);
  printf("DS3231 Real-Time Clock\n");
  printf("To set time, enter YYMMDDwHHMMSS via serial\n");
}

void loop() {
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

  DateTime now = myRTC.now();
  printf("%04d/%02d/%02d %02d:%02d:%02d\n",
    now.year(), now.month(), now.day(),
    now.hour(), now.minute(), now.second());
  delay(5000);
}
