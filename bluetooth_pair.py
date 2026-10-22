#!/usr/bin/env python3
"""Bluetooth controller discovery, pairing, reconnection and diagnostics (Linux/BlueZ).

No motor commands are sent. Requires bluetoothctl; no pip packages needed.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

MAC = re.compile(r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
DEVICE = re.compile(r"^Device\s+((?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})\s+(.+)$")
FIELD = re.compile(r"^\s*(Paired|Trusted|Connected|Blocked):\s*(yes|no)\s*$", re.I | re.M)
GAMEPAD = re.compile(r"dualsense|wireless controller|playstation|sony|xbox|gamepad", re.I)


class BTError(Exception):
    pass


def bt(*args, timeout=20, allow_failure=False):
    try:
        result = subprocess.run(["bluetoothctl", *args], capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError as exc:
        raise BTError("bluetoothctl is unavailable. Install/configure BlueZ.") from exc
    except subprocess.TimeoutExpired as exc:
        raise BTError("Bluetooth operation timed out: " + " ".join(args)) from exc
    output = "\n".join(x for x in (result.stdout.strip(), result.stderr.strip()) if x)
    failed = re.search(r"(?im)^\s*(Failed to|Error:|No default controller|Device .* not available)", output)
    if (result.returncode != 0 or failed) and not allow_failure:
        raise BTError(output or "bluetoothctl returned " + str(result.returncode))
    return output


def parse_devices(output):
    found = {}
    for line in output.splitlines():
        match = DEVICE.match(line.strip())
        if match:
            address, name = match.groups()
            found[address.upper()] = (address.upper(), name.strip())
    return sorted(found.values(), key=lambda item: (item[1].casefold(), item[0]))


def parse_info(info):
    return {key.lower(): val.lower() == "yes" for key, val in FIELD.findall(info)}


def device_info(address):
    if not MAC.fullmatch(address):
        raise BTError("Invalid Bluetooth MAC address")
    return bt("info", address)


def state(address):
    return parse_info(device_info(address))


def devices():
    return parse_devices(bt("devices"))


def scan(seconds):
    print("\nScanning for", seconds, "seconds. Put the controller in pairing mode.")
    try:
        output = bt("--timeout", str(seconds), "scan", "on", timeout=seconds + 8, allow_failure=True)
        if re.search(r"(?i)no default controller|failed to start discovery", output):
            print("Scan warning:", output)
    except BTError as exc:
        print("Scan warning:", exc)
    return devices()  # May include BlueZ cached discoveries, not only fresh scan hits.


def choose(found):
    if not found:
        print("No devices listed. Check Bluetooth power and pairing mode.")
        return None
    print("\nDevices (may include previously discovered devices):")
    for i, (address, name) in enumerate(found, 1):
        print(f"  {i}. {name} [{address}]")
    while True:
        try:
            entry = input("\nNumber, exact name, MAC, [r]escan, [q]uit: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if entry.lower() == "q":
            return None
        if entry.lower() == "r":
            return "rescan"
        if entry.isdecimal() and 1 <= int(entry) <= len(found):
            return found[int(entry) - 1]
        matches = [item for item in found if entry.casefold() == item[1].casefold()
                   or entry.upper() == item[0]]
        if len(matches) == 1:
            return matches[0]
        print("Multiple devices have that name; use a number." if matches else "Unknown selection.")


def input_devices():
    try:
        content = Path("/proc/bus/input/devices").read_text(errors="replace")
    except OSError:
        return []
    output = []
    for block in content.strip().split("\n\n"):
        name = re.search(r'^N:\s+Name="([^"]+)"', block, re.M)
        if name and GAMEPAD.search(name.group(1)):
            handlers = re.search(r"^H:\s+Handlers=(.+)$", block, re.M)
            output.append((name.group(1), handlers.group(1) if handlers else "unknown"))
    return output


def wait_for(address, key, value=True, seconds=6):
    end = time.monotonic() + seconds
    last = {}
    while True:
        try:
            last = state(address)
        except BTError:
            pass
        if last.get(key) is value:
            return True, last
        if time.monotonic() >= end:
            return False, last
        time.sleep(0.7)


def report(address, name):
    info = state(address)
    print(f"\nBluetooth status: {name} [{address}]")
    for key in ("paired", "trusted", "connected", "blocked"):
        print(f"  {key.title():10} {'yes' if info.get(key) else 'no/unknown'}")
    inputs = input_devices()
    if inputs:
        print("\nGame-controller-like Linux inputs:")
        for devname, handlers in inputs:
            print(f"  {devname} — {handlers}")
        print("Input node detected; test actual button/axis events separately.")
    else:
        print("\nNo game-controller-like Linux input devices detected.")
        print("Bluetooth connection does not prove that a PlayStation HID driver works.")
    return all(info.get(k) for k in ("paired", "trusted", "connected"))


def connect(address, name, retries=1):
    info = state(address)
    if info.get("blocked"):
        raise BTError("Device is blocked; inspect Bluetooth settings.")
    if not info.get("paired"):
        print("Pairing... (put controller in pairing mode)")
        output = bt("pair", address, timeout=50)
        ok, info = wait_for(address, "paired")
        if not ok:
            raise BTError("Pairing not verified: " + output)
    if not info.get("trusted"):
        print("Trusting...")
        bt("trust", address)
        ok, info = wait_for(address, "trusted")
        if not ok:
            raise BTError("Trusted: yes was not verified.")
    if not info.get("connected"):
        for attempt in range(retries + 1):
            print(f"Connecting, attempt {attempt + 1}/{retries + 1}...")
            try:
                bt("connect", address, timeout=30)
            except BTError as exc:
                print("Connection attempt:", exc)
            ok, info = wait_for(address, "connected", seconds=5)
            if ok:
                break
            if attempt < retries:
                time.sleep(1)
    success = report(address, name)
    if success:
        print("\nPaired, trusted and connected at time of check.")
        print("IMPORTANT: controller HID input must still be tested before motor use.")
    else:
        print("\nINCOMPLETE: paired/trusted/connected status was not fully verified.")
    return success


def diagnose():
    print("Bluetooth adapter:")
    print(bt("show"))
    print("\nKernel:", os.uname().release)
    print("\nController-like input devices:")
    print(input_devices() or "  None registered")
    config = Path("/boot/config-" + os.uname().release)
    if config.is_file():
        text = config.read_text(errors="replace")
        for key in ("CONFIG_HID_PLAYSTATION", "CONFIG_HID_SONY", "CONFIG_INPUT_JOYDEV", "CONFIG_UHID"):
            match = re.search(r"^(?:" + key + r"=.*|# " + key + r" is not set)$", text, re.M)
            print(match.group(0) if match else key + ": not listed")
    else:
        print("Kernel config unavailable.")
    print("This utility cannot install missing kernel HID drivers.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Bluetooth pairing and diagnostics for Linux game controllers")
    parser.add_argument("--scan-seconds", type=int, default=12)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--list", action="store_true", help="List known devices")
    parser.add_argument("--diagnose", action="store_true", help="Adapter, kernel and input information")
    parser.add_argument("--reconnect", metavar="MAC", help="Reconnect previously known controller")
    args = parser.parse_args(argv)
    if not 3 <= args.scan_seconds <= 60 or not 0 <= args.retries <= 3:
        parser.error("--scan-seconds must be 3-60 and --retries must be 0-3")
    if not shutil.which("bluetoothctl"):
        print("bluetoothctl not found (BlueZ required).", file=sys.stderr)
        return 2
    try:
        if args.diagnose:
            diagnose()
            return 0
        bt("power", "on", timeout=15)
        if args.list:
            for i, (address, name) in enumerate(devices(), 1):
                print(f"{i}. {name} [{address}]")
            return 0
        if args.reconnect:
            address = args.reconnect.upper()
            info = device_info(address)
            match = re.search(r"^\s*Name:\s*(.+)$", info, re.M)
            return 0 if connect(address, match.group(1) if match else address, args.retries) else 1
        while True:
            selection = choose(scan(args.scan_seconds))
            if selection == "rescan":
                continue
            if selection is None:
                print("Cancelled.")
                return 0
            address, name = selection
            return 0 if connect(address, name, args.retries) else 1
    except BTError as exc:
        print("ERROR:", exc, file=sys.stderr)
        print("Check controller charge/pairing mode. Try --diagnose.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
