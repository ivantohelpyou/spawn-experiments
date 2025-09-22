#!/usr/bin/env python3
"""
Example usage of the File Path Validator
"""

from path_validator import PathValidator, validate_path, is_valid_path, validate_paths

def main():
    print("File Path Validator - Example Usage")
    print("=" * 50)

    # Example 1: Quick validation
    print("\n1. Quick Boolean Validation:")
    test_paths = [
        "/home/user/document.txt",
        "C:\\Users\\file.doc",
        "/invalid<path",
        "",
        "valid_filename.py"
    ]

    for path in test_paths:
        valid = is_valid_path(path)
        print(f"  {'✓' if valid else '✗'} {path}")

    # Example 2: Detailed validation with error messages
    print("\n2. Detailed Validation:")
    problematic_paths = [
        "CON.txt",  # Windows reserved
        "/path/with<invalid>chars",  # Invalid characters
        "file" + "x" * 300 + ".txt",  # Too long component
        "/path/ending_with_space ",  # Invalid Windows format
    ]

    for path in problematic_paths:
        result = validate_path(path)
        if result.is_valid:
            print(f"  ✓ {path}")
        else:
            print(f"  ✗ {path}")
            for error in result.errors:
                print(f"    - {error}")

    # Example 3: Batch validation
    print("\n3. Batch Validation:")
    batch_paths = [
        "/project/src/main.py",
        "/project/docs/README.md",
        "/project/test<invalid>.py",
        "/project/data/file.json"
    ]

    results = validate_paths(batch_paths)
    valid_count = sum(1 for r in results if r.is_valid)
    print(f"  Validated {len(results)} paths: {valid_count} valid, {len(results) - valid_count} invalid")

    for result in results:
        status = "✓" if result.is_valid else "✗"
        print(f"  {status} {result.path}")

    # Example 4: Advanced usage with validator instance
    print("\n4. Advanced Usage:")
    validator = PathValidator(strict_mode=True)

    # Check if paths exist
    current_file = __file__
    print(f"  Current file exists: {validator.exists(current_file)}")

    # Normalize paths
    relative_path = "../test/../example_usage.py"
    normalized = validator.normalize(relative_path)
    print(f"  Normalized path: {normalized}")

    # Custom validation
    result = validator.validate("/custom/path/file.txt")
    print(f"  Custom validation: {'Valid' if result.is_valid else 'Invalid'}")

    print("\n" + "=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()