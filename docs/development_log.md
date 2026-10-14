# Development Log

## October 11, 2026 — Initial setup

Configured Armbian Linux on Orange Pi Zero 2W. Xbox controller detected over USB with `jstest /dev/input/js1`; Pygame 2.6.1 and [controller_test.py](../controller_test.py) verified controller input.

## October 12–13, 2026 — Remote development and Bluetooth

- Established SSH and VS Code Remote-SSH over local Wi-Fi.
- Paired Xbox controller over Bluetooth and tested controller input. Bluetooth input mapping differs from USB; D-pad mapping needs verification.
- Experienced intermittent display/Remote-SSH freezes; RAM/ZRAM usage increased but root cause was not established.

## October 13, 2026 — First complete wireless servo demonstration

- ELEGOO UNO R3 drove an unloaded SG90 at 45°/90°/135°.
- Orange Pi identified Arduino as `/dev/ttyACM0` via USB hub; PySerial 3.5 installed.
- Serial commands from Orange Pi moved servo.
- [servo_control.py](../servo_control.py) mapped Xbox Bluetooth left joystick to servo position; full chain verified.
- Saved tested Arduino and Python programs and [servo guide](servo_demo_guide.md).

## October 13, 2026 — Portable Wi-Fi-free development connection verified

- Initial Orange Pi hotspot attempt failed: `unisoc_wifi` advertised AP but `wpa_supplicant` reported `Failed to initialize AP interface`; returned to Wi-Fi during debugging.
- USB Ethernet gadget initially stalled at `usb0 NO-CARRIER`, UDC `not attached`, and Windows detected nothing. `g_ether` and the device-tree peripheral configuration alone were insufficient.
- **Key breakthrough:** swapping which physical Orange Pi USB-C ports carried the laptop and USB hub. The functional gadget-capable USB0 port had earlier been mistaken for a power-only port. Gadget UDC changed to `configured`.
- Windows then enumerated `USB\\VID_0525&PID_A4A2` as `USB Serial Device (COM7)`, an incorrect class binding.
- Windows built-in `netrndis.inf` registration did not fix binding. Matching signed RNDIS package (`rndis.inf`/`rndis.cat`) extracted from Microsoft Update Catalog; `pnputil /add-driver ... /install` confirmed **driver package installed on device**.
- `Get-NetAdapter` listed **Ethernet 6 — USB Ethernet/RNDIS Gadget — Up**.
- Windows USB IPv4 `192.168.7.1/24`; Orange Pi `usb0` `192.168.7.2/24`. Windows ping: 4/4 replies, 0% loss, sub-millisecond latency. Direct USB SSH succeeded; VS Code Remote-SSH connected to Linux on `192.168.7.2`.
- Enabled `g_ether` loading via `/etc/modules-load.d/robotarm-usb.conf` and systemd `robotarm-usb.service` setting the USB interface address. Service reported **active** and remote access reconnected after Orange Pi reboot.
- Disabled Orange Pi Wi-Fi using `sudo nmcli radio wifi off`; `wlan0` unavailable but SSH terminal still responded to `hostname`, confirming Wi-Fi-free remote access.
- Arduino remained connected through USB hub on separate USB port throughout working laptop USB development connection.
- Full instructions: [portable USB development guide](usb_development_setup.md).

**Still unverified:** Windows laptop reboot IP persistence; second laptop onboarding; complete Orange Pi power cycle and extended simultaneous-use stability; automatic startup of the servo controller itself.

**Next development target:** improve joystick-to-servo control robustness, safety, and precision before additional actuators.
