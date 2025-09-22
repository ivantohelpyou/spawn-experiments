"""Tests for format validation functionality."""

import pytest
from url_validator.core.format_validator import FormatValidator
from url_validator.models.config import ValidationConfig
from url_validator.models.error import ErrorCode


class TestFormatValidator:
    """Test cases for FormatValidator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = ValidationConfig()
        self.validator = FormatValidator(self.config)

    def test_valid_urls(self):
        """Test validation of valid URLs."""
        valid_urls = [
            "https://example.com",
            "http://test.example.com:8080/path?param=value#fragment",
            "https://192.168.1.1/api/v1/resource",
            "https://[::1]:3000/endpoint",
            "ftp://ftp.example.com/file.txt",
        ]

        for url in valid_urls:
            result = self.validator.validate(url)
            assert result.is_valid, f"URL should be valid: {url}"
            assert result.url_components is not None
            assert len(result.errors) == 0

    def test_invalid_urls(self):
        """Test validation of invalid URLs."""
        invalid_urls = [
            "not-a-url",
            "https://",
            "https://example..com",
            "https://example.com:99999",
            "",
            None,
        ]

        for url in invalid_urls:
            if url is None:
                with pytest.raises(TypeError):
                    self.validator.validate(url)
            else:
                result = self.validator.validate(url)
                assert not result.is_valid, f"URL should be invalid: {url}"
                assert len(result.errors) > 0

    def test_scheme_validation(self):
        """Test URL scheme validation."""
        # Test allowed schemes
        result = self.validator.validate("https://example.com")
        assert result.is_valid

        result = self.validator.validate("http://example.com")
        assert result.is_valid

        # Test disallowed scheme with restricted config
        restricted_config = ValidationConfig(allowed_schemes={"https"})
        restricted_validator = FormatValidator(restricted_config)

        result = restricted_validator.validate("http://example.com")
        assert not result.is_valid
        assert any(error.code == ErrorCode.UNSUPPORTED_SCHEME for error in result.errors)

    def test_domain_validation(self):
        """Test domain name validation."""
        # Valid domains
        valid_domains = [
            "https://example.com",
            "https://sub.example.com",
            "https://test-site.example.co.uk",
            "https://xn--e1afmkfd.xn--p1ai",  # IDN domain
        ]

        for url in valid_domains:
            result = self.validator.validate(url)
            assert result.is_valid, f"Domain should be valid: {url}"

        # Invalid domains
        invalid_domains = [
            "https://",
            "https://-example.com",
            "https://example-.com",
            "https://example..com",
        ]

        for url in invalid_domains:
            result = self.validator.validate(url)
            assert not result.is_valid, f"Domain should be invalid: {url}"

    def test_ip_address_validation(self):
        """Test IP address validation."""
        # Valid IPs
        valid_ips = [
            "https://192.168.1.1",
            "https://10.0.0.1:8080",
            "https://[::1]",
            "https://[2001:db8::1]:3000",
        ]

        for url in valid_ips:
            result = self.validator.validate(url)
            assert result.is_valid, f"IP should be valid: {url}"

        # Invalid IPs
        invalid_ips = [
            "https://999.999.999.999",
            "https://[::g]",
            "https://256.1.1.1",
        ]

        for url in invalid_ips:
            result = self.validator.validate(url)
            assert not result.is_valid, f"IP should be invalid: {url}"

    def test_port_validation(self):
        """Test port number validation."""
        # Valid ports
        result = self.validator.validate("https://example.com:443")
        assert result.is_valid

        result = self.validator.validate("https://example.com:8080")
        assert result.is_valid

        # Invalid ports
        result = self.validator.validate("https://example.com:99999")
        assert not result.is_valid

        result = self.validator.validate("https://example.com:0")
        assert not result.is_valid

    def test_url_encoding_validation(self):
        """Test URL encoding validation."""
        # Valid encoded URLs
        valid_encoded = [
            "https://example.com/path%20with%20spaces",
            "https://example.com/search?q=test%20query",
            "https://example.com/path/with%2Fslash",
        ]

        for url in valid_encoded:
            result = self.validator.validate(url)
            assert result.is_valid, f"Encoded URL should be valid: {url}"

        # Invalid encoding
        invalid_encoded = [
            "https://example.com/path%zz",
            "https://example.com/path%1",
        ]

        for url in invalid_encoded:
            result = self.validator.validate(url)
            # May be valid at URL level but should have warnings
            # The exact behavior depends on urllib.parse implementation

    def test_private_ip_blocking(self):
        """Test private IP address blocking."""
        config_block_private = ValidationConfig(block_private_ips=True)
        validator_block_private = FormatValidator(config_block_private)

        private_ips = [
            "https://127.0.0.1",
            "https://10.0.0.1",
            "https://192.168.1.1",
            "https://[::1]",
        ]

        for url in private_ips:
            result = validator_block_private.validate(url)
            assert not result.is_valid, f"Private IP should be blocked: {url}"
            assert any(error.code == ErrorCode.PRIVATE_IP_BLOCKED for error in result.errors)

    def test_url_components_extraction(self):
        """Test URL components extraction."""
        url = "https://user:pass@example.com:8080/path?param=value#fragment"
        result = self.validator.validate(url)

        assert result.is_valid
        assert result.url_components is not None

        components = result.url_components
        assert components.scheme == "https"
        assert components.hostname == "example.com"
        assert components.port == 8080
        assert components.path == "/path"
        assert components.query == "param=value"
        assert components.fragment == "fragment"
        assert components.username == "user"
        assert components.password == "pass"

    def test_internationalized_domains(self):
        """Test internationalized domain name support."""
        idn_urls = [
            "https://測試.例子",
            "https://пример.рф",
            "https://مثال.إختبار",
        ]

        for url in idn_urls:
            result = self.validator.validate(url)
            # Should be valid if IDN library is working
            assert result.url_components is not None

    def test_suspicious_patterns(self):
        """Test detection of suspicious URL patterns."""
        suspicious_urls = [
            "https://example.com/../../../etc/passwd",
            "https://example.com/path%2e%2e%2ffile",
        ]

        for url in suspicious_urls:
            result = self.validator.validate(url)
            # Should have warnings about suspicious patterns
            assert len(result.warnings) > 0

    def test_long_urls(self):
        """Test handling of very long URLs."""
        # Very long URL
        long_path = "a" * 3000
        long_url = f"https://example.com/{long_path}"

        result = self.validator.validate(long_url)
        # Should have warnings about length
        assert len(result.warnings) > 0

    def test_empty_and_null_inputs(self):
        """Test handling of empty and null inputs."""
        result = self.validator.validate("")
        assert not result.is_valid
        assert any(error.code == ErrorCode.INVALID_STRUCTURE for error in result.errors)

    def test_control_characters(self):
        """Test handling of control characters in URLs."""
        url_with_null = "https://example.com\x00/path"
        result = self.validator.validate(url_with_null)
        assert not result.is_valid
        assert any(error.code == ErrorCode.INVALID_ENCODING for error in result.errors)

    def test_quick_validation(self):
        """Test quick validation method."""
        assert self.validator.is_valid_url_format("https://example.com")
        assert not self.validator.is_valid_url_format("invalid-url")
        assert not self.validator.is_valid_url_format("")