#!/usr/bin/env python3
"""
URL Validator using urllib.parse and requests libraries
"""

import urllib.parse
import requests
from typing import Tuple, Optional
import socket


class URLValidator:
    """A class to validate URLs for proper formatting and accessibility."""

    def __init__(self, timeout: int = 5):
        """
        Initialize the URL validator.

        Args:
            timeout: Timeout for HTTP requests in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        # Set a reasonable user agent to avoid bot detection
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })

    def is_valid_format(self, url: str) -> Tuple[bool, str]:
        """
        Check if URL has proper format using urllib.parse.

        Args:
            url: The URL string to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not url or not isinstance(url, str):
            return False, "URL must be a non-empty string"

        url = url.strip()
        if not url:
            return False, "URL cannot be empty or whitespace only"

        try:
            parsed = urllib.parse.urlparse(url)

            # Check if scheme exists and is http/https
            if not parsed.scheme:
                return False, "URL missing scheme (http/https)"

            if parsed.scheme.lower() not in ['http', 'https']:
                return False, f"Unsupported scheme: {parsed.scheme}"

            # Check if netloc (domain) exists
            if not parsed.netloc:
                return False, "URL missing domain/host"

            # Check for valid domain format
            # Allow localhost, IPs, and domains with ports
            netloc_host = parsed.netloc.split(':')[0]  # Remove port if present
            if ('.' not in netloc_host and
                netloc_host not in ['localhost'] and
                not netloc_host.replace('.', '').replace(':', '').isdigit()):  # Basic IP check
                return False, "Invalid domain format"

            return True, ""

        except Exception as e:
            return False, f"URL parsing error: {str(e)}"

    def is_accessible(self, url: str) -> Tuple[bool, str, Optional[int]]:
        """
        Check if URL is accessible via HTTP request.

        Args:
            url: The URL to check accessibility

        Returns:
            Tuple of (is_accessible, message, status_code)
        """
        try:
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)

            if response.status_code < 400:
                return True, f"URL accessible (HTTP {response.status_code})", response.status_code
            else:
                return False, f"HTTP error {response.status_code}", response.status_code

        except requests.exceptions.ConnectionError:
            return False, "Connection failed - host unreachable", None
        except requests.exceptions.Timeout:
            return False, f"Request timeout after {self.timeout} seconds", None
        except requests.exceptions.TooManyRedirects:
            return False, "Too many redirects", None
        except requests.exceptions.RequestException as e:
            return False, f"Request error: {str(e)}", None
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", None

    def validate(self, url: str, check_accessibility: bool = True) -> dict:
        """
        Comprehensive URL validation.

        Args:
            url: The URL to validate
            check_accessibility: Whether to check if URL is accessible

        Returns:
            Dictionary with validation results
        """
        result = {
            'url': url,
            'is_valid_format': False,
            'is_accessible': None,
            'format_error': '',
            'accessibility_error': '',
            'status_code': None,
            'parsed_components': None
        }

        # Check format first
        is_valid_format, format_error = self.is_valid_format(url)
        result['is_valid_format'] = is_valid_format
        result['format_error'] = format_error

        if is_valid_format:
            # Parse URL components for additional info
            parsed = urllib.parse.urlparse(url)
            result['parsed_components'] = {
                'scheme': parsed.scheme,
                'netloc': parsed.netloc,
                'path': parsed.path,
                'params': parsed.params,
                'query': parsed.query,
                'fragment': parsed.fragment
            }

            # Check accessibility if requested and format is valid
            if check_accessibility:
                is_accessible, accessibility_msg, status_code = self.is_accessible(url)
                result['is_accessible'] = is_accessible
                result['accessibility_error'] = accessibility_msg if not is_accessible else ''
                result['status_code'] = status_code

        return result


def validate_url(url: str, check_accessibility: bool = True, timeout: int = 5) -> dict:
    """
    Convenience function to validate a single URL.

    Args:
        url: The URL to validate
        check_accessibility: Whether to check if URL is accessible
        timeout: Timeout for HTTP requests in seconds

    Returns:
        Dictionary with validation results
    """
    validator = URLValidator(timeout=timeout)
    return validator.validate(url, check_accessibility)


if __name__ == "__main__":
    # Example usage and testing
    test_urls = [
        "https://www.google.com",
        "http://httpbin.org/status/200",
        "https://nonexistent-domain-12345.com",
        "invalid-url",
        "ftp://example.com",
        "https://",
        "",
        "https://httpbin.org/status/404",
        "http://localhost:8080",
        "https://www.github.com/path/to/repo?param=value#section"
    ]

    print("URL Validator Test Results")
    print("=" * 50)

    for url in test_urls:
        print(f"\nTesting: {url}")
        result = validate_url(url)

        print(f"  Format Valid: {result['is_valid_format']}")
        if result['format_error']:
            print(f"  Format Error: {result['format_error']}")

        if result['is_accessible'] is not None:
            print(f"  Accessible: {result['is_accessible']}")
            if result['status_code']:
                print(f"  Status Code: {result['status_code']}")
            if result['accessibility_error']:
                print(f"  Access Error: {result['accessibility_error']}")

        if result['parsed_components']:
            components = result['parsed_components']
            print(f"  Scheme: {components['scheme']}")
            print(f"  Domain: {components['netloc']}")
            if components['path']:
                print(f"  Path: {components['path']}")
            if components['query']:
                print(f"  Query: {components['query']}")