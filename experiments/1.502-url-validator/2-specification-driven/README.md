# URL Validator - Specification-Driven Implementation

A comprehensive URL validation library for Python that validates URLs for format correctness and accessibility using `urllib.parse` and `requests` libraries.

## Overview

This implementation follows a specification-driven development approach, with comprehensive requirements analysis, technical specifications, and implementation planning completed before any code development.

## Features

### Core Functionality
- **Format Validation**: Uses `urllib.parse` for RFC-compliant URL structure validation
- **Accessibility Testing**: Uses `requests` for HTTP/HTTPS connectivity verification
- **Batch Processing**: Concurrent validation of multiple URLs
- **Comprehensive Error Handling**: Detailed error categorization and reporting
- **Security Features**: SSRF protection, input sanitization, and rate limiting

### Validation Capabilities
- URL scheme validation (HTTP, HTTPS, FTP, etc.)
- Domain name and IP address validation (IPv4/IPv6)
- Port number validation
- URL encoding and special character handling
- Internationalized domain name (IDN) support
- SSL certificate validation
- Redirect following with configurable limits

### Security Features
- SSRF (Server-Side Request Forgery) protection
- Private IP address blocking
- Input sanitization and injection prevention
- Rate limiting for request management
- Malicious pattern detection

## Installation

```bash
# Install the package
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"

# Install with test dependencies only
pip install -e ".[test]"
```

## Quick Start

### Basic Usage

```python
from url_validator import validate_url, URLValidator

# Validate a single URL
result = validate_url("https://example.com")
print(f"Valid: {result.is_valid}, Accessible: {result.is_accessible}")

# Format validation only
result = validate_url("https://example.com", check_accessibility=False)
print(f"Valid format: {result.is_valid}")

# Batch validation
from url_validator import validate_urls

urls = ["https://example.com", "https://google.com", "invalid-url"]
results = validate_urls(urls)

for result in results:
    print(f"{result.url}: Valid={result.is_valid}, Accessible={result.is_accessible}")
```

### Advanced Usage

```python
from url_validator import URLValidator, ValidationConfig

# Custom configuration
config = ValidationConfig(
    timeout=30,
    max_redirects=10,
    verify_ssl=False,
    block_private_ips=True,
    allowed_schemes={"https"}
)

# Use with context manager
with URLValidator(config) as validator:
    result = validator.validate("https://example.com")

    # Batch processing with custom worker count
    results = validator.validate_batch(urls, max_workers=5)
```

### Configuration Options

```python
from url_validator import ValidationConfig

# Predefined configurations
permissive_config = ValidationConfig.create_permissive()  # For development
strict_config = ValidationConfig.create_strict()         # For production
fast_config = ValidationConfig.create_fast()            # For performance

# Custom configuration
config = ValidationConfig(
    timeout=10,                    # Request timeout in seconds
    max_redirects=5,              # Maximum redirects to follow
    verify_ssl=True,              # SSL certificate verification
    user_agent="MyApp/1.0",       # Custom User-Agent
    allowed_schemes={"http", "https"},  # Allowed URL schemes
    block_private_ips=False,      # Block private IP addresses
    retry_attempts=3,             # Retry attempts for failed requests
    retry_delay=1.0,              # Delay between retries
    custom_headers={"X-App": "MyApp"}  # Custom headers
)
```

## Command Line Interface

The package includes a comprehensive CLI tool:

```bash
# Validate a single URL
url-validator https://example.com

# Validate multiple URLs
url-validator --batch https://example.com https://google.com

# Validate URLs from file
url-validator -f urls.txt

# Format validation only
url-validator https://example.com --no-accessibility

# Custom output format
url-validator https://example.com -o json
url-validator --batch url1 url2 url3 -o csv

# Verbose output
url-validator https://example.com -v

# Custom configuration
url-validator https://example.com --timeout 30 --max-redirects 10

# Security options
url-validator https://example.com --block-private-ips --no-ssl-verify

# Save output to file
url-validator -f urls.txt -o json --output-file results.json
```

## Error Handling

The library provides comprehensive error handling with detailed error codes:

```python
from url_validator import validate_url
from url_validator.models.error import ErrorCode

result = validate_url("invalid-url")

if not result.is_valid:
    for error in result.errors:
        print(f"Error [{error.code}]: {error.message}")
        print(f"Category: {error.category.value}")

        # Check specific error types
        if error.code == ErrorCode.INVALID_DOMAIN:
            print("Domain name is invalid")
        elif error.code == ErrorCode.MISSING_SCHEME:
            print("URL is missing a scheme")
```

### Error Categories

- **Format Errors**: Invalid URL structure, scheme, domain, etc.
- **Network Errors**: Connection timeouts, DNS failures, SSL errors
- **Security Errors**: SSRF attempts, private IP blocks, malicious patterns
- **Configuration Errors**: Invalid configuration parameters
- **System Errors**: Unexpected system-level errors

## Security Features

### SSRF Protection

```python
from url_validator.security import SSRFProtection

ssrf = SSRFProtection(block_private_ips=True)
is_safe, error = ssrf.check_url("https://127.0.0.1")

if not is_safe:
    print(f"Security issue: {error.message}")
```

### Input Sanitization

```python
from url_validator.security import InputSanitizer

sanitizer = InputSanitizer()
clean_url, error = sanitizer.sanitize("  https://example.com  ")

if error:
    print(f"Sanitization error: {error.message}")
else:
    print(f"Clean URL: {clean_url}")
```

### Rate Limiting

```python
from url_validator.security import RateLimiter, RateLimitConfig

config = RateLimitConfig(requests_per_minute=100, requests_per_hour=1000)
limiter = RateLimiter(config)

allowed, error = limiter.check_rate_limit("client_id")
if not allowed:
    print(f"Rate limit exceeded: {error.message}")
```

## Result Objects

### ValidationResult

```python
result = validate_url("https://example.com")

# Basic properties
print(f"URL: {result.url}")
print(f"Valid: {result.is_valid}")
print(f"Accessible: {result.is_accessible}")
print(f"Duration: {result.duration}s")

# Error information
print(f"Errors: {len(result.errors)}")
print(f"Warnings: {len(result.warnings)}")
print(f"Error codes: {result.error_codes}")

# URL components (if valid)
if result.url_components:
    print(f"Scheme: {result.url_components.scheme}")
    print(f"Hostname: {result.url_components.hostname}")
    print(f"Port: {result.url_components.port}")

# Accessibility information
if result.accessibility_result:
    print(f"Status code: {result.accessibility_result.status_code}")
    print(f"Response time: {result.accessibility_result.response_time}s")
    print(f"Redirects: {result.accessibility_result.redirect_count}")

# Export to different formats
print(result.to_json(indent=2))
print(result.to_dict())
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=url_validator --cov-report=html

# Run specific test categories
pytest tests/test_format_validator.py
pytest tests/test_accessibility_checker.py
pytest tests/test_security/

# Run performance tests
pytest tests/performance/
```

## Development

### Project Structure

```
url_validator/
├── __init__.py                 # Package initialization
├── models/                     # Data models
│   ├── config.py              # Configuration management
│   ├── result.py              # Result objects
│   └── error.py               # Error handling
├── core/                      # Core validation logic
│   ├── format_validator.py   # URL format validation
│   ├── accessibility_checker.py  # Accessibility testing
│   └── validator.py          # Main validator class
├── validators/                # Specialized validators
│   ├── domain_validator.py   # Domain name validation
│   └── ip_validator.py       # IP address validation
├── security/                  # Security features
│   ├── ssrf_protection.py    # SSRF prevention
│   ├── input_sanitizer.py    # Input sanitization
│   └── rate_limiter.py       # Rate limiting
├── cli/                       # Command line interface
│   ├── main.py               # CLI entry point
│   └── formatter.py          # Output formatting
└── utils/                     # Utility functions
```

### Code Quality

The project follows strict code quality standards:

- **PEP 8 compliance**: Enforced with Black formatter
- **Type hints**: Required for all public interfaces
- **Documentation**: Comprehensive docstrings for all classes and methods
- **Test coverage**: Minimum 90% coverage requirement

### Running Quality Checks

```bash
# Format code
black url_validator/

# Type checking
mypy url_validator/

# Linting
flake8 url_validator/

# Run all quality checks
make quality  # If Makefile is provided
```

## Performance

### Benchmarks

The library is designed for high performance:

- **Single URL validation**: < 5 seconds for responsive sites
- **Batch processing**: 100 URLs in < 60 seconds
- **Memory usage**: < 50MB for typical workloads
- **Concurrency**: Configurable thread pool for optimal performance

### Optimization Tips

```python
# Use format-only validation when accessibility isn't needed
result = validate_url(url, check_accessibility=False)

# Optimize batch processing with appropriate worker count
results = validate_urls(urls, max_workers=20)

# Use fast configuration for performance-critical applications
config = ValidationConfig.create_fast()
validator = URLValidator(config)
```

## Documentation

### Comprehensive Documentation

- [Requirements Analysis](docs/requirements-analysis.md) - Detailed functional requirements
- [Technical Specifications](docs/technical-specifications.md) - System architecture and design
- [Testing Requirements](docs/testing-requirements.md) - Testing strategy and acceptance criteria
- [Implementation Plan](docs/implementation-plan.md) - Development phases and guidelines

### API Reference

Complete API documentation is available in the `docs/` directory and can be generated using Sphinx:

```bash
# Generate documentation
cd docs/
make html

# View documentation
open _build/html/index.html
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the coding standards
4. Add tests for new functionality
5. Ensure all tests pass and coverage is maintained
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Changelog

### Version 1.0.0
- Initial specification-driven implementation
- Comprehensive URL format validation using urllib.parse
- Accessibility checking using requests
- Security features including SSRF protection
- Command line interface
- Extensive test suite with 90%+ coverage

## Support

For bug reports, feature requests, and questions:

- GitHub Issues: [Project Issues](https://github.com/urlvalidator/url-validator/issues)
- Documentation: [Full Documentation](https://url-validator.readthedocs.io/)
- Email: contact@urlvalidator.com

## Acknowledgments

This implementation was developed following specification-driven development principles, with comprehensive planning and documentation completed before implementation. The approach ensures high code quality, maintainability, and adherence to requirements.