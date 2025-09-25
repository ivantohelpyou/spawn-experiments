"""
Comprehensive test suite for Email Validator
EXPERIMENT 1.501.1 - Method 2: Specification-driven Development

Tests cover all specification requirements systematically.
"""

import unittest
from email_validator import validate_email


class TestEmailValidator(unittest.TestCase):
    """Comprehensive test suite following specification requirements."""

    def test_basic_structure_valid(self):
        """Test basic valid email structures."""
        valid_emails = [
            "user@example.com",
            "test@domain.org",
            "a@b.co",
            "simple@test.net",
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email))

    def test_basic_structure_invalid(self):
        """Test basic invalid structures (no @, multiple @)."""
        invalid_emails = [
            "invalid",
            "invalid.email",
            "@domain.com",
            "user@",
            "user@@domain.com",
            "user@domain@com",
            "",
            None,
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email))

    def test_length_limits(self):
        """Test RFC 5321 length limits."""
        # Test maximum valid lengths
        long_local = "a" * 64  # Max local part
        long_domain = "b" * 59 + ".com"  # Max domain part (63 total)
        max_email = long_local + "@" + long_domain  # 64 + 1 + 63 = 128 chars
        self.assertTrue(validate_email(max_email))

        # Test length violations
        too_long_local = "a" * 65 + "@example.com"
        self.assertFalse(validate_email(too_long_local))

        # Test total email length (254 chars max)
        very_long_domain = "x" * 240 + ".com"
        very_long_email = "test@" + very_long_domain
        if len(very_long_email) > 254:
            self.assertFalse(validate_email(very_long_email))

    def test_local_part_valid_characters(self):
        """Test valid characters in local part."""
        valid_locals = [
            "user@example.com",
            "test123@example.com",
            "user.name@example.com",
            "user_name@example.com",
            "user-name@example.com",
            "user+tag@example.com",
            "123@example.com",
            "a.b.c@example.com",
        ]
        for email in valid_locals:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email))

    def test_local_part_invalid_rules(self):
        """Test local part rule violations."""
        invalid_locals = [
            ".user@example.com",      # Leading dot
            "user.@example.com",      # Trailing dot
            "us..er@example.com",     # Consecutive dots
            "-user@example.com",      # Leading hyphen
            "user-@example.com",      # Trailing hyphen
            "user space@example.com", # Invalid char space
            "user#hash@example.com",  # Invalid char #
        ]
        for email in invalid_locals:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email))

    def test_domain_structure_valid(self):
        """Test valid domain structures."""
        valid_domains = [
            "user@example.com",
            "user@sub.example.com",
            "user@a.b.c.com",
            "user@test-domain.org",
            "user@domain123.net",
        ]
        for email in valid_domains:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email))

    def test_domain_structure_invalid(self):
        """Test invalid domain structures."""
        invalid_domains = [
            "user@domain",            # No dot
            "user@.domain.com",       # Leading dot
            "user@domain.com.",       # Trailing dot
            "user@domain..com",       # Consecutive dots
            "user@domain-.com",       # Label ending with hyphen
            "user@-domain.com",       # Label starting with hyphen
        ]
        for email in invalid_domains:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email))

    def test_tld_validation(self):
        """Test TLD (Top-Level Domain) validation."""
        # Valid TLDs (≥2 chars, letters only)
        valid_tlds = [
            "user@example.co",
            "user@example.com",
            "user@example.org",
            "user@example.info",
        ]
        for email in valid_tlds:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email))

        # Invalid TLDs
        invalid_tlds = [
            "user@example.c",         # Too short (<2 chars)
            "user@example.123",       # Numbers not allowed
            "user@example.c0m",       # Numbers not allowed
            "user@example.c-m",       # Hyphens not allowed
        ]
        for email in invalid_tlds:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email))

    def test_domain_label_length(self):
        """Test domain label length limits (1-63 chars)."""
        # Valid label lengths
        short_label = "user@a.com"
        self.assertTrue(validate_email(short_label))

        max_label = "user@" + "b" * 63 + ".com"
        self.assertTrue(validate_email(max_label))

        # Invalid label length (>63 chars)
        too_long_label = "user@" + "c" * 64 + ".com"
        self.assertFalse(validate_email(too_long_label))

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        edge_cases = [
            # Minimal valid email
            ("a@b.co", True),
            # Empty parts
            ("@domain.com", False),
            ("user@", False),
            # Non-string input
            (123, False),
            ([], False),
            ({}, False),
        ]

        for email, expected in edge_cases:
            with self.subTest(email=email):
                result = validate_email(email)
                self.assertEqual(result, expected)

    def test_specification_compliance(self):
        """Test compliance with specification requirements."""
        # Test cases directly from specification
        spec_test_cases = [
            # Should pass
            ("valid@example.com", True),
            ("user.name@domain.org", True),
            ("test+tag@site.co", True),

            # Should fail - not supported features
            # (IP addresses, quoted strings, internationalized domains would go here
            # but specification explicitly excludes them)

            # Should fail - basic violations
            ("invalid", False),
            ("user@domain", False),
            (".user@domain.com", False),
            ("user@domain.c", False),
        ]

        for email, expected in spec_test_cases:
            with self.subTest(email=email):
                result = validate_email(email)
                self.assertEqual(result, expected,
                    f"Failed for {email}: got {result}, expected {expected}")


if __name__ == "__main__":
    # Run the test suite
    unittest.main(verbosity=2)