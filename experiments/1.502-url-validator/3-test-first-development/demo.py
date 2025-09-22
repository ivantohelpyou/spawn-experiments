#!/usr/bin/env python3
"""
Demonstration of the URL Validator built using Test-Driven Development.
"""

from url_validator import URLValidator


def main():
    validator = URLValidator()

    # Test URLs to demonstrate functionality
    test_urls = [
        "https://www.google.com",
        "http://example.com",
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",
        "ftp://example.com",
        "example.com",
        "http://",
        "",
        None,
        "http://this-domain-should-not-exist-12345.com"
    ]

    print("URL Validator Demo - Test-Driven Development")
    print("=" * 50)

    for url in test_urls:
        print(f"\nTesting URL: {repr(url)}")

        # Format validation
        valid = validator.is_valid(url)
        print(f"  Valid format: {valid}")

        # Accessibility check (only if format is valid)
        if valid:
            accessible = validator.is_accessible(url)
            print(f"  Accessible: {accessible}")

            # Complete validation
            complete = validator.validate_completely(url)
            print(f"  Complete check: {complete}")
        else:
            print(f"  Accessible: N/A (invalid format)")
            print(f"  Complete check: {{'valid': False, 'accessible': False}}")


if __name__ == "__main__":
    main()