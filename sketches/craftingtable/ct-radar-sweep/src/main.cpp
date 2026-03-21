#include <Arduino.h>
#include <Servo.h>
#include <MCUFRIEND_kbv.h>

// Pin assignments — must match wiring.yaml
// These pins avoid conflict with the LCD shield (which uses D2-D9, A0-A4)
constexpr uint8_t TRIGGER_PIN = 22;
constexpr uint8_t ECHO_PIN    = 23;
constexpr uint8_t SERVO_PIN   = 24;

MCUFRIEND_kbv tft;
Servo myServo;

long maxDistance = 0;
long displayMaxDistance = 10000;
int scanCount = 0;

void distanceCheck(int direction);
void distancePlot(int x, int y, float degrees, int length);
void drawRanges();

void setup() {
  Serial.begin(9600);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  myServo.attach(SERVO_PIN);

  tft.begin(tft.readID());
  tft.setRotation(0);  // Portrait, upper-left above 9V plug
  drawRanges();

  Serial.println("180-Degree Radar Sweep");
}

void loop() {
  // Uncomment these two lines to calibrate servo (points straight ahead at 90°)
  // myServo.write(90);
  // return;

  // Sweep 0° to 180° in 2° steps
  for (int dir = 0; dir <= 180; dir += 2) {
    myServo.write(dir);
    delay(20);
    distanceCheck(dir);
  }

  // Sweep back 180° to 0°
  for (int dir = 180; dir >= 0; dir -= 2) {
    myServo.write(dir);
    delay(20);
    distanceCheck(dir);
  }

  drawRanges();
  displayMaxDistance = maxDistance;
}

void distanceCheck(int direction) {
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  long rawDistance = pulseIn(ECHO_PIN, HIGH);
  if (rawDistance > maxDistance) {
    maxDistance = rawDistance;
  }

  distancePlot(0, 160, direction, map(rawDistance, 0, displayMaxDistance, 0, 160));
}

void distancePlot(int x, int y, float degrees, int length) {
  float angle_rad = (180 - degrees) * (PI / 180.0);
  int x2 = x + length * sin(angle_rad);
  int y2 = y - length * cos(angle_rad);
  tft.fillCircle(x2, y2, 1, TFT_CYAN);
}

void drawRanges() {
  if (scanCount++ % 10 == 0 || (displayMaxDistance - maxDistance) > 100) {
    tft.fillScreen(TFT_BLACK);
  }
  tft.drawCircle(0, 160, 40, TFT_BLUE);
  tft.drawCircle(0, 160, 80, TFT_BLUE);
  tft.drawCircle(0, 160, 120, TFT_BLUE);
  tft.drawCircle(0, 160, 160, TFT_BLUE);
  tft.drawLine(0, 160, 160, 160, TFT_BLUE);
}
