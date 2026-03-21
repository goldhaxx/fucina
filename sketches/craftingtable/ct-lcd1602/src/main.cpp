#include <Arduino.h>
#include <LiquidCrystal.h>

// Pin assignments — must match wiring.yaml
// LiquidCrystal(RS, E, D4, D5, D6, D7)
constexpr int RS_PIN = 12;
constexpr int E_PIN  = 11;
constexpr int D4_PIN = 2;
constexpr int D5_PIN = 3;
constexpr int D6_PIN = 4;
constexpr int D7_PIN = 5;

LiquidCrystal lcd(RS_PIN, E_PIN, D4_PIN, D5_PIN, D6_PIN, D7_PIN);

void setup() {
  lcd.begin(16, 2);
}

void loop() {
  // Show all 32 characters
  lcd.setCursor(0, 0);
  lcd.print("0123456789ABCDEF");
  lcd.setCursor(0, 1);
  lcd.print("0123456789ABCDEF");
  delay(2000);

  // Scanning cursor demo
  for (int row = 0; row < 2; row++) {
    for (int col = 0; col < 16; col++) {
      lcd.setCursor(col, row);
      lcd.print("0");
      delay(100);
      lcd.clear();
    }
  }
}
