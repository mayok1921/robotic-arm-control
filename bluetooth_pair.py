#!/usr/bin/env python3
"""Bluetooth controller discovery, pairing, reconnection and diagnostics (Linux/BlueZ).

No motor commands are sent. Requires bluetoothctl; no pip packages needed.
"""
import argparse
import errno
import pty
import select
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

MAC = re.compile(r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
DEVICE = re.compile(r"^Device\s+((?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})\s+(.+)$")
FIELD = re.compile(r"^\s*(Paired|Bonded|Trusted|Connected|Blocked):\s*(yes|no)\s*$", re.I | re.M)
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


def joystick_handlers(controller_name=None):
    """Check selected controller has a joystick node; another controller is insufficient."""
    lower = (controller_name or "").lower()
    expected = "dualsense" if "dualsense" in lower else "xbox" if "xbox" in lower else None
    nodes = set(path.name for path in Path("/dev/input").glob("js[0-9]*"))
    return [(name, handlers) for name, handlers in input_devices()
            if any(token in nodes for token in re.findall(r"\\bjs\\d+\\b", handlers))
            and (expected is None or expected in name.lower())]


def hid_diagnostics():
    """Read-only local diagnosis; never modify kernel drivers or Bluetooth bonds."""
    print("\nAutomatic HID diagnostic:")
    print("  Kernel:", os.uname().release)
    for name in ("hidp", "uhid", "hid_playstation", "hid_generic", "joydev"):
        module = Path("/sys/module") / name
        print(f"  {name}: {'present (loaded or built-in)' if module.exists() else 'not exposed in /sys/module'}")
    try:
        config = Path("/boot/config-" + os.uname().release).read_text(errors="replace")
    except OSError:
        config = ""
    if config:
        for name in ("CONFIG_BT_HIDP", "CONFIG_UHID", "CONFIG_INPUT_JOYDEV",
                     "CONFIG_HID_PLAYSTATION", "CONFIG_HID_SONY"):
            match = re.search(r"^(?:" + name + r"=.*|# " + name + r" is not set)$", config, re.M)
            print("  " + (match.group(0) if match else name + ": not listed"))
    else:
        print("  Kernel configuration file unavailable.")
    print("  Bluetooth can connect without exposing a usable Linux input device.")
    print("  If input remains absent, kernel/BlueZ HID support may require system-level repair.")
    config = Path("/etc/bluetooth/input.conf")
    if config.is_file():
        try:
            contents = config.read_text(errors="replace")
            match = re.search(r"(?im)^\s*ClassicBondedOnly\s*=\s*(true|false)", contents)
            print("  BlueZ ClassicBondedOnly:", match.group(1) if match else "default (true)")
        except OSError:
            print("  BlueZ input.conf: unreadable")
    else:
        print("  BlueZ ClassicBondedOnly: default (true), unless configured elsewhere")
    if shutil.which("journalctl"):
        try:
            logs = subprocess.run(
                ["journalctl", "-u", "bluetooth", "--since", "-10 minutes",
                 "--no-pager", "-o", "cat"],
                capture_output=True, text=True, timeout=8
            ).stdout
            matches = [line.strip() for line in logs.splitlines()
                       if re.search(r"(?i)bond|hidp|uhid|input|reject|auth|permission|fail", line)]
            if matches:
                print("  Recent Bluetooth service messages:")
                for line in matches[-8:]:
                    print("   ", line[:240])
            else:
                print("  No relevant Bluetooth service messages available.")
        except (OSError, subprocess.TimeoutExpired):
            print("  Bluetooth service logs unavailable.")
    print("  No kernel or system settings were changed.")


def report(address, name, input_wait=10):
    print(f"\\nBluetooth status: {name} [{address}]")
    info = state(address)
    for key in ("paired", "bonded", "trusted", "connected", "blocked"):
        val = info.get(key)
        print(f"  {key.title():10} {'yes' if val else 'no' if val is False else 'unknown'}")
    if info.get("bonded") is False:
        print("  WARNING: BlueZ reports Bonded: no; reconnection after restart may fail.")
    if not all(info.get(k) for k in ("paired", "trusted", "connected")):
        print("\\RESULT: Bluetooth setup incomplete.")
        return False
    print(f"\\nChecking Linux joystick registration (up to {input_wait} seconds)...")
    deadline = time.monotonic() + input_wait
    while True:
        inputs = joystick_handlers(name)
        if inputs:
            if not state(address).get("connected"):
                print("RESULT: Bluetooth disconnected during input registration.")
                return False
            for devname, handlers in inputs:
                print(f"  {devname} — {handlers}")
            print("RESULT: Bluetooth connected and Linux joystick node detected.")
            print("IMPORTANT: Test actual input events before controlling motors.")
            return True
        if time.monotonic() >= deadline:
            break
        time.sleep(0.5)
    if not state(address).get("connected"):
        print("RESULT: Bluetooth disconnected before input became available.")
    else:
        print("RESULT: Bluetooth connected, but NO usable Linux joystick was registered.")
    hid_diagnostics()
    return False


def pair_interactively(address, timeout=55):
    """Keep BlueZ pairing agent alive until the bond is confirmed.

    Previous one-shot bluetoothctl invocation could exit before authorization.
    KeyboardDisplay supports explicit pairing authorization; if BlueZ still asks for human
    authorization, forward that request in this program rather than silently
    approving unknown nearby devices.
    """
    if not MAC.fullmatch(address):
        raise BTError("Invalid Bluetooth MAC address")
    master, slave = pty.openpty()
    process = None
    recent = ""
    try:
        process = subprocess.Popen(
            ["bluetoothctl", "-a", "KeyboardDisplay"],
            stdin=slave, stdout=slave, stderr=slave,
            close_fds=True, start_new_session=True
        )
        os.close(slave)
        slave = -1

        def send(command):
            os.write(master, (command + "\n").encode())

        send("power on")
        send("agent KeyboardDisplay")
        send("default-agent")
        send("pair " + address)
        deadline = time.monotonic() + timeout
        last_check = 0.0
        approved_prompt = False
        while time.monotonic() < deadline:
            readable, _, _ = select.select([master], [], [], 0.5)
            if readable:
                try:
                    chunk = os.read(master, 4096).decode("utf-8", "replace")
                except OSError as exc:
                    if exc.errno == errno.EIO:
                        break
                    raise
                if not chunk:
                    break
                # Remove ANSI terminal color codes and control characters.
                clean = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", chunk)
                recent = (recent + clean)[-6000:]
                if "Accept pairing (yes/no)" in recent and not approved_prompt:
                    print("\nBlueZ requested pairing authorization.")
                    print("Approve ONLY if the request is for the selected controller.")
                    try:
                        answer = input("Accept pairing request? [y/N]: ").strip().lower()
                    except (EOFError, KeyboardInterrupt):
                        answer = "n"
                    send("yes" if answer in ("y", "yes") else "no")
                    approved_prompt = True
                    recent = ""
                if re.search(r"(?i)Failed to pair|AuthenticationFailed|AuthenticationCanceled", recent):
                    raise BTError("BlueZ pairing failed: " + recent[-600:])
            if process.poll() is not None:
                break
            now = time.monotonic()
            if now - last_check >= 1:
                last_check = now
                try:
                    if state(address).get("paired"):
                        return True
                except BTError:
                    pass
        return bool(state(address).get("paired"))
    finally:
        if process and process.poll() is None:
            try:
                os.write(master, b"quit\n")
                process.wait(timeout=2)
            except (OSError, subprocess.TimeoutExpired):
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
        try:
            os.close(master)
        except OSError:
            pass
        if slave >= 0:
            os.close(slave)


def connect(address, name, retries=1):
    info = state(address)
    # Paired is not the same as bonded. BlueZ usually requires a stored
    # Bluetooth bond before its input profile will expose HID events.
    if info.get("paired") and info.get("bonded") is False:
        print("\nThis controller is paired but NOT bonded.")
        print("BlueZ may refuse joystick input from an unbonded controller.")
        print("The program can forget and re-pair ONLY this selected controller.")
        print("This does not alter the Xbox pairing or change kernel settings.")
        try:
            approval = input("Repair this controller pairing now? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            approval = "n"
        if approval in ("y", "yes"):
            bt("remove", address)
            print("Selected controller pairing removed. Hold Create + PS")
            print("until the DualSense flashes rapidly, then press Enter.")
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                raise BTError("Pairing reset cancelled before re-pairing.")
            info = {"paired": False}
        else:
            print("Retaining current pairing; continuing diagnostics.")
    if info.get("blocked"):
        raise BTError("Device is blocked; inspect Bluetooth settings.")
    if not info.get("paired"):
        print("Pairing... (put controller in pairing mode)")
        ok = pair_interactively(address)
        if not ok:
            raise BTError("Pairing not verified. Check controller pairing mode, charge, and BlueZ logs.")
        info = state(address)
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
        print("\nController ready for joystick event testing.")
        print("IMPORTANT: controller HID input must still be tested before motor use.")
    else:
        print("\nNOT READY: Bluetooth and joystick input requirements were not both met.")
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
        print("The program will report input/HID diagnostics when Bluetooth connects without joystick support.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
