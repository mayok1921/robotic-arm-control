# Headless and offline development plan

**Goal:** edit code on a computer, transfer it over a direct cable, and run it on the Orange Pi Zero 2W without Wi-Fi, display, or keyboard on the board.

## Phase 1 — Identify a supported wired connection
1. With existing access to the Orange Pi terminal, run:
   ```bash
   ls /sys/class/udc
   ```
2. Record the output, the Armbian kernel (`uname -a`), and the USB port in use.
3. Check the board's USB device/gadget capability and power arrangement **before** configuring any gadget modules.
4. If supported, configure USB Ethernet gadget networking and a stable host/device IP pair, then test SSH.
5. If unsupported, evaluate a USB-to-UART serial console for administration or a compatible wired Ethernet interface for SSH.

**Status:** Not configured or tested. Do not disable existing network access until the wired path works.

## Phase 2 — SSH and file transfer
- Establish an SSH session from the development computer over the verified wired link.
- Use SCP or a local Git checkout to transfer files; the Orange Pi does not need GitHub access.
- Test a file transfer and execute `controller_test.py`.

## Phase 3 — Autonomous execution
- Create a systemd service **after** the actual controller program is working.
- Define a safe startup state, a shutdown procedure, and recovery behavior if the controller disconnects.
- Confirm restart and boot behavior with actuators disconnected.

## Power and security
- USB/OTG data connectivity does not guarantee adequate power delivery.
- Use a reliable, documented power supply arrangement; avoid connecting two power sources without verifying the board's electrical requirements.
- Change default passwords, use SSH keys where possible, and keep credentials out of Git.
