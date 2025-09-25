"""
Test suite for QR Code Generator - Adaptive TDD V4.1
Starting with the simplest possible failing test.
"""

import unittest
import os
from qr_generator import generate_qr, validate_input


class TestQRGenerator(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.test_file = "test_qr.png"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Clean up after tests."""
        test_files = [
            self.test_file, "empty_text.png", "none_text.png", "advanced_test.png",
            "long_text.png", "very_long_text.png", "special_chars.png"
        ]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)

    def test_generate_qr_exists(self):
        """Test that the generate_qr function exists and is callable."""
        self.assertTrue(callable(generate_qr))

    def test_generate_qr_creates_file(self):
        """Test that generate_qr creates a PNG file."""
        result = generate_qr("Hello World", self.test_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))

    def test_validate_input_exists(self):
        """Test that validate_input function exists."""
        self.assertTrue(callable(validate_input))

    def test_validate_input_accepts_valid_text(self):
        """Test that validate_input returns True for valid text."""
        self.assertTrue(validate_input("Hello World"))
        self.assertTrue(validate_input("123"))
        self.assertTrue(validate_input("Test with spaces and symbols!@#"))

    def test_validate_input_rejects_invalid_text(self):
        """Test that validate_input returns False for invalid input."""
        self.assertFalse(validate_input(""))
        self.assertFalse(validate_input(None))

        # Test text length limit
        too_long_text = "A" * 2001
        self.assertFalse(validate_input(too_long_text))

        # Test at the limit
        limit_text = "B" * 2000
        self.assertTrue(validate_input(limit_text))

    def test_generate_qr_with_validation(self):
        """Test that generate_qr validates input before processing."""
        # Valid input should succeed
        result = generate_qr("Valid text", self.test_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))

        # Clean up for next test
        os.remove(self.test_file)

        # Invalid input should fail gracefully
        result = generate_qr("", "empty_text.png")
        self.assertFalse(result)
        self.assertFalse(os.path.exists("empty_text.png"))

        result = generate_qr(None, "none_text.png")
        self.assertFalse(result)
        self.assertFalse(os.path.exists("none_text.png"))

    def test_generate_qr_with_options(self):
        """Test generate_qr with error correction and scale options."""
        from qr_generator import generate_qr_advanced

        result = generate_qr_advanced("Test", "advanced_test.png", error='H', scale=10)
        self.assertTrue(result)
        self.assertTrue(os.path.exists("advanced_test.png"))

    def test_generate_qr_with_long_text(self):
        """Test QR generation with long text (up to 2000 chars)."""
        long_text = "A" * 1000  # 1000 characters
        result = generate_qr(long_text, "long_text.png")
        self.assertTrue(result)
        self.assertTrue(os.path.exists("long_text.png"))

        # Test at the upper limit
        very_long_text = "B" * 2000  # 2000 characters
        result = generate_qr(very_long_text, "very_long_text.png")
        self.assertTrue(result)
        self.assertTrue(os.path.exists("very_long_text.png"))

    def test_generate_qr_with_special_characters(self):
        """Test QR generation with Unicode and special characters."""
        special_text = "Hello 世界! @#$%^&*()_+ 🌟"
        result = generate_qr(special_text, "special_chars.png")
        self.assertTrue(result)
        self.assertTrue(os.path.exists("special_chars.png"))


if __name__ == '__main__':
    unittest.main()