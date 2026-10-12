# Hardware inventory

## Available
- Orange Pi Zero 2W running Armbian Linux
- Wired Xbox One S controller
- Computer used for development

## Not yet selected
- Robotic arm and actuators
- Motor drivers and power supply
- Arduino (optional, depending on the control architecture)
- Communication adapter or cable for reliable offline deployment

## Important
The Orange Pi's USB/OTG connector is being investigated for a direct wired computer connection. USB gadget support has **not** been verified on the installed Armbian kernel. Do not assume that plugging a USB-C cable into the computer will establish SSH.

Verify connector power requirements and USB host/device mode before connecting hardware. Do not power motors directly from GPIO pins.
