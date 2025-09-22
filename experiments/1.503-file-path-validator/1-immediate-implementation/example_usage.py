#!/usr/bin/env python3
"""
Example usage of the File Path Validator
"""

from path_validator import PathValidator, validate_paths


def main():
    """Demonstrate various uses of the path validator."""

    print("File Path Validator - Usage Examples")
    print("=" * 50)

    # Create a validator instance
    validator = PathValidator()

    # Example 1: Validate a single path
    print("\n1. Single Path Validation:")
    test_path = "/home/user/documents/report.pdf"
    result = validator.validate_path(test_path)

    print(f"Path: {test_path}")
    print(f"Valid: {result['is_valid']}")
    print(f"Exists: {result['exists']}")
    print(f"Type: {'Absolute' if result['is_absolute'] else 'Relative'}")

    if result['warnings']:
        print(f"Warnings: {', '.join(result['warnings'])}")
    if result['errors']:
        print(f"Errors: {', '.join(result['errors'])}")

    # Example 2: Validate multiple paths at once
    print("\n2. Multiple Path Validation:")
    paths_to_check = [
        "/tmp",
        "relative/file.txt",
        "/nonexistent/path",
        "",
        "file with spaces.txt",
        ".hidden_file"
    ]

    results = validate_paths(paths_to_check)

    for path, result in results.items():
        status = "✓" if result['is_valid'] else "✗"
        existence = "exists" if result['exists'] else "not found"
        print(f"{status} '{path}' - {existence}")

    # Example 3: Check for specific conditions
    print("\n3. Conditional Checks:")

    # Check if a path exists and is a directory
    dir_path = "/tmp"
    result = validator.validate_path(dir_path)
    if result['is_valid'] and result['exists'] and result['is_directory']:
        print(f"✓ {dir_path} is a valid existing directory")

    # Check if a path is safe for creating a new file
    new_file_path = "/tmp/new_file.txt"
    result = validator.validate_path(new_file_path)
    if result['is_valid'] and not result['exists'] and result['parent_exists']:
        print(f"✓ {new_file_path} is safe for creating a new file")
    elif result['is_valid'] and not result['parent_exists']:
        print(f"! {new_file_path} parent directory doesn't exist")

    # Example 4: Error handling
    print("\n4. Error Handling:")

    invalid_paths = [None, "", "\\invalid\\on\\unix"]
    for path in invalid_paths:
        result = validator.validate_path(path)
        if not result['is_valid']:
            print(f"✗ Invalid path: {repr(path)} - {result['errors'][0] if result['errors'] else 'Unknown error'}")

    # Example 5: Working with the results programmatically
    print("\n5. Programmatic Usage:")

    def safe_file_operation(file_path):
        """Example function that checks path safety before operations."""
        result = validator.validate_path(file_path)

        if not result['is_valid']:
            return False, f"Invalid path: {result['errors'][0] if result['errors'] else 'Unknown error'}"

        if not result['parent_exists']:
            return False, "Parent directory does not exist"

        if result['exists'] and result['is_directory']:
            return False, "Path points to an existing directory"

        if result['warnings']:
            print(f"Warning for '{file_path}': {result['warnings'][0]}")

        return True, "Path is safe for file operations"

    test_files = ["/tmp/test.txt", "/nonexistent/dir/file.txt", "/tmp"]

    for file_path in test_files:
        safe, message = safe_file_operation(file_path)
        status = "✓" if safe else "✗"
        print(f"{status} {file_path}: {message}")


if __name__ == "__main__":
    main()