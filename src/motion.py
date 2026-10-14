"""Pure joystick-to-servo motion calculations, independent of hardware."""


def apply_deadzone(value: float, deadzone: float) -> float:
    if not 0 <= deadzone < 1:
        raise ValueError("deadzone must be within [0, 1)")
    value = max(-1.0, min(1.0, value))
    if abs(value) <= deadzone:
        return 0.0
    return (1 if value > 0 else -1) * (abs(value) - deadzone) / (1 - deadzone)


def next_angle(angle: float, axis: float, dt: float, speed: float,
               minimum: int, maximum: int, deadzone: float) -> float:
    if not 0 <= minimum < maximum <= 180:
        raise ValueError("invalid angle limits")
    if dt < 0 or speed < 0:
        raise ValueError("dt and speed must be nonnegative")
    angle += apply_deadzone(axis, deadzone) * speed * min(dt, 0.1)
    return max(minimum, min(maximum, angle))
