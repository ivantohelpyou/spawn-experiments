#!/usr/bin/env python3
"""
JSON Schema Validator CLI Tool - Method 1E External Library Variant
Professional JSON validation with rich external library integration
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
import jsonschema
from jsonschema import Draft7Validator, ValidationError
from email_validator import validate_email, EmailNotValidError
import validators
import colorama

# Initialize colorama for cross-platform colored output
colorama.init()

console = Console()


class ValidationResult:
    """Container for validation results with rich formatting support"""

    def __init__(self, is_valid: bool, errors: List[str] = None, warnings: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []
        self.details = {}

    def add_error(self, error: str):
        """Add an error to the result"""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str):
        """Add a warning to the result"""
        self.warnings.append(warning)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON output"""
        return {
            "valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings)
        }


class JSONSchemaValidator:
    """Professional JSON Schema validator with external library integration"""

    def __init__(self, output_format: str = "text", quiet: bool = False):
        self.output_format = output_format
        self.quiet = quiet
        self.console = Console(quiet=quiet)

    def validate_json_data(self, data: Any, schema: Dict[str, Any]) -> ValidationResult:
        """Validate JSON data against schema using jsonschema library"""
        result = ValidationResult(True)

        try:
            # Use Draft7Validator for comprehensive validation
            validator = Draft7Validator(schema)

            # Collect all validation errors
            validation_errors = list(validator.iter_errors(data))

            for error in validation_errors:
                error_path = " -> ".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
                error_msg = f"At '{error_path}': {error.message}"
                result.add_error(error_msg)

            # Additional custom validations using external libraries
            self._perform_custom_validations(data, result)

        except Exception as e:
            result.add_error(f"Schema validation failed: {str(e)}")

        return result

    def _perform_custom_validations(self, data: Any, result: ValidationResult):
        """Perform custom validations using external libraries"""
        self._validate_emails_in_data(data, result)
        self._validate_urls_in_data(data, result)

    def _validate_emails_in_data(self, data: Any, result: ValidationResult, path: str = ""):
        """Recursively validate email addresses using email-validator"""
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                if "email" in key.lower() and isinstance(value, str):
                    try:
                        validate_email(value)
                    except EmailNotValidError as e:
                        result.add_error(f"Invalid email at '{current_path}': {str(e)}")
                else:
                    self._validate_emails_in_data(value, result, current_path)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path}[{i}]" if path else f"[{i}]"
                self._validate_emails_in_data(item, result, current_path)

    def _validate_urls_in_data(self, data: Any, result: ValidationResult, path: str = ""):
        """Recursively validate URLs using validators library"""
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                if "url" in key.lower() and isinstance(value, str):
                    if not validators.url(value):
                        result.add_error(f"Invalid URL at '{current_path}': {value}")
                else:
                    self._validate_urls_in_data(value, result, current_path)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path}[{i}]" if path else f"[{i}]"
                self._validate_urls_in_data(item, result, current_path)

    def load_json_file(self, file_path: Path) -> Any:
        """Load JSON from file with error handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise click.ClickException(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            raise click.ClickException(f"Invalid JSON in {file_path}: {str(e)}")
        except Exception as e:
            raise click.ClickException(f"Error reading {file_path}: {str(e)}")

    def parse_json_string(self, json_str: str) -> Any:
        """Parse JSON string with error handling"""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise click.ClickException(f"Invalid JSON string: {str(e)}")

    def display_result(self, result: ValidationResult, data_source: str = ""):
        """Display validation result based on output format"""
        if self.output_format == "json":
            output = result.to_dict()
            if data_source:
                output["source"] = data_source
            click.echo(json.dumps(output, indent=2))

        elif self.output_format == "quiet":
            # Only exit code matters in quiet mode
            sys.exit(0 if result.is_valid else 1)

        else:  # text format
            self._display_text_result(result, data_source)

    def _display_text_result(self, result: ValidationResult, data_source: str):
        """Display result in rich text format"""
        # Create title
        title = f"JSON Validation Result"
        if data_source:
            title += f" - {data_source}"

        # Status panel
        if result.is_valid:
            status_panel = Panel(
                "[bold green]✓ VALID[/bold green]",
                title=title,
                border_style="green"
            )
        else:
            status_panel = Panel(
                "[bold red]✗ INVALID[/bold red]",
                title=title,
                border_style="red"
            )

        self.console.print(status_panel)

        # Error details
        if result.errors:
            error_table = Table(title="Validation Errors", title_style="bold red")
            error_table.add_column("Error", style="red")

            for error in result.errors:
                error_table.add_row(error)

            self.console.print(error_table)

        # Warning details
        if result.warnings:
            warning_table = Table(title="Warnings", title_style="bold yellow")
            warning_table.add_column("Warning", style="yellow")

            for warning in result.warnings:
                warning_table.add_row(warning)

            self.console.print(warning_table)

        # Summary
        if not self.quiet:
            summary = f"Errors: {len(result.errors)}, Warnings: {len(result.warnings)}"
            self.console.print(f"\n[dim]{summary}[/dim]")


@click.command()
@click.argument('schema_file', type=click.Path(exists=True, path_type=Path))
@click.option('--data-file', '-f', type=click.Path(exists=True, path_type=Path),
              help='JSON data file to validate')
@click.option('--data-string', '-s', type=str,
              help='JSON data as string to validate')
@click.option('--stdin', is_flag=True,
              help='Read JSON data from stdin')
@click.option('--output-format', '-o',
              type=click.Choice(['text', 'json', 'quiet']),
              default='text',
              help='Output format')
@click.option('--quiet', '-q', is_flag=True,
              help='Quiet mode (no output, only exit code)')
@click.version_option(version='1.0.0', prog_name='JSON Schema Validator')
def main(schema_file: Path, data_file: Optional[Path], data_string: Optional[str],
         stdin: bool, output_format: str, quiet: bool):
    """
    JSON Schema Validator CLI Tool - External Library Variant

    Validates JSON data against JSON Schema specifications using professional
    external Python libraries for enhanced functionality.

    SCHEMA_FILE: Path to the JSON schema file

    Examples:
        json_validator.py schema.json --data-file data.json
        json_validator.py schema.json --data-string '{"name": "test"}'
        cat data.json | json_validator.py schema.json --stdin
        json_validator.py schema.json -f data.json -o json
    """
    # Determine quiet mode
    if output_format == 'quiet':
        quiet = True

    validator = JSONSchemaValidator(output_format, quiet)

    # Load schema
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=validator.console,
            disable=quiet
        ) as progress:
            task = progress.add_task("Loading schema...", total=None)
            schema = validator.load_json_file(schema_file)
            progress.remove_task(task)
    except Exception as e:
        if not quiet:
            console.print(f"[red]Error loading schema: {e}[/red]")
        sys.exit(1)

    # Determine data source and load data
    data_source = ""
    data = None

    if data_file:
        data_source = str(data_file)
        data = validator.load_json_file(data_file)
    elif data_string:
        data_source = "command line string"
        data = validator.parse_json_string(data_string)
    elif stdin:
        data_source = "stdin"
        try:
            stdin_content = sys.stdin.read()
            data = validator.parse_json_string(stdin_content)
        except Exception as e:
            if not quiet:
                console.print(f"[red]Error reading from stdin: {e}[/red]")
            sys.exit(1)
    else:
        if not quiet:
            console.print("[red]Error: Must specify data source (--data-file, --data-string, or --stdin)[/red]")
        sys.exit(1)

    # Perform validation
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=validator.console,
            disable=quiet
        ) as progress:
            task = progress.add_task("Validating data...", total=None)
            result = validator.validate_json_data(data, schema)
            progress.remove_task(task)
    except Exception as e:
        if not quiet:
            console.print(f"[red]Validation error: {e}[/red]")
        sys.exit(1)

    # Display results
    validator.display_result(result, data_source)

    # Exit with appropriate code
    sys.exit(0 if result.is_valid else 1)


if __name__ == '__main__':
    main()