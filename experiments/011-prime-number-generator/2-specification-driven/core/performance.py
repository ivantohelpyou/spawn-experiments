"""
Performance monitoring and benchmarking for the Prime Number Generator application.

This module provides comprehensive performance analysis capabilities including
execution time measurement, memory usage tracking, and algorithm comparison.
"""

import time
import gc
import tracemalloc
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
try:
    from ..utils.exceptions import PerformanceError
    from ..utils.helpers import format_time, format_memory, get_system_info
except ImportError:
    from utils.exceptions import PerformanceError
    from utils.helpers import format_time, format_memory, get_system_info


@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics for algorithm execution."""
    algorithm_name: str
    input_parameters: Dict[str, Any]
    execution_time: float
    memory_peak: int
    memory_current: int
    operations_count: Optional[int] = None
    result_size: Optional[int] = None
    system_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComparisonResult:
    """Result of algorithm performance comparison."""
    test_name: str
    parameters: Dict[str, Any]
    metrics: List[PerformanceMetrics]
    fastest_algorithm: str
    slowest_algorithm: str
    memory_efficient_algorithm: str
    memory_intensive_algorithm: str
    recommendations: List[str]


class PerformanceMonitor:
    """
    Monitor and measure performance of prime number operations.

    This class provides detailed performance monitoring including
    execution time, memory usage, and system resource utilization.
    """

    def __init__(self):
        self.system_info = get_system_info()

    def measure_execution(self, func: Callable, *args, **kwargs) -> PerformanceMetrics:
        """
        Measure execution performance of a function.

        Args:
            func: Function to measure
            *args: Positional arguments for function
            **kwargs: Keyword arguments for function

        Returns:
            PerformanceMetrics object with detailed measurements

        Raises:
            PerformanceError: If measurement fails
        """
        try:
            # Start memory monitoring
            tracemalloc.start()
            gc.collect()  # Clean up before measurement

            # Record start time
            start_time = time.perf_counter()

            # Execute function
            result = func(*args, **kwargs)

            # Record end time
            end_time = time.perf_counter()

            # Get memory usage
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Calculate metrics
            execution_time = end_time - start_time
            result_size = len(result) if hasattr(result, '__len__') else None

            return PerformanceMetrics(
                algorithm_name=getattr(func, '__name__', str(func)),
                input_parameters={'args': args, 'kwargs': kwargs},
                execution_time=execution_time,
                memory_peak=peak,
                memory_current=current,
                result_size=result_size,
                system_info=self.system_info
            )

        except Exception as e:
            raise PerformanceError(f"Performance measurement failed: {e}")

    def benchmark_algorithm(self, algorithm_func: Callable, test_cases: List[Dict[str, Any]],
                          iterations: int = 1) -> List[PerformanceMetrics]:
        """
        Benchmark an algorithm across multiple test cases.

        Args:
            algorithm_func: Algorithm function to benchmark
            test_cases: List of test case parameters
            iterations: Number of iterations per test case

        Returns:
            List of PerformanceMetrics for each test case
        """
        results = []

        for test_case in test_cases:
            # Run multiple iterations and take the best time
            best_metrics = None
            best_time = float('inf')

            for _ in range(iterations):
                metrics = self.measure_execution(algorithm_func, **test_case)

                if metrics.execution_time < best_time:
                    best_time = metrics.execution_time
                    best_metrics = metrics

            if best_metrics:
                # Update with test case info
                best_metrics.input_parameters = test_case
                results.append(best_metrics)

        return results

    def profile_memory_usage(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Detailed memory profiling of function execution.

        Args:
            func: Function to profile
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Dictionary with detailed memory usage information
        """
        tracemalloc.start()
        gc.collect()

        # Record initial memory
        initial_current, _ = tracemalloc.get_traced_memory()

        # Execute function
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        # Get final memory stats
        final_current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            'initial_memory': initial_current,
            'final_memory': final_current,
            'peak_memory': peak,
            'memory_delta': final_current - initial_current,
            'execution_time': end_time - start_time,
            'result_size': len(result) if hasattr(result, '__len__') else None
        }


class AlgorithmComparator:
    """
    Compare performance of different prime number generation algorithms.

    This class provides side-by-side comparison of algorithms across
    various input parameters and generates optimization recommendations.
    """

    def __init__(self):
        self.monitor = PerformanceMonitor()

    def compare_algorithms(self, algorithms: Dict[str, Callable], test_parameters: Dict[str, Any],
                         iterations: int = 3) -> ComparisonResult:
        """
        Compare multiple algorithms on the same test parameters.

        Args:
            algorithms: Dictionary mapping algorithm names to functions
            test_parameters: Parameters to test with
            iterations: Number of iterations for each algorithm

        Returns:
            ComparisonResult with detailed comparison data
        """
        metrics_list = []

        for name, algorithm in algorithms.items():
            try:
                # Run benchmark for this algorithm
                test_cases = [test_parameters]
                metrics = self.monitor.benchmark_algorithm(algorithm, test_cases, iterations)

                if metrics:
                    # Update algorithm name
                    metrics[0].algorithm_name = name
                    metrics_list.append(metrics[0])

            except Exception as e:
                # Create error metrics for failed algorithms
                error_metrics = PerformanceMetrics(
                    algorithm_name=name,
                    input_parameters=test_parameters,
                    execution_time=float('inf'),
                    memory_peak=0,
                    memory_current=0,
                    operations_count=None,
                    result_size=None
                )
                metrics_list.append(error_metrics)

        # Analyze results
        fastest_algorithm = min(metrics_list, key=lambda m: m.execution_time).algorithm_name
        slowest_algorithm = max(metrics_list, key=lambda m: m.execution_time).algorithm_name
        memory_efficient = min(metrics_list, key=lambda m: m.memory_peak).algorithm_name
        memory_intensive = max(metrics_list, key=lambda m: m.memory_peak).algorithm_name

        # Generate recommendations
        recommendations = self._generate_recommendations(metrics_list, test_parameters)

        return ComparisonResult(
            test_name=f"Algorithm Comparison",
            parameters=test_parameters,
            metrics=metrics_list,
            fastest_algorithm=fastest_algorithm,
            slowest_algorithm=slowest_algorithm,
            memory_efficient_algorithm=memory_efficient,
            memory_intensive_algorithm=memory_intensive,
            recommendations=recommendations
        )

    def _generate_recommendations(self, metrics: List[PerformanceMetrics],
                                test_parameters: Dict[str, Any]) -> List[str]:
        """
        Generate optimization recommendations based on performance metrics.

        Args:
            metrics: List of performance metrics
            test_parameters: Test parameters used

        Returns:
            List of recommendation strings
        """
        recommendations = []

        if not metrics:
            return ["No metrics available for analysis"]

        # Time-based recommendations
        time_diff = max(m.execution_time for m in metrics) / min(m.execution_time for m in metrics)
        if time_diff > 10:
            fastest = min(metrics, key=lambda m: m.execution_time)
            recommendations.append(
                f"Significant performance difference detected. "
                f"Use '{fastest.algorithm_name}' for best speed."
            )

        # Memory-based recommendations
        memory_diff = max(m.memory_peak for m in metrics) / max(min(m.memory_peak for m in metrics), 1)
        if memory_diff > 5:
            memory_efficient = min(metrics, key=lambda m: m.memory_peak)
            recommendations.append(
                f"Large memory usage difference detected. "
                f"Use '{memory_efficient.algorithm_name}' for memory efficiency."
            )

        # Parameter-specific recommendations
        limit = test_parameters.get('limit', 0)
        if limit > 100000:
            recommendations.append("For large limits, consider using Sieve of Eratosthenes")
        elif limit < 1000:
            recommendations.append("For small limits, Trial Division is sufficient")

        if 'start' in test_parameters and 'end' in test_parameters:
            range_size = test_parameters['end'] - test_parameters['start']
            if range_size > 50000:
                recommendations.append("For large ranges, Sieve-based algorithms are more efficient")

        return recommendations

    def run_comprehensive_benchmark(self, algorithms: Dict[str, Callable]) -> List[ComparisonResult]:
        """
        Run comprehensive benchmarks across various input sizes.

        Args:
            algorithms: Dictionary of algorithms to compare

        Returns:
            List of ComparisonResult objects for different test scenarios
        """
        test_scenarios = [
            {'name': 'Small Range', 'parameters': {'limit': 100}},
            {'name': 'Medium Range', 'parameters': {'limit': 10000}},
            {'name': 'Large Range', 'parameters': {'limit': 100000}},
            {'name': 'Range Test', 'parameters': {'start': 1000, 'end': 2000}},
            {'name': 'First N Primes', 'parameters': {'count': 1000}},
        ]

        results = []

        for scenario in test_scenarios:
            try:
                # Filter algorithms that support the parameters
                compatible_algorithms = {}
                for name, func in algorithms.items():
                    try:
                        # Test if algorithm supports these parameters
                        func(**scenario['parameters'])
                        compatible_algorithms[name] = func
                    except Exception:
                        continue  # Skip incompatible algorithms

                if compatible_algorithms:
                    result = self.compare_algorithms(
                        compatible_algorithms,
                        scenario['parameters']
                    )
                    result.test_name = scenario['name']
                    results.append(result)

            except Exception as e:
                # Log error but continue with other scenarios
                continue

        return results


class BenchmarkRunner:
    """
    Standardized benchmark runner for prime number generation performance.

    This class provides pre-defined benchmark suites and performance
    regression testing capabilities.
    """

    def __init__(self):
        self.comparator = AlgorithmComparator()
        self.standard_test_cases = [
            {'limit': 100, 'expected_count': 25},
            {'limit': 1000, 'expected_count': 168},
            {'limit': 10000, 'expected_count': 1229},
            {'limit': 100000, 'expected_count': 9592},
        ]

    def run_standard_benchmarks(self, algorithms: Dict[str, Callable]) -> Dict[str, Any]:
        """
        Run standardized benchmark suite.

        Args:
            algorithms: Dictionary of algorithms to benchmark

        Returns:
            Dictionary with comprehensive benchmark results
        """
        results = {
            'timestamp': time.time(),
            'system_info': get_system_info(),
            'algorithm_results': {},
            'comparisons': [],
            'summary': {}
        }

        # Individual algorithm benchmarks
        for name, algorithm in algorithms.items():
            algorithm_results = []

            for test_case in self.standard_test_cases:
                try:
                    metrics = self.comparator.monitor.measure_execution(
                        algorithm, limit=test_case['limit']
                    )
                    metrics.algorithm_name = name

                    # Verify correctness
                    result = algorithm(limit=test_case['limit'])
                    actual_count = len(result) if hasattr(result, '__len__') else 0
                    metrics.operations_count = actual_count

                    algorithm_results.append({
                        'test_case': test_case,
                        'metrics': metrics,
                        'correct': actual_count == test_case['expected_count']
                    })

                except Exception as e:
                    algorithm_results.append({
                        'test_case': test_case,
                        'error': str(e),
                        'correct': False
                    })

            results['algorithm_results'][name] = algorithm_results

        # Comparative benchmarks
        for test_case in self.standard_test_cases:
            try:
                comparison = self.comparator.compare_algorithms(
                    algorithms,
                    {'limit': test_case['limit']}
                )
                results['comparisons'].append(comparison)
            except Exception:
                continue

        # Generate summary
        results['summary'] = self._generate_benchmark_summary(results)

        return results

    def _generate_benchmark_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate summary statistics from benchmark results.

        Args:
            results: Benchmark results dictionary

        Returns:
            Summary statistics dictionary
        """
        summary = {
            'total_tests': 0,
            'passed_tests': 0,
            'algorithm_rankings': {},
            'performance_insights': []
        }

        # Count total tests and passes
        for algorithm_name, algorithm_results in results['algorithm_results'].items():
            for result in algorithm_results:
                summary['total_tests'] += 1
                if result.get('correct', False):
                    summary['passed_tests'] += 1

        # Calculate pass rate
        if summary['total_tests'] > 0:
            summary['pass_rate'] = summary['passed_tests'] / summary['total_tests']
        else:
            summary['pass_rate'] = 0

        # Algorithm rankings based on average performance
        algorithm_avg_times = {}
        for algorithm_name, algorithm_results in results['algorithm_results'].items():
            times = []
            for result in algorithm_results:
                if 'metrics' in result:
                    times.append(result['metrics'].execution_time)

            if times:
                algorithm_avg_times[algorithm_name] = sum(times) / len(times)

        # Sort by average time
        sorted_algorithms = sorted(algorithm_avg_times.items(), key=lambda x: x[1])
        summary['algorithm_rankings'] = {
            'by_speed': [alg for alg, _ in sorted_algorithms],
            'average_times': dict(sorted_algorithms)
        }

        return summary


def format_performance_report(metrics: PerformanceMetrics) -> str:
    """
    Format performance metrics into a human-readable report.

    Args:
        metrics: Performance metrics to format

    Returns:
        Formatted report string
    """
    report = f"Performance Report for {metrics.algorithm_name}\n"
    report += "=" * (len(report) - 1) + "\n\n"

    report += f"Execution Time: {format_time(metrics.execution_time)}\n"
    report += f"Peak Memory Usage: {format_memory(metrics.memory_peak)}\n"
    report += f"Current Memory Usage: {format_memory(metrics.memory_current)}\n"

    if metrics.result_size is not None:
        report += f"Result Size: {metrics.result_size:,} items\n"

    if metrics.operations_count is not None:
        report += f"Operations Count: {metrics.operations_count:,}\n"

    report += f"\nInput Parameters:\n"
    for key, value in metrics.input_parameters.items():
        report += f"  {key}: {value}\n"

    return report


def format_comparison_report(comparison: ComparisonResult) -> str:
    """
    Format algorithm comparison results into a readable report.

    Args:
        comparison: Comparison results to format

    Returns:
        Formatted comparison report
    """
    report = f"Algorithm Comparison Report: {comparison.test_name}\n"
    report += "=" * (len(report) - 1) + "\n\n"

    report += "Test Parameters:\n"
    for key, value in comparison.parameters.items():
        report += f"  {key}: {value}\n"
    report += "\n"

    report += "Results:\n"
    for metrics in comparison.metrics:
        report += f"  {metrics.algorithm_name}:\n"
        report += f"    Time: {format_time(metrics.execution_time)}\n"
        report += f"    Memory: {format_memory(metrics.memory_peak)}\n"
        if metrics.result_size:
            report += f"    Results: {metrics.result_size:,} items\n"
        report += "\n"

    report += f"Fastest Algorithm: {comparison.fastest_algorithm}\n"
    report += f"Most Memory Efficient: {comparison.memory_efficient_algorithm}\n\n"

    if comparison.recommendations:
        report += "Recommendations:\n"
        for rec in comparison.recommendations:
            report += f"  • {rec}\n"

    return report