#!/usr/bin/env python3
"""
Test script for the Path Validator
"""

import os
import tempfile
from path_validator import PathValidator, validate_paths


def test_basic_validation():
    """Test basic path validation functionality."""
    print("Testing basic path validation...")
    validator = PathValidator()

    # Test valid paths
    valid_paths = [
        "/home/user/file.txt",
        "relative/path.txt",
        ".",
        "..",
        "/tmp"
    ]

    for path in valid_paths:
        result = validator.validate_path(path)
        assert result['is_valid'], f"Path should be valid: {path}"
        print(f"✓ Valid path: {path}")

    # Test invalid paths
    invalid_paths = [
        "",  # Empty string
        None,  # None type (will be caught by isinstance check)
    ]

    for path in invalid_paths:
        result = validator.validate_path(path)
        assert not result['is_valid'], f"Path should be invalid: {path}"
        print(f"✓ Invalid path detected: {path}")


def test_existence_checks():
    """Test path existence validation."""
    print("\nTesting path existence checks...")
    validator = PathValidator()

    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = temp_file.name
        temp_file.write(b"test content")

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Test existing file
        result = validator.validate_path(temp_path)
        assert result['exists'], "Temporary file should exist"
        assert result['is_file'], "Should be detected as file"
        assert not result['is_directory'], "Should not be detected as directory"
        print(f"✓ File existence detected: {temp_path}")

        # Test existing directory
        result = validator.validate_path(temp_dir)
        assert result['exists'], "Temporary directory should exist"
        assert result['is_directory'], "Should be detected as directory"
        assert not result['is_file'], "Should not be detected as file"
        print(f"✓ Directory existence detected: {temp_dir}")

        # Test non-existing path
        result = validator.validate_path("/nonexistent/path/file.txt")
        assert not result['exists'], "Non-existent path should not exist"
        assert not result['is_file'], "Non-existent path should not be file"
        assert not result['is_directory'], "Non-existent path should not be directory"
        print("✓ Non-existence correctly detected")

    finally:
        # Clean up
        os.unlink(temp_path)
        os.rmdir(temp_dir)


def test_path_types():
    """Test absolute vs relative path detection."""
    print("\nTesting path type detection...")
    validator = PathValidator()

    # Test absolute paths
    absolute_paths = ["/home/user", "/tmp", "/usr/bin/python"]
    for path in absolute_paths:
        result = validator.validate_path(path)
        assert result['is_absolute'], f"Should be absolute: {path}"
        assert not result['is_relative'], f"Should not be relative: {path}"
        print(f"✓ Absolute path detected: {path}")

    # Test relative paths
    relative_paths = ["file.txt", "../parent", "./current", "sub/dir"]
    for path in relative_paths:
        result = validator.validate_path(path)
        assert result['is_relative'], f"Should be relative: {path}"
        assert not result['is_absolute'], f"Should not be absolute: {path}"
        print(f"✓ Relative path detected: {path}")


def test_edge_cases():
    """Test common edge cases."""
    print("\nTesting edge cases...")
    validator = PathValidator()

    # Test paths with spaces
    result = validator.validate_path("file with spaces.txt")
    assert result['is_valid'], "Paths with spaces should be valid"
    print("✓ Paths with spaces handled")

    # Test very long paths
    long_path = "a" * 300  # 300 characters, exceeds Windows MAX_PATH of 260
    result = validator.validate_path(long_path)
    assert result['is_valid'], "Long paths should be valid"
    assert any("exceeds" in warning.lower() for warning in result['warnings']), "Should warn about long paths"
    print("✓ Long paths handled with warning")

    # Test paths ending with space
    result = validator.validate_path("file.txt ")
    assert result['is_valid'], "Paths ending with space should be valid"
    assert any("ends with space" in warning for warning in result['warnings']), "Should warn about trailing space"
    print("✓ Trailing space warning")

    # Test hidden files
    result = validator.validate_path(".hidden/file.txt")
    assert result['is_valid'], "Hidden file paths should be valid"
    assert any("hidden" in warning.lower() for warning in result['warnings']), "Should warn about hidden files"
    print("✓ Hidden file warning")


def test_multiple_paths():
    """Test batch validation of multiple paths."""
    print("\nTesting multiple path validation...")

    test_paths = [
        "/tmp",
        "relative.txt",
        "",
        "/nonexistent"
    ]

    results = validate_paths(test_paths)
    assert len(results) == len(test_paths), "Should return results for all paths"

    for path in test_paths:
        assert path in results, f"Should have result for path: {path}"

    print("✓ Multiple path validation works")


def test_windows_specific():
    """Test Windows-specific validations (when applicable)."""
    print("\nTesting Windows-specific validations...")
    validator = PathValidator()

    # Test reserved names (these should be invalid on Windows)
    reserved_paths = ["CON", "PRN", "AUX", "COM1", "LPT1"]

    for path in reserved_paths:
        result = validator.validate_path(path)
        if validator.system == 'Windows':
            assert not result['is_valid'], f"Reserved name should be invalid on Windows: {path}"
            print(f"✓ Windows reserved name rejected: {path}")
        else:
            print(f"✓ Reserved name test skipped (not Windows): {path}")

    # Test invalid characters
    invalid_char_paths = ['file<name.txt', 'file>name.txt', 'file|name.txt']

    for path in invalid_char_paths:
        result = validator.validate_path(path)
        if validator.system == 'Windows':
            assert not result['is_valid'], f"Invalid chars should be rejected on Windows: {path}"
            print(f"✓ Windows invalid character rejected: {path}")
        else:
            print(f"✓ Invalid character test skipped (not Windows): {path}")


def run_all_tests():
    """Run all test functions."""
    print("File Path Validator - Comprehensive Tests")
    print("=" * 50)

    test_basic_validation()
    test_existence_checks()
    test_path_types()
    test_edge_cases()
    test_multiple_paths()
    test_windows_specific()

    print("\n" + "=" * 50)
    print("All tests passed! ✓")


if __name__ == "__main__":
    run_all_tests()