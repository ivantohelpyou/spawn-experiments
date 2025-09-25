"""
Test suite for Email Validator - Method 1: Immediate Implementation
"""

from email_validator import validate_email


def test_valid_emails():
    """Test valid email addresses."""
    valid_emails = [
        "test@example.com",
        "user.name@domain.co.uk",
        "first_last@company.org",
        "user+tag@service.net",
        "123@numbers.com",
        "a@b.co",
        "long.email.with.many.dots@sub.domain.example.com",
        "user-name@test-domain.info",
        "test123@example123.com"
    ]

    for email in valid_emails:
        assert validate_email(email), f"Should be valid: {email}"
    print(f"✓ All {len(valid_emails)} valid emails passed")


def test_invalid_emails():
    """Test invalid email addresses."""
    invalid_emails = [
        # Basic format issues
        "",
        "notanemail",
        "no@at@symbol.com",
        "@nolocal.com",
        "nodomain@",
        "no@domain",

        # Local part issues
        ".startswithdot@example.com",
        "endswithdot.@example.com",
        "double..dots@example.com",
        "-startshyphen@example.com",
        "endshyphen-@example.com",
        "invalid$char@example.com",
        "spaces in@example.com",

        # Domain issues
        "user@nodots",
        "user@.startsdot.com",
        "user@endsdot.",
        "user@double..dots.com",
        "user@-startshyphen.com",
        "user@endshyphen-.com",
        "user@invalid$.com",
        "user@spaces in.com",
        "user@domain.x",  # TLD too short
        "user@domain.123",  # TLD not letters

        # Length issues
        "a" * 65 + "@example.com",  # local part too long
        "user@" + "a" * 250 + ".com",  # domain too long
        "a" * 250 + "@" + "b" * 250 + ".com",  # total too long
    ]

    for email in invalid_emails:
        assert not validate_email(email), f"Should be invalid: {email}"
    print(f"✓ All {len(invalid_emails)} invalid emails correctly rejected")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    # Exact length limits
    assert validate_email("a" * 64 + "@b.co"), "Local part at max length should be valid"
    assert not validate_email("a" * 65 + "@b.co"), "Local part over max should be invalid"

    # Domain label length
    long_label = "a" * 63
    assert validate_email(f"user@{long_label}.com"), "Domain label at max length should be valid"

    # TLD minimum length
    assert validate_email("user@domain.co"), "2-char TLD should be valid"
    assert not validate_email("user@domain.c"), "1-char TLD should be invalid"

    # None and non-string inputs
    assert not validate_email(None), "None should be invalid"
    assert not validate_email(123), "Number should be invalid"
    assert not validate_email([]), "List should be invalid"

    print("✓ All edge cases handled correctly")


def run_all_tests():
    """Run all test suites."""
    print("Running Email Validator Tests - Method 1: Immediate Implementation")
    print("=" * 70)

    test_valid_emails()
    test_invalid_emails()
    test_edge_cases()

    print("=" * 70)
    print("✓ All tests passed!")


if __name__ == "__main__":
    run_all_tests()