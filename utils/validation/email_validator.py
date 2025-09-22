"""
Email validator implementation.
Created using Test-Driven Development.

This module provides a function to validate email addresses according to RFC 5321
specifications with additional practical constraints for real-world usage.
"""

import re
from typing import Union

# Pre-compiled regex patterns for better performance
LOCAL_PART_PATTERN = re.compile(r'^[a-zA-Z0-9._+-]+$')
DOMAIN_PART_PATTERN = re.compile(r'^[a-zA-Z0-9.-]+$')

# RFC 5321 length limits
MAX_EMAIL_LENGTH = 320
MAX_LOCAL_PART_LENGTH = 64
MAX_DOMAIN_PART_LENGTH = 253


def is_valid_email(email: Union[str, None]) -> bool:
    """
    Validate email address format according to RFC 5321 with practical constraints.

    This function validates email addresses using a practical subset of RFC 5321
    rules, focusing on commonly accepted email formats while preventing
    common security issues and malformed addresses.

    Args:
        email: String representing email address to validate, or None

    Returns:
        bool: True if email is valid according to our rules, False otherwise

    Examples:
        >>> is_valid_email("user@domain.com")
        True
        >>> is_valid_email("invalid.email")
        False
        >>> is_valid_email("user+tag@my-domain.org")
        True
        >>> is_valid_email("")
        False
    """
    # Fast validation for common invalid cases
    if not isinstance(email, str) or not email or len(email) > MAX_EMAIL_LENGTH:
        return False

    # Must contain exactly one @ symbol
    at_count = email.count('@')
    if at_count != 1:
        return False

    # Split and validate both parts
    local_part, domain_part = email.split('@')
    return (_is_valid_local_part(local_part) and
            _is_valid_domain_part(domain_part))


def _is_valid_local_part(local_part: str) -> bool:
    """
    Validate the local part (before @) of an email address.

    Rules applied:
    - Must not be empty
    - Length must not exceed 64 characters (RFC 5321)
    - Cannot start or end with dot
    - Cannot contain spaces
    - Must contain only allowed characters: a-z, A-Z, 0-9, ., _, +, -

    Args:
        local_part: The local part of the email address

    Returns:
        bool: True if valid, False otherwise
    """
    # Fast checks for common invalid cases
    if (not local_part or
        len(local_part) > MAX_LOCAL_PART_LENGTH or
        local_part[0] == '.' or
        local_part[-1] == '.' or
        '..' in local_part or
        ' ' in local_part):
        return False

    # Character validation using pre-compiled regex
    return bool(LOCAL_PART_PATTERN.match(local_part))


def _is_valid_domain_part(domain_part: str) -> bool:
    """
    Validate the domain part (after @) of an email address.

    Rules applied:
    - Must not be empty
    - Length must not exceed 253 characters (RFC 5321)
    - Must contain at least one dot
    - Cannot start or end with dot
    - Cannot have consecutive dots
    - Cannot contain spaces
    - Each label (between dots) cannot start/end with hyphen
    - Must contain only allowed characters: a-z, A-Z, 0-9, ., -

    Args:
        domain_part: The domain part of the email address

    Returns:
        bool: True if valid, False otherwise
    """
    # Fast checks for common invalid cases
    if (not domain_part or
        len(domain_part) > MAX_DOMAIN_PART_LENGTH or
        '.' not in domain_part or
        domain_part[0] == '.' or
        domain_part[-1] == '.' or
        '..' in domain_part or
        ' ' in domain_part):
        return False

    # Character validation using pre-compiled regex
    if not DOMAIN_PART_PATTERN.match(domain_part):
        return False

    # Validate each label (domain segment between dots)
    labels = domain_part.split('.')
    for label in labels:
        if not label or label[0] == '-' or label[-1] == '-':
            return False

    return True