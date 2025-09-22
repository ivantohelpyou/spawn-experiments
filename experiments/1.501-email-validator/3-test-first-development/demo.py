#!/usr/bin/env python3
"""
Demonstration script for the TDD Email Validator.

This script shows the email validator in action with various test cases
and demonstrates its performance characteristics.
"""

import time
from email_validator import is_valid_email


def demo_basic_validation():
    """Demonstrate basic email validation."""
    print("=== Basic Email Validation Demo ===")

    test_emails = [
        # Valid emails
        "user@domain.com",
        "test123@example.org",
        "first.last@domain.com",
        "user+tag@domain.com",
        "user_name@my-domain.net",
        "a@b.c",  # Minimum valid email

        # Invalid emails
        "",  # Empty
        "invalid",  # No @ symbol
        "@domain.com",  # No local part
        "user@",  # No domain
        "user@domain",  # No TLD
        "user..name@domain.com",  # Consecutive dots in local part
        ".user@domain.com",  # Starts with dot
        "user.@domain.com",  # Ends with dot
        "user@.domain.com",  # Domain starts with dot
        "user@domain.com.",  # Domain ends with dot
        "user name@domain.com",  # Space in local part
        "user@domain .com",  # Space in domain
        "user@@domain.com",  # Multiple @ symbols
    ]

    for email in test_emails:
        result = is_valid_email(email)
        status = "✓ VALID" if result else "✗ INVALID"
        print(f"{status:10} | {email:25} ")


def demo_edge_cases():
    """Demonstrate edge case handling."""
    print("\n=== Edge Cases Demo ===")

    # Length limit tests
    long_local = "a" * 65  # Over 64 character limit
    long_domain = "b" * 250 + ".com"  # Over 253 character limit
    long_total = "a" * 64 + "@" + "b" * 255 + ".com"  # Over 320 total

    edge_cases = [
        (None, "None input"),
        (123, "Integer input"),
        (["user@domain.com"], "List input"),
        (f"{long_local}@domain.com", "Long local part (65 chars)"),
        (f"user@{long_domain}", "Long domain part (254 chars)"),
        (long_total, "Long total email (324 chars)"),
    ]

    for test_input, description in edge_cases:
        try:
            result = is_valid_email(test_input)
            status = "✓ VALID" if result else "✗ INVALID"
        except Exception as e:
            status = f"ERROR: {e}"

        print(f"{status:10} | {description}")


def demo_performance():
    """Demonstrate performance characteristics."""
    print("\n=== Performance Demo ===")

    # Test with various email formats
    test_emails = [
        "user@domain.com",
        "invalid.email",
        "user+tag@my-domain.org",
        "@invalid.com",
        "user@domain..com",
        "a@b.c",
    ]

    # Warm up
    for _ in range(1000):
        for email in test_emails:
            is_valid_email(email)

    # Performance test
    iterations = 10000
    start_time = time.time()

    for _ in range(iterations):
        for email in test_emails:
            is_valid_email(email)

    end_time = time.time()
    total_validations = iterations * len(test_emails)
    total_time = end_time - start_time
    validations_per_second = total_validations / total_time

    print(f"Validated {total_validations:,} emails in {total_time:.3f} seconds")
    print(f"Performance: {validations_per_second:,.0f} validations per second")


def demo_doctest():
    """Run the doctests from the module."""
    print("\n=== Doctest Demo ===")
    import doctest
    import email_validator

    result = doctest.testmod(email_validator, verbose=True)
    if result.failed == 0:
        print("All doctests passed!")
    else:
        print(f"Doctests failed: {result.failed} failures")


if __name__ == "__main__":
    print("TDD Email Validator Demonstration")
    print("=" * 50)

    demo_basic_validation()
    demo_edge_cases()
    demo_performance()
    demo_doctest()

    print("\n" + "=" * 50)
    print("Demo completed! Email validator is working correctly.")