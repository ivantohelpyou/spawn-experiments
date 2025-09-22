"""
Comprehensive test suite for the Email Validator implementation.

This test suite verifies that the implementation correctly follows all
specifications defined in the email_validator_specifications.md document.
"""

import unittest
from email_validator import validate_email, get_validation_details


class TestEmailValidator(unittest.TestCase):
    """Test cases for email validation according to specifications."""

    def test_valid_emails_standard_cases(self):
        """Test standard valid email formats."""
        valid_emails = [
            "user@example.com",
            "john.doe@company.org",
            "test_email@domain.co.uk",
            "user+tag@example.com",
            "a@b.co",
            "123@example.com",
            "user-name@sub.domain.com"
        ]

        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Should be valid: {email}")

    def test_valid_emails_edge_cases(self):
        """Test edge cases that should be valid."""
        valid_edge_cases = [
            "x@y.ab",  # minimum valid format
            "very.long.local.part@example.com",
            "user+multiple+tags@domain.com",
            "1234567890@example.com",
            "a.b.c.d@example.com",
            "user_name@example.com",
            "user-name@example-domain.com"
        ]

        for email in valid_edge_cases:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Should be valid: {email}")

    def test_invalid_emails_missing_components(self):
        """Test emails with missing components."""
        invalid_emails = [
            "@example.com",  # no local part
            "user@",  # no domain part
            "userexample.com",  # no @ symbol
            "user@@example.com",  # multiple @ symbols
            "user@@@example.com",  # multiple @ symbols
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email), f"Should be invalid: {email}")

    def test_invalid_emails_local_part_violations(self):
        """Test local part violations."""
        invalid_emails = [
            ".user@example.com",  # starts with dot
            "user.@example.com",  # ends with dot
            "user..name@example.com",  # consecutive dots
            "user-@example.com",  # ends with hyphen
            "-user@example.com",  # starts with hyphen
            "@example.com",  # empty local part
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email), f"Should be invalid: {email}")

    def test_invalid_emails_domain_part_violations(self):
        """Test domain part violations."""
        invalid_emails = [
            "user@example",  # no TLD
            "user@.example.com",  # starts with dot
            "user@example.",  # ends with dot
            "user@example..com",  # consecutive dots
            "user@example.c",  # TLD too short
            "user@example.123",  # TLD contains digits
            "user@-example.com",  # domain label starts with hyphen
            "user@example-.com",  # domain label ends with hyphen
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email), f"Should be invalid: {email}")

    def test_length_violations(self):
        """Test length limit violations."""
        # Test local part exceeding 64 characters
        long_local = "a" * 65
        self.assertFalse(validate_email(f"{long_local}@example.com"))

        # Test domain part exceeding 253 characters
        long_domain = "a" * 250 + ".com"  # 254 characters total
        self.assertFalse(validate_email(f"user@{long_domain}"))

        # Test total email exceeding 254 characters
        long_email = "a" * 250 + "@b.co"  # 255 characters total
        self.assertFalse(validate_email(long_email))

        # Test valid lengths at boundaries
        local_64 = "a" * 64
        self.assertTrue(validate_email(f"{local_64}@example.com"))

    def test_input_validation(self):
        """Test handling of None, empty strings, and non-string types."""
        invalid_inputs = [
            None,
            "",
            "   ",  # whitespace only
            123,
            [],
            {},
            True,
            False
        ]

        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                self.assertFalse(validate_email(invalid_input))

    def test_case_sensitivity(self):
        """Test that validation is case-insensitive."""
        test_cases = [
            ("User@Example.Com", True),
            ("USER@EXAMPLE.COM", True),
            ("user@example.com", True),
            ("User.Name@Example.Org", True),
            (".User@Example.Com", False),  # Invalid regardless of case
            ("User@Example", False),  # Invalid regardless of case
        ]

        for email, expected in test_cases:
            with self.subTest(email=email):
                self.assertEqual(validate_email(email), expected)

    def test_whitespace_handling(self):
        """Test handling of whitespace around email addresses."""
        test_cases = [
            ("  user@example.com  ", True),
            ("\tuser@example.com\t", True),
            ("\nuser@example.com\n", True),
            ("  user@example.com", True),
            ("user@example.com  ", True),
        ]

        for email, expected in test_cases:
            with self.subTest(email=email):
                self.assertEqual(validate_email(email), expected)

    def test_special_characters_support(self):
        """Test support for allowed special characters."""
        valid_emails = [
            "user.name@example.com",  # dot
            "user_name@example.com",  # underscore
            "user-name@example.com",  # hyphen
            "user+tag@example.com",   # plus
            "user.name+tag@example.com",  # combination
        ]

        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email))

    def test_unsupported_features(self):
        """Test that unsupported features are rejected."""
        unsupported_emails = [
            '"user name"@example.com',  # quoted strings
            'user@[192.168.1.1]',       # IP addresses
            'user(comment)@example.com', # comments
            'user@例え.テスト',           # Unicode/IDN
        ]

        for email in unsupported_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email))

    def test_get_validation_details(self):
        """Test the detailed validation function."""
        # Test valid email
        result = get_validation_details("user@example.com")
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['local_part'], 'user')
        self.assertEqual(result['domain_part'], 'example.com')

        # Test invalid email
        result = get_validation_details(".user@example.com")
        self.assertFalse(result['is_valid'])
        self.assertIn('Local part cannot start with dot', result['errors'])

        # Test None input
        result = get_validation_details(None)
        self.assertFalse(result['is_valid'])
        self.assertIn('Input must be a string', result['errors'])

    def test_boundary_conditions(self):
        """Test boundary conditions and edge cases."""
        # Minimum valid email
        self.assertTrue(validate_email("a@b.co"))

        # Maximum local part length (64 chars)
        max_local = "a" * 64
        self.assertTrue(validate_email(f"{max_local}@example.com"))

        # One character over limit
        over_local = "a" * 65
        self.assertFalse(validate_email(f"{over_local}@example.com"))

        # TLD boundary cases
        self.assertTrue(validate_email("user@example.ab"))  # 2 char TLD
        self.assertFalse(validate_email("user@example.a"))  # 1 char TLD

    def test_regex_patterns_compliance(self):
        """Test that the implementation follows the specified regex patterns."""
        # Test local part pattern compliance
        valid_local_patterns = [
            "user",
            "user.name",
            "user_name",
            "user-name",
            "user+tag",
            "123",
            "a1b2c3"
        ]

        for local in valid_local_patterns:
            with self.subTest(local=local):
                self.assertTrue(validate_email(f"{local}@example.com"))

        # Test domain label patterns
        valid_domains = [
            "example.com",
            "sub.domain.com",
            "a1b2.com",
            "test-domain.org"
        ]

        for domain in valid_domains:
            with self.subTest(domain=domain):
                self.assertTrue(validate_email(f"user@{domain}"))

    def test_performance_with_long_inputs(self):
        """Test performance with various input lengths."""
        # This test ensures the validator handles long inputs gracefully
        # without causing performance issues

        # Very long but valid structure
        long_local = "a" * 60  # Within limit
        long_domain = "b" * 60 + ".com"  # Within limit
        long_email = f"{long_local}@{long_domain}"

        # Should handle long valid emails
        result = validate_email(long_email)
        self.assertIsInstance(result, bool)

        # Should handle very long invalid emails gracefully
        very_long_invalid = "a" * 1000 + "@" + "b" * 1000 + ".com"
        result = validate_email(very_long_invalid)
        self.assertFalse(result)


class TestEmailValidatorIntegration(unittest.TestCase):
    """Integration tests for the email validator."""

    def test_real_world_email_examples(self):
        """Test with real-world email examples."""
        real_world_valid = [
            "test@gmail.com",
            "user.name@company.co.uk",
            "support+tickets@example.org",
            "admin@sub.domain.com",
            "noreply@example.io",
        ]

        for email in real_world_valid:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email))

        real_world_invalid = [
            "plainaddress",
            "@missingdomain.com",
            "missing-at-sign.com",
            "missing.domain@.com",
            "spaces in@email.com",
        ]

        for email in real_world_invalid:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email))

    def test_specification_compliance(self):
        """Test that all specification requirements are met."""
        # This test verifies key specification points

        # 1. Exactly one @ symbol requirement
        self.assertFalse(validate_email("user@@example.com"))
        self.assertFalse(validate_email("userexample.com"))
        self.assertTrue(validate_email("user@example.com"))

        # 2. Length limits (RFC 5321)
        self.assertFalse(validate_email("a" * 255 + "@b.co"))  # > 254 total
        self.assertFalse(validate_email("a" * 65 + "@example.com"))  # > 64 local

        # 3. Case insensitivity
        self.assertTrue(validate_email("User@Example.COM"))

        # 4. Required domain structure
        self.assertFalse(validate_email("user@example"))  # No TLD
        self.assertTrue(validate_email("user@example.com"))  # Has TLD

        # 5. TLD requirements
        self.assertFalse(validate_email("user@example.1"))  # Numeric TLD
        self.assertFalse(validate_email("user@example.c"))  # Too short TLD
        self.assertTrue(validate_email("user@example.co"))  # Valid TLD


if __name__ == "__main__":
    # Run the test suite
    unittest.main(verbosity=2)