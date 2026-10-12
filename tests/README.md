# Testing plan

The current verified result is controller detection using `controller_test.py` (one Xbox One S controller, six axes, eleven buttons).

Planned checks:
1. Controller connect/disconnect and button/axis events
2. Dead zones and controller mapping
3. Safe neutral output on input loss or program failure
4. Communication timeouts and malformed commands
5. Joint limits and emergency stop before attaching motors

No automated tests have been implemented yet.
