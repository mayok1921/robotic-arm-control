# Wiring notes

No robotic arm, motor driver, or Arduino wiring has been selected or verified.

Before creating a wiring diagram, record:
- Board model and connector pinouts from official documentation
- Actuator voltage, peak/stall current, and motor-driver ratings
- Logic voltage compatibility (including Orange Pi GPIO voltage)
- Common-ground and power-isolation requirements
- Fusing, emergency-stop behavior, and physical joint limits

Do not connect motors directly to Orange Pi or Arduino GPIO pins. This document will be updated after hardware selection.
