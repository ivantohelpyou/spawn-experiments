"""IP address validation utilities."""

import ipaddress
from typing import Optional, Tuple, Union

from ..models.error import ValidationError, ErrorCode


class IPValidator:
    """
    Validates IPv4 and IPv6 addresses.

    This class provides comprehensive IP address validation including:
    - IPv4 address validation
    - IPv6 address validation
    - Private IP detection
    - Reserved IP detection
    """

    @classmethod
    def validate(cls, ip_str: str) -> Tuple[bool, Optional[ValidationError], Optional[Union[ipaddress.IPv4Address, ipaddress.IPv6Address]]]:
        """
        Validate an IP address string.

        Args:
            ip_str: IP address string to validate

        Returns:
            Tuple of (is_valid, error_if_invalid, ip_object_if_valid)
        """
        if not ip_str:
            return False, ValidationError.format_error(
                ErrorCode.INVALID_IP_ADDRESS,
                "IP address cannot be empty"
            ), None

        # Try IPv4 first
        ipv4_result = cls.validate_ipv4(ip_str)
        if ipv4_result[0]:
            return ipv4_result

        # Try IPv6
        ipv6_result = cls.validate_ipv6(ip_str)
        if ipv6_result[0]:
            return ipv6_result

        # Neither IPv4 nor IPv6
        return False, ValidationError.format_error(
            ErrorCode.INVALID_IP_ADDRESS,
            f"Invalid IP address format: {ip_str}",
            {"ip": ip_str}
        ), None

    @classmethod
    def validate_ipv4(cls, ip_str: str) -> Tuple[bool, Optional[ValidationError], Optional[ipaddress.IPv4Address]]:
        """
        Validate an IPv4 address.

        Args:
            ip_str: IPv4 address string to validate

        Returns:
            Tuple of (is_valid, error_if_invalid, ipv4_object_if_valid)
        """
        try:
            ip_obj = ipaddress.IPv4Address(ip_str)
            return True, None, ip_obj
        except ipaddress.AddressValueError as e:
            return False, ValidationError.format_error(
                ErrorCode.INVALID_IP_ADDRESS,
                f"Invalid IPv4 address: {ip_str} - {e}",
                {"ip": ip_str, "type": "IPv4", "error": str(e)}
            ), None
        except Exception as e:
            return False, ValidationError.format_error(
                ErrorCode.INVALID_IP_ADDRESS,
                f"Error validating IPv4 address: {ip_str} - {e}",
                {"ip": ip_str, "type": "IPv4", "error": str(e)}
            ), None

    @classmethod
    def validate_ipv6(cls, ip_str: str) -> Tuple[bool, Optional[ValidationError], Optional[ipaddress.IPv6Address]]:
        """
        Validate an IPv6 address.

        Args:
            ip_str: IPv6 address string to validate

        Returns:
            Tuple of (is_valid, error_if_invalid, ipv6_object_if_valid)
        """
        # Handle IPv6 addresses in brackets (common in URLs)
        if ip_str.startswith('[') and ip_str.endswith(']'):
            ip_str = ip_str[1:-1]

        try:
            ip_obj = ipaddress.IPv6Address(ip_str)
            return True, None, ip_obj
        except ipaddress.AddressValueError as e:
            return False, ValidationError.format_error(
                ErrorCode.INVALID_IP_ADDRESS,
                f"Invalid IPv6 address: {ip_str} - {e}",
                {"ip": ip_str, "type": "IPv6", "error": str(e)}
            ), None
        except Exception as e:
            return False, ValidationError.format_error(
                ErrorCode.INVALID_IP_ADDRESS,
                f"Error validating IPv6 address: {ip_str} - {e}",
                {"ip": ip_str, "type": "IPv6", "error": str(e)}
            ), None

    @classmethod
    def is_private(cls, ip: Union[str, ipaddress.IPv4Address, ipaddress.IPv6Address]) -> bool:
        """
        Check if an IP address is private.

        Args:
            ip: IP address string or object

        Returns:
            True if IP address is private

        Raises:
            ValidationError: If IP address is invalid
        """
        if isinstance(ip, str):
            is_valid, error, ip_obj = cls.validate(ip)
            if not is_valid:
                raise error
            ip = ip_obj

        return ip.is_private

    @classmethod
    def is_loopback(cls, ip: Union[str, ipaddress.IPv4Address, ipaddress.IPv6Address]) -> bool:
        """
        Check if an IP address is loopback.

        Args:
            ip: IP address string or object

        Returns:
            True if IP address is loopback

        Raises:
            ValidationError: If IP address is invalid
        """
        if isinstance(ip, str):
            is_valid, error, ip_obj = cls.validate(ip)
            if not is_valid:
                raise error
            ip = ip_obj

        return ip.is_loopback

    @classmethod
    def is_reserved(cls, ip: Union[str, ipaddress.IPv4Address, ipaddress.IPv6Address]) -> bool:
        """
        Check if an IP address is reserved.

        Args:
            ip: IP address string or object

        Returns:
            True if IP address is reserved

        Raises:
            ValidationError: If IP address is invalid
        """
        if isinstance(ip, str):
            is_valid, error, ip_obj = cls.validate(ip)
            if not is_valid:
                raise error
            ip = ip_obj

        return ip.is_reserved

    @classmethod
    def is_multicast(cls, ip: Union[str, ipaddress.IPv4Address, ipaddress.IPv6Address]) -> bool:
        """
        Check if an IP address is multicast.

        Args:
            ip: IP address string or object

        Returns:
            True if IP address is multicast

        Raises:
            ValidationError: If IP address is invalid
        """
        if isinstance(ip, str):
            is_valid, error, ip_obj = cls.validate(ip)
            if not is_valid:
                raise error
            ip = ip_obj

        return ip.is_multicast

    @classmethod
    def is_global(cls, ip: Union[str, ipaddress.IPv4Address, ipaddress.IPv6Address]) -> bool:
        """
        Check if an IP address is global (publicly routable).

        Args:
            ip: IP address string or object

        Returns:
            True if IP address is global

        Raises:
            ValidationError: If IP address is invalid
        """
        if isinstance(ip, str):
            is_valid, error, ip_obj = cls.validate(ip)
            if not is_valid:
                raise error
            ip = ip_obj

        return ip.is_global

    @classmethod
    def get_ip_type(cls, ip: Union[str, ipaddress.IPv4Address, ipaddress.IPv6Address]) -> str:
        """
        Get the type classification of an IP address.

        Args:
            ip: IP address string or object

        Returns:
            String describing IP type (e.g., 'private', 'loopback', 'global')

        Raises:
            ValidationError: If IP address is invalid
        """
        if isinstance(ip, str):
            is_valid, error, ip_obj = cls.validate(ip)
            if not is_valid:
                raise error
            ip = ip_obj

        if ip.is_loopback:
            return "loopback"
        elif ip.is_private:
            return "private"
        elif ip.is_reserved:
            return "reserved"
        elif ip.is_multicast:
            return "multicast"
        elif ip.is_global:
            return "global"
        else:
            return "unknown"

    @classmethod
    def normalize(cls, ip_str: str) -> str:
        """
        Normalize an IP address string.

        Args:
            ip_str: IP address string to normalize

        Returns:
            Normalized IP address string

        Raises:
            ValidationError: If IP address is invalid
        """
        is_valid, error, ip_obj = cls.validate(ip_str)
        if not is_valid:
            raise error

        return str(ip_obj)

    @classmethod
    def should_block(cls, ip: Union[str, ipaddress.IPv4Address, ipaddress.IPv6Address],
                    block_private: bool = False) -> Tuple[bool, Optional[str]]:
        """
        Determine if an IP address should be blocked based on security policy.

        Args:
            ip: IP address string or object
            block_private: Whether to block private IP addresses

        Returns:
            Tuple of (should_block, reason_if_blocked)

        Raises:
            ValidationError: If IP address is invalid
        """
        if isinstance(ip, str):
            is_valid, error, ip_obj = cls.validate(ip)
            if not is_valid:
                raise error
            ip = ip_obj

        # Always block loopback for security
        if ip.is_loopback:
            return True, "loopback address"

        # Block private IPs if configured
        if block_private and ip.is_private:
            return True, "private address"

        # Block reserved addresses
        if ip.is_reserved:
            return True, "reserved address"

        # Block multicast addresses
        if ip.is_multicast:
            return True, "multicast address"

        return False, None