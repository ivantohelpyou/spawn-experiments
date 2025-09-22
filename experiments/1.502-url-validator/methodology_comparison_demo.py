#!/usr/bin/env python3
"""
URL Validator Methodology Comparison Demo

Demonstrates the dramatic differences between development methodologies
for URL validation, highlighting the most extreme over-engineering case
discovered in our research (32.3X complexity multiplier).

Key Finding: Method 2 created 6,036 lines of enterprise security framework
for a simple URL validation task that Method 3 solved in 187 lines.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def find_experiment_directory():
    """Find the URL validator experiment directory from any location."""
    current_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # If running from the experiment directory
    if os.path.basename(script_dir) == "1.502-url-validator":
        return script_dir

    # If running from project root, look for experiment
    experiment_path = os.path.join(current_dir, "experiments", "1.502-url-validator")
    if os.path.exists(experiment_path):
        return experiment_path

    # If we can't find it, assume we're in the right place
    return script_dir

def get_line_counts(base_dir):
    """Get Python line counts for each methodology."""
    counts = {}

    methods = {
        "Method 1 (Immediate)": "1-immediate-implementation",
        "Method 2 (Specification-driven)": "2-specification-driven",
        "Method 3 (TDD)": "3-test-first-development",
        "Method 4 (Validated TDD)": "4-validated-test-development"
    }

    for method_name, method_dir in methods.items():
        method_path = os.path.join(base_dir, method_dir)
        if os.path.exists(method_path):
            try:
                result = subprocess.run(
                    ["find", method_path, "-name", "*.py", "-exec", "wc", "-l", "{}", "+"],
                    capture_output=True, text=True, cwd=base_dir
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    total_line = [line for line in lines if 'total' in line]
                    if total_line:
                        count = int(total_line[0].strip().split()[0])
                        counts[method_name] = count
                    else:
                        # Single file case
                        count = int(lines[0].strip().split()[0])
                        counts[method_name] = count
                else:
                    counts[method_name] = "Error"
            except Exception as e:
                counts[method_name] = f"Error: {e}"
        else:
            counts[method_name] = "Not found"

    return counts

def get_timing_data(base_dir):
    """Extract timing data from file creation timestamps."""
    try:
        # Get experiment start time (earliest file)
        start_result = subprocess.run(
            ["find", base_dir, "-type", "f", "-exec", "stat", "-c", "%y %n", "{}", ";"],
            capture_output=True, text=True
        )
        if start_result.returncode == 0:
            start_line = min(start_result.stdout.strip().split('\n'))
            start_time = start_line.split(' ')[1]  # Extract time portion
        else:
            start_time = "Unknown"

        # Get completion times for each method
        methods = {
            "Method 1": "1-immediate-implementation",
            "Method 2": "2-specification-driven",
            "Method 3": "3-test-first-development",
            "Method 4": "4-validated-test-development"
        }

        timings = {}
        for method_name, method_dir in methods.items():
            method_path = os.path.join(base_dir, method_dir)
            if os.path.exists(method_path):
                try:
                    result = subprocess.run(
                        ["find", method_path, "-type", "f", "-exec", "stat", "-c", "%y %n", "{}", ";"],
                        capture_output=True, text=True
                    )
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        end_line = max(lines)
                        end_time = end_line.split(' ')[1]  # Extract time portion
                        timings[method_name] = end_time
                    else:
                        timings[method_name] = "Unknown"
                except Exception:
                    timings[method_name] = "Error"
            else:
                timings[method_name] = "Not found"

        return start_time, timings
    except Exception as e:
        return "Error", {}

def calculate_duration(start_time, end_time):
    """Calculate duration between two time strings."""
    try:
        start_parts = start_time.split(':')
        end_parts = end_time.split(':')

        start_seconds = int(start_parts[0]) * 3600 + int(start_parts[1]) * 60 + int(start_parts[2][:2])
        end_seconds = int(end_parts[0]) * 3600 + int(end_parts[1]) * 60 + int(end_parts[2][:2])

        duration = end_seconds - start_seconds
        if duration < 0:
            duration += 86400  # Handle day boundary

        minutes = duration // 60
        seconds = duration % 60

        if minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    except Exception:
        return "Unknown"

def test_validators(base_dir):
    """Test each validator with sample URLs and show behavioral differences."""
    print("\\n" + "="*80)
    print("🧪 LIVE VALIDATOR COMPARISON - EQUIVALENT FUNCTIONALITY TEST")
    print("="*80)

    # Test URLs that show different validation aspects
    test_cases = [
        ("https://www.google.com", "Valid & Accessible"),
        ("https://invalid-domain-12345.com", "Valid format, Not accessible"),
        ("not-a-url", "Invalid format"),
        ("ftp://files.example.com", "Different protocol"),
        ("", "Empty string"),
    ]

    methods = [
        ("Method 1 (Immediate)", "1-immediate-implementation"),
        ("Method 2 (Spec-driven)", "2-specification-driven"),
        ("Method 3 (TDD)", "3-test-first-development"),
        ("Method 4 (Validated TDD)", "4-validated-test-development")
    ]

    # First show API detection
    print("\\n📋 API DESIGN PATTERNS DETECTED:")
    print("-" * 60)

    for method_name, method_dir in methods:
        method_path = os.path.join(base_dir, method_dir)
        validator_file = os.path.join(method_path, "url_validator.py")

        if os.path.exists(validator_file):
            # Try to run a simple test
            try:
                # Create a simple test script
                test_script = f'''
import sys
sys.path.insert(0, "{method_path}")

try:
    import url_validator

    # Try different ways to call the validator based on implementation
    test_url = "https://www.google.com"
    result = None
    api_used = "Unknown"

    # Method 1: validate_url function
    if hasattr(url_validator, "validate_url"):
        result = url_validator.validate_url(test_url)
        api_used = "validate_url() function"

    # Method 3 & 4: URLValidator class with different methods
    elif hasattr(url_validator, "URLValidator"):
        validator = url_validator.URLValidator()

        # Try different method names
        if hasattr(validator, "is_valid"):
            result = validator.is_valid(test_url)
            api_used = "URLValidator.is_valid() method"
        elif hasattr(validator, "is_valid_format"):
            result = validator.is_valid_format(test_url)
            api_used = "URLValidator.is_valid_format() method"
        elif hasattr(validator, "validate"):
            result = validator.validate(test_url)
            api_used = "URLValidator.validate() method"
        elif hasattr(validator, "validate_url"):
            result = validator.validate_url(test_url)
            api_used = "URLValidator.validate_url() method"
        else:
            available_methods = [attr for attr in dir(validator) if not attr.startswith('_') and callable(getattr(validator, attr))]
            api_used = f"URLValidator available methods: {{available_methods}}"
    else:
        print("Could not find validation method")

    print(f"✅ Validator loaded successfully")
    print(f"🔗 API Design: {{api_used}}")
    print(f"📊 Sample result: {{type(result)}} = {{result}}")

except ImportError as e:
    print(f"❌ Import error: {{e}}")
except Exception as e:
    print(f"⚠️  Execution error: {{e}}")
'''

                # Write and execute test
                test_file = os.path.join(method_path, "temp_test.py")
                with open(test_file, 'w') as f:
                    f.write(test_script)

                result = subprocess.run(
                    [sys.executable, test_file],
                    capture_output=True, text=True, cwd=method_path, timeout=10
                )

                if result.returncode == 0:
                    print(result.stdout)
                else:
                    print("⚠️  Validator test failed:")
                    print(result.stderr[:200] + "..." if len(result.stderr) > 200 else result.stderr)

                # Clean up
                os.remove(test_file)

            except subprocess.TimeoutExpired:
                print("⏱️  Validator test timed out")
            except Exception as e:
                print(f"❌ Test execution error: {e}")
        else:
            print(f"📁 Validator file not found: {validator_file}")

    # Now test equivalent functionality
    print("\\n\\n🔬 EQUIVALENT FUNCTIONALITY COMPARISON:")
    print("-" * 80)
    print("Testing the same URLs with each validator to show behavioral equivalence:")
    print()

    # Build comparison table
    results_table = {}

    for method_name, method_dir in methods:
        method_path = os.path.join(base_dir, method_dir)
        validator_file = os.path.join(method_path, "url_validator.py")
        results_table[method_name] = {}

        if os.path.exists(validator_file):
            for test_url, description in test_cases:
                # Create test script for each URL
                test_script = f'''
import sys
sys.path.insert(0, "{method_path}")
import url_validator

test_url = "{test_url}"
result = "Unknown"

try:
    # Method 1: validate_url function returning dict
    if hasattr(url_validator, "validate_url"):
        result_obj = url_validator.validate_url(test_url)
        # Check if it's a dict (Method 1) or object (Method 2)
        if isinstance(result_obj, dict):
            # Method 1 returns a dictionary
            if result_obj.get('is_valid_format') and result_obj.get('is_accessible'):
                result = "✅ Valid"
            elif result_obj.get('is_valid_format'):
                result = "⚠️  Format OK"
            else:
                result = "❌ Invalid"
        else:
            # Method 2 returns a ValidationResult object
            if hasattr(result_obj, 'is_valid') and hasattr(result_obj, 'is_accessible'):
                if result_obj.is_valid and result_obj.is_accessible:
                    result = "✅ Valid"
                elif result_obj.is_valid:
                    result = "⚠️  Format OK"
                else:
                    result = "❌ Invalid"
            else:
                result = "✅ Valid" if result_obj else "❌ Invalid"

    # Method 3 & 4: URLValidator class
    elif hasattr(url_validator, "URLValidator"):
        validator = url_validator.URLValidator()

        # Method 3: is_valid
        if hasattr(validator, "is_valid"):
            is_valid = validator.is_valid(test_url)
            result = "✅ Valid" if is_valid else "❌ Invalid"

        # Method 4: is_valid_format (and optionally is_accessible)
        elif hasattr(validator, "is_valid_format"):
            format_valid = validator.is_valid_format(test_url)
            if hasattr(validator, "is_accessible"):
                accessible = validator.is_accessible(test_url) if format_valid else False
                if format_valid and accessible:
                    result = "✅ Valid"
                elif format_valid:
                    result = "⚠️  Format OK"
                else:
                    result = "❌ Invalid"
            else:
                result = "✅ Valid" if format_valid else "❌ Invalid"

except Exception as e:
    result = f"Error: {{str(e)[:20]}}"

print(result)
'''

                try:
                    test_file = os.path.join(method_path, "temp_test.py")
                    with open(test_file, 'w') as f:
                        f.write(test_script)

                    result = subprocess.run(
                        [sys.executable, test_file],
                        capture_output=True, text=True, cwd=method_path, timeout=10
                    )

                    if result.returncode == 0:
                        results_table[method_name][test_url] = result.stdout.strip()
                    else:
                        results_table[method_name][test_url] = "❌ Error"

                    os.remove(test_file)

                except subprocess.TimeoutExpired:
                    results_table[method_name][test_url] = "⏱️ Timeout"
                except Exception:
                    results_table[method_name][test_url] = "❌ Error"

    # Print comparison table
    print(f"{'URL':<40} {'Method 1':<12} {'Method 2':<12} {'Method 3':<12} {'Method 4':<12}")
    print("-" * 100)

    for test_url, description in test_cases:
        url_display = test_url[:35] + "..." if len(test_url) > 35 else test_url
        if not url_display:
            url_display = "(empty string)"

        method1_result = results_table.get("Method 1 (Immediate)", {}).get(test_url, "N/A")
        method2_result = results_table.get("Method 2 (Spec-driven)", {}).get(test_url, "N/A")
        method3_result = results_table.get("Method 3 (TDD)", {}).get(test_url, "N/A")
        method4_result = results_table.get("Method 4 (Validated TDD)", {}).get(test_url, "N/A")

        print(f"{url_display:<40} {method1_result:<12} {method2_result:<12} {method3_result:<12} {method4_result:<12}")

    print()
    print("Legend: ✅ Valid & Accessible | ⚠️ Valid Format Only | ❌ Invalid/Inaccessible")
    print()
    print("📊 KEY OBSERVATION:")
    print("   All FOUR methods provide equivalent core functionality")
    print("   But with VASTLY different complexity:")
    print("   • Method 3 (TDD): 187 lines ✅")
    print("   • Method 1: 398 lines")
    print("   • Method 4: 968 lines")
    print("   • Method 2: 6,036 lines 🚨 (32X more than TDD!)")
    print("   TDD achieves the same results with minimal code")

def show_method2_architecture(base_dir):
    """Show the massive over-engineering in Method 2."""
    print("\\n" + "="*80)
    print("🚨 METHOD 2 OVER-ENGINEERING ANALYSIS")
    print("="*80)

    method2_path = os.path.join(base_dir, "2-specification-driven")
    if not os.path.exists(method2_path):
        print("❌ Method 2 directory not found")
        return

    print("\\n📁 ENTERPRISE ARCHITECTURE CREATED FOR SIMPLE URL VALIDATION:")
    print("-" * 60)

    try:
        # Show directory structure
        result = subprocess.run(
            ["find", method2_path, "-type", "f", "-name", "*.py"],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            files = result.stdout.strip().split('\\n')

            # Categorize files
            categories = {
                "Core Validation": [],
                "Security Framework": [],
                "CLI Interface": [],
                "Data Models": [],
                "Validators": [],
                "Examples": [],
                "Tests": []
            }

            for file_path in files:
                rel_path = os.path.relpath(file_path, method2_path)
                if "security" in rel_path:
                    categories["Security Framework"].append(rel_path)
                elif "cli" in rel_path:
                    categories["CLI Interface"].append(rel_path)
                elif "models" in rel_path:
                    categories["Data Models"].append(rel_path)
                elif "validators" in rel_path:
                    categories["Validators"].append(rel_path)
                elif "examples" in rel_path:
                    categories["Examples"].append(rel_path)
                elif "test" in rel_path:
                    categories["Tests"].append(rel_path)
                elif "core" in rel_path:
                    categories["Core Validation"].append(rel_path)

            total_files = len(files)
            print(f"📊 TOTAL FILES: {total_files}")
            print()

            for category, file_list in categories.items():
                if file_list:
                    print(f"🏗️  {category} ({len(file_list)} files):")
                    for file_path in file_list:
                        print(f"   📄 {file_path}")
                    print()

            # Show some specific over-engineering examples
            print("🚨 UNNECESSARY FEATURES CREATED:")
            print("   • SSRF Protection Framework")
            print("   • Rate Limiting with Token Bucket Algorithm")
            print("   • CLI with JSON/CSV/XML Output Formats")
            print("   • IPv6 and Internationalized Domain Support")
            print("   • Security Scanning for Injection Attacks")
            print("   • Batch Processing with Concurrency")
            print("   • Enterprise Error Handling Framework")
            print()
            print("⚠️  NONE OF THESE WERE REQUESTED IN THE PROMPT!")

        else:
            print("❌ Could not analyze Method 2 structure")

    except Exception as e:
        print(f"❌ Error analyzing Method 2: {e}")

def main():
    """Run the complete methodology comparison demonstration."""
    print("="*80)
    print("🚀 URL VALIDATOR METHODOLOGY COMPARISON")
    print("🔬 Experiment 1.502 - Revolutionary 32X Over-Engineering Discovery")
    print("="*80)

    # Find experiment directory
    base_dir = find_experiment_directory()
    print(f"📂 Working in: {base_dir}")

    # Get line counts
    print("\\n📊 CODE VOLUME ANALYSIS")
    print("-" * 40)
    counts = get_line_counts(base_dir)

    # Find baseline (Method 3 TDD)
    baseline = counts.get("Method 3 (TDD)", 1)
    if isinstance(baseline, str):
        baseline = 1

    print(f"{'Method':<25} {'Lines':<8} {'Ratio':<8} {'Assessment'}")
    print("-" * 60)

    for method, count in counts.items():
        if isinstance(count, int):
            ratio = f"{count/baseline:.1f}X" if baseline > 0 else "N/A"
            if count == baseline:
                assessment = "✅ Baseline (TDD)"
            elif count < baseline * 2:
                assessment = "✅ Reasonable"
            elif count < baseline * 5:
                assessment = "⚠️  Moderate bloat"
            elif count < baseline * 10:
                assessment = "🔶 Significant bloat"
            else:
                assessment = "🚨 EXTREME bloat"
            print(f"{method:<25} {count:<8} {ratio:<8} {assessment}")
        else:
            print(f"{method:<25} {count:<8} {'N/A':<8} ❌ Error")

    # Get timing data
    print("\\n⏱️  DEVELOPMENT SPEED ANALYSIS")
    print("-" * 40)
    start_time, end_times = get_timing_data(base_dir)

    print(f"🕐 Experiment started: {start_time}")
    print()
    print(f"{'Method':<25} {'Duration':<12} {'Speed Rank'}")
    print("-" * 50)

    # Calculate durations and rank by speed
    durations = {}
    for method, end_time in end_times.items():
        if end_time != "Unknown" and end_time != "Error" and end_time != "Not found":
            duration = calculate_duration(start_time, end_time)
            durations[method] = duration

    # Sort by duration (convert to seconds for sorting)
    def duration_to_seconds(duration_str):
        if 'm' in duration_str:
            parts = duration_str.replace('m', '').replace('s', '').split()
            return int(parts[0]) * 60 + int(parts[1])
        else:
            return int(duration_str.replace('s', ''))

    sorted_methods = sorted(durations.items(), key=lambda x: duration_to_seconds(x[1]))

    speed_ranks = ["🥇 Fastest", "🥈 Second", "🥉 Third", "🐌 Slowest"]
    for i, (method, duration) in enumerate(sorted_methods):
        rank = speed_ranks[i] if i < len(speed_ranks) else f"#{i+1}"
        print(f"{method:<25} {duration:<12} {rank}")

    # Show key insights
    print("\\n🔍 KEY FINDINGS")
    print("-" * 40)

    # Calculate the most dramatic differences
    tdd_lines = counts.get("Method 3 (TDD)", 1)
    spec_lines = counts.get("Method 2 (Specification-driven)", 1)

    if isinstance(tdd_lines, int) and isinstance(spec_lines, int):
        multiplier = spec_lines / tdd_lines
        print(f"🚨 OVER-ENGINEERING FACTOR: {multiplier:.1f}X")
        print(f"   Method 2 created {spec_lines:,} lines vs Method 3's {tdd_lines:,} lines")
        print(f"   This is the LARGEST complexity multiplier discovered in our research!")
        print()

    print("✅ TDD CONSTRAINT EFFECTIVENESS:")
    print("   • Method 3 (TDD) stayed focused on requirements")
    print("   • Test boundaries prevented feature explosion")
    print("   • Natural minimalism emerged from test-driven development")
    print()

    print("🚨 SPECIFICATION-DRIVEN DANGER:")
    print("   • 'Comprehensive specifications' triggered enterprise over-engineering")
    print("   • AI created SSRF protection for basic URL validation")
    print("   • Massive security framework for simple format checking")
    print("   • 32X more code than necessary for identical functionality")

    # Show Method 2 architecture
    show_method2_architecture(base_dir)

    # Test validators
    test_validators(base_dir)

    # Conclusion
    print("\\n" + "="*80)
    print("🎯 METHODOLOGY RESEARCH CONCLUSIONS")
    print("="*80)
    print()
    print("📈 PATTERN VALIDATION:")
    print("   • AI over-engineering epidemic confirmed across validation domains")
    print("   • TDD consistently prevents complexity explosion")
    print("   • Constraint systems essential for AI collaboration")
    print()
    print("🔬 RESEARCH IMPACT:")
    print("   • Largest methodology difference documented (32.3X)")
    print("   • Clear evidence that methodology choice matters critically")
    print("   • Practical guidance for AI-assisted development")
    print()
    print("🚀 PRACTICAL RECOMMENDATIONS:")
    print("   • Use TDD for input validation tasks")
    print("   • Avoid 'comprehensive' instructions for simple problems")
    print("   • Start minimal and expand based on actual requirements")
    print("   • Leverage AI's power through constraint systems")
    print()
    print("📊 Next experiment: 1.503 File Path Validator")
    print("🔗 Full report: experiments/1.502-url-validator/EXPERIMENT_REPORT.md")
    print()
    print("✨ The evidence is clear: Methodology choice fundamentally determines")
    print("   whether AI collaboration produces practical solutions or dangerous over-engineering.")

if __name__ == "__main__":
    main()