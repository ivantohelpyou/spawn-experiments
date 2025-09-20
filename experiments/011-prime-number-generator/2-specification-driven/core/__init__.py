"""
Core modules for the Prime Number Generator application.

This package contains the core functionality including algorithms,
validators, and performance monitoring capabilities.
"""

from .algorithms import (
    PrimeGenerator,
    SieveOfEratosthenes,
    TrialDivision,
    OptimizedTrialDivision,
    AlgorithmConfig
)

from .validators import (
    PrimeValidator,
    BatchValidator,
    ValidationResult,
    quick_prime_check,
    validate_prime_list
)

from .performance import (
    PerformanceMonitor,
    AlgorithmComparator,
    BenchmarkRunner,
    PerformanceMetrics,
    ComparisonResult,
    format_performance_report,
    format_comparison_report
)

__all__ = [
    # Algorithms
    'PrimeGenerator',
    'SieveOfEratosthenes',
    'TrialDivision',
    'OptimizedTrialDivision',
    'AlgorithmConfig',

    # Validators
    'PrimeValidator',
    'BatchValidator',
    'ValidationResult',
    'quick_prime_check',
    'validate_prime_list',

    # Performance
    'PerformanceMonitor',
    'AlgorithmComparator',
    'BenchmarkRunner',
    'PerformanceMetrics',
    'ComparisonResult',
    'format_performance_report',
    'format_comparison_report'
]