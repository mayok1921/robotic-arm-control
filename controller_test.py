import pygame

pygame.init()
pygame.joystick.init()

count = pygame.joystick.get_count()

print("Controllers detected:", count)

for i in range(count):
    controller = pygame.joystick.Joystick(i)
    controller.init()

    print("Controller:", controller.get_name())
    print("Axes:", controller.get_numaxes())
    print("Buttons:", controller.get_numbuttons())
