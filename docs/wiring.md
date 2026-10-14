# Wiring notes

## Verified bench servo circuit

| SG90 wire | Arduino UNO R3 |
| --- | --- |
| Brown | GND |
| Red | 5V |
| Orange | D9 |

Used for **one unloaded SG90 servo only**. Final loaded/multiple-actuator systems require a suitable external motor supply, current protection and common ground where required. Never connect motor power directly to Orange Pi GPIO.

## Verified USB connections

```text
Windows laptop (VS Code + RNDIS, 192.168.7.1)
     |
     | USB data cable (g_ether network)
     v
Orange Pi Zero 2W USB0 (usb0, 192.168.7.2)
     |
     +-- Bluetooth <-- Xbox controller
     |
     +-- USB1 (host) --> USB hub --> Arduino UNO R3 --> SG90 on D9
```

This **simultaneous USB arrangement was observed working**. USB0 and USB1 should not be treated as interchangeable. Follow the [portable USB setup](usb_development_setup.md) for host drivers, software and tested connection.

The Arduino serial port was `/dev/ttyACM0` during testing but may change after reconnection. For servo code/wiring see [servo demonstration guide](servo_demo_guide.md).

## Future robotic arm wiring (unverified)

Record motor models, rated/stall currents, control signal requirements, driver specifications, cable routing, emergency stop, limits and grounding before final construction.
