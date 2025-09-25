#!/usr/bin/env python3
"""
JSON Schema Validator CLI Tool
A command-line tool for validating JSON data against JSON schemas.
"""

import argparse
import json
import sys
import os
import csv
import io
from pathlib import Path
from typing import Dict, List, Any, Optional
import glob
import time
from datetime import datetime

try:
    import jsonschema
    from jsonschema import Draft7Validator, validators
    from jsonschema.exceptions import ValidationError, SchemaError
except ImportError:
    print("Error: jsonschema library is required. Install with: pip install jsonschema")
    sys.exit(1)

class ProgressIndicator:
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()

    def update(self, increment: int = 1):
        self.current += increment
        if self.total > 0:
            percentage = (self.current / self.total) * 100
            elapsed = time.time() - self.start_time
            if self.current > 0:
                eta = (elapsed / self.current) * (self.total - self.current)
                print(f"\r{self.description}: {self.current}/{self.total} ({percentage:.1f}%) - ETA: {eta:.1f}s", end="", flush=True)
            else:
                print(f"\r{self.description}: {self.current}/{self.total} ({percentage:.1f}%)", end="", flush=True)
        else:
            print(f"\r{self.description}: {self.current}", end="", flush=True)

    def finish(self):
        elapsed = time.time() - self.start_time
        print(f"\r{self.description}: {self.current}/{self.total} (100.0%) - Completed in {elapsed:.1f}s")

class ValidationResult:
    def __init__(self, file_path: str, is_valid: bool, errors: List[str] = None, schema_file: str = None):
        self.file_path = file_path
        self.is_valid = is_valid
        self.errors = errors or []
        self.schema_file = schema_file
        self.timestamp = datetime.now().isoformat()

class JSONSchemaValidator:
    def __init__(self):
        self.results: List[ValidationResult] = []

    def load_json(self, file_path: str) -> Dict[str, Any]:
        """Load JSON from file or stdin."""
        try:
            if file_path == "stdin":
                content = sys.stdin.read()
                return json.loads(content)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {str(e)}")
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Error reading {file_path}: {str(e)}")

    def validate_schema(self, schema: Dict[str, Any]) -> List[str]:
        """Validate that the schema itself is valid."""
        errors = []
        try:
            Draft7Validator.check_schema(schema)
        except SchemaError as e:
            errors.append(f"Invalid schema: {str(e)}")
        return errors

    def validate_data(self, data: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
        """Validate data against schema and return list of error messages."""
        errors = []
        try:
            validator = Draft7Validator(schema)
            for error in validator.iter_errors(data):
                error_path = " -> ".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
                errors.append(f"Path '{error_path}': {error.message}")
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
        return errors

    def validate_single(self, data_file: str, schema_file: str, dry_run: bool = False) -> ValidationResult:
        """Validate a single JSON file against a schema."""
        try:
            # Load schema
            schema = self.load_json(schema_file)

            # Validate schema itself
            schema_errors = self.validate_schema(schema)
            if schema_errors:
                return ValidationResult(data_file, False, schema_errors, schema_file)

            if dry_run:
                return ValidationResult(data_file, True, ["Dry run - schema is valid"], schema_file)

            # Load and validate data
            data = self.load_json(data_file)
            errors = self.validate_data(data, schema)
            is_valid = len(errors) == 0

            return ValidationResult(data_file, is_valid, errors, schema_file)

        except Exception as e:
            return ValidationResult(data_file, False, [str(e)], schema_file)

    def validate_batch(self, data_files: List[str], schema_file: str, dry_run: bool = False) -> List[ValidationResult]:
        """Validate multiple JSON files against a schema with progress indication."""
        results = []
        progress = ProgressIndicator(len(data_files), "Validating files")

        for data_file in data_files:
            result = self.validate_single(data_file, schema_file, dry_run)
            results.append(result)
            progress.update()

        progress.finish()
        return results

class OutputFormatter:
    @staticmethod
    def format_text(results: List[ValidationResult]) -> str:
        """Format results as human-readable text."""
        output = []
        valid_count = sum(1 for r in results if r.is_valid)
        total_count = len(results)

        output.append(f"Validation Results: {valid_count}/{total_count} files valid\n")
        output.append("=" * 50)

        for result in results:
            output.append(f"\nFile: {result.file_path}")
            output.append(f"Schema: {result.schema_file}")
            output.append(f"Status: {'VALID' if result.is_valid else 'INVALID'}")
            output.append(f"Timestamp: {result.timestamp}")

            if not result.is_valid and result.errors:
                output.append("Errors:")
                for error in result.errors:
                    output.append(f"  - {error}")

        return "\n".join(output)

    @staticmethod
    def format_json(results: List[ValidationResult]) -> str:
        """Format results as JSON."""
        json_results = []
        for result in results:
            json_results.append({
                "file_path": result.file_path,
                "schema_file": result.schema_file,
                "is_valid": result.is_valid,
                "errors": result.errors,
                "timestamp": result.timestamp
            })

        return json.dumps({
            "summary": {
                "total_files": len(results),
                "valid_files": sum(1 for r in results if r.is_valid),
                "invalid_files": sum(1 for r in results if not r.is_valid)
            },
            "results": json_results
        }, indent=2)

    @staticmethod
    def format_csv(results: List[ValidationResult]) -> str:
        """Format results as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(["file_path", "schema_file", "is_valid", "error_count", "errors", "timestamp"])

        # Write data
        for result in results:
            error_text = "; ".join(result.errors) if result.errors else ""
            writer.writerow([
                result.file_path,
                result.schema_file,
                result.is_valid,
                len(result.errors),
                error_text,
                result.timestamp
            ])

        return output.getvalue()

def expand_file_patterns(patterns: List[str]) -> List[str]:
    """Expand file patterns (with wildcards) to actual file paths."""
    files = []
    for pattern in patterns:
        if '*' in pattern or '?' in pattern:
            files.extend(glob.glob(pattern))
        else:
            files.append(pattern)
    return files

def main():
    parser = argparse.ArgumentParser(
        description="JSON Schema Validator CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jsv validate data.json schema.json
  jsv batch validate *.json --schema=schema.json --output=csv
  jsv check-schema schema.json --dry-run
  jsv validate --data=stdin --schema=schema.json
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a single JSON file')
    validate_parser.add_argument('data', nargs='?', help='JSON data file')
    validate_parser.add_argument('schema', nargs='?', help='JSON schema file')
    validate_parser.add_argument('--data', dest='data_flag', help='JSON data file or "stdin"')
    validate_parser.add_argument('--schema', dest='schema_flag', help='JSON schema file')
    validate_parser.add_argument('--output', choices=['text', 'json', 'csv'], default='text',
                                help='Output format (default: text)')
    validate_parser.add_argument('--dry-run', action='store_true',
                                help='Only validate schema, skip data validation')

    # Batch validate command
    batch_parser = subparsers.add_parser('batch', help='Batch validation commands')
    batch_subparsers = batch_parser.add_subparsers(dest='batch_command')

    batch_validate_parser = batch_subparsers.add_parser('validate', help='Validate multiple JSON files')
    batch_validate_parser.add_argument('files', nargs='+', help='JSON files to validate (supports wildcards)')
    batch_validate_parser.add_argument('--schema', required=True, help='JSON schema file')
    batch_validate_parser.add_argument('--output', choices=['text', 'json', 'csv'], default='text',
                                      help='Output format (default: text)')
    batch_validate_parser.add_argument('--dry-run', action='store_true',
                                      help='Only validate schema, skip data validation')

    # Check schema command
    check_parser = subparsers.add_parser('check-schema', help='Check if a schema is valid')
    check_parser.add_argument('schema', help='JSON schema file to check')
    check_parser.add_argument('--output', choices=['text', 'json', 'csv'], default='text',
                             help='Output format (default: text)')
    check_parser.add_argument('--dry-run', action='store_true', help='Dry run mode')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    validator = JSONSchemaValidator()
    formatter = OutputFormatter()

    try:
        if args.command == 'validate':
            # Handle single file validation
            # Get data file - prefer flag over positional
            data_file = getattr(args, 'data_flag', None) or getattr(args, 'data', None)

            # Get schema file - prefer flag over positional
            schema_file = getattr(args, 'schema_flag', None) or getattr(args, 'schema', None)

            if not data_file:
                print("Error: No data file specified. Use 'jsv validate data.json schema.json' or --data flag.", file=sys.stderr)
                return 1

            if not schema_file:
                print("Error: No schema file specified. Use 'jsv validate data.json schema.json' or --schema flag.", file=sys.stderr)
                return 1

            result = validator.validate_single(data_file, schema_file, args.dry_run)
            results = [result]

        elif args.command == 'batch' and args.batch_command == 'validate':
            # Handle batch validation
            files = expand_file_patterns(args.files)
            if not files:
                print("Error: No files found matching the patterns.", file=sys.stderr)
                return 1

            results = validator.validate_batch(files, args.schema, args.dry_run)

        elif args.command == 'check-schema':
            # Handle schema checking
            schema_file = args.schema if hasattr(args, 'schema') and args.schema else None
            if not schema_file:
                print("Error: No schema file specified.", file=sys.stderr)
                return 1
            result = validator.validate_single("dummy", schema_file, dry_run=True)
            results = [result]

        else:
            print(f"Error: Unknown command or subcommand.", file=sys.stderr)
            return 1

        # Format and output results
        if args.output == 'json':
            print(formatter.format_json(results))
        elif args.output == 'csv':
            print(formatter.format_csv(results))
        else:
            print(formatter.format_text(results))

        # Return exit code based on validation results
        if any(not result.is_valid for result in results):
            return 1
        else:
            return 0

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())