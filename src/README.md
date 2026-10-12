# Application source (planned)

The working controller detection script remains at [../controller_test.py](../controller_test.py) so existing instructions do not break.

Future Python modules may include:
- `controller_input.py` — read live joystick events
- `controller_mapping.py` — convert inputs into bounded joint commands
- `main.py` — application startup and safe shutdown

These files have not been implemented or tested. Avoid moving the working script until imports and launch instructions are updated.
