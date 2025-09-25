#!/usr/bin/env python3
"""
Demo Script for Experiment 2.505.2: Severed Branch Timing Comparison
Tests all 4 method implementations to verify they work as expected
"""

import subprocess
import json
import tempfile
import os
import sys
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_status(message, status="INFO"):
    colors = {"INFO": BLUE, "SUCCESS": GREEN, "ERROR": RED, "WARNING": YELLOW}
    print(f"{colors.get(status, RESET)}[{status}] {message}{RESET}")

def create_test_files(temp_dir):
    """Create test schema and data files"""
    # Test schema
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "email": {"type": "string", "format": "email"},
            "age": {"type": "integer", "minimum": 0}
        },
        "required": ["name", "email", "age"]
    }

    # Valid test data
    valid_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }

    # Invalid test data
    invalid_data = {
        "name": "",
        "email": "invalid-email",
        "age": -5
    }

    schema_file = temp_dir / "test_schema.json"
    valid_file = temp_dir / "valid_data.json"
    invalid_file = temp_dir / "invalid_data.json"

    with open(schema_file, 'w') as f:
        json.dump(schema, f, indent=2)

    with open(valid_file, 'w') as f:
        json.dump(valid_data, f, indent=2)

    with open(invalid_file, 'w') as f:
        json.dump(invalid_data, f, indent=2)

    return schema_file, valid_file, invalid_file

def test_method_implementation(method_dir, method_name, schema_file, valid_file, invalid_file):
    """Test a specific method implementation"""
    print_status(f"Testing {method_name}", "INFO")

    jsv_script = method_dir / "jsv.py"
    if not jsv_script.exists():
        print_status(f"No jsv.py found in {method_dir}", "ERROR")
        return False

    # Make script executable
    os.chmod(jsv_script, 0o755)

    try:
        # Test 1: Validate valid data
        print_status(f"  Test 1: Valid data validation", "INFO")
        result = subprocess.run([
            sys.executable, str(jsv_script),
            "validate", str(valid_file), str(schema_file)
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print_status(f"    ✓ Valid data correctly accepted", "SUCCESS")
        else:
            print_status(f"    ✗ Valid data rejected: {result.stderr}", "ERROR")
            return False

        # Test 2: Validate invalid data
        print_status(f"  Test 2: Invalid data validation", "INFO")
        result = subprocess.run([
            sys.executable, str(jsv_script),
            "validate", str(invalid_file), str(schema_file)
        ], capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print_status(f"    ✓ Invalid data correctly rejected", "SUCCESS")
        else:
            print_status(f"    ✗ Invalid data incorrectly accepted", "ERROR")
            return False

        # Test 3: Help command
        print_status(f"  Test 3: Help command", "INFO")
        result = subprocess.run([
            sys.executable, str(jsv_script), "--help"
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0 and "JSON Schema Validator" in result.stdout:
            print_status(f"    ✓ Help command works", "SUCCESS")
        else:
            print_status(f"    ✗ Help command failed", "ERROR")
            return False

        # Test 4: Check schema command (if supported)
        print_status(f"  Test 4: Schema checking", "INFO")
        result = subprocess.run([
            sys.executable, str(jsv_script),
            "check-schema", str(schema_file)
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print_status(f"    ✓ Schema checking works", "SUCCESS")
        else:
            print_status(f"    ⚠ Schema checking not supported or failed", "WARNING")

        print_status(f"{method_name} implementation: WORKING ✓", "SUCCESS")
        return True

    except subprocess.TimeoutExpired:
        print_status(f"  ✗ Test timed out", "ERROR")
        return False
    except Exception as e:
        print_status(f"  ✗ Test failed: {str(e)}", "ERROR")
        return False

def main():
    print_status("=== Demo Script for Experiment 2.505.2 ===", "INFO")
    print_status("Testing all 4 severed branch method implementations", "INFO")
    print()

    # Get experiment directory
    experiment_dir = Path(__file__).parent

    # Create temporary test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print_status(f"Created test files in: {temp_path}", "INFO")

        schema_file, valid_file, invalid_file = create_test_files(temp_path)

        # Test each method
        methods = [
            ("1-immediate-implementation", "Method 1: Immediate Implementation"),
            ("2-specification-driven", "Method 2: Specification-driven Development"),
            ("3-test-first-development", "Method 3: Test-First Development (TDD)"),
            ("4-adaptive-tdd-v4.1", "Method 4: Adaptive TDD V4.1")
        ]

        results = {}

        for method_folder, method_name in methods:
            method_dir = experiment_dir / method_folder
            if method_dir.exists():
                results[method_name] = test_method_implementation(
                    method_dir, method_name, schema_file, valid_file, invalid_file
                )
                print()
            else:
                print_status(f"Method directory not found: {method_dir}", "ERROR")
                results[method_name] = False

        # Summary
        print_status("=== DEMO RESULTS SUMMARY ===", "INFO")
        working_count = 0
        for method_name, working in results.items():
            status = "WORKING ✓" if working else "FAILED ✗"
            color = "SUCCESS" if working else "ERROR"
            print_status(f"{method_name}: {status}", color)
            if working:
                working_count += 1

        print()
        if working_count == len(results):
            print_status(f"ALL {working_count} implementations working correctly! 🎉", "SUCCESS")
            return 0
        else:
            print_status(f"Only {working_count}/{len(results)} implementations working", "WARNING")
            return 1

if __name__ == "__main__":
    sys.exit(main())