# Development Log

## October 11, 2026 — Initial setup

Configured Armbian Linux on an Orange Pi Zero 2W and connected an Xbox One S controller by USB. Verified controller input using `jstest /dev/input/js1`. Installed Pygame 2.6.1; [controller_test.py](../controller_test.py) detected one controller, 6 axes and 11 buttons.

## October 12–13, 2026 — Remote development and Bluetooth

- Established SSH access and VS Code Remote-SSH from Windows over the local Wi-Fi network.
- Paired and connected the Xbox controller via Bluetooth and confirmed reconnection. Bluetooth input reported 6 axes and 16 buttons, different from USB.
- Began testing live inputs; D-pad mapping still needs verification.
- Experienced intermittent HDMI/SSH hangs while VS Code Remote-SSH was running. Memory inspection showed increased RAM/ZRAM usage, but no definitive cause was established. Do not consider stability resolved.

## October 13, 2026 — First complete wireless servo demonstration

- Used the existing ELEGOO UNO R3 and small SG90 servo, unloaded.
- Confirmed direct Arduino movement via a 45°/90°/135° sweep test.
- Connected Arduino to Orange Pi USB hub; serial interface appeared at `/dev/ttyACM0`.
- Installed and verified PySerial 3.5.
- Uploaded serial-command Arduino sketch. Confirmed servo movement when sending a serial angle from the Orange Pi.
- Ran [servo_control.py](../servo_control.py) with the Bluetooth Xbox controller. **Moving the left joystick moved the SG90 servo successfully.**
- Recorded a [reproduction guide](servo_demo_guide.md) and saved the working Arduino and Python programs.

**Next:** Preserve this working baseline, then refine safety/robustness, offline deployment, and automatic startup. Final arm hardware not yet integrated.
