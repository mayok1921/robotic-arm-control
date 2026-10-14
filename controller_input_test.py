
import os
import time
import pygame

os.environ["SDL_VIDEODRIVER"] = "dummy"

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    pygame.quit()
    raise SystemExit("No controller detected.")

controller = pygame.joystick.Joystick(0)
controller.init()

print("Controller:", controller.get_name())
print("Axes:", controller.get_numaxes())
print("Buttons:", controller.get_numbuttons())
print("Hats:", controller.get_numhats())
print()
print("Tracking controller inputs...")
print("Press Ctrl+C to stop.")
print()

deadzone = 0.20
axis_change = 0.10

previous_buttons = [
    controller.get_button(i)
    for i in range(controller.get_numbuttons())
]

previous_axes = [
    None for _ in range(controller.get_numaxes())
]

previous_hats = [
    controller.get_hat(i)
    for i in range(controller.get_numhats())
]

try:
    while True:
        pygame.event.pump()

        # Track button presses and releases
        for i in range(controller.get_numbuttons()):
            state = controller.get_button(i)

            if state != previous_buttons[i]:
                action = "PRESSED" if state else "RELEASED"
                print(f"Button {i}: {action}")
                previous_buttons[i] = state

        # Track joystick and trigger movement
        for i in range(controller.get_numaxes()):
            value = controller.get_axis(i)

            if abs(value) < deadzone:
                value = 0.0

            previous = previous_axes[i]

            if previous is None or abs(value - previous) >= axis_change:
                print(f"Axis {i}: {value:+.2f}")
                previous_axes[i] = value

        # Track D-pad when mapped as a hat
        for i in range(controller.get_numhats()):
            state = controller.get_hat(i)

            if state != previous_hats[i]:
                print(f"D-pad {i}: {state}")
                previous_hats[i] = state

        time.sleep(0.02)

except KeyboardInterrupt:
    print("\nController tracking stopped.")

finally:
    pygame.quit()
