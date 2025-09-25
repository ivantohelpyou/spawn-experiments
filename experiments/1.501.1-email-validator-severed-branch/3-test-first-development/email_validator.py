"""
Email validator implementation following Test-First Development methodology
Implements practical email validation according to baseline specification
"""

# Character sets for validation
LOCAL_PART_ALLOWED_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-+')
DOMAIN_LABEL_ALLOWED_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-')


def validate_email(email_address: str) -> bool:
    """
    Validate email address according to practical standards.

    Args:
        email_address: The email address string to validate

    Returns:
        bool: True if email is valid, False otherwise
    """
    # Handle None and empty string
    if not email_address or not isinstance(email_address, str):
        return False

    # Remove leading/trailing whitespace would make it invalid
    if email_address != email_address.strip():
        return False

    # Check for any whitespace characters in email
    if any(c.isspace() for c in email_address):
        return False

    # Total length check (RFC 5321 limit)
    if len(email_address) > 254:
        return False

    # Must contain exactly one '@' symbol
    at_count = email_address.count('@')
    if at_count != 1:
        return False

    # Split into local and domain parts
    try:
        local_part, domain_part = email_address.split('@', 1)
    except ValueError:
        return False

    # Validate local part
    if not _validate_local_part(local_part):
        return False

    # Validate domain part
    if not _validate_domain_part(domain_part):
        return False

    return True


def _validate_local_part(local_part: str) -> bool:
    """Validate the local part of an email address (before @)"""
    # Check length constraints
    if len(local_part) == 0 or len(local_part) > 64:
        return False

    # Check allowed characters: a-z, A-Z, 0-9, ., _, -, +
    if not all(c in LOCAL_PART_ALLOWED_CHARS for c in local_part):
        return False

    # Dot rules: cannot start or end with dot, no consecutive dots
    if local_part.startswith('.') or local_part.endswith('.'):
        return False

    if '..' in local_part:
        return False

    # Hyphen rules: cannot start or end with hyphen
    if local_part.startswith('-') or local_part.endswith('-'):
        return False

    return True


def _validate_domain_part(domain_part: str) -> bool:
    """Validate the domain part of an email address (after @)"""
    # Check basic constraints
    if len(domain_part) == 0 or len(domain_part) > 253:
        return False

    # Must contain at least one dot
    if '.' not in domain_part:
        return False

    # Cannot start or end with dot
    if domain_part.startswith('.') or domain_part.endswith('.'):
        return False

    # No consecutive dots
    if '..' in domain_part:
        return False

    # Split into labels
    labels = domain_part.split('.')

    # Must have at least 2 labels (domain.tld)
    if len(labels) < 2:
        return False

    # Validate each label
    for i, label in enumerate(labels):
        if not _validate_domain_label(label, is_tld=(i == len(labels) - 1)):
            return False

    return True


def _validate_domain_label(label: str, is_tld: bool = False) -> bool:
    """Validate a single domain label"""
    # Length constraints
    if len(label) == 0 or len(label) > 63:
        return False

    # TLD specific rules
    if is_tld:
        # TLD must be at least 2 characters
        if len(label) < 2:
            return False
        # TLD must be letters only
        if not label.isalpha():
            return False
    else:
        # Regular domain labels: a-z, A-Z, 0-9, hyphens (not at start/end)
        if not all(c in DOMAIN_LABEL_ALLOWED_CHARS for c in label):
            return False

        # Cannot start or end with hyphen
        if label.startswith('-') or label.endswith('-'):
            return False

    return True