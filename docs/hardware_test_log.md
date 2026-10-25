# Hardware test log — Enercon robotic-arm controls

This log records direct observations separately from assumptions and future tests. The current objective is to reuse the prior team's available hardware and demonstrate smooth, proportional joystick control of an unloaded joint actuator before integrating the new arm.

## 2026-10-25 — Initial power supply verification

**Hardware provenance:** The DOCYKE motor(s), existing power supply, and wiring came from the previous group's system. No replacement motors or electronics have been purchased for this test. Some existing exposed connections were improved with heat-shrink tubing and electrical tape. Parts of the existing system were brought home for bench testing.

**Reported current condition:**
- Motor/control wiring disconnected for a fresh setup; Orange Pi Zero 2W connected over USB, but SSH connection not yet re-established.
- User has acquired a multimeter and is reviewing how to use it.
- User measured **24.1–24.2 V DC** across the power supply's output terminals (reported as V_out).
- Measurement was taken while the motor system was disconnected, so treat this as **approximately no-load supply voltage**, not verified loaded voltage or the actuator's rated operating voltage.
- Multimeter model, meter settings, measurement polarity, power supply nameplate rating, motor model/rating, and load current are **not yet documented**.

**Interpretation:** The measured output is consistent with a nominal 24 V DC supply. It does **not** establish that the DOCYKE motor is rated for 24 V, that the supply can provide sufficient current, or that the existing wiring is safe under load.

**Immediate next steps:**
1. Photograph and identify multimeter model, input jacks, and selector positions; review DC-voltage and current-measurement methods. Never place meter probes across a powered supply in current/A mode.
2. Record nameplate voltage/current ratings for the supply and exact motor model and control interface.
3. With mains disconnected before any wiring changes, inspect DC polarity, connector condition, insulation, and strain relief; do not open the PSU enclosure or probe mains terminals.
4. Reconnect Orange Pi over SSH and verify existing wired-controller-to-Arduino test path.
5. Only after confirming motor and supply compatibility, test one securely restrained, unloaded actuator with an appropriate power-disconnect method.
6. Evaluate whether incremental position commands provide slower proportional joystick motion and measure actual response.

**Desired control behavior:** Slight joystick deflection gives slow joint motion; larger deflection gives faster motion; release stops changing the joint target. Actual motor speed and stopping behavior must be verified before attaching a load.

**Not yet verified:** loaded supply voltage, motor current, motor continuous torque, motor electrical compatibility, correct direction, control protocol, joystick-to-DOCYKE operation, or a safe stopped state under load.
