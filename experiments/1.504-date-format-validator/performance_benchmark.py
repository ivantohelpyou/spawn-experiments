#!/usr/bin/env python3
"""
Performance Benchmark - Date Format Validator Methods
Collect execution speed data across all 5 methodology implementations
"""

import time
import sys
import os
from pathlib import Path

def benchmark_method(method_path, method_name, test_cases, iterations=10000):
    """Benchmark a specific method implementation."""
    print(f"\n🔥 Benchmarking {method_name}...")

    try:
        # Add method to path
        sys.path.insert(0, method_path)

        # Import the validator
        import date_validator

        # Warm up
        for case in test_cases[:5]:
            date_validator.validate_date(case)

        # Benchmark
        start_time = time.time()
        for _ in range(iterations):
            for test_case in test_cases:
                date_validator.validate_date(test_case)
        end_time = time.time()

        total_validations = iterations * len(test_cases)
        total_time = end_time - start_time
        validations_per_second = total_validations / total_time

        # Remove from path
        sys.path.remove(method_path)
        if 'date_validator' in sys.modules:
            del sys.modules['date_validator']

        return {
            'total_time': total_time,
            'validations_per_second': validations_per_second,
            'total_validations': total_validations,
            'status': 'success'
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

def main():
    """Run performance benchmarks across all methods."""
    print("="*80)
    print("📊 DATE FORMAT VALIDATOR - PERFORMANCE BENCHMARK")
    print("="*80)

    base_dir = "/home/ivan/projects/spawn-experiments/experiments/1.504-date-format-validator"

    # Test cases for benchmarking
    test_cases = [
        "02/29/2024",  # Valid leap year
        "02/29/2023",  # Invalid leap year
        "13/01/2024",  # EU format
        "01/13/2024",  # US format
        "12/31/2020",  # Valid date
        "2/5/2020",    # Single digits
        "",            # Empty string
        "abc",         # Invalid format
        "32/01/2020",  # Invalid day
        "02/30/2020"   # Feb 30
    ]

    methods = {
        "Method 1 (Immediate)": f"{base_dir}/1-immediate-implementation",
        "Method 2 (Specification)": f"{base_dir}/2-specification-driven",
        "Method 3 (Pure TDD)": f"{base_dir}/3-test-first-development",
        "Method 4 V4.0 (Guided TDD)": f"{base_dir}/4-specification-guided-tdd",
        "Method 4 V4.1 (Adaptive TDD)": f"{base_dir}/4-adaptive-tdd-v41"
    }

    results = {}
    iterations = 1000  # Reduced for reasonable runtime

    print(f"Running {iterations:,} iterations of {len(test_cases)} test cases each...")
    print(f"Total validations per method: {iterations * len(test_cases):,}")
    print()

    # Run benchmarks
    for method_name, method_path in methods.items():
        if os.path.exists(method_path):
            result = benchmark_method(method_path, method_name, test_cases, iterations)
            results[method_name] = result
        else:
            print(f"⚠️  {method_name}: Directory not found")
            results[method_name] = {'status': 'not_found'}

    # Display results
    print("\n" + "="*80)
    print("📊 PERFORMANCE RESULTS")
    print("="*80)

    print(f"{'Method':<30} {'Status':<10} {'Validations/sec':<15} {'Total Time':<12}")
    print("-" * 80)

    successful_results = []

    for method_name, result in results.items():
        if result['status'] == 'success':
            validations_per_sec = f"{result['validations_per_second']:,.0f}"
            total_time = f"{result['total_time']:.3f}s"
            status = "✅ Success"
            successful_results.append((method_name, result['validations_per_second']))
        elif result['status'] == 'error':
            validations_per_sec = "N/A"
            total_time = "N/A"
            status = f"❌ Error"
        else:
            validations_per_sec = "N/A"
            total_time = "N/A"
            status = "⚠️  Not found"

        print(f"{method_name:<30} {status:<10} {validations_per_sec:<15} {total_time:<12}")

    # Performance ranking
    if successful_results:
        print("\n🏆 PERFORMANCE RANKING:")
        successful_results.sort(key=lambda x: x[1], reverse=True)

        for i, (method_name, speed) in enumerate(successful_results, 1):
            print(f"   {i}. {method_name}: {speed:,.0f} validations/sec")

        # Speed comparison
        if len(successful_results) >= 2:
            fastest_speed = successful_results[0][1]
            print(f"\n📈 SPEED COMPARISON (vs fastest):")
            for method_name, speed in successful_results:
                ratio = speed / fastest_speed
                percentage = ratio * 100
                print(f"   {method_name}: {percentage:.1f}% of fastest speed")

    print(f"\n⚙️  Benchmark Details:")
    print(f"   • Test cases: {len(test_cases)}")
    print(f"   • Iterations: {iterations:,}")
    print(f"   • Total validations per method: {iterations * len(test_cases):,}")
    print(f"   • Python version: {sys.version.split()[0]}")

if __name__ == "__main__":
    main()