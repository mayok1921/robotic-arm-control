# Hardware inventory

## Available and tested

- Orange Pi Zero 2W running Armbian Linux
- Xbox wireless controller (previously tested over USB and now Bluetooth)
- ELEGOO Arduino UNO R3 from the starter kit
- SG90 micro servo (single unloaded servo tested)
- USB hub connected to Orange Pi USB/OTG port
- Jumper wires and USB cable
- Windows computer for development

## Not yet accessible or finalized

- Final robotic arm servos/actuators and their dedicated power supply
- Motor driver/controller selection for the final robot
- A tested offline laptop-to-Orange-Pi software update connection

## Important

The Orange Pi USB/OTG port currently **hosts a USB hub** for devices including the Arduino. The same port cannot simultaneously host the hub and function as a USB device/gadget for a laptop under the current arrangement.

Direct USB gadget networking to Windows has **not been verified**. Wi-Fi is used for current SSH/VS Code development, but the demonstrated controller-to-servo operation itself does not need Wi-Fi.

Final actuator wiring and power design must be validated separately. See [verified SG90 demo guide](servo_demo_guide.md).
