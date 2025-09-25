# Baseline Specification: Email Validator

## Core Requirements

Create a Python function that validates email addresses according to practical standards while maintaining reasonable complexity.

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
- Hyphens (-) in the middle of labels only
- Dots (.) as separators between labels

**Restrictions:**
- Labels must not start or end with hyphens
- Must not start or end with dots
- TLD (final part) must be at least 2 characters and contain only letters

### 4. What NOT to Support (Scope Limitations)
- Quoted strings in local part ("test@example.com")
- IP addresses as domain ([192.168.1.1])
- Internationalized domain names (IDN)
- Comments in email addresses
- Complex RFC 5322 features

## Function Interface

```python
def validate_email(email_address: str) -> bool:
    """
    Validate email address according to practical standards.

    Args:
        email_address (str): Email address to validate

    Returns:
        bool: True if valid, False if invalid
    """
```

## Expected Deliverables

1. **Core validation function** meeting the above requirements
2. **Test suite** demonstrating the function works correctly
3. **Example usage** showing how to use the function

## Test Coverage Requirements

The implementation should handle these test cases correctly:

**Valid emails:**
- `user@domain.com`
- `user.name@domain.co.uk`
- `user+tag@subdomain.domain.com`
- `user_name@domain-name.org`

**Invalid emails:**
- `user@domain` (no TLD)
- `user@@domain.com` (double @)
- `user@domain..com` (consecutive dots)
- `user.@domain.com` (local part ends with dot)
- `.user@domain.com` (local part starts with dot)
- Empty string and malformed formats

---

*This specification is identical to the original 1.501 experiment to enable direct timing comparison between normal development context and severed branch isolation.*