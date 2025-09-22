"""Domain name validation utilities."""

import re
import idna
from typing import Optional, Tuple

from ..models.error import ValidationError, ErrorCode


class DomainValidator:
    """
    Validates domain names according to RFC standards.

    This class provides comprehensive domain name validation including:
    - Basic format validation
    - Length validation
    - Character set validation
    - Internationalized domain name (IDN) support
    """

    # Domain name pattern (basic validation)
    DOMAIN_PATTERN = re.compile(
        r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?'
        r'(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    )

    # Maximum lengths according to RFC standards
    MAX_DOMAIN_LENGTH = 253
    MAX_LABEL_LENGTH = 63

    @classmethod
    def validate(cls, domain: str) -> Tuple[bool, Optional[ValidationError]]:
        """
        Validate a domain name.

        Args:
            domain: Domain name to validate

        Returns:
            Tuple of (is_valid, error_if_invalid)
        """
        if not domain:
            return False, ValidationError.format_error(
                ErrorCode.INVALID_DOMAIN,
                "Domain name cannot be empty"
            )

        # Check overall length
        if len(domain) > cls.MAX_DOMAIN_LENGTH:
            return False, ValidationError.format_error(
                ErrorCode.INVALID_DOMAIN,
                f"Domain name too long: {len(domain)} > {cls.MAX_DOMAIN_LENGTH}",
                {"length": len(domain), "max_length": cls.MAX_DOMAIN_LENGTH}
            )

        # Handle internationalized domain names
        try:
            ascii_domain = idna.encode(domain).decode('ascii')
        except (idna.core.IDNAError, UnicodeError) as e:
            return False, ValidationError.format_error(
                ErrorCode.INVALID_DOMAIN,
                f"Invalid internationalized domain name: {e}",
                {"original_domain": domain, "idna_error": str(e)}
            )

        # Validate ASCII domain
        return cls._validate_ascii_domain(ascii_domain, domain)

    @classmethod
    def _validate_ascii_domain(cls, ascii_domain: str, original_domain: str) -> Tuple[bool, Optional[ValidationError]]:
        """
        Validate ASCII domain name.

        Args:
            ascii_domain: ASCII representation of domain
            original_domain: Original domain (for error reporting)

        Returns:
            Tuple of (is_valid, error_if_invalid)
        """
        # Check basic pattern
        if not cls.DOMAIN_PATTERN.match(ascii_domain):
            return False, ValidationError.format_error(
                ErrorCode.INVALID_DOMAIN,
                f"Invalid domain format: {original_domain}",
                {"domain": original_domain, "ascii_domain": ascii_domain}
            )

        # Validate individual labels
        labels = ascii_domain.split('.')

        for label in labels:
            if not label:
                return False, ValidationError.format_error(
                    ErrorCode.INVALID_DOMAIN,
                    f"Empty label in domain: {original_domain}",
                    {"domain": original_domain}
                )

            if len(label) > cls.MAX_LABEL_LENGTH:
                return False, ValidationError.format_error(
                    ErrorCode.INVALID_DOMAIN,
                    f"Label too long in domain: {label} ({len(label)} > {cls.MAX_LABEL_LENGTH})",
                    {"domain": original_domain, "label": label, "length": len(label)}
                )

            # Check for invalid characters in label
            if not re.match(r'^[a-zA-Z0-9\-]+$', label):
                return False, ValidationError.format_error(
                    ErrorCode.INVALID_DOMAIN,
                    f"Invalid characters in domain label: {label}",
                    {"domain": original_domain, "label": label}
                )

            # Labels cannot start or end with hyphen
            if label.startswith('-') or label.endswith('-'):
                return False, ValidationError.format_error(
                    ErrorCode.INVALID_DOMAIN,
                    f"Domain label cannot start or end with hyphen: {label}",
                    {"domain": original_domain, "label": label}
                )

        # Additional validations
        return cls._validate_domain_semantics(ascii_domain, original_domain)

    @classmethod
    def _validate_domain_semantics(cls, ascii_domain: str, original_domain: str) -> Tuple[bool, Optional[ValidationError]]:
        """
        Validate domain semantics and special cases.

        Args:
            ascii_domain: ASCII representation of domain
            original_domain: Original domain (for error reporting)

        Returns:
            Tuple of (is_valid, error_if_invalid)
        """
        # Domain must have at least one dot for valid FQDN
        # (single-word domains like 'localhost' are allowed but warned about)
        if '.' not in ascii_domain:
            # This is often localhost or similar, which is technically valid
            # but we might want to warn about it
            pass

        # Check for consecutive dots
        if '..' in ascii_domain:
            return False, ValidationError.format_error(
                ErrorCode.INVALID_DOMAIN,
                f"Consecutive dots not allowed in domain: {original_domain}",
                {"domain": original_domain}
            )

        # Cannot start or end with dot
        if ascii_domain.startswith('.') or ascii_domain.endswith('.'):
            return False, ValidationError.format_error(
                ErrorCode.INVALID_DOMAIN,
                f"Domain cannot start or end with dot: {original_domain}",
                {"domain": original_domain}
            )

        # All validations passed
        return True, None

    @classmethod
    def normalize(cls, domain: str) -> str:
        """
        Normalize a domain name.

        Args:
            domain: Domain name to normalize

        Returns:
            Normalized domain name

        Raises:
            ValidationError: If domain cannot be normalized
        """
        if not domain:
            raise ValidationError.format_error(
                ErrorCode.INVALID_DOMAIN,
                "Cannot normalize empty domain"
            )

        # Convert to lowercase
        domain = domain.lower().strip()

        # Handle IDN
        try:
            # This will convert IDN to ASCII and back to ensure proper encoding
            ascii_domain = idna.encode(domain).decode('ascii')
            return idna.decode(ascii_domain)
        except (idna.core.IDNAError, UnicodeError) as e:
            raise ValidationError.format_error(
                ErrorCode.INVALID_DOMAIN,
                f"Cannot normalize internationalized domain: {e}",
                {"domain": domain, "error": str(e)}
            )

    @classmethod
    def is_international(cls, domain: str) -> bool:
        """
        Check if domain contains international characters.

        Args:
            domain: Domain name to check

        Returns:
            True if domain contains non-ASCII characters
        """
        try:
            domain.encode('ascii')
            return False
        except UnicodeEncodeError:
            return True

    @classmethod
    def to_ascii(cls, domain: str) -> str:
        """
        Convert domain to ASCII representation.

        Args:
            domain: Domain name to convert

        Returns:
            ASCII representation of domain

        Raises:
            ValidationError: If domain cannot be converted
        """
        try:
            return idna.encode(domain).decode('ascii')
        except (idna.core.IDNAError, UnicodeError) as e:
            raise ValidationError.format_error(
                ErrorCode.INVALID_DOMAIN,
                f"Cannot convert domain to ASCII: {e}",
                {"domain": domain, "error": str(e)}
            )