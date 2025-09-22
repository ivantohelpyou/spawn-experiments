# URL Validator - Validated Test Development Implementation

A comprehensive URL validator built using Test-Driven Development (TDD) with enhanced test validation methodology. This implementation demonstrates rigorous testing practices by validating each test through deliberate failure scenarios before implementing correct functionality.

## Implementation Approach

This project follows an **enhanced TDD process**:

1. **Write failing test** for specific functionality
2. **Validate test quality** by implementing incorrectly to ensure proper failure detection
3. **Implement correct functionality** to make tests pass
4. **Verify test robustness** through deliberate failure scenarios
5. **Refactor** if needed while maintaining test coverage
6. **Repeat** for comprehensive edge case validation

## Features

### Core Validation Capabilities

- **Format Validation**: URL structure using `urllib.parse`
- **Protocol Validation**: Support for HTTP, HTTPS, FTP, FTPS protocols
- **Domain Validation**: Comprehensive domain name and IP address validation
- **Port Validation**: Valid port range checking (1-65535)
- **Accessibility Checking**: Network reachability using `requests` library
- **Security Analysis**: Detection of malicious patterns and suspicious content

### Security Features

- **Malicious Pattern Detection**: JavaScript injection, XSS attempts
- **URL Encoding Analysis**: Detection of encoded malicious content
- **Suspicious Domain Detection**: URL shorteners, private IPs, localhost
- **Homograph Attack Detection**: International domain names with suspicious characters
- **Port Security**: Detection of dangerous service ports
- **Length Validation**: Protection against buffer overflow attacks

### Edge Case Handling

- **Unicode Support**: International domain names and special characters
- **IPv6 Validation**: Support for IPv6 address formats
- **Boundary Conditions**: Extreme values, empty inputs, very long URLs
- **Error Resilience**: Comprehensive exception handling

## Files

### Core Implementation
- `url_validator.py` - Main URLValidator class with all validation methods
- `test_url_validator.py` - Comprehensive test suite with TDD validation
- `demo.py` - Demonstration script showing validator capabilities

### Key Classes and Methods

#### URLValidator Class

```python
class URLValidator:
    def __init__(self, timeout=5):
        """Initialize validator with optional request timeout."""

    def is_valid_format(self, url):
        """Validate URL format and structure."""

    def is_accessible(self, url):
        """Check if URL is accessible via HTTP request."""

    def is_secure_url(self, url):
        """Analyze URL for security issues and malicious patterns."""

    def validate_url(self, url):
        """Comprehensive validation combining all checks."""
```

## Test Categories

### 1. Format Validation Tests
- Basic valid/invalid URL patterns
- Protocol validation and edge cases
- Domain and IP address validation
- Port number validation

### 2. Accessibility Tests
- Network connectivity simulation
- HTTP status code handling
- Timeout and error scenarios
- Request exception handling

### 3. Security Validation Tests
- Malicious pattern detection
- URL encoding attack detection
- Suspicious domain identification
- Port security analysis
- Homograph attack detection

### 4. Edge Case Tests
- Empty and None value handling
- Unicode and special character support
- Very long URL components
- Unusual IP addresses and ports
- IPv6 address support
- Malformed URL patterns

## TDD Validation Methodology

Each test category demonstrates the enhanced TDD process:

1. **Test Creation**: Write comprehensive tests covering expected functionality
2. **Failure Validation**: Implement methods incorrectly to verify tests catch errors
3. **Correct Implementation**: Implement proper functionality to pass tests
4. **Edge Case Coverage**: Add boundary condition tests with validation
5. **Comprehensive Verification**: Run full test suite to ensure reliability

## Usage Examples

### Basic Format Validation
```python
from url_validator import URLValidator

validator = URLValidator()

# Format validation
is_valid = validator.is_valid_format("https://www.example.com")
print(f"Valid format: {is_valid}")  # True

# Security analysis
is_secure, issues = validator.is_secure_url("javascript:alert('XSS')")
print(f"Secure: {is_secure}")  # False
print(f"Issues: {issues}")     # ['Suspicious pattern detected: javascript:', ...]
```

### Comprehensive Validation
```python
# Full validation including accessibility
result = validator.validate_url("https://www.example.com")
print(result)
# {
#     "url": "https://www.example.com",
#     "format_valid": True,
#     "format_error": None,
#     "accessible": True,  # Requires network access
#     "accessibility_error": "URL is accessible",
#     "overall_valid": True
# }
```

## Test Execution

Run the complete test suite:
```bash
python -m unittest test_url_validator.TestURLValidator -v
```

Run specific test categories:
```bash
# Format validation tests
python -m unittest test_url_validator.TestURLValidator.test_valid_basic_url_format -v

# Security validation tests
python -m unittest test_url_validator.TestURLValidator.test_security_malicious_patterns -v

# Edge case tests
python -m unittest test_url_validator.TestURLValidator.test_edge_case_malformed_urls -v
```

## Dependencies

- **Python 3.6+**
- **urllib.parse** (built-in) - URL parsing and validation
- **requests** - HTTP accessibility checking
- **ipaddress** (built-in) - IP address validation
- **re** (built-in) - Pattern matching
- **unittest.mock** (built-in) - Test mocking for network calls

## Test Coverage

The implementation includes **28 comprehensive test methods** covering:
- ✅ Basic format validation (valid/invalid patterns)
- ✅ Protocol validation and edge cases
- ✅ Network accessibility with mocked responses
- ✅ Security pattern detection
- ✅ Malicious URL encoding detection
- ✅ Edge cases and boundary conditions
- ✅ Error handling and exception scenarios
- ✅ Test validation through deliberate failures

## Key Learning Outcomes

1. **Enhanced TDD Methodology**: Validating test quality through deliberate failures
2. **Comprehensive URL Security**: Understanding various attack vectors and mitigation
3. **Edge Case Engineering**: Handling boundary conditions and unexpected inputs
4. **Test Design Patterns**: Writing robust, maintainable test suites
5. **Library Integration**: Effective use of urllib.parse and requests for URL handling
6. **Security-First Development**: Building validation with security considerations

This implementation demonstrates professional-grade URL validation with emphasis on security, reliability, and comprehensive test coverage using validated TDD practices.