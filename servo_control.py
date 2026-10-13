import os
import time
import pygame
import serial

os.environ["SDL_VIDEODRIVER"] = "dummy"

servo = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
time.sleep(2)

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    servo.close()
    pygame.quit()
    raise SystemExit("No Xbox controller detected.")

controller = pygame.joystick.Joystick(0)
controller.init()

print("Controller:", controller.get_name())
print("Move the left joystick horizontally.")
print("Press Ctrl+C to stop.")

axis = 0
last_angle = None

try:
    while True:
        pygame.event.pump()

        value = controller.get_axis(axis)

        if abs(value) < 0.1:
            value = 0

        angle = round(90 + value * 45)
        angle = max(45, min(135, angle))

        if angle != last_angle:
            servo.write(f"{angle}\n".encode())
            last_angle = angle
            print(f"Servo angle: {angle}")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nStopping controller.")

finally:
    servo.close()
    pygame.quit()
