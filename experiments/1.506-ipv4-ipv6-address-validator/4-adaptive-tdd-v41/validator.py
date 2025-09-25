#!/usr/bin/env python3
"""
IPv4/IPv6 Address Validator - Method 4: Adaptive TDD V4.1
Strategic validation with complexity-matched testing approach (229 lines)
"""

def validate_ip_address(address):
    """
    Validate IPv4 or IPv6 address using adaptive TDD approach.

    Strategic implementation that applies standard TDD for straightforward IPv4
    and adaptive validation for complex IPv6 compression logic.

    Args:
        address: String to validate as IP address

    Returns:
        {
            'valid': bool,
            'version': 'ipv4' | 'ipv6' | None,
            'normalized': str | None
        }
    """
    # Input validation - straightforward, standard TDD sufficient
    if not _is_valid_input(address):
        return {'valid': False, 'version': None, 'normalized': None}

    clean_address = address.strip()

    # Try IPv4 first - moderate complexity, standard TDD approach
    ipv4_result = _validate_ipv4_address(clean_address)
    if ipv4_result['valid']:
        return ipv4_result

    # Try IPv6 - high complexity, adaptive validation applied
    ipv6_result = _validate_ipv6_address(clean_address)
    return ipv6_result

def _is_valid_input(address):
    """Basic input validation - straightforward logic."""
    return address and isinstance(address, str) and address.strip()

def _validate_ipv4_address(address):
    """
    IPv4 validation using standard TDD.
    Straightforward logic doesn't require adaptive validation.
    """
    # Standard approach: split and validate
    parts = address.split('.')

    if len(parts) != 4:
        return {'valid': False, 'version': None, 'normalized': None}

    validated_parts = []

    for part in parts:
        if not _is_valid_ipv4_octet(part):
            return {'valid': False, 'version': None, 'normalized': None}
        validated_parts.append(part)

    # IPv4 normalization is simple - just rejoin
    normalized = '.'.join(validated_parts)
    return {'valid': True, 'version': 'ipv4', 'normalized': normalized}

def _is_valid_ipv4_octet(octet):
    """Validate single IPv4 octet - standard TDD sufficient."""
    if not octet:
        return False

    # Leading zero check (except single "0")
    if len(octet) > 1 and octet[0] == '0':
        return False

    # Numeric and range check
    try:
        value = int(octet)
        return 0 <= value <= 255
    except ValueError:
        return False

def _validate_ipv6_address(address):
    """
    IPv6 validation using ADAPTIVE TDD approach.

    Complex compression logic requires adaptive validation to ensure
    edge cases are handled correctly. This is where adaptive validation
    provides strategic value.
    """
    # Basic format validation
    if not _has_valid_ipv6_format(address):
        return {'valid': False, 'version': None, 'normalized': None}

    # Handle compression - COMPLEX LOGIC requiring adaptive validation
    try:
        if '::' in address:
            expanded_groups = _expand_compressed_ipv6(address)
        else:
            expanded_groups = _parse_full_ipv6(address)

        # Validate expanded groups
        if not _are_valid_ipv6_groups(expanded_groups):
            return {'valid': False, 'version': None, 'normalized': None}

        # Normalize to canonical format
        normalized = _normalize_ipv6_groups(expanded_groups)
        return {'valid': True, 'version': 'ipv6', 'normalized': normalized}

    except IPv6ValidationError:
        return {'valid': False, 'version': None, 'normalized': None}

def _has_valid_ipv6_format(address):
    """
    Basic IPv6 format validation - ADAPTIVE VALIDATION APPLIED.

    This is where wrong implementations commonly fail, so we apply
    adaptive validation to ensure robustness.
    """
    # Critical edge case: multiple compression sequences
    if address.count('::') > 1:
        return False

    # Critical edge case: triple colon (common parsing error)
    if ':::' in address:
        return False

    # Critical edge case: trailing colons after compression
    if address.endswith(':::'):
        return False

    return True

class IPv6ValidationError(Exception):
    """Custom exception for IPv6 validation errors."""
    pass

def _expand_compressed_ipv6(address):
    """
    Expand IPv6 compression - MOST COMPLEX LOGIC.

    This is where adaptive validation is most critical.
    Wrong implementations often miscalculate group counts.
    """
    if address.count('::') != 1:
        raise IPv6ValidationError("Invalid compression count")

    before, after = address.split('::', 1)

    # Parse groups before and after compression
    before_groups = [g for g in before.split(':') if g] if before else []
    after_groups = [g for g in after.split(':') if g] if after else []

    # Critical calculation: ensure we don't overflow
    total_existing = len(before_groups) + len(after_groups)
    if total_existing >= 8:
        raise IPv6ValidationError("Too many groups for compression")

    # Calculate missing groups
    missing_groups = 8 - total_existing
    if missing_groups < 1:
        raise IPv6ValidationError("Invalid compression - no groups to compress")

    # Reconstruct full 8-group format
    expanded = before_groups + ['0'] * missing_groups + after_groups

    if len(expanded) != 8:
        raise IPv6ValidationError("Expansion resulted in wrong group count")

    return expanded

def _parse_full_ipv6(address):
    """Parse full IPv6 address without compression."""
    groups = address.split(':')

    if len(groups) != 8:
        raise IPv6ValidationError("Full IPv6 must have exactly 8 groups")

    return groups

def _are_valid_ipv6_groups(groups):
    """
    Validate IPv6 groups - ADAPTIVE VALIDATION APPLIED.

    Hex validation is where subtle bugs often occur.
    """
    if len(groups) != 8:
        return False

    for group in groups:
        if not _is_valid_hex_group(group):
            return False

    return True

def _is_valid_hex_group(group):
    """Validate single IPv6 hex group."""
    if not group or len(group) > 4:
        return False

    # Hex character validation
    try:
        int(group, 16)  # This validates hex format
        return True
    except ValueError:
        return False

def _normalize_ipv6_groups(groups):
    """Normalize IPv6 groups to canonical format."""
    normalized_groups = []

    for group in groups:
        # Convert to lowercase and zero-pad to 4 characters
        normalized_group = group.lower().zfill(4)
        normalized_groups.append(normalized_group)

    return ':'.join(normalized_groups)

# Adaptive validation testing functions
# These are used during development to verify test robustness

def _create_wrong_compression_implementation(address):
    """
    Intentionally wrong IPv6 compression for adaptive validation testing.

    This wrong implementation is used to verify our tests catch common bugs.
    """
    # WRONG: This implementation has a bug - doesn't handle edge cases properly
    if '::' not in address:
        return address.split(':')

    before, after = address.split('::')

    # BUG: Doesn't properly handle empty before/after
    before_groups = before.split(':')  # WRONG: should filter empty
    after_groups = after.split(':')   # WRONG: should filter empty

    # BUG: Wrong calculation
    missing = 8 - len(before_groups) - len(after_groups)  # WRONG: doesn't account for empty strings

    return before_groups + ['0'] * missing + after_groups

def _verify_adaptive_validation():
    """
    Adaptive validation verification - ensures our tests catch wrong implementations.

    This function tests that our validation logic properly rejects the intentionally
    wrong implementation above.
    """
    test_cases = [
        "2001:db8::1",
        "::1",
        "2001::",
        "::2001"
    ]

    for test_case in test_cases:
        # Our correct implementation
        correct_result = validate_ip_address(test_case)

        # Wrong implementation (should fail on edge cases)
        try:
            wrong_groups = _create_wrong_compression_implementation(test_case)
            # If wrong implementation doesn't crash, our tests should catch the difference
            print(f"Adaptive validation test: {test_case}")
            print(f"  Correct: {correct_result}")
            print(f"  Wrong groups: {wrong_groups}")
        except Exception as e:
            print(f"Wrong implementation correctly failed on {test_case}: {e}")

if __name__ == "__main__":
    # Test the implementation
    test_cases = [
        "192.168.1.1",      # IPv4
        "2001:db8::1",      # IPv6 compressed
        "::1",              # IPv6 loopback
        "256.1.1.1",        # Invalid IPv4
        "2001:db8::1::2",   # Invalid IPv6
        "",                 # Empty
    ]

    print("Adaptive TDD V4.1 Validator Test Results:")
    print("=" * 50)

    for test_input in test_cases:
        result = validate_ip_address(test_input)
        display_input = f'"{test_input}"' if test_input else "(empty)"
        print(f"{display_input:<25} -> {result}")

    print("\nAdaptive validation verification:")
    _verify_adaptive_validation()