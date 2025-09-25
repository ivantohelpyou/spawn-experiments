"""
Demo script for Email Validator
EXPERIMENT 1.501.1 - Method 2: Specification-driven Development

Demonstrates the email validator with various test cases.
"""

from email_validator import validate_email


def demo_email_validation():
    """Demonstrate email validation with comprehensive examples."""

    print("Email Validator Demo")
    print("=" * 50)
    print("Specification-driven Implementation")
    print()

    # Test cases organized by category
    test_categories = {
        "Valid Basic Emails": [
            "user@example.com",
            "test@domain.org",
            "simple@site.net",
            "a@b.co",
        ],
        "Valid Complex Emails": [
            "user.name@example.com",
            "test+tag@domain.org",
            "user_123@test-site.co",
            "long.email.address@sub.domain.example.com",
        ],
        "Invalid - Basic Structure": [
            "invalid",
            "user@",
            "@domain.com",
            "user@@domain.com",
            "",
        ],
        "Invalid - Local Part Issues": [
            ".user@domain.com",
            "user.@domain.com",
            "us..er@domain.com",
            "-user@domain.com",
            "user-@domain.com",
            "user space@domain.com",
        ],
        "Invalid - Domain Issues": [
            "user@domain",
            "user@.domain.com",
            "user@domain..com",
            "user@domain-.com",
            "user@-domain.com",
            "user@domain.c",
            "user@domain.123",
        ],
    }

    for category, emails in test_categories.items():
        print(f"{category}:")
        print("-" * len(category))

        for email in emails:
            result = validate_email(email)
            status = "✓" if result else "✗"
            print(f"  {status} {email:35} -> {result}")
        print()

    # Test edge cases
    print("Edge Cases:")
    print("-" * 10)

    # Test length limits
    max_local = "a" * 64
    valid_max_email = max_local + "@example.com"
    print(f"  Max local part (64 chars): {validate_email(valid_max_email)}")

    too_long_local = "a" * 65 + "@example.com"
    print(f"  Too long local (65 chars): {validate_email(too_long_local)}")

    # Test non-string inputs
    print(f"  Non-string input (123): {validate_email(123)}")
    print(f"  Non-string input (None): {validate_email(None)}")


if __name__ == "__main__":
    demo_email_validation()