# Email Validator Specifications

## 1. Core Functional Requirements

The email validator function shall:
- Accept a string input representing an email address
- Return a boolean value (True for valid, False for invalid)
- Validate email format according to commonly accepted patterns
- Handle empty strings and None inputs gracefully

## 2. Valid Email Format Patterns (Examples)

### Basic Valid Formats
- `user@domain.com`
- `test@example.org`
- `admin@site.net`

### Valid with Numbers and Hyphens
- `user123@domain.com`
- `test-user@example.org`
- `admin.user@my-site.net`

### Valid with Dots in Local Part
- `first.last@domain.com`
- `user.name.ext@example.org`

### Valid with Plus Signs (commonly used for email aliases)
- `user+tag@domain.com`
- `test+123@example.org`

### Valid with Underscores
- `user_name@domain.com`
- `test_user@example.org`

## 3. Invalid Email Format Patterns (Examples)

### Missing Components
- `@domain.com` (no local part)
- `user@` (no domain)
- `user` (no @ symbol)
- `user@domain` (no TLD)

### Invalid Characters
- `user space@domain.com` (space in local part)
- `user@domain .com` (space in domain)
- `user@domain..com` (consecutive dots)
- `user@@domain.com` (multiple @ symbols)

### Invalid Structure
- `.user@domain.com` (starts with dot)
- `user.@domain.com` (ends with dot)
- `user@.domain.com` (domain starts with dot)
- `user@domain.com.` (domain ends with dot)

### Length Issues
- Local part longer than 64 characters
- Domain part longer than 253 characters
- Total email longer than 320 characters

## 4. RFC Compliance Requirements

### Basic RFC 5322 Compliance
- Local part: 1-64 characters
- Domain part: 1-253 characters
- Total length: maximum 320 characters
- Case insensitive domain matching
- Allowed characters in local part: a-z, A-Z, 0-9, . + - _
- Allowed characters in domain: a-z, A-Z, 0-9, . -

### Domain Requirements
- Must contain at least one dot
- Must have valid TLD (2+ characters)
- Cannot start or end with hyphen
- Cannot have consecutive dots

## 5. Edge Cases

### Unicode and Special Characters
- ASCII characters only (no unicode support initially)
- No special characters beyond allowed set

### Length Limits
- Empty string handling
- Maximum length validation
- Minimum length validation (at least 5 characters: a@b.c)

### Boundary Conditions
- Single character local/domain parts
- Maximum allowed lengths
- Dot placement validation

## 6. Error Handling and Return Value Requirements

### Input Validation
- Handle None input → return False
- Handle empty string → return False
- Handle non-string input → return False

### Return Values
- Valid email → return True
- Invalid email → return False
- No exceptions should be raised for any input

### Function Signature
```python
def is_valid_email(email: str) -> bool:
    """
    Validate email address format.

    Args:
        email: String representing email address to validate

    Returns:
        bool: True if email is valid, False otherwise
    """
    pass
```

## 7. Performance Considerations

### Efficiency Requirements
- Function should execute in O(n) time where n is email length
- No complex regex patterns that cause exponential backtracking
- Efficient early validation to avoid unnecessary processing
- Memory usage should be minimal (no large data structures)

### Scalability
- Function should handle thousands of validations per second
- No external dependencies or network calls
- Pure function with no side effects
- Thread-safe implementation

## Implementation Strategy

### TDD Phases
1. Start with simplest valid cases
2. Add basic invalid cases
3. Implement edge cases progressively
4. Add performance optimizations in refactor phase

### Test Categories
1. Basic valid emails
2. Basic invalid emails
3. Edge cases and boundary conditions
4. Performance and stress tests