# Main robotic arm integration plan

**Status:** Planning only. Actual robot electrical specifications and motor models have not been supplied yet.

## Scope

The Orange Pi, Arduino and SG90 currently used for development are **personal bench equipment** and will not be installed in the group's robot. The group already has an Arduino and plans to **reuse the robot's existing motors**. Purchase a dedicated SBC only after checking compatibility and power requirements.

## Information to collect from the group

| Item | Record |
| --- | --- |
| Group Arduino model and available I/O | Unknown |
| Number of joints and degrees of freedom | Unknown |
| Motor model / type / quantity per joint | Unknown |
| Rated voltage, running/stall current, torque | Unknown |
| Motor drivers already on the robot | Unknown |
| Feedback: encoders, potentiometers, limits | Unknown |
| Existing supply voltage and current rating | Unknown |
| Required motion range, gear ratios, payload | Unknown |
| Preferred one-cord vs battery power arrangement | One primary source preferred; source type undecided |

Do not assume the robot uses hobby RC servos simply because the bench prototype does.

## Integration milestones

1. **Preserve working prototype:** maintain the legacy `servo_control.py` and `arduino/servo_serial/` as reference.
2. **Software safety:** validate new serial protocol on a *single unloaded servo*; check correct response to garbage data, unplugged Arduino, and disconnected controller.
3. **Multi-joint abstraction:** create a joint interface that supports different actuator types and configurable limits. Do not energize all joints at once.
4. **Dedicated hardware:** prepare SBC image, Bluetooth, USB and Arduino deployment on nonpersonal hardware.
5. **Electrical design:** select drivers and protected single-source power distribution based on actual current/voltage measurements and motor specs. Separate motor-power cutoff from SBC shutdown where appropriate.
6. **Bench bring-up:** power and test each motor/driver independently with mechanical loads safely supported; add feedback, calibration, limits and emergency stop.
7. **Whole arm:** test startup, watchdogs, stop behavior, unexpected disconnect, brownout and operator stop under controlled conditions.

## Known gaps

- Servo power instability / occasional stop during repeated bench movement has not been diagnosed.
- Current hobby servo demonstration is **not closed-loop joint feedback** and isn't suitable as-is for a loaded arm.
- Hardware-specific failure modes need an explicit safe state (a servo holding a position or detaching is not universally safe).
- Xbox Bluetooth auto-reconnection observed; startup of control application has **not** been configured.

See [bill of materials](bill_of_materials.md), [development log](development_log.md), and [wiring](wiring.md).
