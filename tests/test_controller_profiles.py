"""Hardware-independent DualSense and Xbox profile regression tests."""
import unittest
from src.controller_profiles import (
    identify_controller, joystick_value, trigger_value, input_snapshot, DUALSENSE_USB,
)


class FakeJoystick:
    def __init__(self):
        self.axes = [0.5, -0.5, -0.25, -1.0, 1.0, 0.25]

    def get_axis(self, index):
        return self.axes[index]

    def get_hat(self, index):
        return (1, 0)


class ProfilesTests(unittest.TestCase):
    def test_wired_dualsense_signature(self):
        self.assertEqual(identify_controller("Sony Interactive Entertainment DualSense Wireless Controller", 6, 15, 1), DUALSENSE_USB)

    def test_does_not_assume_wireless_mapping(self):
        self.assertIsNone(identify_controller("DualSense Wireless Controller", 6, 16, 1))

    def test_unknown(self):
        self.assertIsNone(identify_controller("Other joystick", 6, 15, 1))

    def test_xbox_partial(self):
        self.assertFalse(identify_controller("Xbox Wireless Controller", 6, 16, 0).verified)

    def test_deadzone_scaled(self):
        self.assertEqual(joystick_value(0.12, 0.12), 0)
        self.assertAlmostEqual(joystick_value(0.56, 0.12), 0.5)
        self.assertAlmostEqual(joystick_value(-0.56, 0.12), -0.5)
        self.assertEqual(joystick_value(1, 0.12), 1)

    def test_triggers(self):
        self.assertEqual(trigger_value(-1), 0)
        self.assertEqual(trigger_value(0), 0.5)
        self.assertEqual(trigger_value(1), 1)

    def test_semantic_snapshot(self):
        data = input_snapshot(FakeJoystick(), DUALSENSE_USB, 0.0)
        self.assertEqual(data["right_y"], 0.25)
        self.assertEqual(data["left_trigger"], 0)
        self.assertEqual(data["right_trigger"], 1)
        self.assertEqual(data["dpad"], (1, 0))


if __name__ == "__main__":
    unittest.main()
