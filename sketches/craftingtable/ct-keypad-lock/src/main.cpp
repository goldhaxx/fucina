#include <Arduino.h>
#include <Keypad.h>

constexpr byte ROWS = 4;
constexpr byte COLS = 4;

const char BUTTONS[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

// Pin assignments — must match wiring.yaml
// Uses high-numbered pins (23-37 odd) to avoid conflicts
byte rowPins[ROWS] = {23, 25, 27, 29};
byte colPins[COLS] = {31, 33, 35, 37};

Keypad keypad = Keypad(makeKeymap(BUTTONS), rowPins, colPins, ROWS, COLS);

const String SECRET_CODE = "1234";
String entered_code = "";

void setup() {
  Serial.begin(9600);
  Serial.println("Keypad Door Lock ready");
  Serial.println("Enter 4-digit code (* to reset, # to delete)");
}

void loop() {
  char key = keypad.getKey();
  if (!key) return;

  if (key == '*') {
    entered_code = "";
    Serial.println("Code reset");
    return;
  }

  if (key == '#') {
    if (entered_code.length() > 0) {
      entered_code = entered_code.substring(0, entered_code.length() - 1);
    }
    Serial.print("Code so far: ");
    Serial.println(entered_code);
    return;
  }

  entered_code += key;
  Serial.print("Entered: ");
  Serial.println(entered_code);

  if (entered_code.length() == SECRET_CODE.length()) {
    if (entered_code == SECRET_CODE) {
      Serial.println("*** DOOR UNLOCKED ***");
      delay(2000);
      Serial.println("Door re-locked");
    } else {
      Serial.println("Wrong code!");
    }
    entered_code = "";
  }
}
