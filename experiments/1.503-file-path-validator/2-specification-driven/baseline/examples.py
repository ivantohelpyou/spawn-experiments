#!/usr/bin/env python3
"""
Example usage of the File Path Validator library.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the path_validator to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from path_validator import (
    PathValidator,
    ValidationConfig,
    SecurityPolicy,
    SymlinkPolicy,
    validate_path,
    is_valid_path,
    BatchPathValidator,
    ValidatedPath,
    validate_path_args,
)


def example_basic_validation():
    """Example 1: Basic path validation."""
    print("Example 1: Basic Path Validation")
    print("-" * 40)

    # Create a validator with default settings
    validator = PathValidator()

    # Test various paths
    test_paths = [
        'documents/file.txt',
        '/absolute/path/to/file.log',
        '../../../etc/passwd',  # Traversal attack
        'normal_file.doc',
        'CON.txt',  # Windows reserved name
    ]

    for path in test_paths:
        result = validator.validate(path)
        status = "✓ VALID" if result.valid else "✗ INVALID"
        print(f"{status:10} | {path}")

        if not result.valid:
            print(f"           Error: {result.error}")
            if result.suggestions:
                print(f"           Suggestions: {', '.join(result.suggestions)}")
        elif result.normalized_path != path:
            print(f"           Normalized: {result.normalized_path}")

    print()


def example_security_configuration():
    """Example 2: Security-focused validation."""
    print("Example 2: Security-Focused Configuration")
    print("-" * 45)

    # Create security policy
    security_policy = SecurityPolicy(
        prevent_traversal=True,
        sanitize_input=True,
        symlink_policy=SymlinkPolicy.FORBID,
        max_path_length=1000
    )

    # Create validator with security policy
    config = ValidationConfig(
        strict_mode=True,
        security_policy=security_policy
    )
    validator = PathValidator(config)

    # Test potentially malicious paths
    malicious_paths = [
        '../../../etc/passwd',
        'file.txt\x00.exe',  # Null byte injection
        'normal/path/../../../sensitive',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',  # URL encoded traversal
    ]

    print("Testing malicious paths:")
    for path in malicious_paths:
        result = validator.validate(path)
        if result.valid:
            print(f"⚠️  UNEXPECTED: {path} was accepted")
        else:
            print(f"🛡️  BLOCKED: {path}")
            print(f"    Reason: {result.error}")

    print()


def example_cross_platform_validation():
    """Example 3: Cross-platform validation."""
    print("Example 3: Cross-Platform Validation")
    print("-" * 42)

    # Test same paths on different platforms
    test_path = "documents/project/file.txt"

    platforms = ['windows', 'posix']
    for platform in platforms:
        config = ValidationConfig(target_platform=platform)
        validator = PathValidator(config)

        result = validator.validate(test_path)
        print(f"{platform.capitalize():8} | {test_path} -> {result.normalized_path}")

    # Test platform-specific features
    print("\nPlatform-specific tests:")

    # Windows reserved names
    windows_config = ValidationConfig(target_platform='windows')
    windows_validator = PathValidator(windows_config)

    result = windows_validator.validate('CON.txt')
    print(f"Windows  | CON.txt -> {'Valid' if result.valid else 'Invalid (reserved name)'}")

    # POSIX case sensitivity
    posix_config = ValidationConfig(target_platform='posix')
    posix_validator = PathValidator(posix_config)

    result = posix_validator.validate('File.TXT')
    print(f"POSIX    | File.TXT -> Valid (case-sensitive)")

    print()


def example_batch_processing():
    """Example 4: High-performance batch processing."""
    print("Example 4: Batch Processing")
    print("-" * 32)

    # Create a large list of paths to validate
    test_paths = []
    for i in range(100):
        test_paths.extend([
            f'documents/file_{i}.txt',
            f'logs/system_{i}.log',
            f'../invalid/traversal_{i}',  # Some invalid paths
            f'temp/data_{i}.tmp',
        ])

    print(f"Validating {len(test_paths)} paths...")

    # Create batch validator
    batch_validator = BatchPathValidator()

    # Validate with performance comparison
    result = batch_validator.validate_batch(test_paths, parallel=True)

    print(f"Results:")
    print(f"  Total paths: {result.total_count}")
    print(f"  Valid paths: {result.valid_count}")
    print(f"  Invalid paths: {result.invalid_count}")
    print(f"  Success rate: {result.success_rate:.1f}%")

    # Show error breakdown
    if result.error_counts:
        print(f"  Error types:")
        for error_type, count in result.error_counts.items():
            print(f"    {error_type}: {count}")

    # Filter only valid paths
    valid_paths = batch_validator.filter_valid_paths(test_paths[:10])
    print(f"  First 10 valid paths: {len(valid_paths)} found")

    print()


def example_file_operations():
    """Example 5: Integration with file operations."""
    print("Example 5: Integration with File Operations")
    print("-" * 47)

    # Create a temporary directory for demonstration
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Working in: {temp_dir}")

        # Configure validator to check existence
        config = ValidationConfig(
            check_existence=True,
            require_absolute=False
        )
        validator = PathValidator(config)

        # Test with existing and non-existing files
        test_file = os.path.join(temp_dir, 'test_file.txt')

        # Create the file
        Path(test_file).write_text("Test content")

        # Validate existing file
        result = validator.validate(test_file)
        print(f"Existing file: {result.valid}")
        if result.existence_info:
            print(f"  Is file: {result.existence_info.is_file}")
            print(f"  Is readable: {result.existence_info.is_readable}")
            print(f"  Size: {result.existence_info.size} bytes")

        # Validate non-existing file
        non_existing = os.path.join(temp_dir, 'does_not_exist.txt')
        result = validator.validate(non_existing)
        print(f"Non-existing file: {result.valid}")
        if result.existence_info:
            print(f"  Exists: {result.existence_info.exists}")

    print()


def example_pathlib_integration():
    """Example 6: Integration with pathlib."""
    print("Example 6: Pathlib Integration")
    print("-" * 34)

    # Use ValidatedPath - a Path subclass with validation
    try:
        # Valid path
        validated_path = ValidatedPath('documents', 'project', 'file.txt')
        print(f"Valid path created: {validated_path}")

        # Try to join with invalid component
        safe_join = validated_path.joinpath('safe_file.log')
        print(f"Safe join result: {safe_join}")

        # This would raise an error if the path was invalid
        # invalid_path = ValidatedPath('../../../etc/passwd')

    except Exception as e:
        print(f"Validation error: {e}")

    # Using regular pathlib with validation
    regular_path = Path('documents/file.txt')
    result = validate_path(regular_path)
    print(f"Regular Path validation: {'Valid' if result.valid else 'Invalid'}")

    print()


def example_decorator_usage():
    """Example 7: Using validation decorators."""
    print("Example 7: Decorator Usage")
    print("-" * 31)

    # Define a function that processes files
    @validate_path_args('input_file', 'output_file')
    def process_file(input_file, output_file, verbose=False):
        """Process a file with validated paths."""
        if verbose:
            print(f"Processing: {input_file} -> {output_file}")
        return f"Processed {input_file}"

    try:
        # Valid usage
        result = process_file('input.txt', 'output.txt', verbose=True)
        print(f"Success: {result}")

        # This would raise an error due to path traversal
        # process_file('../../../etc/passwd', 'output.txt')

    except Exception as e:
        print(f"Validation prevented unsafe operation: {e}")

    print()


def example_custom_rules():
    """Example 8: Custom validation rules."""
    print("Example 8: Custom Validation Rules")
    print("-" * 38)

    from path_validator.core.rules import ValidationRules, CustomRule, ExtensionRule

    # Create custom validation rules
    rules = ValidationRules()

    # Add custom rule for allowed extensions
    rules.add_rule(ExtensionRule(
        allowed_extensions=['.txt', '.log', '.md'],
        forbidden_extensions=['.exe', '.bat', '.sh']
    ))

    # Add custom rule for naming convention
    def validate_naming_convention(path):
        """Only allow lowercase filenames with underscores."""
        filename = os.path.basename(path)
        return filename.islower() and ' ' not in filename

    rules.add_rule(CustomRule(
        name='naming_convention',
        validator_func=validate_naming_convention,
        error_message='Filename must be lowercase without spaces'
    ))

    # Test paths against custom rules
    test_paths = [
        'document.txt',        # Valid
        'Document.TXT',        # Invalid case
        'file with spaces.txt', # Invalid spaces
        'script.exe',          # Invalid extension
        'valid_file.log',      # Valid
    ]

    print("Testing custom rules:")
    for path in test_paths:
        results = rules.validate_all(path)
        errors = [r for r in results if not r.passed]

        if errors:
            print(f"✗ {path}")
            for error in errors:
                print(f"    {error.message}")
        else:
            print(f"✓ {path}")

    print()


def example_performance_monitoring():
    """Example 9: Performance monitoring."""
    print("Example 9: Performance Monitoring")
    print("-" * 38)

    # Create paths for performance testing
    test_paths = [f'path_{i}/file_{i}.txt' for i in range(1000)]

    batch_validator = BatchPathValidator()

    # Run performance benchmark
    print("Running performance benchmark...")
    perf_results = batch_validator.benchmark_performance(test_paths, iterations=3)

    print(f"Performance Results:")
    print(f"  Paths tested: {perf_results['path_count']}")
    print(f"  Sequential: {perf_results['sequential']['throughput_per_sec']:.0f} paths/sec")
    print(f"  Parallel: {perf_results['parallel']['throughput_per_sec']:.0f} paths/sec")
    print(f"  Speedup: {perf_results['speedup']:.1f}x")

    print()


def main():
    """Run all examples."""
    print("File Path Validator - Usage Examples")
    print("=" * 50)
    print()

    examples = [
        example_basic_validation,
        example_security_configuration,
        example_cross_platform_validation,
        example_batch_processing,
        example_file_operations,
        example_pathlib_integration,
        example_decorator_usage,
        example_custom_rules,
        example_performance_monitoring,
    ]

    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"❌ Example failed: {e}")
            print()

    print("🎉 All examples completed!")


if __name__ == '__main__':
    main()