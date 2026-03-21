#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>
#include <LiquidCrystal.h>

// RFID pin assignments
constexpr uint8_t RST_PIN = 26;
constexpr uint8_t SS_PIN  = 53;

// LCD pin assignments (RS, E, D4, D5, D6, D7)
LiquidCrystal lcd(22, 24, 23, 25, 27, 29);

MFRC522 mfrc522(SS_PIN, RST_PIN);

// Approved RFID codes — add your card's bytes here after first scan
const byte APPROVED[][10] = {
  {0, 0, 0, 0}  // Placeholder — replace with your card's UID bytes
};
constexpr int NUM_APPROVED = sizeof(APPROVED) / sizeof(APPROVED[0]);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();

  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("  Tap to Enter  ");

  Serial.println("RFID Door Lock ready");
  Serial.println("Scan a card to see its UID");
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;
  if (mfrc522.uid.size == 0) return;

  // Print UID to serial
  Serial.print("Card UID: ");
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (i > 0) Serial.print(", ");
    Serial.print(mfrc522.uid.uidByte[i]);
  }
  Serial.println();

  // Check against approved list
  bool match = false;
  for (int i = 0; i < NUM_APPROVED; i++) {
    byte j;
    for (j = 0; j < mfrc522.uid.size; j++) {
      if (mfrc522.uid.uidByte[j] != APPROVED[i][j]) break;
    }
    if (j == mfrc522.uid.size) {
      match = true;
      break;
    }
  }

  lcd.setCursor(0, 1);
  if (match) {
    Serial.println("ACCESS GRANTED");
    lcd.print("  Come on in!   ");
  } else {
    Serial.println("ACCESS DENIED");
    lcd.print("    NO MATCH    ");
  }
  delay(2000);
  lcd.setCursor(0, 1);
  lcd.print("                ");

  mfrc522.PICC_HaltA();
}
