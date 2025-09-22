#!/usr/bin/env python3
"""
JSON Schema Validator CLI Tool - Immediate Implementation with External Libraries
Experiment 2.505.1 Method 1E

A fast, feature-rich JSON Schema validation tool built with external libraries
for maximum development speed.
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import email_validator
from urllib.parse import urlparse

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
import jsonschema
from jsonschema import Draft7Validator, FormatChecker
from jsonschema.exceptions import ValidationError, SchemaError
from tabulate import tabulate
from tqdm import tqdm

# Initialize rich console
console = Console()

# Custom format checkers for enhanced validation
def is_valid_email(instance: str) -> bool:
    """Validate email format using email-validator library"""
    try:
        email_validator.validate_email(instance, check_deliverability=False)
        return True
    except email_validator.EmailNotValidError:
        return False

def is_valid_date(instance: str) -> bool:
    """Validate date format (ISO 8601)"""
    try:
        datetime.fromisoformat(instance.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

def is_valid_uri(instance: str) -> bool:
    """Validate URI format"""
    try:
        result = urlparse(instance)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

# Enhanced format checker
format_checker = FormatChecker()
format_checker.checks('email')(is_valid_email)
format_checker.checks('date')(is_valid_date)
format_checker.checks('uri')(is_valid_uri)
format_checker.checks('url')(is_valid_uri)

class ValidationResult:
    """Container for validation results"""
    def __init__(self, file_path: str, is_valid: bool, errors: List[str] = None,
                 schema_path: Optional[str] = None):
        self.file_path = file_path
        self.is_valid = is_valid
        self.errors = errors or []
        self.schema_path = schema_path
        self.timestamp = datetime.now()

class JSONSchemaValidator:
    """Main validator class with comprehensive functionality"""

    def __init__(self, output_format: str = 'text', quiet: bool = False):
        self.output_format = output_format
        self.quiet = quiet
        self.results: List[ValidationResult] = []

    def load_json_file(self, file_path: Path) -> Tuple[Optional[Dict], Optional[str]]:
        """Load and parse JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f), None
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON: {e}"
        except Exception as e:
            return None, f"Error reading file: {e}"

    def validate_single_file(self, data_file: Path, schema_file: Path) -> ValidationResult:
        """Validate a single JSON file against a schema"""
        # Load data file
        data, error = self.load_json_file(data_file)
        if error:
            return ValidationResult(str(data_file), False, [error], str(schema_file))

        # Load schema file
        schema, error = self.load_json_file(schema_file)
        if error:
            return ValidationResult(str(data_file), False, [f"Schema error: {error}"], str(schema_file))

        # Validate
        try:
            validator = Draft7Validator(schema, format_checker=format_checker)
            errors = []
            for validation_error in validator.iter_errors(data):
                error_path = ' -> '.join(str(p) for p in validation_error.absolute_path)
                error_msg = f"{error_path}: {validation_error.message}" if error_path else validation_error.message
                errors.append(error_msg)

            is_valid = len(errors) == 0
            return ValidationResult(str(data_file), is_valid, errors, str(schema_file))

        except SchemaError as e:
            return ValidationResult(str(data_file), False, [f"Invalid schema: {e}"], str(schema_file))
        except Exception as e:
            return ValidationResult(str(data_file), False, [f"Validation error: {e}"], str(schema_file))

    def validate_from_stdin(self, schema_file: Path) -> ValidationResult:
        """Validate JSON from stdin"""
        try:
            stdin_data = sys.stdin.read()
            data = json.loads(stdin_data)
        except json.JSONDecodeError as e:
            return ValidationResult("<stdin>", False, [f"Invalid JSON from stdin: {e}"])
        except Exception as e:
            return ValidationResult("<stdin>", False, [f"Error reading stdin: {e}"])

        # Load schema
        schema, error = self.load_json_file(schema_file)
        if error:
            return ValidationResult("<stdin>", False, [f"Schema error: {error}"], str(schema_file))

        # Validate
        try:
            validator = Draft7Validator(schema, format_checker=format_checker)
            errors = []
            for validation_error in validator.iter_errors(data):
                error_path = ' -> '.join(str(p) for p in validation_error.absolute_path)
                error_msg = f"{error_path}: {validation_error.message}" if error_path else validation_error.message
                errors.append(error_msg)

            is_valid = len(errors) == 0
            return ValidationResult("<stdin>", is_valid, errors, str(schema_file))

        except SchemaError as e:
            return ValidationResult("<stdin>", False, [f"Invalid schema: {e}"], str(schema_file))
        except Exception as e:
            return ValidationResult("<stdin>", False, [f"Validation error: {e}"], str(schema_file))

    def batch_validate(self, data_files: List[Path], schema_file: Path,
                      show_progress: bool = True) -> List[ValidationResult]:
        """Validate multiple files with progress indication"""
        results = []

        if show_progress and not self.quiet:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console
            ) as progress:
                task = progress.add_task("Validating files...", total=len(data_files))

                for data_file in data_files:
                    result = self.validate_single_file(data_file, schema_file)
                    results.append(result)
                    progress.update(task, advance=1, description=f"Validating {data_file.name}")
        else:
            for data_file in data_files:
                result = self.validate_single_file(data_file, schema_file)
                results.append(result)

        return results

    def output_results(self, results: List[ValidationResult]):
        """Output results in specified format"""
        self.results = results

        if self.output_format == 'json':
            self._output_json()
        elif self.output_format == 'csv':
            self._output_csv()
        elif self.output_format == 'table':
            self._output_table()
        else:  # text format
            self._output_text()

    def _output_text(self):
        """Output in human-readable text format"""
        if self.quiet:
            # Just print file paths and status
            for result in self.results:
                status = "VALID" if result.is_valid else "INVALID"
                print(f"{result.file_path}: {status}")
        else:
            valid_count = sum(1 for r in self.results if r.is_valid)
            total_count = len(self.results)

            # Summary panel
            summary_text = f"[green]{valid_count}[/green] valid, [red]{total_count - valid_count}[/red] invalid out of {total_count} files"
            console.print(Panel(summary_text, title="Validation Summary", expand=False))

            # Detailed results
            for result in self.results:
                if result.is_valid:
                    console.print(f"✅ [green]{result.file_path}[/green]: Valid")
                else:
                    console.print(f"❌ [red]{result.file_path}[/red]: Invalid")
                    for error in result.errors:
                        console.print(f"   • [yellow]{error}[/yellow]")
                    console.print()

    def _output_json(self):
        """Output in JSON format"""
        output = {
            "summary": {
                "total": len(self.results),
                "valid": sum(1 for r in self.results if r.is_valid),
                "invalid": sum(1 for r in self.results if not r.is_valid),
                "timestamp": datetime.now().isoformat()
            },
            "results": [
                {
                    "file": result.file_path,
                    "valid": result.is_valid,
                    "errors": result.errors,
                    "schema": result.schema_path,
                    "timestamp": result.timestamp.isoformat()
                }
                for result in self.results
            ]
        }
        print(json.dumps(output, indent=2))

    def _output_csv(self):
        """Output in CSV format"""
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['file', 'valid', 'errors', 'schema'])

        for result in self.results:
            writer.writerow([
                result.file_path,
                result.is_valid,
                '; '.join(result.errors),
                result.schema_path or ''
            ])

        print(output.getvalue().strip())

    def _output_table(self):
        """Output in table format using tabulate"""
        headers = ['File', 'Status', 'Errors']
        rows = []

        for result in self.results:
            status = "✅ Valid" if result.is_valid else "❌ Invalid"
            errors = '; '.join(result.errors) if result.errors else ""
            rows.append([result.file_path, status, errors])

        print(tabulate(rows, headers=headers, tablefmt='grid'))

@click.command()
@click.option('--schema', '-s', required=True, type=click.Path(exists=True, path_type=Path),
              help='JSON schema file to validate against')
@click.option('--file', '-f', 'files', multiple=True, type=click.Path(exists=True, path_type=Path),
              help='JSON file(s) to validate (can be used multiple times)')
@click.option('--directory', '-d', type=click.Path(exists=True, file_okay=False, path_type=Path),
              help='Directory containing JSON files to validate')
@click.option('--pattern', '-p', default='*.json',
              help='File pattern for directory validation (default: *.json)')
@click.option('--output-format', '-o', type=click.Choice(['text', 'json', 'csv', 'table']),
              default='text', help='Output format (default: text)')
@click.option('--quiet', '-q', is_flag=True, help='Quiet mode - minimal output')
@click.option('--no-progress', is_flag=True, help='Disable progress bar')
@click.option('--stdin', is_flag=True, help='Read JSON from stdin')
@click.version_option(version='1.0.0', prog_name='JSON Schema Validator')
def main(schema, files, directory, pattern, output_format, quiet, no_progress, stdin):
    """
    JSON Schema Validator CLI Tool

    Validates JSON files against JSON Schema with support for:
    - Single file and batch validation
    - Multiple output formats (text, json, csv, table)
    - Progress indicators and colored output
    - Pipeline operations (stdin/stdout)
    - Format validation (email, date, uri)

    Examples:
      json_schema_validator -s schema.json -f data.json
      json_schema_validator -s schema.json -d ./data/ -p "*.json"
      cat data.json | json_schema_validator -s schema.json --stdin
      json_schema_validator -s schema.json -f data.json -o json
    """

    validator = JSONSchemaValidator(output_format=output_format, quiet=quiet)

    try:
        # Handle stdin input
        if stdin:
            result = validator.validate_from_stdin(schema)
            validator.output_results([result])
            sys.exit(0 if result.is_valid else 1)

        # Collect files to validate
        data_files = []

        # Add individual files
        if files:
            data_files.extend(files)

        # Add files from directory
        if directory:
            data_files.extend(directory.glob(pattern))

        # Validate we have files to process
        if not data_files:
            if not quiet:
                console.print("[red]Error:[/red] No files specified. Use --file, --directory, or --stdin", err=True)
            sys.exit(1)

        # Remove duplicates and sort
        data_files = sorted(set(data_files))

        if not quiet:
            console.print(f"Validating {len(data_files)} file(s) against schema: {schema}")

        # Perform validation
        show_progress = not no_progress and len(data_files) > 1
        results = validator.batch_validate(data_files, schema, show_progress=show_progress)

        # Output results
        validator.output_results(results)

        # Exit with appropriate code
        invalid_count = sum(1 for r in results if not r.is_valid)
        sys.exit(0 if invalid_count == 0 else 1)

    except KeyboardInterrupt:
        if not quiet:
            console.print("\n[yellow]Validation interrupted by user[/yellow]", err=True)
        sys.exit(130)
    except Exception as e:
        if not quiet:
            console.print(f"[red]Error:[/red] {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()