# Headless development — recommended local VS Code workflow

**Verified October 13, 2026:** Windows laptop communicates directly with the Orange Pi Zero 2W via USB/RNDIS at `192.168.7.2`, even with the Orange Pi Wi-Fi disabled. The `robotarm-usb.service` persists the gadget IP across Orange Pi reboots. The robot application itself does **not** autostart yet.

## Recommended approach

1. Open your **local Windows** clone of `robotic-arm-control` in VS Code.
2. Edit Python on the laptop. Keep Pylance and other editor extensions **off the Orange Pi**.
3. In the **local VS Code PowerShell terminal**, run:
   ```powershell
   scp .\servo_control.py mayok1921@192.168.7.2:/home/mayok1921/robotic_arm/servo_control.py
   ssh mayok1921@192.168.7.2
   ```
4. In SSH, run `cd ~/robotic_arm && python3 servo_control.py` with the matching legacy sketch on the bench Arduino.
5. To test experimental files later, use [`scripts/deploy.ps1`](../scripts/deploy.ps1), flash matching v2 Arduino firmware independently, and run `python3 -m src.control`.

**Do not use VS Code Remote-SSH as the standard development environment.** Previous Pylance, extension host and related server processes were consuming hundreds of MiB of RAM; killing those processes increased available RAM from ~284 MiB to ~667 MiB. Regular terminal SSH works without running remote editor services.

See [complete USB setup](usb_development_setup.md) for the correct USB-C ports, RNDIS driver binding, static IPv4 addresses, troubleshooting and persistence.

## Still to do

- Independently test normal boot after power cycling laptop and Orange Pi.
- Configure safe, **separate** robot controller autostart only after behavior on input loss is verified.
- Support additional developer machines using their own SSH account/key credentials and network drivers.
