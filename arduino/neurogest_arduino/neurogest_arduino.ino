/*
  NEUROGEST - Gesture Control Home Automation System
  Arduino UNO receives a finger count (0-5) over USB serial.
  It turns on that number of LEDs and updates a 16x2 LCD.
*/

#include <LiquidCrystal.h>

// LCD pins: RS, E, D4, D5, D6, D7
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

// Five LED output pins
const int leds[5] = {2, 3, 4, 5, 6};
const int MAX_LEDS = 5;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < MAX_LEDS; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], LOW);
  }

  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("NEUROGEST");
  lcd.setCursor(0, 1);
  lcd.print("LED Count: 0");
}

void loop() {
  if (Serial.available() > 0) {
    int ledCount = Serial.parseInt();
    ledCount = constrain(ledCount, 0, MAX_LEDS);

    // Turn on the first N LEDs and turn the remaining LEDs off.
    for (int i = 0; i < MAX_LEDS; i++) {
      digitalWrite(leds[i], (i < ledCount) ? HIGH : LOW);
    }

    // Refresh the LCD status line.
    lcd.setCursor(0, 1);
    lcd.print("LED Count: ");
    lcd.print(ledCount);
    lcd.print("     ");  // Clear any leftover characters.
  }
}
