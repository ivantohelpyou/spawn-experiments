"""
Test suite for email validator function.
Following TDD principles: Red-Green-Refactor
"""

import unittest
from email_validator import is_valid_email


class TestEmailValidator(unittest.TestCase):
    """Test cases for email validation function."""

    def test_basic_valid_email(self):
        """Test basic valid email format."""
        self.assertTrue(is_valid_email("user@domain.com"))

    def test_valid_email_with_numbers(self):
        """Test valid email with numbers."""
        self.assertTrue(is_valid_email("user123@domain.com"))

    def test_valid_email_with_dot_in_local(self):
        """Test valid email with dot in local part."""
        self.assertTrue(is_valid_email("first.last@domain.com"))

    # Invalid email tests
    def test_empty_string(self):
        """Test empty string is invalid."""
        self.assertFalse(is_valid_email(""))

    def test_none_input(self):
        """Test None input is invalid."""
        self.assertFalse(is_valid_email(None))

    def test_missing_at_symbol(self):
        """Test email without @ symbol is invalid."""
        self.assertFalse(is_valid_email("userdomaincom"))

    def test_multiple_at_symbols(self):
        """Test email with multiple @ symbols is invalid."""
        self.assertFalse(is_valid_email("user@domain@com"))

    def test_missing_local_part(self):
        """Test email without local part is invalid."""
        self.assertFalse(is_valid_email("@domain.com"))

    def test_missing_domain_part(self):
        """Test email without domain part is invalid."""
        self.assertFalse(is_valid_email("user@"))

    def test_domain_without_dot(self):
        """Test domain without dot is invalid."""
        self.assertFalse(is_valid_email("user@domain"))

    def test_domain_starting_with_dot(self):
        """Test domain starting with dot is invalid."""
        self.assertFalse(is_valid_email("user@.domain.com"))

    def test_domain_ending_with_dot(self):
        """Test domain ending with dot is invalid."""
        self.assertFalse(is_valid_email("user@domain.com."))

    def test_consecutive_dots_in_domain(self):
        """Test consecutive dots in domain is invalid."""
        self.assertFalse(is_valid_email("user@domain..com"))

    def test_local_part_starting_with_dot(self):
        """Test local part starting with dot is invalid."""
        self.assertFalse(is_valid_email(".user@domain.com"))

    def test_local_part_ending_with_dot(self):
        """Test local part ending with dot is invalid."""
        self.assertFalse(is_valid_email("user.@domain.com"))

    def test_consecutive_dots_in_local_part(self):
        """Test consecutive dots in local part is invalid."""
        self.assertFalse(is_valid_email("user..name@domain.com"))

    # Edge cases and special characters
    def test_valid_email_with_plus(self):
        """Test valid email with plus sign."""
        self.assertTrue(is_valid_email("user+tag@domain.com"))

    def test_valid_email_with_hyphen_in_domain(self):
        """Test valid email with hyphen in domain."""
        self.assertTrue(is_valid_email("user@my-domain.com"))

    def test_valid_email_with_underscore(self):
        """Test valid email with underscore."""
        self.assertTrue(is_valid_email("user_name@domain.com"))

    def test_invalid_space_in_local_part(self):
        """Test space in local part is invalid."""
        self.assertFalse(is_valid_email("user name@domain.com"))

    def test_invalid_space_in_domain(self):
        """Test space in domain is invalid."""
        self.assertFalse(is_valid_email("user@domain .com"))

    def test_minimum_valid_email(self):
        """Test shortest possible valid email."""
        self.assertTrue(is_valid_email("a@b.c"))

    def test_long_local_part_invalid(self):
        """Test local part exceeding 64 characters is invalid."""
        long_local = "a" * 65
        self.assertFalse(is_valid_email(f"{long_local}@domain.com"))

    def test_long_domain_invalid(self):
        """Test domain exceeding 253 characters is invalid."""
        long_domain = "a" * 250 + ".com"  # 254 characters total
        self.assertFalse(is_valid_email(f"user@{long_domain}"))

    def test_total_length_invalid(self):
        """Test total email exceeding 320 characters is invalid."""
        long_local = "a" * 64
        long_domain = "b" * 252 + ".com"  # 64 + 1 + 256 = 321 characters
        self.assertFalse(is_valid_email(f"{long_local}@{long_domain}"))

    def test_domain_without_tld(self):
        """Test domain without proper TLD structure."""
        self.assertFalse(is_valid_email("user@domain."))

    def test_non_string_input(self):
        """Test non-string input is invalid."""
        self.assertFalse(is_valid_email(123))
        self.assertFalse(is_valid_email(['user@domain.com']))


if __name__ == "__main__":
    unittest.main()