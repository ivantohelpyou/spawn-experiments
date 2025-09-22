#!/usr/bin/env python3
"""
Demo script showing URL validator usage examples
"""

from url_validator import URLValidator, validate_url


def demo_basic_usage():
    """Demonstrate basic URL validation usage."""
    print("Basic URL Validation Demo")
    print("=" * 40)

    # Simple validation examples
    urls = [
        "https://www.example.com",
        "http://localhost:3000",
        "https://api.github.com/user",
        "invalid-url",
        "https://192.168.1.1:8080"
    ]

    for url in urls:
        result = validate_url(url)
        print(f"\nURL: {url}")
        print(f"  Valid Format: {result['is_valid_format']}")
        if result['is_accessible'] is not None:
            print(f"  Accessible: {result['is_accessible']}")


def demo_format_only():
    """Demonstrate format-only validation (no network requests)."""
    print("\n\nFormat-Only Validation Demo")
    print("=" * 40)

    urls = [
        "https://www.example.com/path?param=value#section",
        "http://subdomain.domain.org:8080",
        "ftp://invalid-scheme.com",
        "just-a-string"
    ]

    for url in urls:
        # Validate format only, skip accessibility check
        result = validate_url(url, check_accessibility=False)
        print(f"\nURL: {url}")
        print(f"  Valid Format: {result['is_valid_format']}")
        if result['format_error']:
            print(f"  Error: {result['format_error']}")
        if result['parsed_components']:
            comp = result['parsed_components']
            print(f"  Components: {comp['scheme']}://{comp['netloc']}{comp['path']}")


def demo_edge_cases():
    """Demonstrate handling of edge cases."""
    print("\n\nEdge Cases Demo")
    print("=" * 40)

    edge_cases = [
        "",  # Empty string
        "   ",  # Whitespace only
        "https://",  # Missing domain
        "www.example.com",  # Missing scheme
        "https://example",  # Domain without TLD
        "https://example.com:99999",  # High port number
        "https://192.168.1.1",  # IP address
        "http://localhost",  # Localhost
    ]

    validator = URLValidator()

    for url in edge_cases:
        is_valid, error = validator.is_valid_format(url)
        print(f"\nURL: '{url}'")
        print(f"  Valid: {is_valid}")
        if error:
            print(f"  Error: {error}")


def demo_custom_timeout():
    """Demonstrate custom timeout settings."""
    print("\n\nCustom Timeout Demo")
    print("=" * 40)

    # Create validator with short timeout
    fast_validator = URLValidator(timeout=2)

    url = "https://httpbin.org/delay/5"  # This URL delays response by 5 seconds
    print(f"Testing {url} with 2-second timeout...")

    is_accessible, message, status = fast_validator.is_accessible(url)
    print(f"  Accessible: {is_accessible}")
    print(f"  Message: {message}")


if __name__ == "__main__":
    demo_basic_usage()
    demo_format_only()
    demo_edge_cases()
    demo_custom_timeout()