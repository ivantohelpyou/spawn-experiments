"""
Command-line interface for JSON Schema Validator.
Built using Click and following TDD approach.
"""

import click
import json
import sys
import csv
import io
from pathlib import Path
from typing import List, Dict, Any
from validator import JSONSchemaValidator, ValidationResult
import colorama
from colorama import Fore, Style

# Initialize colorama for colored output
colorama.init()


class OutputFormatter:
    """Handles different output formats for validation results."""

    @staticmethod
    def format_text(results: List[ValidationResult], colored: bool = True) -> str:
        """Format results as human-readable text."""
        output = []

        for result in results:
            if result.filename:
                prefix = f"{result.filename}: "
            else:
                prefix = ""

            if result.is_valid:
                if colored:
                    output.append(f"{prefix}{Fore.GREEN}✓ Valid{Style.RESET_ALL}")
                else:
                    output.append(f"{prefix}✓ Valid")
            else:
                if colored:
                    output.append(f"{prefix}{Fore.RED}✗ Invalid{Style.RESET_ALL}")
                    for error in result.errors:
                        output.append(f"  {Fore.RED}Error: {error}{Style.RESET_ALL}")
                else:
                    output.append(f"{prefix}✗ Invalid")
                    for error in result.errors:
                        output.append(f"  Error: {error}")

        return "\n".join(output)

    @staticmethod
    def format_json(results: List[ValidationResult]) -> str:
        """Format results as JSON."""
        output_data = []

        for result in results:
            output_data.append({
                "filename": result.filename,
                "valid": result.is_valid,
                "errors": result.errors
            })

        return json.dumps(output_data, indent=2)

    @staticmethod
    def format_csv(results: List[ValidationResult]) -> str:
        """Format results as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(["filename", "valid", "errors"])

        # Write data
        for result in results:
            errors_str = "; ".join(result.errors) if result.errors else ""
            writer.writerow([
                result.filename or "",
                "true" if result.is_valid else "false",
                errors_str
            ])

        return output.getvalue()


@click.group()
def cli():
    """JSON Schema Validator (jsv) - Validate JSON files against JSON Schema."""
    pass


@cli.command()
@click.argument('data_file', required=False)
@click.option('--schema', '-s', required=True, help='JSON schema file path')
@click.option('--quiet', '-q', is_flag=True, help='Quiet mode - only return exit codes')
@click.option('--no-color', is_flag=True, help='Disable colored output')
def validate(data_file, schema, quiet, no_color):
    """Validate a JSON file against a schema."""
    validator = JSONSchemaValidator()

    try:
        if data_file:
            # Validate file
            result = validator.validate_file(data_file, schema)
        else:
            # Read from stdin
            stdin_data = sys.stdin.read()
            if not stdin_data.strip():
                click.echo("Error: No input data provided", err=True)
                sys.exit(1)

            try:
                data = json.loads(stdin_data)
                with open(schema, 'r') as f:
                    schema_data = json.load(f)
                result = validator.validate(data, schema_data)
            except json.JSONDecodeError as e:
                click.echo(f"Error: Invalid JSON input: {e}", err=True)
                sys.exit(1)

        if quiet:
            # Quiet mode - only return exit code
            sys.exit(0 if result.is_valid else 1)

        # Format and display output
        formatter = OutputFormatter()
        output = formatter.format_text([result], colored=not no_color)
        click.echo(output)

        sys.exit(0 if result.is_valid else 1)

    except FileNotFoundError as e:
        if not quiet:
            click.echo(f"Error: File not found: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        if not quiet:
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('files', nargs=-1, required=True)
@click.option('--schema', '-s', required=True, help='JSON schema file path')
@click.option('--output', '-o', type=click.Choice(['text', 'json', 'csv']), default='text',
              help='Output format')
@click.option('--quiet', '-q', is_flag=True, help='Quiet mode - only return exit codes')
@click.option('--no-color', is_flag=True, help='Disable colored output')
def batch(files, schema, output, quiet, no_color):
    """Validate multiple JSON files against a schema."""
    validator = JSONSchemaValidator()
    results = []

    try:
        for file_path in files:
            try:
                result = validator.validate_file(file_path, schema)
                results.append(result)
            except Exception as e:
                # Create error result for failed file
                error_result = ValidationResult(
                    is_valid=False,
                    errors=[str(e)],
                    filename=file_path
                )
                results.append(error_result)

        if quiet:
            # Quiet mode - only return exit code
            has_invalid = any(not result.is_valid for result in results)
            sys.exit(1 if has_invalid else 0)

        # Format and display output
        formatter = OutputFormatter()

        if output == 'json':
            output_text = formatter.format_json(results)
        elif output == 'csv':
            output_text = formatter.format_csv(results)
        else:  # text
            output_text = formatter.format_text(results, colored=not no_color)

        click.echo(output_text)

        # Exit with error if any file is invalid
        has_invalid = any(not result.is_valid for result in results)
        sys.exit(1 if has_invalid else 0)

    except FileNotFoundError as e:
        if not quiet:
            click.echo(f"Error: Schema file not found: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        if not quiet:
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('schema_file')
@click.option('--quiet', '-q', is_flag=True, help='Quiet mode - only return exit codes')
def check(schema_file, quiet):
    """Verify that a JSON Schema file is valid."""
    try:
        with open(schema_file, 'r') as f:
            schema_data = json.load(f)

        # Validate schema using jsonschema's meta-schema
        from jsonschema import Draft7Validator
        from jsonschema.exceptions import SchemaError

        try:
            Draft7Validator.check_schema(schema_data)

            if not quiet:
                click.echo(f"{Fore.GREEN}✓ Valid schema{Style.RESET_ALL}")
            sys.exit(0)

        except SchemaError as e:
            if not quiet:
                click.echo(f"{Fore.RED}✗ Invalid schema: {e}{Style.RESET_ALL}", err=True)
            sys.exit(1)

    except FileNotFoundError:
        if not quiet:
            click.echo(f"Error: Schema file not found: {schema_file}", err=True)
        sys.exit(1)
    except json.JSONDecodeError as e:
        if not quiet:
            click.echo(f"Error: Invalid JSON in schema file: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        if not quiet:
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)


# Expose commands for testing
validate_command = validate
batch_command = batch
check_command = check


if __name__ == '__main__':
    cli()