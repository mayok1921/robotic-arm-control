# Hardware inventory and port assignments

## Available and verified

- Orange Pi Zero 2W running Armbian Linux
- Xbox wireless controller paired over Bluetooth
- ELEGOO Arduino UNO R3, accessible through Orange Pi USB hub (`/dev/ttyACM0` during testing)
- SG90 micro servo, tested unloaded with Arduino
- USB hub, data cable, jumper wires
- Windows laptop using USB Ethernet/RNDIS Gadget and VS Code Remote-SSH

## Crucial USB port discovery

**Both Orange Pi USB-C ports are distinct.** The tested configuration uses:

- **USB0 (gadget/peripheral-capable):** direct data cable to Windows laptop. `g_ether` on Orange Pi, RNDIS adapter on Windows, USB SSH.
- **USB1 (host):** USB hub connecting Arduino and other host peripherals.

The port originally assumed to be power-only proved to be the functional gadget connection in the user's setup. The Arduino and Windows USB SSH links worked concurrently. Review the Orange Pi board labels and safe power supply wiring; connecting multiple power sources must follow the board's electrical specifications.

Full verified USB procedure: [portable setup](usb_development_setup.md).

## Future hardware

- Final robotic arm servos/actuators and suitable motor driver(s)
- Dedicated properly rated actuator power supply and electrical protection
- Mechanical limits, emergency stop and safe enclosure as appropriate

Only a **single unloaded SG90** was tested. Final arm hardware is not yet purchased/accessed/validated.
