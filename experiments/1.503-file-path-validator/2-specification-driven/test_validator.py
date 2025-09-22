#!/usr/bin/env python3
"""
Comprehensive test suite for the path validator.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add the path_validator to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from path_validator import (
    PathValidator,
    ValidationConfig,
    SecurityPolicy,
    SymlinkPolicy,
    validate_path,
    is_valid_path,
    BatchPathValidator,
    PathValidationError,
    PathSyntaxError,
    PathSecurityError,
    PathTraversalError,
    PathPlatformError,
    PathLengthError,
)


class TestBasicValidation(unittest.TestCase):
    """Test basic path validation functionality."""

    def setUp(self):
        self.validator = PathValidator()

    def test_valid_absolute_paths(self):
        """Test validation of valid absolute paths."""
        if os.name == 'nt':  # Windows
            test_paths = [
                'C:\\Users\\test\\file.txt',
                'D:\\Documents\\folder\\',
                'C:\\',
                'Z:\\very\\long\\path\\to\\file.ext'
            ]
        else:  # POSIX
            test_paths = [
                '/home/user/file.txt',
                '/var/log/system.log',
                '/tmp/',
                '/usr/local/bin/executable'
            ]

        for path in test_paths:
            with self.subTest(path=path):
                result = self.validator.validate(path)
                self.assertTrue(result.valid, f"Path should be valid: {path}")
                self.assertIsNotNone(result.normalized_path)

    def test_valid_relative_paths(self):
        """Test validation of valid relative paths."""
        test_paths = [
            'file.txt',
            'folder/file.txt',
            './current/file.txt',
            'documents/projects/readme.md'
        ]

        for path in test_paths:
            with self.subTest(path=path):
                result = self.validator.validate(path)
                self.assertTrue(result.valid, f"Path should be valid: {path}")

    def test_empty_path(self):
        """Test that empty paths are rejected."""
        result = self.validator.validate('')
        self.assertFalse(result.valid)
        self.assertIsInstance(result.error, PathSyntaxError)

    def test_null_byte_injection(self):
        """Test that null byte injection is detected."""
        malicious_paths = [
            'file.txt\x00.exe',
            'normal/path\x00../../../etc/passwd',
            '\x00malicious'
        ]

        for path in malicious_paths:
            with self.subTest(path=path):
                result = self.validator.validate(path)
                self.assertFalse(result.valid)
                self.assertIsInstance(result.error, PathSyntaxError)


class TestSecurityValidation(unittest.TestCase):
    """Test security-related validation features."""

    def setUp(self):
        security_policy = SecurityPolicy(
            prevent_traversal=True,
            sanitize_input=True
        )
        config = ValidationConfig(security_policy=security_policy)
        self.validator = PathValidator(config)

    def test_path_traversal_detection(self):
        """Test detection of path traversal attacks."""
        traversal_paths = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system32\\config\\sam',
            'normal/path/../../../sensitive',
            '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
            '....//....//....//etc/passwd',
            '\u002e\u002e\u002fconfig'
        ]

        for path in traversal_paths:
            with self.subTest(path=path):
                result = self.validator.validate(path)
                self.assertFalse(result.valid, f"Traversal should be detected: {path}")
                self.assertIsInstance(result.error, (PathTraversalError, PathSecurityError))

    def test_control_character_detection(self):
        """Test detection of control characters."""
        control_paths = [
            'file\rname.txt',
            'file\nname.txt',
            'file\tname.txt',
            'file\x01name.txt'
        ]

        for path in control_paths:
            with self.subTest(path=path):
                result = self.validator.validate(path)
                # Some control chars might be allowed, but should at least be sanitized
                if not result.valid:
                    self.assertIsInstance(result.error, PathSecurityError)

    def test_sandbox_validation(self):
        """Test sandbox constraint validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            security_policy = SecurityPolicy(
                sandbox_roots=[temp_dir],
                prevent_traversal=True
            )
            config = ValidationConfig(security_policy=security_policy)
            validator = PathValidator(config)

            # Valid path within sandbox
            valid_path = os.path.join(temp_dir, 'allowed_file.txt')
            result = validator.validate(valid_path)
            self.assertTrue(result.valid)

            # Invalid path outside sandbox
            invalid_path = '/etc/passwd'
            result = validator.validate(invalid_path)
            self.assertFalse(result.valid)
            self.assertIsInstance(result.error, PathSecurityError)


class TestPlatformSpecificValidation(unittest.TestCase):
    """Test platform-specific validation rules."""

    def test_windows_reserved_names(self):
        """Test Windows reserved name detection."""
        config = ValidationConfig(target_platform='windows')
        validator = PathValidator(config)

        reserved_names = [
            'CON.txt',
            'PRN',
            'AUX.log',
            'COM1.dat',
            'LPT1.tmp'
        ]

        for name in reserved_names:
            with self.subTest(name=name):
                result = validator.validate(name)
                self.assertFalse(result.valid, f"Reserved name should be rejected: {name}")
                self.assertIsInstance(result.error, PathPlatformError)

    def test_windows_forbidden_characters(self):
        """Test Windows forbidden character detection."""
        config = ValidationConfig(target_platform='windows')
        validator = PathValidator(config)

        forbidden_paths = [
            'file<name.txt',
            'file>name.txt',
            'file:name.txt',
            'file"name.txt',
            'file|name.txt',
            'file?name.txt',
            'file*name.txt'
        ]

        for path in forbidden_paths:
            with self.subTest(path=path):
                result = validator.validate(path)
                self.assertFalse(result.valid, f"Forbidden char should be detected: {path}")
                self.assertIsInstance(result.error, PathSyntaxError)

    def test_path_length_limits(self):
        """Test path length validation."""
        config = ValidationConfig(max_path_length=100)
        validator = PathValidator(config)

        # Valid short path
        short_path = 'short.txt'
        result = validator.validate(short_path)
        self.assertTrue(result.valid)

        # Invalid long path
        long_path = 'a' * 150 + '.txt'
        result = validator.validate(long_path)
        self.assertFalse(result.valid)
        self.assertIsInstance(result.error, PathLengthError)


class TestNormalization(unittest.TestCase):
    """Test path normalization functionality."""

    def setUp(self):
        self.validator = PathValidator()

    def test_separator_normalization(self):
        """Test path separator normalization."""
        if os.name == 'nt':  # Windows
            test_cases = [
                ('path/to/file.txt', 'path\\to\\file.txt'),
                ('mixed\\path/to\\file', 'mixed\\path\\to\\file')
            ]
        else:  # POSIX
            test_cases = [
                ('path\\to\\file.txt', 'path/to/file.txt'),
                ('mixed/path\\to/file', 'mixed/path/to/file')
            ]

        for input_path, expected in test_cases:
            with self.subTest(input_path=input_path):
                result = self.validator.validate(input_path)
                if result.valid:
                    self.assertEqual(result.normalized_path, expected)

    def test_redundant_separator_removal(self):
        """Test removal of redundant separators."""
        test_cases = [
            ('path//to//file.txt', 'path/to/file.txt'),
            ('path/./to/file.txt', 'path/to/file.txt'),
        ]

        for input_path, expected_pattern in test_cases:
            with self.subTest(input_path=input_path):
                result = self.validator.validate(input_path)
                if result.valid:
                    # Check that redundant separators are removed
                    self.assertNotIn('//', result.normalized_path)
                    self.assertNotIn('/./', result.normalized_path)


class TestBatchValidation(unittest.TestCase):
    """Test batch validation functionality."""

    def setUp(self):
        self.batch_validator = BatchPathValidator()

    def test_batch_validation_mixed(self):
        """Test batch validation with mixed valid/invalid paths."""
        test_paths = [
            'valid/path/file1.txt',
            'another/valid/path.log',
            '../../../etc/passwd',  # Invalid traversal
            'valid_file.doc',
            'CON.txt',  # May be invalid on Windows
            'normal/file.txt'
        ]

        result = self.batch_validator.validate_batch(test_paths)
        self.assertEqual(len(result.results), len(test_paths))
        self.assertGreater(result.valid_count, 0)
        self.assertGreater(result.invalid_count, 0)

    def test_batch_performance(self):
        """Test batch validation performance."""
        # Generate test paths
        test_paths = [f'path_{i}/file_{i}.txt' for i in range(100)]

        # Test sequential processing
        result_seq = self.batch_validator.validate_batch(test_paths, parallel=False)

        # Test parallel processing
        result_par = self.batch_validator.validate_batch(test_paths, parallel=True)

        # Both should have same results
        self.assertEqual(len(result_seq.results), len(result_par.results))
        self.assertEqual(result_seq.valid_count, result_par.valid_count)

    def test_filter_valid_paths(self):
        """Test filtering to only valid paths."""
        test_paths = [
            'valid/path1.txt',
            '../invalid/traversal',
            'valid/path2.log',
            'valid_file.doc'
        ]

        valid_paths = self.batch_validator.filter_valid_paths(test_paths)
        self.assertGreater(len(valid_paths), 0)
        self.assertLess(len(valid_paths), len(test_paths))

        # All returned paths should be valid
        validator = PathValidator()
        for path in valid_paths:
            result = validator.validate(path)
            self.assertTrue(result.valid, f"Filtered path should be valid: {path}")


class TestConfigurationManagement(unittest.TestCase):
    """Test configuration management functionality."""

    def test_default_configuration(self):
        """Test default configuration values."""
        config = ValidationConfig()
        self.assertTrue(config.strict_mode)
        self.assertIsNone(config.target_platform)
        self.assertEqual(config.max_path_length, 4096)
        self.assertIsNotNone(config.security_policy)

    def test_custom_configuration(self):
        """Test custom configuration settings."""
        security_policy = SecurityPolicy(
            prevent_traversal=False,
            max_path_length=1000
        )
        config = ValidationConfig(
            strict_mode=False,
            target_platform='windows',
            max_path_length=500,
            security_policy=security_policy
        )

        validator = PathValidator(config)
        self.assertEqual(validator.config.max_path_length, 500)
        self.assertEqual(validator.config.target_platform, 'windows')
        self.assertFalse(validator.config.strict_mode)

    def test_symlink_policy_configuration(self):
        """Test symlink policy configuration."""
        for policy in SymlinkPolicy:
            with self.subTest(policy=policy):
                security_policy = SecurityPolicy(symlink_policy=policy)
                config = ValidationConfig(security_policy=security_policy)
                validator = PathValidator(config)
                self.assertEqual(validator.config.security_policy.symlink_policy, policy)


class TestConvenienceFunctions(unittest.TestCase):
    """Test standalone convenience functions."""

    def test_validate_path_function(self):
        """Test standalone validate_path function."""
        result = validate_path('valid/path.txt')
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'valid'))

    def test_is_valid_path_function(self):
        """Test standalone is_valid_path function."""
        # Valid path
        self.assertTrue(is_valid_path('valid/path.txt'))

        # Invalid path (traversal)
        self.assertFalse(is_valid_path('../../../etc/passwd'))

    def test_normalize_path_function(self):
        """Test standalone normalize_path function."""
        from path_validator.validators.sync import normalize_path

        normalized = normalize_path('path/with/./redundant/../separators')
        self.assertNotIn('/./', normalized)
        self.assertNotIn('/../', normalized)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and reporting."""

    def setUp(self):
        self.validator = PathValidator()

    def test_error_suggestions(self):
        """Test that validation errors include helpful suggestions."""
        # Test traversal error
        result = self.validator.validate('../../../etc/passwd')
        self.assertFalse(result.valid)
        self.assertGreater(len(result.suggestions), 0)

        # Test length error
        config = ValidationConfig(max_path_length=10)
        validator = PathValidator(config)
        result = validator.validate('very_long_path_name.txt')
        self.assertFalse(result.valid)
        self.assertGreater(len(result.suggestions), 0)

    def test_error_metadata(self):
        """Test that errors include useful metadata."""
        config = ValidationConfig(max_path_length=20)
        validator = PathValidator(config)
        result = validator.validate('this_is_a_very_long_path_name.txt')

        if not result.valid and isinstance(result.error, PathLengthError):
            self.assertIsNotNone(result.error.actual_length)
            self.assertIsNotNone(result.error.max_length)


def run_basic_smoke_test():
    """Run a basic smoke test to verify the library works."""
    print("Running basic smoke test...")

    try:
        # Test basic validation
        validator = PathValidator()
        result = validator.validate('test/path.txt')
        print(f"✓ Basic validation: {'PASS' if result.valid else 'FAIL'}")

        # Test batch validation
        batch_validator = BatchPathValidator()
        paths = ['path1.txt', 'path2.txt', '../invalid']
        batch_result = batch_validator.validate_batch(paths)
        print(f"✓ Batch validation: PASS ({batch_result.valid_count}/{batch_result.total_count} valid)")

        # Test convenience functions
        is_valid = is_valid_path('simple/path.txt')
        print(f"✓ Convenience functions: {'PASS' if is_valid else 'FAIL'}")

        # Test security validation
        security_result = validator.validate('../../../etc/passwd')
        print(f"✓ Security validation: {'PASS' if not security_result.valid else 'FAIL'}")

        print("\n✅ All smoke tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Smoke test failed: {e}")
        return False


if __name__ == '__main__':
    print("File Path Validator - Test Suite")
    print("=" * 50)

    # Run smoke test first
    if not run_basic_smoke_test():
        sys.exit(1)

    print("\nRunning comprehensive test suite...")
    print("-" * 40)

    # Run unittest suite
    unittest.main(argv=[''], exit=False, verbosity=2)

    print("\n🎉 Test suite completed!")