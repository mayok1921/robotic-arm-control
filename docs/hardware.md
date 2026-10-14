# Hardware inventory and proposed robot integration

## Verified personal bench hardware (not intended for group robot installation)

- Orange Pi Zero 2W (1GB) with Armbian Linux
- Xbox wireless controller over Bluetooth
- ELEGOO Arduino UNO R3, USB serial `/dev/ttyACM0` during testing
- Single unloaded SG90 servo, with orange signal on Arduino D9, red to Arduino 5V and brown to GND for bench only
- USB hub, data cables, jumper wires
- Windows laptop using local VS Code and USB Ethernet/RNDIS + SSH/SCP

## USB port roles

- **USB0 (USB gadget):** USB-C connection to laptop; `usb0` IP `192.168.7.2/24`
- **USB1 (USB host):** USB hub to Arduino

Do not assume the two connectors are interchangeable or that all multi-source powering combinations are safe. See [USB guide](usb_development_setup.md).

## Group robot

- Existing Arduino: **model to be identified**
- Existing robot motors: **models and quantities to be identified; reuse intended**
- Existing motor drivers, sensors and power supply: **unknown**
- Dedicated SBC: likely Orange Pi Zero 2W, pending hardware review and budget
- Power: one properly rated main source with protected motor/electronics branches, sized after identifying installed motors

See [integration plan](integration_plan.md) and [bill of materials](bill_of_materials.md). The prototype's servo supply sometimes appears unreliable after repeated movement; its exact cause has not been established.
