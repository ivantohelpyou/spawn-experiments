"""
Email Validator - Specification-driven Implementation
EXPERIMENT 1.501.1 - Method 2

Validates email addresses according to practical standards.
Implemented following thorough specification analysis and architectural design.
"""

import re


def validate_email(email_address: str) -> bool:
    """
    Validate email address according to practical standards.

    Args:
        email_address: The email address string to validate

    Returns:
        bool: True if email is valid, False otherwise

    Validation Rules:
    1. Basic Format: exactly one '@', length limits
    2. Local Part: allowed chars, no leading/trailing/consecutive dots
    3. Domain Part: ≥1 dot, valid labels, proper TLD
    """
    if not email_address or not isinstance(email_address, str):
        return False

    # Basic structure validation: exactly one '@'
    at_count = email_address.count('@')
    if at_count != 1:
        return False

    # Split into local and domain parts
    local_part, domain_part = email_address.split('@')

    # Length validations (RFC 5321)
    if len(email_address) > 254:
        return False
    if len(local_part) > 64 or len(local_part) == 0:
        return False
    if len(domain_part) > 253 or len(domain_part) == 0:
        return False

    # Validate local part
    if not _validate_local_part(local_part):
        return False

    # Validate domain part
    if not _validate_domain_part(domain_part):
        return False

    return True


def _validate_local_part(local: str) -> bool:
    """
    Validate the local part (before @) of an email address.

    Rules:
    - Allowed: a-z, A-Z, 0-9, . (dot), _ (underscore), - (hyphen), + (plus)
    - Must not start/end with dot
    - No consecutive dots
    - No leading/trailing hyphens
    """
    if not local:
        return False

    # Check for leading/trailing dots or hyphens
    if local.startswith('.') or local.endswith('.'):
        return False
    if local.startswith('-') or local.endswith('-'):
        return False

    # Check for consecutive dots
    if '..' in local:
        return False

    # Character validation: only allowed characters
    allowed_chars = re.compile(r'^[a-zA-Z0-9._+-]+$')
    if not allowed_chars.match(local):
        return False

    return True


def _validate_domain_part(domain: str) -> bool:
    """
    Validate the domain part (after @) of an email address.

    Rules:
    - Must contain at least one dot
    - Must have at least two parts (domain.tld)
    - Each label 1-63 characters
    - Labels: a-z, A-Z, 0-9, hyphens in middle only
    - TLD: ≥2 characters, letters only
    """
    if not domain or '.' not in domain:
        return False

    # Split into labels
    labels = domain.split('.')

    # Must have at least 2 parts (domain.tld)
    if len(labels) < 2:
        return False

    # Validate each label
    for i, label in enumerate(labels):
        if not _validate_domain_label(label, is_tld=(i == len(labels) - 1)):
            return False

    return True


def _validate_domain_label(label: str, is_tld: bool = False) -> bool:
    """
    Validate a single domain label.

    Args:
        label: The domain label to validate
        is_tld: True if this is the top-level domain

    Rules:
    - Length: 1-63 characters
    - Regular labels: a-z, A-Z, 0-9, hyphens in middle only
    - TLD: ≥2 characters, letters only
    """
    if not label:
        return False

    # Length check
    if len(label) > 63:
        return False

    # TLD specific validation
    if is_tld:
        if len(label) < 2:
            return False
        # TLD must be letters only
        if not re.match(r'^[a-zA-Z]+$', label):
            return False
        return True

    # Regular label validation
    if len(label) < 1:
        return False

    # Cannot start or end with hyphen
    if label.startswith('-') or label.endswith('-'):
        return False

    # Only allowed characters: letters, digits, hyphens
    if not re.match(r'^[a-zA-Z0-9-]+$', label):
        return False

    return True


if __name__ == "__main__":
    # Test examples for immediate validation
    test_cases = [
        # Valid cases
        ("user@example.com", True),
        ("test.email+tag@domain.co", True),
        ("user_name@test-domain.org", True),
        ("a@b.co", True),

        # Invalid cases - basic structure
        ("invalid", False),
        ("@domain.com", False),
        ("user@", False),
        ("user@@domain.com", False),

        # Invalid cases - local part
        (".user@domain.com", False),
        ("user.@domain.com", False),
        ("us..er@domain.com", False),
        ("-user@domain.com", False),
        ("user-@domain.com", False),

        # Invalid cases - domain part
        ("user@domain", False),
        ("user@.domain.com", False),
        ("user@domain..com", False),
        ("user@domain-", False),
        ("user@domain.c", False),
        ("user@domain.123", False),
    ]

    print("Email Validator Test Results:")
    print("=" * 40)

    all_passed = True
    for email, expected in test_cases:
        result = validate_email(email)
        status = "PASS" if result == expected else "FAIL"
        if result != expected:
            all_passed = False
        print(f"{status}: {email:25} -> {result} (expected {expected})")

    print("=" * 40)
    print(f"Overall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")