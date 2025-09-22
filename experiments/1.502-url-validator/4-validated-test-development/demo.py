#!/usr/bin/env python3
"""
Demonstration script for the URL validator.

This script shows how to use the URLValidator class for comprehensive URL validation
including format checking, accessibility verification, and security analysis.
"""

from url_validator import URLValidator
import json


def main():
    """Demonstrate URL validator functionality."""
    print("=" * 60)
    print("URL Validator Demonstration")
    print("=" * 60)

    # Initialize validator
    validator = URLValidator(timeout=5)

    # Test URLs with various characteristics
    test_urls = [
        "https://www.example.com",                    # Valid URL
        "http://192.168.1.1",                        # Private IP
        "javascript:alert('XSS')",                   # Malicious JavaScript
        "https://bit.ly/test",                       # URL shortener
        "http://example.com:22",                     # Dangerous port
        "not-a-url",                                 # Invalid format
        "https://еxample.com",                       # Homograph attack
        "https://example.com?param=%3Cscript%3E",   # Encoded malicious content
        "ftp://ftp.example.com",                     # FTP protocol
        "https://example.com/" + "a" * 2100,        # Very long URL
    ]

    print("\n1. Format Validation:")
    print("-" * 30)
    for url in test_urls:
        is_valid = validator.is_valid_format(url)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{status:12} | {url[:50]}")

    print("\n2. Security Analysis:")
    print("-" * 30)
    for url in test_urls[:6]:  # Test subset for security
        is_secure, issues = validator.is_secure_url(url)
        status = "✓ SECURE" if is_secure else "⚠ UNSAFE"
        print(f"{status:12} | {url[:50]}")
        if issues:
            for issue in issues[:2]:  # Show first 2 issues
                print(f"              Issue: {issue}")

    print("\n3. Comprehensive Validation (simulated):")
    print("-" * 50)
    # Note: Accessibility checking requires actual network requests
    # For demo purposes, we'll show the structure without real network calls
    sample_url = "https://www.example.com"

    print(f"Analyzing: {sample_url}")

    # Format validation
    format_valid = validator.is_valid_format(sample_url)
    print(f"Format Valid: {format_valid}")

    # Security validation
    is_secure, security_issues = validator.is_secure_url(sample_url)
    print(f"Security Status: {'Secure' if is_secure else 'Issues found'}")

    if security_issues:
        print("Security Issues:")
        for issue in security_issues:
            print(f"  - {issue}")

    # Accessibility (would require network access in real scenario)
    print("Accessibility: Would check via HTTP request in real usage")

    print("\n" + "=" * 60)
    print("URL Validator Features Summary:")
    print("=" * 60)
    print("✓ Format validation using urllib.parse")
    print("✓ Protocol validation (http, https, ftp, ftps)")
    print("✓ Domain and IP address validation")
    print("✓ Port range validation (1-65535)")
    print("✓ Security pattern detection")
    print("✓ Malicious URL encoding detection")
    print("✓ Suspicious domain detection")
    print("✓ Homograph attack detection")
    print("✓ Network accessibility checking (with requests)")
    print("✓ Comprehensive error handling")
    print("✓ Extensive test coverage with TDD validation")


if __name__ == "__main__":
    main()