#!/usr/bin/env python3
"""
JSON Schema Validator CLI Tool
Usage: jsv <command> [options]
"""
import argparse
import sys
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        prog='jsv',
        description='JSON Schema Validator - Validate JSON data against schemas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jsv validate data.json schema.json
  jsv validate --data=stdin --schema=schema.json
  jsv batch validate *.json --schema=schema.json --output=csv
  jsv check-schema schema.json --dry-run
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate JSON data against schema')
    validate_parser.add_argument('data_file', nargs='?', help='JSON data file')
    validate_parser.add_argument('schema_file', nargs='?', help='JSON schema file')
    validate_parser.add_argument('--data', help='Data file path or "stdin"')
    validate_parser.add_argument('--schema', help='Schema file path')
    validate_parser.add_argument('--output', choices=['text', 'json', 'csv'], default='text')

    # Check schema command
    check_parser = subparsers.add_parser('check-schema', help='Check schema validity')
    check_parser.add_argument('schema', help='Schema file to check')
    check_parser.add_argument('--dry-run', action='store_true')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        import jsonschema
        from jsonschema import Draft7Validator, FormatChecker
    except ImportError:
        print("Error: jsonschema library required. Install with: pip install jsonschema", file=sys.stderr)
        return 1

    if args.command == 'validate':
        # Get file paths
        data_file = args.data or args.data_file
        schema_file = args.schema or args.schema_file

        if not data_file or not schema_file:
            print("Error: Both data and schema files required", file=sys.stderr)
            return 1

        try:
            # Load schema
            with open(schema_file, 'r') as f:
                schema = json.load(f)

            # Load data
            if data_file == 'stdin':
                data = json.load(sys.stdin)
            else:
                with open(data_file, 'r') as f:
                    data = json.load(f)

            # Validate
            validator = Draft7Validator(schema, format_checker=FormatChecker())
            errors = list(validator.iter_errors(data))

            if not errors:
                print("✓ Valid")
                return 0
            else:
                print("✗ Invalid")
                for error in errors:
                    print(f"  - {error.message}")
                return 1

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.command == 'check-schema':
        if args.dry_run:
            print(f"Dry run: Would check schema {args.schema}")
            return 0

        try:
            with open(args.schema, 'r') as f:
                schema = json.load(f)

            Draft7Validator.check_schema(schema)
            print("✓ Schema is valid")
            return 0

        except Exception as e:
            print(f"✗ Schema invalid: {e}")
            return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())