"""UNTESTED single-servo runner for Arduino servo_serial_v2 firmware.

Run from repository root: python3 -m src.control
Do not run against the original servo_serial.ino protocol.
Not safe for a loaded robotic arm.
"""

import json
import time
from pathlib import Path

from .motion import next_angle


ROOT = Path(__file__).resolve().parent.parent


def main():
    from .inputs import XboxInput
    from .transport import ArduinoServoTransport

    config = json.loads((ROOT / "config" / "settings.json").read_text())
    servo = config["servo"]
    loop = config["control"]
    angle = float(servo["initial_angle"])
    last_sent = None

    with XboxInput() as controller, ArduinoServoTransport(
        config["serial"]["port"], config["serial"]["baudrate"]
    ) as arduino:
        previous = time.monotonic()
        try:
            while True:
                axis = controller.read_axis(loop["axis"])
                now = time.monotonic()
                dt = now - previous
                previous = now
                angle = next_angle(
                    angle, axis, dt, loop["degrees_per_second"],
                    servo["min_angle"], servo["max_angle"], loop["deadzone"]
                )
                rounded = round(angle)
                if rounded != last_sent:
                    arduino.send_angle(rounded)
                    last_sent = rounded
                    print("Acknowledged angle:", rounded)
                time.sleep(loop["update_interval_seconds"])
        except KeyboardInterrupt:
            print("\nStopped by user")
        except RuntimeError as error:
            # Stop generating new commands; servo continues to hold its last
            # commanded position, which is NOT sufficient for a loaded arm.
            print("Control halted:", error)
            raise SystemExit(1)


if __name__ == "__main__":
    main()
