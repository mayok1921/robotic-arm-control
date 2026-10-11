# Development Log

## October 11, 2026 — Initial Setup

Configured Armbian Linux on an Orange Pi Zero 2W and connected an Xbox One S controller via USB. Verified controller input using `jstest /dev/input/js1`. Installed Pygame 2.6.1 and tested controller detection with [controller_test.py](../controller_test.py). The script detected one Xbox One S controller with 6 axes and 11 buttons.

**Next:** Read analog stick and button inputs in real time, then map inputs to future robotic arm movements.
