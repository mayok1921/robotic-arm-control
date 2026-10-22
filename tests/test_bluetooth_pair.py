"""Hardware-independent regression tests for the Bluetooth setup utility."""
import unittest
from unittest.mock import patch

import bluetooth_pair as bp


class BluetoothPairTests(unittest.TestCase):
    def test_parse_devices_deduplicates(self):
        raw = ("Device AA:BB:CC:DD:EE:FF Wireless Controller\n"
               "Device 11:22:33:44:55:66 Xbox Wireless Controller\n"
               "Device AA:BB:CC:DD:EE:FF Wireless Controller")
        result = bp.parse_devices(raw)
        self.assertEqual(len(result), 2)
        self.assertIn(("AA:BB:CC:DD:EE:FF", "Wireless Controller"), result)

    def test_parse_info(self):
        result = bp.parse_info("Paired: yes\nTrusted: yes\nConnected: no\nBlocked: no")
        self.assertEqual(result, dict(paired=True, trusted=True, connected=False, blocked=False))

    def test_duplicate_names_need_number(self):
        found = [("AA:BB:CC:DD:EE:FF", "Wireless Controller"),
                 ("11:22:33:44:55:66", "Wireless Controller")]
        with patch("builtins.input", side_effect=["Wireless Controller", "2"]):
            self.assertEqual(bp.choose(found), found[1])

    def test_report_refuses_false_success(self):
        with patch.object(bp, "state", return_value=dict(paired=True, trusted=True, connected=False)), \
             patch.object(bp, "input_devices", return_value=[]):
            self.assertFalse(bp.report("AA:BB:CC:DD:EE:FF", "Test"))

    def test_invalid_address(self):
        with self.assertRaises(bp.BTError):
            bp.device_info("bad-address")


if __name__ == "__main__":
    unittest.main()
