"""
Batch validation functionality with progress indicators.
Supports large-scale validation operations with user feedback.
"""

import sys
import time
import json
from typing import List, Dict, Any, Optional, Callable

from .validator import JSONSchemaValidator


class ProgressIndicator:
    """
    Progress indicator for batch operations.
    Shows completion percentage and current status.
    """

    def __init__(self, total: int, enabled: bool = True):
        """
        Initialize progress indicator.

        Args:
            total: Total number of items to process
            enabled: Whether to show progress output
        """
        self.total = total
        self.current = 0
        self.enabled = enabled
        self.start_time = time.time()

    def update(self, increment: int = 1):
        """
        Update progress by increment.

        Args:
            increment: Number of items completed
        """
        self.current += increment

    def percentage(self) -> float:
        """Get current completion percentage."""
        if self.total == 0:
            return 100.0
        return (self.current / self.total) * 100.0

    def display(self):
        """Display current progress."""
        if not self.enabled:
            return

        percentage = self.percentage()
        elapsed = time.time() - self.start_time

        # Create progress bar
        bar_width = 30
        filled = int(bar_width * self.current / self.total) if self.total > 0 else 0
        bar = '█' * filled + '░' * (bar_width - filled)

        # Estimate time remaining
        if self.current > 0 and elapsed > 0:
            rate = self.current / elapsed
            remaining = (self.total - self.current) / rate if rate > 0 else 0
            eta = f" ETA: {remaining:.1f}s" if remaining > 0 else ""
        else:
            eta = ""

        progress_line = f"\rProgress: |{bar}| {self.current}/{self.total} ({percentage:.1f}%){eta}"

        # Write progress line
        sys.stdout.write(progress_line)
        sys.stdout.flush()

        # Newline when complete
        if self.current >= self.total:
            sys.stdout.write("\n")


class BatchValidator:
    """
    Batch validation orchestrator with progress reporting.
    """

    def __init__(self):
        pass

    def validate_batch(
        self,
        files: List[str],
        schema_file: str,
        show_progress: bool = True,
        progress_callback: Optional[Callable[[int, int, Dict[str, Any]], None]] = None
    ) -> List[Dict[str, Any]]:
        """
        Validate multiple files with progress tracking.

        Args:
            files: List of file paths to validate
            schema_file: Path to JSON schema file
            show_progress: Whether to show progress indicator
            progress_callback: Optional callback for progress updates

        Returns:
            list: List of validation results
        """
        if not files:
            return []

        results = []
        progress = ProgressIndicator(total=len(files), enabled=show_progress)

        if show_progress:
            print(f"Validating {len(files)} files against {schema_file}")

        for i, file_path in enumerate(files):
            # Validate single file
            result = self._validate_single_file(file_path, schema_file)
            results.append(result)

            # Update progress
            progress.update(1)
            if show_progress:
                progress.display()

            # Call progress callback if provided
            if progress_callback:
                progress_callback(i + 1, len(files), result)

        if show_progress:
            # Show summary
            summary = self.get_summary_statistics(results)
            print(f"\nValidation complete: {summary['valid']}/{summary['total']} files valid "
                  f"({summary['success_rate']:.1%} success rate)")

        return results

    def _validate_single_file(self, data_file: str, schema_file: str) -> Dict[str, Any]:
        """
        Validate a single JSON file against schema.

        Args:
            data_file: Path to JSON data file
            schema_file: Path to JSON schema file

        Returns:
            dict: Validation result with file info
        """
        try:
            # Load schema
            with open(schema_file, 'r') as f:
                schema = json.load(f)

            # Load data
            with open(data_file, 'r') as f:
                data = json.load(f)

            # Validate
            validator = JSONSchemaValidator(schema)
            result = validator.validate_with_errors(data)
            result['file'] = data_file

            return result

        except FileNotFoundError as e:
            return {
                'valid': False,
                'file': data_file,
                'errors': [f"File not found: {e}"]
            }
        except json.JSONDecodeError as e:
            return {
                'valid': False,
                'file': data_file,
                'errors': [f"JSON decode error: {e}"]
            }
        except Exception as e:
            return {
                'valid': False,
                'file': data_file,
                'errors': [f"Unexpected error: {e}"]
            }

    def get_summary_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate summary statistics for batch results.

        Args:
            results: List of validation results

        Returns:
            dict: Summary statistics
        """
        total = len(results)
        valid = sum(1 for r in results if r.get('valid', False))
        invalid = total - valid

        return {
            'total': total,
            'valid': valid,
            'invalid': invalid,
            'success_rate': valid / total if total > 0 else 0.0
        }

    def validate_with_parallel_processing(
        self,
        files: List[str],
        schema_file: str,
        max_workers: int = 4,
        show_progress: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Validate files using parallel processing for better performance.

        Args:
            files: List of file paths to validate
            schema_file: Path to JSON schema file
            max_workers: Maximum number of worker threads
            show_progress: Whether to show progress indicator

        Returns:
            list: List of validation results
        """
        # Note: This is a placeholder for potential parallel implementation
        # For now, fall back to sequential processing
        return self.validate_batch(files, schema_file, show_progress)

    def filter_results(
        self,
        results: List[Dict[str, Any]],
        filter_type: str = 'all'
    ) -> List[Dict[str, Any]]:
        """
        Filter validation results based on criteria.

        Args:
            results: List of validation results
            filter_type: Filter criteria ('all', 'valid', 'invalid', 'errors')

        Returns:
            list: Filtered results
        """
        if filter_type == 'valid':
            return [r for r in results if r.get('valid', False)]
        elif filter_type == 'invalid':
            return [r for r in results if not r.get('valid', False)]
        elif filter_type == 'errors':
            return [r for r in results if r.get('errors') and len(r['errors']) > 0]
        else:  # 'all'
            return results

    def generate_batch_report(
        self,
        results: List[Dict[str, Any]],
        include_details: bool = True
    ) -> str:
        """
        Generate a detailed batch validation report.

        Args:
            results: List of validation results
            include_details: Whether to include detailed error information

        Returns:
            str: Formatted report
        """
        summary = self.get_summary_statistics(results)
        report_lines = []

        # Header
        report_lines.append("=" * 60)
        report_lines.append("BATCH VALIDATION REPORT")
        report_lines.append("=" * 60)

        # Summary
        report_lines.append(f"Total files processed: {summary['total']}")
        report_lines.append(f"Valid files: {summary['valid']}")
        report_lines.append(f"Invalid files: {summary['invalid']}")
        report_lines.append(f"Success rate: {summary['success_rate']:.1%}")
        report_lines.append("")

        if include_details:
            # Invalid files details
            invalid_results = self.filter_results(results, 'invalid')
            if invalid_results:
                report_lines.append("FAILED VALIDATIONS:")
                report_lines.append("-" * 30)
                for result in invalid_results:
                    file_name = result.get('file', '<unknown>')
                    errors = result.get('errors', [])
                    report_lines.append(f"File: {file_name}")
                    for i, error in enumerate(errors, 1):
                        report_lines.append(f"  {i}. {error}")
                    report_lines.append("")

        return "\n".join(report_lines)