# Hardware inventory and proposed robot integration

## Personal bench hardware — verified

- Orange Pi Zero 2W (1GB) with Armbian Linux; Xbox controller over Bluetooth
- Personal ELEGOO Arduino UNO R3 with an unloaded SG90 test servo
- Orange Pi USB0 to Windows laptop by USB/RNDIS; USB1 host to Arduino via hub
- Windows laptop runs VS Code **locally**, transferring files with SCP and testing via lightweight SSH

**Personal equipment is not earmarked for installation on the group's robot.**

## Existing glovebox robotic arm — documented, physically reconfirm before energizing

The original **Spring 2026 ME 416 final report** describes the inherited arm. It is more useful than treating installed hardware as wholly unknown.

- High-torque motors: **DOCYKE S550 high-power servo family**, approximately **550 kg·cm advertised torque**; the prior project described high-power servos on the major joints. Earlier hardware inventory indicates **four high-torque servos**; confirm count and installed labels on the current arm.
- Low-torque servos: about **80 kg·cm advertised torque** on smaller joints/gripper, reportedly **two smaller servos**; verify part numbers and counts.
- Power discussed in project history: **SE-1200-24-class 24 V, 50 A, 1,200 W supply**; verify unit label, present wiring and actual condition before reuse. This rating is **maximum supply capability, not measured robot draw**.
- Earlier team documents **Arduino-based servo control** and later **ESP32 + PS5 DualSense** wireless operation. The current team reports the inherited Arduino is available. Confirm exact board model and whether the ESP32 or other control electronics are still installed.
- Predominantly 3D-printed mechanical structure and gripper; servo loading and mechanical limits must be evaluated before commanding motion.

**Electrical safety:** Neither the 24V rail nor an RC-style 5V PWM control signal may be assumed suitable for *every* installed servo. Check each motor's true operating voltage, signal interface, and current using the manufacturer documentation and the actual installed labeling. The reported high-power stall current can be tens of amperes; do not test stall on an assembled arm.

Source: [Spring 2026 ME 416 final report](https://docs.google.com/document/d/1urSUX6SLoGXcrml9DO4g4pWCwH8FJFKZ/edit) (including motor specifications, torque/thermal analysis, wiring diagram and original BOM).

## USB port roles on the personal Orange Pi

- USB0 (gadget): direct laptop development over `192.168.7.2/24`
- USB1 (host): hub to Arduino

See [USB setup](usb_development_setup.md). Do not use unverified power combinations on the USB-C ports.

## Planned dedicated hardware

- Dedicated SBC: Orange Pi Zero 2W **candidate**, subject to available power, USB host and support requirements
- Reuse the inherited Arduino and installed motors if compatible
- Keep existing power supply **only after** evaluating demand, protection, output rails, condition and wiring
- Motor-power emergency stop, fuses, DC/DC rails and protection sized from the electrical-load worksheet rather than the personal SG90 test

See [electrical load plan](electrical_load_plan.md), [integration plan](integration_plan.md) and [bill of materials](bill_of_materials.md).

## Existing project source

See the predecessor team's Spring 2026 ME 416 final report in Google Drive, *Robotic Arm for Removal of Glovebox HEPA Filter*, for the original motor selections, wiring diagram, BOM and high-power servo thermal analysis. Treat the report as the design baseline, not as confirmation that the physical arm remains unchanged.
