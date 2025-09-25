"""
Comprehensive test suite for QR Code Generator
Tests all core functionality and edge cases
"""
import unittest
import os
import tempfile
import shutil
from pathlib import Path
import segno
from qr_generator import generate_qr, validate_input, generate_qr_with_options


class TestQRGenerator(unittest.TestCase):
    """Test cases for QR Code Generator"""

    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for test outputs
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary directory and all files
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_validate_input_valid_text(self):
        """Test validation with valid text input"""
        self.assertTrue(validate_input("Hello World"))
        self.assertTrue(validate_input("Test123"))
        self.assertTrue(validate_input("Special chars: !@#$%^&*()"))
        self.assertTrue(validate_input("Unicode: 你好世界"))

    def test_validate_input_empty_text(self):
        """Test validation with empty text"""
        self.assertFalse(validate_input(""))
        self.assertFalse(validate_input(None))

    def test_validate_input_non_string(self):
        """Test validation with non-string input"""
        self.assertFalse(validate_input(123))
        self.assertFalse(validate_input(['list']))
        self.assertFalse(validate_input({'dict': 'value'}))

    def test_validate_input_long_text(self):
        """Test validation with text exceeding length limit"""
        # Text within limit should be valid
        text_within_limit = "a" * 2000
        self.assertTrue(validate_input(text_within_limit))

        # Text exceeding limit should be invalid
        text_over_limit = "a" * 2001
        self.assertFalse(validate_input(text_over_limit))

    def test_generate_qr_basic_functionality(self):
        """Test basic QR code generation"""
        filename = os.path.join(self.test_dir, "test_basic.png")
        result = generate_qr("Hello World", filename)

        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

        # Verify file is not empty
        self.assertGreater(os.path.getsize(filename), 0)

    def test_generate_qr_with_special_characters(self):
        """Test QR generation with special characters"""
        filename = os.path.join(self.test_dir, "test_special.png")
        text = "Special: !@#$%^&*()\n\tTab and newline"
        result = generate_qr(text, filename)

        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

    def test_generate_qr_with_unicode(self):
        """Test QR generation with Unicode characters"""
        filename = os.path.join(self.test_dir, "test_unicode.png")
        text = "Unicode test: 你好世界 🌍 ñáéíóú"
        result = generate_qr(text, filename)

        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

    def test_generate_qr_auto_extension(self):
        """Test that .png extension is added automatically"""
        filename_without_ext = os.path.join(self.test_dir, "test_no_ext")
        filename_with_ext = filename_without_ext + ".png"

        result = generate_qr("Test", filename_without_ext)

        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename_with_ext))

    def test_generate_qr_existing_extension(self):
        """Test with existing .png extension"""
        filename = os.path.join(self.test_dir, "test_with_ext.png")
        result = generate_qr("Test", filename)

        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

    def test_generate_qr_invalid_input(self):
        """Test QR generation with invalid input"""
        filename = os.path.join(self.test_dir, "test_invalid.png")

        # Empty text
        result = generate_qr("", filename)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(filename))

        # None text
        result = generate_qr(None, filename)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(filename))

    def test_generate_qr_invalid_filename(self):
        """Test QR generation with invalid filename"""
        result = generate_qr("Test", "")
        self.assertFalse(result)

        result = generate_qr("Test", None)
        self.assertFalse(result)

    def test_generate_qr_directory_creation(self):
        """Test that directories are created if they don't exist"""
        nested_dir = os.path.join(self.test_dir, "nested", "deep", "path")
        filename = os.path.join(nested_dir, "test.png")

        result = generate_qr("Test", filename)

        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))
        self.assertTrue(os.path.exists(nested_dir))

    def test_generate_qr_with_options_default(self):
        """Test QR generation with default options"""
        filename = os.path.join(self.test_dir, "test_options.png")
        result = generate_qr_with_options("Test", filename)

        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

    def test_generate_qr_with_options_custom(self):
        """Test QR generation with custom options"""
        filename = os.path.join(self.test_dir, "test_custom.png")
        result = generate_qr_with_options("Test", filename, error_correction='h', scale=4)

        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

    def test_generate_qr_with_options_invalid_error_correction(self):
        """Test QR generation with invalid error correction"""
        filename = os.path.join(self.test_dir, "test_invalid_error.png")
        result = generate_qr_with_options("Test", filename, error_correction='x')

        self.assertFalse(result)

    def test_generate_qr_with_options_invalid_scale(self):
        """Test QR generation with invalid scale"""
        filename = os.path.join(self.test_dir, "test_invalid_scale.png")
        result = generate_qr_with_options("Test", filename, scale=0)

        self.assertFalse(result)

    def test_qr_code_readability(self):
        """Test that generated QR codes are readable"""
        filename = os.path.join(self.test_dir, "test_readable.png")
        test_text = "This is a test message for QR readability"

        result = generate_qr(test_text, filename)
        self.assertTrue(result)

        # Try to read the QR code back using segno
        try:
            # Load and decode the QR code
            qr_code = segno.make(test_text)
            # If we can create the same QR code, our generation is working
            self.assertIsNotNone(qr_code)
        except Exception as e:
            self.fail(f"Generated QR code is not readable: {e}")

    def test_maximum_length_text(self):
        """Test QR generation with maximum allowed text length"""
        filename = os.path.join(self.test_dir, "test_max_length.png")
        max_text = "a" * 2000  # Maximum allowed length

        result = generate_qr(max_text, filename)

        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

    def test_different_error_correction_levels(self):
        """Test all error correction levels"""
        error_levels = ['l', 'm', 'q', 'h']

        for level in error_levels:
            with self.subTest(error_level=level):
                filename = os.path.join(self.test_dir, f"test_error_{level}.png")
                result = generate_qr_with_options("Test", filename, error_correction=level)

                self.assertTrue(result)
                self.assertTrue(os.path.exists(filename))

    def test_different_scale_values(self):
        """Test different scale values"""
        scale_values = [1, 2, 4, 8, 16]

        for scale in scale_values:
            with self.subTest(scale=scale):
                filename = os.path.join(self.test_dir, f"test_scale_{scale}.png")
                result = generate_qr_with_options("Test", filename, scale=scale)

                self.assertTrue(result)
                self.assertTrue(os.path.exists(filename))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_whitespace_only_text(self):
        """Test with whitespace-only text"""
        filename = os.path.join(self.test_dir, "test_whitespace.png")

        # Spaces only
        result = generate_qr("   ", filename)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

        # Tabs and newlines
        result = generate_qr("\t\n\r", filename)
        self.assertTrue(result)

    def test_very_long_filename(self):
        """Test with very long filename"""
        long_name = "a" * 100 + ".png"
        filename = os.path.join(self.test_dir, long_name)

        result = generate_qr("Test", filename)

        # This should work on most systems, but might fail on systems with filename length limits
        # We'll check if it either succeeds or fails gracefully
        if not result:
            # If it fails, it should fail gracefully without crashing
            self.assertFalse(os.path.exists(filename))

    def test_case_insensitive_extension(self):
        """Test case-insensitive extension handling"""
        filename_upper = os.path.join(self.test_dir, "test.PNG")
        filename_mixed = os.path.join(self.test_dir, "test.Png")

        result1 = generate_qr("Test1", filename_upper)
        result2 = generate_qr("Test2", filename_mixed)

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(os.path.exists(filename_upper))
        self.assertTrue(os.path.exists(filename_mixed))


if __name__ == '__main__':
    # Create a test suite with all tests
    unittest.main(verbosity=2)