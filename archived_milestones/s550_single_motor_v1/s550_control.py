
import os
import time

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import serial

# Connection settings
serial_port = "/dev/ttyACM0"
baud_rate = 9600

# S550 command settings
neutral_pulse = 1500
min_pulse = 1250
max_pulse = 1750
deadzone = 0.20
max_offset = 250

# Smooth movement
update_interval = 0.05
max_step = 16  # Previously 8

# Confirmed PS5 button mapping
arm_button = 0       # Square
disarm_button = 1    # Cross


def apply_deadzone(value):
    if abs(value) <= deadzone:
        return 0.0

    direction = 1 if value > 0 else -1

    return direction * (
        (abs(value) - deadzone) / (1 - deadzone)
    )


def find_controller():
    pygame.joystick.init()

    for index in range(pygame.joystick.get_count()):
        device = pygame.joystick.Joystick(index)
        device.init()

        name = device.get_name().lower()

        if (
            "dualsense" in name
            or "wireless controller" in name
            or "sony" in name
        ):
            return device

    raise RuntimeError("PS5 controller not found.")


def send_command(arduino, command):
    arduino.write((command + "\n").encode())


def ramp_value(current, target):
    difference = target - current

    if abs(difference) <= max_step:
        return target

    if difference > 0:
        return current + max_step

    return current - max_step


pygame.init()

arduino = None
armed = False
current_pulse = neutral_pulse

try:
    controller = find_controller()
    controller_id = controller.get_instance_id()

    print("Controller:", controller.get_name())

    arduino = serial.Serial(
        serial_port,
        baud_rate,
        timeout=0.5,
        write_timeout=0.5
    )

    # Wait for Arduino Uno serial reset
    time.sleep(2)
    arduino.reset_input_buffer()

    # Explicitly verify the initial DISARM
    send_command(arduino, "DISARM")
    arduino.flush()

    response = arduino.readline().decode(
        errors="replace"
    ).strip()

    if response != "DISARMED":
        raise RuntimeError(
            f"Startup disarm not confirmed: {response!r}"
        )

    print("Arduino:", serial_port)
    print("Startup DISARM confirmed.")
    print()
    print("Square: ARM")
    print("Cross: DISARM")
    print("Left stick: Proportional movement")
    print("Ctrl+C: Exit")
    print()
    print("Motor control is DISARMED.")

    last_pulse = None

    while True:
        for event in pygame.event.get():

            if event.type == pygame.JOYDEVICEREMOVED:
                if event.instance_id == controller_id:
                    raise RuntimeError(
                        "PS5 controller disconnected."
                    )

            if event.type == pygame.JOYBUTTONDOWN:
                if event.instance_id != controller_id:
                    continue

                if event.button == disarm_button:
                    send_command(arduino, "DISARM")
                    armed = False
                    current_pulse = neutral_pulse
                    last_pulse = None
                    print("MOTOR DISARMED")

                elif event.button == arm_button:
                    if armed:
                        continue

                    joystick = controller.get_axis(0)

                    if abs(joystick) > deadzone:
                        print(
                            "Center joystick before arming."
                        )
                        continue

                    # Enable output deliberately
                    send_command(arduino, "ARM")
                    current_pulse = neutral_pulse
                    send_command(
                        arduino, f"P{current_pulse}"
                    )

                    armed = True
                    last_pulse = None

                    print("MOTOR ARMED")

        # Drain Arduino acknowledgments
        if arduino.in_waiting:
            response = arduino.read(
                arduino.in_waiting
            ).decode(errors="replace")

            for line in response.splitlines():
                if "TIMEOUT_DISARMED" in line:
                    armed = False
                    current_pulse = neutral_pulse
                    print("ARDUINO TIMEOUT - DISARMED")

        if armed:
            joystick = controller.get_axis(0)
            adjusted = apply_deadzone(joystick)

            target_pulse = round(
                neutral_pulse + adjusted * max_offset
            )

            target_pulse = max(
                min_pulse,
                min(max_pulse, target_pulse)
            )

            current_pulse = ramp_value(
                current_pulse,
                target_pulse
            )

            send_command(
                arduino,
                f"P{current_pulse}"
            )

            if current_pulse != last_pulse:
                print(
                    f"Stick: {joystick:+.2f} | "
                    f"Target: {target_pulse} us | "
                    f"Output: {current_pulse} us",
                    flush=True
                )
                last_pulse = current_pulse

        time.sleep(update_interval)

except KeyboardInterrupt:
    print("\nStopping program.")

except (
    RuntimeError,
    pygame.error,
    serial.SerialException,
    OSError
) as error:
    print("\nError:", error)

finally:
    if arduino is not None and arduino.is_open:
        try:
            send_command(arduino, "DISARM")
            arduino.flush()
        except (serial.SerialException, OSError):
            pass

        arduino.close()

    pygame.quit()
    print("Program closed.")

