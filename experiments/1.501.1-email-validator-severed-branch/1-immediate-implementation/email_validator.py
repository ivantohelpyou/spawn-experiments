"""
Email Validator - Method 1: Immediate Implementation
Created for severed branch timing experiment 1.501.1
"""

import re


def validate_email(email_address: str) -> bool:
    """Validate email address according to practical standards."""

    # Basic null/empty check
    if not email_address or not isinstance(email_address, str):
        return False

    # Basic format - must have exactly one @
    if email_address.count('@') != 1:
        return False

    # Split into local and domain parts
    local_part, domain_part = email_address.split('@')

    # Length checks per RFC 5321
    if len(email_address) > 254:
        return False
    if len(local_part) > 64:
        return False
    if len(domain_part) > 253:
        return False

    # Validate local part
    if not _validate_local_part(local_part):
        return False

    # Validate domain part
    if not _validate_domain_part(domain_part):
        return False

    return True


def _validate_local_part(local: str) -> bool:
    """Validate the local part (before @) of email address."""

    # Must not be empty
    if not local:
        return False

    # Must not start or end with dot
    if local.startswith('.') or local.endswith('.'):
        return False

    # Must not start or end with hyphen
    if local.startswith('-') or local.endswith('-'):
        return False

    # No consecutive dots
    if '..' in local:
        return False

    # Check allowed characters: a-z, A-Z, 0-9, ., _, -, +
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-+')
    for char in local:
        if char not in allowed_chars:
            return False

    return True


def _validate_domain_part(domain: str) -> bool:
    """Validate the domain part (after @) of email address."""

    # Must not be empty
    if not domain:
        return False

    # Must contain at least one dot
    if '.' not in domain:
        return False

    # Split into labels (parts separated by dots)
    labels = domain.split('.')

    # Must have at least 2 labels (domain.tld)
    if len(labels) < 2:
        return False

    # Validate each label
    for i, label in enumerate(labels):
        if not _validate_domain_label(label, is_tld=(i == len(labels) - 1)):
            return False

    return True


def _validate_domain_label(label: str, is_tld: bool = False) -> bool:
    """Validate a single domain label."""

    # Must not be empty and length 1-63 characters
    if not label or len(label) > 63:
        return False

    # Must not start or end with hyphen
    if label.startswith('-') or label.endswith('-'):
        return False

    if is_tld:
        # TLD must be at least 2 characters and letters only
        if len(label) < 2:
            return False
        if not label.isalpha():
            return False
    else:
        # Regular domain labels: a-z, A-Z, 0-9, hyphens in middle only
        allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-')
        for char in label:
            if char not in allowed_chars:
                return False

    return True