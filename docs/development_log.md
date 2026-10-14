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

## October 13, 2026 — Extended servo exercise, joystick drift, and memory cleanup

- Continued testing the **unloaded SG90** with Bluetooth-connected **Xbox Series X Controller**, Orange Pi / Pygame, and Arduino serial control. The newer velocity-based `servo_control.py` commands **45–135°**, changing servo angle proportionally to joystick displacement and elapsed time. The controller and servo moved smoothly for repeated sweeps, but the user observed that the physical servo sometimes **stops moving after a while**. This behavior remains **unresolved**; Python angle logs indicate commands sent, not measured physical position.
- Direct Pygame axis test showed left joystick values reaching approximately `-1.0` and `+1.0`, with apparent resting offset intermittently about `0.09–0.16`. The original `deadzone = 0.12` allowed potential drift; a local adjustment to `0.20` was proposed and subsequent file upload/test attempted, **but this log does not independently establish the exact deployed value**. Confirm the deployed setting with `grep '^deadzone =' ~/robotic_arm/servo_control.py`.
- Memory investigation on Orange Pi before cleanup: **970 MiB RAM total, 284 MiB available; 460/485 MiB swap used**. `ps aux --sort=-rss` identified leftover VS Code Remote-SSH / Pylance processes (Pylance ~221,164 KiB RSS, extension host ~76,972 KiB RSS). Stopped unused remote VS Code processes with `pkill -f '/home/mayok1921/.vscode-server/'`; after cleanup **667 MiB RAM available, 63 MiB swap used**. Continue coding locally on Windows VS Code and transferring over USB SCP; use lightweight SSH terminal to run.
- Retest with available memory improved showed mostly continuous Python command progression, with occasional multi-degree jumps. Because the control loop is time-based, skipped integer angle values **do not alone prove malfunction**. **Physical servo periodically ceasing motion remains unresolved**; may involve power distribution, Arduino/USB serial operation, or servo behavior.
- Current bench wiring: servo powered by **Arduino UNO 5V**, Arduino connected to Orange Pi USB hub. Potential USB/hub supply limitation is **a hypothesis, not confirmed**. User discussed a wall adapter for Arduino or a breadboard and 9V battery; **no power wiring change is reported/tested**. Do **not** apply 9V directly to SG90. For an independent servo supply, use appropriately regulated ~5V power with sufficient current, a common GND with Arduino, and **do not tie separate 5V sources together**. A barrel-jack adapter alone does not guarantee sufficient servo current.

### Next session

1. With servo unpowered, review safe power wiring and verify any supply's label/rating before connecting it.
2. Reproduce motor stopping while checking whether terminal angles continue to change and whether it resumes after resting; stop if heating, buzzing or stalling.
3. Check Arduino serial/device reconnection and power quality as needed; avoid assuming Python log lines are actual servo feedback.
4. Verify which `deadzone` setting is deployed, and commit/push any intended local changes separately.
5. Bluetooth `bluetooth_pair.py` prototype was created locally, transferred over USB and tested for basic discovery; selecting by **name or number** is intended, but pairing a never-before-paired controller is **not yet verified**. See [Bluetooth pairing design](bluetooth_pairing_design.md).

**Robot startup and full safety features are still pending.**

## October 13, 2026 — Repository architecture update (experimental)

- Preserved the tested root `servo_control.py` and `arduino/servo_serial/servo_serial.ino` as a compatible legacy pair; **no deployed hardware or proven working code was modified**.
- Added `src/` for input, motion, acknowledged serial transport, and prototype runner; `config/settings.json` for experimental 20% deadzone and other parameters; `arduino/servo_serial_v2/` for stricter `SET <angle>` input validation; `tests/test_motion.py`; USB-only PowerShell deploy script and new documentation.
- **New firmware and runner are untested on hardware and must be tested as a matching pair**: old ASCII angle protocol and new `SET` acknowledgement protocol are incompatible. Static/pure tests do not establish safety of a loaded arm.
- Main robot scope: group already owns an Arduino and motors, and the personal bench Orange Pi/Arduino/SG90 are not planned as final hardware. Purchasing decisions remain blocked on existing motor/driver model numbers and power specifications.
- Local Windows VS Code + SCP + ordinary USB SSH remains the recommended development approach; old Remote-SSH usage is recorded only for historical context.
