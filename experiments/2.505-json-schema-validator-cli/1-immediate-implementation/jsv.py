#!/usr/bin/env python3
"""
JSON Schema Validator CLI Tool
A command-line tool for validating JSON data against JSON Schema (Draft 7 subset).
"""

import argparse
import json
import sys
import os
import glob
import csv
import io
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import re
import urllib.parse

# Colors for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def colorize(text: str, color: str) -> str:
    """Add color to text if stdout is a TTY."""
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.RESET}"
    return text

class ValidationError:
    """Represents a validation error."""
    def __init__(self, message: str, path: str = "", line: Optional[int] = None):
        self.message = message
        self.path = path
        self.line = line

class JSONSchemaValidator:
    """A simple JSON Schema validator supporting Draft 7 subset."""

    def __init__(self):
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        self.uri_pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')

    def validate(self, data: Any, schema: Dict[str, Any], path: str = "") -> List[ValidationError]:
        """Validate data against schema and return list of errors."""
        errors = []

        # Type validation
        if "type" in schema:
            type_errors = self._validate_type(data, schema["type"], path)
            errors.extend(type_errors)
            if type_errors:  # Don't continue if type is wrong
                return errors

        # Format validation
        if "format" in schema and isinstance(data, str):
            format_errors = self._validate_format(data, schema["format"], path)
            errors.extend(format_errors)

        # String validations
        if isinstance(data, str):
            if "minLength" in schema:
                if len(data) < schema["minLength"]:
                    errors.append(ValidationError(f"String too short (min: {schema['minLength']})", path))
            if "maxLength" in schema:
                if len(data) > schema["maxLength"]:
                    errors.append(ValidationError(f"String too long (max: {schema['maxLength']})", path))

        # Number validations
        if isinstance(data, (int, float)):
            if "minimum" in schema:
                if data < schema["minimum"]:
                    errors.append(ValidationError(f"Value too small (min: {schema['minimum']})", path))
            if "maximum" in schema:
                if data > schema["maximum"]:
                    errors.append(ValidationError(f"Value too large (max: {schema['maximum']})", path))

        # Object validations
        if isinstance(data, dict):
            # Required properties
            if "required" in schema:
                for required_prop in schema["required"]:
                    if required_prop not in data:
                        errors.append(ValidationError(f"Required property '{required_prop}' missing", path))

            # Property validations
            if "properties" in schema:
                for prop, prop_schema in schema["properties"].items():
                    if prop in data:
                        prop_path = f"{path}.{prop}" if path else prop
                        prop_errors = self.validate(data[prop], prop_schema, prop_path)
                        errors.extend(prop_errors)

        # Array validations
        if isinstance(data, list):
            if "items" in schema:
                for i, item in enumerate(data):
                    item_path = f"{path}[{i}]" if path else f"[{i}]"
                    item_errors = self.validate(item, schema["items"], item_path)
                    errors.extend(item_errors)

        return errors

    def _validate_type(self, data: Any, expected_type: Union[str, List[str]], path: str) -> List[ValidationError]:
        """Validate data type."""
        errors = []

        if isinstance(expected_type, list):
            valid = any(self._check_type(data, t) for t in expected_type)
            if not valid:
                errors.append(ValidationError(f"Invalid type. Expected one of: {expected_type}", path))
        else:
            if not self._check_type(data, expected_type):
                errors.append(ValidationError(f"Invalid type. Expected: {expected_type}", path))

        return errors

    def _check_type(self, data: Any, expected_type: str) -> bool:
        """Check if data matches expected type."""
        if expected_type == "string":
            return isinstance(data, str)
        elif expected_type == "number":
            return isinstance(data, (int, float))
        elif expected_type == "integer":
            return isinstance(data, int)
        elif expected_type == "boolean":
            return isinstance(data, bool)
        elif expected_type == "object":
            return isinstance(data, dict)
        elif expected_type == "array":
            return isinstance(data, list)
        elif expected_type == "null":
            return data is None
        return False

    def _validate_format(self, data: str, format_type: str, path: str) -> List[ValidationError]:
        """Validate string format."""
        errors = []

        if format_type == "email":
            if not self.email_pattern.match(data):
                errors.append(ValidationError(f"Invalid email format", path))
        elif format_type == "date":
            if not self.date_pattern.match(data):
                errors.append(ValidationError(f"Invalid date format (expected YYYY-MM-DD)", path))
        elif format_type == "uri":
            if not self.uri_pattern.match(data):
                errors.append(ValidationError(f"Invalid URI format", path))

        return errors

class ValidationResult:
    """Represents the result of validating a file."""
    def __init__(self, filename: str, is_valid: bool, errors: List[ValidationError],
                 elapsed_time: float = 0.0):
        self.filename = filename
        self.is_valid = is_valid
        self.errors = errors
        self.elapsed_time = elapsed_time

class OutputFormatter:
    """Handles different output formats."""

    @staticmethod
    def format_text(results: List[ValidationResult], verbose: bool = True) -> str:
        """Format results as human-readable text."""
        output = []

        for result in results:
            if result.is_valid:
                status = colorize("✓ VALID", Colors.GREEN)
                output.append(f"{status} {result.filename}")
            else:
                status = colorize("✗ INVALID", Colors.RED)
                output.append(f"{status} {result.filename}")

                if verbose:
                    for error in result.errors:
                        path_info = f" at {error.path}" if error.path else ""
                        line_info = f" (line {error.line})" if error.line else ""
                        error_msg = colorize(f"  - {error.message}{path_info}{line_info}", Colors.RED)
                        output.append(error_msg)

        return "\n".join(output)

    @staticmethod
    def format_json(results: List[ValidationResult]) -> str:
        """Format results as JSON."""
        json_results = []

        for result in results:
            json_result = {
                "filename": result.filename,
                "valid": result.is_valid,
                "elapsed_time": result.elapsed_time,
                "errors": [
                    {
                        "message": error.message,
                        "path": error.path,
                        "line": error.line
                    }
                    for error in result.errors
                ]
            }
            json_results.append(json_result)

        return json.dumps(json_results, indent=2)

    @staticmethod
    def format_csv(results: List[ValidationResult]) -> str:
        """Format results as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(["filename", "valid", "error_count", "elapsed_time", "errors"])

        # Data rows
        for result in results:
            errors_str = "; ".join([f"{e.path}: {e.message}" for e in result.errors])
            writer.writerow([
                result.filename,
                result.is_valid,
                len(result.errors),
                f"{result.elapsed_time:.3f}",
                errors_str
            ])

        return output.getvalue()

def load_json_file(filepath: str) -> Dict[str, Any]:
    """Load and parse a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {filepath}: {e}")

def load_json_from_stdin() -> Dict[str, Any]:
    """Load and parse JSON from stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from stdin: {e}")

def validate_single_file(filepath: str, schema: Dict[str, Any], validator: JSONSchemaValidator) -> ValidationResult:
    """Validate a single JSON file against schema."""
    start_time = datetime.now()

    try:
        data = load_json_file(filepath)
        errors = validator.validate(data, schema)
        is_valid = len(errors) == 0
    except Exception as e:
        errors = [ValidationError(str(e))]
        is_valid = False

    elapsed_time = (datetime.now() - start_time).total_seconds()
    return ValidationResult(filepath, is_valid, errors, elapsed_time)

def validate_stdin_data(data: Dict[str, Any], schema: Dict[str, Any], validator: JSONSchemaValidator) -> ValidationResult:
    """Validate JSON data from stdin against schema."""
    start_time = datetime.now()

    try:
        errors = validator.validate(data, schema)
        is_valid = len(errors) == 0
    except Exception as e:
        errors = [ValidationError(str(e))]
        is_valid = False

    elapsed_time = (datetime.now() - start_time).total_seconds()
    return ValidationResult("<stdin>", is_valid, errors, elapsed_time)

def show_progress(current: int, total: int, filename: str):
    """Show progress indicator for batch operations."""
    if sys.stderr.isatty():
        percent = (current / total) * 100
        bar_length = 40
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        sys.stderr.write(f'\r[{bar}] {percent:5.1f}% ({current}/{total}) {filename[:50]}')
        sys.stderr.flush()

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="JSON Schema Validator CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file validation
  jsv validate data.json --schema=schema.json

  # Batch validation
  jsv batch *.json --schema=schema.json --output=csv

  # Pipeline validation
  cat data.json | jsv validate --schema=schema.json

  # Schema verification
  jsv check schema.json
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate JSON data against schema')
    validate_parser.add_argument('file', nargs='?', help='JSON file to validate (use stdin if not provided)')
    validate_parser.add_argument('--schema', '-s', required=True, help='JSON schema file')
    validate_parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text',
                                help='Output format')
    validate_parser.add_argument('--quiet', '-q', action='store_true',
                                help='Quiet mode (only exit codes)')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Validate multiple JSON files')
    batch_parser.add_argument('files', nargs='+', help='JSON files to validate (supports glob patterns)')
    batch_parser.add_argument('--schema', '-s', required=True, help='JSON schema file')
    batch_parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text',
                             help='Output format')
    batch_parser.add_argument('--quiet', '-q', action='store_true',
                             help='Quiet mode (only exit codes)')
    batch_parser.add_argument('--progress', '-p', action='store_true',
                             help='Show progress indicator')

    # Check command
    check_parser = subparsers.add_parser('check', help='Verify JSON schema syntax')
    check_parser.add_argument('schema', help='JSON schema file to check')
    check_parser.add_argument('--quiet', '-q', action='store_true',
                             help='Quiet mode (only exit codes)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'validate':
            # Load schema
            schema = load_json_file(args.schema)
            validator = JSONSchemaValidator()

            # Load data
            if args.file:
                result = validate_single_file(args.file, schema, validator)
                results = [result]
            else:
                # Read from stdin
                data = load_json_from_stdin()
                result = validate_stdin_data(data, schema, validator)
                results = [result]

            # Output results
            if not args.quiet:
                if args.output == 'json':
                    print(OutputFormatter.format_json(results))
                elif args.output == 'csv':
                    print(OutputFormatter.format_csv(results))
                else:
                    print(OutputFormatter.format_text(results))

            # Exit with appropriate code
            sys.exit(0 if all(r.is_valid for r in results) else 1)

        elif args.command == 'batch':
            # Expand glob patterns
            all_files = []
            for pattern in args.files:
                if '*' in pattern or '?' in pattern:
                    all_files.extend(glob.glob(pattern))
                else:
                    all_files.append(pattern)

            if not all_files:
                print(colorize("No files found matching the pattern(s)", Colors.YELLOW), file=sys.stderr)
                sys.exit(1)

            # Load schema
            schema = load_json_file(args.schema)
            validator = JSONSchemaValidator()

            # Validate all files
            results = []
            total_files = len(all_files)

            for i, filepath in enumerate(all_files, 1):
                if args.progress and not args.quiet:
                    show_progress(i, total_files, filepath)

                result = validate_single_file(filepath, schema, validator)
                results.append(result)

            if args.progress and not args.quiet:
                sys.stderr.write('\n')  # New line after progress bar

            # Output results
            if not args.quiet:
                if args.output == 'json':
                    print(OutputFormatter.format_json(results))
                elif args.output == 'csv':
                    print(OutputFormatter.format_csv(results))
                else:
                    print(OutputFormatter.format_text(results))

            # Exit with appropriate code
            sys.exit(0 if all(r.is_valid for r in results) else 1)

        elif args.command == 'check':
            # Just try to load the schema file
            try:
                schema = load_json_file(args.schema)

                if not args.quiet:
                    print(colorize(f"✓ Schema is valid JSON: {args.schema}", Colors.GREEN))

                sys.exit(0)
            except Exception as e:
                if not args.quiet:
                    print(colorize(f"✗ Schema is invalid: {e}", Colors.RED))
                sys.exit(1)

    except KeyboardInterrupt:
        print(colorize("\nOperation cancelled by user", Colors.YELLOW), file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(colorize(f"Error: {e}", Colors.RED), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()