# Reproduction guide: Xbox controller to SG90 servo

**Verified milestone: October 13, 2026.** A Bluetooth Xbox controller moved an SG90 servo using the Orange Pi Zero 2W and an Arduino UNO R3.

## Hardware

- Orange Pi Zero 2W running Armbian Linux
- Arduino UNO R3 and compatible USB cable
- SG90 micro servo, unloaded for this demonstration
- Three male-to-male jumper wires for the servo's 3-pin female plug
- USB hub connected to the Orange Pi's USB/OTG port
- Xbox wireless controller (paired over Bluetooth)
- Suitable power for the Orange Pi

The Arduino is a low-level servo controller. The Orange Pi reads the controller and decides the target position. The final robotic arm's motor-control hardware remains to be selected.

## 1. Wire the SG90

**Unplug the Arduino while wiring.**

| SG90 wire | Arduino UNO R3 |
| --- | --- |
| Brown / ground | GND |
| Red / supply | 5V |
| Orange / control signal | D9 |

This 5V connection was used only for **one small unloaded SG90** during bench testing. For additional servos or loaded motors, choose an appropriately rated separate motor power supply and common ground. Never power motors from Orange Pi GPIO pins. Stop testing if the servo stalls, buzzes persistently, heats up, or the board resets.

## 2. Verify the servo on the Arduino first

Connect the Arduino to a development computer, open Arduino IDE, select **Arduino Uno** and the correct port. Upload a basic Servo-library sketch that commands 45°, 90°, and 135° with one-second delays. Verify that the unloaded servo moves.

## 3. Upload the serial-command firmware

Open [servo_serial.ino](../arduino/servo_serial/servo_serial.ino) in Arduino IDE and upload it. This replaces the automatic sweep.

- Serial rate: **9600 baud**
- Initial servo position: **90°**
- Input: ASCII angle, e.g. `45` followed by newline
- Target angle: **0–180°** (the Python demo limits commands to 45–135°)
- Responses: `READY` on startup and `ANGLE:<value>` when accepted

**Prototype limitation:** This is the *verified demonstration firmware*, not production safety firmware. It uses `Serial.parseInt()`, which can interpret malformed input or a leftover line ending as zero. Add robust line-based parsing and command timeouts before connecting a loaded arm.

Disconnect the Arduino from the development computer and plug it into the Orange Pi's USB hub.

## 4. Confirm USB serial access on the Orange Pi

Run:

```bash
ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null
```

In this build the Arduino appeared as **`/dev/ttyACM0`**. Device names may change after reconnecting.

Install the Python serial package if needed:

```bash
sudo apt update
sudo apt install python3-serial
python3 -c "import serial; print(serial.__version__)"
```

The tested version was **PySerial 3.5**. Ensure Pygame is installed and the Xbox controller is paired; see [controller_test.py](../controller_test.py) for detection.

Optional manual serial check:

```bash
python3 -m serial.tools.miniterm /dev/ttyACM0 9600
```

Send `45` plus Enter to request a servo position. Exit with **Ctrl + ]** before running Python so the serial port is free. The servo movement was verified in this test.

If you encounter permission errors, check the serial device permissions and the user's group membership rather than running the entire control script as root.

## 5. Run the combined controller demo

With the Arduino plugged into the Orange Pi and the Xbox controller connected via Bluetooth:

```bash
cd ~/robotic_arm
python3 servo_control.py
```

Move the **left joystick horizontally**:

| Input | Servo target |
| --- | --- |
| Full left | approximately 45° |
| Center | 90° |
| Full right | approximately 135° |

The script sends a new angle when it changes, uses a small joystick deadzone, and exits with **Ctrl+C**. The tested setup successfully moved the servo with the wireless joystick.

The demo uses axis index `0` and port `/dev/ttyACM0`. Confirm and adapt these values if your device mapping differs. It controls **position**, not calibrated servo speed.

## 6. Current limitations and next work

- Automatic startup of the **robot application** is **not yet configured**; direct, Wi-Fi-free USB development access is now configured and tested after an Orange Pi reboot.
- **USB networking is now verified**: Windows connects over USB0 to the Orange Pi at `192.168.7.2` using SSH/VS Code, while Arduino remains connected through a USB hub on USB1. See [portable USB setup](usb_development_setup.md).
- Hardware safety features, lost-controller behavior, communications watchdog, and validated joint limits are **not yet implemented**. Do not use this prototype to drive a loaded robotic arm.
- The D-pad mapping needs further testing.
- The Orange Pi previously experienced freezes while using VS Code Remote-SSH; system stability needs additional testing.

## Verified signal path

**Xbox controller (Bluetooth) → Orange Pi Zero 2W (Python/Pygame) → USB serial (PySerial, 9600) → Arduino UNO R3 (Servo library) → SG90 servo**.

This proves the control chain, not the suitability of the final robotic arm actuators.
