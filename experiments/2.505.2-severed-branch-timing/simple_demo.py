#!/usr/bin/env python3
"""
Simple Demo Script for 2.505.2 (no colors)
"""
import subprocess
import json
import tempfile
import sys
from pathlib import Path

def create_test_files(temp_dir):
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "email": {"type": "string", "format": "email"},
            "age": {"type": "integer", "minimum": 0}
        },
        "required": ["name", "email", "age"]
    }

    valid_data = {"name": "John", "email": "john@test.com", "age": 30}
    invalid_data = {"name": "", "email": "invalid", "age": -5}

    schema_file = temp_dir / "schema.json"
    valid_file = temp_dir / "valid.json"
    invalid_file = temp_dir / "invalid.json"

    with open(schema_file, 'w') as f:
        json.dump(schema, f)
    with open(valid_file, 'w') as f:
        json.dump(valid_data, f)
    with open(invalid_file, 'w') as f:
        json.dump(invalid_data, f)

    return schema_file, valid_file, invalid_file

def test_method(method_dir, name):
    print(f"\n=== Testing {name} ===")

    jsv = method_dir / "jsv.py"
    if not jsv.exists():
        print(f"ERROR: No jsv.py in {method_dir}")
        return False

    with tempfile.TemporaryDirectory() as tmp:
        temp_path = Path(tmp)
        schema, valid, invalid = create_test_files(temp_path)

        try:
            # Test valid data
            result = subprocess.run([sys.executable, str(jsv), "validate", str(valid), str(schema)],
                                 capture_output=True, timeout=10)
            if result.returncode != 0:
                print(f"FAIL: Valid data rejected")
                return False
            print("PASS: Valid data accepted")

            # Test invalid data
            result = subprocess.run([sys.executable, str(jsv), "validate", str(invalid), str(schema)],
                                 capture_output=True, timeout=10)
            if result.returncode == 0:
                print(f"FAIL: Invalid data accepted")
                return False
            print("PASS: Invalid data rejected")

            return True

        except Exception as e:
            print(f"ERROR: {e}")
            return False

def main():
    print("=== Simple Demo for 2.505.2 ===")

    base_dir = Path(__file__).parent
    methods = [
        ("1-immediate-implementation", "Method 1: Immediate"),
        ("2-specification-driven", "Method 2: Spec-driven"),
        ("3-test-first-development", "Method 3: TDD"),
        ("4-adaptive-tdd-v4.1", "Method 4: Adaptive TDD")
    ]

    results = {}
    for folder, name in methods:
        method_dir = base_dir / folder
        if method_dir.exists():
            results[name] = test_method(method_dir, name)
        else:
            print(f"\nERROR: {method_dir} not found")
            results[name] = False

    print(f"\n=== SUMMARY ===")
    working = 0
    for name, status in results.items():
        print(f"{name}: {'WORKING' if status else 'FAILED'}")
        if status:
            working += 1

    print(f"\nResult: {working}/{len(results)} implementations working")
    return 0 if working == len(results) else 1

if __name__ == "__main__":
    sys.exit(main())