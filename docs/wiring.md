# Wiring notes

## Verified bench prototype — October 13, 2026

Single unloaded SG90 servo attached to Arduino UNO R3:

| SG90 wire | Arduino UNO |
| --- | --- |
| Brown | GND |
| Red | 5V |
| Orange | D9 |

- Arduino UNO R3 connects by USB to a hub attached to Orange Pi Zero 2W.
- Arduino appears on the Orange Pi as `/dev/ttyACM0` in the tested setup (may vary).
- Xbox wireless controller communicates with Orange Pi over Bluetooth.
- Complete wiring, code and tests: [servo demo guide](servo_demo_guide.md).

**Safety:** Powering one unloaded SG90 from the Arduino 5V pin was acceptable for this brief bench test; do not extrapolate to loaded or multiple servos. Never connect a motor directly to an Orange Pi GPIO pin. Choose dedicated power, drivers, shared grounding and current protection for future actuators.

## Future robotic arm wiring (not yet verified)

Before creating final wiring diagrams, record motor models, voltage and stall current, driver specifications, logic-level compatibility, shared-ground requirements, limit-switch/safety circuits and supply protection.
