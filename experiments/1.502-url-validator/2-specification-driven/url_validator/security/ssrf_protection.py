"""SSRF (Server-Side Request Forgery) protection utilities."""

import ipaddress
import re
from typing import List, Optional, Set, Tuple, Union
from urllib.parse import urlparse

from ..models.error import ValidationError, ErrorCode
from ..validators.ip_validator import IPValidator


class SSRFProtection:
    """
    Provides protection against Server-Side Request Forgery (SSRF) attacks.

    This class implements various security checks to prevent malicious URLs
    from being used to access internal or restricted resources.
    """

    # Default blocked IP ranges (RFC 1918 private networks + others)
    DEFAULT_BLOCKED_NETWORKS = [
        "10.0.0.0/8",          # RFC 1918 - Private networks
        "172.16.0.0/12",       # RFC 1918 - Private networks
        "192.168.0.0/16",      # RFC 1918 - Private networks
        "127.0.0.0/8",         # RFC 990 - Loopback
        "169.254.0.0/16",      # RFC 3927 - Link-local
        "224.0.0.0/4",         # RFC 3171 - Multicast
        "240.0.0.0/4",         # RFC 1112 - Reserved
        "0.0.0.0/8",           # RFC 5735 - "This" network
        "::1/128",             # IPv6 loopback
        "fe80::/10",           # IPv6 link-local
        "fc00::/7",            # IPv6 unique local
        "ff00::/8",            # IPv6 multicast
    ]

    # Dangerous URL patterns
    DANGEROUS_PATTERNS = [
        r"file://",
        r"data:",
        r"javascript:",
        r"vbscript:",
        r"\\\\",               # UNC paths
        r"@.*:",               # Credentials in URLs
        r"[\x00-\x1f]",       # Control characters
    ]

    # Suspicious hostnames
    SUSPICIOUS_HOSTNAMES = {
        "localhost",
        "127.0.0.1",
        "::1",
        "0.0.0.0",
        "0",
        "metadata.google.internal",
        "169.254.169.254",     # AWS/GCP metadata service
        "100.100.100.200",     # Alibaba Cloud metadata
    }

    def __init__(self, blocked_networks: Optional[List[str]] = None,
                 allowed_schemes: Optional[Set[str]] = None,
                 block_private_ips: bool = True):
        """
        Initialize SSRF protection.

        Args:
            blocked_networks: Custom list of blocked network ranges
            allowed_schemes: Set of allowed URL schemes
            block_private_ips: Whether to block private IP addresses
        """
        self.block_private_ips = block_private_ips
        self.allowed_schemes = allowed_schemes or {"http", "https"}

        # Parse blocked networks
        if blocked_networks is None:
            blocked_networks = self.DEFAULT_BLOCKED_NETWORKS

        self.blocked_networks = []
        for network in blocked_networks:
            try:
                self.blocked_networks.append(ipaddress.ip_network(network, strict=False))
            except ipaddress.AddressValueError:
                pass  # Skip invalid network specifications

        # Compile dangerous patterns
        self.dangerous_pattern = re.compile("|".join(self.DANGEROUS_PATTERNS), re.IGNORECASE)

    def check_url(self, url: str) -> Tuple[bool, Optional[ValidationError]]:
        """
        Check if URL is safe from SSRF perspective.

        Args:
            url: URL to check

        Returns:
            Tuple of (is_safe, error_if_unsafe)
        """
        # Check for dangerous patterns
        if self.dangerous_pattern.search(url):
            return False, ValidationError.security_error(
                ErrorCode.SSRF_DETECTED,
                "URL contains dangerous pattern",
                {"url": url, "reason": "dangerous_pattern"}
            )

        # Parse URL
        try:
            parsed = urlparse(url)
        except Exception as e:
            return False, ValidationError.security_error(
                ErrorCode.SSRF_DETECTED,
                f"Failed to parse URL for SSRF check: {e}",
                {"url": url, "error": str(e)}
            )

        # Check scheme
        if parsed.scheme.lower() not in self.allowed_schemes:
            return False, ValidationError.security_error(
                ErrorCode.SSRF_DETECTED,
                f"Disallowed scheme: {parsed.scheme}",
                {"url": url, "scheme": parsed.scheme, "allowed_schemes": list(self.allowed_schemes)}
            )

        # Check hostname
        if not parsed.hostname:
            return False, ValidationError.security_error(
                ErrorCode.SSRF_DETECTED,
                "URL missing hostname",
                {"url": url}
            )

        return self._check_hostname(parsed.hostname, url)

    def _check_hostname(self, hostname: str, original_url: str) -> Tuple[bool, Optional[ValidationError]]:
        """
        Check if hostname is safe.

        Args:
            hostname: Hostname to check
            original_url: Original URL for error reporting

        Returns:
            Tuple of (is_safe, error_if_unsafe)
        """
        hostname_lower = hostname.lower()

        # Check suspicious hostnames
        if hostname_lower in self.SUSPICIOUS_HOSTNAMES:
            return False, ValidationError.security_error(
                ErrorCode.SSRF_DETECTED,
                f"Suspicious hostname: {hostname}",
                {"url": original_url, "hostname": hostname, "reason": "suspicious_hostname"}
            )

        # Check if it's an IP address
        is_valid_ip, ip_error, ip_obj = IPValidator.validate(hostname)

        if is_valid_ip:
            return self._check_ip_address(ip_obj, original_url)
        else:
            return self._check_domain_name(hostname, original_url)

    def _check_ip_address(self, ip_obj: Union[ipaddress.IPv4Address, ipaddress.IPv6Address],
                         original_url: str) -> Tuple[bool, Optional[ValidationError]]:
        """
        Check if IP address is safe.

        Args:
            ip_obj: IP address object
            original_url: Original URL for error reporting

        Returns:
            Tuple of (is_safe, error_if_unsafe)
        """
        # Check against blocked networks
        for network in self.blocked_networks:
            if ip_obj in network:
                return False, ValidationError.security_error(
                    ErrorCode.PRIVATE_IP_BLOCKED,
                    f"IP address in blocked network: {ip_obj} in {network}",
                    {"url": original_url, "ip": str(ip_obj), "network": str(network)}
                )

        # Additional IP-specific checks
        if self.block_private_ips:
            if ip_obj.is_private:
                return False, ValidationError.security_error(
                    ErrorCode.PRIVATE_IP_BLOCKED,
                    f"Private IP address blocked: {ip_obj}",
                    {"url": original_url, "ip": str(ip_obj), "reason": "private_ip"}
                )

            if ip_obj.is_loopback:
                return False, ValidationError.security_error(
                    ErrorCode.PRIVATE_IP_BLOCKED,
                    f"Loopback IP address blocked: {ip_obj}",
                    {"url": original_url, "ip": str(ip_obj), "reason": "loopback"}
                )

            if ip_obj.is_reserved:
                return False, ValidationError.security_error(
                    ErrorCode.PRIVATE_IP_BLOCKED,
                    f"Reserved IP address blocked: {ip_obj}",
                    {"url": original_url, "ip": str(ip_obj), "reason": "reserved"}
                )

        return True, None

    def _check_domain_name(self, hostname: str, original_url: str) -> Tuple[bool, Optional[ValidationError]]:
        """
        Check if domain name is safe.

        Args:
            hostname: Domain name to check
            original_url: Original URL for error reporting

        Returns:
            Tuple of (is_safe, error_if_unsafe)
        """
        # Check for domain name that might resolve to dangerous IPs
        # This is a basic check - a full implementation might do DNS resolution
        # and check the resolved IPs against blocked networks

        # Check for obvious local domains
        local_domains = [
            "localhost",
            "local",
            "internal",
            "corp",
            "intranet",
        ]

        hostname_parts = hostname.lower().split('.')
        for part in hostname_parts:
            if part in local_domains:
                return False, ValidationError.security_error(
                    ErrorCode.SSRF_DETECTED,
                    f"Suspicious domain name: {hostname}",
                    {"url": original_url, "hostname": hostname, "reason": "local_domain"}
                )

        # Check for homograph attacks (basic check)
        if self._contains_homograph_characters(hostname):
            return False, ValidationError.security_error(
                ErrorCode.SSRF_DETECTED,
                f"Potential homograph attack in domain: {hostname}",
                {"url": original_url, "hostname": hostname, "reason": "homograph"}
            )

        return True, None

    def _contains_homograph_characters(self, hostname: str) -> bool:
        """
        Basic check for homograph attack characters.

        Args:
            hostname: Hostname to check

        Returns:
            True if suspicious characters detected
        """
        # This is a simplified check - a full implementation would be more comprehensive
        suspicious_chars = [
            '\u0430',  # Cyrillic 'a'
            '\u043e',  # Cyrillic 'o'
            '\u0440',  # Cyrillic 'p'
            '\u0440',  # Cyrillic 'r'
            '\u0435',  # Cyrillic 'e'
        ]

        for char in suspicious_chars:
            if char in hostname:
                return True

        return False

    def is_safe_redirect(self, original_url: str, redirect_url: str) -> Tuple[bool, Optional[ValidationError]]:
        """
        Check if a redirect is safe.

        Args:
            original_url: Original URL
            redirect_url: URL being redirected to

        Returns:
            Tuple of (is_safe, error_if_unsafe)
        """
        # Check the redirect URL itself
        is_safe, error = self.check_url(redirect_url)
        if not is_safe:
            return False, error

        # Additional redirect-specific checks
        try:
            original_parsed = urlparse(original_url)
            redirect_parsed = urlparse(redirect_url)

            # Warn about protocol downgrade
            if (original_parsed.scheme == 'https' and
                redirect_parsed.scheme == 'http'):
                return False, ValidationError.security_error(
                    ErrorCode.SSRF_DETECTED,
                    "Redirect from HTTPS to HTTP (protocol downgrade)",
                    {
                        "original_url": original_url,
                        "redirect_url": redirect_url,
                        "reason": "protocol_downgrade"
                    }
                )

            # Check for redirect to different domain (potential open redirect)
            if (original_parsed.hostname and redirect_parsed.hostname and
                original_parsed.hostname.lower() != redirect_parsed.hostname.lower()):
                # This might be legitimate, but we should warn about it
                pass

        except Exception:
            # If we can't parse URLs, be conservative
            return False, ValidationError.security_error(
                ErrorCode.SSRF_DETECTED,
                "Could not validate redirect safety",
                {"original_url": original_url, "redirect_url": redirect_url}
            )

        return True, None

    def add_blocked_network(self, network: str) -> None:
        """
        Add a network to the blocked list.

        Args:
            network: Network in CIDR notation (e.g., "192.168.0.0/16")

        Raises:
            ValueError: If network format is invalid
        """
        try:
            network_obj = ipaddress.ip_network(network, strict=False)
            self.blocked_networks.append(network_obj)
        except ipaddress.AddressValueError as e:
            raise ValueError(f"Invalid network format: {network} - {e}")

    def remove_blocked_network(self, network: str) -> bool:
        """
        Remove a network from the blocked list.

        Args:
            network: Network in CIDR notation

        Returns:
            True if network was found and removed
        """
        try:
            network_obj = ipaddress.ip_network(network, strict=False)
            if network_obj in self.blocked_networks:
                self.blocked_networks.remove(network_obj)
                return True
        except ipaddress.AddressValueError:
            pass

        return False

    def get_blocked_networks(self) -> List[str]:
        """
        Get list of blocked networks.

        Returns:
            List of blocked networks in CIDR notation
        """
        return [str(network) for network in self.blocked_networks]