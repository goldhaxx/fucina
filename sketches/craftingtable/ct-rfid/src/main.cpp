#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>

// Pin assignments — must match wiring.yaml
constexpr uint8_t RST_PIN = 26;
constexpr uint8_t SS_PIN  = 53;

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  while (!Serial);
  SPI.begin();
  mfrc522.PCD_Init();
  mfrc522.PCD_DumpVersionToSerial();
  Serial.println(F("Scan an RFID card or tag..."));
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) {
    Serial.println("Bad read");
    return;
  }

  Serial.print("Card UID: ");
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (i > 0) Serial.print("-");
    Serial.print(mfrc522.uid.uidByte[i]);
  }
  Serial.println();

  mfrc522.PICC_HaltA();
}
