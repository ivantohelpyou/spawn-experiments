"""Text output formatter for JSON Schema Validator CLI."""

from typing import List, Optional
from ..validator import ValidationResult
from ..utils.color import ColorFormatter


class TextFormatter:
    """Formats validation results as human-readable text."""

    def __init__(self, use_color: Optional[bool] = None, show_summary: bool = True):
        """Initialize text formatter.

        Args:
            use_color: Whether to use colored output
            show_summary: Whether to show summary statistics
        """
        self.color = ColorFormatter(use_color)
        self.show_summary = show_summary

    def format_results(self, results: List[ValidationResult]) -> str:
        """Format validation results as text.

        Args:
            results: List of validation results

        Returns:
            Formatted text output
        """
        if not results:
            return "No files to validate."

        lines = []

        # Format individual results
        for result in results:
            lines.append(self._format_single_result(result))

        # Add summary if requested and multiple files
        if self.show_summary and len(results) > 1:
            lines.append("")
            lines.append(self._format_summary(results))

        return "\n".join(lines)

    def _format_single_result(self, result: ValidationResult) -> str:
        """Format a single validation result.

        Args:
            result: Single validation result

        Returns:
            Formatted text for the result
        """
        lines = []

        # Main status line
        if result.is_valid:
            status_line = f"{self.color.success('✓')} {result.file_path}: {self.color.success('Valid')}"
        else:
            status_line = f"{self.color.error('✗')} {result.file_path}: {self.color.error('Invalid')}"

        lines.append(status_line)

        # Error details
        if result.errors:
            for error in result.errors:
                error_line = self._format_error(error)
                lines.append(f"  {error_line}")

        return "\n".join(lines)

    def _format_error(self, error) -> str:
        """Format a single validation error.

        Args:
            error: ValidationError instance

        Returns:
            Formatted error text
        """
        # Build error message components
        parts = []

        # Add line number if available
        if error.line_number:
            parts.append(self.color.dim(f"Line {error.line_number}"))

        # Add JSON path if not root
        if error.path and error.path != "$":
            parts.append(self.color.dim(f"Path {error.path}"))

        # Add the error message
        parts.append(self.color.error(error.message))

        # Join with separator
        if parts[:-1]:  # If we have line/path info
            return f"{': '.join(parts[:-1])}: {parts[-1]}"
        else:
            return parts[-1]

    def _format_summary(self, results: List[ValidationResult]) -> str:
        """Format summary statistics.

        Args:
            results: List of validation results

        Returns:
            Formatted summary text
        """
        total = len(results)
        valid = sum(1 for r in results if r.is_valid)
        invalid = total - valid
        total_errors = sum(r.error_count for r in results)

        summary_parts = []

        # Basic counts
        if valid > 0:
            summary_parts.append(self.color.success(f"{valid} valid"))
        if invalid > 0:
            summary_parts.append(self.color.error(f"{invalid} invalid"))

        summary_line = f"Summary: {', '.join(summary_parts)}"

        # Add error count if any
        if total_errors > 0:
            summary_line += f" ({self.color.warning(f'{total_errors} total errors')})"

        # Add timing information if available
        total_time = sum(r.validation_time for r in results)
        if total_time > 0.01:  # Only show if meaningful
            summary_line += f" in {total_time:.2f}s"

        return summary_line

    def format_schema_check(self, check_result: dict) -> str:
        """Format schema check results.

        Args:
            check_result: Schema check result dictionary

        Returns:
            Formatted schema check output
        """
        lines = []

        # Main status
        file_path = check_result['file_path']
        if check_result['is_valid']:
            status_line = f"{self.color.success('✓')} {file_path}: {self.color.success('Valid Schema')}"
        else:
            status_line = f"{self.color.error('✗')} {file_path}: {self.color.error('Invalid Schema')}"

        lines.append(status_line)

        # Schema errors
        for error in check_result.get('errors', []):
            error_msg = error['message']
            error_text = f"  {self.color.error(f'Error: {error_msg}')}"
            lines.append(error_text)

        # Schema warnings
        for warning in check_result.get('warnings', []):
            warning_msg = warning['message']
            warning_text = f"  {self.color.warning(f'Warning: {warning_msg}')}"
            lines.append(warning_text)

        # Schema information (if valid and detailed output requested)
        if check_result['is_valid'] and self.show_summary:
            lines.append("")
            lines.append(self._format_schema_info(check_result['schema_info']))

        return "\n".join(lines)

    def _format_schema_info(self, schema_info: dict) -> str:
        """Format schema information.

        Args:
            schema_info: Schema analysis information

        Returns:
            Formatted schema info text
        """
        lines = [self.color.bold("Schema Information:")]

        # Basic info
        if schema_info.get('title') != 'not specified':
            lines.append(f"  Title: {schema_info['title']}")

        if schema_info.get('description') != 'not specified':
            lines.append(f"  Description: {schema_info['description']}")

        lines.append(f"  Type: {schema_info.get('type', 'not specified')}")

        # Property counts
        if schema_info.get('has_properties'):
            prop_count = schema_info.get('property_count', 0)
            req_count = schema_info.get('required_count', 0)
            lines.append(f"  Properties: {prop_count} total, {req_count} required")

        # Validation rules
        rule_count = schema_info.get('validation_rule_count', 0)
        if rule_count > 0:
            rules = schema_info.get('validation_rules', [])
            lines.append(f"  Validation rules: {', '.join(rules)}")

        return "\n".join(lines)