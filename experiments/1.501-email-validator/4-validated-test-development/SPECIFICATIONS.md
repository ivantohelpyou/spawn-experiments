# Email Validator Specifications

## 1. Core Functional Requirements

The email validator must:
- Accept a string input and return a boolean indicating validity
- Follow a simplified RFC-inspired approach (not full RFC 5322 compliance)
- Provide clear, deterministic validation rules
- Handle common real-world email patterns correctly
- Reject obviously invalid formats

## 2. Valid Email Format Patterns

### Basic Structure
- Must contain exactly one '@' symbol
- Must have non-empty local part (before @)
- Must have non-empty domain part (after @)
- Format: `local@domain`

### Valid Local Part Examples
- `user` - simple alphanumeric
- `user.name` - dots allowed (not at start/end)
- `user_name` - underscores allowed
- `user-name` - hyphens allowed
- `user123` - numbers allowed
- `user+tag` - plus signs allowed
- `a` - single character allowed

### Valid Domain Part Examples
- `example.com` - standard domain
- `sub.example.com` - subdomain
- `example-site.com` - hyphens in domain
- `123.456.789.012` - IP addresses (basic format)
- `x.co` - short domains
- `very-long-domain-name.example.org` - long domains

### Complete Valid Email Examples
- `user@example.com`
- `test.email@subdomain.example.org`
- `user+tag@example.co.uk`
- `simple@x.co`
- `user123@test-domain.com`

## 3. Invalid Email Format Patterns

### Structure Violations
- No @ symbol: `userexample.com`
- Multiple @ symbols: `user@@example.com`, `user@exam@ple.com`
- Empty local part: `@example.com`
- Empty domain part: `user@`
- Empty string: ``
- Only @ symbol: `@`

### Local Part Violations
- Starts with dot: `.user@example.com`
- Ends with dot: `user.@example.com`
- Consecutive dots: `user..name@example.com`
- Contains spaces: `user name@example.com`
- Contains invalid chars: `user<>@example.com`

### Domain Part Violations
- Starts with dot: `user@.example.com`
- Ends with dot: `user@example.com.`
- Consecutive dots: `user@example..com`
- No dot in domain: `user@examplecom`
- Contains spaces: `user@exam ple.com`
- Contains invalid chars: `user@exam<>ple.com`

## 4. RFC Compliance Requirements (Simplified)

Our validator will implement a **practical subset** of RFC 5322:
- Case-insensitive domain names
- Basic character set for local part: a-z, A-Z, 0-9, ., _, -, +
- Basic character set for domain: a-z, A-Z, 0-9, ., -
- Domain must contain at least one dot
- No quoted strings or escape sequences
- No comments in parentheses

## 5. Edge Cases

### Unicode Handling
- **NOT SUPPORTED**: Non-ASCII characters will be rejected
- Examples that should fail: `üser@example.com`, `user@münchen.de`

### Special Characters
- Local part allows: letters, numbers, dots, underscores, hyphens, plus signs
- Domain part allows: letters, numbers, dots, hyphens
- All other characters are invalid

### Length Limits
- Maximum email length: 254 characters (RFC limit)
- Maximum local part length: 64 characters
- Maximum domain part length: 253 characters
- Minimum total length: 3 characters (a@b.c format)

### Boundary Cases
- Single character local part: valid
- Single character domain labels: valid
- Very long but valid emails: should be accepted if under limits

## 6. Error Handling and Return Values

### Function Signature
```python
def is_valid_email(email: str) -> bool:
    """
    Validates an email address according to simplified RFC rules.

    Args:
        email (str): The email address to validate

    Returns:
        bool: True if email is valid, False otherwise

    Raises:
        TypeError: If input is not a string
    """
```

### Return Behavior
- Returns `True` for valid emails
- Returns `False` for invalid emails
- Raises `TypeError` if input is not a string
- Never returns `None` or other values

### Input Handling
- Must handle empty strings gracefully (return `False`)
- Must handle whitespace-only strings (return `False`)
- Must strip leading/trailing whitespace before validation
- Must handle very long strings without crashing

## 7. Performance Considerations

### Efficiency Requirements
- Should validate typical emails in O(n) time where n is email length
- Should fail fast on obvious invalid formats
- Should not use excessive memory for any input
- Should handle 10,000+ email validations per second

### Implementation Constraints
- Use only Python standard library (specifically `re` module)
- Avoid complex regex that could cause catastrophic backtracking
- Use simple string operations where possible
- Cache compiled regex patterns

## 8. Testing Requirements

### Test Coverage Expectations
- Test all valid format patterns
- Test all invalid format patterns
- Test all edge cases and boundary conditions
- Test error handling for non-string inputs
- Test performance with long inputs

### Test Quality Standards
- Each test should verify one specific validation rule
- Tests should have descriptive names explaining what they verify
- Tests should include both positive and negative cases
- Tests should catch common implementation mistakes
- Test validation step must prove tests work correctly

## 9. Implementation Phases

1. **Basic Structure**: @ symbol presence and splitting
2. **Local Part**: Character validation and format rules
3. **Domain Part**: Domain format and structure validation
4. **Edge Cases**: Unicode, length limits, special cases
5. **Error Handling**: Type checking and graceful failures
6. **Performance**: Optimization and efficiency validation