"""Tests run without controller, Arduino, or Pygame: python -m unittest discover -s tests."""
import unittest
from src.motion import apply_deadzone, next_angle


class MotionTests(unittest.TestCase):
    def test_deadzone(self):
        self.assertEqual(apply_deadzone(0.15, 0.20), 0)
        self.assertEqual(apply_deadzone(-0.15, 0.20), 0)
        self.assertEqual(apply_deadzone(1, 0.20), 1)
        self.assertEqual(apply_deadzone(-1, 0.20), -1)

    def test_limits(self):
        self.assertEqual(next_angle(134, 1, 1, 60, 45, 135, 0.2), 135)
        self.assertEqual(next_angle(46, -1, 1, 60, 45, 135, 0.2), 45)

    def test_center_holds(self):
        self.assertEqual(next_angle(90, 0.1, 0.02, 60, 45, 135, 0.2), 90)


if __name__ == "__main__":
    unittest.main()
