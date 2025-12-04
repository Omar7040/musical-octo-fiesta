"""Tests for the VIN Scanner module."""

import unittest
from toyota_service.services.vin_scanner import (
    scan_vin,
    validate_vin,
    get_vin_summary,
    VINInfo
)


class TestVINScanner(unittest.TestCase):
    """Test cases for VIN Scanner."""

    def test_valid_toyota_vin(self):
        """Test scanning a valid Toyota VIN."""
        # Example Toyota VIN
        vin = "JT2BG22K8Y0123456"
        result = scan_vin(vin)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.manufacturer, "Toyota")
        self.assertEqual(result.vin, vin)
        self.assertEqual(result.error_message, "")

    def test_invalid_vin_length(self):
        """Test VIN with wrong length."""
        vin = "JT2BG22K"  # Too short
        result = scan_vin(vin)
        
        self.assertFalse(result.is_valid)
        self.assertIn("17 caracteres", result.error_message)

    def test_invalid_vin_characters(self):
        """Test VIN with invalid characters (I, O, Q)."""
        vin = "JT2BG22K8IO123456"  # Contains I and O
        result = scan_vin(vin)
        
        self.assertFalse(result.is_valid)
        self.assertIn("inválidos", result.error_message)

    def test_non_toyota_vin(self):
        """Test VIN from non-Toyota vehicle."""
        vin = "1HGBH41JXMN109186"  # Honda VIN
        result = scan_vin(vin)
        
        self.assertFalse(result.is_valid)
        self.assertIn("no corresponde a un vehículo Toyota", result.error_message)

    def test_empty_vin(self):
        """Test empty VIN."""
        result = scan_vin("")
        
        self.assertFalse(result.is_valid)
        self.assertIn("vacío", result.error_message)

    def test_validate_vin_valid(self):
        """Test validate_vin with valid VIN."""
        is_valid, error = validate_vin("JT2BG22K8Y0123456")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_vin_invalid(self):
        """Test validate_vin with invalid VIN."""
        is_valid, error = validate_vin("INVALID")
        self.assertFalse(is_valid)
        self.assertNotEqual(error, "")

    def test_vin_info_to_dict(self):
        """Test VINInfo to_dict method."""
        vin = "JT2BG22K8Y0123456"
        result = scan_vin(vin)
        
        vin_dict = result.to_dict()
        self.assertIsInstance(vin_dict, dict)
        self.assertIn("vin", vin_dict)
        self.assertIn("is_valid", vin_dict)
        self.assertIn("manufacturer", vin_dict)
        self.assertIn("model", vin_dict)
        self.assertIn("year", vin_dict)

    def test_get_vin_summary_valid(self):
        """Test get_vin_summary with valid VIN."""
        summary = get_vin_summary("JT2BG22K8Y0123456")
        self.assertIn("Toyota", summary)

    def test_get_vin_summary_invalid(self):
        """Test get_vin_summary with invalid VIN."""
        summary = get_vin_summary("INVALID")
        self.assertIn("inválido", summary)

    def test_vin_case_insensitive(self):
        """Test that VIN scanning is case insensitive."""
        vin_upper = "JT2BG22K8Y0123456"
        vin_lower = "jt2bg22k8y0123456"
        
        result_upper = scan_vin(vin_upper)
        result_lower = scan_vin(vin_lower)
        
        self.assertEqual(result_upper.is_valid, result_lower.is_valid)
        self.assertEqual(result_upper.model, result_lower.model)

    def test_vin_with_whitespace(self):
        """Test VIN with leading/trailing whitespace."""
        vin = "  JT2BG22K8Y0123456  "
        result = scan_vin(vin)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.vin, "JT2BG22K8Y0123456")


class TestVINScannerUSA(unittest.TestCase):
    """Test VIN scanning for US-made Toyota vehicles."""

    def test_usa_vin(self):
        """Test scanning a USA Toyota VIN."""
        vin = "4T1BG22K8YU123456"
        result = scan_vin(vin)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.country, "Estados Unidos")


class TestVINScannerCanada(unittest.TestCase):
    """Test VIN scanning for Canada-made Toyota vehicles."""

    def test_canada_vin(self):
        """Test scanning a Canada Toyota VIN."""
        vin = "2T1BG22K8YU123456"
        result = scan_vin(vin)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.country, "Canadá")


if __name__ == "__main__":
    unittest.main()
