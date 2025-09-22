"""
Test suite for email validator with comprehensive test validation.

This module follows Test-Driven Development with rigorous test validation.
Each test is designed to catch specific validation errors and prove the
validator implementation is correct.
"""

import unittest
from email_validator import is_valid_email


class TestBasicEmailStructure(unittest.TestCase):
    """
    Test basic email structure validation.

    These tests verify the most fundamental requirement: emails must contain
    exactly one @ symbol with non-empty parts before and after it.
    """

    def test_valid_basic_email_structure(self):
        """
        Test that emails with exactly one @ and non-empty parts are valid.

        This test verifies:
        - Presence of exactly one @ symbol
        - Non-empty local part (before @)
        - Non-empty domain part (after @)

        If this test passes with an incorrect validator, it could mean:
        - Validator accepts multiple @ symbols
        - Validator accepts empty local or domain parts
        - Validator has other structural flaws
        """
        # Simple valid emails with basic structure
        valid_emails = [
            "user@domain.com",
            "a@b.co",
            "test@example.org",
            "simple@site.net"
        ]

        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(
                    is_valid_email(email),
                    f"Valid email '{email}' should be accepted"
                )

    def test_no_at_symbol_invalid(self):
        """
        Test that emails without @ symbol are invalid.

        This test verifies:
        - Emails must contain at least one @ symbol
        - Simple string validation catches missing @

        If this test fails, the validator might:
        - Not check for @ symbol presence
        - Have incorrect parsing logic
        """
        invalid_emails = [
            "userdomain.com",
            "plaintext",
            "no.at.symbol.here",
            "user.domain.com"
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    is_valid_email(email),
                    f"Email without @ symbol '{email}' should be rejected"
                )

    def test_multiple_at_symbols_invalid(self):
        """
        Test that emails with multiple @ symbols are invalid.

        This test verifies:
        - Emails must contain exactly one @ symbol
        - Multiple @ symbols are rejected

        If this test fails, the validator might:
        - Only check for @ presence, not uniqueness
        - Have incorrect splitting logic
        - Accept malformed email structures
        """
        invalid_emails = [
            "user@@domain.com",
            "user@domain@com",
            "user@sub@domain.com",
            "@@",
            "@user@domain.com"
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    is_valid_email(email),
                    f"Email with multiple @ symbols '{email}' should be rejected"
                )

    def test_empty_local_part_invalid(self):
        """
        Test that emails with empty local part (before @) are invalid.

        This test verifies:
        - Local part must be non-empty
        - @ at start of string is rejected

        If this test fails, the validator might:
        - Not validate local part presence
        - Have incorrect splitting logic
        """
        invalid_emails = [
            "@domain.com",
            "@example.org",
            "@site.net"
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    is_valid_email(email),
                    f"Email with empty local part '{email}' should be rejected"
                )

    def test_empty_domain_part_invalid(self):
        """
        Test that emails with empty domain part (after @) are invalid.

        This test verifies:
        - Domain part must be non-empty
        - @ at end of string is rejected

        If this test fails, the validator might:
        - Not validate domain part presence
        - Have incorrect splitting logic
        """
        invalid_emails = [
            "user@",
            "example@",
            "test@"
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    is_valid_email(email),
                    f"Email with empty domain part '{email}' should be rejected"
                )

    def test_only_at_symbol_invalid(self):
        """
        Test that a string containing only @ symbol is invalid.

        This test verifies:
        - Single @ character is not a valid email
        - Both local and domain parts are required

        If this test fails, the validator might:
        - Only check for @ presence
        - Not validate part lengths
        """
        self.assertFalse(
            is_valid_email("@"),
            "Single @ symbol should be rejected"
        )

    def test_empty_string_invalid(self):
        """
        Test that empty string is invalid.

        This test verifies:
        - Empty input is rejected
        - Validator handles edge case gracefully

        If this test fails, the validator might:
        - Not handle empty input
        - Have missing input validation
        """
        self.assertFalse(
            is_valid_email(""),
            "Empty string should be rejected"
        )


class TestLengthLimitsAndPerformance(unittest.TestCase):
    """
    Test length limits and performance characteristics.

    These tests verify the validator handles length constraints
    correctly and performs efficiently on various inputs.
    """

    def test_maximum_email_length(self):
        """
        Test that emails at or exceeding maximum length are handled correctly.

        This test verifies:
        - Emails up to 254 characters are accepted if otherwise valid
        - Emails over 254 characters are rejected
        - Length limits are enforced correctly

        If this test fails, the validator might:
        - Not enforce total length limits
        - Have incorrect length calculations
        """
        # Create a valid email at exactly 254 characters
        # Format: "a"*50 + "@" + "b"*48 + "." + "c"*154
        # Total: 50 + 1 + 48 + 1 + 154 = 254 characters
        local_part = "a" * 50
        domain_part = "b" * 48 + "." + "c" * 154
        valid_max_email = local_part + "@" + domain_part

        self.assertEqual(len(valid_max_email), 254)
        self.assertTrue(
            is_valid_email(valid_max_email),
            "Valid email at 254 characters should be accepted"
        )

        # Create an email that's too long (255 characters)
        invalid_long_email = "a" * 51 + "@" + "b" * 48 + "." + "c" * 154
        self.assertEqual(len(invalid_long_email), 255)
        self.assertFalse(
            is_valid_email(invalid_long_email),
            "Email over 254 characters should be rejected"
        )

    def test_local_part_length_limits(self):
        """
        Test that local part length limits are enforced.

        This test verifies:
        - Local parts up to 64 characters are accepted
        - Local parts over 64 characters are rejected

        If this test fails, the validator might:
        - Not enforce local part length limits
        - Have incorrect local part length calculations
        """
        # Valid local part at exactly 64 characters
        valid_local = "a" * 64
        valid_email = valid_local + "@example.com"
        self.assertTrue(
            is_valid_email(valid_email),
            "Email with 64-character local part should be accepted"
        )

        # Invalid local part at 65 characters
        invalid_local = "a" * 65
        invalid_email = invalid_local + "@example.com"
        self.assertFalse(
            is_valid_email(invalid_email),
            "Email with 65-character local part should be rejected"
        )

    def test_domain_part_length_limits(self):
        """
        Test that domain part length limits are enforced.

        This test verifies:
        - Very long domain parts are rejected
        - Domain length limit validation works

        If this test fails, the validator might:
        - Not enforce domain part length limits
        - Have incorrect domain part length calculations
        """
        # Test that a domain over 253 characters is rejected
        # Use a short local part to avoid total email length issues
        long_domain = "a" * 254 + ".co"  # 257 characters total
        invalid_email = "a@" + long_domain
        self.assertFalse(
            is_valid_email(invalid_email),
            "Email with overly long domain should be rejected"
        )

        # Test that a reasonably long domain is accepted
        reasonable_domain = "example.com"
        valid_email = "a@" + reasonable_domain
        self.assertTrue(
            is_valid_email(valid_email),
            "Email with reasonable domain should be accepted"
        )

    def test_minimum_length_requirements(self):
        """
        Test minimum length requirements.

        This test verifies:
        - Very short but valid emails work
        - Minimum viable email format is accepted

        If this test fails, the validator might:
        - Be too restrictive on short emails
        - Not handle minimal valid formats
        """
        minimal_emails = [
            "a@b.co",    # 6 characters total
            "1@2.co",    # numbers
            "x@y.co",    # minimal letters
        ]

        for email in minimal_emails:
            with self.subTest(email=email):
                self.assertTrue(
                    is_valid_email(email),
                    f"Minimal valid email '{email}' should be accepted"
                )

    def test_performance_with_long_inputs(self):
        """
        Test that validator performs efficiently with long inputs.

        This test verifies:
        - Very long invalid inputs fail quickly
        - No catastrophic backtracking in regex
        - Reasonable performance characteristics

        If this test fails, the validator might:
        - Have inefficient algorithms
        - Use problematic regex patterns
        - Not fail fast on obviously invalid inputs
        """
        import time

        # Test very long string without @
        long_no_at = "a" * 10000
        start_time = time.time()
        result = is_valid_email(long_no_at)
        elapsed = time.time() - start_time

        self.assertFalse(result, "Long string without @ should be invalid")
        self.assertLess(elapsed, 0.1, "Should reject long invalid string quickly")

        # Test very long string with invalid characters
        long_invalid_chars = "a" * 5000 + "@" + "b" * 5000
        start_time = time.time()
        result = is_valid_email(long_invalid_chars)
        elapsed = time.time() - start_time

        self.assertFalse(result, "Overly long email should be invalid")
        self.assertLess(elapsed, 0.1, "Should reject overly long email quickly")

        # Test string with many special characters
        special_chars = "a<>b[]c{}d" * 1000 + "@example.com"
        start_time = time.time()
        result = is_valid_email(special_chars)
        elapsed = time.time() - start_time

        self.assertFalse(result, "Email with special characters should be invalid")
        self.assertLess(elapsed, 0.1, "Should reject special characters quickly")


class TestEdgeCasesAndUnicode(unittest.TestCase):
    """
    Test edge cases, unicode handling, and boundary conditions.

    These tests verify the validator handles unusual inputs correctly
    and follows the specification for unicode rejection.
    """

    def test_whitespace_handling(self):
        """
        Test that emails with whitespace are handled correctly.

        This test verifies:
        - Leading/trailing whitespace is stripped and email validated
        - Internal whitespace in local or domain parts is rejected
        - Whitespace-only strings are rejected

        If this test fails, the validator might:
        - Not strip whitespace properly
        - Allow internal whitespace incorrectly
        - Not handle whitespace-only inputs
        """
        # Valid emails with leading/trailing whitespace (should be stripped)
        valid_emails_with_whitespace = [
            " user@example.com ",
            "\tuser@example.com\t",
            "\nuser@example.com\n",
            "  user@example.com  ",
        ]

        for email in valid_emails_with_whitespace:
            with self.subTest(email=repr(email)):
                self.assertTrue(
                    is_valid_email(email),
                    f"Email with whitespace '{repr(email)}' should be accepted after stripping"
                )

        # Invalid emails with internal whitespace (should be rejected)
        invalid_emails_with_whitespace = [
            "user @example.com",          # space after local part
            "user@ example.com",          # space before domain
            "user @ example.com",         # spaces around @
            "us er@example.com",          # space in local part
            "user@exam ple.com",          # space in domain
            " ",                          # space only
            "\t",                         # tab only
            "\n",                         # newline only
            "   ",                        # multiple spaces only
        ]

        for email in invalid_emails_with_whitespace:
            with self.subTest(email=repr(email)):
                self.assertFalse(
                    is_valid_email(email),
                    f"Email with internal/only whitespace '{repr(email)}' should be rejected"
                )

    def test_unicode_characters_rejected(self):
        """
        Test that unicode characters are rejected.

        This test verifies:
        - Non-ASCII characters in local part are rejected
        - Non-ASCII characters in domain part are rejected
        - Common unicode characters are properly handled

        If this test fails, the validator might:
        - Allow unicode characters (against specification)
        - Not properly validate character encoding
        """
        invalid_unicode_emails = [
            "üser@example.com",           # umlaut in local part
            "user@münchen.de",            # umlaut in domain
            "tëst@example.com",           # accented e in local part
            "user@tëst.com",              # accented e in domain
            "用户@example.com",            # Chinese characters in local part
            "user@例え.com",               # Japanese characters in domain
            "пользователь@example.com",   # Cyrillic in local part
            "user@пример.рф",             # Cyrillic in domain
            "user@café.com",              # accented characters in domain
            "café@example.com",           # accented characters in local part
            "user@résumé.com",            # multiple accents in domain
            "🙂@example.com",             # emoji in local part
            "user@🙂.com",                # emoji in domain
        ]

        for email in invalid_unicode_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    is_valid_email(email),
                    f"Email with unicode characters '{email}' should be rejected"
                )

    def test_case_sensitivity_handling(self):
        """
        Test that case sensitivity is handled correctly.

        This test verifies:
        - Domain names are case-insensitive (per RFC)
        - Local parts preserve case (but validation should be case-insensitive for characters)
        - Mixed case emails are valid

        If this test fails, the validator might:
        - Be case-sensitive when it shouldn't be
        - Not handle mixed case properly
        """
        valid_mixed_case_emails = [
            "User@Example.Com",
            "USER@EXAMPLE.COM",
            "user@EXAMPLE.com",
            "User@example.COM",
            "TeSt@ExAmPlE.cOm",
            "A@B.Co",
            "test123@SUB.EXAMPLE.ORG",
        ]

        for email in valid_mixed_case_emails:
            with self.subTest(email=email):
                self.assertTrue(
                    is_valid_email(email),
                    f"Mixed case email '{email}' should be accepted"
                )

    def test_boundary_conditions(self):
        """
        Test boundary conditions and extreme cases.

        This test verifies:
        - Single character parts work where valid
        - Very short but valid emails work
        - Edge cases around dots and hyphens

        If this test fails, the validator might:
        - Be too restrictive on short inputs
        - Not handle boundary cases correctly
        """
        valid_boundary_emails = [
            "a@b.co",                     # minimal valid email
            "1@2.co",                     # numbers only
            "a@x.y",                      # single char labels
            "test@a.b",                   # minimal domain
            "a.b@c.de",                   # dots in local part
            "a-b@c-d.ef",                 # hyphens
        ]

        for email in valid_boundary_emails:
            with self.subTest(email=email):
                self.assertTrue(
                    is_valid_email(email),
                    f"Boundary case email '{email}' should be accepted"
                )

        invalid_boundary_emails = [
            "@",                          # only @
            "a@",                         # missing domain
            "@b.co",                      # missing local part
            "a@b",                        # missing TLD
            "",                           # empty string
            "a@b.",                       # trailing dot
            ".a@b.co",                    # leading dot in local
            "a.@b.co",                    # trailing dot in local
            "a@.b.co",                    # leading dot in domain
            "a@b.co.",                    # trailing dot in domain
        ]

        for email in invalid_boundary_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    is_valid_email(email),
                    f"Invalid boundary case '{email}' should be rejected"
                )


class TestDomainPartValidation(unittest.TestCase):
    """
    Test domain part (after @) validation rules.

    These tests verify domain structure, character restrictions,
    and formatting rules for the domain part of email addresses.
    """

    def test_valid_domain_formats(self):
        """
        Test that domains with valid formats are accepted.

        This test verifies:
        - Basic domain.tld format works
        - Subdomains are allowed
        - Multiple subdomain levels work
        - Hyphens in domain names are allowed
        - Numbers in domains are allowed
        - Short and long domains work

        If this test fails, the validator might:
        - Be too restrictive on domain formats
        - Not handle subdomains correctly
        - Have incorrect domain validation logic
        """
        valid_emails = [
            "user@example.com",          # basic domain
            "user@sub.example.com",      # subdomain
            "user@deep.sub.example.org", # multiple subdomains
            "user@test-site.com",        # hyphen in domain
            "user@example123.net",       # numbers in domain
            "user@x.co",                 # short domain
            "user@very-long-domain.example.org",  # long domain
            "user@a.b",                  # minimal valid domain
            "user@test.co.uk",           # country code TLD
            "user@site-name.example.com" # hyphens with subdomain
        ]

        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(
                    is_valid_email(email),
                    f"Email with valid domain '{email}' should be accepted"
                )

    def test_invalid_domain_missing_dot(self):
        """
        Test that domains without dots are invalid.

        This test verifies:
        - Domains must contain at least one dot
        - Single-word domains are rejected
        - TLD requirement is enforced

        If this test fails, the validator might:
        - Not require dots in domains
        - Allow malformed domain structures
        """
        invalid_emails = [
            "user@localhost",
            "user@domain",
            "user@test",
            "user@singleword",
            "user@example",
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    is_valid_email(email),
                    f"Email with dotless domain '{email}' should be rejected"
                )

    def test_invalid_domain_dot_placement(self):
        """
        Test that domains with invalid dot placement are rejected.

        This test verifies:
        - Domains cannot start with dots
        - Domains cannot end with dots
        - Consecutive dots are not allowed

        If this test fails, the validator might:
        - Not validate domain dot placement
        - Allow malformed domain structures
        """
        invalid_emails = [
            "user@.example.com",         # dot at start
            "user@example.com.",         # dot at end
            "user@example..com",         # consecutive dots
            "user@.example.com.",        # dots at both ends
            "user@sub..example.com",     # consecutive dots in middle
            "user@...example.com",       # multiple dots at start
            "user@example.com...",       # multiple dots at end
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    is_valid_email(email),
                    f"Email with invalid domain dot placement '{email}' should be rejected"
                )

    def test_invalid_domain_characters(self):
        """
        Test that domains with invalid characters are rejected.

        This test verifies:
        - Spaces are not allowed in domains
        - Special characters (except hyphens) are not allowed
        - Underscores are not allowed in domains (different from local part)

        If this test fails, the validator might:
        - Be too permissive with domain characters
        - Not properly restrict domain character set
        """
        invalid_emails = [
            "user@exam ple.com",         # space
            "user@example_.com",         # underscore (not allowed in domains)
            "user@exam<>ple.com",        # angle brackets
            "user@exam[]ple.com",        # square brackets
            "user@exam()ple.com",        # parentheses
            "user@exam{}ple.com",        # curly braces
            "user@exam,ple.com",         # comma
            "user@exam;ple.com",         # semicolon
            "user@exam:ple.com",         # colon
            "user@exam\"ple.com",        # quote
            "user@exam'ple.com",         # apostrophe
            "user@exam\\ple.com",        # backslash
            "user@exam/ple.com",         # forward slash
            "user@exam*ple.com",         # asterisk
            "user@exam?ple.com",         # question mark
            "user@exam!ple.com",         # exclamation
            "user@exam%ple.com",         # percent
            "user@exam&ple.com",         # ampersand
            "user@exam=ple.com",         # equals
            "user@exam|ple.com",         # pipe
            "user@exam~ple.com",         # tilde
            "user@exam`ple.com",         # backtick
            "user@exam^ple.com",         # caret
            "user@exam$ple.com",         # dollar sign
            "user@exam#ple.com",         # hash
            "user@exam+ple.com",         # plus (not allowed in domains)
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    is_valid_email(email),
                    f"Email with invalid domain character '{email}' should be rejected"
                )

    def test_invalid_domain_hyphen_placement(self):
        """
        Test that domains with invalid hyphen placement are rejected.

        This test verifies:
        - Domain labels cannot start with hyphens
        - Domain labels cannot end with hyphens
        - Only internal hyphens are allowed

        If this test fails, the validator might:
        - Not validate hyphen placement in domains
        - Allow malformed domain labels
        """
        invalid_emails = [
            "user@-example.com",         # starts with hyphen
            "user@example-.com",         # ends with hyphen
            "user@sub.-example.com",     # subdomain starts with hyphen
            "user@sub-.example.com",     # subdomain ends with hyphen
            "user@example.-com",         # TLD starts with hyphen
            "user@example.com-",         # TLD ends with hyphen
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    is_valid_email(email),
                    f"Email with invalid domain hyphen placement '{email}' should be rejected"
                )

    def test_empty_domain_part_already_covered(self):
        """
        Note: Empty domain part testing is already covered in TestBasicEmailStructure.
        This test documents that we don't need to duplicate that testing here.
        """
        pass


class TestLocalPartValidation(unittest.TestCase):
    """
    Test local part (before @) validation rules.

    These tests verify character restrictions and formatting rules
    for the local part of email addresses.
    """

    def test_valid_local_part_characters(self):
        """
        Test that local parts with valid characters are accepted.

        This test verifies:
        - Letters (a-z, A-Z) are allowed
        - Numbers (0-9) are allowed
        - Dots (.) are allowed in middle
        - Underscores (_) are allowed
        - Hyphens (-) are allowed
        - Plus signs (+) are allowed

        If this test fails, the validator might:
        - Be too restrictive on allowed characters
        - Have incorrect character validation logic
        """
        valid_emails = [
            "user@domain.com",           # letters
            "USER@domain.com",           # uppercase letters
            "user123@domain.com",        # numbers
            "user.name@domain.com",      # dots in middle
            "user_name@domain.com",      # underscores
            "user-name@domain.com",      # hyphens
            "user+tag@domain.com",       # plus signs
            "a@domain.com",              # single character
            "user.123@domain.com",       # mixed valid chars
            "test_user-123+tag@domain.com"  # all valid chars
        ]

        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(
                    is_valid_email(email),
                    f"Email with valid local part '{email}' should be accepted"
                )

    def test_invalid_local_part_dot_placement(self):
        """
        Test that local parts with invalid dot placement are rejected.

        This test verifies:
        - Dots cannot be at the start of local part
        - Dots cannot be at the end of local part
        - Consecutive dots are not allowed

        If this test fails, the validator might:
        - Not validate dot placement rules
        - Allow malformed local parts
        """
        invalid_emails = [
            ".user@domain.com",          # dot at start
            "user.@domain.com",          # dot at end
            "user..name@domain.com",     # consecutive dots
            "..user@domain.com",         # multiple dots at start
            "user..@domain.com",         # consecutive dots at end
            ".user.@domain.com",         # dots at both ends
            "user...name@domain.com",    # three consecutive dots
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    is_valid_email(email),
                    f"Email with invalid dot placement '{email}' should be rejected"
                )

    def test_invalid_local_part_characters(self):
        """
        Test that local parts with invalid characters are rejected.

        This test verifies:
        - Spaces are not allowed
        - Special characters like <, >, [, ], etc. are not allowed
        - Control characters are not allowed

        If this test fails, the validator might:
        - Be too permissive with character validation
        - Not properly restrict character set
        """
        invalid_emails = [
            "user name@domain.com",      # space
            "user<>@domain.com",         # angle brackets
            "user[]@domain.com",         # square brackets
            "user()@domain.com",         # parentheses
            "user{}@domain.com",         # curly braces
            "user,@domain.com",          # comma
            "user;@domain.com",          # semicolon
            "user:@domain.com",          # colon
            "user\"@domain.com",         # quote
            "user'@domain.com",          # apostrophe
            "user\\@domain.com",         # backslash
            "user/@domain.com",          # forward slash
            "user*@domain.com",          # asterisk
            "user?@domain.com",          # question mark
            "user!@domain.com",          # exclamation
            "user%@domain.com",          # percent
            "user&@domain.com",          # ampersand
            "user=@domain.com",          # equals
            "user|@domain.com",          # pipe
            "user~@domain.com",          # tilde
            "user`@domain.com",          # backtick
            "user^@domain.com",          # caret
            "user$@domain.com",          # dollar sign
            "user#@domain.com",          # hash
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    is_valid_email(email),
                    f"Email with invalid character in local part '{email}' should be rejected"
                )

    def test_empty_local_part_already_covered(self):
        """
        Note: Empty local part testing is already covered in TestBasicEmailStructure.
        This test documents that we don't need to duplicate that testing here.
        """
        pass


if __name__ == "__main__":
    unittest.main()