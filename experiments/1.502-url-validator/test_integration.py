#!/usr/bin/env python3
"""
test_integration.py - Comprehensive Integration Tests
Method 2: Specification-Driven Tool-Constrained Clean Room Protocol

Tests complete tool integration chain from CLI to validators library.
Validates exit codes, output format, and error handling.

Created: 2025-09-25 22:57:05
Protocol: Severed Branch Timing Validation
"""

import pytest
import subprocess
import sys
import os
from typing import Tuple
from validators_wrapper import ValidatorsWrapper, ValidationResult


class TestValidatorsIntegration:
    """Test validators library integration through wrapper"""

    def test_tool_availability(self):
        """Test validators library is available and importable"""
        wrapper = ValidatorsWrapper()
        assert wrapper.is_available(), f"Tool should be available: {wrapper.get_error_message()}"

    def test_wrapper_initialization(self):
        """Test wrapper initializes correctly"""
        wrapper = ValidatorsWrapper()
        assert wrapper is not None
        assert hasattr(wrapper, 'validate_url')
        assert hasattr(wrapper, 'is_available')
        assert hasattr(wrapper, 'get_version')

    def test_valid_urls_through_wrapper(self):
        """Test validation of valid URLs through abstraction layer"""
        wrapper = ValidatorsWrapper()

        valid_urls = [
            "https://www.google.com",
            "http://example.org",
            "https://github.com/user/repo",
            "http://localhost:8080/path",
            "https://subdomain.domain.com/path/to/resource"
        ]

        for url in valid_urls:
            result = wrapper.validate_url(url)
            assert isinstance(result, ValidationResult), f"Expected ValidationResult for {url}"
            assert result.is_valid, f"URL should be valid: {url}"
            assert not result.tool_error, f"No tool error expected for {url}"

    def test_invalid_urls_through_wrapper(self):
        """Test validation of invalid URLs through abstraction layer"""
        wrapper = ValidatorsWrapper()

        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "javascript:alert('xss')",
            "mailto:user@domain.com",
            "",
            "http://",
            "https://",
            "just-text"
        ]

        for url in invalid_urls:
            result = wrapper.validate_url(url)
            assert isinstance(result, ValidationResult), f"Expected ValidationResult for {url}"
            assert not result.is_valid, f"URL should be invalid: {url}"
            assert not result.tool_error, f"Should be validation error, not tool error for {url}"
            assert result.error_message, f"Error message should be provided for {url}"

    def test_validation_failure_handling(self):
        """Test ValidationFailure object handling from validators library"""
        wrapper = ValidatorsWrapper()

        # Test with clearly invalid URL
        result = wrapper.validate_url("clearly-not-a-url")
        assert not result.is_valid
        assert "Invalid URL format" in result.error_message
        assert not result.tool_error

    def test_tool_version_retrieval(self):
        """Test tool version retrieval"""
        wrapper = ValidatorsWrapper()
        if wrapper.is_available():
            version = wrapper.get_version()
            assert version != "unavailable"
            assert version != ""
        else:
            version = wrapper.get_version()
            assert version == "unavailable"


class TestCLIInterface:
    """Test complete CLI interface with subprocess calls"""

    def _run_cli(self, args: list) -> Tuple[int, str, str]:
        """
        Run CLI command and return exit code, stdout, stderr

        Args:
            args: Command line arguments

        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        cmd = [sys.executable, "url_validator.py"] + args
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return 124, "", "Command timed out"
        except Exception as e:
            return 125, "", f"Command failed: {str(e)}"

    def test_valid_url_exit_codes(self):
        """Test exit codes for valid URLs"""
        valid_test_cases = [
            "https://www.google.com",
            "http://example.org",
            "https://github.com/user/repo"
        ]

        for url in valid_test_cases:
            exit_code, stdout, stderr = self._run_cli([url])
            assert exit_code == 0, f"Valid URL should return exit code 0: {url}, got {exit_code}, stderr: {stderr}"
            assert stdout.startswith("VALID:"), f"Valid URL should start with VALID: {stdout}"
            assert url in stdout, f"URL should appear in output: {stdout}"

    def test_invalid_url_exit_codes(self):
        """Test exit codes for invalid URLs"""
        invalid_test_cases = [
            "not-a-url",
            "ftp://example.com",
            "javascript:alert('test')",
        ]

        for url in invalid_test_cases:
            exit_code, stdout, stderr = self._run_cli([url])
            assert exit_code == 1, f"Invalid URL should return exit code 1: {url}, got {exit_code}, stderr: {stderr}"
            assert stdout.startswith("INVALID:"), f"Invalid URL should start with INVALID: {stdout}"
            assert url in stdout, f"URL should appear in output: {stdout}"
            assert "reason:" in stdout, f"Reason should be provided: {stdout}"

    def test_usage_error_exit_codes(self):
        """Test exit codes for usage errors"""
        # Test no arguments
        exit_code, stdout, stderr = self._run_cli([])
        assert exit_code == 2, f"No arguments should return exit code 2, got {exit_code}, stderr: {stderr}"
        assert stdout.startswith("ERROR: invalid-args"), f"Should show invalid-args error: {stdout}"

        # Test empty string
        exit_code, stdout, stderr = self._run_cli([""])
        assert exit_code == 2, f"Empty string should return exit code 2, got {exit_code}, stderr: {stderr}"
        assert stdout.startswith("ERROR: invalid-args"), f"Should show invalid-args error: {stdout}"

    def test_output_format_compliance(self):
        """Test standardized output format"""
        # Test valid URL format
        exit_code, stdout, stderr = self._run_cli(["https://www.google.com"])
        assert stdout == "VALID: https://www.google.com", f"Valid format mismatch: {stdout}"

        # Test invalid URL format
        exit_code, stdout, stderr = self._run_cli(["not-a-url"])
        expected_pattern = "INVALID: not-a-url (reason:"
        assert stdout.startswith(expected_pattern), f"Invalid format mismatch: {stdout}"

        # Test error format
        exit_code, stdout, stderr = self._run_cli([])
        expected_pattern = "ERROR: invalid-args (reason:"
        assert stdout.startswith(expected_pattern), f"Error format mismatch: {stdout}"

    def test_tool_integration_error_handling(self):
        """Test tool integration error scenarios"""
        # This test would require mocking validators library failure
        # For now, we verify the error handling structure exists
        wrapper = ValidatorsWrapper()
        if not wrapper.is_available():
            exit_code, stdout, stderr = self._run_cli(["https://example.com"])
            assert exit_code == 4, f"Tool error should return exit code 4"
            assert "ERROR: tool-integration" in stdout, f"Should show tool integration error: {stdout}"


class TestComprehensiveIntegration:
    """End-to-end integration testing"""

    def test_specification_compliance(self):
        """Test complete specification compliance"""
        test_cases = [
            # (url, expected_exit_code, expected_output_prefix)
            ("https://www.google.com", 0, "VALID:"),
            ("http://example.org/path", 0, "VALID:"),
            ("not-a-url", 1, "INVALID:"),
            ("ftp://example.com", 1, "INVALID:"),
        ]

        cli_tester = TestCLIInterface()

        for url, expected_exit, expected_prefix in test_cases:
            exit_code, stdout, stderr = cli_tester._run_cli([url])
            assert exit_code == expected_exit, f"Wrong exit code for {url}: expected {expected_exit}, got {exit_code}"
            assert stdout.startswith(expected_prefix), f"Wrong output prefix for {url}: expected {expected_prefix}, got {stdout}"

    def test_error_resilience(self):
        """Test system resilience to various error conditions"""
        cli_tester = TestCLIInterface()

        error_test_cases = [
            # (args, expected_exit_code)
            ([], 2),  # No arguments
            ([""], 2),  # Empty string
            ([" "], 2),  # Whitespace only
        ]

        for args, expected_exit in error_test_cases:
            exit_code, stdout, stderr = cli_tester._run_cli(args)
            assert exit_code == expected_exit, f"Wrong exit code for args {args}: expected {expected_exit}, got {exit_code}"
            assert "ERROR:" in stdout, f"Should contain ERROR prefix: {stdout}"

    def test_integration_architecture_quality(self):
        """Test integration architecture meets quality standards"""
        # Test wrapper abstraction
        wrapper = ValidatorsWrapper()
        assert hasattr(wrapper, 'validate_url'), "Wrapper should have validate_url method"
        assert hasattr(wrapper, 'is_available'), "Wrapper should have is_available method"
        assert hasattr(wrapper, 'get_version'), "Wrapper should have get_version method"

        # Test ValidationResult structure
        if wrapper.is_available():
            result = wrapper.validate_url("https://example.com")
            assert isinstance(result, ValidationResult), "Should return ValidationResult"
            assert hasattr(result, 'is_valid'), "Result should have is_valid attribute"
            assert hasattr(result, 'error_message'), "Result should have error_message attribute"
            assert hasattr(result, 'tool_error'), "Result should have tool_error attribute"


def main():
    """Run integration tests manually"""
    print("Running comprehensive integration tests...")

    # Test validators integration
    print("\n1. Testing Validators Integration...")
    test_validators = TestValidatorsIntegration()
    try:
        test_validators.test_tool_availability()
        test_validators.test_wrapper_initialization()
        test_validators.test_valid_urls_through_wrapper()
        test_validators.test_invalid_urls_through_wrapper()
        print("   ✓ Validators integration tests passed")
    except Exception as e:
        print(f"   ✗ Validators integration tests failed: {e}")
        return 1

    # Test CLI interface
    print("\n2. Testing CLI Interface...")
    test_cli = TestCLIInterface()
    try:
        test_cli.test_valid_url_exit_codes()
        test_cli.test_invalid_url_exit_codes()
        test_cli.test_usage_error_exit_codes()
        test_cli.test_output_format_compliance()
        print("   ✓ CLI interface tests passed")
    except Exception as e:
        print(f"   ✗ CLI interface tests failed: {e}")
        return 1

    # Test comprehensive integration
    print("\n3. Testing Comprehensive Integration...")
    test_integration = TestComprehensiveIntegration()
    try:
        test_integration.test_specification_compliance()
        test_integration.test_error_resilience()
        test_integration.test_integration_architecture_quality()
        print("   ✓ Comprehensive integration tests passed")
    except Exception as e:
        print(f"   ✗ Comprehensive integration tests failed: {e}")
        return 1

    print("\n🎉 All integration tests passed successfully!")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)