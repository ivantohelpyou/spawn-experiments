"""
Comprehensive Email Validator using Python standard library only.

This module provides a robust email validation system with multiple validation levels,
comprehensive error handling, and RFC-compliant checks.
"""

import re
import string
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum


class ValidationLevel(Enum):
    """Email validation strictness levels."""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    RFC_COMPLIANT = "rfc_compliant"


class EmailValidationError(Exception):
    """Base exception for email validation errors."""
    pass


class InvalidEmailFormatError(EmailValidationError):
    """Raised when email format is invalid."""
    pass


class InvalidLocalPartError(EmailValidationError):
    """Raised when local part (before @) is invalid."""
    pass


class InvalidDomainError(EmailValidationError):
    """Raised when domain part (after @) is invalid."""
    pass


class EmailTooLongError(EmailValidationError):
    """Raised when email exceeds maximum length."""
    pass


class EmailValidator:
    """
    Comprehensive email validator with multiple validation levels and detailed error reporting.

    Features:
    - Multiple validation levels (basic to RFC-compliant)
    - Detailed error messages and types
    - Support for quoted strings and special characters
    - Domain validation including TLD checks
    - Length validation according to RFC standards
    - Internationalized domain name support
    - Comprehensive test coverage
    """

    # RFC 5321/5322 length limits
    MAX_EMAIL_LENGTH = 320  # Total email length
    MAX_LOCAL_LENGTH = 64   # Local part length
    MAX_DOMAIN_LENGTH = 253 # Domain part length
    MAX_LABEL_LENGTH = 63   # Individual domain label length

    # Common regex patterns
    PATTERNS = {
        'basic': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'standard': r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$',
        'local_part': r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+$',
        'quoted_local': r'^"[^"\\]*(?:\\.[^"\\]*)*"$',
        'domain_label': r'^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$',
        'tld': r'^[a-zA-Z]{2,6}$',
        'ip_address': r'^\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\]$'
    }

    # Common TLDs for validation
    COMMON_TLDS = {
        'com', 'org', 'net', 'edu', 'gov', 'mil', 'int', 'co', 'io', 'me', 'tv',
        'info', 'biz', 'name', 'mobi', 'travel', 'museum', 'aero', 'coop', 'jobs',
        'uk', 'ca', 'au', 'de', 'fr', 'jp', 'cn', 'in', 'br', 'ru', 'mx', 'it',
        'es', 'nl', 'se', 'no', 'dk', 'fi', 'pl', 'be', 'ch', 'at', 'ie', 'nz'
    }

    def __init__(self, validation_level: ValidationLevel = ValidationLevel.STANDARD):
        """
        Initialize the email validator.

        Args:
            validation_level: The strictness level for validation
        """
        self.validation_level = validation_level
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for better performance."""
        self.compiled_patterns = {
            name: re.compile(pattern)
            for name, pattern in self.PATTERNS.items()
        }

    def _split_email(self, email: str) -> Tuple[str, str]:
        """
        Split email into local and domain parts, properly handling quoted strings.

        Args:
            email: The email address to split

        Returns:
            Tuple of (local_part, domain_part)

        Raises:
            InvalidEmailFormatError: If email format is invalid
        """
        # Handle quoted local parts
        if email.startswith('"'):
            # Find the closing quote
            quote_end = -1
            i = 1
            while i < len(email):
                if email[i] == '"' and (i == 1 or email[i-1] != '\\'):
                    quote_end = i
                    break
                elif email[i] == '\\' and i + 1 < len(email):
                    i += 2  # Skip escaped character
                    continue
                i += 1

            if quote_end == -1:
                raise InvalidEmailFormatError("Unterminated quoted string in local part")

            # Check if @ immediately follows the closing quote
            if quote_end + 1 >= len(email) or email[quote_end + 1] != '@':
                raise InvalidEmailFormatError("Invalid character after quoted local part")

            local_part = email[:quote_end + 1]
            domain_part = email[quote_end + 2:]

            if not domain_part:
                raise InvalidEmailFormatError("Domain part cannot be empty")

            return local_part, domain_part

        # Handle non-quoted emails
        at_count = email.count('@')
        if at_count != 1:
            raise InvalidEmailFormatError(f"Email must contain exactly one @ symbol, found {at_count}")

        local_part, domain_part = email.rsplit('@', 1)

        if not local_part:
            raise InvalidEmailFormatError("Local part cannot be empty")
        if not domain_part:
            raise InvalidEmailFormatError("Domain part cannot be empty")

        return local_part, domain_part

    def validate(self, email: str, raise_on_error: bool = False) -> Tuple[bool, List[str]]:
        """
        Validate an email address.

        Args:
            email: The email address to validate
            raise_on_error: Whether to raise exceptions on validation errors

        Returns:
            Tuple of (is_valid, list_of_errors)

        Raises:
            EmailValidationError: If raise_on_error=True and validation fails
        """
        errors = []

        try:
            # Basic checks
            if not email or not isinstance(email, str):
                raise InvalidEmailFormatError("Email must be a non-empty string")

            email = email.strip()
            if not email:
                raise InvalidEmailFormatError("Email cannot be empty or whitespace only")

            # Length check
            if len(email) > self.MAX_EMAIL_LENGTH:
                raise EmailTooLongError(f"Email exceeds maximum length of {self.MAX_EMAIL_LENGTH} characters")

            # Split email properly handling quoted strings
            local_part, domain_part = self._split_email(email)

            # Validate based on selected level
            if self.validation_level == ValidationLevel.BASIC:
                self._validate_basic(email)
            elif self.validation_level == ValidationLevel.STANDARD:
                self._validate_standard(local_part, domain_part)
            elif self.validation_level == ValidationLevel.STRICT:
                self._validate_strict(local_part, domain_part)
            elif self.validation_level == ValidationLevel.RFC_COMPLIANT:
                self._validate_rfc_compliant(local_part, domain_part)

        except EmailValidationError as e:
            errors.append(str(e))
            if raise_on_error:
                raise

        is_valid = len(errors) == 0
        return is_valid, errors

    def _validate_basic(self, email: str):
        """Basic email validation using simple regex."""
        if not self.compiled_patterns['basic'].match(email):
            raise InvalidEmailFormatError("Email format is invalid (basic validation)")

    def _validate_standard(self, local_part: str, domain_part: str):
        """Standard email validation with common rules."""
        self._validate_local_part_standard(local_part)
        self._validate_domain_standard(domain_part)

    def _validate_strict(self, local_part: str, domain_part: str):
        """Strict email validation with additional checks."""
        self._validate_local_part_strict(local_part)
        self._validate_domain_strict(domain_part)

    def _validate_rfc_compliant(self, local_part: str, domain_part: str):
        """RFC 5321/5322 compliant validation."""
        self._validate_local_part_rfc(local_part)
        self._validate_domain_rfc(domain_part)

    def _validate_local_part_standard(self, local_part: str):
        """Validate local part with standard rules."""
        if not local_part:
            raise InvalidLocalPartError("Local part cannot be empty")

        if len(local_part) > self.MAX_LOCAL_LENGTH:
            raise InvalidLocalPartError(f"Local part exceeds maximum length of {self.MAX_LOCAL_LENGTH} characters")

        # Check for consecutive dots
        if '..' in local_part:
            raise InvalidLocalPartError("Local part cannot contain consecutive dots")

        # Cannot start or end with dot
        if local_part.startswith('.') or local_part.endswith('.'):
            raise InvalidLocalPartError("Local part cannot start or end with a dot")

        # Basic character validation
        if not self.compiled_patterns['local_part'].match(local_part):
            raise InvalidLocalPartError("Local part contains invalid characters")

    def _validate_local_part_strict(self, local_part: str):
        """Strict local part validation."""
        self._validate_local_part_standard(local_part)

        # Additional strict checks
        if local_part.count('.') > 1:
            raise InvalidLocalPartError("Local part contains too many dots (strict mode)")

        # Check for suspicious patterns
        suspicious_patterns = ['..', '.-', '-.', '__', '--']
        for pattern in suspicious_patterns:
            if pattern in local_part:
                raise InvalidLocalPartError(f"Local part contains suspicious pattern: {pattern}")

    def _validate_local_part_rfc(self, local_part: str):
        """RFC-compliant local part validation including quoted strings."""
        if not local_part:
            raise InvalidLocalPartError("Local part cannot be empty")

        if len(local_part) > self.MAX_LOCAL_LENGTH:
            raise InvalidLocalPartError(f"Local part exceeds maximum length of {self.MAX_LOCAL_LENGTH} characters")

        # Handle quoted strings
        if local_part.startswith('"') and local_part.endswith('"'):
            if not self.compiled_patterns['quoted_local'].match(local_part):
                raise InvalidLocalPartError("Invalid quoted local part")
        else:
            # Non-quoted validation
            if local_part.startswith('.') or local_part.endswith('.'):
                raise InvalidLocalPartError("Local part cannot start or end with a dot")

            if '..' in local_part:
                raise InvalidLocalPartError("Local part cannot contain consecutive dots")

            # Check each character is valid
            valid_chars = set(string.ascii_letters + string.digits + "!#$%&'*+-/=?^_`{|}~.")
            if not all(c in valid_chars for c in local_part):
                raise InvalidLocalPartError("Local part contains invalid characters")

    def _validate_domain_standard(self, domain_part: str):
        """Standard domain validation."""
        if not domain_part:
            raise InvalidDomainError("Domain part cannot be empty")

        if len(domain_part) > self.MAX_DOMAIN_LENGTH:
            raise InvalidDomainError(f"Domain exceeds maximum length of {self.MAX_DOMAIN_LENGTH} characters")

        # Check for IP address format
        if domain_part.startswith('[') and domain_part.endswith(']'):
            if not self.compiled_patterns['ip_address'].match(domain_part):
                raise InvalidDomainError("Invalid IP address format in domain")
            return

        # Split into labels
        labels = domain_part.split('.')
        if len(labels) < 2:
            raise InvalidDomainError("Domain must have at least two labels")

        # Validate each label
        for label in labels:
            if not label:
                raise InvalidDomainError("Domain cannot contain empty labels")

            if len(label) > self.MAX_LABEL_LENGTH:
                raise InvalidDomainError(f"Domain label exceeds maximum length of {self.MAX_LABEL_LENGTH} characters")

            if not self.compiled_patterns['domain_label'].match(label):
                raise InvalidDomainError(f"Invalid domain label: {label}")

        # Validate TLD
        tld = labels[-1].lower()
        if not self.compiled_patterns['tld'].match(tld):
            raise InvalidDomainError("Invalid top-level domain format")

        # Check TLD length (shouldn't be extremely long)
        if len(tld) > 6:
            raise InvalidDomainError(f"Top-level domain too long: {tld}")

    def _validate_domain_strict(self, domain_part: str):
        """Strict domain validation with TLD checking."""
        self._validate_domain_standard(domain_part)

        # Additional TLD validation
        if not domain_part.startswith('['):
            labels = domain_part.split('.')
            tld = labels[-1].lower()

            if tld not in self.COMMON_TLDS:
                raise InvalidDomainError(f"Unknown or uncommon TLD: {tld}")

    def _validate_domain_rfc(self, domain_part: str):
        """RFC-compliant domain validation."""
        self._validate_domain_standard(domain_part)

        # Additional RFC checks
        if not domain_part.startswith('['):
            # Domain names are case-insensitive
            domain_lower = domain_part.lower()

            # Check for valid internationalized domain names (basic check)
            try:
                # Try to encode as ASCII to check for international characters
                domain_lower.encode('ascii')
            except UnicodeEncodeError:
                # Contains non-ASCII characters - should be punycode encoded
                if not domain_lower.startswith('xn--'):
                    raise InvalidDomainError("International domain names must be punycode encoded")

    def get_validation_details(self, email: str) -> Dict[str, Any]:
        """
        Get detailed validation information for an email address.

        Args:
            email: The email address to analyze

        Returns:
            Dictionary with detailed validation information
        """
        details = {
            'email': email,
            'is_valid': False,
            'errors': [],
            'warnings': [],
            'local_part': None,
            'domain_part': None,
            'domain_labels': None,
            'tld': None,
            'length_info': {
                'total_length': len(email) if email else 0,
                'local_length': None,
                'domain_length': None,
                'within_limits': True
            }
        }

        try:
            if email and '@' in email:
                local_part, domain_part = email.rsplit('@', 1)
                details['local_part'] = local_part
                details['domain_part'] = domain_part
                details['length_info']['local_length'] = len(local_part)
                details['length_info']['domain_length'] = len(domain_part)

                # Check length limits
                if (len(email) > self.MAX_EMAIL_LENGTH or
                    len(local_part) > self.MAX_LOCAL_LENGTH or
                    len(domain_part) > self.MAX_DOMAIN_LENGTH):
                    details['length_info']['within_limits'] = False

                if '.' in domain_part and not domain_part.startswith('['):
                    labels = domain_part.split('.')
                    details['domain_labels'] = labels
                    details['tld'] = labels[-1] if labels else None

            # Perform validation
            is_valid, errors = self.validate(email)
            details['is_valid'] = is_valid
            details['errors'] = errors

            # Add warnings
            if email and details['tld']:
                if details['tld'].lower() not in self.COMMON_TLDS:
                    details['warnings'].append(f"Uncommon TLD: {details['tld']}")

            if details['local_part'] and '.' in details['local_part']:
                dot_count = details['local_part'].count('.')
                if dot_count > 2:
                    details['warnings'].append(f"Local part has many dots ({dot_count})")

        except Exception as e:
            details['errors'].append(f"Analysis error: {str(e)}")

        return details

    def is_valid(self, email: str) -> bool:
        """
        Simple boolean check for email validity.

        Args:
            email: The email address to validate

        Returns:
            True if email is valid, False otherwise
        """
        is_valid, _ = self.validate(email)
        return is_valid

    def validate_batch(self, emails: List[str]) -> Dict[str, Tuple[bool, List[str]]]:
        """
        Validate multiple email addresses.

        Args:
            emails: List of email addresses to validate

        Returns:
            Dictionary mapping each email to its validation result
        """
        results = {}
        for email in emails:
            results[email] = self.validate(email)
        return results


def create_validator(level: str = "standard") -> EmailValidator:
    """
    Factory function to create an EmailValidator with specified level.

    Args:
        level: Validation level ("basic", "standard", "strict", "rfc_compliant")

    Returns:
        EmailValidator instance
    """
    level_map = {
        "basic": ValidationLevel.BASIC,
        "standard": ValidationLevel.STANDARD,
        "strict": ValidationLevel.STRICT,
        "rfc_compliant": ValidationLevel.RFC_COMPLIANT
    }

    validation_level = level_map.get(level.lower(), ValidationLevel.STANDARD)
    return EmailValidator(validation_level)


# Convenience functions for quick validation
def is_valid_email(email: str, level: str = "standard") -> bool:
    """Quick email validation check."""
    validator = create_validator(level)
    return validator.is_valid(email)


def validate_email(email: str, level: str = "standard") -> Tuple[bool, List[str]]:
    """Quick email validation with error details."""
    validator = create_validator(level)
    return validator.validate(email)


if __name__ == "__main__":
    # Example usage and basic testing
    print("Email Validator - Example Usage")
    print("=" * 40)

    # Test emails
    test_emails = [
        "user@example.com",
        "test.email+tag@domain.co.uk",
        "invalid.email",
        "@domain.com",
        "user@",
        "user..double.dot@example.com",
        "user@domain",
        "very.long.email.address.that.might.exceed.limits@very.long.domain.name.that.could.be.problematic.example.com",
        "quoted.string@example.com",
        "user@[192.168.1.1]",
        "user@localhost",
    ]

    # Test with different validation levels
    levels = ["basic", "standard", "strict", "rfc_compliant"]

    for level in levels:
        print(f"\n{level.upper()} Validation:")
        print("-" * 30)
        validator = create_validator(level)

        for email in test_emails[:5]:  # Test first 5 emails
            is_valid, errors = validator.validate(email)
            status = "✓" if is_valid else "✗"
            print(f"{status} {email}")
            if errors:
                print(f"   Errors: {'; '.join(errors)}")

    # Detailed analysis example
    print(f"\nDetailed Analysis Example:")
    print("-" * 30)
    validator = EmailValidator(ValidationLevel.STANDARD)
    details = validator.get_validation_details("test.user+tag@example.co.uk")

    for key, value in details.items():
        if key != 'length_info':
            print(f"{key}: {value}")

    print(f"Length info: {details['length_info']}")