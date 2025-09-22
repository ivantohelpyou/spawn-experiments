"""
Email Validator Implementation

This module provides email validation functionality according to practical standards
as defined in the accompanying specifications document.
"""

import re
from typing import Union


def validate_email(email: Union[str, None]) -> bool:
    """
    Validate an email address according to practical standards.

    This function validates email addresses based on a practical subset of email
    standards, focusing on commonly used patterns while maintaining reasonable
    complexity.

    Args:
        email: The email address to validate (can be None or non-string)

    Returns:
        bool: True if the email is valid according to the specifications, False otherwise

    Examples:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid.email")
        False
        >>> validate_email("user@")
        False
        >>> validate_email(None)
        False
    """
    # Handle None and non-string inputs
    if not isinstance(email, str):
        return False

    # Trim whitespace and convert to lowercase for consistent processing
    email = email.strip().lower()

    # Check for empty string after trimming
    if not email:
        return False

    # Basic structure validation: must contain exactly one '@' symbol
    if email.count('@') != 1:
        return False

    # Split into local and domain parts
    local_part, domain_part = email.split('@')

    # Validate length limits according to RFC 5321
    if len(email) > 254:  # Total email length limit
        return False
    if len(local_part) > 64:  # Local part length limit
        return False
    if len(domain_part) > 253:  # Domain part length limit
        return False

    # Validate local part
    if not _validate_local_part(local_part):
        return False

    # Validate domain part
    if not _validate_domain_part(domain_part):
        return False

    return True


def _validate_local_part(local_part: str) -> bool:
    """
    Validate the local part (before '@') of an email address.

    Args:
        local_part: The local part to validate

    Returns:
        bool: True if valid, False otherwise
    """
    # Must not be empty
    if not local_part:
        return False

    # Must not start or end with dot
    if local_part.startswith('.') or local_part.endswith('.'):
        return False

    # Must not start or end with hyphen
    if local_part.startswith('-') or local_part.endswith('-'):
        return False

    # Must not contain consecutive dots
    if '..' in local_part:
        return False

    # Check allowed characters and pattern
    # Pattern: alphanumeric start, followed by allowed chars, no consecutive separators
    local_pattern = r'^[a-zA-Z0-9]+([._+-][a-zA-Z0-9]+)*$'

    return bool(re.match(local_pattern, local_part))


def _validate_domain_part(domain_part: str) -> bool:
    """
    Validate the domain part (after '@') of an email address.

    Args:
        domain_part: The domain part to validate

    Returns:
        bool: True if valid, False otherwise
    """
    # Must not be empty
    if not domain_part:
        return False

    # Must contain at least one dot to separate domain levels
    if '.' not in domain_part:
        return False

    # Must not start or end with dot
    if domain_part.startswith('.') or domain_part.endswith('.'):
        return False

    # Must not contain consecutive dots
    if '..' in domain_part:
        return False

    # Split into domain labels
    labels = domain_part.split('.')

    # Must have at least 2 labels (domain.tld)
    if len(labels) < 2:
        return False

    # Validate each domain label
    for i, label in enumerate(labels):
        if not _validate_domain_label(label, is_tld=(i == len(labels) - 1)):
            return False

    return True


def _validate_domain_label(label: str, is_tld: bool = False) -> bool:
    """
    Validate a single domain label.

    Args:
        label: The domain label to validate
        is_tld: Whether this label is the top-level domain

    Returns:
        bool: True if valid, False otherwise
    """
    # Must not be empty
    if not label:
        return False

    # Length must be 1-63 characters
    if len(label) < 1 or len(label) > 63:
        return False

    # Must not start or end with hyphen
    if label.startswith('-') or label.endswith('-'):
        return False

    if is_tld:
        # TLD specific validation
        # Must be at least 2 characters long
        if len(label) < 2:
            return False

        # Must contain only alphabetic characters
        if not re.match(r'^[a-zA-Z]+$', label):
            return False
    else:
        # Regular domain label validation
        # Must contain only alphanumeric characters and hyphens
        if not re.match(r'^[a-zA-Z0-9-]+$', label):
            return False

    return True


# Additional utility functions for comprehensive testing and validation

def get_validation_details(email: Union[str, None]) -> dict:
    """
    Get detailed validation information about an email address.

    Args:
        email: The email address to analyze

    Returns:
        dict: Detailed validation results including specific failure reasons
    """
    result = {
        'is_valid': False,
        'email': email,
        'errors': []
    }

    # Handle None and non-string inputs
    if not isinstance(email, str):
        result['errors'].append('Input must be a string')
        return result

    original_email = email
    email = email.strip().lower()
    result['normalized_email'] = email

    # Check for empty string after trimming
    if not email:
        result['errors'].append('Email cannot be empty')
        return result

    # Basic structure validation
    at_count = email.count('@')
    if at_count == 0:
        result['errors'].append('Email must contain @ symbol')
        return result
    elif at_count > 1:
        result['errors'].append('Email must contain exactly one @ symbol')
        return result

    # Split into parts
    local_part, domain_part = email.split('@')
    result['local_part'] = local_part
    result['domain_part'] = domain_part

    # Length validations
    if len(email) > 254:
        result['errors'].append(f'Total email length ({len(email)}) exceeds 254 characters')
    if len(local_part) > 64:
        result['errors'].append(f'Local part length ({len(local_part)}) exceeds 64 characters')
    if len(domain_part) > 253:
        result['errors'].append(f'Domain part length ({len(domain_part)}) exceeds 253 characters')

    # Validate local part
    if not local_part:
        result['errors'].append('Local part cannot be empty')
    else:
        local_errors = _get_local_part_errors(local_part)
        result['errors'].extend(local_errors)

    # Validate domain part
    if not domain_part:
        result['errors'].append('Domain part cannot be empty')
    else:
        domain_errors = _get_domain_part_errors(domain_part)
        result['errors'].extend(domain_errors)

    # Set validity
    result['is_valid'] = len(result['errors']) == 0

    return result


def _get_local_part_errors(local_part: str) -> list:
    """Get specific error messages for local part validation."""
    errors = []

    if local_part.startswith('.'):
        errors.append('Local part cannot start with dot')
    if local_part.endswith('.'):
        errors.append('Local part cannot end with dot')
    if local_part.startswith('-'):
        errors.append('Local part cannot start with hyphen')
    if local_part.endswith('-'):
        errors.append('Local part cannot end with hyphen')
    if '..' in local_part:
        errors.append('Local part cannot contain consecutive dots')

    # Check for invalid characters
    local_pattern = r'^[a-zA-Z0-9._+-]+$'
    if not re.match(local_pattern, local_part):
        errors.append('Local part contains invalid characters')

    return errors


def _get_domain_part_errors(domain_part: str) -> list:
    """Get specific error messages for domain part validation."""
    errors = []

    if '.' not in domain_part:
        errors.append('Domain part must contain at least one dot')
        return errors

    if domain_part.startswith('.'):
        errors.append('Domain part cannot start with dot')
    if domain_part.endswith('.'):
        errors.append('Domain part cannot end with dot')
    if '..' in domain_part:
        errors.append('Domain part cannot contain consecutive dots')

    labels = domain_part.split('.')
    if len(labels) < 2:
        errors.append('Domain part must have at least two labels')

    for i, label in enumerate(labels):
        is_tld = (i == len(labels) - 1)
        label_errors = _get_domain_label_errors(label, is_tld)
        errors.extend(label_errors)

    return errors


def _get_domain_label_errors(label: str, is_tld: bool = False) -> list:
    """Get specific error messages for domain label validation."""
    errors = []

    if not label:
        errors.append('Domain label cannot be empty')
        return errors

    if len(label) > 63:
        errors.append(f'Domain label "{label}" exceeds 63 characters')

    if label.startswith('-'):
        errors.append(f'Domain label "{label}" cannot start with hyphen')
    if label.endswith('-'):
        errors.append(f'Domain label "{label}" cannot end with hyphen')

    if is_tld:
        if len(label) < 2:
            errors.append(f'TLD "{label}" must be at least 2 characters long')
        if not re.match(r'^[a-zA-Z]+$', label):
            errors.append(f'TLD "{label}" must contain only alphabetic characters')
    else:
        if not re.match(r'^[a-zA-Z0-9-]+$', label):
            errors.append(f'Domain label "{label}" contains invalid characters')

    return errors


if __name__ == "__main__":
    # Basic demonstration of the validator
    test_emails = [
        # Valid emails
        "user@example.com",
        "john.doe@company.org",
        "test_email@domain.co.uk",
        "user+tag@example.com",
        "a@b.co",

        # Invalid emails
        "@example.com",
        "user@",
        "userexample.com",
        ".user@example.com",
        "user@example",
        "user@example.c",
        None,
        ""
    ]

    print("Email Validation Results:")
    print("=" * 40)

    for email in test_emails:
        is_valid = validate_email(email)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{str(email):25} -> {status}")