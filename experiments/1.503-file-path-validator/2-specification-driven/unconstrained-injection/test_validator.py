#!/usr/bin/env python3
"""
Quick tests for the path validator to ensure it works.
"""

import pathlib
from path_validator import PathValidator, validate_path, is_valid_path


def test_basic_validation():
    """Test basic path validation."""
    validator = PathValidator()

    # Valid paths
    assert validator.is_valid("/valid/path/file.txt")
    assert validator.is_valid("relative/path.py")
    assert validator.is_valid("C:\\Windows\\valid.txt")

    # Invalid paths
    assert not validator.is_valid("")
    assert not validator.is_valid("/path/with<invalid")
    assert not validator.is_valid("CON.txt")  # Reserved on Windows


def test_convenience_functions():
    """Test convenience functions."""
    assert is_valid_path("/valid/path.txt")
    assert not is_valid_path("")

    result = validate_path("/test/path.py")
    assert result.is_valid
    assert result.path == "/test/path.py"


def test_batch_validation():
    """Test batch validation."""
    validator = PathValidator()
    paths = ["/valid1.txt", "/valid2.py", "/invalid<.txt"]

    results = validator.validate_batch(paths)
    assert len(results) == 3
    assert results[0].is_valid
    assert results[1].is_valid
    assert not results[2].is_valid


def test_pathlib_support():
    """Test pathlib.Path support."""
    validator = PathValidator()
    path_obj = pathlib.Path("/test/pathlib.txt")

    assert validator.is_valid(path_obj)


def test_normalization():
    """Test path normalization."""
    validator = PathValidator()
    normalized = validator.normalize("../test/../file.txt")
    assert isinstance(normalized, str)
    assert "file.txt" in normalized


if __name__ == "__main__":
    # Run basic tests
    print("Running basic validator tests...")

    try:
        test_basic_validation()
        print("✓ Basic validation tests passed")

        test_convenience_functions()
        print("✓ Convenience function tests passed")

        test_batch_validation()
        print("✓ Batch validation tests passed")

        test_pathlib_support()
        print("✓ Pathlib support tests passed")

        test_normalization()
        print("✓ Normalization tests passed")

        print("\n🎉 All tests passed! Path validator is working.")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        exit(1)