"""Output formatting utilities for CLI."""

import json
import csv
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional, TextIO
from datetime import datetime
import sys

from ..models.result import ValidationResult


class OutputFormatter:
    """
    Formats validation results for various output formats.

    Supports multiple output formats including JSON, CSV, XML, and human-readable text.
    """

    def __init__(self, format_type: str = "text", verbose: bool = False):
        """
        Initialize output formatter.

        Args:
            format_type: Output format (text, json, csv, xml)
            verbose: Whether to include verbose information
        """
        self.format_type = format_type.lower()
        self.verbose = verbose

    def format_results(self, results: List[ValidationResult]) -> str:
        """
        Format validation results.

        Args:
            results: List of validation results

        Returns:
            Formatted output string
        """
        if self.format_type == "json":
            return self._format_json(results)
        elif self.format_type == "csv":
            return self._format_csv(results)
        elif self.format_type == "xml":
            return self._format_xml(results)
        elif self.format_type == "text":
            return self._format_text(results)
        else:
            raise ValueError(f"Unsupported output format: {self.format_type}")

    def format_single_result(self, result: ValidationResult) -> str:
        """
        Format a single validation result.

        Args:
            result: Validation result

        Returns:
            Formatted output string
        """
        return self.format_results([result])

    def _format_json(self, results: List[ValidationResult]) -> str:
        """Format results as JSON."""
        if len(results) == 1:
            data = results[0].to_dict()
        else:
            data = {
                "validation_results": [result.to_dict() for result in results],
                "summary": self._generate_summary(results)
            }

        return json.dumps(data, indent=2, default=str)

    def _format_csv(self, results: List[ValidationResult]) -> str:
        """Format results as CSV."""
        import io

        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        if self.verbose:
            header = [
                "url", "is_valid", "is_accessible", "status_code", "response_time",
                "error_count", "warning_count", "error_codes", "final_url", "duration"
            ]
        else:
            header = ["url", "is_valid", "is_accessible", "status_code", "error_codes"]

        writer.writerow(header)

        # Write data
        for result in results:
            if self.verbose:
                row = [
                    result.url,
                    result.is_valid,
                    result.is_accessible,
                    result.accessibility_result.status_code if result.accessibility_result else "",
                    result.accessibility_result.response_time if result.accessibility_result else "",
                    len(result.errors),
                    len(result.warnings),
                    ";".join(result.error_codes),
                    result.accessibility_result.final_url if result.accessibility_result else "",
                    result.duration
                ]
            else:
                row = [
                    result.url,
                    result.is_valid,
                    result.is_accessible,
                    result.accessibility_result.status_code if result.accessibility_result else "",
                    ";".join(result.error_codes)
                ]
            writer.writerow(row)

        return output.getvalue()

    def _format_xml(self, results: List[ValidationResult]) -> str:
        """Format results as XML."""
        root = ET.Element("validation_results")

        # Add summary
        summary_elem = ET.SubElement(root, "summary")
        summary = self._generate_summary(results)
        for key, value in summary.items():
            elem = ET.SubElement(summary_elem, key)
            elem.text = str(value)

        # Add results
        results_elem = ET.SubElement(root, "results")
        for result in results:
            result_elem = ET.SubElement(results_elem, "result")

            # Basic info
            url_elem = ET.SubElement(result_elem, "url")
            url_elem.text = result.url

            valid_elem = ET.SubElement(result_elem, "is_valid")
            valid_elem.text = str(result.is_valid)

            accessible_elem = ET.SubElement(result_elem, "is_accessible")
            accessible_elem.text = str(result.is_accessible)

            # Errors
            if result.errors:
                errors_elem = ET.SubElement(result_elem, "errors")
                for error in result.errors:
                    error_elem = ET.SubElement(errors_elem, "error")
                    error_elem.set("code", error.code)
                    error_elem.set("category", error.category.value)
                    error_elem.text = error.message

            # Accessibility info
            if result.accessibility_result and self.verbose:
                access_elem = ET.SubElement(result_elem, "accessibility")
                if result.accessibility_result.status_code:
                    status_elem = ET.SubElement(access_elem, "status_code")
                    status_elem.text = str(result.accessibility_result.status_code)
                if result.accessibility_result.response_time:
                    time_elem = ET.SubElement(access_elem, "response_time")
                    time_elem.text = str(result.accessibility_result.response_time)

        return ET.tostring(root, encoding='unicode')

    def _format_text(self, results: List[ValidationResult]) -> str:
        """Format results as human-readable text."""
        lines = []

        if len(results) > 1:
            # Summary for multiple results
            summary = self._generate_summary(results)
            lines.append("VALIDATION SUMMARY")
            lines.append("=" * 50)
            lines.append(f"Total URLs: {summary['total_urls']}")
            lines.append(f"Valid URLs: {summary['valid_urls']}")
            lines.append(f"Accessible URLs: {summary['accessible_urls']}")
            lines.append(f"Success Rate: {summary['success_rate']:.1f}%")
            lines.append("")

        # Individual results
        for i, result in enumerate(results):
            if len(results) > 1:
                lines.append(f"[{i+1}] {result.url}")
            else:
                lines.append(f"URL: {result.url}")

            # Status
            status_parts = []
            if result.is_valid:
                status_parts.append("✓ VALID FORMAT")
            else:
                status_parts.append("✗ INVALID FORMAT")

            if result.is_valid:
                if result.is_accessible:
                    status_parts.append("✓ ACCESSIBLE")
                else:
                    status_parts.append("✗ INACCESSIBLE")

            lines.append(f"Status: {' | '.join(status_parts)}")

            # Response details
            if result.accessibility_result and self.verbose:
                acc = result.accessibility_result
                if acc.status_code:
                    lines.append(f"HTTP Status: {acc.status_code}")
                if acc.response_time:
                    lines.append(f"Response Time: {acc.response_time:.3f}s")
                if acc.final_url and acc.final_url != result.url:
                    lines.append(f"Final URL: {acc.final_url}")
                if acc.redirect_count > 0:
                    lines.append(f"Redirects: {acc.redirect_count}")

            # Errors
            if result.errors:
                lines.append("Errors:")
                for error in result.errors:
                    lines.append(f"  - [{error.code}] {error.message}")

            # Warnings
            if result.warnings and self.verbose:
                lines.append("Warnings:")
                for warning in result.warnings:
                    lines.append(f"  - {warning}")

            # Performance
            if self.verbose:
                lines.append(f"Validation Time: {result.duration:.3f}s")

            lines.append("")

        return "\n".join(lines)

    def _generate_summary(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Generate summary statistics."""
        total = len(results)
        valid = sum(1 for r in results if r.is_valid)
        accessible = sum(1 for r in results if r.is_accessible)

        return {
            "total_urls": total,
            "valid_urls": valid,
            "accessible_urls": accessible,
            "invalid_urls": total - valid,
            "inaccessible_urls": valid - accessible,
            "success_rate": (accessible / total * 100) if total > 0 else 0,
            "validation_time": datetime.now().isoformat()
        }

    def write_results(self, results: List[ValidationResult], file: Optional[TextIO] = None) -> None:
        """
        Write formatted results to file or stdout.

        Args:
            results: Validation results
            file: Output file (default: stdout)
        """
        output = self.format_results(results)
        if file:
            file.write(output)
        else:
            print(output)

    def format_error(self, error: Exception) -> str:
        """
        Format an error message.

        Args:
            error: Error to format

        Returns:
            Formatted error message
        """
        if self.format_type == "json":
            return json.dumps({
                "error": str(error),
                "type": type(error).__name__
            }, indent=2)
        else:
            return f"ERROR: {error}"

    def format_progress(self, current: int, total: int, url: str = "") -> str:
        """
        Format progress information.

        Args:
            current: Current item number
            total: Total items
            url: Current URL being processed

        Returns:
            Formatted progress string
        """
        percentage = (current / total * 100) if total > 0 else 0
        if self.verbose and url:
            return f"[{current}/{total}] ({percentage:.1f}%) {url}"
        else:
            return f"[{current}/{total}] ({percentage:.1f}%)"