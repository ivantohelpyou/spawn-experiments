#!/usr/bin/env python3
"""
Example usage of the FilePathValidator class demonstrating various validation scenarios.
"""

from pathlib import Path
from file_path_validator import FilePathValidator


def demonstrate_basic_validation():
    """Demonstrate basic path validation functionality."""
    print("=== Basic Path Validation ===")
    validator = FilePathValidator()

    test_paths = [
        "documents/file.txt",           # Valid relative path
        "/home/user/documents/file.txt", # Valid absolute path
        "",                             # Invalid empty path
        "file\x00name.txt",            # Invalid null character
        "a" * 5000,                    # Invalid too long path
        Path("config/settings.ini"),    # Valid pathlib Path object
    ]

    for path in test_paths:
        result = validator.is_valid_path(path)
        print(f"Path: {repr(path)}")
        print(f"  Valid: {result.is_valid}")
        print(f"  Type: {result.path_type}")
        print(f"  Input Type: {result.original_input_type}")
        if not result.is_valid:
            print(f"  Error: {result.error_message}")
        print()


def demonstrate_security_validation():
    """Demonstrate security validation for path traversal protection."""
    print("=== Security Validation ===")
    validator = FilePathValidator()
    base_dir = "/home/user/sandbox"

    test_paths = [
        "documents/file.txt",           # Safe relative path
        "subdirectory/nested/file.log", # Safe nested path
        "../../../etc/passwd",          # Dangerous path traversal
        "/etc/passwd",                  # Dangerous absolute path
        "..\\..\\windows\\system32",    # Windows path traversal
    ]

    for path in test_paths:
        result = validator.is_secure_path(path, base_dir)
        print(f"Path: {repr(path)}")
        print(f"  Secure: {result.is_secure}")
        if not result.is_secure:
            print(f"  Reason: {result.error_message}")
        print()


def demonstrate_existence_checking():
    """Demonstrate path existence checking."""
    print("=== Path Existence Checking ===")
    validator = FilePathValidator()

    test_paths = [
        "/tmp",                # Existing directory
        "/etc/passwd",         # Existing file (on most Unix systems)
        "/nonexistent/path",   # Non-existing path
        ".",                   # Current directory
    ]

    for path in test_paths:
        result = validator.path_exists(path)
        print(f"Path: {repr(path)}")
        print(f"  Exists: {result.exists}")
        if result.exists:
            print(f"  Type: {result.path_type}")
        print()


def demonstrate_path_normalization():
    """Demonstrate path normalization functionality."""
    print("=== Path Normalization ===")
    validator = FilePathValidator()

    test_paths = [
        "./documents/../config.ini",           # Relative with '..'
        "documents//subdirectory///file.txt",  # Multiple separators
        "/home/user/../user/file.txt",         # Absolute with '..'
        "documents\\subdirectory\\file.txt",   # Windows separators on Unix
    ]

    for path in test_paths:
        result = validator.normalize_path(path)
        print(f"Original: {repr(path)}")
        print(f"Normalized: {repr(result.normalized_path)}")
        print()


def demonstrate_validator_configurations():
    """Demonstrate different validator configurations."""
    print("=== Validator Configurations ===")

    # Strict validator (no relative paths, no path traversal)
    print("Strict Validator (no relative paths):")
    strict_validator = FilePathValidator(
        allow_relative=False,
        allow_path_traversal=False,
        max_length=255
    )

    relative_path = "../documents/file.txt"
    result = strict_validator.is_valid_path(relative_path)
    print(f"  Path: {repr(relative_path)}")
    print(f"  Valid: {result.is_valid}")
    if not result.is_valid:
        print(f"  Error: {result.error_message}")
    print()

    # Permissive validator
    print("Permissive Validator:")
    permissive_validator = FilePathValidator(
        allow_relative=True,
        allow_path_traversal=True,
        max_length=1000
    )

    result = permissive_validator.is_valid_path(relative_path)
    print(f"  Path: {repr(relative_path)}")
    print(f"  Valid: {result.is_valid}")
    print()


def demonstrate_cross_platform_handling():
    """Demonstrate cross-platform path handling."""
    print("=== Cross-Platform Path Handling ===")
    validator = FilePathValidator()

    cross_platform_paths = [
        "documents/subdirectory/file.txt",    # Unix style
        "documents\\subdirectory\\file.txt",  # Windows style
        "documents/mixed\\path/file.txt",     # Mixed separators
    ]

    for path in cross_platform_paths:
        result = validator.is_valid_path(path)
        normalized = validator.normalize_path(path)
        print(f"Original: {repr(path)}")
        print(f"  Valid: {result.is_valid}")
        print(f"  Normalized: {repr(normalized.normalized_path)}")
        print()


if __name__ == "__main__":
    print("File Path Validator - Example Usage\n")
    print("This example demonstrates the usage of os.path and pathlib libraries")
    print("for comprehensive file path validation.\n")

    demonstrate_basic_validation()
    demonstrate_security_validation()
    demonstrate_existence_checking()
    demonstrate_path_normalization()
    demonstrate_validator_configurations()
    demonstrate_cross_platform_handling()

    print("=== Summary ===")
    print("The FilePathValidator provides:")
    print("- Basic path validation (emptiness, length, characters)")
    print("- Security validation (path traversal protection)")
    print("- Existence checking with type determination")
    print("- Path normalization using both os.path and pathlib")
    print("- Cross-platform compatibility")
    print("- Configurable validation rules")
    print("- Support for both string and pathlib.Path inputs")