// EXPERIMENTAL / UNTESTED. For one unloaded SG90 only.
// Separate protocol from legacy servo_serial.ino. Requires "SET <angle>\n".
#include <Servo.h>

Servo testServo;
const byte SERVO_PIN = 9;
const int MIN_ANGLE = 45;
const int MAX_ANGLE = 135;
const unsigned long MAX_LINE_AGE_MS = 150;
char line[20];
byte length = 0;
unsigned long lineStarted = 0;

void rejectLine() {
  length = 0;
  line[0] = '\0';
  Serial.println(F("ERR"));
}

void applyLine() {
  line[length] = '\0';
  // Require exact prefix and digits only, no signs or trailing garbage.
  if (length < 5 || line[0] != 'S' || line[1] != 'E' ||
      line[2] != 'T' || line[3] != ' ') {
    rejectLine();
    return;
  }
  int value = 0;
  for (byte i = 4; i < length; ++i) {
    if (line[i] < '0' || line[i] > '9') {
      rejectLine();
      return;
    }
    value = value * 10 + (line[i] - '0');
    if (value > MAX_ANGLE) {
      rejectLine();
      return;
    }
  }
  if (value < MIN_ANGLE || value > MAX_ANGLE) {
    rejectLine();
    return;
  }
  testServo.write(value);
  Serial.print(F("OK "));
  Serial.println(value);
  length = 0;
}

void setup() {
  Serial.begin(9600);
  testServo.attach(SERVO_PIN);
  testServo.write(90);
  Serial.println(F("READY"));
}

void loop() {
  while (Serial.available()) {
    char ch = static_cast<char>(Serial.read());
    if (ch == '\n') {
      applyLine();
    } else if (ch == '\r') {
      // Accept CRLF as well as LF.
    } else if (length >= sizeof(line) - 1) {
      rejectLine();
    } else {
      if (length == 0) lineStarted = millis();
      line[length++] = ch;
    }
  }
  if (length && millis() - lineStarted > MAX_LINE_AGE_MS) {
    rejectLine();
  }
}
