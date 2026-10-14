"""Pygame joystick adapter. Runs only on the Orange Pi."""

import os

# Headless Linux does not need a video window.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame  # noqa: E402


class XboxInput:
    def __enter__(self):
        pygame.init()
        pygame.joystick.init()
        if not pygame.joystick.get_count():
            pygame.quit()
            raise RuntimeError("No joystick detected; connect controller first")
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        print("Controller:", self.controller.get_name())
        return self

    def read_axis(self, index: int) -> float:
        pygame.event.pump()
        if not self.controller.get_init() or not self.controller.get_attached():
            raise RuntimeError("Controller disconnected; stopping commands")
        return float(self.controller.get_axis(index))

    def __exit__(self, *_):
        pygame.quit()
