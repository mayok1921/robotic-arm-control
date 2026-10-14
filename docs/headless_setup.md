# Headless development — verified USB method

**Status (October 13, 2026):** Wired USB SSH/VS Code from Windows to Orange Pi Zero 2W works **without Orange Pi Wi-Fi**. USB networking reconnected after reboot; automatic robot application startup is **not yet configured**.

Follow the complete [portable USB development instructions](usb_development_setup.md).

## Proven workflow

1. Connect Windows laptop with a data cable to the **USB0 gadget-capable USB-C port** on Orange Pi.
2. Orange Pi uses `g_ether`, the `usb0` interface, and `192.168.7.2/24` via an enabled systemd service.
3. Windows recognizes **USB Ethernet/RNDIS Gadget** after installing a matching signed RNDIS driver; its USB network adapter uses `192.168.7.1/24`.
4. Connect `ssh mayok1921@192.168.7.2` from Windows, or use VS Code Remote-SSH and select Linux.
5. Open `~/robotic_arm`, edit files and run Python. The Arduino may remain on the separate Orange Pi USB1 port via a hub.

USB Wi-Fi-free access was verified with the Orange Pi Wi-Fi radio disabled and a responsive SSH terminal. No local TV/keyboard needed for normal development when the USB connection works.

## Further work

- Test clean power-on/off and Windows laptop reboot persistence.
- Set up authorized per-developer SSH keys, recovery and onboarding.
- Define safe automatic startup for robot program (separate from USB networking).
- Verify stability with servos/controllers attached; never power a loaded arm from Arduino 5V.

Original investigation found that using the wrong physical USB-C port leaves the Linux gadget `not attached`, even while `g_ether` is loaded. Refer to the full guide rather than changing kernel/device-tree files.
