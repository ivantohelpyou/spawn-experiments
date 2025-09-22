"""
Test-Driven Development tests for URL validator with comprehensive validation.

This module follows enhanced TDD process:
1. Write failing test
2. Validate test by implementing incorrectly
3. Implement correct functionality
4. Verify test quality through deliberate failures
5. Refactor if needed
"""

import unittest
from unittest.mock import patch, Mock
import requests
from url_validator import URLValidator


class TestURLValidator(unittest.TestCase):
    """Test cases for URL validator with comprehensive validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = URLValidator()

    def test_valid_basic_url_format(self):
        """Test basic valid URL format validation."""
        valid_urls = [
            "https://www.example.com",
            "http://example.com",
            "https://subdomain.example.com",
            "https://example.com/path",
            "https://example.com/path?query=value",
            "https://example.com:8080",
        ]

        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(
                    self.validator.is_valid_format(url),
                    f"URL {url} should be valid format"
                )

    def test_invalid_basic_url_format(self):
        """Test invalid URL format validation."""
        invalid_urls = [
            "",  # Empty string
            "not-a-url",  # No protocol
            "://example.com",  # Missing protocol
            "http://",  # No domain
            "http:// example.com",  # Space in URL
            "http://exam ple.com",  # Space in domain
            "http://256.256.256.256",  # Invalid IP
            "http://.com",  # Invalid domain start
            "http://com.",  # Invalid domain end
        ]

        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(
                    self.validator.is_valid_format(url),
                    f"URL {url} should be invalid format"
                )

    def test_protocol_validation(self):
        """Test protocol (scheme) validation with various protocols."""
        valid_protocols = [
            "http://example.com",
            "https://example.com",
            "ftp://example.com",
            "ftps://example.com",
        ]

        for url in valid_protocols:
            with self.subTest(url=url):
                self.assertTrue(
                    self.validator.is_valid_format(url),
                    f"URL {url} should have valid protocol"
                )

    def test_invalid_protocol_validation(self):
        """Test invalid protocol validation."""
        invalid_protocols = [
            "httpx://example.com",  # Invalid protocol
            "file://example.com",   # File protocol not allowed
            "javascript:alert(1)",  # JavaScript protocol
            "data:text/html,<script>alert(1)</script>",  # Data protocol
            "about:blank",          # About protocol
            "chrome://settings",    # Chrome protocol
            "tel:+1234567890",      # Tel protocol
            "mailto:test@example.com",  # Mailto protocol
        ]

        for url in invalid_protocols:
            with self.subTest(url=url):
                self.assertFalse(
                    self.validator.is_valid_format(url),
                    f"URL {url} should have invalid protocol"
                )

    def test_protocol_edge_cases(self):
        """Test protocol edge cases and malformed protocols."""
        edge_cases = [
            "HTTP://example.com",   # Uppercase protocol
            "HTTPS://example.com",  # Uppercase protocol
            "Http://example.com",   # Mixed case protocol
            "http:/example.com",    # Missing second slash
            "http:///example.com",  # Triple slash
            "://example.com",       # Missing protocol entirely
            "http//example.com",    # Missing colon
        ]

        # Test uppercase/mixed case (should be valid)
        self.assertTrue(self.validator.is_valid_format("HTTP://example.com"))
        self.assertTrue(self.validator.is_valid_format("HTTPS://example.com"))
        self.assertTrue(self.validator.is_valid_format("Http://example.com"))

        # Test malformed protocols (should be invalid)
        malformed = [
            "http:/example.com",
            "http:///example.com",
            "://example.com",
            "http//example.com",
        ]

        for url in malformed:
            with self.subTest(url=url):
                self.assertFalse(
                    self.validator.is_valid_format(url),
                    f"URL {url} should be invalid due to malformed protocol"
                )

    @patch('url_validator.requests.head')
    def test_accessibility_success(self, mock_head):
        """Test successful URL accessibility checking."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        accessible, message = self.validator.is_accessible("https://example.com")

        self.assertTrue(accessible)
        self.assertEqual(message, "URL is accessible")
        mock_head.assert_called_once_with(
            "https://example.com",
            timeout=5,
            allow_redirects=True
        )

    @patch('url_validator.requests.head')
    def test_accessibility_http_errors(self, mock_head):
        """Test HTTP error responses during accessibility checking."""
        test_cases = [
            (404, "HTTP error: 404"),
            (500, "HTTP error: 500"),
            (403, "HTTP error: 403"),
            (401, "HTTP error: 401"),
        ]

        for status_code, expected_message in test_cases:
            with self.subTest(status_code=status_code):
                mock_response = Mock()
                mock_response.status_code = status_code
                mock_head.return_value = mock_response

                accessible, message = self.validator.is_accessible("https://example.com")

                self.assertFalse(accessible)
                self.assertEqual(message, expected_message)

    @patch('url_validator.requests.head')
    def test_accessibility_network_errors(self, mock_head):
        """Test network error scenarios during accessibility checking."""
        test_cases = [
            (requests.exceptions.ConnectionError(), "Connection error: Unable to connect to the server"),
            (requests.exceptions.Timeout(), "Timeout error: Request timed out after 5 seconds"),
            (requests.exceptions.TooManyRedirects(), "Too many redirects"),
            (requests.exceptions.InvalidURL(), "Invalid URL for requests"),
            (requests.exceptions.InvalidSchema(), "Invalid URL schema"),
            (requests.exceptions.MissingSchema(), "Missing URL schema"),
        ]

        for exception, expected_message in test_cases:
            with self.subTest(exception=type(exception).__name__):
                mock_head.side_effect = exception

                accessible, message = self.validator.is_accessible("https://example.com")

                self.assertFalse(accessible)
                self.assertEqual(message, expected_message)

    @patch('url_validator.requests.head')
    def test_accessibility_custom_timeout(self, mock_head):
        """Test accessibility checking with custom timeout."""
        validator = URLValidator(timeout=10)

        mock_head.side_effect = requests.exceptions.Timeout()

        accessible, message = validator.is_accessible("https://example.com")

        self.assertFalse(accessible)
        self.assertEqual(message, "Timeout error: Request timed out after 10 seconds")

    def test_accessibility_invalid_format(self):
        """Test accessibility checking with invalid URL format."""
        accessible, message = self.validator.is_accessible("not-a-url")

        self.assertFalse(accessible)
        self.assertEqual(message, "Invalid URL format")

    @patch('url_validator.requests.head')
    def test_comprehensive_validation(self, mock_head):
        """Test comprehensive URL validation combining format and accessibility."""
        # Test valid format and accessible URL
        mock_response = Mock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        result = self.validator.validate_url("https://example.com")

        expected = {
            "url": "https://example.com",
            "format_valid": True,
            "format_error": None,
            "accessible": True,
            "accessibility_error": "URL is accessible",
            "overall_valid": True
        }

        self.assertEqual(result, expected)

        # Test invalid format
        result = self.validator.validate_url("not-a-url")

        expected = {
            "url": "not-a-url",
            "format_valid": False,
            "format_error": "Invalid URL format",
            "accessible": False,
            "accessibility_error": None,
            "overall_valid": False
        }

        self.assertEqual(result, expected)

        # Test valid format but inaccessible URL
        mock_head.side_effect = requests.exceptions.ConnectionError()

        result = self.validator.validate_url("https://nonexistent.example.com")

        expected = {
            "url": "https://nonexistent.example.com",
            "format_valid": True,
            "format_error": None,
            "accessible": False,
            "accessibility_error": "Connection error: Unable to connect to the server",
            "overall_valid": False
        }

        self.assertEqual(result, expected)

    def test_security_safe_urls(self):
        """Test that safe URLs pass security validation."""
        safe_urls = [
            "https://www.example.com",
            "http://example.com/path",
            "https://subdomain.example.com:8080",
            "ftp://ftp.example.com",
        ]

        for url in safe_urls:
            with self.subTest(url=url):
                is_secure, issues = self.validator.is_secure_url(url)
                self.assertTrue(is_secure, f"URL {url} should be secure")
                self.assertEqual(issues, [])

    def test_security_malicious_patterns(self):
        """Test detection of malicious patterns in URLs."""
        malicious_urls = [
            ("javascript:alert(1)", ["Suspicious pattern detected: javascript:", "Potentially dangerous protocol: javascript"]),
            ("data:text/html,<script>alert(1)</script>", ["Suspicious pattern detected: data:", "Suspicious pattern detected: <script", "Potentially dangerous protocol: data"]),
            ("https://example.com?onclick=alert(1)", ["Suspicious pattern detected: onclick="]),
            ("https://example.com?eval(document.cookie)", ["Suspicious pattern detected: eval(", "Suspicious pattern detected: document.cookie"]),
            ("vbscript:msgbox('XSS')", ["Suspicious pattern detected: vbscript:", "Potentially dangerous protocol: vbscript"]),
        ]

        for url, expected_issues in malicious_urls:
            with self.subTest(url=url):
                is_secure, issues = self.validator.is_secure_url(url)
                self.assertFalse(is_secure, f"URL {url} should not be secure")
                for expected_issue in expected_issues:
                    self.assertIn(expected_issue, issues)

    def test_security_url_encoding_attacks(self):
        """Test detection of malicious patterns hidden in URL encoding."""
        encoded_urls = [
            "https://example.com?param=%3Cscript%3Ealert(1)%3C/script%3E",  # <script>alert(1)</script>
            "https://example.com?param=javascript%3Aalert(1)",  # javascript:alert(1)
        ]

        for url in encoded_urls:
            with self.subTest(url=url):
                is_secure, issues = self.validator.is_secure_url(url)
                self.assertFalse(is_secure, f"URL {url} should not be secure")
                self.assertTrue(any("Suspicious pattern in decoded URL" in issue for issue in issues))

    def test_security_suspicious_domains(self):
        """Test detection of suspicious domain patterns."""
        suspicious_urls = [
            ("http://localhost/test", "Suspicious domain pattern: localhost"),
            ("http://127.0.0.1/test", "Private/local IP address detected: 127.0.0.1"),
            ("https://bit.ly/test", "Suspicious domain pattern: bit.ly"),
            ("https://tinyurl.com/test", "Suspicious domain pattern: tinyurl.com"),
            ("http://10.0.0.1/test", "Private/local IP address detected: 10.0.0.1"),
        ]

        for url, expected_issue in suspicious_urls:
            with self.subTest(url=url):
                is_secure, issues = self.validator.is_secure_url(url)
                self.assertFalse(is_secure, f"URL {url} should not be secure")
                self.assertIn(expected_issue, issues)

    def test_security_dangerous_ports(self):
        """Test detection of dangerous ports."""
        dangerous_port_urls = [
            ("http://example.com:22", "Potentially dangerous port: 22"),  # SSH
            ("http://example.com:3389", "Potentially dangerous port: 3389"),  # RDP
            ("http://example.com:1433", "Potentially dangerous port: 1433"),  # SQL Server
            ("http://example.com:3306", "Potentially dangerous port: 3306"),  # MySQL
        ]

        for url, expected_issue in dangerous_port_urls:
            with self.subTest(url=url):
                is_secure, issues = self.validator.is_secure_url(url)
                self.assertFalse(is_secure, f"URL {url} should not be secure")
                self.assertIn(expected_issue, issues)

    def test_security_long_urls(self):
        """Test detection of excessively long URLs."""
        long_url = "https://example.com/" + "a" * 2100  # Exceeds 2048 character limit

        is_secure, issues = self.validator.is_secure_url(long_url)

        self.assertFalse(is_secure)
        self.assertIn("URL length exceeds safe limits (2048 characters)", issues)

    def test_security_homograph_attacks(self):
        """Test detection of potential homograph attacks."""
        # Using Cyrillic characters that look similar to Latin
        homograph_url = "https://еxample.com"  # 'е' is Cyrillic, not Latin 'e'

        is_secure, issues = self.validator.is_secure_url(homograph_url)

        self.assertFalse(is_secure)
        self.assertIn("International domain detected - possible homograph attack", issues)

    def test_security_invalid_format(self):
        """Test security validation with invalid URL format."""
        is_secure, issues = self.validator.is_secure_url("not-a-url")

        self.assertFalse(is_secure)
        self.assertEqual(issues, ["Invalid URL format"])

    def test_edge_case_empty_and_none_values(self):
        """Test edge cases with empty and None values."""
        edge_cases = [
            None,
            "",
            " ",
            "   ",
            "\t",
            "\n",
        ]

        for value in edge_cases:
            with self.subTest(value=repr(value)):
                if value is None:
                    # None should cause an exception or be handled gracefully
                    try:
                        result = self.validator.is_valid_format(value)
                        self.assertFalse(result)
                    except (TypeError, AttributeError):
                        pass  # This is acceptable behavior for None
                else:
                    self.assertFalse(self.validator.is_valid_format(value))

    def test_edge_case_unicode_and_special_characters(self):
        """Test URLs with Unicode and special characters."""
        unicode_urls = [
            "https://例え.テスト",  # Japanese domain
            "https://müller.de",   # German umlaut
            "https://café.com",    # French accent
            "https://москва.рф",   # Russian Cyrillic
            "https://example.com/路径",  # Chinese path
            "https://example.com/café/ñoño",  # Mixed special chars
        ]

        for url in unicode_urls:
            with self.subTest(url=url):
                # These might be valid or invalid depending on implementation
                # But should not crash
                try:
                    result = self.validator.is_valid_format(url)
                    self.assertIsInstance(result, bool)
                except Exception as e:
                    self.fail(f"URL {url} caused exception: {e}")

    def test_edge_case_very_long_components(self):
        """Test URLs with very long components."""
        # Very long domain
        long_domain = "a" * 253 + ".com"  # Max domain length
        long_domain_url = f"https://{long_domain}"

        # Very long path
        long_path = "a" * 1000
        long_path_url = f"https://example.com/{long_path}"

        # Very long query
        long_query = "param=" + "a" * 1000
        long_query_url = f"https://example.com?{long_query}"

        test_cases = [
            (long_domain_url, "long domain"),
            (long_path_url, "long path"),
            (long_query_url, "long query"),
        ]

        for url, description in test_cases:
            with self.subTest(description=description):
                try:
                    result = self.validator.is_valid_format(url)
                    self.assertIsInstance(result, bool)
                except Exception as e:
                    self.fail(f"URL with {description} caused exception: {e}")

    def test_edge_case_unusual_ports(self):
        """Test URLs with unusual port numbers."""
        port_cases = [
            ("https://example.com:0", False),     # Port 0
            ("https://example.com:1", True),      # Port 1
            ("https://example.com:65535", True),  # Max valid port
            ("https://example.com:65536", False), # Port too high
            ("https://example.com:99999", False), # Port way too high
            ("https://example.com:80", True),     # Standard HTTP
            ("https://example.com:443", True),    # Standard HTTPS
        ]

        for url, should_be_valid in port_cases:
            with self.subTest(url=url):
                result = self.validator.is_valid_format(url)
                if should_be_valid:
                    self.assertTrue(result, f"URL {url} should be valid")
                else:
                    self.assertFalse(result, f"URL {url} should be invalid")

    def test_edge_case_unusual_ip_addresses(self):
        """Test URLs with unusual IP addresses."""
        ip_cases = [
            ("http://0.0.0.0", True),      # All zeros
            ("http://255.255.255.255", True),  # All max values
            ("http://192.168.1.1", True),   # Private IP
            ("http://10.0.0.1", True),      # Private IP
            ("http://172.16.0.1", True),    # Private IP
            ("http://169.254.1.1", True),   # Link-local
            ("http://224.0.0.1", True),     # Multicast
            ("http://1.2.3", False),        # Incomplete IP
            ("http://1.2.3.4.5", False),    # Too many octets
            ("http://300.1.2.3", False),    # Invalid octet
        ]

        for url, should_be_valid in ip_cases:
            with self.subTest(url=url):
                result = self.validator.is_valid_format(url)
                if should_be_valid:
                    self.assertTrue(result, f"URL {url} should be valid")
                else:
                    self.assertFalse(result, f"URL {url} should be invalid")

    def test_edge_case_ipv6_addresses(self):
        """Test URLs with IPv6 addresses."""
        ipv6_cases = [
            "http://[::1]",                    # Loopback
            "http://[2001:db8::1]",           # Standard IPv6
            "http://[::ffff:192.0.2.1]",      # IPv4-mapped IPv6
            "http://[2001:db8::1]:8080",      # IPv6 with port
            "http://[invalid:ipv6]",          # Invalid IPv6
        ]

        for url in ipv6_cases:
            with self.subTest(url=url):
                # IPv6 support may vary, but should not crash
                try:
                    result = self.validator.is_valid_format(url)
                    self.assertIsInstance(result, bool)
                except Exception as e:
                    self.fail(f"IPv6 URL {url} caused exception: {e}")

    def test_edge_case_unusual_schemes(self):
        """Test URLs with unusual but potentially valid schemes."""
        scheme_cases = [
            ("HTTP://example.com", True),     # Uppercase
            ("hTTp://example.com", True),     # Mixed case
            ("h://example.com", False),       # Too short
            ("verylongscheme://example.com", False),  # Not in our allowed list
        ]

        for url, should_be_valid in scheme_cases:
            with self.subTest(url=url):
                result = self.validator.is_valid_format(url)
                if should_be_valid:
                    self.assertTrue(result, f"URL {url} should be valid")
                else:
                    self.assertFalse(result, f"URL {url} should be invalid")

    def test_edge_case_malformed_urls(self):
        """Test various malformed URL patterns."""
        malformed_urls = [
            "http://",                    # No domain
            "http:///",                   # Triple slash, no domain
            "http://.com",               # Domain starts with dot
            "http://com.",               # Domain ends with dot
            "http://exa..mple.com",      # Double dots in domain
            "http://example..com",       # Double dots before TLD
            "http://example.c",          # Single char TLD
            "http://example.",           # Missing TLD
            "http://-example.com",       # Domain starts with hyphen
            "http://example-.com",       # Domain ends with hyphen
            "http://ex ample.com",       # Space in domain
            "http://example.com:abc",    # Non-numeric port
            "http://example.com:-80",    # Negative port
        ]

        for url in malformed_urls:
            with self.subTest(url=url):
                self.assertFalse(
                    self.validator.is_valid_format(url),
                    f"Malformed URL {url} should be invalid"
                )

    @patch('url_validator.requests.head')
    def test_edge_case_accessibility_edge_cases(self, mock_head):
        """Test accessibility checking edge cases."""
        # Test 3xx redirect codes (should be considered accessible)
        redirect_codes = [301, 302, 303, 307, 308]
        for code in redirect_codes:
            with self.subTest(status_code=code):
                mock_response = Mock()
                mock_response.status_code = code
                mock_head.return_value = mock_response

                accessible, message = self.validator.is_accessible("https://example.com")
                self.assertTrue(accessible, f"Status {code} should be accessible")

        # Test boundary status codes
        mock_response = Mock()
        mock_response.status_code = 399  # Last 3xx code
        mock_head.return_value = mock_response

        accessible, message = self.validator.is_accessible("https://example.com")
        self.assertTrue(accessible, "Status 399 should be accessible")

        mock_response.status_code = 400  # First 4xx code
        mock_head.return_value = mock_response

        accessible, message = self.validator.is_accessible("https://example.com")
        self.assertFalse(accessible, "Status 400 should not be accessible")


if __name__ == "__main__":
    unittest.main()