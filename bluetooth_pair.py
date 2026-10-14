
import re
import subprocess

scan_time = 12


def bluetooth_command(*arguments, timeout=20):
    try:
        result = subprocess.run(
            ["bluetoothctl", *arguments],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()

    except subprocess.TimeoutExpired:
        return False, "", "Bluetooth command timed out."

    except FileNotFoundError:
        return False, "", "bluetoothctl is not installed."


def scan_devices():
    print(f"\nScanning for Bluetooth devices ({scan_time} seconds)...")

    success, output, error = bluetooth_command(
        "--timeout", str(scan_time),
        "scan", "on",
        timeout=scan_time + 5
    )

    if not success:
        print("Scan warning:", error or output)

    success, output, error = bluetooth_command("devices")

    if not success:
        print("Unable to list Bluetooth devices:", error)
        return []

    devices = []

    for line in output.splitlines():
        match = re.match(
            r"^Device\s+([0-9A-Fa-f:]{17})\s+(.+)$",
            line
        )

        if match:
            address, name = match.groups()
            devices.append((address, name.strip()))

    return devices


def select_device(devices):
    print("\nAvailable Bluetooth devices:")

    for number, (address, name) in enumerate(devices, start=1):
        print(f"{number}. {name} ({address})")

    while True:
        selection = input(
            "\nSelect a device by number or name (q to quit): "
        ).strip()

        if selection.lower() == "q":
            return None

        if selection.isdigit():
            index = int(selection) - 1

            if 0 <= index < len(devices):
                return devices[index]

        matches = [
            device for device in devices
            if device[1].casefold() == selection.casefold()
        ]

        if len(matches) == 1:
            return matches[0]

        if len(matches) > 1:
            print("Multiple devices share that name. Select by number.")
        else:
            print("Device not found. Try again.")


def connect_device(address, name):
    print(f"\nSelected: {name}")

    success, info, error = bluetooth_command("info", address)

    if not success:
        print("Unable to check pairing status:", error or info)
        return

    if "Paired: yes" not in info:
        print("Pairing...")
        success, output, error = bluetooth_command(
            "pair", address, timeout=45
        )

        if not success or "Failed to pair" in output:
            print("Pairing failed:", error or output)
            return

    print("Trusting device...")
    success, output, error = bluetooth_command("trust", address)

    if not success:
        print("Trust failed:", error or output)
        return

    print("Connecting...")
    success, output, error = bluetooth_command(
        "connect", address, timeout=30
    )

    if success and "Failed to connect" not in output:
        print(f"\nConnected to {name}!")
    else:
        print("Connection failed:", error or output)


def main():
    devices = scan_devices()

    if not devices:
        print("No Bluetooth devices found.")
        return

    selected = select_device(devices)

    if selected is None:
        print("Pairing cancelled.")
        return

    address, name = selected
    connect_device(address, name)


if __name__ == "__main__":
    main()
