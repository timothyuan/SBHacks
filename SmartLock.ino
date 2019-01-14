// Navid Mir

#include <Servo.h>
#include <Wire.h>
#include "rgb_lcd.h"
#define RED_LED 8
#define BLUE_LED 2
#define RASPBERRY 3 // use for true/false access from server to pi to arduino 

Servo servo;
rgb_lcd lcd;
int raspberry = 0;

void lock() { // lock the door
  displayLocked();
  servo.attach(13);
  digitalWrite(BLUE_LED, HIGH);
  servo.write(180);
  delay(1000);
  servo.detach();
  digitalWrite(BLUE_LED, LOW);
}

void unlock() { // unlock the door
  displayGranted();
  servo.attach(13);
  digitalWrite(RED_LED, HIGH);
  servo.write(0);
  delay(1000);
  servo.detach();
  digitalWrite(RED_LED, LOW);
}

void displayLocked() { // display "Locked" on LCD
  lcd.clear();
  lcd.setRGB(255, 0, 0);
  lcd.print("Locked");
}

void displayDenied() { // display "Access Denied" on LCD
  lcd.clear();
  lcd.setRGB(255, 0, 0);
  lcd.print("Access Denied.");
  delay(5000);
}

void displayGranted() { // display "Access Granted" on LCD
  lcd.clear();
  lcd.setRGB(0, 255, 0);
  lcd.print("Access Granted");
}

void setup() {
  lcd.begin(16, 2);
  lcd.setRGB(0, 0, 0);
  pinMode(RASPBERRY, INPUT);
  pinMode(BLUE_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
}

void loop() {
  raspberry = digitalRead(RASPBERRY);
  if (raspberry == HIGH) {
    unlock();
    delay(5000);
    lock();
    lcd.clear();
    lcd.setRGB(0, 0, 0);
    exit(0);
  } else {
    displayDenied();
    lcd.clear();
  }
}
