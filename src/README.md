# Experimental modular controller — not hardware validated

The verified reference remains at [../servo_control.py](../servo_control.py). **Do not use this prototype with the original Arduino firmware.**

- `motion.py`: pure Python input deadzone, bounded position and speed integration
- `inputs.py`: Pygame joystick input with detach detection
- `transport.py`: acknowledged USB serial transport
- `control.py`: single unloaded-servo command loop
- `../config/settings.json`: deadzone, joint limits, rate and serial configuration

## Testing

Run the pure-software tests from repository root:

```bash
python -m unittest discover -s tests -v
```

Only after reviewing both protocols, flash [v2 Arduino firmware](../arduino/servo_serial_v2/servo_serial_v2.ino) **to the bench Arduino**, transfer `src/` and `config/` to the Orange Pi, then launch **from the repository root**:

```bash
python3 -m src.control
```

The experimental v2 protocol is `SET 90\n` → `OK 90`. The original code sends `90\n` and is incompatible with v2.

**Limitations:** one servo, no reconnect loop, no independent hardware motion watchdog, no encoder/position feedback, no validated power supply. On disconnection software ceases generating motion commands; the Arduino servo may continue holding torque. Holding torque or detaching is *not* a guaranteed safe state for a loaded robot. This is **not ready for group robot installation**.

## Controller-neutral input layer (October 22, 2026)

- [Controller mapping](../docs/controller_mapping.md) records the observed **wired USB DualSense** layout: axes 0/1 for left stick, 2/5 for right stick, 3/4 for L2/R2, and hat 0 for D-pad. Xbox profile is currently partial.
- `controller_profiles.py` has pure mapping/normalization functions (center deadzone for sticks; -1..+1 to 0..1 for DualSense triggers).
- `inputs.py` exposes `ControllerInput.read_inputs()` with named inputs and retains `XboxInput` alias and `read_axis()` for backward compatibility with the **experimental**, unchanged `src/control.py`.
- For an input-only live check on the Orange Pi, run from the repository root: `python3 controller_profile_test.py` (no motor commands). Use `controller_input_test.py` for unknown controller layouts.
- The new semantic input adapter has software tests, but **has not yet been validated on Orange Pi hardware**. The existing runner still uses a raw axis; multi-joint servo mapping is not yet implemented.
