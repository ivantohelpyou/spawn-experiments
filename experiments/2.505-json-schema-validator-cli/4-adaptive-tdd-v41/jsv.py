#!/usr/bin/env python3
"""
JSON Schema Validator CLI tool.

A command-line tool for validating JSON data against JSON Schema (Draft 7 subset).
"""

import argparse
import sys
import os
import json
import glob
from typing import List, Optional
from pathlib import Path

from validator import JSONSchemaValidator, ValidationResult
from formatters import get_formatter


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='jsv',
        description='JSON Schema Validator - Validate JSON data against JSON Schema',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a single file
  jsv validate data.json --schema=schema.json

  # Batch validation with CSV output
  jsv batch *.json --schema=schema.json --output=csv

  # Validate from stdin
  cat data.json | jsv validate --schema=schema.json

  # Check schema validity
  jsv check schema.json

  # Quiet mode (only exit codes)
  jsv validate data.json --schema=schema.json --quiet
        """)

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Validate command
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate a single JSON file or stdin against a schema'
    )
    validate_parser.add_argument(
        'input_file',
        nargs='?',
        help='JSON file to validate (omit to read from stdin)'
    )
    validate_parser.add_argument(
        '--schema',
        required=True,
        help='JSON Schema file to validate against'
    )
    validate_parser.add_argument(
        '--output',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )
    validate_parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    validate_parser.add_argument(
        '--quiet',
        action='store_true',
        help='Quiet mode - only return exit codes'
    )

    # Batch command
    batch_parser = subparsers.add_parser(
        'batch',
        help='Validate multiple JSON files against a schema'
    )
    batch_parser.add_argument(
        'input_files',
        nargs='+',
        help='JSON files to validate (supports glob patterns)'
    )
    batch_parser.add_argument(
        '--schema',
        required=True,
        help='JSON Schema file to validate against'
    )
    batch_parser.add_argument(
        '--output',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )
    batch_parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    batch_parser.add_argument(
        '--quiet',
        action='store_true',
        help='Quiet mode - only return exit codes'
    )

    # Check command
    check_parser = subparsers.add_parser(
        'check',
        help='Check if a JSON Schema is valid'
    )
    check_parser.add_argument(
        'schema_file',
        help='JSON Schema file to check'
    )
    check_parser.add_argument(
        '--output',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    check_parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    check_parser.add_argument(
        '--quiet',
        action='store_true',
        help='Quiet mode - only return exit codes'
    )

    return parser


def expand_file_patterns(patterns: List[str]) -> List[str]:
    """
    Expand glob patterns to actual file paths.

    Args:
        patterns: List of file patterns (may include globs)

    Returns:
        List of expanded file paths
    """
    expanded = []
    for pattern in patterns:
        if '*' in pattern or '?' in pattern or '[' in pattern:
            # It's a glob pattern
            matches = glob.glob(pattern)
            if matches:
                expanded.extend(sorted(matches))
            else:
                # No matches for pattern
                print(f"Warning: No files match pattern '{pattern}'", file=sys.stderr)
        else:
            # It's a literal file path
            expanded.append(pattern)
    return expanded


def validate_command(args) -> int:
    """Handle the validate command."""
    validator = JSONSchemaValidator()

    # Load schema
    try:
        schema = validator.load_schema_file(args.schema)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading schema: {e}", file=sys.stderr)
        return 1

    # Validate schema first
    schema_result = validator.validate_schema(schema)
    if not schema_result.is_valid:
        print(f"Invalid schema: {schema_result.errors[0]}", file=sys.stderr)
        return 1

    # Determine output format
    output_format = 'quiet' if args.quiet else args.output
    formatter = get_formatter(output_format, not args.no_color)

    # Validate input
    if args.input_file:
        # Validate file
        result = validator.validate_file(args.input_file, schema)
    else:
        # Validate stdin
        try:
            data = json.load(sys.stdin)
            result = validator.validate(data, schema)
        except json.JSONDecodeError as e:
            result = ValidationResult(False, [f"JSON parse error from stdin: {str(e)}"])

    # Output result
    output = formatter.format_single_result(result)
    if output:
        print(output)

    return 0 if result.is_valid else 1


def batch_command(args) -> int:
    """Handle the batch command."""
    validator = JSONSchemaValidator()

    # Load schema
    try:
        schema = validator.load_schema_file(args.schema)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading schema: {e}", file=sys.stderr)
        return 1

    # Validate schema first
    schema_result = validator.validate_schema(schema)
    if not schema_result.is_valid:
        print(f"Invalid schema: {schema_result.errors[0]}", file=sys.stderr)
        return 1

    # Expand file patterns
    file_paths = expand_file_patterns(args.input_files)
    if not file_paths:
        print("Error: No files to validate", file=sys.stderr)
        return 1

    # Determine output format
    output_format = 'quiet' if args.quiet else args.output
    formatter = get_formatter(output_format, not args.no_color)

    # Show progress for large batches (only in text mode)
    show_progress = len(file_paths) > 10 and args.output == 'text' and not args.quiet

    # Validate files
    results = []
    for i, file_path in enumerate(file_paths):
        if show_progress:
            print(f"Processing {i+1}/{len(file_paths)}: {file_path}", file=sys.stderr)

        result = validator.validate_file(file_path, schema)
        results.append(result)

    # Output results
    output = formatter.format_batch_results(results)
    if output:
        print(output)

    # Return exit code based on validation results
    return 0 if all(r.is_valid for r in results) else 1


def check_command(args) -> int:
    """Handle the check command."""
    validator = JSONSchemaValidator()

    # Load and validate schema
    try:
        schema = validator.load_schema_file(args.schema_file)
        result = validator.validate_schema(schema)
    except FileNotFoundError:
        result = ValidationResult(False, [f"Schema file not found: {args.schema_file}"])
    except json.JSONDecodeError as e:
        result = ValidationResult(False, [f"JSON parse error in schema: {str(e)}"])

    # Set file path for consistent output formatting
    result.file_path = args.schema_file

    # Determine output format
    output_format = 'quiet' if args.quiet else args.output
    formatter = get_formatter(output_format, not args.no_color)

    # Output result
    output = formatter.format_single_result(result)
    if output:
        print(output)

    return 0 if result.is_valid else 1


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == 'validate':
            return validate_command(args)
        elif args.command == 'batch':
            return batch_command(args)
        elif args.command == 'check':
            return check_command(args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 1

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())