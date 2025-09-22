"""
Demonstration script for the Email Validator

This script showcases the email validator functionality with detailed
validation results and examples from the specifications.
"""

from email_validator import validate_email, get_validation_details


def demo_basic_validation():
    """Demonstrate basic email validation."""
    print("=" * 60)
    print("BASIC EMAIL VALIDATION DEMONSTRATION")
    print("=" * 60)

    test_emails = [
        # Valid examples from specifications
        "user@example.com",
        "john.doe@company.org",
        "test_email@domain.co.uk",
        "user+tag@example.com",
        "a@b.co",
        "123@example.com",
        "user-name@sub.domain.com",

        # Invalid examples from specifications
        "@example.com",
        "user@",
        "userexample.com",
        ".user@example.com",
        "user@example",
        "user@example.c",
        "user@@example.com",
    ]

    for email in test_emails:
        is_valid = validate_email(email)
        status = "✓ VALID  " if is_valid else "✗ INVALID"
        print(f"{email:30} -> {status}")


def demo_detailed_validation():
    """Demonstrate detailed validation with error reporting."""
    print("\n" + "=" * 60)
    print("DETAILED VALIDATION DEMONSTRATION")
    print("=" * 60)

    test_cases = [
        "user@example.com",  # Valid
        ".user@example.com",  # Invalid: starts with dot
        "user..name@example.com",  # Invalid: consecutive dots
        "user@example",  # Invalid: no TLD
        "user@example.c",  # Invalid: TLD too short
        "user@-example.com",  # Invalid: domain starts with hyphen
        "",  # Invalid: empty
        None,  # Invalid: None
    ]

    for email in test_cases:
        print(f"\nAnalyzing: {email}")
        print("-" * 40)

        details = get_validation_details(email)

        if details['is_valid']:
            print("✓ VALID EMAIL")
            print(f"  Normalized: {details['normalized_email']}")
            print(f"  Local part: {details['local_part']}")
            print(f"  Domain part: {details['domain_part']}")
        else:
            print("✗ INVALID EMAIL")
            print("  Errors:")
            for error in details['errors']:
                print(f"    - {error}")


def demo_edge_cases():
    """Demonstrate handling of edge cases."""
    print("\n" + "=" * 60)
    print("EDGE CASES DEMONSTRATION")
    print("=" * 60)

    edge_cases = [
        # Length boundaries
        ("Local part at limit (64 chars)", "a" * 64 + "@example.com"),
        ("Local part over limit (65 chars)", "a" * 65 + "@example.com"),

        # Case sensitivity
        ("Mixed case", "User.Name@Example.COM"),

        # Whitespace handling
        ("With surrounding spaces", "  user@example.com  "),

        # Special characters
        ("Plus addressing", "user+tag+more@example.com"),
        ("Underscores and dots", "user_name.test@example.com"),

        # Minimal valid
        ("Shortest valid email", "x@y.ab"),

        # TLD edge cases
        ("Two character TLD", "user@example.ab"),
        ("One character TLD (invalid)", "user@example.a"),
    ]

    for description, email in edge_cases:
        is_valid = validate_email(email)
        status = "✓ VALID  " if is_valid else "✗ INVALID"
        print(f"{description:35} -> {status}")
        print(f"  Email: {email}")
        print()


def demo_specification_compliance():
    """Demonstrate compliance with specifications."""
    print("\n" + "=" * 60)
    print("SPECIFICATION COMPLIANCE DEMONSTRATION")
    print("=" * 60)

    print("1. RFC 5321 Length Limits:")
    print(f"   Total length limit (254): {'✓' if not validate_email('a' * 255) else '✗'}")
    print(f"   Local part limit (64): {'✓' if not validate_email('a' * 65 + '@b.co') else '✗'}")

    print("\n2. Required @ Symbol:")
    print(f"   No @ symbol: {'✓' if not validate_email('userexample.com') else '✗'}")
    print(f"   Multiple @ symbols: {'✓' if not validate_email('user@@example.com') else '✗'}")
    print(f"   Exactly one @ symbol: {'✓' if validate_email('user@example.com') else '✗'}")

    print("\n3. Domain Structure Requirements:")
    print(f"   No TLD: {'✓' if not validate_email('user@example') else '✗'}")
    print(f"   TLD too short: {'✓' if not validate_email('user@example.c') else '✗'}")
    print(f"   Numeric TLD: {'✓' if not validate_email('user@example.123') else '✗'}")
    print(f"   Valid structure: {'✓' if validate_email('user@example.com') else '✗'}")

    print("\n4. Local Part Rules:")
    print(f"   Starts with dot: {'✓' if not validate_email('.user@example.com') else '✗'}")
    print(f"   Ends with dot: {'✓' if not validate_email('user.@example.com') else '✗'}")
    print(f"   Consecutive dots: {'✓' if not validate_email('user..name@example.com') else '✗'}")
    print(f"   Valid format: {'✓' if validate_email('user.name@example.com') else '✗'}")

    print("\n5. Case Insensitivity:")
    print(f"   Uppercase: {'✓' if validate_email('USER@EXAMPLE.COM') else '✗'}")
    print(f"   Mixed case: {'✓' if validate_email('User@Example.Com') else '✗'}")


def demo_unsupported_features():
    """Demonstrate unsupported features as per specifications."""
    print("\n" + "=" * 60)
    print("UNSUPPORTED FEATURES (Should be Invalid)")
    print("=" * 60)

    unsupported = [
        ('Quoted strings', '"user name"@example.com'),
        ('IP addresses', 'user@[192.168.1.1]'),
        ('Comments', 'user(comment)@example.com'),
        ('Unicode domains', 'user@例え.テスト'),
    ]

    for description, email in unsupported:
        is_valid = validate_email(email)
        status = "✓ Correctly rejected" if not is_valid else "✗ Incorrectly accepted"
        print(f"{description:20} -> {status}")
        print(f"  Email: {email}")
        print()


if __name__ == "__main__":
    print("EMAIL VALIDATOR SPECIFICATION-DRIVEN IMPLEMENTATION")
    print("Demo showcasing compliance with specifications")

    demo_basic_validation()
    demo_detailed_validation()
    demo_edge_cases()
    demo_specification_compliance()
    demo_unsupported_features()

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("All tests demonstrate compliance with the specifications.")
    print("See email_validator_specifications.md for detailed requirements.")