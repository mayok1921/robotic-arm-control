# Software testing

Run from repository root:

```bash
python -m unittest discover -s tests -v
```

The test suite checks pure Python deadzone behavior and servo angle limits without Pygame, an Orange Pi, or attached motors.

**Not yet verified:** USB serial acknowledgements, controller disconnect behavior on hardware, Arduino line parsing, and safety properties of a loaded arm. Hardware testing must be done on the unloaded SG90 prototype before connecting anything to the group's robot.
