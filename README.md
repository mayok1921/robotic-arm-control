# Robotic Arm Control System

Portable robotic arm control prototype using an **Orange Pi Zero 2W**, an **Xbox wireless controller**, **Python/Pygame**, and an **Arduino UNO R3** driving a single test SG90 servo.

## Verified milestones — October 13, 2026

1. **Xbox controller → Bluetooth → Orange Pi → USB serial → Arduino → SG90 servo**: left joystick successfully moved the unloaded servo.
2. **Windows laptop → USB → Orange Pi Zero 2W → SSH/VS Code**: direct USB networking worked without Orange Pi Wi-Fi, and reconnected after an Orange Pi reboot.
3. **Concurrent connections**: Laptop connected via USB0 while the Arduino remained connected through a USB hub on USB1.

## Start here

- **[Portable, Wi-Fi-free USB development setup](docs/usb_development_setup.md)** — correct USB ports, Windows RNDIS driver workaround, static IPs, SSH, VS Code, boot persistence and troubleshooting
- **[Servo-control demonstration](docs/servo_demo_guide.md)** — SG90 wiring, Arduino firmware, Python joystick script, test instructions
- **[Development log](docs/development_log.md)** — decisions, verified results, and limitations
- **[Bluetooth pairing design](docs/bluetooth_pairing_design.md)** — planned numbered device selector and eventual physical pairing button

## Architecture

**Controller (Bluetooth) → Orange Pi (Python/Pygame) → USB serial → Arduino UNO R3 (Servo library) → SG90 servo**

A development laptop can connect **independently through the other Orange Pi USB-C port** using USB networking and Remote-SSH. The Orange Pi need not join an external Wi-Fi network to be programmed in the tested setup.

## Hardware and software

- Orange Pi Zero 2W, Armbian Linux (observed kernel `6.18.55-current-sunxi64`)
- Xbox wireless controller
- ELEGOO Arduino UNO R3, SG90 test servo, USB hub and jumper wires
- Windows computer with VS Code Remote-SSH
- Python 3.14.4, Pygame 2.6.1, PySerial 3.5 (observed environment)

Final robotic arm motors, drivers and motor power supply remain to be chosen or accessed.

## Files

- [servo_control.py](servo_control.py) — tested joystick-to-servo demo
- [arduino/servo_serial/servo_serial.ino](arduino/servo_serial/servo_serial.ino) — tested serial-command Arduino sketch
- [controller_test.py](controller_test.py) — earlier controller test
- [scripts/robotarm-usb.service](scripts/robotarm-usb.service) — copy of tested automatic USB networking service
- [docs/hardware.md](docs/hardware.md) and [docs/wiring.md](docs/wiring.md) — hardware and wiring notes

## Roadmap

1. ~~Set up Armbian and Xbox controller detection.~~
2. ~~Verify serial control of unloaded SG90 from Orange Pi through Arduino.~~
3. ~~Move SG90 with Bluetooth Xbox joystick.~~
4. ~~Establish and test laptop-to-Orange-Pi USB networking without Orange Pi Wi-Fi, including reboot.~~
5. **Next: improve servo command parsing, failsafes and smooth joystick control.**
6. Implement an on-demand numbered Bluetooth device pairing utility; later add a physical pair button.
7. Validate offline access after complete power cycles and Windows reboot; test second developer's laptop.
8. Configure safe automatic startup of robotic-arm controller.
9. Integrate actual arm actuators and properly rated motor power supply, then validate mechanical safety.

**Status:** Working portable development link and bench servo-control prototype. Not a finished or safety-qualified robotic arm.
