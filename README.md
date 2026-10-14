# Robotic Arm Control System

Portable robotic-arm controller based on an **Xbox wireless controller → Orange Pi → USB serial → Arduino → actuators**.

**Project intent:** The Orange Pi, Arduino UNO and unloaded SG90 used in the demonstration are **personal development hardware**. The group's robot already has an Arduino and motors; **reuse those components** and purchase dedicated computer/control hardware only where needed.

## Project status (October 13, 2026)

| Capability | Status |
| --- | --- |
| Wireless Xbox controller recognized by Orange Pi | **Verified** |
| Python/Pygame sends USB serial commands to Arduino | **Verified** |
| Arduino drives one unloaded SG90 from controller | **Verified** |
| Laptop SSH/SCP to Orange Pi over USB without Wi-Fi | **Verified** |
| Xbox auto-reconnect after power cycling controller | **Observed** |
| SG90 reliable over extended operation | **Unresolved** (occasionally stops moving) |
| New modular Python runner and stricter Arduino firmware | **Written, untested on hardware** |
| Number-or-name Bluetooth pairing tool | **Prototype tested locally for discovery only; not yet checked into this repository** |
| Multi-motor group robot and safe auto-start | **Not implemented** |

## Repository layout

```text
robotic-arm-control/
├── README.md
├── requirements.txt
├── servo_control.py                # ORIGINAL, tested Python bench demo
├── controller_test.py              # ORIGINAL controller inspection
├── src/                            # NEW, experimental modular Python code
│   ├── control.py
│   ├── inputs.py
│   ├── motion.py
│   └── transport.py
├── config/settings.json            # NEW, experimental control settings
├── arduino/
│   ├── servo_serial/               # ORIGINAL, tested Arduino sketch
│   └── servo_serial_v2/            # NEW, strict line-command sketch; untested
├── tests/                           # pure software tests
├── scripts/                         # USB network service and deployment
└── docs/                            # guides, hardware plan and test history
```

**Important:** The legacy sketch expects plain `90\n` angle messages. The experimental v2 sketch expects `SET 90\n` and acknowledges with `OK 90`. **These two protocols are NOT interchangeable.** Keep using the legacy Python + legacy Arduino pair until intentionally testing both experimental files together.

## Start here

- [Verified servo demonstration](docs/servo_demo_guide.md) — bench wiring and original program
- [USB development setup](docs/usb_development_setup.md) — Windows RNDIS, Orange Pi USB0/USB1, SSH and troubleshooting
- [Headless / local development](docs/headless_setup.md) — recommended laptop workflow
- [Experimental modular Python](src/README.md) — new isolated controller design and limitations
- [Integration plan](docs/integration_plan.md) — how to transfer to the group's robot
- [Preliminary bill of materials](docs/bill_of_materials.md) — reuse/buy/verify decisions
- [Bluetooth pairing plan](docs/bluetooth_pairing_design.md)
- [Development log](docs/development_log.md)

## Development workflow

Use **Windows VS Code locally**, not VS Code Remote-SSH. The Orange Pi has only 1GB RAM; previous Pylance/remote-server processes consumed hundreds of MiB.

1. Develop on the laptop; from a local PowerShell terminal, use `git pull --rebase origin main` before making local changes.
2. Check and run **hardware-independent** tests with `python -m unittest discover -s tests -v`.
3. Deploy via `scp` or `scripts/deploy.ps1` using the working USB link to `192.168.7.2`.
4. Test from a lightweight terminal: `ssh mayok1921@192.168.7.2`. Use legacy `python3 servo_control.py` for known bench firmware; only run `python3 -m src.control` when the matching **v2 Arduino firmware is installed**.
5. Commit/push only tested or clearly labeled experimental changes; keep an up-to-date development log.

## Next work

1. Verify bench reliability and power distribution without overinvesting in SG90 demonstration hardware.
2. Test v2 serial parsing, acknowledgement, deadzone and controller-disconnection behavior on **one unloaded servo**.
3. Identify the **group's Arduino model**, **existing motor and driver models**, voltage/current, available feedback and mechanical limits.
4. Add an actuator-independent multi-joint interface, appropriate hardware watchdog, e-stop, joint limits and safe boot behavior.
5. Select one appropriately protected main power supply and dedicated SBC based on actual robot requirements, then integrate one axis at a time.
6. Configure safe automatic startup and reconnection after failure handling is proven.

**Safety:** This is a bench proof of concept, not a safety-qualified controller. Do not connect experimental code directly to a loaded arm.
