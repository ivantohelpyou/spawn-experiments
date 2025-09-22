"""
URL validator implementation using urllib.parse and requests libraries.

This module provides comprehensive URL validation including:
- Format validation
- Protocol handling
- Accessibility checking
- Security validation
"""

from urllib.parse import urlparse
import requests
import re
import ipaddress


class URLValidator:
    """URL validator with comprehensive validation capabilities."""

    def __init__(self, timeout=5):
        """Initialize URL validator.

        Args:
            timeout (int): Timeout for network requests in seconds
        """
        self.timeout = timeout

    def is_valid_format(self, url):
        """
        Validate URL format.

        Args:
            url (str): URL to validate

        Returns:
            bool: True if URL format is valid, False otherwise
        """
        # Correct implementation using urllib.parse and comprehensive validation
        if not url or not isinstance(url, str):
            return False

        # Remove leading/trailing whitespace
        url = url.strip()

        if not url:
            return False

        try:
            # Parse the URL
            parsed = urlparse(url)

            # Check if scheme (protocol) exists and is valid (case-insensitive)
            if not parsed.scheme or parsed.scheme.lower() not in ['http', 'https', 'ftp', 'ftps']:
                return False

            # Check if netloc (domain) exists
            if not parsed.netloc:
                return False

            # Check for spaces in URL (which should not be present)
            if ' ' in url:
                return False

            # Validate port if present
            if parsed.port is not None:
                if not (1 <= parsed.port <= 65535):
                    return False

            # Validate domain/hostname
            hostname = parsed.hostname
            if hostname:
                # Check for invalid domain patterns
                if hostname.startswith('.') or hostname.endswith('.'):
                    return False

                # Check if it's an IP address
                try:
                    ip = ipaddress.ip_address(hostname)
                    # Validate IPv4 ranges (IPv6 will be handled by ipaddress)
                    if isinstance(ip, ipaddress.IPv4Address):
                        octets = str(ip).split('.')
                        for octet in octets:
                            if int(octet) > 255:
                                return False
                except (ipaddress.AddressValueError, ValueError):
                    # Not an IP address, check if it looks like an invalid IP
                    if re.match(r'^\d+\.\d+\.\d+\.\d+$', hostname):
                        # It looks like an IP but was rejected by ipaddress module
                        return False

                    # Validate as domain name
                    # Domain must have at least one dot and valid TLD
                    if '.' not in hostname:
                        return False

                    # Check for consecutive dots
                    if '..' in hostname:
                        return False

                    # Split into parts and validate each
                    parts = hostname.split('.')

                    # Must have at least 2 parts (domain.tld)
                    if len(parts) < 2:
                        return False

                    # TLD (last part) must be at least 2 characters
                    tld = parts[-1]
                    if len(tld) < 2:
                        return False

                    # Validate each part
                    for part in parts:
                        if not part:  # Empty part
                            return False
                        if part.startswith('-') or part.endswith('-'):
                            return False
                        if not re.match(r'^[a-zA-Z0-9\-]+$', part):
                            return False

            return True

        except Exception:
            return False

    def is_accessible(self, url):
        """
        Check if URL is accessible via HTTP request.

        Args:
            url (str): URL to check accessibility

        Returns:
            tuple: (bool, str) - (is_accessible, error_message)
        """
        # First validate format
        if not self.is_valid_format(url):
            return False, "Invalid URL format"

        try:
            # Make a HEAD request first (lighter than GET)
            response = requests.head(url, timeout=self.timeout, allow_redirects=True)

            # Check if status code indicates success
            if 200 <= response.status_code < 400:
                return True, "URL is accessible"
            else:
                return False, f"HTTP error: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return False, "Connection error: Unable to connect to the server"
        except requests.exceptions.Timeout:
            return False, f"Timeout error: Request timed out after {self.timeout} seconds"
        except requests.exceptions.TooManyRedirects:
            return False, "Too many redirects"
        except requests.exceptions.InvalidURL:
            return False, "Invalid URL for requests"
        except requests.exceptions.InvalidSchema:
            return False, "Invalid URL schema"
        except requests.exceptions.MissingSchema:
            return False, "Missing URL schema"
        except requests.exceptions.RequestException as e:
            return False, f"Request error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def validate_url(self, url):
        """
        Comprehensive URL validation including format and accessibility.

        Args:
            url (str): URL to validate

        Returns:
            dict: Validation results with format and accessibility status
        """
        result = {
            "url": url,
            "format_valid": False,
            "format_error": None,
            "accessible": False,
            "accessibility_error": None,
            "overall_valid": False
        }

        # Check format
        result["format_valid"] = self.is_valid_format(url)
        if not result["format_valid"]:
            result["format_error"] = "Invalid URL format"
            return result

        # Check accessibility
        result["accessible"], result["accessibility_error"] = self.is_accessible(url)

        # Overall validation
        result["overall_valid"] = result["format_valid"] and result["accessible"]

        return result

    def is_secure_url(self, url):
        """
        Check URL for security issues and malicious patterns.

        Args:
            url (str): URL to check for security issues

        Returns:
            tuple: (bool, list) - (is_secure, list_of_security_issues)
        """
        # Note: We don't immediately reject based on format validation
        # as we want to analyze security issues even in malformed URLs

        security_issues = []

        # Check if format is valid according to our format validator
        format_valid = self.is_valid_format(url)
        if not format_valid:
            security_issues.append("Invalid URL format")

        parsed = urlparse(url)

        # Check for suspicious patterns
        suspicious_patterns = [
            'javascript:',
            'data:',
            'vbscript:',
            '<script',
            '</script>',
            'onload=',
            'onerror=',
            'onclick=',
            'onmouseover=',
            'eval(',
            'alert(',
            'document.cookie',
            'window.location',
        ]

        url_lower = url.lower()
        for pattern in suspicious_patterns:
            if pattern in url_lower:
                security_issues.append(f"Suspicious pattern detected: {pattern}")

        # Check for potentially dangerous protocols
        dangerous_protocols = ['javascript', 'data', 'vbscript', 'file', 'about']
        if parsed.scheme.lower() in dangerous_protocols:
            security_issues.append(f"Potentially dangerous protocol: {parsed.scheme}")

        # Check for URL encoding that might hide malicious content
        if '%' in url:
            import urllib.parse
            try:
                decoded = urllib.parse.unquote(url)
                if decoded != url:
                    # Check decoded URL for suspicious patterns
                    decoded_lower = decoded.lower()
                    for pattern in suspicious_patterns:
                        if pattern in decoded_lower:
                            security_issues.append(f"Suspicious pattern in decoded URL: {pattern}")
            except Exception:
                security_issues.append("Invalid URL encoding detected")

        # Check for excessive length (potential buffer overflow or DoS)
        if len(url) > 2048:
            security_issues.append("URL length exceeds safe limits (2048 characters)")

        # Check for suspicious domains
        if parsed.hostname:
            hostname = parsed.hostname.lower()

            # Check for IP addresses that might be used to bypass domain restrictions
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', hostname):
                # Additional check for private/local IP ranges
                try:
                    ip = ipaddress.ip_address(hostname)
                    if ip.is_private or ip.is_loopback or ip.is_link_local:
                        security_issues.append(f"Private/local IP address detected: {hostname}")
                except ValueError:
                    pass

            # Check for suspicious domain patterns
            suspicious_domains = [
                'localhost',
                '127.0.0.1',
                '0.0.0.0',
                '::1',
                'bit.ly',
                'tinyurl.com',
                't.co',
            ]

            for suspicious in suspicious_domains:
                if suspicious in hostname:
                    security_issues.append(f"Suspicious domain pattern: {suspicious}")

            # Check for homograph attacks (similar looking characters)
            if any(ord(char) > 127 for char in hostname):
                security_issues.append("International domain detected - possible homograph attack")

        # Check for suspicious ports
        if parsed.port:
            dangerous_ports = [21, 22, 23, 25, 53, 135, 139, 445, 1433, 1521, 3306, 3389, 5432]
            if parsed.port in dangerous_ports:
                security_issues.append(f"Potentially dangerous port: {parsed.port}")

        is_secure = len(security_issues) == 0
        return is_secure, security_issues