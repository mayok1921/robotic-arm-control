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
