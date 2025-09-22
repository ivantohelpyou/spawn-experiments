import unittest
from url_validator import URLValidator


class TestURLValidator(unittest.TestCase):

    def setUp(self):
        self.validator = URLValidator()

    def test_valid_basic_http_url(self):
        """Test that a basic HTTP URL is considered valid"""
        result = self.validator.is_valid("http://example.com")
        self.assertTrue(result)

    def test_invalid_url_without_protocol(self):
        """Test that a URL without protocol is considered invalid"""
        result = self.validator.is_valid("example.com")
        self.assertFalse(result)

    def test_valid_https_url(self):
        """Test that HTTPS URLs are considered valid"""
        result = self.validator.is_valid("https://example.com")
        self.assertTrue(result)

    def test_invalid_ftp_protocol(self):
        """Test that FTP protocol is considered invalid"""
        result = self.validator.is_valid("ftp://example.com")
        self.assertFalse(result)

    def test_url_accessibility_check(self):
        """Test that URL accessibility can be verified"""
        # This should check if the URL is actually accessible
        result = self.validator.is_accessible("https://httpbin.org/status/200")
        self.assertTrue(result)

    def test_inaccessible_url_returns_false(self):
        """Test that inaccessible URLs return False"""
        result = self.validator.is_accessible("https://httpbin.org/status/404")
        self.assertFalse(result)

    def test_empty_string_is_invalid(self):
        """Test that empty string is considered invalid"""
        result = self.validator.is_valid("")
        self.assertFalse(result)

    def test_none_value_is_invalid(self):
        """Test that None value is considered invalid"""
        result = self.validator.is_valid(None)
        self.assertFalse(result)

    def test_url_with_netloc_required(self):
        """Test that URL must have a network location"""
        result = self.validator.is_valid("http://")
        self.assertFalse(result)

    def test_unreachable_url_returns_false(self):
        """Test that unreachable URLs return False"""
        # Using a URL that should cause a network error
        result = self.validator.is_accessible("http://this-domain-should-not-exist-12345.com")
        self.assertFalse(result)

    def test_complete_validation_valid_and_accessible(self):
        """Test complete validation for valid and accessible URL"""
        result = self.validator.validate_completely("https://httpbin.org/status/200")
        self.assertTrue(result['valid'])
        self.assertTrue(result['accessible'])

    def test_complete_validation_invalid_url(self):
        """Test complete validation for invalid URL"""
        result = self.validator.validate_completely("invalid-url")
        self.assertFalse(result['valid'])
        self.assertFalse(result['accessible'])


if __name__ == '__main__':
    unittest.main()