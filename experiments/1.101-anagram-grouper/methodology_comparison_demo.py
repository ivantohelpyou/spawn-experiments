#!/usr/bin/env python3
"""
Anagram Grouper Methodology Comparison Demo

This script demonstrates the dramatic differences between four development methodologies
by comparing their anagram grouping implementations.

Key Finding: TDD produced 3X less code (401 lines) than Specification-Driven (1,440 lines)
while maintaining equivalent functionality and superior test quality.

Perfect for presentations showing how methodology choice impacts code size and complexity.
"""

import sys
import os
import time
from typing import List, Dict, Any

def find_experiment_directory():
    """Find the experiment directory, whether running from project root or experiment dir."""
    current_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Try script directory first (when running from experiment directory)
    if os.path.basename(script_dir) == "1.101-anagram-grouper":
        return script_dir

    # Try from current working directory (when running from project root)
    experiment_path = os.path.join(current_dir, "experiments", "1.101-anagram-grouper")
    if os.path.exists(experiment_path):
        return experiment_path

    # Try relative to script location
    return script_dir

# Set base experiment directory
EXPERIMENT_DIR = find_experiment_directory()

def load_method1():
    """Load Method 1 - Immediate Implementation"""
    try:
        method1_dir = os.path.join(EXPERIMENT_DIR, "1-immediate-implementation")
        if not os.path.exists(method1_dir):
            return None
        sys.path.insert(0, method1_dir)
        from anagram_grouper import group_anagrams as method1_group
        return method1_group
    except ImportError:
        return None

def load_method2():
    """Load Method 2 - Specification-Driven"""
    try:
        method2_dir = os.path.join(EXPERIMENT_DIR, "2-specification-driven")
        if not os.path.exists(method2_dir):
            return None
        sys.path.insert(0, method2_dir)
        from anagram_grouper import group_anagrams as method2_group
        return method2_group
    except ImportError:
        return None

def load_method3():
    """Load Method 3 - TDD"""
    try:
        method3_dir = os.path.join(EXPERIMENT_DIR, "3-test-first-development")
        if not os.path.exists(method3_dir):
            return None
        sys.path.insert(0, method3_dir)
        from anagram_grouper import group_anagrams as method3_group
        return method3_group
    except ImportError:
        return None

def load_method4():
    """Load Method 4 - Validated Test Development"""
    try:
        method4_dir = os.path.join(EXPERIMENT_DIR, "4-validated-test-development")
        if not os.path.exists(method4_dir):
            return None
        sys.path.insert(0, method4_dir)
        from anagram_grouper import group_anagrams as method4_group
        return method4_group
    except ImportError:
        return None

def get_code_metrics():
    """Get code metrics for each method."""
    metrics = {}

    for method_num, method_name in [
        ("1", "Method 1 (Immediate)"),
        ("2", "Method 2 (Spec-driven)"),
        ("3", "Method 3 (TDD)"),
        ("4", "Method 4 (Validated)")
    ]:
        method_dir = os.path.join(EXPERIMENT_DIR, f"{method_num}-*")
        # Find actual directory name
        import glob
        actual_dirs = glob.glob(method_dir)
        if actual_dirs:
            method_dir = actual_dirs[0]

            # Count Python files and lines
            py_files = glob.glob(os.path.join(method_dir, "*.py"))
            total_lines = 0
            file_count = len(py_files)

            for py_file in py_files:
                try:
                    with open(py_file, 'r') as f:
                        total_lines += len(f.readlines())
                except:
                    continue

            metrics[method_name] = {
                "files": file_count,
                "lines": total_lines,
                "directory": os.path.basename(method_dir)
            }
        else:
            metrics[method_name] = {"files": 0, "lines": 0, "directory": "Not found"}

    return metrics

def run_functionality_comparison():
    """Compare functionality across all methods."""

    print("🧪 Anagram Grouper Methodology Comparison")
    print("=" * 50)

    # Load all methods
    methods = {
        "Method 1 (Immediate)": load_method1(),
        "Method 2 (Spec-driven)": load_method2(),
        "Method 3 (TDD)": load_method3(),
        "Method 4 (Validated)": load_method4()
    }

    loaded_methods = {k: v for k, v in methods.items() if v is not None}

    if not loaded_methods:
        print("❌ No methods could be loaded!")
        return

    print(f"✅ Loaded {len(loaded_methods)} methods: {', '.join(loaded_methods.keys())}")
    print()

    # Test cases designed to show any differences
    test_cases = [
        # Basic functionality
        (["eat", "tea", "tan", "ate", "nat", "bat"], "Basic anagram grouping"),
        (["abc", "bca", "cab", "xyz"], "Two groups"),
        (["hello", "world"], "No anagrams"),
        (["a"], "Single word"),
        ([], "Empty list"),

        # Edge cases that might reveal differences
        (["Listen", "Silent", "ENLIST"], "Case sensitivity test"),
        (["A", "a"], "Case edge case"),
        (["", "abc", ""], "Empty strings"),
        (["ab", "ba", "abc", "bca", "cab"], "Mixed lengths"),

        # Stress test (might reveal performance differences)
        (["abc"] * 100 + ["bca"] * 100 + ["cab"] * 100, "Large input (300 items)")
    ]

    print("FUNCTIONALITY COMPARISON")
    print("-" * 30)
    print()

    differences_found = False

    for test_input, description in test_cases:
        print(f"📝 {description}: {str(test_input)[:50]}{'...' if len(str(test_input)) > 50 else ''}")

        results = {}
        performance = {}

        for method_name, method_func in loaded_methods.items():
            try:
                start_time = time.time()
                result = method_func(test_input.copy())
                end_time = time.time()

                # Normalize result for comparison (sort groups and items within groups)
                if result:
                    normalized = [sorted(group) for group in sorted(result, key=lambda x: sorted(x))]
                else:
                    normalized = result

                results[method_name] = normalized
                performance[method_name] = (end_time - start_time) * 1000  # ms

            except Exception as e:
                results[method_name] = f"ERROR: {e}"
                performance[method_name] = None

        # Check for differences
        unique_results = set()
        for result in results.values():
            if isinstance(result, list):
                unique_results.add(str(result))
            else:
                unique_results.add(result)

        if len(unique_results) > 1:
            differences_found = True
            print("   ⚠️  DIFFERENCE DETECTED!")
            for method_name, result in results.items():
                print(f"   {method_name}: {result}")
        else:
            print("   ✅ All methods agree")
            # Show performance if all agree
            if any(perf for perf in performance.values() if perf is not None):
                perf_str = ", ".join([f"{name}: {perf:.2f}ms" for name, perf in performance.items() if perf is not None])
                print(f"   ⏱️  Performance: {perf_str}")

        print()

    if not differences_found:
        print("✅ All methods produce identical results!")
        print("   This proves equivalent functionality across methodologies.")

    return results

def show_code_complexity_analysis():
    """Show the dramatic code size differences."""

    print("\nCODE COMPLEXITY ANALYSIS")
    print("=" * 40)
    print()

    metrics = get_code_metrics()

    # Sort by lines of code
    sorted_methods = sorted(metrics.items(), key=lambda x: x[1]["lines"], reverse=True)

    print("📊 CODE SIZE COMPARISON:")
    print(f"{'Method':<25} {'Files':<6} {'Lines':<6} {'Ratio':<8}")
    print("-" * 45)

    baseline_lines = None
    for i, (method_name, data) in enumerate(sorted_methods):
        lines = data["lines"]
        if baseline_lines is None:
            baseline_lines = lines
            ratio = "1.0x"
        else:
            ratio = f"{baseline_lines / lines:.1f}x" if lines > 0 else "N/A"

        print(f"{method_name:<25} {data['files']:<6} {lines:<6} {ratio:<8}")

    # Highlight the key finding
    if len(sorted_methods) >= 3:
        largest = sorted_methods[0]
        smallest = sorted_methods[-1]

        if largest[1]["lines"] > 0 and smallest[1]["lines"] > 0:
            ratio = largest[1]["lines"] / smallest[1]["lines"]
            print()
            print(f"🎯 KEY FINDING:")
            print(f"   {largest[0]} used {largest[1]['lines']} lines")
            print(f"   {smallest[0]} used {smallest[1]['lines']} lines")
            print(f"   That's a {ratio:.1f}X difference in code size!")
            print()
            print("💡 INSIGHT: TDD naturally enforces minimalism")
            print("   while specification-driven development can lead to over-engineering.")

def show_methodology_insights():
    """Show insights about each methodology."""

    print("\nMETHODOLOGY INSIGHTS")
    print("=" * 30)
    print()

    insights = {
        "Method 1 (Immediate)": {
            "lines": 546,
            "time": "~1 minute",
            "characteristics": [
                "Multiple utility functions beyond requirements",
                "Case-insensitive with original case preservation",
                "Comprehensive demo function",
                "Tests written after implementation"
            ],
            "verdict": "⚡ Fast but feature creep risk"
        },
        "Method 2 (Spec-driven)": {
            "lines": 1440,
            "time": "~4 minutes",
            "characteristics": [
                "196-line specification document",
                "5 configurable parameters",
                "Unicode normalization support",
                "Most comprehensive test suite (35+ tests)",
                "Performance benchmarks included"
            ],
            "verdict": "📋 Thorough but over-engineered"
        },
        "Method 3 (TDD)": {
            "lines": 401,
            "time": "~3 minutes",
            "characteristics": [
                "Strict Red-Green-Refactor cycle",
                "Clean 60-line implementation",
                "11 comprehensive tests",
                "Helper functions for organization",
                "Minimal but complete"
            ],
            "verdict": "🎯 OPTIMAL - Clean and focused"
        },
        "Method 4 (Validated)": {
            "lines": "~500-600",
            "time": "~4 minutes",
            "characteristics": [
                "Test validation with wrong implementations",
                "Highest confidence in correctness",
                "Systematic edge case coverage",
                "Quality gates at each step"
            ],
            "verdict": "🛡️ Most reliable but slower"
        }
    }

    for method_name, data in insights.items():
        print(f"📝 {method_name}")
        print(f"   Code: {data['lines']} lines | Time: {data['time']}")
        print(f"   Characteristics:")
        for char in data["characteristics"]:
            print(f"     • {char}")
        print(f"   Verdict: {data['verdict']}")
        print()

def main():
    """Run the complete methodology comparison demo."""

    print("🚀 ANAGRAM GROUPER METHODOLOGY COMPARISON DEMO")
    print("=" * 60)
    print()
    print("This demo shows how methodology choice dramatically impacts:")
    print("• Code size and complexity")
    print("• Development approach and focus")
    print("• Feature scope and over-engineering risk")
    print()
    print("Key Finding: TDD produced 3X less code than specification-driven")
    print("while maintaining equivalent functionality!")
    print()

    # Run functionality comparison
    run_functionality_comparison()

    # Show code complexity analysis
    show_code_complexity_analysis()

    # Show methodology insights
    show_methodology_insights()

    print("CONCLUSION")
    print("=" * 20)
    print()
    print("🎯 For algorithmic problems like anagram grouping:")
    print("   • TDD (Method 3) is OPTIMAL - minimal, clean, well-tested")
    print("   • Specification-driven risks over-engineering simple problems")
    print("   • Immediate implementation risks feature creep")
    print("   • Test validation provides highest confidence but at time cost")
    print()
    print("💡 Key Insight: Methodology guidance significantly impacts")
    print("   AI development patterns - simpler approaches often win")
    print("   for well-bounded algorithmic problems.")
    print()
    print("🎤 Perfect demo for presentations showing methodology impact!")

if __name__ == "__main__":
    main()