#!/usr/bin/env python3
"""
JSON Schema Validator CLI Tool - TDD with External Libraries Approach

This implementation uses external libraries as the primary development approach,
with optional integration of discovered utility components for format validation.

Libraries used: click, rich, pydantic, jsonschema, tqdm, colorama
"""

import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime

# External libraries
import click
import jsonschema
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, ProgressColumn, TimeElapsedColumn
from rich.table import Table
from rich import print as rich_print
from tqdm import tqdm
import pydantic
from pydantic import BaseModel, EmailStr, AnyUrl, ValidationError as PydanticValidationError


# Try to discover and import utils validation components
try:
    sys.path.insert(0, '/home/ivan/projects/spawn-experiments')
    from utils.validation import validate_email, validate_date, validate_url
    UTILS_AVAILABLE = True
    print("Component Discovery: Utils validation components found and integrated")
except ImportError:
    UTILS_AVAILABLE = False
    print("Using external libraries for validation (utils not discovered)")


# Data structures for validation results
@dataclass
class ValidationResult:
    """Result of JSON schema validation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    schema_path: Optional[str] = None
    data_path: Optional[str] = None
    processing_time: Optional[float] = None


@dataclass
class ProcessingResult:
    """Result of processing a single file."""
    file_path: str
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    processing_time: Optional[float] = None


@dataclass
class BatchResult:
    """Result of batch processing multiple files."""
    total_files: int
    valid_files: int
    invalid_files: int
    error_files: int
    results: List[ProcessingResult] = field(default_factory=list)


# Custom exception for validation errors
class ValidationError(Exception):
    """Custom validation error."""
    pass


# JSON Schema Validator Core
class JSONSchemaValidator:
    """Core JSON Schema validator using jsonschema library."""

    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
        self.validator = jsonschema.Draft7Validator(schema)
        self.format_checker = jsonschema.FormatChecker()

        # Register custom format validators
        self._register_format_validators()

    def _register_format_validators(self):
        """Register format validators (email, date, uri)."""

        @self.format_checker.checks('email')
        def check_email(instance):
            if UTILS_AVAILABLE:
                # Use discovered utils component
                return validate_email(instance)
            else:
                # Fallback to pydantic
                try:
                    class EmailModel(BaseModel):
                        email: EmailStr
                    EmailModel(email=instance)
                    return True
                except PydanticValidationError:
                    return False

        @self.format_checker.checks('date')
        def check_date(instance):
            if UTILS_AVAILABLE:
                # Use discovered utils component
                return validate_date(instance)
            else:
                # Fallback to datetime parsing
                try:
                    datetime.strptime(instance, '%Y-%m-%d')
                    return True
                except ValueError:
                    return False

        @self.format_checker.checks('uri')
        def check_uri(instance):
            if UTILS_AVAILABLE:
                # Use discovered utils component
                return validate_url(instance)
            else:
                # Fallback to pydantic
                try:
                    class URLModel(BaseModel):
                        url: AnyUrl
                    URLModel(url=instance)
                    return True
                except PydanticValidationError:
                    return False

    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate JSON data against schema."""
        start_time = time.time()

        try:
            # Use format checker for format validation
            validator = jsonschema.Draft7Validator(
                self.schema,
                format_checker=self.format_checker
            )

            errors = list(validator.iter_errors(data))

            if errors:
                error_messages = [error.message for error in errors]
                return ValidationResult(
                    is_valid=False,
                    errors=error_messages,
                    processing_time=time.time() - start_time
                )
            else:
                return ValidationResult(
                    is_valid=True,
                    errors=[],
                    processing_time=time.time() - start_time
                )

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                processing_time=time.time() - start_time
            )


# Format validators for standalone use
class FormatValidator:
    """Factory for format validators."""

    @staticmethod
    def create(format_type: str):
        """Create a format validator of the specified type."""
        if format_type == "email":
            return EmailValidator()
        elif format_type == "date":
            return DateValidator()
        elif format_type == "uri":
            return URIValidator()
        else:
            raise ValueError(f"Unknown format type: {format_type}")


class EmailValidator:
    """Email format validator."""

    def validate(self, email: str) -> ValidationResult:
        """Validate email format."""
        if UTILS_AVAILABLE:
            is_valid = validate_email(email)
        else:
            try:
                class EmailModel(BaseModel):
                    email: EmailStr
                EmailModel(email=email)
                is_valid = True
            except PydanticValidationError:
                is_valid = False

        return ValidationResult(
            is_valid=is_valid,
            errors=[] if is_valid else [f"Invalid email format: {email}"]
        )


class DateValidator:
    """Date format validator."""

    def validate(self, date_str: str) -> ValidationResult:
        """Validate date format."""
        if UTILS_AVAILABLE:
            is_valid = validate_date(date_str)
        else:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                is_valid = True
            except ValueError:
                is_valid = False

        return ValidationResult(
            is_valid=is_valid,
            errors=[] if is_valid else [f"Invalid date format: {date_str}"]
        )


class URIValidator:
    """URI format validator."""

    def validate(self, uri: str) -> ValidationResult:
        """Validate URI format."""
        if UTILS_AVAILABLE:
            is_valid = validate_url(uri)
        else:
            try:
                class URLModel(BaseModel):
                    url: AnyUrl
                URLModel(url=uri)
                is_valid = True
            except PydanticValidationError:
                is_valid = False

        return ValidationResult(
            is_valid=is_valid,
            errors=[] if is_valid else [f"Invalid URI format: {uri}"]
        )


# Standalone validation functions
def validate_email_format(email: str) -> ValidationResult:
    """Validate email format."""
    validator = EmailValidator()
    return validator.validate(email)


def validate_date_format(date_str: str) -> ValidationResult:
    """Validate date format."""
    validator = DateValidator()
    return validator.validate(date_str)


def validate_uri_format(uri: str) -> ValidationResult:
    """Validate URI format."""
    validator = URIValidator()
    return validator.validate(uri)


def validate_json_against_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
    """Validate JSON data against schema."""
    validator = JSONSchemaValidator(schema)
    return validator.validate(data)


# File operations
def load_schema(schema_path: str) -> Dict[str, Any]:
    """Load JSON schema from file."""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValidationError(f"Schema file not found: {schema_path}")
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON in schema file: {e}")


def load_json_data(data_source: str, from_string: bool = False) -> Dict[str, Any]:
    """Load JSON data from file or string."""
    try:
        if from_string:
            return json.loads(data_source)
        else:
            with open(data_source, 'r') as f:
                return json.load(f)
    except FileNotFoundError:
        raise ValidationError(f"Data file not found: {data_source}")
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON in data file: {e}")


def validate_file(data_file: str, schema_file: str) -> ProcessingResult:
    """Validate a single JSON file against schema."""
    start_time = time.time()

    try:
        schema = load_schema(schema_file)
        data = load_json_data(data_file)

        validator = JSONSchemaValidator(schema)
        result = validator.validate(data)

        return ProcessingResult(
            file_path=data_file,
            is_valid=result.is_valid,
            errors=result.errors,
            processing_time=time.time() - start_time
        )

    except Exception as e:
        return ProcessingResult(
            file_path=data_file,
            is_valid=False,
            errors=[str(e)],
            processing_time=time.time() - start_time
        )


# File discovery and batch processing
def find_json_files(directory: str, pattern: str = "*.json", recursive: bool = False) -> List[str]:
    """Find JSON files in directory."""
    path = Path(directory)

    if recursive:
        files = list(path.rglob(pattern))
    else:
        files = list(path.glob(pattern))

    return [str(f) for f in files if f.is_file()]


class FileProcessor:
    """File processing utilities."""

    def load_json(self, file_path: str) -> Dict[str, Any]:
        """Load JSON from file."""
        return load_json_data(file_path)


class BatchProcessor:
    """Batch processing for multiple files."""

    def __init__(self, schema: Dict[str, Any], progress_callback=None):
        self.schema = schema
        self.validator = JSONSchemaValidator(schema)
        self.progress_callback = progress_callback

    def process_directory(self, directory: str, pattern: str = "*.json",
                         recursive: bool = False, parallel: bool = False) -> BatchResult:
        """Process all JSON files in directory."""
        files = find_json_files(directory, pattern, recursive)

        # Filter out schema files
        schema_files = [f for f in files if 'schema' in Path(f).name.lower()]
        data_files = [f for f in files if f not in schema_files]

        return self._process_files(data_files)

    def _process_files(self, files: List[str]) -> BatchResult:
        """Process list of files."""
        results = []
        valid_count = 0
        invalid_count = 0
        error_count = 0

        for i, file_path in enumerate(files):
            if self.progress_callback:
                self.progress_callback(i + 1, len(files), file_path)

            try:
                data = load_json_data(file_path)
                validation_result = self.validator.validate(data)

                result = ProcessingResult(
                    file_path=file_path,
                    is_valid=validation_result.is_valid,
                    errors=validation_result.errors,
                    processing_time=validation_result.processing_time
                )

                if validation_result.is_valid:
                    valid_count += 1
                else:
                    invalid_count += 1

                results.append(result)

            except Exception as e:
                error_count += 1
                results.append(ProcessingResult(
                    file_path=file_path,
                    is_valid=False,
                    errors=[str(e)]
                ))

        return BatchResult(
            total_files=len(files),
            valid_files=valid_count,
            invalid_files=invalid_count,
            error_files=error_count,
            results=results
        )


def batch_validate_files(file_paths: List[str], schema_file: str) -> BatchResult:
    """Batch validate multiple files."""
    schema = load_schema(schema_file)
    processor = BatchProcessor(schema)
    return processor._process_files(file_paths)


def process_directory(directory: str, schema_file: str,
                     pattern: str = "*.json", recursive: bool = False) -> BatchResult:
    """Process directory of JSON files."""
    schema = load_schema(schema_file)
    processor = BatchProcessor(schema)
    return processor.process_directory(directory, pattern, recursive)


# Output formatting
class OutputFormatter:
    """Base output formatter."""

    @staticmethod
    def create(format_type: str):
        """Create output formatter of specified type."""
        if format_type == "json":
            return JSONFormatter()
        elif format_type == "table":
            return TableFormatter()
        elif format_type == "text":
            return TextFormatter()
        else:
            raise ValueError(f"Unknown format type: {format_type}")

    def format(self, data: Any, **kwargs) -> str:
        """Format data for output."""
        raise NotImplementedError


class JSONFormatter(OutputFormatter):
    """JSON output formatter."""

    def format(self, data: Any, **kwargs) -> str:
        """Format data as JSON."""
        if isinstance(data, (ValidationResult, ProcessingResult, BatchResult)):
            # Convert dataclass to dict
            if hasattr(data, '__dict__'):
                data = data.__dict__

        return json.dumps(data, indent=2, default=str)


class TableFormatter(OutputFormatter):
    """Table output formatter using Rich."""

    def format(self, data: Any, **kwargs) -> str:
        """Format data as table."""
        console = Console(file=sys.stdout, width=120)

        if isinstance(data, list):
            # Batch results
            table = Table(title="Validation Results")
            table.add_column("File", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Errors", style="red")

            for item in data:
                status = " Valid" if item.get('valid', False) else " Invalid"
                errors = ", ".join(item.get('errors', []))[:50]
                table.add_row(
                    str(item.get('file', 'unknown')),
                    status,
                    errors
                )

            with console.capture() as capture:
                console.print(table)
            return capture.get()

        else:
            # Single result
            file_name = getattr(data, 'file_path', getattr(data, 'file', 'unknown'))
            is_valid = getattr(data, 'is_valid', getattr(data, 'valid', False))
            errors = getattr(data, 'errors', [])

            table = Table(title="Validation Result")
            table.add_column("Property", style="bold")
            table.add_column("Value")

            table.add_row("File", str(file_name))
            table.add_row("Status", " Valid" if is_valid else " Invalid")
            if errors:
                table.add_row("Errors", "\n".join(errors))

            with console.capture() as capture:
                console.print(table)
            return capture.get()


class TextFormatter(OutputFormatter):
    """Plain text output formatter."""

    def format(self, data: Any, verbose: bool = False, **kwargs) -> str:
        """Format data as plain text."""
        if isinstance(data, dict):
            file_name = data.get('file', 'unknown')
            is_valid = data.get('valid', False)
            errors = data.get('errors', [])

            if is_valid:
                result = f"{file_name}: VALID"
            else:
                result = f"{file_name}: INVALID"
                if errors:
                    result += f"\n  Errors: {', '.join(errors)}"

            return result

        # Handle dataclass objects
        file_name = getattr(data, 'file_path', getattr(data, 'file', 'unknown'))
        is_valid = getattr(data, 'is_valid', getattr(data, 'valid', False))
        errors = getattr(data, 'errors', [])

        if is_valid:
            result = f"{file_name}: VALID"
        else:
            result = f"{file_name}: INVALID"
            if errors:
                result += f"\n  Errors: {', '.join(errors)}"

        return result


# Colored output using Rich
class ColoredOutput:
    """Colored console output using Rich."""

    def __init__(self, enabled: bool = True):
        self.console = Console(force_terminal=enabled)
        self.enabled = enabled

    def success(self, message: str) -> str:
        """Format success message."""
        if self.enabled:
            with self.console.capture() as capture:
                self.console.print(message, style="green")
            return capture.get().strip()
        return message

    def error(self, message: str) -> str:
        """Format error message."""
        if self.enabled:
            with self.console.capture() as capture:
                self.console.print(message, style="red")
            return capture.get().strip()
        return message

    def warning(self, message: str) -> str:
        """Format warning message."""
        if self.enabled:
            with self.console.capture() as capture:
                self.console.print(message, style="yellow")
            return capture.get().strip()
        return message

    def info(self, message: str) -> str:
        """Format info message."""
        if self.enabled:
            with self.console.capture() as capture:
                self.console.print(message, style="blue")
            return capture.get().strip()
        return message


# Progress indicators
class ProgressIndicator:
    """Progress indicator using Rich or tqdm."""

    def __init__(self, total: int, use_rich: bool = True, callback=None):
        self.total = total
        self.current = 0
        self.use_rich = use_rich
        self.callback = callback

        if use_rich:
            self.progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                ProgressColumn(),
                TimeElapsedColumn(),
                console=Console()
            )
            self.task = None
        else:
            self.progress_bar = tqdm(total=total)

    def update(self, current: int, message: str = ""):
        """Update progress."""
        self.current = current

        if self.callback:
            self.callback(current, self.total, message)

        if self.use_rich:
            if self.task is None:
                self.task = self.progress.add_task(message, total=self.total)
            else:
                self.progress.update(self.task, completed=current, description=message)
        else:
            self.progress_bar.update(current - self.progress_bar.n)
            self.progress_bar.set_description(message)

    def is_complete(self) -> bool:
        """Check if progress is complete."""
        return self.current >= self.total

    def close(self):
        """Close progress indicator."""
        if not self.use_rich and hasattr(self, 'progress_bar'):
            self.progress_bar.close()


def create_progress_bar(total: int, use_rich: bool = True) -> ProgressIndicator:
    """Create a progress bar."""
    return ProgressIndicator(total, use_rich)


# Formatting helper functions
def format_validation_result(result: Union[ValidationResult, ProcessingResult, Dict],
                           format_type: str = "text", **kwargs) -> str:
    """Format validation result."""
    formatter = OutputFormatter.create(format_type)
    return formatter.format(result, **kwargs)


def format_batch_results(batch_result: Union[BatchResult, Dict],
                        format_type: str = "table") -> str:
    """Format batch processing results."""
    formatter = OutputFormatter.create(format_type)

    if isinstance(batch_result, BatchResult):
        # Convert to list format for table display
        results_list = []
        for result in batch_result.results:
            results_list.append({
                'file': result.file_path,
                'valid': result.is_valid,
                'errors': result.errors
            })
        return formatter.format(results_list)
    else:
        return formatter.format(batch_result)


# CLI Implementation using Click
@click.command()
@click.option('--file', '-f', help='JSON file to validate')
@click.option('--schema', '-s', required=True, help='JSON schema file')
@click.option('--batch', '-b', help='Directory for batch processing')
@click.option('--pattern', '-p', default='*.json', help='File pattern for batch processing')
@click.option('--recursive', '-r', is_flag=True, help='Recursive directory processing')
@click.option('--output', '-o', type=click.Choice(['json', 'table', 'text']),
              default='text', help='Output format')
@click.option('--stdin', is_flag=True, help='Read JSON from stdin')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--progress', is_flag=True, help='Show progress bar for batch operations')
@click.option('--no-color', is_flag=True, help='Disable colored output')
def cli(file, schema, batch, pattern, recursive, output, stdin, verbose, progress, no_color):
    """JSON Schema Validator CLI Tool - TDD with External Libraries Implementation."""

    console = Console(force_terminal=not no_color)
    colored = ColoredOutput(enabled=not no_color)

    try:
        # Load schema
        schema_data = load_schema(schema)

        if stdin:
            # Read from stdin
            json_input = sys.stdin.read()
            data = load_json_data(json_input, from_string=True)

            validator = JSONSchemaValidator(schema_data)
            result = validator.validate(data)

            output_result = {
                'file': '<stdin>',
                'valid': result.is_valid,
                'errors': result.errors
            }

            if result.is_valid:
                console.print(colored.success(format_validation_result(output_result, output)))
                sys.exit(0)
            else:
                console.print(colored.error(format_validation_result(output_result, output)))
                sys.exit(1)

        elif file:
            # Single file validation
            result = validate_file(file, schema)

            output_result = {
                'file': result.file_path,
                'valid': result.is_valid,
                'errors': result.errors
            }

            if verbose:
                output_result['processing_time'] = result.processing_time

            formatted = format_validation_result(output_result, output)

            if result.is_valid:
                console.print(colored.success(formatted))
                sys.exit(0)
            else:
                console.print(colored.error(formatted))
                sys.exit(1)

        elif batch:
            # Batch processing
            processor = BatchProcessor(schema_data)

            if progress:
                def progress_callback(current, total, filename):
                    console.print(f"Processing {current}/{total}: {Path(filename).name}")

                processor.progress_callback = progress_callback

            batch_result = processor.process_directory(batch, pattern, recursive)

            # Format output
            formatted = format_batch_results(batch_result, output)
            console.print(formatted)

            # Summary
            console.print(f"\nSummary:")
            console.print(f"  Total files: {batch_result.total_files}")
            console.print(colored.success(f"  Valid: {batch_result.valid_files}"))
            console.print(colored.error(f"  Invalid: {batch_result.invalid_files}"))

            if batch_result.error_files > 0:
                console.print(colored.warning(f"  Errors: {batch_result.error_files}"))

            # Exit with appropriate code
            if batch_result.invalid_files > 0 or batch_result.error_files > 0:
                sys.exit(1)
            else:
                sys.exit(0)

        else:
            console.print(colored.error("Error: Must specify --file, --batch, or --stdin"))
            sys.exit(1)

    except Exception as e:
        console.print(colored.error(f"Error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    cli()