import re


def _is_valid_local_char(char):
    """Check if character is valid in local part."""
    return char.isalnum() or char in '._-+'


def _is_valid_local_part(local_part):
    """Validate local part according to rules."""
    if not local_part:
        return False

    # Check for invalid characters
    for char in local_part:
        if not _is_valid_local_char(char):
            return False

    # Check dot rules
    if local_part.startswith('.') or local_part.endswith('.'):
        return False

    if '..' in local_part:
        return False

    return True


def _is_valid_domain_part(domain_part):
    """Validate domain part according to rules."""
    if not domain_part:
        return False

    if '.' not in domain_part:
        return False

    labels = domain_part.split('.')

    if len(labels) < 2:
        return False

    for label in labels:
        if not label:  # Empty label
            return False
        if len(label) > 63:  # Label too long
            return False
        if not all(c.isalnum() or c == '-' for c in label):  # Invalid chars
            return False
        if label.startswith('-') or label.endswith('-'):  # Invalid hyphen placement
            return False

    # Check TLD (last label)
    tld = labels[-1]
    if len(tld) < 2 or not tld.isalpha():
        return False

    return True


def validate_email(email_address: str) -> bool:
    """Validate email address according to practical standards."""
    # Check total email length
    if len(email_address) > 254:
        return False

    if email_address.count('@') != 1:
        return False

    local_part, domain_part = email_address.split('@')

    if not local_part or not domain_part:
        return False

    # Check length limits
    if len(local_part) > 64:
        return False

    if len(domain_part) > 253:
        return False

    if not _is_valid_local_part(local_part):
        return False

    if not _is_valid_domain_part(domain_part):
        return False

    return True