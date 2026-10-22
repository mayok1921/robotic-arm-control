# Bluetooth controller pairing and reconnection

## Current status (October 22, 2026)

- The earlier pairing utility detected devices and reported a PS5 DualSense connection, but later the PS5 controller was absent from BlueZ's paired-device list.
- On the Orange Pi, Linux listed only `dw_hdmi` in `/proc/bus/input/devices` and no `/dev/input/js*`. The kernel has `CONFIG_INPUT_JOYDEV=y`, but `modinfo hid_playstation` failed and `CONFIG_HID_SONY` is disabled. The complete PlayStation driver state has not been established.
- **The upgraded `bluetooth_pair.py` has been checked in and its core parsers/verification behavior tested with software mocks, but live DualSense pairing and input recognition with this new revision remain unverified.** A successful Bluetooth connection alone does not establish that controller input is available.

## Running from the Orange Pi (over USB SSH)

```bash
cd ~/robotic_arm
python3 bluetooth_pair.py
```

Put a new DualSense into pairing mode with **Create + PS** until the light flashes rapidly. Select a listed device by number, exact displayed name, or Bluetooth MAC address. If multiple devices use the name `Wireless Controller`, select by number. Type `r` to rescan or `q` to cancel.

The tool scans, checks the controller's state, pairs if needed, trusts it, attempts connection, and then **rechecks** `Paired: yes`, `Trusted: yes`, and `Connected: yes`. It reports controller-like Linux input devices **separately**. The scan list can contain previously discovered/cached devices.

### Optional commands

```bash
python3 bluetooth_pair.py --list
python3 bluetooth_pair.py --diagnose
python3 bluetooth_pair.py --scan-seconds 20
python3 bluetooth_pair.py --retries 2
python3 bluetooth_pair.py --reconnect AA:BB:CC:DD:EE:FF
```

Replace the example MAC with the address for a controller you've already paired. `--diagnose` reports adapter information, kernel config indicators, and Linux input devices without pairing or motor activity. Do not commit actual controller addresses or credentials.

## What success means

1. **Pairing:** `Paired: yes` is confirmed after the pair command.
2. **Trust:** `Trusted: yes` is confirmed, helping future reconnect attempts.
3. **Bluetooth link:** `Connected: yes` is confirmed at the time of status check.
4. **HID input:** Linux must separately create an appropriate `/dev/input/event*` and/or `/dev/input/js*` controller device, and a live test must demonstrate actual button/axis events.
5. **Motor control:** Only after all of the above, and a separate actuator safety review, should joystick inputs be allowed to command motors.

The script validates the first three and **reports candidate input devices** for the fourth. It cannot provide missing `hid_playstation` kernel functionality, prove reliable long-term wireless connectivity, or verify real button/axis motion. It does not control motors, modify controller firmware, or auto-start services.

## Troubleshooting the current PS5 problem

If pairing seems to work but `bluetoothctl devices Paired` shows only the Xbox controller, run `python3 bluetooth_pair.py --diagnose` and attempt a fresh DualSense pairing while in flashing pairing mode. Follow the program's actual status output instead of relying on the previous version's optimistic success message.

If Bluetooth shows connected but `/proc/bus/input/devices` has no DualSense input, investigate BlueZ HID registration and the Armbian kernel's PlayStation driver support separately. `uhid` being loaded and `joydev` being built in do **not** by themselves establish DualSense support.

## Development and safety notes

- Keep this utility separate from `servo_control.py`. Never treat a Bluetooth connection as permission for a powered joint to move.
- A powered robot needs independently engineered controller-loss handling, movement limits, and physical emergency stop.
- The normal workflow should reconnect a trusted controller without a Bluetooth scan, but persistence and PS5 reconnection need real hardware validation.
- Run offline unit tests from the repository root with `python3 -m unittest discover -s tests -v`.
- A physical pairing button/LED and automated headless reconnection are **future features**, not implemented.

See [USB development setup](usb_development_setup.md), [servo demonstration](servo_demo_guide.md), and [development log](development_log.md).

## October 22, 2026 — Pairing-agent fix (pending live retest)

During direct `bluetoothctl` testing, the DualSense advertised as **DualSense Wireless Controller** and BlueZ issued `Request authorization` / `[agent] Accept pairing (yes/no)`; after accepting, BlueZ reported `Connected: yes`, `Bonded: yes`, and `Paired: yes`. This shows the pairing workflow required an active authorization agent. **It does not conclusively show that our earlier Python program alone caused the failure or that Bluetooth HID input is working.**

The previous Python utility used a short-lived one-shot `bluetoothctl pair` process. The new `pair_interactively` routine keeps a `bluetoothctl -a NoInputNoOutput` session alive with a terminal (Linux PTY), registers a pairing agent, and requests bonding for the chosen device. If BlueZ still asks to accept a pairing, the program presents that request and accepts only after the operator confirms; it never silently authorizes unknown nearby devices. It then checks the saved pairing state before trusting and connecting. The ordinary numbered-device selection remains unchanged.

**This revision has not yet been live-tested against the user's DualSense.** From Windows local VS Code, `git pull origin main`, then `scp bluetooth_pair.py mayok1921@192.168.7.2:~/robotic_arm/`. On the Orange Pi, disconnect the PS5 USB cable, hold **Create + PS** to enter pairing mode, and run `python3 bluetooth_pair.py --scan-seconds 20`. Select the named DualSense, inspect any program-local authorization request, and verify `bluetoothctl info <address>` and `/proc/bus/input/devices` afterward. No Arduino or motors should be connected during the first test.
