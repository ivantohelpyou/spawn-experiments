"""
Email Validator Demo - Method 1: Immediate Implementation
Demonstrates the email validation functionality with various examples.
"""

from email_validator import validate_email


def demo_email_validation():
    """Demonstrate email validation with various examples."""
    print("Email Validator Demo - Method 1: Immediate Implementation")
    print("=" * 60)

    test_cases = [
        # Valid emails
        ("test@example.com", "Basic valid email"),
        ("user.name@domain.co.uk", "Email with dots and multi-level domain"),
        ("first_last@company.org", "Email with underscore"),
        ("user+tag@service.net", "Email with plus sign"),
        ("a@b.co", "Minimal valid email"),

        # Invalid emails
        ("", "Empty string"),
        ("notanemail", "No @ symbol"),
        ("user@", "Missing domain"),
        ("@domain.com", "Missing local part"),
        (".invalid@example.com", "Local part starts with dot"),
        ("invalid.@example.com", "Local part ends with dot"),
        ("user@domain", "Domain missing TLD"),
        ("user@domain.x", "TLD too short"),
        ("user@domain.123", "TLD not letters only"),
        ("double..dots@example.com", "Consecutive dots in local part"),
    ]

    print(f"{'Email':<30} {'Valid':<7} {'Description'}")
    print("-" * 60)

    for email, description in test_cases:
        is_valid = validate_email(email)
        status = "✓ Yes" if is_valid else "✗ No"
        print(f"{email:<30} {status:<7} {description}")

    print("-" * 60)
    print("Demo completed successfully!")


if __name__ == "__main__":
    demo_email_validation()