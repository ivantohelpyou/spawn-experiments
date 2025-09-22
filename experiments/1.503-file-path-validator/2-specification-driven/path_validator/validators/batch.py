"""
Batch path validation with performance optimizations.
"""

import concurrent.futures
import multiprocessing
from typing import List, Union, Optional, Iterator, Callable, Dict, Any
from pathlib import Path
import time

from ..core.validator import ValidationCore, ValidationResult
from ..utils.config import ValidationConfig
from ..exceptions.errors import PathValidationError


class BatchValidationResult:
    """Result container for batch validation operations."""

    def __init__(self, results: List[ValidationResult]):
        self.results = results
        self._analyze_results()

    def _analyze_results(self):
        """Analyze results and compute summary statistics."""
        self.total_count = len(self.results)
        self.valid_count = sum(1 for r in self.results if r.valid)
        self.invalid_count = self.total_count - self.valid_count
        self.error_counts = {}
        self.warning_counts = {}

        # Count error types
        for result in self.results:
            if result.error:
                error_type = result.error.__class__.__name__
                self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1

            # Count warnings
            for warning in result.warnings:
                self.warning_counts[warning] = self.warning_counts.get(warning, 0) + 1

    @property
    def success_rate(self) -> float:
        """Get the success rate as a percentage."""
        return (self.valid_count / self.total_count * 100) if self.total_count > 0 else 0.0

    def get_valid_results(self) -> List[ValidationResult]:
        """Get only the valid results."""
        return [r for r in self.results if r.valid]

    def get_invalid_results(self) -> List[ValidationResult]:
        """Get only the invalid results."""
        return [r for r in self.results if not r.valid]

    def get_errors_by_type(self, error_type: str) -> List[ValidationResult]:
        """Get results with specific error type."""
        return [r for r in self.results
                if r.error and r.error.__class__.__name__ == error_type]

    def to_summary(self) -> Dict[str, Any]:
        """Get summary statistics as dictionary."""
        return {
            'total_count': self.total_count,
            'valid_count': self.valid_count,
            'invalid_count': self.invalid_count,
            'success_rate': self.success_rate,
            'error_counts': self.error_counts,
            'warning_counts': self.warning_counts,
            'validation_times': [r.validation_time for r in self.results if r.validation_time],
            'avg_validation_time': sum(r.validation_time for r in self.results if r.validation_time) / len(self.results) if self.results else 0
        }


class BatchPathValidator:
    """High-performance batch path validator."""

    def __init__(self, config: Optional[ValidationConfig] = None, max_workers: Optional[int] = None):
        """
        Initialize batch validator.

        Args:
            config: Validation configuration
            max_workers: Maximum number of worker threads/processes
        """
        self.config = config or ValidationConfig()
        self.max_workers = max_workers or min(32, (multiprocessing.cpu_count() or 1) + 4)
        self._core_cache = {}

    def validate_batch(self, paths: List[Union[str, Path]],
                      parallel: bool = True,
                      chunk_size: Optional[int] = None) -> BatchValidationResult:
        """
        Validate a batch of paths.

        Args:
            paths: List of paths to validate
            parallel: Whether to use parallel processing
            chunk_size: Size of chunks for parallel processing

        Returns:
            BatchValidationResult: Comprehensive batch results
        """
        if not paths:
            return BatchValidationResult([])

        if parallel and len(paths) > 10:
            return self._validate_parallel(paths, chunk_size)
        else:
            return self._validate_sequential(paths)

    def _validate_sequential(self, paths: List[Union[str, Path]]) -> BatchValidationResult:
        """Validate paths sequentially."""
        core = ValidationCore(self.config)
        results = []

        for path in paths:
            try:
                result = core.validate(str(path))
                results.append(result)
            except Exception as e:
                # Create error result for unexpected exceptions
                error_result = ValidationResult(
                    valid=False,
                    original_path=str(path),
                    error=PathValidationError(f"Validation failed: {e}", str(path))
                )
                results.append(error_result)

        return BatchValidationResult(results)

    def _validate_parallel(self, paths: List[Union[str, Path]],
                          chunk_size: Optional[int] = None) -> BatchValidationResult:
        """Validate paths in parallel using thread pool."""
        if chunk_size is None:
            chunk_size = max(1, len(paths) // self.max_workers)

        results = [None] * len(paths)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit chunks for processing
            future_to_indices = {}
            for i in range(0, len(paths), chunk_size):
                chunk = paths[i:i + chunk_size]
                indices = list(range(i, min(i + chunk_size, len(paths))))
                future = executor.submit(self._validate_chunk, chunk)
                future_to_indices[future] = indices

            # Collect results
            for future in concurrent.futures.as_completed(future_to_indices):
                indices = future_to_indices[future]
                try:
                    chunk_results = future.result()
                    for idx, result in zip(indices, chunk_results):
                        results[idx] = result
                except Exception as e:
                    # Handle chunk processing errors
                    for idx in indices:
                        error_result = ValidationResult(
                            valid=False,
                            original_path=str(paths[idx]),
                            error=PathValidationError(f"Batch processing error: {e}", str(paths[idx]))
                        )
                        results[idx] = error_result

        return BatchValidationResult(results)

    def _validate_chunk(self, paths: List[Union[str, Path]]) -> List[ValidationResult]:
        """Validate a chunk of paths in a single thread."""
        # Create a core instance for this thread
        thread_id = concurrent.futures.current_executor()._threads.ident if hasattr(concurrent.futures.current_executor(), '_threads') else 0
        if thread_id not in self._core_cache:
            self._core_cache[thread_id] = ValidationCore(self.config)

        core = self._core_cache[thread_id]
        results = []

        for path in paths:
            try:
                result = core.validate(str(path))
                results.append(result)
            except Exception as e:
                error_result = ValidationResult(
                    valid=False,
                    original_path=str(path),
                    error=PathValidationError(f"Validation failed: {e}", str(path))
                )
                results.append(error_result)

        return results

    def validate_streaming(self, paths: Iterator[Union[str, Path]],
                          buffer_size: int = 1000) -> Iterator[ValidationResult]:
        """
        Stream validation results for very large datasets.

        Args:
            paths: Iterator of paths to validate
            buffer_size: Size of internal buffer for batching

        Yields:
            ValidationResult: Individual validation results
        """
        buffer = []
        for path in paths:
            buffer.append(path)

            if len(buffer) >= buffer_size:
                batch_result = self.validate_batch(buffer, parallel=True)
                for result in batch_result.results:
                    yield result
                buffer.clear()

        # Process remaining paths
        if buffer:
            batch_result = self.validate_batch(buffer, parallel=True)
            for result in batch_result.results:
                yield result

    def filter_valid_paths(self, paths: List[Union[str, Path]],
                          parallel: bool = True) -> List[str]:
        """
        Filter paths to only include valid ones.

        Args:
            paths: List of paths to filter
            parallel: Whether to use parallel processing

        Returns:
            List[str]: Only the valid normalized paths
        """
        batch_result = self.validate_batch(paths, parallel=parallel)
        return [r.normalized_path for r in batch_result.get_valid_results()]

    def group_by_validity(self, paths: List[Union[str, Path]],
                         parallel: bool = True) -> Dict[str, List[str]]:
        """
        Group paths by their validation status.

        Args:
            paths: List of paths to group
            parallel: Whether to use parallel processing

        Returns:
            Dict with 'valid' and 'invalid' keys containing respective paths
        """
        batch_result = self.validate_batch(paths, parallel=parallel)

        return {
            'valid': [r.normalized_path for r in batch_result.get_valid_results()],
            'invalid': [r.original_path for r in batch_result.get_invalid_results()]
        }

    def get_error_summary(self, paths: List[Union[str, Path]],
                         parallel: bool = True) -> Dict[str, Any]:
        """
        Get comprehensive error summary for a batch of paths.

        Args:
            paths: List of paths to analyze
            parallel: Whether to use parallel processing

        Returns:
            Dict containing error analysis
        """
        batch_result = self.validate_batch(paths, parallel=parallel)
        summary = batch_result.to_summary()

        # Add detailed error information
        error_details = {}
        for result in batch_result.get_invalid_results():
            if result.error:
                error_type = result.error.__class__.__name__
                if error_type not in error_details:
                    error_details[error_type] = []
                error_details[error_type].append({
                    'path': result.original_path,
                    'message': str(result.error),
                    'code': result.error.error_code,
                    'suggestions': result.suggestions
                })

        summary['error_details'] = error_details
        return summary

    def validate_with_callback(self, paths: List[Union[str, Path]],
                              callback: Callable[[ValidationResult], None],
                              parallel: bool = True) -> BatchValidationResult:
        """
        Validate paths and call callback for each result.

        Args:
            paths: List of paths to validate
            callback: Function to call for each validation result
            parallel: Whether to use parallel processing

        Returns:
            BatchValidationResult: Complete batch results
        """
        batch_result = self.validate_batch(paths, parallel=parallel)

        for result in batch_result.results:
            try:
                callback(result)
            except Exception:
                # Don't let callback errors affect validation
                pass

        return batch_result

    def benchmark_performance(self, paths: List[Union[str, Path]],
                            iterations: int = 3) -> Dict[str, Any]:
        """
        Benchmark validation performance.

        Args:
            paths: List of paths to use for benchmarking
            iterations: Number of benchmark iterations

        Returns:
            Dict containing performance metrics
        """
        sequential_times = []
        parallel_times = []

        for _ in range(iterations):
            # Sequential benchmark
            start_time = time.perf_counter()
            self.validate_batch(paths, parallel=False)
            sequential_times.append(time.perf_counter() - start_time)

            # Parallel benchmark
            start_time = time.perf_counter()
            self.validate_batch(paths, parallel=True)
            parallel_times.append(time.perf_counter() - start_time)

        return {
            'path_count': len(paths),
            'iterations': iterations,
            'sequential': {
                'avg_time': sum(sequential_times) / len(sequential_times),
                'min_time': min(sequential_times),
                'max_time': max(sequential_times),
                'throughput_per_sec': len(paths) / (sum(sequential_times) / len(sequential_times))
            },
            'parallel': {
                'avg_time': sum(parallel_times) / len(parallel_times),
                'min_time': min(parallel_times),
                'max_time': max(parallel_times),
                'throughput_per_sec': len(paths) / (sum(parallel_times) / len(parallel_times))
            },
            'speedup': (sum(sequential_times) / len(sequential_times)) / (sum(parallel_times) / len(parallel_times))
        }