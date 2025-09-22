#!/usr/bin/env python3
"""
Test file for file path validator using os.path and pathlib libraries.
Tests various file path validation scenarios including:
- Valid absolute and relative paths
- Invalid characters and path structures
- Cross-platform compatibility
- Security considerations (path traversal)
- Edge cases
"""

import unittest
import os
import tempfile
from pathlib import Path
from file_path_validator import FilePathValidator


class TestFilePathValidator(unittest.TestCase):
    """Test cases for FilePathValidator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = FilePathValidator()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "test_file.txt")
        with open(self.temp_file, 'w') as f:
            f.write("test content")

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_valid_absolute_path(self):
        """Test validation of valid absolute paths"""
        valid_paths = [
            "/home/user/documents/file.txt",
            "/tmp/test.log",
            "/usr/local/bin/python3",
            self.temp_file
        ]

        for path in valid_paths:
            with self.subTest(path=path):
                result = self.validator.is_valid_path(path)
                self.assertTrue(result.is_valid, f"Path should be valid: {path}")
                self.assertEqual(result.path_type, "absolute")

    def test_valid_relative_path(self):
        """Test validation of valid relative paths"""
        valid_paths = [
            "documents/file.txt",
            "./config.ini",
            "../parent/file.py",
            "subdirectory/another/file.json"
        ]

        for path in valid_paths:
            with self.subTest(path=path):
                result = self.validator.is_valid_path(path)
                self.assertTrue(result.is_valid, f"Path should be valid: {path}")
                self.assertEqual(result.path_type, "relative")

    def test_invalid_characters(self):
        """Test rejection of paths with invalid characters"""
        if os.name == 'nt':  # Windows
            invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
            invalid_paths = [f"file{char}name.txt" for char in invalid_chars]
        else:  # Unix-like systems
            invalid_paths = [
                "file\x00name.txt",  # null character
                "file\x01name.txt",  # control character
            ]

        for path in invalid_paths:
            with self.subTest(path=path):
                result = self.validator.is_valid_path(path)
                self.assertFalse(result.is_valid, f"Path should be invalid: {path}")
                self.assertIn("invalid character", result.error_message.lower())

    def test_path_traversal_security(self):
        """Test protection against path traversal attacks"""
        malicious_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config",
            "../../../../../../root/.ssh/id_rsa",
            "/etc/passwd",
            "C:\\Windows\\System32\\config\\SAM"
        ]

        for path in malicious_paths:
            with self.subTest(path=path):
                result = self.validator.is_secure_path(path, "/home/user/sandbox")
                self.assertFalse(result.is_secure, f"Path should be insecure: {path}")

    def test_path_length_limits(self):
        """Test validation of path length limits"""
        # Test extremely long path
        long_path = "a" * 5000  # Very long path
        result = self.validator.is_valid_path(long_path)
        self.assertFalse(result.is_valid)
        self.assertIn("too long", result.error_message.lower())

        # Test reasonable length path
        normal_path = "documents/file.txt"
        result = self.validator.is_valid_path(normal_path)
        self.assertTrue(result.is_valid)

    def test_empty_and_whitespace_paths(self):
        """Test handling of empty and whitespace-only paths"""
        invalid_paths = ["", "   ", "\t", "\n", "  \t  \n  "]

        for path in invalid_paths:
            with self.subTest(path=repr(path)):
                result = self.validator.is_valid_path(path)
                self.assertFalse(result.is_valid, f"Path should be invalid: {repr(path)}")

    def test_reserved_names_windows(self):
        """Test handling of Windows reserved names"""
        if os.name == 'nt':
            reserved_names = [
                "CON", "PRN", "AUX", "NUL",
                "COM1", "COM2", "COM9",
                "LPT1", "LPT2", "LPT9",
                "con.txt", "aux.log"
            ]

            for name in reserved_names:
                with self.subTest(name=name):
                    result = self.validator.is_valid_path(name)
                    self.assertFalse(result.is_valid, f"Reserved name should be invalid: {name}")

    def test_path_exists_check(self):
        """Test checking if path exists"""
        # Existing file
        result = self.validator.path_exists(self.temp_file)
        self.assertTrue(result.exists)
        self.assertEqual(result.path_type, "file")

        # Existing directory
        result = self.validator.path_exists(self.temp_dir)
        self.assertTrue(result.exists)
        self.assertEqual(result.path_type, "directory")

        # Non-existing path
        result = self.validator.path_exists("/nonexistent/path/file.txt")
        self.assertFalse(result.exists)

    def test_path_normalization(self):
        """Test path normalization functionality"""
        test_cases = [
            ("./documents/../config.ini", "config.ini"),
            ("/home/user/../user/file.txt", "/home/user/file.txt"),
            ("documents//subdirectory///file.txt", "documents/subdirectory/file.txt"),
        ]

        for input_path, expected in test_cases:
            with self.subTest(input_path=input_path):
                result = self.validator.normalize_path(input_path)
                self.assertEqual(result.normalized_path, expected)

    def test_pathlib_integration(self):
        """Test integration with pathlib.Path objects"""
        path_obj = Path("documents/file.txt")
        result = self.validator.is_valid_path(path_obj)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.original_input_type, "pathlib.Path")

    def test_cross_platform_compatibility(self):
        """Test cross-platform path handling"""
        # Test both forward and backward slashes
        paths = [
            "documents/subdirectory/file.txt",
            "documents\\subdirectory\\file.txt"
        ]

        for path in paths:
            with self.subTest(path=path):
                result = self.validator.is_valid_path(path)
                # Should normalize to platform-appropriate separators
                self.assertTrue(result.is_valid)

    def test_validator_configuration(self):
        """Test validator with different configurations"""
        # Strict validator (no relative paths, no path traversal)
        strict_validator = FilePathValidator(
            allow_relative=False,
            allow_path_traversal=False,
            max_length=255
        )

        # Test relative path rejection
        result = strict_validator.is_valid_path("../documents/file.txt")
        self.assertFalse(result.is_valid)

        # Permissive validator
        permissive_validator = FilePathValidator(
            allow_relative=True,
            allow_path_traversal=True,
            max_length=1000
        )

        # Test relative path acceptance
        result = permissive_validator.is_valid_path("../documents/file.txt")
        self.assertTrue(result.is_valid)


if __name__ == '__main__':
    unittest.main()