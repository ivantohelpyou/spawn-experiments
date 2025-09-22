#!/usr/bin/env python3
"""
Basic usage examples for the URL Validator library.

This script demonstrates the fundamental functionality of the URL validator
including single URL validation, batch processing, and error handling.
"""

from url_validator import validate_url, validate_urls, URLValidator, ValidationConfig


def example_single_url_validation():
    """Demonstrate single URL validation."""
    print("=== Single URL Validation ===")

    # Basic validation (format + accessibility)
    result = validate_url("https://example.com")
    print(f"URL: {result.url}")
    print(f"Valid: {result.is_valid}")
    print(f"Accessible: {result.is_accessible}")
    print(f"Duration: {result.duration:.3f}s")

    if result.errors:
        print("Errors:")
        for error in result.errors:
            print(f"  - [{error.code}] {error.message}")

    print()


def example_format_only_validation():
    """Demonstrate format-only validation."""
    print("=== Format-Only Validation ===")

    # Skip accessibility check for faster validation
    result = validate_url("https://example.com", check_accessibility=False)
    print(f"URL: {result.url}")
    print(f"Valid format: {result.is_valid}")
    print(f"Accessibility checked: {result.accessibility_result is not None}")
    print(f"Duration: {result.duration:.3f}s")

    print()


def example_batch_validation():
    """Demonstrate batch URL validation."""
    print("=== Batch Validation ===")

    urls = [
        "https://google.com",
        "https://github.com",
        "https://example.com",
        "invalid-url",
        "https://nonexistent-domain-12345.com"
    ]

    print(f"Validating {len(urls)} URLs...")
    results = validate_urls(urls)

    print("Results:")
    for result in results:
        status = "✓" if result.is_valid else "✗"
        accessible = "✓" if result.is_accessible else "✗"
        print(f"  {status} {result.url}")
        print(f"    Format: {result.is_valid}, Accessible: {result.is_accessible}")

        if result.errors:
            for error in result.errors[:2]:  # Show first 2 errors
                print(f"    Error: [{error.code}] {error.message}")

    print()


def example_custom_configuration():
    """Demonstrate custom configuration."""
    print("=== Custom Configuration ===")

    # Create custom configuration
    config = ValidationConfig(
        timeout=30,
        max_redirects=10,
        verify_ssl=False,
        user_agent="CustomBot/1.0",
        allowed_schemes={"http", "https"},
        block_private_ips=True
    )

    # Use with context manager
    with URLValidator(config) as validator:
        result = validator.validate("http://example.com")
        print(f"Custom validation result: {result.is_valid}")

        # Test private IP blocking
        result = validator.validate("https://127.0.0.1")
        print(f"Localhost validation (should fail with blocking): {result.is_valid}")

    print()


def example_predefined_configurations():
    """Demonstrate predefined configurations."""
    print("=== Predefined Configurations ===")

    test_url = "http://example.com"

    # Permissive configuration (for development)
    print("Permissive configuration:")
    permissive_config = ValidationConfig.create_permissive()
    result = validate_url(test_url, config=permissive_config)
    print(f"  HTTP allowed: {result.is_valid}")

    # Strict configuration (for production)
    print("Strict configuration:")
    strict_config = ValidationConfig.create_strict()
    result = validate_url(test_url, config=strict_config)
    print(f"  HTTP allowed: {result.is_valid} (should be False - HTTPS only)")

    # Fast configuration (for performance)
    print("Fast configuration:")
    fast_config = ValidationConfig.create_fast()
    result = validate_url("https://example.com", config=fast_config)
    print(f"  Fast validation: {result.is_valid}")

    print()


def example_error_handling():
    """Demonstrate comprehensive error handling."""
    print("=== Error Handling ===")

    test_cases = [
        ("", "Empty URL"),
        ("not-a-url", "Invalid format"),
        ("https://", "Missing domain"),
        ("https://example.com:99999", "Invalid port"),
        ("javascript:alert('xss')", "Dangerous scheme"),
    ]

    for url, description in test_cases:
        print(f"Testing: {description}")
        result = validate_url(url)

        print(f"  URL: '{url}'")
        print(f"  Valid: {result.is_valid}")

        if result.errors:
            print("  Errors:")
            for error in result.errors:
                print(f"    - [{error.code}] {error.category.value}: {error.message}")

        if result.warnings:
            print("  Warnings:")
            for warning in result.warnings:
                print(f"    - {warning}")

        print()


def example_url_components():
    """Demonstrate URL component extraction."""
    print("=== URL Components ===")

    complex_url = "https://user:pass@sub.example.com:8080/path/to/resource?param1=value1&param2=value2#section"

    result = validate_url(complex_url, check_accessibility=False)

    if result.url_components:
        components = result.url_components
        print(f"Original URL: {complex_url}")
        print(f"Scheme: {components.scheme}")
        print(f"Username: {components.username}")
        print(f"Password: {'*' * len(components.password) if components.password else None}")
        print(f"Hostname: {components.hostname}")
        print(f"Port: {components.port}")
        print(f"Path: {components.path}")
        print(f"Query: {components.query}")
        print(f"Fragment: {components.fragment}")
        print(f"Is secure: {components.is_secure}")
        print(f"Has auth: {components.has_auth}")

    print()


def example_result_export():
    """Demonstrate result export formats."""
    print("=== Result Export ===")

    result = validate_url("https://example.com")

    # Export as dictionary
    print("As dictionary:")
    result_dict = result.to_dict()
    print(f"  Keys: {list(result_dict.keys())}")

    # Export as JSON
    print("As JSON (truncated):")
    json_output = result.to_json(indent=2)
    print(f"  {json_output[:200]}...")

    # Get summary
    print("Summary:")
    summary = result.get_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")

    print()


def main():
    """Run all examples."""
    print("URL Validator - Basic Usage Examples")
    print("=" * 50)
    print()

    try:
        example_single_url_validation()
        example_format_only_validation()
        example_batch_validation()
        example_custom_configuration()
        example_predefined_configurations()
        example_error_handling()
        example_url_components()
        example_result_export()

        print("All examples completed successfully!")

    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()