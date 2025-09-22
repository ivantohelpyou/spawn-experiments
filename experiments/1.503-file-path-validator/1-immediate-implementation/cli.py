#!/usr/bin/env python3
"""
Command-line interface for the File Path Validator
"""

import argparse
import sys
from path_validator import PathValidator


def main():
    """Command-line interface for path validation."""
    parser = argparse.ArgumentParser(
        description="Validate file paths using os.path and pathlib libraries"
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="One or more paths to validate"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed validation information"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only show validation results (valid/invalid)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )

    args = parser.parse_args()

    validator = PathValidator()

    if args.json:
        import json
        results = {}
        for path in args.paths:
            results[path] = validator.validate_path(path)
        print(json.dumps(results, indent=2))
        return

    exit_code = 0

    for i, path in enumerate(args.paths):
        if i > 0 and not args.quiet:
            print()  # Blank line between multiple paths

        result = validator.validate_path(path)

        if not result['is_valid']:
            exit_code = 1

        if args.quiet:
            # Just show valid/invalid
            status = "VALID" if result['is_valid'] else "INVALID"
            print(f"{path}: {status}")
        elif args.verbose:
            # Show detailed information
            print(f"Path: {path}")
            print(f"Valid: {result['is_valid']}")
            print(f"Exists: {result['exists']}")
            print(f"Type: {'File' if result['is_file'] else 'Directory' if result['is_directory'] else 'N/A'}")
            print(f"Path Type: {'Absolute' if result['is_absolute'] else 'Relative'}")
            print(f"Parent Exists: {result['parent_exists']}")

            if result['normalized_path']:
                print(f"Normalized: {result['normalized_path']}")

            if result['errors']:
                print(f"Errors: {', '.join(result['errors'])}")

            if result['warnings']:
                print(f"Warnings: {', '.join(result['warnings'])}")
        else:
            # Default output
            status_symbol = "✓" if result['is_valid'] else "✗"
            existence = " (exists)" if result['exists'] else ""
            path_type = f" [{('file' if result['is_file'] else 'dir' if result['is_directory'] else 'n/a')}]" if result['exists'] else ""

            print(f"{status_symbol} {path}{existence}{path_type}")

            if result['errors']:
                print(f"  Error: {result['errors'][0]}")

            if result['warnings']:
                print(f"  Warning: {result['warnings'][0]}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()