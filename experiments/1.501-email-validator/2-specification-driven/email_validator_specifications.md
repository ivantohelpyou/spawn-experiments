# Email Validator Specifications

## Overview
This document specifies the requirements and implementation details for an Email Validator function that validates email addresses according to practical standards while maintaining reasonable complexity.

## Validation Rules and Requirements

### 1. Basic Format Requirements
- Email must contain exactly one '@' symbol
- Email must have a local part (before '@') and domain part (after '@')
- Total email length must not exceed 254 characters (RFC 5321 limit)
- Local part must not exceed 64 characters (RFC 5321 limit)
- Domain part must not exceed 253 characters

### 2. Local Part Validation Rules
**Allowed Characters:**
- Alphanumeric characters (a-z, A-Z, 0-9)
- Special characters: . (dot), _ (underscore), - (hyphen), + (plus)

**Restrictions:**
- Must not start or end with a dot (.)
- Must not contain consecutive dots (..)
- Must not be empty
- Must not start or end with hyphen (-)

### 3. Domain Part Validation Rules
**Structure Requirements:**
- Must contain at least one dot (.) to separate domain levels
- Must have at least two parts (e.g., domain.tld)
- Each domain label must be 1-63 characters long

**Allowed Characters:**
- Alphanumeric characters (a-z, A-Z, 0-9)
- Hyphens (-) but not at the beginning or end of a label

**Top-Level Domain (TLD) Requirements:**
- Must be at least 2 characters long
- Must contain only alphabetic characters (a-z, A-Z)
- Must not start with a digit

### 4. Case Sensitivity
- Email validation should be case-insensitive
- Convert to lowercase for consistent processing

## Valid Email Format Cases

### Standard Valid Examples
- `user@example.com`
- `john.doe@company.org`
- `test_email@domain.co.uk`
- `user+tag@example.com`
- `a@b.co`
- `123@example.com`
- `user-name@sub.domain.com`

### Edge Cases (Valid)
- `x@y.ab` (minimum valid format)
- `very.long.local.part@example.com`
- `user+multiple+tags@domain.com`
- `1234567890@example.com`

## Invalid Email Format Cases

### Missing Components
- `@example.com` (no local part)
- `user@` (no domain part)
- `userexample.com` (no @ symbol)
- `user@@example.com` (multiple @ symbols)

### Local Part Violations
- `.user@example.com` (starts with dot)
- `user.@example.com` (ends with dot)
- `user..name@example.com` (consecutive dots)
- `user-@example.com` (ends with hyphen)
- `-user@example.com` (starts with hyphen)
- Empty local part

### Domain Part Violations
- `user@example` (no TLD)
- `user@.example.com` (starts with dot)
- `user@example.` (ends with dot)
- `user@example..com` (consecutive dots)
- `user@example.c` (TLD too short)
- `user@example.123` (TLD contains digits)
- `user@-example.com` (domain label starts with hyphen)
- `user@example-.com` (domain label ends with hyphen)

### Length Violations
- Local part exceeding 64 characters
- Domain part exceeding 253 characters
- Total email exceeding 254 characters

## Technical Approach

### Implementation Strategy
1. **Preprocessing**: Trim whitespace and convert to lowercase
2. **Basic Structure Validation**: Check for single '@' symbol
3. **Length Validation**: Verify overall and component length limits
4. **Local Part Validation**: Apply local part rules using regex
5. **Domain Part Validation**: Apply domain part rules using regex
6. **Return Result**: Boolean indicating validity

### Regular Expression Patterns
- **Local Part Pattern**: `^[a-zA-Z0-9]+([._+-][a-zA-Z0-9]+)*$`
- **Domain Label Pattern**: `^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$`
- **TLD Pattern**: `^[a-zA-Z]{2,}$`

## RFC Standards Compliance

### Followed Standards
- **RFC 5321**: SMTP specification for length limits
- **RFC 5322**: Internet Message Format for basic structure

### Practical Limitations
This implementation focuses on practical email validation rather than full RFC compliance:
- Does not support quoted strings in local part
- Does not support IP address literals in domain part
- Does not support internationalized domain names (IDN)
- Does not support comments in email addresses

## Edge Cases and Special Characters

### Supported Special Characters
- **Dot (.)**: Allowed in local part (not consecutive, not at edges)
- **Underscore (_)**: Allowed in local part
- **Hyphen (-)**: Allowed in local and domain parts (not at edges)
- **Plus (+)**: Allowed in local part for email aliasing

### Unsupported Features
- Quoted strings (e.g., `"user name"@example.com`)
- IP addresses (e.g., `user@[192.168.1.1]`)
- Unicode characters
- Comments (e.g., `user(comment)@example.com`)

## Function Interface

### Function Signature
```python
def validate_email(email: str) -> bool:
    """
    Validate an email address according to practical standards.

    Args:
        email (str): The email address to validate

    Returns:
        bool: True if valid, False otherwise
    """
```

### Input Requirements
- Single string parameter representing the email address
- Handle None or non-string inputs gracefully (return False)

### Output
- Boolean value indicating validation result
- No exceptions should be raised for invalid input

## Testing Requirements

### Test Categories
1. **Valid emails**: All standard and edge case valid formats
2. **Invalid emails**: All categories of invalid formats
3. **Boundary conditions**: Length limits and edge cases
4. **Input validation**: None, empty strings, non-string types
5. **Case sensitivity**: Mixed case inputs

### Performance Requirements
- Function should execute in O(n) time complexity where n is email length
- No external dependencies beyond Python standard library
- Minimal memory overhead