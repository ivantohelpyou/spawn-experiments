"""JSON output formatter for JSON Schema Validator CLI."""

import json
from typing import List, Dict, Any
from ..validator import ValidationResult


class JSONFormatter:
    """Formats validation results as structured JSON."""

    def __init__(self, indent: int = 2):
        """Initialize JSON formatter.

        Args:
            indent: Number of spaces for JSON indentation
        """
        self.indent = indent

    def format_results(self, results: List[ValidationResult]) -> str:
        """Format validation results as JSON.

        Args:
            results: List of validation results

        Returns:
            JSON-formatted output
        """
        if not results:
            output = {
                "summary": {
                    "total": 0,
                    "valid": 0,
                    "invalid": 0,
                    "total_errors": 0
                },
                "results": []
            }
        else:
            # Calculate summary statistics
            total = len(results)
            valid = sum(1 for r in results if r.is_valid)
            invalid = total - valid
            total_errors = sum(r.error_count for r in results)
            total_time = sum(r.validation_time for r in results)

            summary = {
                "total": total,
                "valid": valid,
                "invalid": invalid,
                "total_errors": total_errors,
                "total_time": round(total_time, 3)
            }

            # Format individual results
            formatted_results = [self._format_single_result(result) for result in results]

            output = {
                "summary": summary,
                "results": formatted_results
            }

        return json.dumps(output, indent=self.indent, ensure_ascii=False)

    def _format_single_result(self, result: ValidationResult) -> Dict[str, Any]:
        """Format a single validation result.

        Args:
            result: Single validation result

        Returns:
            Dictionary representation of the result
        """
        formatted_errors = [self._format_error(error) for error in result.errors]

        result_dict = {
            "file": result.file_path,
            "valid": result.is_valid,
            "error_count": result.error_count,
            "validation_time": round(result.validation_time, 3),
            "schema": result.schema_path,
            "errors": formatted_errors
        }

        # Add file size if available
        if result.file_size is not None:
            result_dict["file_size"] = result.file_size

        return result_dict

    def _format_error(self, error) -> Dict[str, Any]:
        """Format a single validation error.

        Args:
            error: ValidationError instance

        Returns:
            Dictionary representation of the error
        """
        error_dict = {
            "path": error.path,
            "message": error.message,
            "type": error.error_type
        }

        # Add optional fields if available
        if error.line_number is not None:
            error_dict["line"] = error.line_number

        if error.schema_path:
            error_dict["schema_path"] = error.schema_path

        return error_dict

    def format_schema_check(self, check_result: dict) -> str:
        """Format schema check results as JSON.

        Args:
            check_result: Schema check result dictionary

        Returns:
            JSON-formatted schema check output
        """
        # The check_result is already a dictionary, we just need to format it as JSON
        return json.dumps(check_result, indent=self.indent, ensure_ascii=False)