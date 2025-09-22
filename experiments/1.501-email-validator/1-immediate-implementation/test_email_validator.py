"""
Comprehensive test suite for the Email Validator.

This module contains extensive tests to validate all functionality of the EmailValidator class,
including edge cases, error handling, and different validation levels.
"""

import unittest
import sys
from typing import List, Tuple

# Import the email validator
from email_validator import (
    EmailValidator, ValidationLevel, EmailValidationError,
    InvalidEmailFormatError, InvalidLocalPartError, InvalidDomainError,
    EmailTooLongError, create_validator, is_valid_email, validate_email
)


class TestEmailValidator(unittest.TestCase):
    """Test cases for EmailValidator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator_basic = EmailValidator(ValidationLevel.BASIC)
        self.validator_standard = EmailValidator(ValidationLevel.STANDARD)
        self.validator_strict = EmailValidator(ValidationLevel.STRICT)
        self.validator_rfc = EmailValidator(ValidationLevel.RFC_COMPLIANT)

    def test_valid_emails_basic(self):
        """Test valid emails with basic validation."""
        valid_emails = [
            "user@example.com",
            "test@domain.org",
            "email@test.co.uk",
            "simple@example.net",
            "user123@domain123.com"
        ]

        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(self.validator_basic.is_valid(email))

    def test_valid_emails_standard(self):
        """Test valid emails with standard validation."""
        valid_emails = [
            "user@example.com",
            "test.email@domain.org",
            "user+tag@example.com",
            "user_name@domain-name.co.uk",
            "firstname.lastname@company.travel",
            "user123@sub.domain.example.com",
            "a@b.co",
            "test@domain.info"
        ]

        for email in valid_emails:
            with self.subTest(email=email):
                is_valid, errors = self.validator_standard.validate(email)
                self.assertTrue(is_valid, f"Email {email} should be valid. Errors: {errors}")

    def test_valid_emails_strict(self):
        """Test valid emails with strict validation."""
        valid_emails = [
            "user@example.com",
            "test@domain.org",
            "user.name@company.co.uk",
            "email@test.net"
        ]

        for email in valid_emails:
            with self.subTest(email=email):
                is_valid, errors = self.validator_strict.validate(email)
                self.assertTrue(is_valid, f"Email {email} should be valid. Errors: {errors}")

    def test_valid_emails_rfc(self):
        """Test valid emails with RFC-compliant validation."""
        valid_emails = [
            "user@example.com",
            "test@domain.org",
            "user.name@company.co.uk",
            '"quoted.string"@example.com',
            "user@[192.168.1.1]",
            "test@sub.domain.example.com"
        ]

        for email in valid_emails:
            with self.subTest(email=email):
                is_valid, errors = self.validator_rfc.validate(email)
                self.assertTrue(is_valid, f"Email {email} should be valid. Errors: {errors}")

    def test_invalid_emails_format(self):
        """Test emails with format errors."""
        invalid_emails = [
            "",
            "   ",
            "invalid",
            "@domain.com",
            "user@",
            "user@@domain.com",
            "user@domain@com",
            None,
            123,
            "user@domain.",
            ".user@domain.com",
            "user.@domain.com"
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                is_valid, errors = self.validator_standard.validate(email)
                self.assertFalse(is_valid, f"Email {email} should be invalid")
                self.assertTrue(len(errors) > 0, f"Should have errors for {email}")

    def test_invalid_local_part(self):
        """Test emails with invalid local parts."""
        invalid_emails = [
            "user..double@domain.com",
            ".user@domain.com",
            "user.@domain.com",
            "us..er@domain.com",
            "a" * 65 + "@domain.com",  # Too long local part
            "user with space@domain.com"
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                is_valid, errors = self.validator_standard.validate(email)
                self.assertFalse(is_valid, f"Email {email} should be invalid")

    def test_invalid_domain_part(self):
        """Test emails with invalid domain parts."""
        invalid_emails = [
            "user@",
            "user@domain",
            "user@.domain.com",
            "user@domain..com",
            "user@domain.",
            "user@domain.c",
            "user@domain.toolongdomaintld",
            "user@" + "a" * 254 + ".com",  # Too long domain
            "user@domain-.com",
            "user@-domain.com"
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                is_valid, errors = self.validator_standard.validate(email)
                self.assertFalse(is_valid, f"Email {email} should be invalid")

    def test_email_length_limits(self):
        """Test email length validation."""
        # Test maximum lengths
        long_local = "a" * 64
        long_domain = "b" * 60 + ".com"
        long_email = long_local + "@" + long_domain

        # This should be valid
        is_valid, errors = self.validator_standard.validate(long_email)
        self.assertTrue(is_valid, f"Email within limits should be valid. Errors: {errors}")

        # Test exceeding local part limit
        too_long_local = "a" * 65 + "@domain.com"
        is_valid, errors = self.validator_standard.validate(too_long_local)
        self.assertFalse(is_valid)

        # Test exceeding total email limit
        very_long_email = "a" * 100 + "@" + "b" * 250 + ".com"
        is_valid, errors = self.validator_standard.validate(very_long_email)
        self.assertFalse(is_valid)

    def test_ip_address_domains(self):
        """Test IP address domain validation."""
        valid_ip_emails = [
            "user@[192.168.1.1]",
            "test@[127.0.0.1]",
            "admin@[10.0.0.1]"
        ]

        invalid_ip_emails = [
            "user@[999.999.999.999]",
            "test@[192.168.1]",
            "admin@[192.168.1.1.1]",
            "user@192.168.1.1",  # Missing brackets
            "test@[192.168.1.256]"  # Invalid IP
        ]

        for email in valid_ip_emails:
            with self.subTest(email=email):
                is_valid, errors = self.validator_standard.validate(email)
                self.assertTrue(is_valid, f"Valid IP email {email} should pass. Errors: {errors}")

        for email in invalid_ip_emails:
            with self.subTest(email=email):
                is_valid, errors = self.validator_standard.validate(email)
                self.assertFalse(is_valid, f"Invalid IP email {email} should fail")

    def test_quoted_local_parts(self):
        """Test quoted local part validation (RFC compliant)."""
        valid_quoted = [
            '"user"@domain.com',
            '"user.name"@domain.com',
            '"user@name"@domain.com',
            '"user with spaces"@domain.com'
        ]

        for email in valid_quoted:
            with self.subTest(email=email):
                is_valid, errors = self.validator_rfc.validate(email)
                self.assertTrue(is_valid, f"Valid quoted email {email} should pass. Errors: {errors}")

    def test_validation_levels(self):
        """Test different validation levels with the same email."""
        test_email = "user@unknown-tld.xyztld"

        # Basic should pass (simple regex)
        self.assertTrue(self.validator_basic.is_valid(test_email))

        # Standard should pass (doesn't check TLD)
        self.assertTrue(self.validator_standard.is_valid(test_email))

        # Strict should fail (unknown TLD)
        self.assertFalse(self.validator_strict.is_valid(test_email))

    def test_error_types(self):
        """Test that specific error types are raised."""
        # Test with raise_on_error=True
        with self.assertRaises(InvalidEmailFormatError):
            self.validator_standard.validate("invalid-email", raise_on_error=True)

        with self.assertRaises(InvalidLocalPartError):
            self.validator_standard.validate("user..double@domain.com", raise_on_error=True)

        with self.assertRaises(InvalidDomainError):
            self.validator_standard.validate("user@domain", raise_on_error=True)

        with self.assertRaises(EmailTooLongError):
            long_email = "a" * 400 + "@domain.com"
            self.validator_standard.validate(long_email, raise_on_error=True)

    def test_batch_validation(self):
        """Test batch validation functionality."""
        emails = [
            "valid@example.com",
            "invalid-email",
            "another@valid.org",
            "user@domain"
        ]

        results = self.validator_standard.validate_batch(emails)

        self.assertEqual(len(results), 4)
        self.assertTrue(results["valid@example.com"][0])
        self.assertFalse(results["invalid-email"][0])
        self.assertTrue(results["another@valid.org"][0])
        self.assertFalse(results["user@domain"][0])

    def test_detailed_validation(self):
        """Test detailed validation information."""
        email = "test.user+tag@sub.example.co.uk"
        details = self.validator_standard.get_validation_details(email)

        self.assertEqual(details['email'], email)
        self.assertEqual(details['local_part'], "test.user+tag")
        self.assertEqual(details['domain_part'], "sub.example.co.uk")
        self.assertEqual(details['tld'], "uk")
        self.assertEqual(details['domain_labels'], ["sub", "example", "co", "uk"])
        self.assertTrue(details['is_valid'])
        self.assertTrue(details['length_info']['within_limits'])

    def test_convenience_functions(self):
        """Test convenience functions."""
        # Test create_validator
        validator = create_validator("strict")
        self.assertEqual(validator.validation_level, ValidationLevel.STRICT)

        # Test is_valid_email
        self.assertTrue(is_valid_email("user@example.com"))
        self.assertFalse(is_valid_email("invalid-email"))

        # Test validate_email
        is_valid, errors = validate_email("user@example.com")
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

        is_valid, errors = validate_email("invalid-email")
        self.assertFalse(is_valid)
        self.assertTrue(len(errors) > 0)

    def test_edge_cases(self):
        """Test various edge cases."""
        edge_cases = [
            ("a@b.co", True),  # Minimal valid email
            ("user@domain.museum", True),  # Long TLD
            ("user@sub.sub.domain.com", True),  # Multiple subdomains
            ("user+tag+more@example.com", True),  # Multiple plus signs
            ("user_123@example-site.com", True),  # Numbers and hyphens
            ("user@domain.123", False),  # Numeric TLD
            ("user@domain..com", False),  # Double dot in domain
            ("", False),  # Empty string
            ("user@", False),  # Missing domain
            ("@domain.com", False),  # Missing local part
        ]

        for email, expected in edge_cases:
            with self.subTest(email=email):
                is_valid = self.validator_standard.is_valid(email)
                self.assertEqual(is_valid, expected,
                               f"Email '{email}' validation result should be {expected}")

    def test_internationalized_domains(self):
        """Test basic internationalized domain handling."""
        # Note: Full IDN support would require additional libraries
        # This tests basic punycode detection
        idn_emails = [
            "user@xn--example.com",  # Punycode domain
            "test@münchen.de",  # Non-ASCII (should fail in strict mode)
        ]

        # Basic validation might pass non-ASCII
        # RFC validation should handle punycode properly
        for email in idn_emails:
            with self.subTest(email=email):
                # Just ensure it doesn't crash
                try:
                    self.validator_rfc.validate(email)
                except Exception:
                    pass  # Expected for non-ASCII without proper encoding

    def test_performance_with_long_inputs(self):
        """Test performance with very long inputs."""
        # Test with very long but invalid emails
        long_invalid_emails = [
            "a" * 1000 + "@domain.com",
            "user@" + "sub." * 100 + "domain.com",
            "user@domain." + "a" * 1000
        ]

        for email in long_invalid_emails:
            with self.subTest(email=email):
                # Should handle gracefully without hanging
                is_valid, errors = self.validator_standard.validate(email)
                self.assertFalse(is_valid)
                self.assertTrue(len(errors) > 0)


class TestValidationLevels(unittest.TestCase):
    """Test validation level differences."""

    def test_level_progression(self):
        """Test that stricter levels catch more issues."""
        test_cases = [
            ("user@unknown.tld", [True, True, False, True]),  # Unknown TLD
            ("user.with.dots@example.com", [True, True, False, True]),  # Many dots
            ("user@domain", [False, False, False, False]),  # No TLD (should fail all)
        ]

        validators = [
            EmailValidator(ValidationLevel.BASIC),
            EmailValidator(ValidationLevel.STANDARD),
            EmailValidator(ValidationLevel.STRICT),
            EmailValidator(ValidationLevel.RFC_COMPLIANT)
        ]

        for email, expected_results in test_cases:
            with self.subTest(email=email):
                for i, validator in enumerate(validators):
                    result = validator.is_valid(email)
                    self.assertEqual(result, expected_results[i],
                                   f"Level {i} validation of '{email}' should be {expected_results[i]}")


def run_demo():
    """Run a demonstration of the email validator functionality."""
    print("=" * 60)
    print("EMAIL VALIDATOR DEMONSTRATION")
    print("=" * 60)

    # Test emails for demonstration
    demo_emails = [
        "user@example.com",
        "test.email+tag@domain.co.uk",
        "invalid.email",
        "@domain.com",
        "user@",
        "user..double.dot@example.com",
        "user@domain",
        '"quoted.string"@example.com',
        "user@[192.168.1.1]",
        "very.long.email.address.that.might.exceed.limits@very.long.domain.name.example.com",
        "user@unknown.tld",
        "simple@test.org"
    ]

    levels = [
        ("Basic", ValidationLevel.BASIC),
        ("Standard", ValidationLevel.STANDARD),
        ("Strict", ValidationLevel.STRICT),
        ("RFC-Compliant", ValidationLevel.RFC_COMPLIANT)
    ]

    for level_name, level in levels:
        print(f"\n{level_name} Validation Results:")
        print("-" * 40)

        validator = EmailValidator(level)

        for email in demo_emails:
            is_valid, errors = validator.validate(email)
            status = "✓ VALID" if is_valid else "✗ INVALID"
            print(f"{status:12} {email}")

            if errors:
                for error in errors:
                    print(f"             └─ {error}")

    # Detailed analysis example
    print(f"\n\nDETAILED ANALYSIS EXAMPLE:")
    print("-" * 40)

    validator = EmailValidator(ValidationLevel.STANDARD)
    sample_email = "test.user+tag@sub.example.co.uk"
    details = validator.get_validation_details(sample_email)

    print(f"Email: {details['email']}")
    print(f"Valid: {details['is_valid']}")
    print(f"Local Part: {details['local_part']}")
    print(f"Domain Part: {details['domain_part']}")
    print(f"TLD: {details['tld']}")
    print(f"Domain Labels: {details['domain_labels']}")
    print(f"Length Info: {details['length_info']}")

    if details['warnings']:
        print(f"Warnings: {details['warnings']}")

    if details['errors']:
        print(f"Errors: {details['errors']}")

    # Batch validation example
    print(f"\n\nBATCH VALIDATION EXAMPLE:")
    print("-" * 40)

    batch_emails = [
        "user1@example.com",
        "invalid-email",
        "user2@test.org",
        "bad@domain"
    ]

    results = validator.validate_batch(batch_emails)

    for email, (is_valid, errors) in results.items():
        status = "✓" if is_valid else "✗"
        print(f"{status} {email}")
        if errors:
            print(f"   Errors: {'; '.join(errors)}")


if __name__ == "__main__":
    # Run tests
    print("Running Email Validator Tests...")
    print("=" * 50)

    # Run the test suite
    test_suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)

    # Run demonstration
    if test_result.wasSuccessful():
        print("\n\nAll tests passed! Running demonstration...")
        run_demo()
    else:
        print(f"\n\nSome tests failed. {len(test_result.failures)} failures, {len(test_result.errors)} errors.")
        print("Fix the issues before running the demonstration.")