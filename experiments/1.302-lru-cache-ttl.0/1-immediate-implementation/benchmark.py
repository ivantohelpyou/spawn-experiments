#!/usr/bin/env python3
"""
Performance Benchmarking for LRU Cache with TTL

This module provides comprehensive performance testing and benchmarking
for the LRU Cache with TTL implementation.

Features:
- Single-threaded and multi-threaded performance tests
- Memory usage analysis
- Operation timing and throughput measurements
- Comparison with standard Python dict and other caches
- Stress testing with various workload patterns
- Performance regression detection
"""

import time
import threading
import multiprocessing
import statistics
import sys
import gc
import random
import string
from typing import List, Dict, Any, Callable
from collections import defaultdict
import psutil
import os
from lru_cache_ttl import LRUCacheWithTTL, create_cache


class PerformanceTimer:
    """Context manager for timing operations."""

    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        gc.collect()  # Clean garbage before timing
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()

    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None or self.end_time is None:
            return 0.0
        return self.end_time - self.start_time

    @property
    def elapsed_ms(self) -> float:
        """Get elapsed time in milliseconds."""
        return self.elapsed * 1000


class MemoryTracker:
    """Track memory usage during operations."""

    def __init__(self):
        self.process = psutil.Process()
        self.initial_memory = None
        self.peak_memory = None

    def start(self):
        """Start memory tracking."""
        gc.collect()
        self.initial_memory = self.process.memory_info().rss
        self.peak_memory = self.initial_memory

    def update(self):
        """Update peak memory usage."""
        current_memory = self.process.memory_info().rss
        if current_memory > self.peak_memory:
            self.peak_memory = current_memory

    def get_usage_mb(self) -> Dict[str, float]:
        """Get memory usage in MB."""
        current_memory = self.process.memory_info().rss
        return {
            'initial_mb': self.initial_memory / 1024 / 1024 if self.initial_memory else 0,
            'current_mb': current_memory / 1024 / 1024,
            'peak_mb': self.peak_memory / 1024 / 1024 if self.peak_memory else 0,
            'delta_mb': (current_memory - self.initial_memory) / 1024 / 1024 if self.initial_memory else 0
        }


class BenchmarkSuite:
    """Comprehensive benchmark suite for LRU Cache with TTL."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.results = defaultdict(list)
        self.memory_tracker = MemoryTracker()

    def log(self, message: str):
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[BENCHMARK] {message}")

    def generate_keys(self, count: int, prefix: str = "key") -> List[str]:
        """Generate random keys for testing."""
        return [f"{prefix}_{i}_{random.randint(1000, 9999)}" for i in range(count)]

    def generate_values(self, count: int, size: str = "small") -> List[Any]:
        """Generate test values of different sizes."""
        if size == "small":
            return [f"value_{i}" for i in range(count)]
        elif size == "medium":
            return [{"id": i, "data": "x" * 100, "timestamp": time.time()} for i in range(count)]
        elif size == "large":
            return [{"id": i, "data": "x" * 1000, "nested": {"more": "x" * 500}} for i in range(count)]
        else:
            return [f"value_{i}" for i in range(count)]

    def benchmark_basic_operations(self, cache_size: int = 1000, num_operations: int = 10000):
        """Benchmark basic cache operations."""
        self.log(f"Benchmarking basic operations (cache_size={cache_size}, operations={num_operations})")

        cache = create_cache(max_size=cache_size)
        keys = self.generate_keys(num_operations)
        values = self.generate_values(num_operations)

        try:
            # Benchmark SET operations
            with PerformanceTimer("SET operations") as timer:
                for i in range(num_operations):
                    cache.set(keys[i % len(keys)], values[i % len(values)])

            set_ops_per_sec = num_operations / timer.elapsed
            self.results['set_ops_per_sec'].append(set_ops_per_sec)
            self.log(f"SET: {set_ops_per_sec:.0f} ops/sec ({timer.elapsed_ms:.2f}ms total)")

            # Benchmark GET operations (with hits and misses)
            hit_keys = keys[:num_operations // 2]
            miss_keys = [f"miss_{i}" for i in range(num_operations // 2)]
            test_keys = hit_keys + miss_keys
            random.shuffle(test_keys)

            with PerformanceTimer("GET operations") as timer:
                for key in test_keys:
                    cache.get(key)

            get_ops_per_sec = len(test_keys) / timer.elapsed
            self.results['get_ops_per_sec'].append(get_ops_per_sec)
            self.log(f"GET: {get_ops_per_sec:.0f} ops/sec ({timer.elapsed_ms:.2f}ms total)")

            # Benchmark DELETE operations
            delete_keys = keys[:num_operations // 4]
            with PerformanceTimer("DELETE operations") as timer:
                for key in delete_keys:
                    cache.delete(key)

            delete_ops_per_sec = len(delete_keys) / timer.elapsed
            self.results['delete_ops_per_sec'].append(delete_ops_per_sec)
            self.log(f"DELETE: {delete_ops_per_sec:.0f} ops/sec ({timer.elapsed_ms:.2f}ms total)")

            # Get final statistics
            stats = cache.get_stats()
            self.log(f"Final stats: {stats}")

        finally:
            cache.close()

    def benchmark_ttl_operations(self, cache_size: int = 1000, num_operations: int = 5000):
        """Benchmark TTL-specific operations."""
        self.log(f"Benchmarking TTL operations (cache_size={cache_size}, operations={num_operations})")

        cache = create_cache(max_size=cache_size, default_ttl=60.0)
        keys = self.generate_keys(num_operations)
        values = self.generate_values(num_operations)

        try:
            # Benchmark SET with TTL
            ttl_values = [random.uniform(1.0, 3600.0) for _ in range(num_operations)]

            with PerformanceTimer("SET with TTL") as timer:
                for i in range(num_operations):
                    cache.set(keys[i], values[i], ttl=ttl_values[i])

            set_ttl_ops_per_sec = num_operations / timer.elapsed
            self.results['set_ttl_ops_per_sec'].append(set_ttl_ops_per_sec)
            self.log(f"SET with TTL: {set_ttl_ops_per_sec:.0f} ops/sec")

            # Benchmark TTL checking
            with PerformanceTimer("TTL checking") as timer:
                for key in keys:
                    cache.ttl(key)

            ttl_check_ops_per_sec = len(keys) / timer.elapsed
            self.results['ttl_check_ops_per_sec'].append(ttl_check_ops_per_sec)
            self.log(f"TTL check: {ttl_check_ops_per_sec:.0f} ops/sec")

            # Test expiration handling
            short_ttl_keys = [f"short_{i}" for i in range(100)]
            for key in short_ttl_keys:
                cache.set(key, "temp_value", ttl=0.1)

            time.sleep(0.2)  # Wait for expiration

            with PerformanceTimer("Expired key access") as timer:
                for key in short_ttl_keys:
                    cache.get(key)  # Should return None for expired keys

            expired_ops_per_sec = len(short_ttl_keys) / timer.elapsed
            self.results['expired_ops_per_sec'].append(expired_ops_per_sec)
            self.log(f"Expired key access: {expired_ops_per_sec:.0f} ops/sec")

        finally:
            cache.close()

    def benchmark_lru_behavior(self, cache_size: int = 100, num_operations: int = 1000):
        """Benchmark LRU eviction behavior."""
        self.log(f"Benchmarking LRU behavior (cache_size={cache_size}, operations={num_operations})")

        cache = create_cache(max_size=cache_size)
        keys = self.generate_keys(num_operations * 2)  # More keys than cache size
        values = self.generate_values(num_operations * 2)

        try:
            # Fill cache beyond capacity to trigger evictions
            with PerformanceTimer("LRU eviction stress test") as timer:
                for i in range(num_operations * 2):
                    cache.set(keys[i], values[i])

            eviction_ops_per_sec = (num_operations * 2) / timer.elapsed
            self.results['eviction_ops_per_sec'].append(eviction_ops_per_sec)

            stats = cache.get_stats()
            eviction_count = stats['evictions']
            self.log(f"LRU evictions: {eviction_ops_per_sec:.0f} ops/sec, {eviction_count} evictions")

            # Test access pattern that affects LRU order
            access_keys = keys[:cache_size // 2]
            with PerformanceTimer("LRU order update") as timer:
                for _ in range(100):
                    for key in access_keys:
                        cache.get(key)

            lru_update_ops_per_sec = (len(access_keys) * 100) / timer.elapsed
            self.results['lru_update_ops_per_sec'].append(lru_update_ops_per_sec)
            self.log(f"LRU order updates: {lru_update_ops_per_sec:.0f} ops/sec")

        finally:
            cache.close()

    def benchmark_concurrency(self, cache_size: int = 1000, num_threads: int = 4, operations_per_thread: int = 1000):
        """Benchmark concurrent access performance."""
        self.log(f"Benchmarking concurrency ({num_threads} threads, {operations_per_thread} ops each)")

        cache = create_cache(max_size=cache_size)
        barrier = threading.Barrier(num_threads)
        results = {}

        def worker(thread_id: int):
            keys = self.generate_keys(operations_per_thread, f"thread_{thread_id}")
            values = self.generate_values(operations_per_thread)

            # Wait for all threads to be ready
            barrier.wait()

            # Mixed operations
            start_time = time.perf_counter()

            for i in range(operations_per_thread):
                if i % 3 == 0:
                    cache.set(keys[i], values[i])
                elif i % 3 == 1:
                    cache.get(keys[i % (len(keys) // 2)])  # Some hits, some misses
                else:
                    if i < len(keys) // 4:
                        cache.delete(keys[i])

            end_time = time.perf_counter()
            results[thread_id] = end_time - start_time

        try:
            threads = []
            for i in range(num_threads):
                t = threading.Thread(target=worker, args=(i,))
                threads.append(t)

            # Start all threads
            overall_start = time.perf_counter()
            for t in threads:
                t.start()

            # Wait for completion
            for t in threads:
                t.join()
            overall_end = time.perf_counter()

            # Calculate metrics
            total_operations = num_threads * operations_per_thread
            overall_ops_per_sec = total_operations / (overall_end - overall_start)
            self.results['concurrent_ops_per_sec'].append(overall_ops_per_sec)

            avg_thread_time = statistics.mean(results.values())
            max_thread_time = max(results.values())
            min_thread_time = min(results.values())

            self.log(f"Concurrent performance: {overall_ops_per_sec:.0f} ops/sec overall")
            self.log(f"Thread times - Avg: {avg_thread_time:.3f}s, Min: {min_thread_time:.3f}s, Max: {max_thread_time:.3f}s")

            stats = cache.get_stats()
            self.log(f"Final stats: {stats}")

        finally:
            cache.close()

    def benchmark_memory_usage(self, cache_sizes: List[int] = None):
        """Benchmark memory usage with different cache sizes."""
        if cache_sizes is None:
            cache_sizes = [100, 1000, 10000, 50000]

        self.log("Benchmarking memory usage")
        self.memory_tracker.start()

        for cache_size in cache_sizes:
            gc.collect()
            initial_memory = self.memory_tracker.process.memory_info().rss

            cache = create_cache(max_size=cache_size)

            try:
                # Fill cache completely
                keys = self.generate_keys(cache_size)
                values = self.generate_values(cache_size, "medium")

                for i in range(cache_size):
                    cache.set(keys[i], values[i])

                final_memory = self.memory_tracker.process.memory_info().rss
                memory_per_item = (final_memory - initial_memory) / cache_size

                self.log(f"Cache size {cache_size}: {memory_per_item:.2f} bytes per item")
                self.results['memory_per_item'].append((cache_size, memory_per_item))

            finally:
                cache.close()

    def benchmark_vs_dict(self, num_operations: int = 10000):
        """Benchmark against standard Python dict."""
        self.log(f"Benchmarking vs Python dict ({num_operations} operations)")

        keys = self.generate_keys(num_operations)
        values = self.generate_values(num_operations)

        # Test LRU Cache
        cache = create_cache(max_size=num_operations)
        try:
            with PerformanceTimer("LRU Cache operations") as cache_timer:
                for i in range(num_operations):
                    cache.set(keys[i], values[i])
                for i in range(num_operations):
                    cache.get(keys[i])

            cache_ops_per_sec = (2 * num_operations) / cache_timer.elapsed
        finally:
            cache.close()

        # Test standard dict
        test_dict = {}
        with PerformanceTimer("Dict operations") as dict_timer:
            for i in range(num_operations):
                test_dict[keys[i]] = values[i]
            for i in range(num_operations):
                _ = test_dict.get(keys[i])

        dict_ops_per_sec = (2 * num_operations) / dict_timer.elapsed

        self.log(f"LRU Cache: {cache_ops_per_sec:.0f} ops/sec")
        self.log(f"Python dict: {dict_ops_per_sec:.0f} ops/sec")
        self.log(f"Overhead: {((dict_ops_per_sec - cache_ops_per_sec) / dict_ops_per_sec * 100):.1f}%")

        self.results['cache_vs_dict'].append({
            'cache_ops_per_sec': cache_ops_per_sec,
            'dict_ops_per_sec': dict_ops_per_sec,
            'overhead_percent': (dict_ops_per_sec - cache_ops_per_sec) / dict_ops_per_sec * 100
        })

    def run_stress_test(self, duration_seconds: int = 30, cache_size: int = 1000):
        """Run a stress test for the specified duration."""
        self.log(f"Running stress test for {duration_seconds} seconds")

        cache = create_cache(max_size=cache_size)
        start_time = time.time()
        operation_count = 0
        errors = 0

        try:
            while time.time() - start_time < duration_seconds:
                try:
                    # Random operations
                    op_type = random.choice(['set', 'get', 'delete'])
                    key = f"stress_key_{random.randint(0, cache_size * 2)}"

                    if op_type == 'set':
                        value = f"stress_value_{operation_count}"
                        ttl = random.choice([None, random.uniform(1, 10)])
                        cache.set(key, value, ttl)
                    elif op_type == 'get':
                        cache.get(key)
                    elif op_type == 'delete':
                        cache.delete(key)

                    operation_count += 1

                except Exception as e:
                    errors += 1
                    if errors > 100:  # Too many errors
                        break

            elapsed = time.time() - start_time
            ops_per_sec = operation_count / elapsed

            self.log(f"Stress test completed: {ops_per_sec:.0f} ops/sec, {errors} errors")
            self.results['stress_test_ops_per_sec'].append(ops_per_sec)

            stats = cache.get_stats()
            self.log(f"Final stats: {stats}")

        finally:
            cache.close()

    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive performance report."""
        report = {
            'summary': {},
            'detailed_results': dict(self.results),
            'memory_usage': self.memory_tracker.get_usage_mb(),
            'system_info': {
                'cpu_count': multiprocessing.cpu_count(),
                'python_version': sys.version,
                'platform': sys.platform
            }
        }

        # Calculate summary statistics
        for metric, values in self.results.items():
            if values and all(isinstance(v, (int, float)) for v in values):
                report['summary'][metric] = {
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'min': min(values),
                    'max': max(values),
                    'stdev': statistics.stdev(values) if len(values) > 1 else 0
                }

        return report

    def print_summary(self):
        """Print a summary of benchmark results."""
        print("\n" + "=" * 60)
        print("PERFORMANCE BENCHMARK SUMMARY")
        print("=" * 60)

        report = self.generate_report()

        print(f"System: {report['system_info']['cpu_count']} CPUs, {report['system_info']['platform']}")
        print(f"Memory: {report['memory_usage']['current_mb']:.1f} MB used")

        print("\nOperation Performance (ops/sec):")
        print("-" * 40)

        performance_metrics = [
            ('Basic SET', 'set_ops_per_sec'),
            ('Basic GET', 'get_ops_per_sec'),
            ('Basic DELETE', 'delete_ops_per_sec'),
            ('SET with TTL', 'set_ttl_ops_per_sec'),
            ('TTL Check', 'ttl_check_ops_per_sec'),
            ('LRU Eviction', 'eviction_ops_per_sec'),
            ('Concurrent', 'concurrent_ops_per_sec'),
            ('Stress Test', 'stress_test_ops_per_sec')
        ]

        for name, metric in performance_metrics:
            if metric in report['summary']:
                stats = report['summary'][metric]
                print(f"{name:15}: {stats['mean']:>10,.0f} ± {stats['stdev']:>8,.0f}")

        # Memory usage
        if 'memory_per_item' in self.results:
            print(f"\nMemory Usage:")
            print("-" * 20)
            for cache_size, memory_per_item in self.results['memory_per_item']:
                print(f"Cache size {cache_size:>6}: {memory_per_item:>6.1f} bytes/item")

        # Comparison with dict
        if 'cache_vs_dict' in self.results:
            comparison = self.results['cache_vs_dict'][-1]
            print(f"\nComparison with Python dict:")
            print("-" * 30)
            print(f"Cache overhead: {comparison['overhead_percent']:>6.1f}%")

        print()


def main():
    """Main function to run all benchmarks."""
    import argparse

    parser = argparse.ArgumentParser(description="LRU Cache with TTL Performance Benchmark")
    parser.add_argument('--quick', action='store_true', help='Run quick benchmark with reduced operations')
    parser.add_argument('--stress-duration', type=int, default=10, help='Stress test duration in seconds')
    parser.add_argument('--max-cache-size', type=int, default=10000, help='Maximum cache size for testing')
    parser.add_argument('--threads', type=int, default=4, help='Number of threads for concurrency test')
    parser.add_argument('--output', help='Save detailed results to JSON file')

    args = parser.parse_args()

    # Adjust parameters for quick mode
    if args.quick:
        operations_scale = 1000
        stress_duration = 5
    else:
        operations_scale = 10000
        stress_duration = args.stress_duration

    benchmark = BenchmarkSuite(verbose=True)

    print("Starting LRU Cache with TTL Performance Benchmark")
    print("=" * 60)

    try:
        # Run all benchmarks
        benchmark.benchmark_basic_operations(
            cache_size=min(1000, args.max_cache_size),
            num_operations=operations_scale
        )

        benchmark.benchmark_ttl_operations(
            cache_size=min(1000, args.max_cache_size),
            num_operations=operations_scale // 2
        )

        benchmark.benchmark_lru_behavior(
            cache_size=min(100, args.max_cache_size // 10),
            num_operations=operations_scale // 10
        )

        benchmark.benchmark_concurrency(
            cache_size=min(1000, args.max_cache_size),
            num_threads=args.threads,
            operations_per_thread=operations_scale // args.threads
        )

        if not args.quick:
            benchmark.benchmark_memory_usage()

        benchmark.benchmark_vs_dict(num_operations=operations_scale // 2)

        benchmark.run_stress_test(duration_seconds=stress_duration)

        # Generate and display results
        benchmark.print_summary()

        # Save detailed results if requested
        if args.output:
            import json
            report = benchmark.generate_report()
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\nDetailed results saved to: {args.output}")

    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user")
    except Exception as e:
        print(f"\nBenchmark failed with error: {e}")
        raise


if __name__ == "__main__":
    main()