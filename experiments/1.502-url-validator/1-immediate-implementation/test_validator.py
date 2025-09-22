#!/usr/bin/env python3
"""
Test script for URL validator
"""

from url_validator import URLValidator, validate_url


def test_format_validation():
    """Test URL format validation without network requests."""
    print("Testing URL Format Validation")
    print("-" * 40)

    test_cases = [
        ("https://www.example.com", True),
        ("http://localhost", True),
        ("https://subdomain.example.org/path", True),
        ("invalid-url", False),
        ("ftp://example.com", False),
        ("https://", False),
        ("", False),
        ("   ", False),
        ("http://example", False),  # No TLD
        ("https://example.com:8080/path?query=value#fragment", True),
    ]

    validator = URLValidator()

    for url, expected in test_cases:
        is_valid, error = validator.is_valid_format(url)
        status = "PASS" if is_valid == expected else "FAIL"
        print(f"{status}: '{url}' -> Valid: {is_valid}")
        if error:
            print(f"      Error: {error}")


def test_accessibility():
    """Test URL accessibility with real network requests."""
    print("\nTesting URL Accessibility")
    print("-" * 40)

    # Test with some reliable URLs
    test_urls = [
        "https://httpbin.org/status/200",  # Should be accessible
        "https://httpbin.org/status/404",  # Should return 404
        "https://nonexistent-domain-99999.com",  # Should fail connection
        "https://www.google.com",  # Should be accessible
    ]

    validator = URLValidator(timeout=10)

    for url in test_urls:
        print(f"\nTesting: {url}")
        is_accessible, message, status_code = validator.is_accessible(url)
        print(f"  Accessible: {is_accessible}")
        print(f"  Message: {message}")
        if status_code:
            print(f"  Status Code: {status_code}")


def test_comprehensive_validation():
    """Test the comprehensive validation function."""
    print("\nComprehensive Validation Test")
    print("-" * 40)

    urls = [
        "https://www.python.org",
        "http://httpbin.org/json",
        "invalid-url-format",
        "https://definitely-not-a-real-domain-12345.com"
    ]

    for url in urls:
        print(f"\nValidating: {url}")
        result = validate_url(url, timeout=8)

        print(f"  Format Valid: {result['is_valid_format']}")
        if result['format_error']:
            print(f"  Format Error: {result['format_error']}")

        if result['is_accessible'] is not None:
            print(f"  Accessible: {result['is_accessible']}")
            if result['status_code']:
                print(f"  HTTP Status: {result['status_code']}")

        if result['parsed_components']:
            comp = result['parsed_components']
            print(f"  Parsed -> Scheme: {comp['scheme']}, Domain: {comp['netloc']}")


if __name__ == "__main__":
    test_format_validation()
    test_accessibility()
    test_comprehensive_validation()