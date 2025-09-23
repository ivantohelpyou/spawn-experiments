#!/usr/bin/env python3
"""
JSON Schema Validator CLI Tool - V4.1 Adaptive TDD with External Libraries

A comprehensive command-line tool for validating JSON data against JSON schemas.
Built using external libraries for maximum efficiency and reliability.
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Iterator, Union

import click
import jsonschema
from jsonschema import ValidationError, SchemaError
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from email_validator import validate_email, EmailNotValidError
from dateutil.parser import parse as parse_date
from dateutil.parser import ParserError


# Global console for rich output
console = Console()


class FormatValidator:
    """Enhanced format validation using external libraries."""

    @staticmethod
    def validate_email(value: str) -> bool:
        """Validate email format using email-validator library."""
        try:
            validate_email(value, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False

    @staticmethod
    def validate_date(value: str) -> bool:
        """Validate date format using dateutil."""
        try:
            parse_date(value)
            return True
        except (ParserError, ValueError, TypeError):
            return False

    @staticmethod
    def validate_uri(value: str) -> bool:
        """Validate URI format using regex pattern."""
        uri_pattern = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(uri_pattern.match(value))


class JSONSchemaValidator:
    """Core JSON schema validation engine leveraging jsonschema library."""

    def __init__(self):
        self.format_validator = FormatValidator()
        self._setup_format_checker()

    def _setup_format_checker(self):
        """Set up custom format checker with enhanced validation."""
        self.format_checker = jsonschema.FormatChecker()

        # Add custom format validators
        @self.format_checker.checks('email')
        def check_email(instance):
            return self.format_validator.validate_email(instance)

        @self.format_checker.checks('date')
        def check_date(instance):
            return self.format_validator.validate_date(instance)

        @self.format_checker.checks('uri')
        def check_uri(instance):
            return self.format_validator.validate_uri(instance)

    def load_schema(self, schema_path: Path) -> Dict[str, Any]:
        """Load and validate JSON schema file."""
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)

            # Validate schema itself
            jsonschema.Draft7Validator.check_schema(schema)
            return schema

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in schema file: {e}")
        except SchemaError as e:
            raise ValueError(f"Invalid JSON schema: {e}")
        except FileNotFoundError:
            raise ValueError(f"Schema file not found: {schema_path}")

    def load_data(self, data_source: Union[Path, str]) -> Any:
        """Load JSON data from file or stdin."""
        if isinstance(data_source, Path):
            try:
                with open(data_source, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in data file: {e}")
            except FileNotFoundError:
                raise ValueError(f"Data file not found: {data_source}")
        else:
            # Data from stdin
            try:
                return json.loads(data_source)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON from stdin: {e}")

    def validate(self, data: Any, schema: Dict[str, Any]) -> List[ValidationError]:
        """Validate data against schema, returning list of errors."""
        validator = jsonschema.Draft7Validator(
            schema,
            format_checker=self.format_checker
        )
        return list(validator.iter_errors(data))

    def validate_file(self, data_path: Path, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single file and return results."""
        try:
            data = self.load_data(data_path)
            errors = self.validate(data, schema)

            return {
                'file': str(data_path),
                'valid': len(errors) == 0,
                'errors': [self._format_error(error) for error in errors]
            }
        except Exception as e:
            return {
                'file': str(data_path),
                'valid': False,
                'errors': [{'message': str(e), 'path': '', 'value': None}]
            }

    def validate_batch(self, data_paths: List[Path], schema: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
        """Validate multiple files with progress tracking."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:

            task = progress.add_task("Validating files...", total=len(data_paths))

            for data_path in data_paths:
                result = self.validate_file(data_path, schema)
                yield result
                progress.advance(task)

    def _format_error(self, error: ValidationError) -> Dict[str, Any]:
        """Format validation error for output."""
        return {
            'message': error.message,
            'path': '.'.join(str(p) for p in error.absolute_path),
            'value': error.instance
        }


class OutputFormatter:
    """Handle different output formats with rich styling."""

    def __init__(self, format_type: str = 'detailed'):
        self.format_type = format_type
        self.console = console

    def format_results(self, results: List[Dict[str, Any]]) -> None:
        """Format and display validation results."""
        if self.format_type == 'json':
            self._format_json(results)
        elif self.format_type == 'table':
            self._format_table(results)
        elif self.format_type == 'summary':
            self._format_summary(results)
        else:  # detailed
            self._format_detailed(results)

    def _format_json(self, results: List[Dict[str, Any]]) -> None:
        """Output results as JSON."""
        print(json.dumps(results, indent=2))

    def _format_table(self, results: List[Dict[str, Any]]) -> None:
        """Output results as a table."""
        table = Table(title="Validation Results")
        table.add_column("File", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("Errors", style="red")

        for result in results:
            status = "[green]✓ Valid[/green]" if result['valid'] else "[red]✗ Invalid[/red]"
            error_count = str(len(result['errors']))
            table.add_row(result['file'], status, error_count)

        self.console.print(table)

    def _format_summary(self, results: List[Dict[str, Any]]) -> None:
        """Output summary statistics."""
        total = len(results)
        valid = sum(1 for r in results if r['valid'])
        invalid = total - valid

        self.console.print(Panel(
            f"[bold]Validation Summary[/bold]\n\n"
            f"Total files: {total}\n"
            f"[green]Valid: {valid}[/green]\n"
            f"[red]Invalid: {invalid}[/red]",
            title="Results"
        ))

    def _format_detailed(self, results: List[Dict[str, Any]]) -> None:
        """Output detailed results with errors."""
        for result in results:
            if result['valid']:
                self.console.print(f"[green]✓[/green] {result['file']}")
            else:
                self.console.print(f"[red]✗[/red] {result['file']}")
                for error in result['errors']:
                    path_str = f" at {error['path']}" if error['path'] else ""
                    self.console.print(f"    [red]Error{path_str}:[/red] {error['message']}")


@click.command()
@click.option('--schema', '-s', type=click.Path(exists=True, path_type=Path),
              required=True, help='JSON schema file to validate against')
@click.option('--data', '-d', type=click.Path(exists=True, path_type=Path),
              multiple=True, help='JSON data file(s) to validate')
@click.option('--directory', type=click.Path(exists=True, file_okay=False, path_type=Path),
              help='Directory containing JSON files to validate')
@click.option('--pattern', default='*.json',
              help='File pattern for directory mode (default: *.json)')
@click.option('--format', 'output_format', type=click.Choice(['detailed', 'json', 'table', 'summary']),
              default='detailed', help='Output format')
@click.option('--stdin', is_flag=True, help='Read JSON data from stdin')
@click.option('--exit-code', is_flag=True,
              help='Set exit code based on validation results')
def main(schema: Path, data: tuple, directory: Optional[Path], pattern: str,
         output_format: str, stdin: bool, exit_code: bool):
    """
    JSON Schema Validator CLI Tool

    Validate JSON data against JSON schemas with comprehensive format checking.
    Supports single files, batch processing, and stdin/stdout operations.
    """

    validator = JSONSchemaValidator()
    formatter = OutputFormatter(output_format)

    try:
        # Load schema
        schema_data = validator.load_schema(schema)

        # Determine data sources
        data_sources = []

        if stdin:
            # Read from stdin
            stdin_data = sys.stdin.read().strip()
            if not stdin_data:
                console.print("[red]Error:[/red] No data provided via stdin", err=True)
                sys.exit(1)

            try:
                data_obj = validator.load_data(stdin_data)
                errors = validator.validate(data_obj, schema_data)
                results = [{
                    'file': '<stdin>',
                    'valid': len(errors) == 0,
                    'errors': [validator._format_error(error) for error in errors]
                }]

                formatter.format_results(results)

                if exit_code and not results[0]['valid']:
                    sys.exit(1)

            except Exception as e:
                console.print(f"[red]Error:[/red] {e}", err=True)
                sys.exit(1)

        elif directory:
            # Batch process directory
            data_sources = list(directory.glob(pattern))
            if not data_sources:
                console.print(f"[yellow]Warning:[/yellow] No files matching '{pattern}' found in {directory}")
                sys.exit(0)

        else:
            # Process specified files
            data_sources = list(data)
            if not data_sources:
                console.print("[red]Error:[/red] No data files specified. Use --data, --directory, or --stdin", err=True)
                sys.exit(1)

        # Process files if any
        if data_sources:
            results = list(validator.validate_batch(data_sources, schema_data))
            formatter.format_results(results)

            # Set exit code based on validation results
            if exit_code:
                invalid_count = sum(1 for r in results if not r['valid'])
                if invalid_count > 0:
                    sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()