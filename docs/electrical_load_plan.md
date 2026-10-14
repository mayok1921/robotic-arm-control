# Preliminary electrical load assessment

This is a **design worksheet**, not a certified power-system design. Before powering the inherited arm, verify the installed labels, wiring and actual condition.

## Reference data and uncertainty

The Spring 2026 ME 416 final report for the glovebox HEPA-filter robotic arm discusses DOCYKE S550 high-torque servos, smaller ~80 kg.cm-class servos, original electrical wiring and thermal calculations. Earlier notes report four large and two smaller servos and a 24V / 50A (1200W) main supply.

The predecessor report calculates around **29.935 A per high-power motor at 24V as a projected stall-current figure** in its thermal-analysis appendix, based on 18V data. This is an **estimate for a fault/stall case**, not a normal operating draw or a guaranteed manufacturer rating. Confirm operating voltage and current from the actual motor datasheet. The 24V / 50A rating describes the supply limit, not the whole robot's measured consumption.

## Inputs to assemble

| Load / branch | Quantity | Required operating voltage | Idle current | Nominal moving current | Peak / stall current | Source |
| --- | --- | --- | --- | --- | --- | --- |
| DOCYKE S550-class servo | Verify, historically ~4 | Verify motor label | Unknown | Unknown | Verify; predecessor appendix projected 29.935A at 24V | Datasheet + measurement |
| Smaller servo ~80 kg.cm | Verify, historically ~2 | Verify | Unknown | Unknown | Unknown | Datasheet + measurement |
| Orange Pi or selected SBC | 1 proposed | Check official spec | Unknown | Unknown | Unknown | SBC specification |
| Arduino / ESP32 / interface | Existing | Verify board | Unknown | Unknown | Unknown | Board specs |
| Sensors, fans, converters | Inventory | Verify | Unknown | Unknown | Unknown | Datasheets |

Do not sum all motor stall currents as if that were normal continuous consumption. Use **at least two scenarios**: a credible simultaneous-motion scenario for supply sizing and a fault/stall scenario for protective design. Multiple stalled 24V high-torque servos can quickly exceed the rated output of a 50A supply.

## Preliminary equations

- Per branch electrical input power: `P = V * I`.
- Simultaneous current on one voltage rail: `I_rail = sum(I_each active load)` (include any startup/inrush requirements and actual duty cycles).
- Converter input power estimate: `P_in = P_out / efficiency`. Then `I_in = P_in / V_in`.
- Supply margin: consider continuous rating, ambient derating, wiring losses and transient behavior rather than treating 100% nameplate output as a desired normal operating point.
- Voltage drop in a round-trip DC conductor: `V_drop = I * R_roundtrip`. Check conductor resistance for the actual length and gauge.
- A fuse protects **wiring and circuits**; size/protection selection must match conductor ampacity, connector ratings, start-up/inrush and motor fault conditions.

## Questions before parts orders

1. Confirm every actuator's make, model, quantity, rated voltage and control signal interface.
2. Confirm the main DC supply nameplate and any separate servo voltage regulators.
3. Check available current and branch protection under plausible simultaneous joint motion.
4. Evaluate the 5V SBC rail and any lower-voltage motor rails separately from 24V.
5. Define a motor-power emergency-stop strategy and how to prevent hazardous motion on Bluetooth/serial failure.
6. Plan controlled current/voltage measurements using appropriate equipment and supervision; do not deliberately stall a loaded arm.

**Next decision:** keep the existing 24V supply if calculations, measurements and electrical inspection support it. Do not automatically replace it.

Source: predecessor Spring 2026 ME 416 final report, *Robotic Arm for Removal of Glovebox HEPA Filter* (original design document).
