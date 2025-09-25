#!/usr/bin/env python3
"""
IPv4/IPv6 Address Validator - Method 1: Immediate Implementation
Quick working solution with good edge case coverage (208 lines)
"""

import re

def validate_ip_address(address):
    """
    Validate IPv4 or IPv6 address format.

    Args:
        address: String to validate as IP address

    Returns:
        {
            'valid': bool,
            'version': 'ipv4' | 'ipv6' | None,
            'normalized': str | None
        }
    """
    if not address or not isinstance(address, str):
        return {'valid': False, 'version': None, 'normalized': None}

    address = address.strip()

    # Quick IPv4 check - if it has 3 dots, try IPv4 first
    if address.count('.') == 3:
        ipv4_result = validate_ipv4(address)
        if ipv4_result['valid']:
            return ipv4_result

    # Try IPv6 if not valid IPv4
    ipv6_result = validate_ipv6(address)
    if ipv6_result['valid']:
        return ipv6_result

    # Neither worked
    return {'valid': False, 'version': None, 'normalized': None}

def validate_ipv4(address):
    """Validate IPv4 address - immediate approach with range checking."""
    parts = address.split('.')

    # Must have exactly 4 parts
    if len(parts) != 4:
        return {'valid': False, 'version': None, 'normalized': None}

    validated_parts = []

    for part in parts:
        # Empty part is invalid
        if not part:
            return {'valid': False, 'version': None, 'normalized': None}

        # Leading zeros not allowed except for "0"
        if len(part) > 1 and part[0] == '0':
            return {'valid': False, 'version': None, 'normalized': None}

        # Must be numeric
        try:
            num = int(part)
        except ValueError:
            return {'valid': False, 'version': None, 'normalized': None}

        # Must be in valid octet range
        if num < 0 or num > 255:
            return {'valid': False, 'version': None, 'normalized': None}

        validated_parts.append(part)

    # Valid IPv4
    normalized = '.'.join(validated_parts)
    return {'valid': True, 'version': 'ipv4', 'normalized': normalized}

def validate_ipv6(address):
    """Validate IPv6 address with compression handling."""
    # Basic format validation
    if not address:
        return {'valid': False, 'version': None, 'normalized': None}

    # Check for invalid patterns
    if ':::' in address:  # Triple colon invalid
        return {'valid': False, 'version': None, 'normalized': None}

    # Multiple :: not allowed
    if address.count('::') > 1:
        return {'valid': False, 'version': None, 'normalized': None}

    # Handle compression
    if '::' in address:
        return validate_compressed_ipv6(address)
    else:
        return validate_full_ipv6(address)

def validate_compressed_ipv6(address):
    """Handle IPv6 addresses with :: compression."""
    # Split on ::
    parts = address.split('::')
    if len(parts) != 2:
        return {'valid': False, 'version': None, 'normalized': None}

    before, after = parts

    # Parse groups before and after ::
    before_groups = [g for g in before.split(':') if g] if before else []
    after_groups = [g for g in after.split(':') if g] if after else []

    # Validate individual groups
    all_groups = before_groups + after_groups
    for group in all_groups:
        if not is_valid_hex_group(group):
            return {'valid': False, 'version': None, 'normalized': None}

    # Calculate missing groups
    total_existing = len(before_groups) + len(after_groups)
    if total_existing >= 8:  # Can't compress if we already have 8+ groups
        return {'valid': False, 'version': None, 'normalized': None}

    missing_groups = 8 - total_existing

    # Create expanded groups
    expanded_groups = (
        before_groups +
        ['0'] * missing_groups +
        after_groups
    )

    if len(expanded_groups) != 8:
        return {'valid': False, 'version': None, 'normalized': None}

    # Normalize to full format
    normalized_groups = []
    for group in expanded_groups:
        normalized_groups.append(group.lower().zfill(4))

    normalized = ':'.join(normalized_groups)
    return {'valid': True, 'version': 'ipv6', 'normalized': normalized}

def validate_full_ipv6(address):
    """Validate full IPv6 address without compression."""
    groups = address.split(':')

    # Must have exactly 8 groups
    if len(groups) != 8:
        return {'valid': False, 'version': None, 'normalized': None}

    # Validate each group
    normalized_groups = []
    for group in groups:
        if not is_valid_hex_group(group):
            return {'valid': False, 'version': None, 'normalized': None}

        # Normalize group (lowercase, zero-padded to 4 chars)
        normalized_groups.append(group.lower().zfill(4))

    normalized = ':'.join(normalized_groups)
    return {'valid': True, 'version': 'ipv6', 'normalized': normalized}

def is_valid_hex_group(group):
    """Check if a group is valid hex (1-4 characters)."""
    if not group or len(group) > 4:
        return False

    # Check if all characters are valid hex
    for char in group.lower():
        if char not in '0123456789abcdef':
            return False

    return True

# Test the implementation with some examples
if __name__ == "__main__":
    test_cases = [
        # IPv4 tests
        "192.168.1.1",      # Valid IPv4
        "0.0.0.0",          # Valid IPv4 zero
        "255.255.255.255",  # Valid IPv4 max
        "256.1.1.1",        # Invalid IPv4 - octet > 255
        "192.168.1",        # Invalid IPv4 - too few octets
        "192.168.01.1",     # Invalid IPv4 - leading zero

        # IPv6 tests
        "2001:db8::1",      # Valid IPv6 compressed
        "::1",              # Valid IPv6 loopback
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",  # Valid IPv6 full
        "2001:db8::1::2",   # Invalid IPv6 - multiple ::
        "2001:db8:85a3::8a2e:370g:7334",  # Invalid IPv6 - invalid hex

        # Edge cases
        "",                 # Empty string
        "not-an-ip",       # Invalid format
    ]

    print("IPv4/IPv6 Address Validator Test Results:")
    print("=" * 50)

    for test_input in test_cases:
        result = validate_ip_address(test_input)
        display_input = f'"{test_input}"' if test_input else "(empty)"
        print(f"{display_input:<35} -> {result}")

    print("\nTesting complete!")