#!/usr/bin/env python3
"""
IPv4/IPv6 Address Validator - Method 3: Test-First Development (TDD)
Clean, constraint-driven implementation - serves as baseline (58 lines)
"""

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

    # Try IPv4 first
    ipv4_result = _validate_ipv4(address.strip())
    if ipv4_result['valid']:
        return ipv4_result

    # Try IPv6
    ipv6_result = _validate_ipv6(address.strip())
    return ipv6_result

def _validate_ipv4(address):
    """Validate IPv4 address format."""
    parts = address.split('.')
    if len(parts) != 4:
        return {'valid': False, 'version': None, 'normalized': None}

    for part in parts:
        if not part or (len(part) > 1 and part[0] == '0'):
            return {'valid': False, 'version': None, 'normalized': None}

        try:
            num = int(part)
            if num < 0 or num > 255:
                return {'valid': False, 'version': None, 'normalized': None}
        except ValueError:
            return {'valid': False, 'version': None, 'normalized': None}

    return {'valid': True, 'version': 'ipv4', 'normalized': address}

def _validate_ipv6(address):
    """Validate IPv6 address format."""
    # Check for multiple ::
    if address.count('::') > 1:
        return {'valid': False, 'version': None, 'normalized': None}

    # Expand :: compression
    if '::' in address:
        before, after = address.split('::', 1)
        before_parts = [p for p in before.split(':') if p] if before else []
        after_parts = [p for p in after.split(':') if p] if after else []

        missing_groups = 8 - len(before_parts) - len(after_parts)
        if missing_groups < 1:
            return {'valid': False, 'version': None, 'normalized': None}

        expanded_parts = before_parts + ['0'] * missing_groups + after_parts
    else:
        expanded_parts = address.split(':')

    if len(expanded_parts) != 8:
        return {'valid': False, 'version': None, 'normalized': None}

    normalized_parts = []
    for part in expanded_parts:
        if len(part) > 4:
            return {'valid': False, 'version': None, 'normalized': None}

        try:
            int(part, 16)
            normalized_parts.append(part.lower().zfill(4))
        except ValueError:
            return {'valid': False, 'version': None, 'normalized': None}

    normalized = ':'.join(normalized_parts)
    return {'valid': True, 'version': 'ipv6', 'normalized': normalized}