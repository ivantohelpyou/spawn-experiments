#!/usr/bin/env python3
"""
JSON Schema Validator CLI tool.
A command-line tool for validating JSON data against JSON Schema.
"""

import json
import sys
import argparse
import os
import glob
import csv
from io import StringIO
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple


@dataclass
class ValidationResult:
    """Result of JSON validation operation."""
    is_valid: bool
    errors: List[str]
    file_path: Optional[str] = None


def validate_json(data: Dict[Any, Any], schema: Dict[str, Any]) -> ValidationResult:
    """
    Validate JSON data against a JSON Schema.

    Args:
        data: The JSON data to validate
        schema: The JSON schema to validate against

    Returns:
        ValidationResult object with validation status and errors
    """
    errors = []

    # Basic type validation
    if 'type' in schema:
        expected_type = schema['type']
        if not _validate_type(data, expected_type):
            errors.append(f"Expected type '{expected_type}' but got '{type(data).__name__}'")

    # Required fields validation
    if 'required' in schema and isinstance(data, dict):
        required_fields = schema['required']
        for field in required_fields:
            if field not in data:
                errors.append(f"Required field '{field}' is missing")

    # Properties validation
    if 'properties' in schema and isinstance(data, dict):
        properties = schema['properties']
        for field_name, field_value in data.items():
            if field_name in properties:
                field_schema = properties[field_name]
                field_result = validate_json(field_value, field_schema)
                if not field_result.is_valid:
                    for error in field_result.errors:
                        errors.append(f"Field '{field_name}': {error}")

    # Constraint validation for numbers
    if isinstance(data, (int, float)):
        if 'minimum' in schema and data < schema['minimum']:
            errors.append(f"Value {data} is less than minimum {schema['minimum']}")
        if 'maximum' in schema and data > schema['maximum']:
            errors.append(f"Value {data} is greater than maximum {schema['maximum']}")

    # Constraint validation for strings
    if isinstance(data, str):
        if 'minLength' in schema and len(data) < schema['minLength']:
            errors.append(f"String length {len(data)} is less than minimum {schema['minLength']}")
        if 'maxLength' in schema and len(data) > schema['maxLength']:
            errors.append(f"String length {len(data)} is greater than maximum {schema['maxLength']}")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors)


def _validate_type(data: Any, expected_type: str) -> bool:
    """Validate that data matches the expected JSON Schema type."""
    type_mapping = {
        'string': str,
        'integer': int,
        'number': (int, float),
        'boolean': bool,
        'array': list,
        'object': dict,
        'null': type(None)
    }

    if expected_type not in type_mapping:
        return False

    expected_python_type = type_mapping[expected_type]
    return isinstance(data, expected_python_type)


def validate_file(data_file_path: str, schema_file_path: str) -> ValidationResult:
    """
    Validate a JSON file against a schema file.

    Args:
        data_file_path: Path to the JSON data file
        schema_file_path: Path to the JSON schema file

    Returns:
        ValidationResult object with validation status and errors
    """
    errors = []

    # Check if data file exists
    if not os.path.exists(data_file_path):
        return ValidationResult(
            is_valid=False,
            errors=[f"Data file not found: {data_file_path}"],
            file_path=data_file_path
        )

    # Check if schema file exists
    if not os.path.exists(schema_file_path):
        return ValidationResult(
            is_valid=False,
            errors=[f"Schema file not found: {schema_file_path}"],
            file_path=data_file_path
        )

    try:
        # Load and parse data file
        with open(data_file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return ValidationResult(
            is_valid=False,
            errors=[f"Invalid JSON in data file: {str(e)}"],
            file_path=data_file_path
        )
    except Exception as e:
        return ValidationResult(
            is_valid=False,
            errors=[f"Error reading data file: {str(e)}"],
            file_path=data_file_path
        )

    try:
        # Load and parse schema file
        with open(schema_file_path, 'r') as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        return ValidationResult(
            is_valid=False,
            errors=[f"Invalid JSON in schema file: {str(e)}"],
            file_path=data_file_path
        )
    except Exception as e:
        return ValidationResult(
            is_valid=False,
            errors=[f"Error reading schema file: {str(e)}"],
            file_path=data_file_path
        )

    # Perform validation
    result = validate_json(data, schema)
    result.file_path = data_file_path
    return result


def batch_validate(file_paths: List[str], schema_file_path: str) -> List[ValidationResult]:
    """
    Validate multiple JSON files against a schema file.

    Args:
        file_paths: List of paths to JSON data files
        schema_file_path: Path to the JSON schema file

    Returns:
        List of ValidationResult objects
    """
    results = []
    for file_path in file_paths:
        result = validate_file(file_path, schema_file_path)
        results.append(result)
    return results


def batch_validate_pattern(pattern: str, schema_file_path: str) -> List[ValidationResult]:
    """
    Validate multiple JSON files matching a pattern against a schema file.

    Args:
        pattern: Glob pattern for JSON files (e.g., "*.json")
        schema_file_path: Path to the JSON schema file

    Returns:
        List of ValidationResult objects
    """
    file_paths = glob.glob(pattern)
    # Filter out the schema file itself if it matches the pattern
    file_paths = [fp for fp in file_paths if fp != schema_file_path]
    return batch_validate(file_paths, schema_file_path)


def format_text(results: List[ValidationResult]) -> str:
    """
    Format validation results as human-readable text.

    Args:
        results: List of validation results

    Returns:
        Formatted text string
    """
    lines = []
    for result in results:
        filename = os.path.basename(result.file_path) if result.file_path else "stdin"
        status = "VALID" if result.is_valid else "INVALID"
        lines.append(f"{filename}: {status}")

        if not result.is_valid and result.errors:
            for error in result.errors:
                lines.append(f"  - {error}")

    return "\n".join(lines)


def format_json(results: List[ValidationResult]) -> str:
    """
    Format validation results as JSON.

    Args:
        results: List of validation results

    Returns:
        JSON string
    """
    serializable_results = []
    for result in results:
        data = asdict(result)
        serializable_results.append(data)

    return json.dumps(serializable_results, indent=2)


def format_csv(results: List[ValidationResult]) -> str:
    """
    Format validation results as CSV.

    Args:
        results: List of validation results

    Returns:
        CSV string
    """
    output = StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['file_path', 'is_valid', 'error_count', 'errors'])

    # Write data rows
    for result in results:
        filename = os.path.basename(result.file_path) if result.file_path else "stdin"
        errors_str = "; ".join(result.errors) if result.errors else ""
        writer.writerow([
            filename,
            result.is_valid,
            len(result.errors),
            errors_str
        ])

    return output.getvalue()


def format_quiet(results: List[ValidationResult]) -> Tuple[str, int]:
    """
    Format validation results for quiet mode (no output, just exit codes).

    Args:
        results: List of validation results

    Returns:
        Tuple of (empty string, exit code)
    """
    # Exit code 0 if all results are valid, 1 if any are invalid
    exit_code = 0 if all(result.is_valid for result in results) else 1
    return "", exit_code


def verify_schema(schema_file_path: str) -> ValidationResult:
    """
    Verify that a JSON Schema file is valid.

    Args:
        schema_file_path: Path to the JSON schema file

    Returns:
        ValidationResult object with verification status and errors
    """
    if not os.path.exists(schema_file_path):
        return ValidationResult(
            is_valid=False,
            errors=[f"Schema file not found: {schema_file_path}"],
            file_path=schema_file_path
        )

    try:
        with open(schema_file_path, 'r') as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        return ValidationResult(
            is_valid=False,
            errors=[f"Invalid JSON in schema file: {str(e)}"],
            file_path=schema_file_path
        )
    except Exception as e:
        return ValidationResult(
            is_valid=False,
            errors=[f"Error reading schema file: {str(e)}"],
            file_path=schema_file_path
        )

    # Basic schema validation - check for valid type definitions
    errors = []
    try:
        if isinstance(schema, dict):
            # Check for known schema properties and valid types
            if 'type' in schema:
                valid_types = {'string', 'integer', 'number', 'boolean', 'object', 'array', 'null'}
                if schema['type'] not in valid_types:
                    errors.append(f"Invalid type '{schema['type']}' in schema")

            if 'properties' in schema:
                for prop_name, prop_def in schema['properties'].items():
                    if isinstance(prop_def, dict) and 'type' in prop_def:
                        if prop_def['type'] not in valid_types:
                            errors.append(f"Invalid type '{prop_def['type']}' for property '{prop_name}'")
        else:
            errors.append("Schema must be a JSON object")

    except Exception as e:
        errors.append(f"Error validating schema structure: {str(e)}")

    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        file_path=schema_file_path
    )


def main() -> int:
    """
    Main CLI entry point.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        args = parse_args()

        if args.command == 'validate':
            # Single file validation
            result = validate_file(args.input_file, args.schema)
            results = [result]

        elif args.command == 'batch':
            # Batch validation
            results = batch_validate_pattern(args.pattern, args.schema)

        elif args.command == 'check':
            # Schema verification
            result = verify_schema(args.schema_file)
            results = [result]

        else:
            print("Unknown command", file=sys.stderr)
            return 1

        # Format output based on chosen format and quiet mode
        if getattr(args, 'quiet', False):
            output, exit_code = format_quiet(results)
            if output:
                print(output, end='')
            return exit_code
        else:
            output_format = getattr(args, 'output', 'text')
            if output_format == 'json':
                output = format_json(results)
            elif output_format == 'csv':
                output = format_csv(results)
            else:  # text format
                output = format_text(results)

            print(output)
            # Return appropriate exit code
            return 0 if all(result.is_valid for result in results) else 1

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


def parse_args(args_list: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments for the JSON Schema Validator.

    Args:
        args_list: Optional list of arguments (for testing). If None, uses sys.argv.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog='jsv',
        description='JSON Schema Validator CLI tool'
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a JSON file against a schema')
    validate_parser.add_argument('input_file', help='JSON file to validate')
    validate_parser.add_argument('--schema', required=True, help='JSON schema file')
    validate_parser.add_argument('--quiet', action='store_true', help='Only return exit codes')
    validate_parser.add_argument('--output', choices=['text', 'json'], default='text',
                                help='Output format (default: text)')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Validate multiple JSON files')
    batch_parser.add_argument('pattern', help='File pattern (e.g., *.json)')
    batch_parser.add_argument('--schema', required=True, help='JSON schema file')
    batch_parser.add_argument('--output', choices=['text', 'json', 'csv'], default='text',
                             help='Output format (default: text)')
    batch_parser.add_argument('--quiet', action='store_true', help='Only return exit codes')

    # Check command
    check_parser = subparsers.add_parser('check', help='Verify a JSON schema file')
    check_parser.add_argument('schema_file', help='JSON schema file to verify')
    check_parser.add_argument('--quiet', action='store_true', help='Only return exit codes')

    if args_list is None:
        return parser.parse_args()
    else:
        return parser.parse_args(args_list)


if __name__ == '__main__':
    sys.exit(main())