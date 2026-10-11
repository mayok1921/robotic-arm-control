# Robotic Arm Control System

A robotics project focused on developing a manually controlled robotic arm using an Orange Pi Zero 2W and an Xbox One S controller. Python will be used to process controller inputs and eventually translate them into robotic arm movements.

## Hardware
- Orange Pi Zero 2W
- Xbox One S Controller (USB)
- Robotic arm hardware (to be determined)

## Software
- Armbian Linux
- Python 3.14.4
- Pygame 2.6.1

## Current Progress

**October 11, 2026 — Initial Setup**

Successfully configured Armbian Linux on the Orange Pi Zero 2W and established communication with an Xbox One S controller through USB. Verified controller functionality using Linux joystick testing utilities and developed an initial Python program using Pygame.

The program successfully detected:
- 1 Xbox One S controller
- 6 analog axes
- 11 buttons

Controller detection is complete. Real-time input processing and robotic arm integration are still in development.

## Project Files

- [controller_test.py](controller_test.py) — Initial Python program for detecting connected controllers.
- [Development Log](docs/development_log.md) — Documentation of project progress and testing.

## Future Development

1. Implement real-time controller input monitoring.
2. Map controller inputs to robotic arm joint movements.
3. Select and integrate robotic arm hardware.
4. Develop motor control and safety features.
5. Test and evaluate robotic arm performance.

## Project Status

**In Development — Phase 1: Controller Integration**

The initial software environment and controller detection have been successfully established. The next objective is to process analog stick movements and button presses in real time.
