#include <Servo.h>
#include <stdlib.h>
#include <string.h>

Servo motor;

const int motorPin = 9;

const int neutralPulse = 1500;
const int minPulse = 1250;
const int maxPulse = 1750;

const unsigned long commandTimeout = 350;

bool motorArmed = false;
unsigned long lastCommandTime = 0;

char commandBuffer[24];
byte commandIndex = 0;

void stopMotor() {
  motor.writeMicroseconds(neutralPulse);
}

void disarmMotor() {
  motorArmed = false;
  stopMotor();
}

void armMotor() {
  if (motorArmed) return;

  stopMotor();
  motorArmed = true;
  lastCommandTime = millis();

  Serial.println("ARMED");
}

void processCommand(char* command) {

  if (strcmp(command, "ARM") == 0) {
    armMotor();
    return;
  }

  if (strcmp(command, "DISARM") == 0) {
    disarmMotor();
    Serial.println("DISARMED");
    return;
  }

  if (!motorArmed) return;

  if (command[0] == 'P') {

    char* endPointer;
    long pulse = strtol(command + 1, &endPointer, 10);

    if (endPointer == command + 1 || *endPointer != '\0') {
      return;
    }

    if (pulse >= minPulse && pulse <= maxPulse) {
      motor.writeMicroseconds((int)pulse);
      lastCommandTime = millis();
    }
  }
}

void setup() {
  Serial.begin(9600);

  // Attach once and maintain a neutral PWM signal.
  motor.writeMicroseconds(neutralPulse);
  motor.attach(motorPin, 500, 2500);
  stopMotor();

  motorArmed = false;

  Serial.println("READY");
}

void loop() {

  while (Serial.available() > 0) {

    char incoming = Serial.read();

    if (incoming == '\n') {
      commandBuffer[commandIndex] = '\0';
      processCommand(commandBuffer);
      commandIndex = 0;
    }
    else if (incoming != '\r') {

      if (commandIndex < sizeof(commandBuffer) - 1) {
        commandBuffer[commandIndex++] = incoming;
      }
      else {
        commandIndex = 0;
      }
    }
  }

  if (motorArmed &&
      millis() - lastCommandTime > commandTimeout) {

    disarmMotor();
    Serial.println("TIMEOUT_DISARMED");
  }
}
