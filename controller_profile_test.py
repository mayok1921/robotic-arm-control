#!/usr/bin/env python3
"""Read normalized controller inputs on Orange Pi; never sends motor commands."""
import time

from src.inputs import ControllerInput


def main():
    with ControllerInput() as device:
        if device.profile is None:
            print("Unknown mapping: use controller_input_test.py to inspect raw axes.")
            return
        if not device.profile.verified:
            print("Partial profile only; use controller_input_test.py for unmapped inputs.")
        print("Move joysticks and triggers. Ctrl+C to stop.")
        previous = None
        try:
            while True:
                readings = device.read_inputs()
                # Round for readable diagnostics, including D-pad tuples.
                current = {key: round(value, 2) if isinstance(value, float) else value
                           for key, value in readings.items()}
                if current != previous:
                    print(current)
                    previous = current
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("\nInput test stopped.")


if __name__ == "__main__":
    main()
