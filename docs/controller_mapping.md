# Controller input mapping — Orange Pi bench setup

## Verified PS5 DualSense USB test (October 22, 2026)

The user connected a Sony DualSense to the Orange Pi Zero 2W over **USB**. Linux enumerated USB ID `054c:0ce6`, with `Handlers=js0 event1`. Pygame 2.6.1 identified `Sony Interactive Entertainment DualSense Wireless Controller` with **6 axes, 15 buttons, 1 hat**. Stick, trigger, button, and D-pad events appeared in `controller_input_test.py`. This **does not demonstrate working DualSense Bluetooth input**, and does not demonstrate servo motor control with this controller.

| Physical control | Pygame | Observed behavior |
| --- | --- | --- |
| Left stick horizontal | Axis 0 | -1 to +1; center ~0 |
| Left stick vertical | Axis 1 | -1 to +1; center ~0 |
| Right stick horizontal | Axis 2 | -1 to +1; center ~0 |
| Right stick vertical | Axis 5 | -1 to +1; center ~0 |
| L2 analog trigger | Axis 3 | -1 at rest to +1 pressed |
| R2 analog trigger | Axis 4 | -1 at rest to +1 pressed |
| L2 / R2 button reports | Buttons 6 / 7 | Press/release events |
| D-pad | Hat 0 | 2D (x, y) including diagonals |

Other button indices were observed but have **not all been explicitly assigned to named physical controls**. Do not treat button index mappings as verified without per-button inspection.

## Code architecture

- `src/controller_profiles.py` defines named controller inputs, the observed DualSense USB profile, a **partial** Xbox profile, and normalized analog values; it has no Pygame or motor dependencies.
- `src/inputs.py` wraps Pygame, detects controller family and signatures, and exposes `read_inputs()` for named inputs. `read_axis()` remains for compatibility with existing experimental code.
- The legacy `servo_control.py` and Arduino firmware have **not** been changed. The experimental `src/control.py` still reads the raw configured axis and needs deliberate integration testing before migrating to semantic controls.
- Xbox Bluetooth mappings beyond the known left horizontal stick were **not** assumed. USB/Bluetooth SDL mappings may vary.

### Proportional control policy

Only **analog sticks and triggers** receive speed scaled to displacement. Sticks use a center deadzone with rescaling to preserve a smooth zero-to-full range. DualSense trigger values normalize from -1..+1 to 0..1. Buttons and D-pad remain intended for fixed actions or preset movements.

This code **only normalizes commands**; it does not prove servo speed, motor acceleration, or safe stop behavior. Do not use with a loaded arm until hardware safety and command-loss handling are validated.

## Run tests

From the Windows project root:

```powershell
python -m unittest discover -s tests -v
```

To perform a live controller read on the Orange Pi (no motors):

```bash
python3 controller_input_test.py
```

**Remaining:** validate the new adapter with real wired-USB Pygame on the Orange Pi; test actual Xbox input assignments; resolve DualSense Bluetooth HID registration; verify a safe multi-joint mapping with motors disconnected first.
