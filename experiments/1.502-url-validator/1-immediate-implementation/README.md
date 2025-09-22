# URL Validator

A Python URL validator using `urllib.parse` and `requests` libraries that can check URL formatting and accessibility.

## Features

- **Format Validation**: Checks if URLs are properly formatted using `urllib.parse`
- **Accessibility Testing**: Verifies if URLs are reachable via HTTP requests using `requests`
- **Edge Case Handling**: Handles common edge cases like empty strings, invalid schemes, missing domains
- **Flexible Configuration**: Customizable timeout settings
- **Comprehensive Results**: Returns detailed validation information including parsed URL components

## Usage

### Basic Usage

```python
from url_validator import validate_url

# Validate format and accessibility
result = validate_url("https://www.example.com")
print(f"Valid: {result['is_valid_format']} | Accessible: {result['is_accessible']}")

# Format-only validation (no network request)
result = validate_url("https://www.example.com", check_accessibility=False)
```

### Using the URLValidator Class

```python
from url_validator import URLValidator

# Create validator with custom timeout
validator = URLValidator(timeout=10)

# Check format only
is_valid, error = validator.is_valid_format("https://www.example.com")

# Check accessibility only
is_accessible, message, status_code = validator.is_accessible("https://www.example.com")

# Comprehensive validation
result = validator.validate("https://www.example.com")
```

## Files

- `url_validator.py` - Main implementation with URLValidator class
- `test_validator.py` - Comprehensive test suite
- `demo.py` - Demonstration of various usage patterns
- `requirements.txt` - Python dependencies

## Running Tests

```bash
python3 test_validator.py
```

## Running Demo

```bash
python3 demo.py
```

## Dependencies

- `requests` - For HTTP accessibility testing
- `urllib.parse` - For URL format validation (built-in)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Validation Features

### Format Validation
- Checks for required HTTP/HTTPS scheme
- Validates domain/host presence
- Handles localhost and IP addresses
- Supports port numbers
- Parses URL components (scheme, domain, path, query, fragment)

### Accessibility Testing
- HTTP HEAD requests to check reachability
- Configurable timeout
- Follows redirects
- Returns HTTP status codes
- Handles connection errors, timeouts, and other network issues

### Edge Cases Handled
- Empty or whitespace-only URLs
- Missing schemes or domains
- Unsupported protocols (FTP, etc.)
- Invalid domain formats
- Network connectivity issues
- HTTP error responses (404, 500, etc.)