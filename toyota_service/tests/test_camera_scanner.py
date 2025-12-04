"""Tests for the Camera Scanner module."""

import unittest
from toyota_service.services.camera_scanner import (
    CameraScanResult,
    check_camera_dependencies,
)


class TestCameraScanner(unittest.TestCase):
    """Test cases for Camera Scanner."""

    def test_camera_scan_result_success(self):
        """Test CameraScanResult with success."""
        result = CameraScanResult(
            success=True,
            vin="JT2BG22K8Y0123456",
            scan_type="barcode"
        )
        self.assertTrue(result.success)
        self.assertEqual(result.vin, "JT2BG22K8Y0123456")
        self.assertEqual(result.scan_type, "barcode")
        self.assertEqual(result.error_message, "")

    def test_camera_scan_result_failure(self):
        """Test CameraScanResult with failure."""
        result = CameraScanResult(
            success=False,
            vin="",
            error_message="Camera not available"
        )
        self.assertFalse(result.success)
        self.assertEqual(result.vin, "")
        self.assertIn("Camera", result.error_message)

    def test_check_camera_dependencies(self):
        """Test check_camera_dependencies returns tuple."""
        available, message = check_camera_dependencies()
        self.assertIsInstance(available, bool)
        self.assertIsInstance(message, str)
        self.assertTrue(len(message) > 0)


class TestCameraScanResultDataclass(unittest.TestCase):
    """Test the CameraScanResult dataclass."""

    def test_default_values(self):
        """Test default values of CameraScanResult."""
        result = CameraScanResult(success=True, vin="TEST123456789012")
        self.assertEqual(result.error_message, "")
        self.assertEqual(result.scan_type, "")

    def test_all_fields(self):
        """Test all fields of CameraScanResult."""
        result = CameraScanResult(
            success=True,
            vin="JT2BG22K8Y0123456",
            error_message="",
            scan_type="qr"
        )
        self.assertTrue(result.success)
        self.assertEqual(result.vin, "JT2BG22K8Y0123456")
        self.assertEqual(result.scan_type, "qr")


if __name__ == "__main__":
    unittest.main()
