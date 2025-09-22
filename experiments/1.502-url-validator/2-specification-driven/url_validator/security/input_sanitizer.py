"""Input sanitization utilities for URL validation."""

import re
import unicodedata
from typing import Optional, Tuple
import urllib.parse

from ..models.error import ValidationError, ErrorCode


class InputSanitizer:
    """
    Provides input sanitization for URL validation to prevent injection attacks.

    This class implements various sanitization techniques to clean and validate
    URL inputs before processing.
    """

    # Maximum reasonable URL length
    MAX_URL_LENGTH = 2048

    # Dangerous URL schemes that should be blocked
    DANGEROUS_SCHEMES = {
        "javascript",
        "vbscript",
        "data",
        "file",
        "ftp",
        "ftps",
        "gopher",
        "ldap",
        "ldaps",
        "telnet",
        "ssh",
        "sftp",
    }

    # Suspicious patterns that might indicate injection attempts
    INJECTION_PATTERNS = [
        r"<script",
        r"javascript:",
        r"vbscript:",
        r"onload=",
        r"onerror=",
        r"onclick=",
        r"eval\(",
        r"expression\(",
        r"url\(",
        r"@import",
        r"\\x[0-9a-fA-F]{2}",  # Hex encoding
        r"%[0-9a-fA-F]{2}%[0-9a-fA-F]{2}",  # Double URL encoding
    ]

    def __init__(self, max_length: int = MAX_URL_LENGTH,
                 allow_dangerous_schemes: bool = False):
        """
        Initialize input sanitizer.

        Args:
            max_length: Maximum allowed URL length
            allow_dangerous_schemes: Whether to allow dangerous URL schemes
        """
        self.max_length = max_length
        self.allow_dangerous_schemes = allow_dangerous_schemes

        # Compile injection patterns
        self.injection_pattern = re.compile("|".join(self.INJECTION_PATTERNS), re.IGNORECASE)

    def sanitize(self, url: str) -> Tuple[str, Optional[ValidationError]]:
        """
        Sanitize URL input.

        Args:
            url: URL string to sanitize

        Returns:
            Tuple of (sanitized_url, error_if_any)
        """
        if not isinstance(url, str):
            return "", ValidationError.format_error(
                ErrorCode.INVALID_STRUCTURE,
                f"URL must be a string, got {type(url).__name__}"
            )

        # Step 1: Basic cleaning
        sanitized = self._basic_clean(url)

        # Step 2: Length validation
        if len(sanitized) > self.max_length:
            return "", ValidationError.format_error(
                ErrorCode.INVALID_STRUCTURE,
                f"URL too long: {len(sanitized)} > {self.max_length}",
                {"length": len(sanitized), "max_length": self.max_length}
            )

        # Step 3: Check for dangerous patterns
        error = self._check_dangerous_patterns(sanitized)
        if error:
            return "", error

        # Step 4: Normalize encoding
        sanitized, error = self._normalize_encoding(sanitized)
        if error:
            return "", error

        # Step 5: Final validation
        error = self._final_validation(sanitized)
        if error:
            return "", error

        return sanitized, None

    def _basic_clean(self, url: str) -> str:
        """
        Perform basic cleaning of URL.

        Args:
            url: URL to clean

        Returns:
            Cleaned URL
        """
        # Strip whitespace
        url = url.strip()

        # Remove null bytes and other control characters
        url = "".join(char for char in url if ord(char) >= 32 or char in "\t")

        # Normalize Unicode characters
        url = unicodedata.normalize('NFKC', url)

        return url

    def _check_dangerous_patterns(self, url: str) -> Optional[ValidationError]:
        """
        Check for dangerous patterns in URL.

        Args:
            url: URL to check

        Returns:
            ValidationError if dangerous pattern found, None otherwise
        """
        # Check for injection patterns
        if self.injection_pattern.search(url):
            return ValidationError.security_error(
                ErrorCode.MALICIOUS_PATTERN,
                "URL contains potentially malicious pattern",
                {"url": url[:100]}  # Limit logged URL length
            )

        # Check scheme if not allowing dangerous schemes
        if not self.allow_dangerous_schemes:
            try:
                parsed = urllib.parse.urlparse(url)
                if parsed.scheme.lower() in self.DANGEROUS_SCHEMES:
                    return ValidationError.security_error(
                        ErrorCode.MALICIOUS_PATTERN,
                        f"Dangerous URL scheme: {parsed.scheme}",
                        {"scheme": parsed.scheme}
                    )
            except Exception:
                # If we can't parse it, we'll catch it later
                pass

        return None

    def _normalize_encoding(self, url: str) -> Tuple[str, Optional[ValidationError]]:
        """
        Normalize URL encoding.

        Args:
            url: URL to normalize

        Returns:
            Tuple of (normalized_url, error_if_any)
        """
        try:
            # Parse and reconstruct URL to normalize encoding
            parsed = urllib.parse.urlparse(url)

            # Check for double encoding or other suspicious encoding
            if self._has_suspicious_encoding(url):
                return "", ValidationError.security_error(
                    ErrorCode.MALICIOUS_PATTERN,
                    "Suspicious URL encoding detected",
                    {"url": url[:100]}
                )

            # Reconstruct URL with normalized components
            normalized = urllib.parse.urlunparse(parsed)
            return normalized, None

        except Exception as e:
            return "", ValidationError.format_error(
                ErrorCode.INVALID_ENCODING,
                f"Failed to normalize URL encoding: {e}",
                {"error": str(e)}
            )

    def _has_suspicious_encoding(self, url: str) -> bool:
        """
        Check for suspicious URL encoding patterns.

        Args:
            url: URL to check

        Returns:
            True if suspicious encoding detected
        """
        # Check for double URL encoding
        if re.search(r"%25[0-9a-fA-F]{2}", url):
            return True

        # Check for overlong UTF-8 sequences
        if re.search(r"%[cC][0-1]%[8-9a-bA-B][0-9a-fA-F]", url):
            return True

        # Check for null byte encoding variants
        null_encodings = ["%00", "%u0000", "\\x00", "\\0"]
        for encoding in null_encodings:
            if encoding.lower() in url.lower():
                return True

        return False

    def _final_validation(self, url: str) -> Optional[ValidationError]:
        """
        Perform final validation checks.

        Args:
            url: URL to validate

        Returns:
            ValidationError if validation fails, None otherwise
        """
        # Check for empty URL after sanitization
        if not url:
            return ValidationError.format_error(
                ErrorCode.INVALID_STRUCTURE,
                "URL is empty after sanitization"
            )

        # Check for minimum length
        if len(url) < 3:  # Minimum: "a:b"
            return ValidationError.format_error(
                ErrorCode.INVALID_STRUCTURE,
                "URL too short after sanitization"
            )

        # Check for basic URL structure
        if ":" not in url:
            return ValidationError.format_error(
                ErrorCode.MISSING_SCHEME,
                "URL missing scheme separator after sanitization"
            )

        return None

    def validate_input(self, url: str) -> Tuple[bool, Optional[ValidationError]]:
        """
        Validate input without modification.

        Args:
            url: URL to validate

        Returns:
            Tuple of (is_valid, error_if_invalid)
        """
        sanitized, error = self.sanitize(url)
        if error:
            return False, error

        # Additional check: ensure sanitization didn't change the URL significantly
        if sanitized != url.strip():
            # If sanitization changed the URL, it might have been malicious
            return False, ValidationError.security_error(
                ErrorCode.MALICIOUS_PATTERN,
                "URL required sanitization (potentially malicious)",
                {"original": url[:100], "sanitized": sanitized[:100]}
            )

        return True, None

    def is_safe_input(self, url: str) -> bool:
        """
        Quick check if input is safe.

        Args:
            url: URL to check

        Returns:
            True if input appears safe
        """
        is_valid, _ = self.validate_input(url)
        return is_valid

    def escape_for_output(self, url: str) -> str:
        """
        Escape URL for safe output (e.g., in HTML context).

        Args:
            url: URL to escape

        Returns:
            Escaped URL safe for output
        """
        # Basic HTML escaping
        url = url.replace("&", "&amp;")
        url = url.replace("<", "&lt;")
        url = url.replace(">", "&gt;")
        url = url.replace('"', "&quot;")
        url = url.replace("'", "&#x27;")

        return url

    def get_clean_domain(self, url: str) -> Optional[str]:
        """
        Extract and clean domain from URL.

        Args:
            url: URL to extract domain from

        Returns:
            Clean domain or None if invalid
        """
        try:
            sanitized, error = self.sanitize(url)
            if error:
                return None

            parsed = urllib.parse.urlparse(sanitized)
            if parsed.hostname:
                return parsed.hostname.lower()

        except Exception:
            pass

        return None

    def remove_sensitive_params(self, url: str, sensitive_params: Optional[list] = None) -> str:
        """
        Remove sensitive parameters from URL.

        Args:
            url: URL to clean
            sensitive_params: List of parameter names to remove

        Returns:
            URL with sensitive parameters removed
        """
        if sensitive_params is None:
            sensitive_params = [
                "password", "passwd", "pwd", "pass",
                "token", "key", "secret", "auth",
                "api_key", "apikey", "access_token",
                "session", "sid", "sessid"
            ]

        try:
            parsed = urllib.parse.urlparse(url)
            if not parsed.query:
                return url

            # Parse query parameters
            params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)

            # Remove sensitive parameters
            for param in list(params.keys()):
                if param.lower() in [sp.lower() for sp in sensitive_params]:
                    del params[param]

            # Reconstruct query string
            new_query = urllib.parse.urlencode(params, doseq=True)

            # Reconstruct URL
            new_parsed = parsed._replace(query=new_query)
            return urllib.parse.urlunparse(new_parsed)

        except Exception:
            # If anything goes wrong, return original URL
            return url