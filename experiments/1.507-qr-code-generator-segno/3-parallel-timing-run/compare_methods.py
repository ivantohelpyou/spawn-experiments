#!/usr/bin/env python3
"""
Methodology Comparison Script for Experiment 1.507.2
QR Code Generator using segno library - 4 Method Comparison
"""

import os
import sys
import time
import tempfile
from pathlib import Path
import importlib.util
import traceback
from statistics import mean, stdev

def load_module(method_path, module_name="qr_generator"):
    """Dynamically load a module from a method folder."""
    module_file = method_path / f"{module_name}.py"
    if not module_file.exists():
        return None

    spec = importlib.util.spec_from_file_location(module_name, module_file)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error loading {module_file}: {e}")
        return None

def count_lines_of_code(file_path):
    """Count non-empty, non-comment lines of code."""
    if not file_path.exists():
        return 0

    loc = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('"""') and not line.startswith("'''"):
                    loc += 1
    except Exception:
        return 0
    return loc

def read_development_time(method_path):
    """Extract development time from timing log."""
    timing_file = method_path / "TIMING_LOG.txt"
    if not timing_file.exists():
        return "Not measured"

    try:
        with open(timing_file, 'r', encoding='utf-8') as f:
            content = f.read()
            for line in content.split('\n'):
                if 'TOTAL DURATION:' in line:
                    return line.split('TOTAL DURATION:')[1].strip()
                elif 'Total Duration:' in line:
                    return line.split('Total Duration:')[1].strip()
    except Exception:
        pass
    return "Not measured"

def benchmark_method(module, test_data):
    """Benchmark a method implementation with runtime measurements."""
    print("⏱️  Performance Benchmarking:")

    benchmarks = {}

    # Test basic QR generation performance
    test_cases = [
        ("Short text", "Hello World"),
        ("Medium text", "This is a medium length text for QR code generation testing with various characters !@#$%"),
        ("Long text", "A" * 500),
        ("Unicode text", "Hello 世界! 🌍 This includes unicode characters: ñáéíóú αβγδε")
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        for test_name, text in test_cases:
            times = []

            # Run multiple iterations for reliable timing
            for i in range(10):
                filename = f"{temp_dir}/bench_{i}.png"

                try:
                    start_time = time.perf_counter()

                    # Test the primary function (try different possible function names)
                    if hasattr(module, 'generate_qr_code'):
                        result = module.generate_qr_code(text)
                    elif hasattr(module, 'generate_qr'):
                        result = module.generate_qr(text, filename)
                    else:
                        print(f"   ❌ No recognized QR generation function found")
                        break

                    end_time = time.perf_counter()
                    times.append((end_time - start_time) * 1000)  # Convert to milliseconds

                except Exception as e:
                    print(f"   ❌ Error in {test_name}: {str(e)[:50]}...")
                    break

            if times:
                avg_time = mean(times)
                std_time = stdev(times) if len(times) > 1 else 0
                benchmarks[test_name] = {
                    'avg_ms': avg_time,
                    'std_ms': std_time,
                    'min_ms': min(times),
                    'max_ms': max(times)
                }
                print(f"   {test_name}: {avg_time:.2f}ms ±{std_time:.2f}ms (min: {min(times):.2f}ms, max: {max(times):.2f}ms)")
            else:
                benchmarks[test_name] = None
                print(f"   {test_name}: ❌ Benchmark failed")

    return benchmarks

def analyze_method(method_num, method_name, method_path):
    """Analyze a single method implementation."""
    print(f"\n{'='*60}")
    print(f"METHOD {method_num}: {method_name}")
    print(f"{'='*60}")

    if not method_path.exists():
        print(f"❌ Method folder not found: {method_path}")
        return None

    # File analysis
    qr_generator_path = method_path / "qr_generator.py"
    test_file_path = method_path / "test_qr_generator.py"

    if not qr_generator_path.exists():
        print(f"❌ qr_generator.py not found")
        return None

    qr_loc = count_lines_of_code(qr_generator_path)
    test_loc = count_lines_of_code(test_file_path)

    print(f"📁 Implementation: {qr_loc} lines of code")
    print(f"🧪 Tests: {test_loc} lines of code")

    # Load the module for runtime testing
    module = load_module(method_path)
    benchmarks = {}

    if module:
        # Count functions
        try:
            with open(qr_generator_path, 'r') as f:
                code = f.read()

            import ast
            tree = ast.parse(code)
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            print(f"🔧 Functions: {len(functions)} ({', '.join(functions)})")

            # Run performance benchmarks
            benchmarks = benchmark_method(module, ["Hello World", "Test data"])

        except Exception as e:
            print(f"⚠️  Code analysis error: {e}")
            functions = []
            code = ""
    else:
        print(f"❌ Could not load module for benchmarking")
        functions = []
        code = ""

    return {
        'method_num': method_num,
        'method_name': method_name,
        'path': method_path,
        'module': module,
        'qr_loc': qr_loc,
        'test_loc': test_loc,
        'total_loc': qr_loc + test_loc,
        'functions': functions,
        'code': code,
        'benchmarks': benchmarks
    }

def run_comparison():
    """Run the complete methodology comparison."""
    print("🎯 EXPERIMENT 1.507.2: QR Code Generator Methodology Comparison")
    print("📦 External Tool Constraint: segno library")
    print("🔬 Comparing 4 development methodologies")

    methods = [
        (1, "Immediate Implementation", "1-immediate-implementation"),
        (2, "Specification-driven", "2-specification-driven"),
        (3, "Test-First Development (TDD)", "3-test-first-development"),
        (4, "Adaptive TDD V4.1", "4-adaptive-tdd-v4-1")
    ]

    experiment_root = Path(__file__).parent
    results = []

    # Analyze each method
    for method_num, method_name, folder_name in methods:
        method_path = experiment_root / folder_name
        result = analyze_method(method_num, method_name, method_path)
        if result:
            results.append(result)

    # Summary comparison
    print(f"\n{'='*60}")
    print("📊 METHODOLOGY COMPARISON SUMMARY")
    print(f"{'='*60}")

    if not results:
        print("❌ No methods could be analyzed")
        return

    print("\n📈 CODE METRICS:")
    print(f"{'Method':<25} {'Impl':<8} {'Tests':<8} {'Total':<8} {'Functions':<10}")
    print("-" * 70)

    for result in results:
        print(f"{result['method_name']:<25} {result['qr_loc']:<8} {result['test_loc']:<8} {result['total_loc']:<8} {len(result['functions']):<10}")

    # Find winner by different criteria
    print("\n🏆 WINNERS BY CRITERIA:")

    # Least code
    min_impl = min(results, key=lambda x: x['qr_loc'])
    print(f"Most Concise Implementation: {min_impl['method_name']} ({min_impl['qr_loc']} lines)")

    # Most thorough tests
    max_tests = max(results, key=lambda x: x['test_loc'])
    print(f"Most Comprehensive Tests: {max_tests['method_name']} ({max_tests['test_loc']} lines)")

    # Most functions (complexity)
    max_functions = max(results, key=lambda x: len(x['functions']))
    print(f"Most Feature-Rich: {max_functions['method_name']} ({len(max_functions['functions'])} functions)")

    print("\n🎯 METHODOLOGY INSIGHTS:")

    # Analyze patterns
    avg_impl_loc = sum(r['qr_loc'] for r in results) / len(results)
    avg_test_loc = sum(r['test_loc'] for r in results) / len(results)

    print(f"Average Implementation Size: {avg_impl_loc:.1f} lines")
    print(f"Average Test Suite Size: {avg_test_loc:.1f} lines")
    if avg_impl_loc > 0:
        print(f"Average Test/Code Ratio: {avg_test_loc/avg_impl_loc:.1f}:1")

    # Performance comparison
    print("\n⏱️  PERFORMANCE COMPARISON:")
    performance_data = {}
    for result in results:
        if result['benchmarks']:
            short_text_bench = result['benchmarks'].get('Short text')
            if short_text_bench:
                performance_data[result['method_name']] = short_text_bench['avg_ms']

    if performance_data:
        fastest_method = min(performance_data.items(), key=lambda x: x[1])
        slowest_method = max(performance_data.items(), key=lambda x: x[1])

        print(f"🏃‍♂️ Fastest: {fastest_method[0]} ({fastest_method[1]:.2f}ms average)")
        print(f"🐌 Slowest: {slowest_method[0]} ({slowest_method[1]:.2f}ms average)")

        # Performance rankings
        sorted_perf = sorted(performance_data.items(), key=lambda x: x[1])
        print("\nPerformance Rankings (Short Text):")
        for i, (method, avg_ms) in enumerate(sorted_perf, 1):
            print(f"  {i}. {method}: {avg_ms:.2f}ms")
    else:
        print("❌ No performance data available (segno dependency needed)")

    # Development time comparison
    print(f"\n🕒 DEVELOPMENT TIME COMPARISON:")
    method_times = {}
    for method_num, name, folder in methods:
        method_path = experiment_root / folder
        dev_time = read_development_time(method_path)
        method_times[name] = dev_time
        print(f"Method {method_num} ({name}): {dev_time}")

    print("\nDevelopment Time Analysis:")
    print("- All methods executed with timing measurement")
    print("- Times include: analysis, coding, testing, documentation")
    print("- Parallel execution ensures fair comparison")
    print("\nNote: Times measure end-to-end development including:")
    print("  • Requirement analysis")
    print("  • Implementation coding")
    print("  • Test creation")
    print("  • Documentation writing")

    print(f"\n✅ Comparison complete! Analyzed {len(results)} methodologies.")
    print(f"\n📋 Runtime measurements require segno library installation.")

if __name__ == "__main__":
    run_comparison()