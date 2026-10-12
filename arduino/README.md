# Arduino integration (planned)

An Arduino is an optional future low-level controller for actuators and sensors. No Arduino firmware has been uploaded for this project yet.

Potential architecture: Xbox controller → Orange Pi Python application → wired serial connection → Arduino → suitable motor drivers.

Before implementation, specify a command protocol, acknowledgements, command timeouts, safe-stop behavior, and motor limits. Do not treat this directory as working firmware.
