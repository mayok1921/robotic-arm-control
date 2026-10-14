# Preliminary bill of materials — group's robotic arm

**Planning list only; not a purchase authorization.** Keep existing robot motors and group Arduino, and do not reuse the personal bench Orange Pi/Arduino/SG90 in the final build.

| Item | Quantity | Decision | Notes |
| --- | --- | --- | --- |
| Dedicated single-board computer | 1 | **Provisional buy** | Orange Pi Zero 2W is a candidate because software was demonstrated on it; no upgrade justified yet. Confirm power, ports, availability and maintenance before ordering. |
| Group's Arduino | 1 existing | **Reuse** | Verify exact model, pins, memory, communication interface and firmware upload access. |
| Robot's installed motors | Predecessor documentation: DOCYKE S550 high-torque servos (~550 kg.cm class) and smaller ~80 kg.cm servos | **Reuse / inspect** | Earlier inventory indicates four large and two smaller servos; confirm actual installed models, quantity, voltage, current, and control signal before energizing. |
| Existing motor drivers/controllers | Unknown | **Inspect first** | May already exist; selection varies dramatically between hobby servo, stepper, brushed DC and smart servos. |
| Existing main 24V power supply | Prior design describes 24V, 50A, 1200W | **Evaluate for reuse** | Rated capacity is not measured draw. Confirm model/condition, voltage branches, peak current and protection before using. |
| DC/DC converter(s) | As needed | **Determine later** | Stable computer and actuator voltage branches from one source, with shared reference where required. |
| Fuses/distribution/wiring/connectors | As needed | **Plan purchase** | Wire gauge, terminal ratings and fusing depend on total current and routing. |
| Motor emergency stop / main disconnect | 1 or system-specific | **Plan purchase** | Rated hardware with safety behavior defined for loaded arm; not merely a software button. |
| USB data cable and suitable hub if required | As needed | **Inventory first** | Orange Pi to Arduino serial link. |
| Housing and mounting hardware | As needed | **Plan purchase** | Strain relief, airflow, physical access to stop controls. |
| PWM servo-expander board | 0 initially | **Optional** | PCA9685 only if existing motors accept hobby-servo PWM control and signal count demands it; board does not power motors. |

## Do not buy yet

- Replacement motors, unless the existing motors fail torque/accuracy/safety requirements.
- A specific motor driver or servo expander before identifying motor interface and current.
- A power supply based on the SG90 bench demo alone.
- A second Arduino if the group's Arduino can run the control firmware.

## Procurement checkpoint

Before recommending exact parts and costs, obtain photos/model numbers of **motors, installed drivers, group Arduino and present power supply**, plus number of axes and payload. Until then all cost estimates are speculative.

## Existing design reference

See the team's original Spring 2026 ME 416 final report (Google Drive) for actuator selection, wiring, torque/thermal calculations and the previous bill of materials. The report documents DOCYKE S550 servo specifications and significant high-power motor stall currents. Treat these as historical design inputs; verify the actual installed arm before purchases.

Complete a preliminary simultaneous electrical-load calculation and identify any lower-voltage branches before selecting converters, fuses or replacing the main supply.
