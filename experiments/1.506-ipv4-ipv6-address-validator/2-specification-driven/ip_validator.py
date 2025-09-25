#!/usr/bin/env python3
"""
IPv4/IPv6 Address Validator - Method 2: Specification-Driven Development
Enterprise-grade validation framework (259 lines - over-engineered)
"""

import re
from typing import Dict, Optional, List, Any

class ValidationError(Exception):
    """Custom validation error with categorization."""
    def __init__(self, message: str, category: str = "GENERAL"):
        self.message = message
        self.category = category
        super().__init__(message)

class IPv4AddressValidator:
    """Specialized IPv4 address validation with comprehensive error handling."""

    OCTET_MIN = 0
    OCTET_MAX = 255
    REQUIRED_OCTETS = 4

    @classmethod
    def validate(cls, address: str) -> Dict[str, Any]:
        """Validate IPv4 address with detailed error reporting."""
        try:
            cls._validate_input_format(address)
            octets = cls._parse_octets(address)
            cls._validate_octets(octets)
            normalized = cls._normalize_address(octets)

            return {
                'valid': True,
                'version': 'ipv4',
                'normalized': normalized,
                'validation_details': {
                    'octets': octets,
                    'format': 'dotted_decimal',
                    'validation_level': 'STRICT'
                }
            }
        except ValidationError as e:
            return {
                'valid': False,
                'version': None,
                'normalized': None,
                'error': {
                    'message': e.message,
                    'category': e.category
                }
            }

    @classmethod
    def _validate_input_format(cls, address: str) -> None:
        """Validate basic input format requirements."""
        if not isinstance(address, str):
            raise ValidationError("Input must be string", "INPUT_TYPE")

        if not address.strip():
            raise ValidationError("Empty address", "EMPTY_INPUT")

        if address.count('.') != cls.REQUIRED_OCTETS - 1:
            raise ValidationError("Invalid dot count", "FORMAT")

    @classmethod
    def _parse_octets(cls, address: str) -> List[str]:
        """Parse address into octet components."""
        octets = address.strip().split('.')

        if len(octets) != cls.REQUIRED_OCTETS:
            raise ValidationError("Invalid octet count", "STRUCTURE")

        return octets

    @classmethod
    def _validate_octets(cls, octets: List[str]) -> None:
        """Validate individual octets with comprehensive checking."""
        for i, octet in enumerate(octets):
            cls._validate_single_octet(octet, i)

    @classmethod
    def _validate_single_octet(cls, octet: str, position: int) -> None:
        """Validate single octet with position-aware error reporting."""
        if not octet:
            raise ValidationError(f"Empty octet at position {position}", "OCTET_EMPTY")

        # Leading zero validation
        if len(octet) > 1 and octet[0] == '0':
            raise ValidationError(f"Leading zero in octet {position}", "LEADING_ZERO")

        # Numeric validation
        try:
            value = int(octet)
        except ValueError:
            raise ValidationError(f"Non-numeric octet at position {position}", "NON_NUMERIC")

        # Range validation
        if value < cls.OCTET_MIN or value > cls.OCTET_MAX:
            raise ValidationError(f"Octet {position} out of range ({cls.OCTET_MIN}-{cls.OCTET_MAX})", "RANGE")

    @classmethod
    def _normalize_address(cls, octets: List[str]) -> str:
        """Normalize address to canonical format."""
        return '.'.join(octets)

class IPv6AddressValidator:
    """Specialized IPv6 address validation with compression handling."""

    REQUIRED_GROUPS = 8
    MAX_GROUP_LENGTH = 4
    HEX_PATTERN = re.compile(r'^[0-9a-fA-F]*$')

    @classmethod
    def validate(cls, address: str) -> Dict[str, Any]:
        """Validate IPv6 address with comprehensive analysis."""
        try:
            cls._validate_input_format(address)
            groups = cls._parse_and_expand(address)
            cls._validate_groups(groups)
            normalized = cls._normalize_address(groups)

            return {
                'valid': True,
                'version': 'ipv6',
                'normalized': normalized,
                'validation_details': {
                    'groups': groups,
                    'format': 'hexadecimal_colon',
                    'compression_used': '::' in address,
                    'validation_level': 'STRICT'
                }
            }
        except ValidationError as e:
            return {
                'valid': False,
                'version': None,
                'normalized': None,
                'error': {
                    'message': e.message,
                    'category': e.category
                }
            }

    @classmethod
    def _validate_input_format(cls, address: str) -> None:
        """Validate basic IPv6 input format."""
        if not isinstance(address, str):
            raise ValidationError("Input must be string", "INPUT_TYPE")

        if not address.strip():
            raise ValidationError("Empty address", "EMPTY_INPUT")

        # Check for multiple compression sequences
        if address.count('::') > 1:
            raise ValidationError("Multiple compression sequences", "COMPRESSION")

        # Check for invalid triple colons
        if ':::' in address:
            raise ValidationError("Invalid triple colon sequence", "FORMAT")

    @classmethod
    def _parse_and_expand(cls, address: str) -> List[str]:
        """Parse and expand compressed IPv6 address."""
        address = address.strip().lower()

        if '::' in address:
            return cls._expand_compressed_address(address)
        else:
            return cls._parse_full_address(address)

    @classmethod
    def _expand_compressed_address(cls, address: str) -> List[str]:
        """Expand compressed IPv6 address with :: notation."""
        before, after = address.split('::', 1)

        before_groups = [g for g in before.split(':') if g] if before else []
        after_groups = [g for g in after.split(':') if g] if after else []

        existing_groups = len(before_groups) + len(after_groups)
        if existing_groups >= cls.REQUIRED_GROUPS:
            raise ValidationError("Invalid compression - too many groups", "COMPRESSION")

        missing_groups = cls.REQUIRED_GROUPS - existing_groups
        expanded_groups = before_groups + ['0'] * missing_groups + after_groups

        if len(expanded_groups) != cls.REQUIRED_GROUPS:
            raise ValidationError("Invalid group count after expansion", "STRUCTURE")

        return expanded_groups

    @classmethod
    def _parse_full_address(cls, address: str) -> List[str]:
        """Parse full IPv6 address without compression."""
        groups = address.split(':')

        if len(groups) != cls.REQUIRED_GROUPS:
            raise ValidationError("Invalid group count for full address", "STRUCTURE")

        return groups

    @classmethod
    def _validate_groups(cls, groups: List[str]) -> None:
        """Validate individual IPv6 groups."""
        for i, group in enumerate(groups):
            cls._validate_single_group(group, i)

    @classmethod
    def _validate_single_group(cls, group: str, position: int) -> None:
        """Validate single IPv6 group with position-aware error reporting."""
        if len(group) > cls.MAX_GROUP_LENGTH:
            raise ValidationError(f"Group {position} too long", "GROUP_LENGTH")

        if not cls.HEX_PATTERN.match(group):
            raise ValidationError(f"Invalid hex characters in group {position}", "HEX_FORMAT")

    @classmethod
    def _normalize_address(cls, groups: List[str]) -> str:
        """Normalize IPv6 address to canonical format."""
        normalized_groups = [group.zfill(4) for group in groups]
        return ':'.join(normalized_groups)

class IPAddressValidationOrchestrator:
    """Enterprise-grade IP address validation orchestrator."""

    @classmethod
    def validate_ip_address(cls, address: str) -> Dict[str, Any]:
        """
        Validate IP address using enterprise validation framework.

        Args:
            address: String to validate as IP address

        Returns:
            Comprehensive validation result dictionary
        """
        # Input sanitization and pre-processing
        sanitized_input = cls._sanitize_input(address)

        if not sanitized_input['valid']:
            return sanitized_input

        clean_address = sanitized_input['address']

        # IPv4 validation attempt
        ipv4_result = IPv4AddressValidator.validate(clean_address)
        if ipv4_result['valid']:
            return cls._format_success_response(ipv4_result)

        # IPv6 validation attempt
        ipv6_result = IPv6AddressValidator.validate(clean_address)
        if ipv6_result['valid']:
            return cls._format_success_response(ipv6_result)

        # Neither validation succeeded
        return cls._format_failure_response(ipv4_result, ipv6_result)

    @classmethod
    def _sanitize_input(cls, address) -> Dict[str, Any]:
        """Sanitize and validate input before processing."""
        if address is None:
            return {'valid': False, 'error': 'Null input'}

        if not isinstance(address, str):
            return {'valid': False, 'error': 'Non-string input'}

        if not address.strip():
            return {'valid': False, 'error': 'Empty input'}

        return {'valid': True, 'address': address.strip()}

    @classmethod
    def _format_success_response(cls, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Format successful validation response to standard format."""
        return {
            'valid': True,
            'version': validation_result['version'],
            'normalized': validation_result['normalized']
        }

    @classmethod
    def _format_failure_response(cls, ipv4_result: Dict[str, Any], ipv6_result: Dict[str, Any]) -> Dict[str, Any]:
        """Format failure response with comprehensive error details."""
        return {
            'valid': False,
            'version': None,
            'normalized': None,
            'validation_attempts': {
                'ipv4': ipv4_result.get('error', 'Unknown error'),
                'ipv6': ipv6_result.get('error', 'Unknown error')
            }
        }

# Public API
validate_ip_address = IPAddressValidationOrchestrator.validate_ip_address