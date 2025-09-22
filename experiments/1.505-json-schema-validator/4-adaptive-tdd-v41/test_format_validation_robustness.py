#!/usr/bin/env python3
"""
Adaptive Validation Tests for Format Validation Logic
Testing robustness of format validation with intentionally wrong implementations
"""

import unittest
import sys
import os

# Add the current directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from json_schema_validator import JSONSchemaValidator


class TestFormatValidationRobustness(unittest.TestCase):
    """
    Test format validation robustness by testing edge cases that could
    be implemented incorrectly
    """

    def setUp(self):
        self.validator = JSONSchemaValidator()

    # Email Format Edge Cases
    def test_email_edge_cases(self):
        """Test email validation edge cases that naive implementations might miss"""
        schema = {"type": "string", "format": "email"}

        # Valid emails that might be rejected by naive regex
        valid_emails = [
            "test@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "123@example.com",
            "test@sub.example.com"
        ]

        for email in valid_emails:
            with self.subTest(email=email):
                result = self.validator.validate(email, schema)
                self.assertTrue(result.is_valid, f"Valid email rejected: {email}")

        # Invalid emails that naive implementations might accept
        invalid_emails = [
            "plainaddress",           # No @ symbol
            "@missingdomain.com",     # Missing local part
            "missing@.com",           # Missing domain
            "spaces @example.com",    # Spaces in local part
            "test@",                  # Missing domain entirely
            "test..test@example.com", # Double dots
            ".test@example.com",      # Leading dot
            "test.@example.com",      # Trailing dot
            "",                       # Empty string
            "test@exam ple.com",      # Space in domain
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                result = self.validator.validate(email, schema)
                self.assertFalse(result.is_valid, f"Invalid email accepted: {email}")

    # Date Format Edge Cases
    def test_date_edge_cases(self):
        """Test date validation edge cases"""
        schema = {"type": "string", "format": "date"}

        # Valid dates
        valid_dates = [
            "2023-01-01",
            "2023-12-31",
            "2000-02-29",  # Leap year
        ]

        for date in valid_dates:
            with self.subTest(date=date):
                result = self.validator.validate(date, schema)
                self.assertTrue(result.is_valid, f"Valid date rejected: {date}")

        # Invalid dates that might pass naive regex-only validation
        invalid_dates = [
            "2023-13-01",  # Invalid month
            "2023-01-32",  # Invalid day
            "2023-02-30",  # Invalid day for February
            "2023-00-01",  # Zero month
            "2023-01-00",  # Zero day
            "23-01-01",    # Wrong year format
            "2023-1-1",    # Missing leading zeros
            "2023/01/01",  # Wrong separator
            "01-01-2023",  # Wrong order
            "",            # Empty string
            "not-a-date",  # Not a date at all
            "2023-01",     # Incomplete
            "2023-01-01T10:30:00",  # Date-time instead of date
        ]

        for date in invalid_dates:
            with self.subTest(date=date):
                result = self.validator.validate(date, schema)
                self.assertFalse(result.is_valid, f"Invalid date accepted: {date}")

    # URI Format Edge Cases
    def test_uri_edge_cases(self):
        """Test URI validation edge cases"""
        schema = {"type": "string", "format": "uri"}

        # Valid URIs
        valid_uris = [
            "https://example.com",
            "http://example.com/path",
            "ftp://ftp.example.com",
            "mailto:test@example.com",
            "file:///path/to/file",
            "https://example.com:8080/path?query=value#fragment",
        ]

        for uri in valid_uris:
            with self.subTest(uri=uri):
                result = self.validator.validate(uri, schema)
                self.assertTrue(result.is_valid, f"Valid URI rejected: {uri}")

        # Invalid URIs
        invalid_uris = [
            "not-a-uri",
            "://missing-scheme.com",
            "",
            "just-a-string",
            "http://",  # Incomplete
            "ht tp://example.com",  # Space in scheme
        ]

        for uri in invalid_uris:
            with self.subTest(uri=uri):
                result = self.validator.validate(uri, schema)
                self.assertFalse(result.is_valid, f"Invalid URI accepted: {uri}")

    def test_format_type_mismatch(self):
        """Test format validation when data is not a string"""
        schema = {"type": "string", "format": "email"}

        # Non-string data should fail type validation before format validation
        non_string_data = [123, True, [], {}, None]

        for data in non_string_data:
            with self.subTest(data=data):
                result = self.validator.validate(data, schema)
                self.assertFalse(result.is_valid)
                # Should have type error, not format error
                self.assertTrue(any("type" in error.lower() for error in result.errors))

    def test_unknown_format(self):
        """Test handling of unknown format types"""
        schema = {"type": "string", "format": "unknown-format"}
        data = "some string"

        result = self.validator.validate(data, schema)
        # Should pass type validation and ignore unknown format
        self.assertTrue(result.is_valid)


class TestAdaptiveValidationWrongImplementations(unittest.TestCase):
    """
    Test wrong implementations to verify our tests would catch them
    This is the adaptive validation part - intentionally testing wrong code
    """

    def test_wrong_email_implementation_would_fail(self):
        """
        Verify that a naive email implementation would fail our tests
        """
        # Simulate a naive email validator that only checks for '@'
        class NaiveValidator:
            def validate_email(self, email):
                return '@' in email

        naive = NaiveValidator()

        # Our tests should catch that this naive implementation is wrong
        # These should fail with naive implementation but pass with correct one
        test_cases = [
            ("@missinglocal.com", False),  # Has @ but no local part
            ("missing@", False),           # Has @ but no domain
            ("test@exam ple.com", False),  # Has @ but space in domain
        ]

        correct_validator = JSONSchemaValidator()
        schema = {"type": "string", "format": "email"}

        for email, expected_valid in test_cases:
            naive_result = naive.validate_email(email)
            correct_result = correct_validator.validate(email, schema)

            # Naive implementation would incorrectly validate these
            if not expected_valid:
                self.assertTrue(naive_result, f"Naive incorrectly accepts: {email}")
                self.assertFalse(correct_result.is_valid, f"Correct rejects: {email}")

    def test_wrong_date_implementation_would_fail(self):
        """
        Verify that a naive date implementation would fail our tests
        """
        # Simulate a naive date validator that only checks regex pattern
        import re

        class NaiveValidator:
            def validate_date(self, date):
                pattern = r'^\d{4}-\d{2}-\d{2}$'
                return bool(re.match(pattern, date))

        naive = NaiveValidator()
        correct_validator = JSONSchemaValidator()
        schema = {"type": "string", "format": "date"}

        # These pass regex but are invalid dates
        invalid_but_regex_matching = [
            "2023-13-01",  # Invalid month
            "2023-02-30",  # Invalid day for February
            "2023-00-01",  # Zero month
        ]

        for date in invalid_but_regex_matching:
            naive_result = naive.validate_date(date)
            correct_result = correct_validator.validate(date, schema)

            # Naive implementation would incorrectly validate these
            self.assertTrue(naive_result, f"Naive incorrectly accepts: {date}")
            self.assertFalse(correct_result.is_valid, f"Correct rejects: {date}")


if __name__ == '__main__':
    # Run the robustness tests
    print("Running adaptive validation tests for format validation...")
    unittest.main(verbosity=2)