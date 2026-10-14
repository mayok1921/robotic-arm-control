
import os
import time
import pygame
import serial

os.environ["SDL_VIDEODRIVER"] = "dummy"

# Settings
servo_port = "/dev/ttyACM0"
servo_pin_min = 45
servo_pin_max = 135
servo_speed = 60  # degrees per second
deadzone = 0.20
update_interval = 0.02

def apply_deadzone(value):
    if abs(value) <= deadzone:
        return 0.0

    direction = 1 if value > 0 else -1
    adjusted = (abs(value) - deadzone) / (1 - deadzone)

    return direction * adjusted

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    pygame.quit()
    raise SystemExit("No Xbox controller detected.")

controller = pygame.joystick.Joystick(0)
controller.init()

arduino = serial.Serial(servo_port, 9600, timeout=1)
time.sleep(2)

angle = 90.0
last_sent = None
last_time = time.monotonic()

print("Controller:", controller.get_name())
print("Move left joystick horizontally.")
print("Ctrl+C to stop.")

try:
    while True:
        pygame.event.pump()

        now = time.monotonic()
        dt = min(now - last_time, 0.1)
        last_time = now

        joystick = apply_deadzone(controller.get_axis(0))

        # Joystick controls movement speed, not position.
        angle += joystick * servo_speed * dt
        angle = max(servo_pin_min, min(servo_pin_max, angle))

        target = round(angle)

        if target != last_sent:
            arduino.write(f"{target}\n".encode())
            last_sent = target
            print(f"Servo angle: {target}")

        time.sleep(update_interval)

except KeyboardInterrupt:
    print("\nStopping.")

finally:
    arduino.close()
    pygame.quit()
