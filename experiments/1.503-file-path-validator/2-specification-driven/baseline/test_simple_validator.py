#!/usr/bin/env python3
"""
Test suite for Simple Path Validator
Comprehensive tests to verify the implementation matches specifications.
"""

import os
import platform
import tempfile
from pathlib import Path
import unittest
from simple_path_validator import PathValidator, validate_path, is_valid_path


class TestSimplePathValidator(unittest.TestCase):
    """Test cases for Simple Path Validator."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = PathValidator()
        self.system = platform.system()

    def test_basic_validation_valid_paths(self):
        """Test basic validation with valid paths."""
        valid_paths = [
            "/home/user/document.txt",
            "relative/path/file.txt",
            "./current/directory",
            "simple_file.txt",
            "/",
            ".",
        ]

        for path in valid_paths:
            with self.subTest(path=path):
                result = self.validator.validate_path(path)
                self.assertTrue(result['is_valid'], f"Path should be valid: {path}")
                self.assertIsInstance(result['errors'], list)
                self.assertIsInstance(result['warnings'], list)

    def test_basic_validation_invalid_paths(self):
        """Test basic validation with invalid paths."""
        invalid_paths = [
            "",  # Empty path
            None,  # None input
        ]

        for path in invalid_paths:
            with self.subTest(path=path):
                result = self.validator.validate_path(path)
                self.assertFalse(result['is_valid'], f"Path should be invalid: {path}")
                self.assertTrue(len(result['errors']) > 0)

    def test_null_byte_detection(self):
        """Test null byte detection in paths."""
        paths_with_null = [
            "file\x00.txt",
            "/path/to\x00/file",
            "\x00malicious.exe",
        ]

        for path in paths_with_null:
            with self.subTest(path=path):
                result = self.validator.validate_path(path)
                self.assertFalse(result['is_valid'])
                self.assertTrue(any("null" in error.lower() for error in result['errors']))

    def test_windows_specific_validation(self):
        """Test Windows-specific validation rules."""
        if self.system != 'Windows':
            self.skipTest("Windows-specific test")

        # Test forbidden characters
        forbidden_chars_paths = [
            "file<name>.txt",
            "file>name.txt",
            "file:name.txt",
            'file"name.txt',
            "file|name.txt",
            "file?name.txt",
            "file*name.txt",
        ]

        for path in forbidden_chars_paths:
            with self.subTest(path=path):
                result = self.validator.validate_path(path)
                self.assertFalse(result['is_valid'])
                self.assertTrue(any("invalid characters" in error.lower() for error in result['errors']))

        # Test reserved names
        reserved_names = ["CON.txt", "PRN.log", "AUX", "NUL.dat", "COM1.txt", "LPT1.txt"]

        for path in reserved_names:
            with self.subTest(path=path):
                result = self.validator.validate_path(path)
                self.assertFalse(result['is_valid'])
                self.assertTrue(any("reserved name" in error.lower() for error in result['errors']))

    def test_posix_specific_validation(self):
        """Test POSIX-specific validation rules."""
        if self.system == 'Windows':
            self.skipTest("POSIX-specific test")

        # POSIX allows most characters except null byte
        allowed_paths = [
            "file<name>.txt",  # These are allowed on POSIX
            "file>name.txt",
            "file:name.txt",
            "file|name.txt",
            "file?name.txt",
            "file*name.txt",
        ]

        for path in allowed_paths:
            with self.subTest(path=path):
                result = self.validator.validate_path(path)
                self.assertTrue(result['is_valid'], f"Path should be valid on POSIX: {path}")

    def test_length_validation(self):
        """Test path length validation."""
        # Test very long path
        long_path = "/very/long/path" + "/component" * 50
        result = self.validator.validate_path(long_path)

        # Should still be valid but with warnings
        self.assertTrue(result['is_valid'])
        self.assertTrue(any("length" in warning.lower() for warning in result['warnings']))

        # Test extremely long component
        long_component = "a" * 300
        long_component_path = f"/path/to/{long_component}"
        result = self.validator.validate_path(long_component_path)
        self.assertTrue(any("component too long" in warning.lower() for warning in result['warnings']))

    def test_traversal_detection(self):
        """Test directory traversal pattern detection."""
        traversal_paths = [
            "../parent/file.txt",
            "../../grandparent/file.txt",
            "path/../other/file.txt",
            "..\\windows\\style",
            "../" * 10 + "deep.txt",
        ]

        for path in traversal_paths:
            with self.subTest(path=path):
                result = self.validator.validate_path(path)
                # Should be valid but with warnings
                self.assertTrue(result['is_valid'])
                self.assertTrue(any("traversal" in warning.lower() for warning in result['warnings']))

    def test_existence_checks(self):
        """Test filesystem existence checks."""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            # Test existing file
            result = self.validator.validate_path(temp_path)
            self.assertTrue(result['is_valid'])
            self.assertTrue(result['exists'])
            self.assertTrue(result['is_file'])
            self.assertFalse(result['is_directory'])

            # Test non-existing file
            nonexistent = temp_path + "_nonexistent"
            result = self.validator.validate_path(nonexistent)
            self.assertTrue(result['is_valid'])
            self.assertFalse(result['exists'])
            self.assertFalse(result['is_file'])
            self.assertFalse(result['is_directory'])

        finally:
            os.unlink(temp_path)

        # Test existing directory
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.validator.validate_path(temp_dir)
            self.assertTrue(result['is_valid'])
            self.assertTrue(result['exists'])
            self.assertFalse(result['is_file'])
            self.assertTrue(result['is_directory'])

    def test_absolute_relative_detection(self):
        """Test absolute vs relative path detection."""
        if self.system == 'Windows':
            absolute_paths = ["C:\\Windows\\System32", "D:\\Data\\file.txt", "\\\\server\\share"]
            relative_paths = ["relative\\path", "..\\parent", ".\\current"]
        else:
            absolute_paths = ["/home/user", "/var/log/syslog", "/tmp"]
            relative_paths = ["relative/path", "../parent", "./current"]

        for path in absolute_paths:
            with self.subTest(path=path):
                result = self.validator.validate_path(path)
                self.assertTrue(result['is_absolute'])

        for path in relative_paths:
            with self.subTest(path=path):
                result = self.validator.validate_path(path)
                self.assertFalse(result['is_absolute'])

    def test_normalization(self):
        """Test path normalization."""
        test_cases = [
            ("./file.txt", "file.txt"),
            ("path//double//slash", "path/double/slash"),
            ("path/../other", "other"),
        ]

        for input_path, expected_normalized in test_cases:
            with self.subTest(input_path=input_path):
                result = self.validator.validate_path(input_path)
                self.assertTrue(result['is_valid'])
                self.assertIsNotNone(result['normalized_path'])
                # Check that normalization occurred
                normalized = result['normalized_path']
                self.assertNotEqual(input_path, normalized)

    def test_convenience_functions(self):
        """Test convenience functions."""
        # Test validate_path function
        result = validate_path("/valid/path")
        self.assertIsInstance(result, dict)
        self.assertIn('is_valid', result)

        # Test is_valid_path function
        self.assertTrue(is_valid_path("/valid/path"))
        self.assertFalse(is_valid_path(""))

    def test_normalize_path_method(self):
        """Test normalize_path method."""
        # Valid path
        normalized = self.validator.normalize_path("./valid/path")
        self.assertIsInstance(normalized, str)

        # Invalid path should raise ValueError
        with self.assertRaises(ValueError):
            self.validator.normalize_path("")

    def test_path_object_input(self):
        """Test validation with Path objects as input."""
        path_obj = Path("/home/user/document.txt")
        result = self.validator.validate_path(path_obj)
        self.assertTrue(result['is_valid'])
        self.assertIsInstance(result['normalized_path'], str)

    def test_edge_cases(self):
        """Test edge cases and unusual inputs."""
        edge_cases = [
            " ",  # Single space
            "   ",  # Multiple spaces
            "\t",  # Tab character
            "\n",  # Newline
        ]

        for path in edge_cases:
            with self.subTest(path=repr(path)):
                result = self.validator.validate_path(path)
                # These should be valid but might have warnings
                self.assertIsInstance(result['is_valid'], bool)

    def test_parent_directory_checks(self):
        """Test parent directory existence checks."""
        # Use temp directory for predictable parent existence
        with tempfile.TemporaryDirectory() as temp_dir:
            # Existing parent
            child_path = os.path.join(temp_dir, "child_file.txt")
            result = self.validator.validate_path(child_path)
            self.assertTrue(result['parent_exists'])

            # Non-existing parent in a deep path
            deep_path = os.path.join(temp_dir, "nonexistent", "very", "deep", "file.txt")
            result = self.validator.validate_path(deep_path)
            self.assertFalse(result['parent_exists'])

    def test_result_structure(self):
        """Test that result structure matches specification."""
        result = self.validator.validate_path("/test/path")

        required_keys = [
            'is_valid', 'exists', 'is_file', 'is_directory',
            'is_absolute', 'normalized_path', 'parent_exists',
            'errors', 'warnings'
        ]

        for key in required_keys:
            with self.subTest(key=key):
                self.assertIn(key, result)

        # Check types
        self.assertIsInstance(result['is_valid'], bool)
        self.assertIsInstance(result['exists'], bool)
        self.assertIsInstance(result['is_file'], bool)
        self.assertIsInstance(result['is_directory'], bool)
        self.assertIsInstance(result['is_absolute'], bool)
        self.assertIsInstance(result['errors'], list)
        self.assertIsInstance(result['warnings'], list)


class TestPlatformSpecificBehavior(unittest.TestCase):
    """Test platform-specific behavior differences."""

    def test_case_sensitivity(self):
        """Test case sensitivity handling."""
        validator = PathValidator()

        if platform.system() == 'Windows':
            # Windows should treat these as potentially the same
            result1 = validator.validate_path("C:\\Windows\\System32")
            result2 = validator.validate_path("c:\\windows\\system32")
            self.assertTrue(result1['is_valid'])
            self.assertTrue(result2['is_valid'])
        else:
            # POSIX treats these as different
            result1 = validator.validate_path("/usr/bin")
            result2 = validator.validate_path("/USR/BIN")
            self.assertTrue(result1['is_valid'])
            self.assertTrue(result2['is_valid'])

    def test_separator_handling(self):
        """Test path separator handling."""
        validator = PathValidator()

        if platform.system() == 'Windows':
            # Both should work on Windows
            result1 = validator.validate_path("C:\\Windows\\System32")
            result2 = validator.validate_path("C:/Windows/System32")
            self.assertTrue(result1['is_valid'])
            self.assertTrue(result2['is_valid'])
        else:
            # Only forward slash on POSIX
            result = validator.validate_path("/usr/bin")
            self.assertTrue(result['is_valid'])


if __name__ == "__main__":
    # Run the demo first
    print("Running demonstration...")
    from simple_path_validator import demo
    demo()

    print("\n" + "="*60)
    print("Running comprehensive tests...")
    unittest.main(verbosity=2)