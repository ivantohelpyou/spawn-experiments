"""CSV output formatter for JSON Schema Validator CLI."""

import csv
import io
from typing import List
from ..validator import ValidationResult


class CSVFormatter:
    """Formats validation results as CSV."""

    def __init__(self, delimiter: str = ',', include_headers: bool = True):
        """Initialize CSV formatter.

        Args:
            delimiter: CSV field delimiter
            include_headers: Whether to include column headers
        """
        self.delimiter = delimiter
        self.include_headers = include_headers

    def format_results(self, results: List[ValidationResult]) -> str:
        """Format validation results as CSV.

        Args:
            results: List of validation results

        Returns:
            CSV-formatted output
        """
        if not results:
            if self.include_headers:
                return "file,valid,error_count,errors,validation_time,schema\n"
            else:
                return ""

        output = io.StringIO()
        writer = csv.writer(output, delimiter=self.delimiter, quoting=csv.QUOTE_MINIMAL)

        # Write headers if requested
        if self.include_headers:
            headers = ["file", "valid", "error_count", "errors", "validation_time", "schema"]
            writer.writerow(headers)

        # Write data rows
        for result in results:
            row = self._format_single_result(result)
            writer.writerow(row)

        return output.getvalue()

    def _format_single_result(self, result: ValidationResult) -> List[str]:
        """Format a single validation result as CSV row.

        Args:
            result: Single validation result

        Returns:
            List of strings representing CSV row fields
        """
        # Combine error messages into a single field
        error_messages = []
        for error in result.errors:
            if error.line_number:
                msg = f"Line {error.line_number}: {error.message}"
            else:
                msg = error.message
            error_messages.append(msg)

        errors_field = "; ".join(error_messages) if error_messages else ""

        return [
            result.file_path,
            str(result.is_valid).lower(),
            str(result.error_count),
            errors_field,
            f"{result.validation_time:.3f}",
            result.schema_path
        ]

    def format_schema_check(self, check_result: dict) -> str:
        """Format schema check results as CSV.

        Args:
            check_result: Schema check result dictionary

        Returns:
            CSV-formatted schema check output
        """
        output = io.StringIO()
        writer = csv.writer(output, delimiter=self.delimiter, quoting=csv.QUOTE_MINIMAL)

        # Write headers
        if self.include_headers:
            headers = ["file", "valid", "error_count", "warning_count", "errors", "warnings"]
            writer.writerow(headers)

        # Combine errors and warnings
        errors = [error['message'] for error in check_result.get('errors', [])]
        warnings = [warning['message'] for warning in check_result.get('warnings', [])]

        errors_field = "; ".join(errors) if errors else ""
        warnings_field = "; ".join(warnings) if warnings else ""

        row = [
            check_result['file_path'],
            str(check_result['is_valid']).lower(),
            str(len(check_result.get('errors', []))),
            str(len(check_result.get('warnings', []))),
            errors_field,
            warnings_field
        ]

        writer.writerow(row)
        return output.getvalue()