"""
Command-line interface for JSON Schema Validator.
Provides multiple commands and output formats.
"""

import argparse
import json
import sys
import os
import glob
from typing import List, Dict, Any, Optional

from .validator import JSONSchemaValidator
from .output import OutputFormatter
from .batch import BatchValidator


class CLIValidator:
    """CLI validation orchestrator."""

    def __init__(self):
        self.output_formatter = OutputFormatter()

    def validate_file(self, data_file: str, schema_file: str) -> Dict[str, Any]:
        """
        Validate a single JSON file against schema.

        Args:
            data_file: Path to JSON data file
            schema_file: Path to JSON schema file

        Returns:
            dict: Validation result with file info
        """
        try:
            # Load schema
            with open(schema_file, 'r') as f:
                schema = json.load(f)

            # Load data
            with open(data_file, 'r') as f:
                data = json.load(f)

            # Validate
            validator = JSONSchemaValidator(schema)
            result = validator.validate_with_errors(data)
            result['file'] = data_file

            return result

        except FileNotFoundError as e:
            return {
                'valid': False,
                'file': data_file,
                'errors': [f"File not found: {e}"]
            }
        except json.JSONDecodeError as e:
            return {
                'valid': False,
                'file': data_file,
                'errors': [f"JSON decode error: {e}"]
            }
        except Exception as e:
            return {
                'valid': False,
                'file': data_file,
                'errors': [f"Unexpected error: {e}"]
            }

    def validate_stdin(self, schema_file: str) -> Dict[str, Any]:
        """
        Validate JSON data from stdin.

        Args:
            schema_file: Path to JSON schema file

        Returns:
            dict: Validation result
        """
        try:
            # Load schema
            with open(schema_file, 'r') as f:
                schema = json.load(f)

            # Read from stdin
            json_input = sys.stdin.read()
            data = json.loads(json_input)

            # Validate
            validator = JSONSchemaValidator(schema)
            result = validator.validate_with_errors(data)
            result['file'] = '<stdin>'

            return result

        except json.JSONDecodeError as e:
            return {
                'valid': False,
                'file': '<stdin>',
                'errors': [f"JSON decode error: {e}"]
            }
        except Exception as e:
            return {
                'valid': False,
                'file': '<stdin>',
                'errors': [f"Unexpected error: {e}"]
            }

    def check_schema(self, schema_file: str) -> Dict[str, Any]:
        """
        Check if a schema file is valid.

        Args:
            schema_file: Path to JSON schema file

        Returns:
            dict: Schema validation result
        """
        try:
            with open(schema_file, 'r') as f:
                schema = json.load(f)

            # Basic schema validation - check for required structure
            if not isinstance(schema, dict):
                return {
                    'valid': False,
                    'file': schema_file,
                    'errors': ["Schema must be a JSON object"]
                }

            # Basic schema validation - check for known types and structure
            errors = []

            # Check for valid type if specified
            if 'type' in schema:
                valid_types = {'string', 'number', 'integer', 'boolean', 'object', 'array', 'null'}
                if schema['type'] not in valid_types:
                    errors.append(f"Unknown type: {schema['type']}")

            # Check for valid format if specified
            if 'format' in schema:
                valid_formats = {'email', 'uri', 'date'}
                if schema['format'] not in valid_formats:
                    errors.append(f"Unknown format: {schema['format']}")

            # Try to create a validator - this will catch other basic schema issues
            try:
                validator = JSONSchemaValidator(schema)
                # Test with a simple value to see if schema works
                validator.validate("test")
            except Exception as e:
                errors.append(f"Schema validation error: {e}")

            return {
                'valid': len(errors) == 0,
                'file': schema_file,
                'errors': errors
            }

        except FileNotFoundError:
            return {
                'valid': False,
                'file': schema_file,
                'errors': ["Schema file not found"]
            }
        except json.JSONDecodeError as e:
            return {
                'valid': False,
                'file': schema_file,
                'errors': [f"JSON decode error: {e}"]
            }

    def batch_validate(self, files: List[str], schema_file: str) -> List[Dict[str, Any]]:
        """
        Validate multiple files against schema.

        Args:
            files: List of file paths to validate
            schema_file: Path to JSON schema file

        Returns:
            list: List of validation results
        """
        results = []
        for file_path in files:
            result = self.validate_file(file_path, schema_file)
            results.append(result)
        return results


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args: Optional argument list (for testing)

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        prog='jsv',
        description='JSON Schema Validator CLI Tool'
    )

    # Global options
    parser.add_argument('--output', '-o',
                       choices=['text', 'json', 'csv'],
                       default='text',
                       help='Output format (default: text)')
    parser.add_argument('--quiet', '-q',
                       action='store_true',
                       help='Quiet mode - only return exit codes')

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate JSON data against schema')
    validate_parser.add_argument('data_file', nargs='?', help='JSON data file (omit for stdin)')
    validate_parser.add_argument('--schema', '-s', required=True, help='JSON schema file')
    validate_parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text', help='Output format')
    validate_parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode - only return exit codes')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Validate multiple JSON files')
    batch_parser.add_argument('pattern', help='File pattern (e.g., *.json)')
    batch_parser.add_argument('--schema', '-s', required=True, help='JSON schema file')
    batch_parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text', help='Output format')
    batch_parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode - only return exit codes')

    # Check command
    check_parser = subparsers.add_parser('check', help='Check schema validity')
    check_parser.add_argument('schema_file', help='JSON schema file to check')
    check_parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text', help='Output format')
    check_parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode - only return exit codes')

    return parser.parse_args(args)


def main() -> int:
    """
    Main CLI entry point.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    args = parse_args()

    if not args.command:
        print("Error: No command specified. Use --help for usage information.")
        return 1

    cli = CLIValidator()
    output_formatter = OutputFormatter()

    try:
        if args.command == 'validate':
            if args.data_file:
                result = cli.validate_file(args.data_file, args.schema)
            else:
                result = cli.validate_stdin(args.schema)

            if not args.quiet:
                output = output_formatter.format_single_result(result, args.output)
                print(output)

            return 0 if result['valid'] else 1

        elif args.command == 'batch':
            files = glob.glob(args.pattern)
            if not files:
                if not args.quiet:
                    print(f"No files found matching pattern: {args.pattern}")
                return 1

            # Use batch validator for better progress tracking
            batch_validator = BatchValidator()
            results = batch_validator.validate_batch(files, args.schema, show_progress=not args.quiet)

            if not args.quiet:
                output = output_formatter.format_batch_results(results, args.output)
                print(output)

            # Return 1 if any validation failed
            return 0 if all(r['valid'] for r in results) else 1

        elif args.command == 'check':
            result = cli.check_schema(args.schema_file)

            if not args.quiet:
                output = output_formatter.format_single_result(result, args.output)
                print(output)

            return 0 if result['valid'] else 1

        else:
            print(f"Unknown command: {args.command}")
            return 1

    except KeyboardInterrupt:
        if not args.quiet:
            print("\nInterrupted by user")
        return 1
    except Exception as e:
        if not args.quiet:
            print(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())