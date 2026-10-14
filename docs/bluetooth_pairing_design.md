# Bluetooth controller pairing and reconnect workflow

**Status: Planned — not yet implemented as a Python utility.** The existing Xbox controller was successfully paired and connected manually using `bluetoothctl`, and automatic reconnection was observed. The number-or-name selection interface and physical button are future work.

## Intended user experience

### Normal operation (no laptop required)

1. Power on Orange Pi / robot.
2. Turn on an already paired and trusted Xbox controller.
3. Bluetooth reconnects automatically.
4. Once controller inputs are available, the robot controller becomes ready.

**No Bluetooth scan, pairing prompt, laptop, or Wi-Fi should be required on every startup.**

### Add or switch a controller (only when requested)

From the Windows laptop's **local** VS Code environment, upload an independent `bluetooth_pair.py` utility over the existing USB SSH connection, then run it on the Orange Pi:

```bash
python3 bluetooth_pair.py
```

Proposed interaction:

```text
Scanning for Bluetooth devices...
1. Xbox Wireless Controller
2. Xbox Elite Wireless Controller
3. Another Bluetooth device

Select device (number or name): Xbox Wireless Controller
Pairing...
Connected; device trusted for future connections.
```

Expected behavior:

- Show nearby devices with readable names, and a distinguishing abbreviated address for similarly named devices.
- Let the user select by **number or the device's displayed Bluetooth name**, without typing a Bluetooth MAC address. Exact names are accepted when unambiguous; if names are duplicated, ask for a number instead.
- Support rescanning, canceling, and helpful error messages.
- Pair, trust and connect to the selected device using the system Bluetooth service.
- Prefer previously paired controller when appropriate; do not reprompt at every boot.
- Keep pairing UI separate from `servo_control.py` so normal robot operation never waits for text input.
- Avoid storing Bluetooth addresses or personal credentials in source code or Git history.
- Ensure a disconnected controller cannot cause unintended actuator movement; safe disconnect handling belongs in the eventual motor-control system.

Proposed implementation: invoke BlueZ via `bluetoothctl` from Python with robust command handling, timeouts and parsing; verify compatibility on the Orange Pi's installed Armbian/BlueZ version before claiming the tool works.

### Future no-laptop pairing option

A physical **Pair** button could launch discovery and pairing mode. An LED could indicate scanning, connection success, or failure. This is a planned usability feature, not currently wired or implemented.

## Existing verified Bluetooth notes

- Xbox controller previously paired/trusted over Bluetooth.
- Pygame identified the Bluetooth-connected controller, with 6 axes and 16 buttons (the previous USB connection reported 6 axes and 11 buttons).
- Reconnection was observed after powering controller off and on.
- One controller is used for robot control; support for operating with multiple controllers simultaneously is **not** part of the current milestone.

## Next steps

1. Create and locally review `bluetooth_pair.py` on the Windows laptop (no VS Code Remote-SSH needed).
2. Upload the utility over working USB SSH/SCP and test discovery and selection by number or name.
3. Validate new controller pairing and reboot reconnection; record exact results and known limitations.
4. Later evaluate a physical pairing button/LED.

See [portable USB development setup](usb_development_setup.md) and [servo demonstration](servo_demo_guide.md).
