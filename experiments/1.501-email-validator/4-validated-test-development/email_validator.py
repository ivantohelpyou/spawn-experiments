"""
Email Validator Implementation

This module provides email validation functionality following simplified RFC rules.
"""

def is_valid_email(email: str) -> bool:
    """
    Validates email addresses according to simplified RFC rules.

    This implementation checks for:
    - Exactly one @ symbol
    - Valid local part (before @): letters, numbers, dots, underscores, hyphens, plus
    - Valid domain part (after @): letters, numbers, dots, hyphens with proper structure
    - Proper dot and hyphen placement rules
    - ASCII-only characters (no unicode)
    - Whitespace handling (stripped from ends, rejected in middle)

    Args:
        email (str): The email address to validate

    Returns:
        bool: True if email is valid, False otherwise

    Raises:
        TypeError: If input is not a string
    """
    # Type checking
    if not isinstance(email, str):
        raise TypeError("Email must be a string")

    # Strip leading/trailing whitespace
    email = email.strip()

    # Handle empty string (including whitespace-only)
    if not email:
        return False

    # Check total email length (RFC 5321 limit)
    if len(email) > 254:
        return False

    # Check for exactly one @ symbol
    at_count = email.count("@")
    if at_count != 1:
        return False

    # Split into local and domain parts
    local_part, domain_part = email.split("@")

    # Check that both parts are non-empty
    if not local_part or not domain_part:
        return False

    # Check local part length (RFC 5321 limit)
    if len(local_part) > 64:
        return False

    # Check domain part length (RFC 5321 limit)
    if len(domain_part) > 253:
        return False

    # Validate local part
    if not _is_valid_local_part(local_part):
        return False

    # Validate domain part
    if not _is_valid_domain_part(domain_part):
        return False

    return True


def _is_valid_domain_part(domain_part: str) -> bool:
    """
    Validates the domain part (after @) of an email address.

    Args:
        domain_part (str): The domain part to validate

    Returns:
        bool: True if domain part is valid, False otherwise
    """
    import re

    # Domain must contain at least one dot
    if "." not in domain_part:
        return False

    # Check for valid characters: letters, numbers, dots, hyphens only
    if not re.match(r'^[a-zA-Z0-9.-]+$', domain_part):
        return False

    # Check dot placement rules
    if domain_part.startswith('.') or domain_part.endswith('.'):
        return False

    # Check for consecutive dots
    if '..' in domain_part:
        return False

    # Split into labels and validate each label
    labels = domain_part.split('.')
    for label in labels:
        if not _is_valid_domain_label(label):
            return False

    return True


def _is_valid_domain_label(label: str) -> bool:
    """
    Validates a single domain label (part between dots).

    Args:
        label (str): The domain label to validate

    Returns:
        bool: True if label is valid, False otherwise
    """
    # Labels cannot be empty (handled by consecutive dot check)
    if not label:
        return False

    # Labels cannot start or end with hyphens
    if label.startswith('-') or label.endswith('-'):
        return False

    return True


def _is_valid_local_part(local_part: str) -> bool:
    """
    Validates the local part (before @) of an email address.

    Args:
        local_part (str): The local part to validate

    Returns:
        bool: True if local part is valid, False otherwise
    """
    import re

    # Check for valid characters: ASCII letters, numbers, dots, underscores, hyphens, plus
    if not re.match(r'^[a-zA-Z0-9._+-]+$', local_part):
        return False

    # Check dot placement rules
    if local_part.startswith('.') or local_part.endswith('.'):
        return False

    # Check for consecutive dots
    if '..' in local_part:
        return False

    return True