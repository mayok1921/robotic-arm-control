#include <Servo.h>

Servo servo;

const int servoPin = 9;
int angle = 90;

void setup() {
  Serial.begin(9600);
  servo.attach(servoPin);
  servo.write(angle);
  Serial.println("READY");
}

void loop() {
  if (Serial.available() > 0) {
    int received = Serial.parseInt();

    if (received >= 0 && received <= 180) {
      angle = received;
      servo.write(angle);
      Serial.print("ANGLE:");
      Serial.println(angle);
    }

    while (Serial.available() > 0) {
      Serial.read();
    }
  }
}
