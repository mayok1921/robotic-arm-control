"""Pygame controller adapter for headless Linux (no motor commands)."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from .controller_profiles import identify_controller, input_snapshot


class ControllerInput:
    def __enter__(self):
        import pygame
        self.pygame = pygame
        pygame.init()
        pygame.joystick.init()
        if not pygame.joystick.get_count():
            pygame.quit()
            raise RuntimeError("No joystick detected; connect controller first")
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.profile = identify_controller(
            self.controller.get_name(), self.controller.get_numaxes(),
            self.controller.get_numbuttons(), self.controller.get_numhats())
        print("Controller:", self.controller.get_name())
        print("Detected profile:", self.profile.family if self.profile else "unknown (raw axes only)")
        return self

    def _ensure_attached(self):
        self.pygame.event.pump()
        if not self.controller.get_init() or not self.controller.get_attached():
            raise RuntimeError("Controller disconnected; stopping commands")

    def read_axis(self, index: int) -> float:
        """Backward-compatible raw axis access used by experimental control.py."""
        self._ensure_attached()
        return float(self.controller.get_axis(index))

    def read_inputs(self, deadzone=0.12):
        self._ensure_attached()
        if self.profile is None:
            raise RuntimeError("Controller mapping unverified; test raw inputs first")
        return input_snapshot(self.controller, self.profile, deadzone)

    def __exit__(self, *_):
        self.pygame.quit()


# Preserve current experimental runner's import, without changing servo operation.
XboxInput = ControllerInput
