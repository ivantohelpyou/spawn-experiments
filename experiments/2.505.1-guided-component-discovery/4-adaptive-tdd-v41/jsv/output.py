"""
Output formatting for different formats: text, JSON, CSV.
Supports colored output for better readability.
"""

import json
import csv
import io
from typing import List, Dict, Any, Union

try:
    import colorama
    from colorama import Fore, Style
    colorama.init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback color constants
    class Fore:
        RED = ''
        GREEN = ''
        YELLOW = ''
        CYAN = ''

    class Style:
        RESET_ALL = ''


class OutputFormatter:
    """
    Output formatter supporting multiple formats and optional colors.
    """

    def __init__(self, colored: bool = True):
        """
        Initialize output formatter.

        Args:
            colored: Whether to use colored output (if available)
        """
        self.colored = colored and COLORS_AVAILABLE

    def format_single_result(self, result: Dict[str, Any], format_type: str) -> str:
        """
        Format a single validation result.

        Args:
            result: Validation result dictionary
            format_type: Output format ('text', 'json', 'csv')

        Returns:
            str: Formatted output
        """
        if format_type == 'json':
            return self._format_json_single(result)
        elif format_type == 'csv':
            return self._format_csv_single(result)
        else:  # Default to text
            return self._format_text_single(result)

    def format_batch_results(self, results: List[Dict[str, Any]], format_type: str) -> str:
        """
        Format batch validation results.

        Args:
            results: List of validation results
            format_type: Output format ('text', 'json', 'csv')

        Returns:
            str: Formatted output
        """
        if format_type == 'json':
            return self._format_json_batch(results)
        elif format_type == 'csv':
            return self._format_csv_batch(results)
        else:  # Default to text
            return self._format_text_batch(results)

    def _format_text_single(self, result: Dict[str, Any]) -> str:
        """Format single result as text."""
        file_name = result.get('file', '<unknown>')
        is_valid = result.get('valid', False)
        errors = result.get('errors', [])

        if is_valid:
            status = self._colorize("✓ Valid", Fore.GREEN) if self.colored else "✓ Valid"
            return f"{file_name}: {status}"
        else:
            status = self._colorize("✗ Invalid", Fore.RED) if self.colored else "✗ Invalid"
            output = f"{file_name}: {status}"

            if errors:
                output += "\n" + self._format_errors(errors)

            return output

    def _format_text_batch(self, results: List[Dict[str, Any]]) -> str:
        """Format batch results as text."""
        output_lines = []
        valid_count = 0
        total_count = len(results)

        for result in results:
            output_lines.append(self._format_text_single(result))
            if result.get('valid', False):
                valid_count += 1

        # Add summary
        summary_color = Fore.GREEN if valid_count == total_count else Fore.YELLOW
        summary = f"\nSummary: {valid_count}/{total_count} files valid"
        if self.colored:
            summary = self._colorize(summary, summary_color)

        output_lines.append(summary)

        return "\n".join(output_lines)

    def _format_json_single(self, result: Dict[str, Any]) -> str:
        """Format single result as JSON."""
        # Convert ValidationError objects to strings
        json_result = dict(result)
        if 'errors' in json_result:
            json_result['errors'] = [str(error) for error in json_result['errors']]

        return json.dumps(json_result, indent=2)

    def _format_json_batch(self, results: List[Dict[str, Any]]) -> str:
        """Format batch results as JSON."""
        json_results = []
        for result in results:
            json_result = dict(result)
            if 'errors' in json_result:
                json_result['errors'] = [str(error) for error in json_result['errors']]
            json_results.append(json_result)

        return json.dumps(json_results, indent=2)

    def _format_csv_single(self, result: Dict[str, Any]) -> str:
        """Format single result as CSV."""
        return self._format_csv_batch([result])

    def _format_csv_batch(self, results: List[Dict[str, Any]]) -> str:
        """Format batch results as CSV."""
        output = io.StringIO()
        fieldnames = ['file', 'valid', 'error_count', 'errors']
        writer = csv.DictWriter(output, fieldnames=fieldnames)

        writer.writeheader()

        for result in results:
            errors = result.get('errors', [])
            row = {
                'file': result.get('file', ''),
                'valid': result.get('valid', False),
                'error_count': len(errors),
                'errors': '; '.join(str(error) for error in errors)
            }
            writer.writerow(row)

        return output.getvalue()

    def _format_errors(self, errors: List[Any]) -> str:
        """Format error list for text output."""
        if not errors:
            return ""

        error_lines = []
        for i, error in enumerate(errors, 1):
            error_text = f"  {i}. {str(error)}"
            if self.colored:
                error_text = self._colorize(error_text, Fore.RED)
            error_lines.append(error_text)

        return "\n".join(error_lines)

    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if self.colored and COLORS_AVAILABLE:
            return f"{color}{text}{Style.RESET_ALL}"
        return text