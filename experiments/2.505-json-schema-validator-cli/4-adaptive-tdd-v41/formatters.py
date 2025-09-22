#!/usr/bin/env python3
"""
Output formatters for JSON Schema Validator CLI tool.
"""

import json
import csv
import sys
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from io import StringIO

from validator import ValidationResult


class OutputFormatter(ABC):
    """Abstract base class for output formatters."""

    @abstractmethod
    def format_single_result(self, result: ValidationResult) -> str:
        """Format a single validation result."""
        pass

    @abstractmethod
    def format_batch_results(self, results: List[ValidationResult]) -> str:
        """Format multiple validation results."""
        pass


class TextFormatter(OutputFormatter):
    """Human-readable text output formatter."""

    def __init__(self, use_colors: bool = True):
        """
        Initialize the text formatter.

        Args:
            use_colors: Whether to use colored output
        """
        self.use_colors = use_colors and sys.stdout.isatty()

    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if not self.use_colors:
            return text

        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'reset': '\033[0m'
        }

        return f"{colors.get(color, '')}{text}{colors.get('reset', '')}"

    def format_single_result(self, result: ValidationResult) -> str:
        """Format a single validation result."""
        if result.is_valid:
            status = self._colorize("✓ VALID", "green")
            if result.file_path:
                return f"{status}: {result.file_path}"
            else:
                return f"{status}: JSON data is valid"
        else:
            status = self._colorize("✗ INVALID", "red")
            output = []
            if result.file_path:
                output.append(f"{status}: {result.file_path}")
            else:
                output.append(f"{status}: JSON data is invalid")

            for error in result.errors:
                output.append(f"  {self._colorize('Error:', 'red')} {error}")

            return "\n".join(output)

    def format_batch_results(self, results: List[ValidationResult]) -> str:
        """Format multiple validation results."""
        output = []
        valid_count = sum(1 for r in results if r.is_valid)
        total_count = len(results)

        # Summary header
        summary = f"Validation Summary: {valid_count}/{total_count} files valid"
        if valid_count == total_count:
            summary = self._colorize(summary, "green")
        elif valid_count == 0:
            summary = self._colorize(summary, "red")
        else:
            summary = self._colorize(summary, "yellow")

        output.append(summary)
        output.append("=" * 50)

        # Individual results
        for result in results:
            output.append(self.format_single_result(result))
            output.append("")

        return "\n".join(output)


class JSONFormatter(OutputFormatter):
    """JSON output formatter for programmatic use."""

    def format_single_result(self, result: ValidationResult) -> str:
        """Format a single validation result as JSON."""
        data = {
            "valid": result.is_valid,
            "errors": result.errors
        }
        if result.file_path:
            data["file"] = result.file_path

        return json.dumps(data, indent=2)

    def format_batch_results(self, results: List[ValidationResult]) -> str:
        """Format multiple validation results as JSON."""
        data = {
            "summary": {
                "total_files": len(results),
                "valid_files": sum(1 for r in results if r.is_valid),
                "invalid_files": sum(1 for r in results if not r.is_valid)
            },
            "results": []
        }

        for result in results:
            result_data = {
                "valid": result.is_valid,
                "errors": result.errors
            }
            if result.file_path:
                result_data["file"] = result.file_path
            data["results"].append(result_data)

        return json.dumps(data, indent=2)


class CSVFormatter(OutputFormatter):
    """CSV output formatter for batch validation results."""

    def format_single_result(self, result: ValidationResult) -> str:
        """Format a single validation result as CSV."""
        output = StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(["file", "valid", "error_count", "errors"])

        # Data
        errors_str = "; ".join(result.errors) if result.errors else ""
        writer.writerow([
            result.file_path or "stdin",
            result.is_valid,
            len(result.errors),
            errors_str
        ])

        return output.getvalue().strip()

    def format_batch_results(self, results: List[ValidationResult]) -> str:
        """Format multiple validation results as CSV."""
        output = StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(["file", "valid", "error_count", "errors"])

        # Data rows
        for result in results:
            errors_str = "; ".join(result.errors) if result.errors else ""
            writer.writerow([
                result.file_path or "stdin",
                result.is_valid,
                len(result.errors),
                errors_str
            ])

        return output.getvalue().strip()


class QuietFormatter(OutputFormatter):
    """Quiet formatter that produces no output (only exit codes)."""

    def format_single_result(self, result: ValidationResult) -> str:
        """Format a single validation result (empty for quiet mode)."""
        return ""

    def format_batch_results(self, results: List[ValidationResult]) -> str:
        """Format multiple validation results (empty for quiet mode)."""
        return ""


def get_formatter(format_type: str, use_colors: bool = True) -> OutputFormatter:
    """
    Get an output formatter instance.

    Args:
        format_type: The type of formatter ('text', 'json', 'csv', 'quiet')
        use_colors: Whether to use colored output (only applies to text formatter)

    Returns:
        An OutputFormatter instance

    Raises:
        ValueError: If format_type is not supported
    """
    formatters = {
        'text': TextFormatter(use_colors),
        'json': JSONFormatter(),
        'csv': CSVFormatter(),
        'quiet': QuietFormatter()
    }

    if format_type not in formatters:
        raise ValueError(f"Unsupported format type: {format_type}")

    return formatters[format_type]