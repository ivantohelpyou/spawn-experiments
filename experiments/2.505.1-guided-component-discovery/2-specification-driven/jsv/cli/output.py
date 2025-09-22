"""
Output formatters for validation results.
Supports text, JSON, and CSV output formats with optional colors.
"""

import json
import csv
import io
from typing import List, Dict, Any
from ..core.validator import ValidationError


class OutputFormatter:
    """Base class for output formatters."""

    def format_validation_result(self, file_path: str, is_valid: bool, errors: List[ValidationError]) -> str:
        """Format a single validation result."""
        raise NotImplementedError

    def format_batch_results(self, results: List[Dict[str, Any]]) -> str:
        """Format multiple validation results."""
        raise NotImplementedError


class TextFormatter(OutputFormatter):
    """Human-readable text output formatter with optional colors."""

    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors

    def _colorize(self, text: str, color: str) -> str:
        """Add color codes if colors are enabled."""
        if not self.use_colors:
            return text

        colors = {
            'green': '\033[92m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'cyan': '\033[96m',
            'reset': '\033[0m'
        }

        return f"{colors.get(color, '')}{text}{colors.get('reset', '')}"

    def format_validation_result(self, file_path: str, is_valid: bool, errors: List[ValidationError]) -> str:
        """Format a single validation result as text."""
        if is_valid:
            symbol = self._colorize("✓", "green")
            status = self._colorize("Valid", "green")
            return f"{symbol} {file_path}: {status}"
        else:
            symbol = self._colorize("✗", "red")
            error_count = len(errors)
            status = self._colorize(f"{error_count} error{'s' if error_count != 1 else ''}", "red")
            result = f"{symbol} {file_path}: {status}"

            # Add error details
            for error in errors:
                error_line = f"  - {str(error)}"
                result += f"\n{self._colorize(error_line, 'red')}"

            return result

    def format_batch_results(self, results: List[Dict[str, Any]]) -> str:
        """Format multiple validation results as text."""
        output_lines = []
        valid_count = sum(1 for r in results if r['valid'])
        total_count = len(results)

        # Summary header
        if valid_count == total_count:
            summary = self._colorize(f"All {total_count} files are valid", "green")
        else:
            invalid_count = total_count - valid_count
            summary = self._colorize(f"{invalid_count} of {total_count} files have errors", "red")

        output_lines.append(summary)
        output_lines.append("")

        # Individual results
        for result in results:
            formatted = self.format_validation_result(result['file'], result['valid'], result['errors'])
            output_lines.append(formatted)

        return "\n".join(output_lines)


class JSONFormatter(OutputFormatter):
    """JSON output formatter for programmatic use."""

    def format_validation_result(self, file_path: str, is_valid: bool, errors: List[ValidationError]) -> str:
        """Format a single validation result as JSON."""
        result = {
            "file": file_path,
            "valid": is_valid,
            "errors": [
                {
                    "path": error.path,
                    "message": error.message,
                    "line": error.line
                }
                for error in errors
            ]
        }
        return json.dumps(result, indent=2)

    def format_batch_results(self, results: List[Dict[str, Any]]) -> str:
        """Format multiple validation results as JSON."""
        output = {
            "valid": all(r['valid'] for r in results),
            "total_files": len(results),
            "valid_files": sum(1 for r in results if r['valid']),
            "files": []
        }

        for result in results:
            file_result = {
                "file": result['file'],
                "valid": result['valid'],
                "errors": [
                    {
                        "path": error.path,
                        "message": error.message,
                        "line": error.line
                    }
                    for error in result['errors']
                ]
            }
            output["files"].append(file_result)

        return json.dumps(output, indent=2)


class CSVFormatter(OutputFormatter):
    """CSV output formatter for tabular data."""

    def format_validation_result(self, file_path: str, is_valid: bool, errors: List[ValidationError]) -> str:
        """Format a single validation result as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(["file", "valid", "error_count", "errors"])

        # Data
        error_messages = "; ".join(str(error) for error in errors)
        writer.writerow([file_path, is_valid, len(errors), error_messages])

        return output.getvalue().strip()

    def format_batch_results(self, results: List[Dict[str, Any]]) -> str:
        """Format multiple validation results as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(["file", "valid", "error_count", "errors"])

        # Data rows
        for result in results:
            error_messages = "; ".join(str(error) for error in result['errors'])
            writer.writerow([
                result['file'],
                result['valid'],
                len(result['errors']),
                error_messages
            ])

        return output.getvalue().strip()


def get_formatter(format_name: str, use_colors: bool = True) -> OutputFormatter:
    """
    Get output formatter by name.

    Args:
        format_name: Format type ('text', 'json', 'csv')
        use_colors: Whether to use colors for text output

    Returns:
        Appropriate formatter instance
    """
    formatters = {
        'text': lambda: TextFormatter(use_colors),
        'json': lambda: JSONFormatter(),
        'csv': lambda: CSVFormatter()
    }

    if format_name not in formatters:
        raise ValueError(f"Unknown format: {format_name}. Supported: {', '.join(formatters.keys())}")

    return formatters[format_name]()