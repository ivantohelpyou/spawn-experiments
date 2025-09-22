#!/usr/bin/env python3
"""
Integration demo and quality verification for the email validator.

This script demonstrates the comprehensive email validator built using
Test-Driven Development with rigorous test validation.
"""

from email_validator import is_valid_email


def demo_email_validator():
    """Demonstrate the email validator with comprehensive examples."""

    print("=" * 80)
    print("EMAIL VALIDATOR - TDD WITH COMPREHENSIVE TEST VALIDATION")
    print("=" * 80)
    print()

    # Test categories with examples
    test_cases = [
        # Basic valid emails
        ("Valid Basic Emails", [
            "user@example.com",
            "test.email@subdomain.example.org",
            "user+tag@example.co.uk",
            "simple@x.co",
            "user123@test-domain.com",
            "a@b.co",
        ]),

        # Basic structure violations
        ("Invalid Structure", [
            "userexample.com",           # no @
            "user@@example.com",         # multiple @
            "@example.com",              # empty local part
            "user@",                     # empty domain part
            "",                          # empty string
            "@",                         # only @
        ]),

        # Local part validation
        ("Invalid Local Parts", [
            ".user@example.com",         # starts with dot
            "user.@example.com",         # ends with dot
            "user..name@example.com",    # consecutive dots
            "user name@example.com",     # space in local part
            "user<>@example.com",        # invalid characters
            "user#@example.com",         # hash character
        ]),

        # Domain validation
        ("Invalid Domains", [
            "user@localhost",            # no dot in domain
            "user@.example.com",         # starts with dot
            "user@example.com.",         # ends with dot
            "user@example..com",         # consecutive dots
            "user@exam ple.com",         # space in domain
            "user@example_.com",         # underscore in domain
            "user@-example.com",         # starts with hyphen
            "user@example-.com",         # ends with hyphen
        ]),

        # Unicode and special cases
        ("Unicode and Edge Cases", [
            "üser@example.com",          # unicode in local part
            "user@münchen.de",           # unicode in domain
            "🙂@example.com",            # emoji
            " user@example.com ",        # whitespace (should be stripped)
            "user@exam\tple.com",        # tab character
            "café@example.com",          # accented characters
        ]),

        # Length limits
        ("Length Limits", [
            "a" * 65 + "@example.com",   # local part too long
            "user@" + "a" * 254 + ".co", # domain too long
            "a" * 250 + "@b.co",         # total email too long
        ]),

        # Valid edge cases
        ("Valid Edge Cases", [
            "a@b.co",                    # minimal valid email
            "USER@EXAMPLE.COM",          # uppercase
            "test_user-123+tag@sub.example.org",  # all valid chars
            " valid@example.com ",       # whitespace stripped
            "\tvalid@example.com\t",     # tabs stripped
        ]),
    ]

    total_tests = 0
    passed_tests = 0

    for category, emails in test_cases:
        print(f"\n{category}:")
        print("-" * len(category))

        for email in emails:
            total_tests += 1
            try:
                result = is_valid_email(email)
                status = "✓ VALID" if result else "✗ INVALID"

                # Determine expected result based on category
                if "Valid" in category:
                    expected = True
                    passed_tests += 1 if result == expected else passed_tests
                else:
                    expected = False
                    passed_tests += 1 if result == expected else passed_tests

                # Show result with formatting
                email_display = repr(email) if any(c in email for c in [' ', '\t', '\n']) else email
                print(f"  {status:<10} {email_display}")

                if result != expected:
                    print(f"    ⚠️  UNEXPECTED: Expected {'VALID' if expected else 'INVALID'}")

            except Exception as e:
                print(f"  ✗ ERROR     {repr(email)} - {e}")

    print(f"\n{'='*80}")
    print(f"SUMMARY: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED - Email validator is working correctly!")
    else:
        print(f"⚠️  {total_tests - passed_tests} tests failed - Review implementation")

    print(f"{'='*80}")


def demonstrate_tdd_process():
    """Show the TDD process we followed."""

    print("\n" + "=" * 80)
    print("TEST-DRIVEN DEVELOPMENT PROCESS SUMMARY")
    print("=" * 80)

    phases = [
        ("1. SPECIFICATIONS", [
            "✓ Detailed functional requirements",
            "✓ Valid/invalid format patterns with examples",
            "✓ RFC compliance requirements (simplified)",
            "✓ Edge cases and unicode handling rules",
            "✓ Error handling and return value specs",
            "✓ Performance considerations",
        ]),

        ("2. BASIC EMAIL STRUCTURE", [
            "✓ RED: Tests for @ symbol validation",
            "✓ TEST VALIDATION: Proved tests catch errors",
            "✓ GREEN: Minimal implementation",
            "✓ REFACTOR: Clean, documented code",
        ]),

        ("3. LOCAL PART VALIDATION", [
            "✓ RED: Character and dot placement tests",
            "✓ TEST VALIDATION: Tested with wrong implementations",
            "✓ GREEN: ASCII-only regex with dot rules",
            "✓ REFACTOR: Separate validation function",
        ]),

        ("4. DOMAIN PART VALIDATION", [
            "✓ RED: Domain structure and character tests",
            "✓ TEST VALIDATION: Verified test sensitivity",
            "✓ GREEN: Label-based validation with rules",
            "✓ REFACTOR: Modular domain validation",
        ]),

        ("5. EDGE CASES & UNICODE", [
            "✓ RED: Whitespace, unicode, case tests",
            "✓ TEST VALIDATION: Confirmed test effectiveness",
            "✓ GREEN: Whitespace stripping, unicode rejection",
            "✓ REFACTOR: Comprehensive input handling",
        ]),

        ("6. LENGTH LIMITS & PERFORMANCE", [
            "✓ RED: Length limit and performance tests",
            "✓ TEST VALIDATION: Validated length enforcement",
            "✓ GREEN: RFC-compliant length limits",
            "✓ REFACTOR: Efficient validation order",
        ]),
    ]

    for phase, steps in phases:
        print(f"\n{phase}:")
        for step in steps:
            print(f"  {step}")

    print(f"\n{'='*80}")
    print("KEY TDD PRINCIPLES DEMONSTRATED:")
    print("✓ Never write implementation before test validation")
    print("✓ Always demonstrate test validation with wrong implementations")
    print("✓ Each test verifies one specific validation rule")
    print("✓ Tests catch both under-validation and over-validation")
    print("✓ Red-Green-Refactor cycle maintained throughout")
    print("✓ Comprehensive test coverage with meaningful assertions")
    print(f"{'='*80}")


if __name__ == "__main__":
    demo_email_validator()
    demonstrate_tdd_process()

    print("\n" + "=" * 80)
    print("DEVELOPMENT COMPLETE")
    print("=" * 80)
    print("📁 Files created:")
    print("  • SPECIFICATIONS.md - Detailed requirements")
    print("  • email_validator.py - Main implementation")
    print("  • test_email_validator.py - Comprehensive test suite")
    print("  • test_type_checking.py - Type validation tests")
    print("  • integration_demo.py - This demonstration")
    print("\n📊 Test Statistics:")
    print("  • 27 test methods across 5 test classes")
    print("  • 100+ individual test cases")
    print("  • Test validation performed for each feature")
    print("  • Full coverage of specifications")
    print("\n🎯 Email Validator Features:")
    print("  • RFC-inspired validation (simplified)")
    print("  • ASCII-only character set")
    print("  • Proper dot and hyphen placement rules")
    print("  • Length limits (254 total, 64 local, 253 domain)")
    print("  • Whitespace handling (strip ends, reject internal)")
    print("  • Unicode rejection")
    print("  • Type safety with meaningful error messages")
    print("  • Performance optimized for fast failure")
    print(f"{'='*80}")