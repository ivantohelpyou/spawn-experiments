"""URL format validation using urllib.parse."""

import urllib.parse
from typing import Optional, List, Tuple
import re

from ..models.result import URLComponents, ValidationResult
from ..models.error import ValidationError, ErrorCode
from ..models.config import ValidationConfig
from ..validators.domain_validator import DomainValidator
from ..validators.ip_validator import IPValidator


class FormatValidator:
    """
    Validates URL format using urllib.parse and custom validation logic.

    This class provides comprehensive URL format validation including:
    - Basic URL structure validation
    - Scheme validation
    - Domain/IP address validation
    - Port number validation
    - Path and query parameter validation
    """

    def __init__(self, config: ValidationConfig):
        """
        Initialize format validator with configuration.

        Args:
            config: Validation configuration
        """
        self.config = config
        self.logger = config.get_logger(__name__)

    def validate(self, url: str) -> ValidationResult:
        """
        Validate URL format.

        Args:
            url: URL string to validate

        Returns:
            ValidationResult with format validation details
        """
        result = ValidationResult(url=url, is_valid=True, is_accessible=False)

        try:
            # Basic input validation
            self._validate_input(url, result)
            if result.has_errors:
                return result

            # Parse URL
            parsed = self._parse_url(url, result)
            if result.has_errors:
                return result

            # Create URL components
            components = self._create_url_components(parsed, result)
            if result.has_errors:
                return result

            result.set_url_components(components)

            # Validate components
            self._validate_scheme(components.scheme, result)
            self._validate_netloc(parsed, components, result)
            self._validate_path(components.path, result)
            self._validate_query(components.query, result)

        except Exception as e:
            self.logger.error(f"Unexpected error during format validation: {e}")
            result.add_error(ValidationError.format_error(
                ErrorCode.MALFORMED_URL,
                f"Unexpected error during validation: {e}",
                {"error": str(e), "type": type(e).__name__}
            ))

        return result

    def _validate_input(self, url: str, result: ValidationResult) -> None:
        """
        Validate basic input requirements.

        Args:
            url: URL string to validate
            result: ValidationResult to update
        """
        if not url:
            result.add_error(ValidationError.format_error(
                ErrorCode.INVALID_STRUCTURE,
                "URL cannot be empty"
            ))
            return

        if not isinstance(url, str):
            result.add_error(ValidationError.format_error(
                ErrorCode.INVALID_STRUCTURE,
                f"URL must be a string, got {type(url).__name__}"
            ))
            return

        # Check length limits
        if len(url) > 2048:  # Common URL length limit
            result.add_warning(f"URL is very long ({len(url)} characters)")

        # Check for null bytes and other problematic characters
        if '\x00' in url:
            result.add_error(ValidationError.format_error(
                ErrorCode.INVALID_ENCODING,
                "URL contains null bytes"
            ))

        # Check for control characters
        if any(ord(c) < 32 for c in url if c != '\t'):
            result.add_error(ValidationError.format_error(
                ErrorCode.INVALID_ENCODING,
                "URL contains control characters"
            ))

    def _parse_url(self, url: str, result: ValidationResult) -> Optional[urllib.parse.ParseResult]:
        """
        Parse URL using urllib.parse.

        Args:
            url: URL string to parse
            result: ValidationResult to update

        Returns:
            ParseResult object or None if parsing failed
        """
        try:
            parsed = urllib.parse.urlparse(url)
            return parsed
        except Exception as e:
            result.add_error(ValidationError.format_error(
                ErrorCode.INVALID_STRUCTURE,
                f"Failed to parse URL: {e}",
                {"error": str(e)}
            ))
            return None

    def _create_url_components(self, parsed: urllib.parse.ParseResult,
                             result: ValidationResult) -> Optional[URLComponents]:
        """
        Create URLComponents from parsed URL.

        Args:
            parsed: ParseResult from urllib.parse
            result: ValidationResult to update

        Returns:
            URLComponents object or None if creation failed
        """
        try:
            components = URLComponents(
                scheme=parsed.scheme.lower(),
                netloc=parsed.netloc,
                path=parsed.path,
                params=parsed.params,
                query=parsed.query,
                fragment=parsed.fragment,
                username=parsed.username,
                password=parsed.password,
                hostname=parsed.hostname,
                port=parsed.port
            )
            return components
        except Exception as e:
            result.add_error(ValidationError.format_error(
                ErrorCode.INVALID_STRUCTURE,
                f"Failed to create URL components: {e}",
                {"error": str(e)}
            ))
            return None

    def _validate_scheme(self, scheme: str, result: ValidationResult) -> None:
        """
        Validate URL scheme.

        Args:
            scheme: URL scheme to validate
            result: ValidationResult to update
        """
        if not scheme:
            result.add_error(ValidationError.format_error(
                ErrorCode.MISSING_SCHEME,
                "URL must have a scheme (e.g., http, https)"
            ))
            return

        if scheme not in self.config.allowed_schemes:
            result.add_error(ValidationError.format_error(
                ErrorCode.UNSUPPORTED_SCHEME,
                f"Unsupported scheme: {scheme}",
                {
                    "scheme": scheme,
                    "allowed_schemes": list(self.config.allowed_schemes)
                }
            ))
            return

        # Validate scheme format
        if not re.match(r'^[a-z][a-z0-9+.-]*$', scheme):
            result.add_error(ValidationError.format_error(
                ErrorCode.UNSUPPORTED_SCHEME,
                f"Invalid scheme format: {scheme}",
                {"scheme": scheme}
            ))

    def _validate_netloc(self, parsed: urllib.parse.ParseResult,
                        components: URLComponents, result: ValidationResult) -> None:
        """
        Validate network location (hostname/IP and port).

        Args:
            parsed: ParseResult from urllib.parse
            components: URLComponents object
            result: ValidationResult to update
        """
        if not components.netloc:
            result.add_error(ValidationError.format_error(
                ErrorCode.INVALID_STRUCTURE,
                "URL must have a network location (hostname or IP address)"
            ))
            return

        # Validate hostname/IP
        hostname = components.hostname
        if hostname:
            self._validate_hostname_or_ip(hostname, result)

        # Validate port
        if components.port is not None:
            self._validate_port(components.port, result)

        # Validate userinfo if present
        if components.username is not None or components.password is not None:
            result.add_warning("URL contains authentication information")

    def _validate_hostname_or_ip(self, hostname: str, result: ValidationResult) -> None:
        """
        Validate hostname or IP address.

        Args:
            hostname: Hostname or IP address to validate
            result: ValidationResult to update
        """
        # Try IP validation first
        is_valid_ip, ip_error, ip_obj = IPValidator.validate(hostname)

        if is_valid_ip:
            # It's a valid IP address
            self._validate_ip_security(ip_obj, result)
        else:
            # Try domain validation
            is_valid_domain, domain_error = DomainValidator.validate(hostname)

            if not is_valid_domain:
                # Neither valid IP nor valid domain
                result.add_error(ValidationError.format_error(
                    ErrorCode.INVALID_DOMAIN,
                    f"Invalid hostname or IP address: {hostname}",
                    {
                        "hostname": hostname,
                        "ip_error": str(ip_error) if ip_error else None,
                        "domain_error": str(domain_error) if domain_error else None
                    }
                ))

    def _validate_ip_security(self, ip_obj, result: ValidationResult) -> None:
        """
        Validate IP address for security concerns.

        Args:
            ip_obj: IP address object
            result: ValidationResult to update
        """
        should_block, reason = IPValidator.should_block(ip_obj, self.config.block_private_ips)

        if should_block:
            result.add_error(ValidationError.security_error(
                ErrorCode.PRIVATE_IP_BLOCKED,
                f"IP address blocked: {reason}",
                {"ip": str(ip_obj), "reason": reason}
            ))

    def _validate_port(self, port: int, result: ValidationResult) -> None:
        """
        Validate port number.

        Args:
            port: Port number to validate
            result: ValidationResult to update
        """
        if not (1 <= port <= 65535):
            result.add_error(ValidationError.format_error(
                ErrorCode.INVALID_PORT,
                f"Invalid port number: {port} (must be 1-65535)",
                {"port": port}
            ))

        # Warn about uncommon ports for HTTP/HTTPS
        common_http_ports = {80, 443, 8080, 8443, 3000, 5000, 8000}
        if port not in common_http_ports:
            result.add_warning(f"Uncommon port number: {port}")

    def _validate_path(self, path: str, result: ValidationResult) -> None:
        """
        Validate URL path component.

        Args:
            path: URL path to validate
            result: ValidationResult to update
        """
        if not path:
            # Empty path is valid (defaults to "/")
            return

        # Check for path traversal attempts
        if '..' in path:
            result.add_warning("URL path contains '..' (potential path traversal)")

        # Check for suspicious patterns
        suspicious_patterns = [
            r'\.\./',
            r'%2e%2e',
            r'%252e%252e',
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                result.add_warning(f"Suspicious pattern in path: {pattern}")

        # Validate URL encoding
        try:
            urllib.parse.unquote(path, errors='strict')
        except UnicodeDecodeError as e:
            result.add_error(ValidationError.format_error(
                ErrorCode.INVALID_ENCODING,
                f"Invalid URL encoding in path: {e}",
                {"path": path, "error": str(e)}
            ))

    def _validate_query(self, query: str, result: ValidationResult) -> None:
        """
        Validate URL query component.

        Args:
            query: URL query string to validate
            result: ValidationResult to update
        """
        if not query:
            return

        # Validate URL encoding in query
        try:
            urllib.parse.unquote(query, errors='strict')
        except UnicodeDecodeError as e:
            result.add_error(ValidationError.format_error(
                ErrorCode.INVALID_ENCODING,
                f"Invalid URL encoding in query: {e}",
                {"query": query, "error": str(e)}
            ))

        # Check query length
        if len(query) > 2048:
            result.add_warning(f"Very long query string ({len(query)} characters)")

        # Parse query parameters for additional validation
        try:
            params = urllib.parse.parse_qs(query)
            # Could add parameter-specific validation here
        except Exception as e:
            result.add_warning(f"Could not parse query parameters: {e}")

    def is_valid_url_format(self, url: str) -> bool:
        """
        Quick check if URL has valid format.

        Args:
            url: URL string to check

        Returns:
            True if URL format is valid
        """
        result = self.validate(url)
        return result.is_valid