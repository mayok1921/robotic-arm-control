# Robotic Arm Control System

Prototype of a Bluetooth Xbox-controller-operated robotic arm control system using **Orange Pi Zero 2W**, **Python/Pygame**, and an **Arduino UNO R3** as a temporary low-level servo controller.

## Verified demonstration — October 13, 2026

**Xbox wireless controller → Bluetooth → Orange Pi Zero 2W → USB serial → Arduino UNO R3 → SG90 servo**

The joystick successfully moved the unloaded SG90 servo through the full chain.

## Reproduce the demo

**[Step-by-step setup, wiring, commands, and test results](docs/servo_demo_guide.md)**

## Hardware currently used

- Orange Pi Zero 2W running Armbian Linux
- Xbox wireless controller connected over Bluetooth
- Arduino UNO R3 connected through the Orange Pi USB hub
- SG90 micro servo with three jumper wires

The eventual robotic arm actuators and motor driver are not yet selected/accessible.

## Software

- Python 3.14.4, Pygame 2.6.1, PySerial 3.5 (tested environment)
- Arduino IDE and Servo library
- Armbian Linux; SSH/VS Code used for development over Wi-Fi

## Project files

- [servo_control.py](servo_control.py) — tested Python joystick-to-servo demo
- [arduino/servo_serial/servo_serial.ino](arduino/servo_serial/servo_serial.ino) — tested Arduino serial/servo sketch
- [controller_test.py](controller_test.py) — earlier controller detection test
- [Servo demonstration guide](docs/servo_demo_guide.md) — reproducible wiring, setup, and testing
- [Development log](docs/development_log.md) — milestones and observations
- [Wiring notes](docs/wiring.md) and [hardware inventory](docs/hardware.md)

## Roadmap

1. ~~Configure Armbian and verify Bluetooth controller input.~~
2. ~~Move an unloaded SG90 using Arduino, then Orange Pi USB serial.~~
3. ~~Move SG90 using Xbox joystick through the full system.~~
4. Refine parsing, safety behavior, and controller mapping; test stability.
5. Set up automatic startup without a laptop or Wi-Fi for normal operation.
6. Establish a reliable offline code-update workflow.
7. Select the final robotic arm motors, drivers, and suitable power.
8. Integrate and validate the complete arm.

**Status:** Working bench prototype; not yet a safe or finished robotic arm system.
