"""Command-line interface for JSON Schema Validator CLI."""

import sys
from pathlib import Path
from typing import List, Optional

import click

from . import __version__
from .validator import JSONValidator
from .schema_checker import SchemaChecker
from .formatters import TextFormatter, JSONFormatter, CSVFormatter
from .utils.file_utils import find_files
from .utils.progress import ProgressTracker
from .exceptions import JSVError, SchemaError, FileError, UsageError


# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_FAILED = 1
EXIT_SCHEMA_ERROR = 2
EXIT_FILE_ERROR = 3
EXIT_USAGE_ERROR = 4


def get_formatter(output_format: str, use_color: bool = True, quiet: bool = False):
    """Get the appropriate formatter for the output format.

    Args:
        output_format: Output format (text, json, csv)
        use_color: Whether to use colored output
        quiet: Whether to suppress detailed output

    Returns:
        Formatter instance

    Raises:
        UsageError: If output format is unknown
    """
    if output_format == "text":
        return TextFormatter(use_color=use_color, show_summary=not quiet)
    elif output_format == "json":
        return JSONFormatter(indent=2)
    elif output_format == "csv":
        return CSVFormatter(include_headers=True)
    else:
        raise UsageError(f"Unknown output format: {output_format}")


@click.group()
@click.version_option(version=__version__)
@click.option('--quiet', '-q', is_flag=True, help='Quiet mode - only return exit codes')
@click.option('--no-color', is_flag=True, help='Disable colored output')
@click.option('--output', '-o', type=click.Choice(['text', 'json', 'csv']),
              default='text', help='Output format')
@click.pass_context
def cli(ctx, quiet, no_color, output):
    """JSON Schema Validator CLI - Validate JSON data against JSON Schema."""
    # Store global options in context
    ctx.ensure_object(dict)
    ctx.obj['quiet'] = quiet
    ctx.obj['use_color'] = not no_color
    ctx.obj['output_format'] = output


@cli.command()
@click.argument('file', required=False)
@click.option('--schema', '-s', required=True, help='JSON Schema file path')
@click.option('--strict', is_flag=True, help='Enable strict validation mode')
@click.pass_context
def validate(ctx, file, schema, strict):
    """Validate a JSON file against a schema.

    If FILE is not provided, reads JSON data from stdin.

    Examples:
        jsv validate data.json --schema=schema.json
        cat data.json | jsv validate --schema=schema.json
    """
    quiet = ctx.obj['quiet']
    use_color = ctx.obj['use_color']
    output_format = ctx.obj['output_format']

    try:
        # Create validator
        validator = JSONValidator(schema, strict=strict)

        # Validate from file or stdin
        if file:
            result = validator.validate_file(file)
        else:
            result = validator.validate_stdin()

        # Output results unless in quiet mode
        if not quiet:
            formatter = get_formatter(output_format, use_color, quiet)
            output = formatter.format_results([result])
            click.echo(output)

        # Exit with appropriate code
        if result.is_valid:
            sys.exit(EXIT_SUCCESS)
        else:
            sys.exit(EXIT_VALIDATION_FAILED)

    except SchemaError as e:
        if not quiet:
            click.echo(f"Schema error: {e}", err=True)
        sys.exit(EXIT_SCHEMA_ERROR)
    except FileError as e:
        if not quiet:
            click.echo(f"File error: {e}", err=True)
        sys.exit(EXIT_FILE_ERROR)
    except JSVError as e:
        if not quiet:
            click.echo(f"Error: {e}", err=True)
        sys.exit(EXIT_USAGE_ERROR)


@cli.command()
@click.argument('files', nargs=-1, required=True)
@click.option('--schema', '-s', required=True, help='JSON Schema file path')
@click.option('--strict', is_flag=True, help='Enable strict validation mode')
@click.option('--continue-on-error', is_flag=True,
              help='Continue validation even if some files fail')
@click.option('--max-workers', type=int, default=4,
              help='Number of parallel validation workers')
@click.pass_context
def batch(ctx, files, schema, strict, continue_on_error, max_workers):
    """Validate multiple JSON files against a schema.

    Supports glob patterns for file selection.

    Examples:
        jsv batch *.json --schema=schema.json
        jsv batch data/*.json config/*.json --schema=schema.json --output=csv
    """
    quiet = ctx.obj['quiet']
    use_color = ctx.obj['use_color']
    output_format = ctx.obj['output_format']

    try:
        # Find all files matching the patterns
        file_paths = find_files(list(files))

        if not file_paths:
            if not quiet:
                click.echo("No files found matching the patterns.", err=True)
            sys.exit(EXIT_FILE_ERROR)

        # Create validator
        validator = JSONValidator(schema, strict=strict)

        # Show progress for batch operations
        show_progress = not quiet and len(file_paths) > 1

        # Validate files with progress tracking
        with ProgressTracker(len(file_paths), "Validating files", show_progress) as progress:
            results = []

            # For large batches, use parallel validation
            if len(file_paths) > 3:
                batch_results = validator.validate_batch(file_paths, max_workers)
                for result in batch_results:
                    results.append(result)
                    progress.update(1)

                    # Update progress with current status
                    valid_count = sum(1 for r in results if r.is_valid)
                    invalid_count = len(results) - valid_count
                    progress.set_postfix(valid=valid_count, invalid=invalid_count)

                    # Stop on first error if not continuing
                    if not continue_on_error and not result.is_valid:
                        break
            else:
                # Sequential validation for small batches
                for file_path in file_paths:
                    result = validator.validate_file(file_path)
                    results.append(result)
                    progress.update(1)

                    # Stop on first error if not continuing
                    if not continue_on_error and not result.is_valid:
                        break

        # Output results unless in quiet mode
        if not quiet:
            formatter = get_formatter(output_format, use_color, quiet)
            output = formatter.format_results(results)
            click.echo(output)

        # Determine exit code
        if all(r.is_valid for r in results):
            sys.exit(EXIT_SUCCESS)
        else:
            sys.exit(EXIT_VALIDATION_FAILED)

    except SchemaError as e:
        if not quiet:
            click.echo(f"Schema error: {e}", err=True)
        sys.exit(EXIT_SCHEMA_ERROR)
    except FileError as e:
        if not quiet:
            click.echo(f"File error: {e}", err=True)
        sys.exit(EXIT_FILE_ERROR)
    except JSVError as e:
        if not quiet:
            click.echo(f"Error: {e}", err=True)
        sys.exit(EXIT_USAGE_ERROR)


@cli.command()
@click.argument('schema_file')
@click.pass_context
def check(ctx, schema_file):
    """Verify that a JSON Schema file is valid.

    Examples:
        jsv check schema.json
        jsv check schema.json --output=json
    """
    quiet = ctx.obj['quiet']
    use_color = ctx.obj['use_color']
    output_format = ctx.obj['output_format']

    try:
        # Check the schema
        checker = SchemaChecker()
        result = checker.check_schema(schema_file)

        # Output results unless in quiet mode
        if not quiet:
            formatter = get_formatter(output_format, use_color, quiet)
            output = formatter.format_schema_check(result)
            click.echo(output)

        # Exit with appropriate code
        if result['is_valid']:
            sys.exit(EXIT_SUCCESS)
        else:
            sys.exit(EXIT_SCHEMA_ERROR)

    except SchemaError as e:
        if not quiet:
            click.echo(f"Schema error: {e}", err=True)
        sys.exit(EXIT_SCHEMA_ERROR)
    except FileError as e:
        if not quiet:
            click.echo(f"File error: {e}", err=True)
        sys.exit(EXIT_FILE_ERROR)
    except JSVError as e:
        if not quiet:
            click.echo(f"Error: {e}", err=True)
        sys.exit(EXIT_USAGE_ERROR)


def main():
    """Main entry point for the CLI application."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled by user.", err=True)
        sys.exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(EXIT_USAGE_ERROR)


if __name__ == '__main__':
    main()