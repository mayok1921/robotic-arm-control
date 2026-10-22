"""Controller-independent input names and proven/partial hardware profiles.

Pure Python: can be tested without Pygame, Bluetooth, or motors.
DualSense mapping verified with wired USB Pygame on Orange Pi, 2026-10-22.
Bluetooth mappings may differ; inspect them separately before motor control.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ControllerProfile:
    family: str
    connection: str
    axes: dict
    triggers: dict
    hat: int | None = None
    verified: bool = False


DUALSENSE_USB = ControllerProfile(
    family="dualsense", connection="usb",
    axes={"left_x": 0, "left_y": 1, "right_x": 2, "right_y": 5},
    triggers={"left_trigger": 3, "right_trigger": 4},
    hat=0, verified=True,
)

# Only left stick horizontal was used in the working Xbox Bluetooth SG90 demo.
# Other Xbox axis assignments need fresh confirmation before integration.
XBOX_PARTIAL = ControllerProfile(
    family="xbox", connection="unverified",
    axes={"left_x": 0}, triggers={}, verified=False,
)


def identify_controller(name, num_axes=None, num_buttons=None, num_hats=None):
    """Return a safe profile if we recognize the signature, else None.

    PS5 profile is specifically from the wired-USB signature. Bluetooth isn't
    presumed equivalent; nonmatching signatures are intentionally rejected.
    """
    n = name.casefold()
    if "dualsense" in n or "sony interactive entertainment" in n:
        if (num_axes, num_buttons, num_hats) == (6, 15, 1):
            return DUALSENSE_USB
        return None
    if "xbox" in n or "microsoft" in n:
        return XBOX_PARTIAL
    return None


def joystick_value(raw, deadzone=0.12):
    """Signed stick displacement [-1, 1], with rescaled center deadzone."""
    if not 0 <= deadzone < 1:
        raise ValueError("deadzone must be in [0, 1)")
    raw = max(-1.0, min(1.0, float(raw)))
    amount = abs(raw)
    if amount <= deadzone:
        return 0.0
    return (1 if raw > 0 else -1) * (amount - deadzone) / (1.0 - deadzone)


def trigger_value(raw):
    """Normalize a DualSense trigger axis (-1 released, +1 fully pressed)."""
    return max(0.0, min(1.0, (float(raw) + 1.0) / 2.0))


def input_snapshot(controller, profile, deadzone=0.12):
    """Read semantic, proportionally scaled analog inputs for diagnostics.

    Does not command hardware. Call after pumping Pygame events.
    """
    data = {name: joystick_value(controller.get_axis(index), deadzone)
            for name, index in profile.axes.items()}
    data.update({name: trigger_value(controller.get_axis(index))
                 for name, index in profile.triggers.items()})
    if profile.hat is not None:
        data["dpad"] = controller.get_hat(profile.hat)
    return data
