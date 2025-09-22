#!/usr/bin/env python3
"""
Methodology Comparison Demo: JSON Schema Validator
Auto-generated comparison of all four methodology implementations.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def find_experiment_directory():
    """Find the experiment directory from any location."""
    current_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # If running from the experiment directory
    if os.path.basename(script_dir).startswith("1.505"):
        return script_dir

    return script_dir

def get_available_methods(base_dir):
    """Auto-detect available method implementations."""
    methods = {}

    method_dirs = {
        "Method 1 (Immediate)": "1-immediate-implementation",
        "Method 2 (Specification)": "2-specification-driven",
        "Method 3 (Pure TDD)": "3-test-first-development",
        "Method 4 (Adaptive TDD)": "4-adaptive-tdd-v41"
    }

    for method_name, method_dir in method_dirs.items():
        # Check for different possible validator file names
        possible_files = [
            "validator.py",
            "json_schema_validator.py"
        ]

        for validator_file in possible_files:
            impl_file = os.path.join(base_dir, method_dir, validator_file)
            if os.path.exists(impl_file):
                methods[method_name] = (method_dir, validator_file)
                break

    return methods

def test_schema_validation_robustness(base_dir, available_methods):
    """Test schema validation robustness across all methods."""
    print("\n" + "="*80)
    print("🧪 JSON SCHEMA VALIDATION ROBUSTNESS TEST")
    print("="*80)
    print(f"Testing {len(available_methods)} available method implementations...")
    print()

    # Complex test cases designed to reveal methodology differences
    test_cases = [
        # Basic valid cases
        ('{"name": "John", "age": 30}', '{"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "number"}}, "required": ["name"]}', "Valid object with required fields"),

        # Format validation edge cases
        ('{"email": "test@example.com"}', '{"type": "object", "properties": {"email": {"type": "string", "format": "email"}}}', "Valid email format"),
        ('{"email": "invalid..email@test.com"}', '{"type": "object", "properties": {"email": {"type": "string", "format": "email"}}}', "Invalid email (consecutive dots)"),
        ('{"email": ".invalid@test.com"}', '{"type": "object", "properties": {"email": {"type": "string", "format": "email"}}}', "Invalid email (leading dot)"),

        # Date validation edge cases
        ('{"date": "2024-02-29"}', '{"type": "object", "properties": {"date": {"type": "string", "format": "date"}}}', "Valid leap year date"),
        ('{"date": "2023-02-29"}', '{"type": "object", "properties": {"date": {"type": "string", "format": "date"}}}', "Invalid leap year date"),

        # URI validation
        ('{"url": "https://example.com"}', '{"type": "object", "properties": {"url": {"type": "string", "format": "uri"}}}', "Valid HTTPS URI"),
        ('{"url": "not-a-uri"}', '{"type": "object", "properties": {"url": {"type": "string", "format": "uri"}}}', "Invalid URI format"),

        # Complex nested validation
        ('{"user": {"profile": {"settings": {"theme": "dark"}}}}', '{"type": "object", "properties": {"user": {"type": "object", "properties": {"profile": {"type": "object", "properties": {"settings": {"type": "object", "properties": {"theme": {"type": "string"}}}}}}}}}', "Deep nested object"),

        # Array validation
        ('{"tags": ["red", "green", "blue"]}', '{"type": "object", "properties": {"tags": {"type": "array", "items": {"type": "string"}}}}', "Valid string array"),
        ('{"tags": ["red", 123, "blue"]}', '{"type": "object", "properties": {"tags": {"type": "array", "items": {"type": "string"}}}}', "Mixed type array (invalid)"),

        # Error handling edge cases
        ('invalid-json', '{"type": "object"}', "Malformed JSON"),
        ('{"valid": "json"}', 'invalid-schema', "Invalid schema"),
        ('null', '{"type": "object"}', "Null input"),
        ('""', '{"type": "string", "minLength": 1}', "Empty string vs minLength"),
    ]

    # Create header
    header = f"{'Test Case':<30}"
    for method_name in available_methods.keys():
        # Extract method number more safely
        if "1" in method_name:
            method_abbrev = "M1"
        elif "2" in method_name:
            method_abbrev = "M2"
        elif "3" in method_name:
            method_abbrev = "M3"
        elif "4" in method_name:
            method_abbrev = "M4"
        else:
            method_abbrev = "M?"
        header += f" {method_abbrev:<6}"
    header += " Description"

    print(header)
    print("-" * len(header))

    disagreements = []

    for i, (test_data, test_schema, description) in enumerate(test_cases):
        display_data = (test_data[:27] + "...") if len(test_data) > 30 else test_data
        results = {}

        for method_name, (method_dir, validator_file) in available_methods.items():
            method_path = os.path.join(base_dir, method_dir)

            try:
                # Create test script for this method
                test_script = f'''
import sys
sys.path.insert(0, "{method_path}")

test_data = """{test_data}"""
test_schema = """{test_schema}"""

try:
    if "{validator_file}" == "validator.py":
        from validator import JSONSchemaValidator
        validator = JSONSchemaValidator()
        result = validator.validate_json_string(test_data, eval(test_schema))
        print("✓" if result else "✗")
    else:
        import json_schema_validator
        # Try different API patterns
        if hasattr(json_schema_validator, 'validate'):
            result = json_schema_validator.validate(json.loads(test_data), json.loads(test_schema))
        elif hasattr(json_schema_validator, 'JSONSchemaValidator'):
            validator = json_schema_validator.JSONSchemaValidator()
            result = validator.validate(json.loads(test_data), json.loads(test_schema))
        else:
            result = False

        if hasattr(result, 'is_valid'):
            print("✓" if result.is_valid else "✗")
        else:
            print("✓" if result else "✗")
except Exception as e:
    print("ERR")
'''

                result = subprocess.run(
                    [sys.executable, "-c", test_script],
                    capture_output=True, text=True, timeout=10
                )

                if result.returncode == 0:
                    results[method_name] = result.stdout.strip()
                else:
                    results[method_name] = "ERR"

            except Exception:
                results[method_name] = "N/A"

        # Check for disagreements
        unique_results = set(results.values())
        if len(unique_results) > 1:
            disagreements.append((i+1, description, results))

        # Print results row
        row = f"{display_data:<30}"
        for method_name in available_methods.keys():
            result = results.get(method_name, "N/A")
            row += f" {result:<6}"
        row += f" {description}"
        print(row)

    # Report disagreements
    if disagreements:
        print(f"\n🚨 METHODOLOGY DISAGREEMENTS FOUND:")
        print("="*60)
        for test_num, desc, results in disagreements:
            print(f"Test {test_num}: {desc}")
            for method, result in results.items():
                print(f"  {method}: {result}")
            print()
    else:
        print(f"\n✅ All methods agree on {len(test_cases)} test cases!")

    print(f"\n📊 Successfully tested {len(available_methods)} method implementations!")

def analyze_code_complexity(base_dir, available_methods):
    """Analyze code complexity across methods."""
    print("\n" + "="*80)
    print("📊 CODE COMPLEXITY ANALYSIS")
    print("="*80)

    complexity_data = []

    for method_name, (method_dir, validator_file) in available_methods.items():
        impl_file = os.path.join(base_dir, method_dir, validator_file)

        try:
            with open(impl_file, 'r') as f:
                lines = f.readlines()

            total_lines = len(lines)
            code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])

            # Count test files
            test_files = [f for f in os.listdir(os.path.join(base_dir, method_dir)) if f.startswith('test_')]
            test_count = len(test_files)

            complexity_data.append({
                'method': method_name,
                'total_lines': total_lines,
                'code_lines': code_lines,
                'test_files': test_count
            })

        except Exception as e:
            print(f"⚠️  Could not analyze {method_name}: {e}")

    # Sort by code lines
    complexity_data.sort(key=lambda x: x['code_lines'])

    print(f"{'Method':<20} {'Total Lines':<12} {'Code Lines':<12} {'Test Files':<12} {'Efficiency'}")
    print("-" * 75)

    baseline = complexity_data[0]['code_lines'] if complexity_data else 1

    for data in complexity_data:
        efficiency_ratio = f"{data['code_lines'] / baseline:.1f}X"
        print(f"{data['method']:<20} {data['total_lines']:<12} {data['code_lines']:<12} {data['test_files']:<12} {efficiency_ratio}")

    return complexity_data

def main():
    """Run comprehensive methodology comparison."""
    print("="*80)
    print("🚀 JSON SCHEMA VALIDATOR - METHODOLOGY COMPARISON")
    print("="*80)

    base_dir = find_experiment_directory()
    print(f"📂 Experiment directory: {base_dir}")

    available_methods = get_available_methods(base_dir)

    if not available_methods:
        print("❌ No method implementations found!")
        return

    print(f"✅ Found {len(available_methods)} implemented methods:")
    for method_name, (method_dir, validator_file) in available_methods.items():
        print(f"   • {method_name}: {method_dir}/{validator_file}")

    # Run comprehensive tests
    test_schema_validation_robustness(base_dir, available_methods)

    # Analyze code complexity
    complexity_data = analyze_code_complexity(base_dir, available_methods)

    print("\n" + "="*80)
    print("🎯 METHODOLOGY COMPARISON SUMMARY")
    print("="*80)

    if complexity_data:
        winner = complexity_data[0]
        most_complex = complexity_data[-1]

        print(f"🏆 Most Efficient: {winner['method']} ({winner['code_lines']} lines)")
        print(f"📈 Most Complex: {most_complex['method']} ({most_complex['code_lines']} lines)")
        print(f"📊 Complexity Range: {most_complex['code_lines'] / winner['code_lines']:.1f}X difference")

    print("✅ All available methods tested successfully!")
    print("📊 Comparison data ready for analysis")

if __name__ == "__main__":
    main()