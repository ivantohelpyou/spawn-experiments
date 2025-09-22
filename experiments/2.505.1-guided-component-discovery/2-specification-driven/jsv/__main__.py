"""
Main entry point for JSV (JSON Schema Validator) CLI tool.
Handles argument parsing and command dispatch.
"""

import sys
import argparse
from typing import List, Optional
from .cli.commands import validate_command, batch_command, check_command
from .cli.progress import colored


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for JSV CLI."""
    parser = argparse.ArgumentParser(
        prog='jsv',
        description='JSON Schema Validator - Validate JSON data against JSON Schema (Draft 7 subset)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Single file validation
  jsv validate data.json --schema=schema.json
  jsv validate data.json --schema=schema.json --format=json

  # Batch validation
  jsv batch *.json --schema=schema.json
  jsv batch file1.json file2.json --schema=schema.json --output=csv

  # Pipeline validation
  cat data.json | jsv validate --schema=schema.json
  echo '{"name":"test"}' | jsv validate --schema=schema.json --format=json

  # Schema verification
  jsv check schema.json
  cat schema.json | jsv check

  # Quiet mode (only exit codes)
  jsv validate data.json --schema=schema.json --quiet

Format support:
  email, date (MM/DD/YYYY or DD/MM/YYYY), uri/url

Output formats:
  text (default), json, csv
        '''
    )

    parser.add_argument('--version', action='version', version='JSV 1.0.0')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Quiet mode - only return exit codes (0=valid, 1=invalid)')
    parser.add_argument('--no-color', action='store_true',
                       help='Disable colored output')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a single JSON file')
    validate_parser.add_argument('data_file', nargs='?', default='-',
                                help='JSON data file (use "-" or omit for stdin)')
    validate_parser.add_argument('--schema', '-s', required=True,
                                help='JSON schema file')
    validate_parser.add_argument('--format', '-f', choices=['text', 'json', 'csv'], default='text',
                                help='Output format (default: text)')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Validate multiple JSON files')
    batch_parser.add_argument('data_files', nargs='+',
                             help='JSON data files (supports glob patterns)')
    batch_parser.add_argument('--schema', '-s', required=True,
                             help='JSON schema file')
    batch_parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text',
                             help='Output format (default: text)')
    batch_parser.add_argument('--progress', '-p', action='store_true',
                             help='Show progress bar')

    # Check command
    check_parser = subparsers.add_parser('check', help='Verify JSON Schema file')
    check_parser.add_argument('schema_file', nargs='?', default='-',
                             help='JSON schema file (use "-" or omit for stdin)')

    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for JSV CLI.

    Args:
        args: Command line arguments (defaults to sys.argv)

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    # Handle no command case
    if not parsed_args.command:
        parser.print_help()
        return 1

    try:
        # Dispatch to appropriate command
        if parsed_args.command == 'validate':
            return validate_command(
                data_file=parsed_args.data_file,
                schema_file=parsed_args.schema,
                quiet=parsed_args.quiet,
                format_name=parsed_args.format,
                no_color=parsed_args.no_color
            )

        elif parsed_args.command == 'batch':
            return batch_command(
                data_files=parsed_args.data_files,
                schema_file=parsed_args.schema,
                quiet=parsed_args.quiet,
                format_name=parsed_args.output,
                no_color=parsed_args.no_color,
                progress=parsed_args.progress
            )

        elif parsed_args.command == 'check':
            return check_command(
                schema_file=parsed_args.schema_file,
                quiet=parsed_args.quiet,
                no_color=parsed_args.no_color
            )

        else:
            if not parsed_args.quiet:
                colored.print_error(f"Unknown command: {parsed_args.command}")
            return 1

    except KeyboardInterrupt:
        if not parsed_args.quiet:
            colored.print_warning("\nOperation cancelled by user")
        return 1
    except Exception as e:
        if not parsed_args.quiet:
            colored.print_error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())