#!/usr/bin/env python3
"""
JSON Schema Validator CLI tool.
A command-line tool for validating JSON data against JSON Schema.
"""

import json
import sys
import argparse
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


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
    # Placeholder for CLI functionality
    print("JSON Schema Validator CLI")
    sys.exit(0)