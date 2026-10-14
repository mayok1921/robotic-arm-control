"""Simple acknowledged serial transport for servo_serial_v2 firmware."""

import time


class ArduinoServoTransport:
    def __init__(self, port: str, baudrate: int = 9600):
        import serial  # only needed on robot
        self.serial = serial.Serial(port, baudrate=baudrate, timeout=0.5)
        # Opening UNO USB serial resets it; allow time for firmware startup.
        time.sleep(2)
        self.serial.reset_input_buffer()

    def send_angle(self, angle: int) -> None:
        if type(angle) is not int or not 0 <= angle <= 180:
            raise ValueError("invalid servo angle")
        self.serial.write(f"SET {angle}\n".encode("ascii"))
        self.serial.flush()
        response = self.serial.readline().decode("ascii", errors="replace").strip()
        if response != f"OK {angle}":
            raise RuntimeError(f"No valid Arduino acknowledgement: {response!r}")

    def close(self):
        self.serial.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
