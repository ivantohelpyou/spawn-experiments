"""
CLI command implementations.
Handles validate, batch, and check commands with proper error handling.
"""

import sys
import json
import glob
import os
from typing import List, Dict, Any, Optional
from ..core.validator import validate_json_file, validate_json_data
from ..core.schema_checker import check_schema_file, check_schema_data
from .output import get_formatter
from .progress import create_progress_bar, colored


class CommandRunner:
    """Handles execution of CLI commands."""

    def __init__(self, quiet: bool = False, format_name: str = "text", use_colors: bool = True):
        self.quiet = quiet
        self.format_name = format_name
        self.use_colors = use_colors
        self.formatter = get_formatter(format_name, use_colors)

        # Disable colors if in quiet mode or not using text format
        if quiet or format_name != "text":
            self.use_colors = False
            colored.use_colors = False

    def validate_single_file(self, data_file: str, schema_file: str) -> int:
        """
        Validate a single JSON file against a schema.

        Args:
            data_file: Path to JSON data file (or '-' for stdin)
            schema_file: Path to JSON schema file

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        try:
            # Load schema
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema = json.load(f)
        except Exception as e:
            if not self.quiet:
                colored.print_error(f"Error loading schema: {e}")
            return 1

        # Validate data
        if data_file == '-':
            # Read from stdin
            try:
                data = sys.stdin.read()
                is_valid, errors = validate_json_data(data, schema)
                file_path = "<stdin>"
            except Exception as e:
                if not self.quiet:
                    colored.print_error(f"Error reading from stdin: {e}")
                return 1
        else:
            is_valid, errors = validate_json_file(data_file, schema)
            file_path = data_file

        # Output results
        if not self.quiet:
            result = self.formatter.format_validation_result(file_path, is_valid, errors)
            print(result)

        return 0 if is_valid else 1

    def validate_batch_files(self, data_files: List[str], schema_file: str,
                           show_progress: bool = False) -> int:
        """
        Validate multiple JSON files against a schema.

        Args:
            data_files: List of JSON data file paths
            schema_file: Path to JSON schema file
            show_progress: Whether to show progress bar

        Returns:
            Exit code (0 for all valid, 1 for any failures)
        """
        try:
            # Load schema
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema = json.load(f)
        except Exception as e:
            if not self.quiet:
                colored.print_error(f"Error loading schema: {e}")
            return 1

        # Expand glob patterns
        expanded_files = []
        for pattern in data_files:
            matches = glob.glob(pattern)
            if matches:
                expanded_files.extend(matches)
            else:
                expanded_files.append(pattern)  # Keep as-is if no matches

        if not expanded_files:
            if not self.quiet:
                colored.print_error("No files found to validate")
            return 1

        # Filter to existing files
        existing_files = [f for f in expanded_files if os.path.isfile(f)]
        if len(existing_files) != len(expanded_files):
            missing = set(expanded_files) - set(existing_files)
            if not self.quiet:
                for f in missing:
                    colored.print_warning(f"File not found: {f}")

        if not existing_files:
            if not self.quiet:
                colored.print_error("No valid files found to validate")
            return 1

        # Initialize progress bar
        progress = None
        if show_progress and not self.quiet and self.use_colors:
            progress = create_progress_bar(len(existing_files))

        # Validate files
        results = []
        all_valid = True

        for i, file_path in enumerate(existing_files):
            is_valid, errors = validate_json_file(file_path, schema)

            results.append({
                'file': file_path,
                'valid': is_valid,
                'errors': errors
            })

            if not is_valid:
                all_valid = False

            if progress:
                progress.update()

        if progress:
            progress.finish()

        # Output results
        if not self.quiet:
            if len(results) == 1:
                # Single file result
                result = results[0]
                output = self.formatter.format_validation_result(
                    result['file'], result['valid'], result['errors']
                )
            else:
                # Batch results
                output = self.formatter.format_batch_results(results)

            print(output)

        return 0 if all_valid else 1

    def check_schema_file(self, schema_file: str) -> int:
        """
        Check if a JSON Schema file is valid.

        Args:
            schema_file: Path to JSON schema file

        Returns:
            Exit code (0 for valid, 1 for invalid)
        """
        is_valid, errors = check_schema_file(schema_file)

        if not self.quiet:
            if is_valid:
                colored.print_success(f"✓ {schema_file}: Valid JSON Schema")
            else:
                colored.print_error(f"✗ {schema_file}: Invalid JSON Schema")
                for error in errors:
                    colored.print_error(f"  - {error}")

        return 0 if is_valid else 1

    def check_schema_stdin(self) -> int:
        """
        Check if JSON Schema from stdin is valid.

        Returns:
            Exit code (0 for valid, 1 for invalid)
        """
        try:
            schema_data = sys.stdin.read()
            is_valid, errors = check_schema_data(schema_data)
        except Exception as e:
            if not self.quiet:
                colored.print_error(f"Error reading schema from stdin: {e}")
            return 1

        if not self.quiet:
            if is_valid:
                colored.print_success("✓ <stdin>: Valid JSON Schema")
            else:
                colored.print_error("✗ <stdin>: Invalid JSON Schema")
                for error in errors:
                    colored.print_error(f"  - {error}")

        return 0 if is_valid else 1


def validate_command(data_file: str, schema_file: str, quiet: bool = False,
                    format_name: str = "text", no_color: bool = False) -> int:
    """
    Execute validate command.

    Args:
        data_file: Path to JSON data file (or '-' for stdin)
        schema_file: Path to JSON schema file
        quiet: Suppress output, only return exit code
        format_name: Output format (text, json, csv)
        no_color: Disable colored output

    Returns:
        Exit code
    """
    runner = CommandRunner(quiet=quiet, format_name=format_name, use_colors=not no_color)
    return runner.validate_single_file(data_file, schema_file)


def batch_command(data_files: List[str], schema_file: str, quiet: bool = False,
                 format_name: str = "text", no_color: bool = False,
                 progress: bool = False) -> int:
    """
    Execute batch validation command.

    Args:
        data_files: List of JSON data file paths/patterns
        schema_file: Path to JSON schema file
        quiet: Suppress output, only return exit code
        format_name: Output format (text, json, csv)
        no_color: Disable colored output
        progress: Show progress bar

    Returns:
        Exit code
    """
    runner = CommandRunner(quiet=quiet, format_name=format_name, use_colors=not no_color)
    return runner.validate_batch_files(data_files, schema_file, show_progress=progress)


def check_command(schema_file: str = None, quiet: bool = False, no_color: bool = False) -> int:
    """
    Execute schema check command.

    Args:
        schema_file: Path to schema file (None for stdin)
        quiet: Suppress output, only return exit code
        no_color: Disable colored output

    Returns:
        Exit code
    """
    runner = CommandRunner(quiet=quiet, format_name="text", use_colors=not no_color)

    if schema_file is None or schema_file == '-':
        return runner.check_schema_stdin()
    else:
        return runner.check_schema_file(schema_file)