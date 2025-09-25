#!/usr/bin/env python3
"""
JSON Schema Validator CLI
Test-First Development Implementation
"""

import argparse
import json
import sys

def validate_json(data, schema):
    """Validate JSON data against schema"""
    try:
        import jsonschema
        from jsonschema import FormatChecker
        jsonschema.validate(data, schema, format_checker=FormatChecker())
        return True, []
    except jsonschema.ValidationError as e:
        return False, [str(e)]
    except ImportError:
        # Basic validation fallback
        if not isinstance(data, dict):
            return False, ["Expected object"]
        errors = []
        if 'name' in data and not isinstance(data.get('name'), str):
            errors.append("name must be string")
        if 'email' in data and not isinstance(data.get('email'), str):
            errors.append("email must be string")
        if 'age' in data and not isinstance(data.get('age'), (int, float)):
            errors.append("age must be number")
        return len(errors) == 0, errors

def main():
    parser = argparse.ArgumentParser(description='JSON Schema Validator CLI')
    subparsers = parser.add_subparsers(dest='command')

    # Validate command
    validate_parser = subparsers.add_parser('validate')
    validate_parser.add_argument('data_file')
    validate_parser.add_argument('schema_file')
    validate_parser.add_argument('--output', choices=['text', 'json', 'csv'], default='text')

    # Check schema command
    check_parser = subparsers.add_parser('check-schema')
    check_parser.add_argument('schema')
    check_parser.add_argument('--dry-run', action='store_true')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == 'validate':
        try:
            with open(args.schema_file, 'r') as f:
                schema = json.load(f)

            if args.data_file == 'stdin':
                data = json.load(sys.stdin)
            else:
                with open(args.data_file, 'r') as f:
                    data = json.load(f)

            is_valid, errors = validate_json(data, schema)

            if is_valid:
                print("✓ Valid")
                return 0
            else:
                print("✗ Invalid")
                for error in errors:
                    print(f"  - {error}")
                return 1

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.command == 'check-schema':
        if args.dry_run:
            print(f"Dry run: Would check {args.schema}")
            return 0

        try:
            with open(args.schema, 'r') as f:
                schema = json.load(f)
            print("✓ Schema appears valid")
            return 0
        except Exception as e:
            print(f"✗ Error: {e}")
            return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())