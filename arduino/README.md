# Arduino integration

**Working bench prototype — October 13, 2026**

The Arduino UNO R3 receives angle commands from the Orange Pi Zero 2W over USB serial (9600 baud) and controls an unloaded SG90 servo on digital pin 9.

- [Servo serial firmware](servo_serial/servo_serial.ino)
- [Step-by-step reproduction guide](../docs/servo_demo_guide.md)
- [Orange Pi Python application](../servo_control.py)

The verified path is Xbox controller → Bluetooth → Orange Pi Python → USB serial → Arduino → SG90 servo.

**Prototype limitations:** The firmware uses `Serial.parseInt()`, which is not robust against malformed input and delimiters, and has no connection-loss watchdog. Do not use this code as-is for a loaded robotic arm. Future work should include strict line-based parsing, acknowledgements, timeout handling, safe stop behavior and physical joint limits.
