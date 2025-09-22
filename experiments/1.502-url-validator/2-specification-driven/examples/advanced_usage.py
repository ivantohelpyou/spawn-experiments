#!/usr/bin/env python3
"""
Advanced usage examples for the URL Validator library.

This script demonstrates advanced features including security features,
performance optimization, custom configurations, and integration patterns.
"""

import time
import threading
from concurrent.futures import ThreadPoolExecutor
from url_validator import URLValidator, ValidationConfig
from url_validator.security import SSRFProtection, InputSanitizer, RateLimiter, RateLimitConfig


def example_security_features():
    """Demonstrate security features."""
    print("=== Security Features ===")

    # SSRF Protection
    print("SSRF Protection:")
    ssrf = SSRFProtection(block_private_ips=True)

    test_urls = [
        "https://example.com",           # Safe
        "https://127.0.0.1",            # Should be blocked
        "https://192.168.1.1",          # Should be blocked
        "file:///etc/passwd",           # Dangerous scheme
        "javascript:alert('xss')",      # Dangerous scheme
    ]

    for url in test_urls:
        is_safe, error = ssrf.check_url(url)
        status = "✓ SAFE" if is_safe else "✗ BLOCKED"
        print(f"  {status}: {url}")
        if error:
            print(f"    Reason: {error.message}")

    print()

    # Input Sanitization
    print("Input Sanitization:")
    sanitizer = InputSanitizer(max_length=100)

    test_inputs = [
        "  https://example.com  ",      # Whitespace
        "https://example.com\x00",      # Null byte
        "https://example.com" + "x" * 200,  # Too long
        "<script>alert('xss')</script>",     # Malicious
    ]

    for input_url in test_inputs:
        clean_url, error = sanitizer.sanitize(input_url)
        if error:
            print(f"  ✗ REJECTED: {input_url[:50]}...")
            print(f"    Reason: {error.message}")
        else:
            print(f"  ✓ CLEANED: {input_url[:30]}... → {clean_url[:30]}...")

    print()

    # Rate Limiting
    print("Rate Limiting:")
    rate_config = RateLimitConfig(requests_per_minute=5, requests_per_hour=50)
    limiter = RateLimiter(rate_config)

    client_id = "test_client"
    for i in range(7):  # Try 7 requests (should hit limit)
        allowed, error = limiter.check_rate_limit(client_id)
        status = "✓ ALLOWED" if allowed else "✗ RATE LIMITED"
        print(f"  Request {i+1}: {status}")
        if error:
            print(f"    Reason: {error.message}")

    print()


def example_performance_optimization():
    """Demonstrate performance optimization techniques."""
    print("=== Performance Optimization ===")

    urls = [
        "https://google.com",
        "https://github.com",
        "https://stackoverflow.com",
        "https://python.org",
        "https://example.com",
    ] * 4  # 20 URLs total

    # Sequential validation (baseline)
    print("Sequential validation:")
    start_time = time.time()
    config = ValidationConfig(timeout=5)

    with URLValidator(config) as validator:
        results = []
        for url in urls:
            result = validator.validate(url, check_accessibility=False)  # Skip network calls for demo
            results.append(result)

    sequential_time = time.time() - start_time
    print(f"  Time: {sequential_time:.3f}s for {len(urls)} URLs")

    # Batch validation (optimized)
    print("Batch validation:")
    start_time = time.time()

    with URLValidator(config) as validator:
        results = validator.validate_batch(
            urls,
            check_accessibility=False,  # Skip network calls for demo
            max_workers=10
        )

    batch_time = time.time() - start_time
    print(f"  Time: {batch_time:.3f}s for {len(urls)} URLs")

    speedup = sequential_time / batch_time if batch_time > 0 else float('inf')
    print(f"  Speedup: {speedup:.1f}x")

    print()


def example_custom_validators():
    """Demonstrate custom validation logic."""
    print("=== Custom Validation Logic ===")

    class CustomURLValidator(URLValidator):
        """Custom validator with additional business rules."""

        def __init__(self, config=None):
            super().__init__(config)
            self.blocked_domains = {"blocked-site.com", "malicious.org"}
            self.required_keywords = ["api", "secure"]

        def validate(self, url, check_accessibility=True):
            # Run standard validation first
            result = super().validate(url, check_accessibility)

            # Add custom business rules
            if result.is_valid and result.url_components:
                hostname = result.url_components.hostname

                # Check blocked domains
                if hostname in self.blocked_domains:
                    from url_validator.models.error import ValidationError, ErrorCode
                    result.add_error(ValidationError.security_error(
                        ErrorCode.SSRF_DETECTED,
                        f"Domain is blocked: {hostname}",
                        {"domain": hostname}
                    ))

                # Check required keywords in path
                path = result.url_components.path.lower()
                if not any(keyword in path for keyword in self.required_keywords):
                    result.add_warning(f"URL path should contain one of: {self.required_keywords}")

            return result

    # Test custom validator
    custom_validator = CustomURLValidator()

    test_urls = [
        "https://blocked-site.com/api/endpoint",  # Blocked domain
        "https://example.com/public/data",        # Missing required keyword
        "https://example.com/api/secure/data",    # Valid
    ]

    for url in test_urls:
        result = custom_validator.validate(url, check_accessibility=False)
        print(f"URL: {url}")
        print(f"  Valid: {result.is_valid}")

        if result.errors:
            for error in result.errors:
                print(f"  Error: {error.message}")

        if result.warnings:
            for warning in result.warnings:
                print(f"  Warning: {warning}")

        print()

    custom_validator.close()


def example_async_patterns():
    """Demonstrate async-like patterns using threading."""
    print("=== Async-like Patterns ===")

    urls = [
        "https://httpbin.org/delay/1",  # Simulated slow endpoint
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",
        "https://httpbin.org/redirect/3",
    ]

    results = {}
    errors = {}

    def validate_url_async(url, validator):
        """Validate URL in separate thread."""
        try:
            result = validator.validate(url)
            results[url] = result
        except Exception as e:
            errors[url] = e

    # Create validator outside threads
    config = ValidationConfig(timeout=10)
    validator = URLValidator(config)

    try:
        # Start all validations concurrently
        threads = []
        for url in urls:
            thread = threading.Thread(target=validate_url_async, args=(url, validator))
            threads.append(thread)
            thread.start()

        # Wait for all to complete
        for thread in threads:
            thread.join()

        print("Async validation results:")
        for url in urls:
            if url in results:
                result = results[url]
                print(f"  ✓ {url}: Valid={result.is_valid}, Accessible={result.is_accessible}")
            elif url in errors:
                print(f"  ✗ {url}: Error={errors[url]}")

    finally:
        validator.close()

    print()


def example_configuration_management():
    """Demonstrate advanced configuration management."""
    print("=== Configuration Management ===")

    # Configuration inheritance and modification
    base_config = ValidationConfig(
        timeout=10,
        max_redirects=5,
        verify_ssl=True
    )

    # Create development configuration
    dev_config = base_config.update(
        verify_ssl=False,
        block_private_ips=False,
        log_level="DEBUG"
    )

    # Create production configuration
    prod_config = base_config.update(
        timeout=5,
        allowed_schemes={"https"},
        block_private_ips=True,
        log_level="WARNING"
    )

    print("Configuration comparison:")
    configs = {
        "Base": base_config,
        "Development": dev_config,
        "Production": prod_config
    }

    for name, config in configs.items():
        print(f"  {name}:")
        print(f"    Timeout: {config.timeout}s")
        print(f"    SSL Verify: {config.verify_ssl}")
        print(f"    Block Private IPs: {config.block_private_ips}")
        print(f"    Allowed Schemes: {list(config.allowed_schemes)}")
        print(f"    Log Level: {config.log_level}")

    # Configuration serialization
    print("Configuration serialization:")
    config_dict = prod_config.to_dict()
    print(f"  Dict keys: {list(config_dict.keys())}")

    # Recreate from dict
    recreated_config = ValidationConfig.from_dict(config_dict)
    print(f"  Recreated timeout: {recreated_config.timeout}")

    print()


def example_monitoring_and_metrics():
    """Demonstrate monitoring and metrics collection."""
    print("=== Monitoring and Metrics ===")

    class MonitoringValidator(URLValidator):
        """Validator with built-in metrics collection."""

        def __init__(self, config=None):
            super().__init__(config)
            self.metrics = {
                "total_validations": 0,
                "valid_urls": 0,
                "accessible_urls": 0,
                "errors_by_code": {},
                "total_duration": 0.0,
            }

        def validate(self, url, check_accessibility=True):
            result = super().validate(url, check_accessibility)

            # Collect metrics
            self.metrics["total_validations"] += 1
            if result.is_valid:
                self.metrics["valid_urls"] += 1
            if result.is_accessible:
                self.metrics["accessible_urls"] += 1

            for error in result.errors:
                code = error.code
                self.metrics["errors_by_code"][code] = \
                    self.metrics["errors_by_code"].get(code, 0) + 1

            self.metrics["total_duration"] += result.duration

            return result

        def get_metrics(self):
            """Get collected metrics."""
            if self.metrics["total_validations"] > 0:
                avg_duration = self.metrics["total_duration"] / self.metrics["total_validations"]
                success_rate = self.metrics["accessible_urls"] / self.metrics["total_validations"] * 100
            else:
                avg_duration = 0.0
                success_rate = 0.0

            return {
                **self.metrics,
                "average_duration": avg_duration,
                "success_rate": success_rate
            }

    # Test monitoring validator
    monitor_validator = MonitoringValidator()

    test_urls = [
        "https://google.com",
        "https://example.com",
        "invalid-url",
        "https://nonexistent-12345.com",
        "https://github.com"
    ]

    print("Validating URLs with monitoring...")
    for url in test_urls:
        result = monitor_validator.validate(url, check_accessibility=False)
        print(f"  {url}: Valid={result.is_valid}")

    # Show metrics
    metrics = monitor_validator.get_metrics()
    print("Collected metrics:")
    for key, value in metrics.items():
        if key == "errors_by_code":
            print(f"  {key}:")
            for error_code, count in value.items():
                print(f"    {error_code}: {count}")
        else:
            print(f"  {key}: {value}")

    monitor_validator.close()
    print()


def example_integration_patterns():
    """Demonstrate integration with other systems."""
    print("=== Integration Patterns ===")

    # Database-like storage pattern
    class URLValidationCache:
        """Simple cache for validation results."""

        def __init__(self):
            self.cache = {}

        def get(self, url):
            return self.cache.get(url)

        def set(self, url, result):
            # Store only essential data to save memory
            self.cache[url] = {
                "is_valid": result.is_valid,
                "is_accessible": result.is_accessible,
                "timestamp": result.timestamp,
                "error_codes": result.error_codes
            }

        def invalidate(self, url):
            self.cache.pop(url, None)

    # Cached validator
    class CachedValidator:
        """Validator with caching support."""

        def __init__(self, config=None):
            self.validator = URLValidator(config)
            self.cache = URLValidationCache()

        def validate(self, url, use_cache=True):
            if use_cache:
                cached = self.cache.get(url)
                if cached:
                    print(f"  Cache hit for: {url}")
                    return cached

            result = self.validator.validate(url, check_accessibility=False)
            self.cache.set(url, result)
            print(f"  Cache miss for: {url}")
            return result

        def close(self):
            self.validator.close()

    # Test cached validator
    cached_validator = CachedValidator()

    test_url = "https://example.com"

    print("Testing validation cache:")
    # First call - cache miss
    result1 = cached_validator.validate(test_url)

    # Second call - cache hit
    result2 = cached_validator.validate(test_url)

    cached_validator.close()
    print()


def main():
    """Run all advanced examples."""
    print("URL Validator - Advanced Usage Examples")
    print("=" * 50)
    print()

    try:
        example_security_features()
        example_performance_optimization()
        example_custom_validators()
        example_async_patterns()
        example_configuration_management()
        example_monitoring_and_metrics()
        example_integration_patterns()

        print("All advanced examples completed successfully!")

    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()