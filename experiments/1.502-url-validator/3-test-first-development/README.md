# URL Validator - Test-Driven Development

This URL validator was built using strict Test-Driven Development (TDD) following the Red-Green-Refactor cycle.

## TDD Process Followed

### 1. Red-Green-Refactor Cycles

Each feature was implemented following these steps:
1. **RED**: Write a failing test first
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Improve code structure while keeping tests passing

### 2. Development Phases

#### Phase 1: Basic URL Format Validation
- **RED**: Test for basic HTTP URL validation
- **GREEN**: Minimal implementation (always return True)
- **RED**: Test for invalid URL without protocol
- **GREEN**: Implement basic urlparse validation

#### Phase 2: Protocol Checking
- **RED**: Tests for HTTPS support and FTP rejection
- **GREEN**: Restrict to HTTP/HTTPS protocols only

#### Phase 3: Accessibility Verification
- **RED**: Test for URL accessibility using requests
- **GREEN**: Implement HTTP HEAD request with status code checking

#### Phase 4: Edge Cases and Error Handling
- **RED**: Tests for empty strings, None values, missing netloc
- **GREEN**: Enhanced validation with netloc checking
- **RED**: Test for network errors
- **GREEN**: Exception handling already covered this

#### Phase 5: Refactoring
- Added constants for allowed schemes and timeout
- Improved documentation with docstrings
- Added comprehensive validation method
- Maintained all existing functionality

## Features

### Format Validation (`is_valid`)
- Checks URL format using `urllib.parse`
- Validates HTTP/HTTPS protocols only
- Requires network location (netloc)
- Handles edge cases (None, empty strings)

### Accessibility Checking (`is_accessible`)
- Uses `requests.head()` for efficiency
- 5-second timeout
- Considers status codes < 400 as accessible
- Handles network errors gracefully

### Complete Validation (`validate_completely`)
- Combines format and accessibility checking
- Returns structured results
- Only checks accessibility for valid URLs

## Technologies Used

- **urllib.parse**: URL parsing and validation
- **requests**: HTTP accessibility checking
- **unittest**: Test framework

## Files

- `url_validator.py`: Main implementation
- `test_url_validator.py`: Comprehensive test suite (12 tests)
- `demo.py`: Demonstration script
- `README.md`: This documentation

## Running the Code

```bash
# Run tests
python test_url_validator.py

# Run demonstration
python demo.py
```

## Test Coverage

The test suite covers:
- Basic HTTP/HTTPS URL validation
- Protocol restriction (rejects FTP, etc.)
- Accessibility verification
- Edge cases (empty strings, None values)
- Network error handling
- Complete validation workflow

All tests follow TDD principles: written before implementation and focused on specific behaviors.