"""
Test suite for email validator - Test-First Development approach
Following TDD methodology: RED-GREEN-REFACTOR cycles
"""

import unittest
from email_validator import validate_email


class TestEmailValidator(unittest.TestCase):
    """Comprehensive test suite for email validation following TDD principles"""

    def test_basic_valid_emails(self):
        """Test basic valid email formats"""
        valid_emails = [
            "test@example.com",
            "user@domain.org",
            "admin@site.net",
            "contact@company.co.uk",
            "info@subdomain.example.com"
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Should be valid: {email}")

    def test_local_part_character_validation(self):
        """Test allowed characters in local part"""
        valid_emails = [
            "abc123@example.com",  # alphanumeric
            "user.name@example.com",  # dots
            "user_name@example.com",  # underscores
            "user-name@example.com",  # hyphens
            "user+tag@example.com",  # plus signs
            "a@example.com",  # single character
            "test123.user_name-tag+extra@example.com"  # combination
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Should be valid: {email}")

    def test_local_part_dot_rules(self):
        """Test dot placement rules in local part"""
        # Valid dot usage
        valid_emails = [
            "user.name@example.com",
            "first.last@example.com",
            "a.b.c@example.com"
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Should be valid: {email}")

        # Invalid dot usage
        invalid_emails = [
            ".user@example.com",  # starts with dot
            "user.@example.com",  # ends with dot
            "user..name@example.com",  # consecutive dots
            "us..er@example.com",  # consecutive dots middle
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email), f"Should be invalid: {email}")

    def test_local_part_hyphen_rules(self):
        """Test hyphen placement rules in local part"""
        # Valid hyphen usage
        valid_emails = [
            "user-name@example.com",
            "test-123@example.com",
            "a-b-c@example.com"
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Should be valid: {email}")

        # Invalid hyphen usage (start/end)
        invalid_emails = [
            "-user@example.com",  # starts with hyphen
            "user-@example.com",  # ends with hyphen
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email), f"Should be invalid: {email}")

    def test_local_part_length_limits(self):
        """Test local part length constraints"""
        # Valid length (64 characters exactly)
        local_64 = "a" * 64
        self.assertTrue(validate_email(f"{local_64}@example.com"))

        # Invalid length (65 characters)
        local_65 = "a" * 65
        self.assertFalse(validate_email(f"{local_65}@example.com"))

        # Empty local part
        self.assertFalse(validate_email("@example.com"))

    def test_at_symbol_validation(self):
        """Test @ symbol requirements"""
        # No @ symbol
        self.assertFalse(validate_email("userexample.com"))

        # Multiple @ symbols
        self.assertFalse(validate_email("user@domain@example.com"))
        self.assertFalse(validate_email("user@@example.com"))

        # Valid single @ symbol
        self.assertTrue(validate_email("user@example.com"))

    def test_domain_part_basic_structure(self):
        """Test domain part basic requirements"""
        # Valid domains
        valid_emails = [
            "user@example.com",
            "user@subdomain.example.org",
            "user@a.bc",  # shortest valid domain
            "user@very-long-subdomain.example-domain.co.uk"
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Should be valid: {email}")

        # Invalid domains
        invalid_emails = [
            "user@",  # empty domain
            "user@domain",  # no TLD
            "user@.com",  # starts with dot
            "user@domain.",  # ends with dot
            "user@domain..com",  # consecutive dots
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email), f"Should be invalid: {email}")

    def test_domain_label_character_validation(self):
        """Test allowed characters in domain labels"""
        # Valid characters
        valid_emails = [
            "user@abc123.com",  # alphanumeric
            "user@test-domain.com",  # hyphen in middle
            "user@sub1.domain2.org",  # numbers
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Should be valid: {email}")

        # Invalid characters
        invalid_emails = [
            "user@domain-.com",  # hyphen at end
            "user@-domain.com",  # hyphen at start
            "user@dom_ain.com",  # underscore
            "user@domain+.com",  # plus sign
            "user@domain$.com",  # special character
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email), f"Should be invalid: {email}")

    def test_domain_label_length_limits(self):
        """Test domain label length constraints"""
        # Valid label length (63 characters)
        label_63 = "a" * 63
        self.assertTrue(validate_email(f"user@{label_63}.com"))

        # Invalid label length (64 characters)
        label_64 = "a" * 64
        self.assertFalse(validate_email(f"user@{label_64}.com"))

        # Empty label
        self.assertFalse(validate_email("user@.com"))

    def test_domain_part_length_limits(self):
        """Test overall domain part length constraints"""
        # Create domain close to 253 character limit
        # domain structure: label.label.label...tld
        label = "a" * 50  # 50 char labels
        domain_parts = [label] * 4 + ["com"]  # 4*50 + 3 dots + 3 = 206 chars
        domain = ".".join(domain_parts)
        self.assertTrue(validate_email(f"user@{domain}"))

        # Test close to 253 character limit (maximum allowed)
        # Create valid domain with multiple labels under 63 chars each
        label_63 = "a" * 63
        label_62 = "b" * 62
        label_61 = "c" * 61
        # 63 + 1 + 62 + 1 + 61 + 1 + 3 = 192 chars - within limits
        domain_192 = f"{label_63}.{label_62}.{label_61}.com"
        self.assertTrue(validate_email(f"user@{domain_192}"))

        # Test domain that would exceed 253 if it had a very long first label
        long_label = "x" * 63
        very_long_domain = ".".join([long_label] * 4) + ".com"  # 63*4 + 3 + 1 + 3 = 259 chars
        self.assertFalse(validate_email(f"user@{very_long_domain}"))

    def test_tld_validation(self):
        """Test Top Level Domain requirements"""
        # Valid TLDs
        valid_emails = [
            "user@example.co",  # 2 characters
            "user@example.com",  # 3 characters
            "user@example.info",  # 4 characters
            "user@example.museum",  # long TLD
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Should be valid: {email}")

        # Invalid TLDs
        invalid_emails = [
            "user@example.c",  # 1 character (too short)
            "user@example.c0m",  # contains number
            "user@example.c-m",  # contains hyphen
            "user@example.123",  # all numbers
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email), f"Should be invalid: {email}")

    def test_total_email_length_limits(self):
        """Test overall email length constraints (RFC 5321 limit)"""
        # Valid total length (254 characters exactly)
        local_part = "a" * 64  # 64 chars
        # Create valid domain part: need 189 chars total for 64+1+189=254
        # Use multiple labels to stay under 63-char label limit
        label1 = "b" * 63  # 63 chars
        label2 = "c" * 63  # 63 chars
        label3 = "d" * 59  # 59 chars
        # 63 + 1 + 63 + 1 + 59 + 1 + 3 = 191 (too long, need 189)
        # So: 63 + 1 + 63 + 1 + 57 + 1 + 3 = 189
        domain_part = f"{label1}.{label2}.{'d' * 57}.com"  # 189 chars total
        email_254 = f"{local_part}@{domain_part}"
        self.assertEqual(len(email_254), 254)
        self.assertTrue(validate_email(email_254))

        # Invalid total length (255 characters)
        domain_part_long = f"{label1}.{label2}.{'d' * 58}.com"  # 190 chars total
        email_255 = f"{local_part}@{domain_part_long}"
        self.assertEqual(len(email_255), 255)
        self.assertFalse(validate_email(email_255))

    def test_edge_cases(self):
        """Test various edge cases"""
        # Empty string
        self.assertFalse(validate_email(""))

        # Whitespace
        self.assertFalse(validate_email(" "))
        self.assertFalse(validate_email("user @example.com"))
        self.assertFalse(validate_email("user@ example.com"))
        self.assertFalse(validate_email(" user@example.com "))

        # Case sensitivity (should be allowed)
        self.assertTrue(validate_email("User@Example.COM"))
        self.assertTrue(validate_email("USER@EXAMPLE.COM"))
        self.assertTrue(validate_email("user@EXAMPLE.com"))

    def test_unsupported_features(self):
        """Test features explicitly NOT supported"""
        # Quoted strings
        self.assertFalse(validate_email('"test user"@example.com'))
        self.assertFalse(validate_email('"test.user"@example.com'))

        # IP addresses
        self.assertFalse(validate_email('user@192.168.1.1'))
        self.assertFalse(validate_email('user@[192.168.1.1]'))

        # Comments
        self.assertFalse(validate_email('user@example.com (comment)'))
        self.assertFalse(validate_email('(comment)user@example.com'))

        # Internationalized domains
        self.assertFalse(validate_email('user@café.com'))
        self.assertFalse(validate_email('user@例え.テスト'))

    def test_comprehensive_invalid_cases(self):
        """Additional comprehensive invalid cases"""
        invalid_emails = [
            # Various malformed cases
            "user",  # no @ or domain
            "@",  # only @
            "@example.com",  # no local part
            "user@",  # no domain
            ".user@example.com",  # local starts with dot
            "user.@example.com",  # local ends with dot
            "user..test@example.com",  # consecutive dots in local
            "user@-example.com",  # domain starts with hyphen
            "user@example-.com",  # domain ends with hyphen
            "user@example.c",  # TLD too short
            "user@example.123",  # TLD all numbers
            "user@.example.com",  # domain starts with dot
            "user@example.com.",  # domain ends with dot
            "user@example..com",  # consecutive dots in domain
            "user@@example.com",  # double @
            "user@ex@ample.com",  # @ in domain
            "user name@example.com",  # space in local
            "user@exa mple.com",  # space in domain
            "\tuser@example.com",  # tab character
            "user@example.com\n",  # newline
        ]

        for email in invalid_emails:
            with self.subTest(email=repr(email)):
                self.assertFalse(validate_email(email), f"Should be invalid: {repr(email)}")


if __name__ == "__main__":
    unittest.main()