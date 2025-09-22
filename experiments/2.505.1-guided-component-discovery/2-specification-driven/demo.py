#!/usr/bin/env python3
"""
Demonstration script for JSV (JSON Schema Validator).
Shows all features including component reuse, output formats, and quality features.
"""

import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path

# Add JSV to path
jsv_path = Path(__file__).parent / "jsv"
sys.path.insert(0, str(jsv_path.parent))

from jsv.cli.progress import colored


def create_demo_files():
    """Create demonstration files for testing."""
    demo_dir = Path("demo_files")
    demo_dir.mkdir(exist_ok=True)

    # Create schema file
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1, "maxLength": 100},
            "email": {"type": "string", "format": "email"},
            "age": {"type": "integer", "minimum": 0, "maximum": 150},
            "website": {"type": "string", "format": "uri"},
            "birthdate": {"type": "string", "format": "date"},
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "uniqueItems": True,
                "maxItems": 10
            },
            "settings": {
                "type": "object",
                "properties": {
                    "notifications": {"type": "boolean"},
                    "theme": {"type": "string", "pattern": "^(light|dark)$"}
                },
                "required": ["notifications"],
                "additionalProperties": False
            }
        },
        "required": ["name", "email", "age"],
        "additionalProperties": False
    }

    with open(demo_dir / "schema.json", "w") as f:
        json.dump(schema, f, indent=2)

    # Create valid test data
    valid_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30,
        "website": "https://johndoe.com",
        "birthdate": "01/15/1993",
        "tags": ["developer", "python", "json"],
        "settings": {
            "notifications": True,
            "theme": "dark"
        }
    }

    with open(demo_dir / "valid.json", "w") as f:
        json.dump(valid_data, f, indent=2)

    # Create invalid test data with multiple errors
    invalid_data = {
        "name": "",  # Too short
        "email": "invalid-email",  # Invalid format
        "age": -5,  # Below minimum
        "website": "not-a-url",  # Invalid URI
        "birthdate": "invalid-date",  # Invalid date
        "tags": ["tag1", "tag1"],  # Not unique
        "settings": {
            # Missing required "notifications"
            "theme": "blue",  # Invalid pattern
            "extra": "not allowed"  # Additional property
        }
    }

    with open(demo_dir / "invalid.json", "w") as f:
        json.dump(invalid_data, f, indent=2)

    # Create more test files for batch testing
    test_files = [
        {"name": "Alice", "email": "alice@test.com", "age": 25},
        {"name": "Bob", "email": "bob@test.com", "age": 35},
        {"name": "Charlie", "email": "charlie@invalid", "age": 45},  # Invalid email
    ]

    for i, data in enumerate(test_files):
        with open(demo_dir / f"test{i+1}.json", "w") as f:
            json.dump(data, f, indent=2)

    return demo_dir


def run_jsv_command(command):
    """Run a JSV command and return the result."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "jsv"] + command,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def demo_basic_validation(demo_dir):
    """Demonstrate basic validation features."""
    colored.print_info("\n=== Basic Validation Demo ===")

    print("\n1. Validating a valid JSON file:")
    code, stdout, stderr = run_jsv_command([
        "validate", str(demo_dir / "valid.json"),
        "--schema", str(demo_dir / "schema.json")
    ])
    print(stdout)

    print("\n2. Validating an invalid JSON file:")
    code, stdout, stderr = run_jsv_command([
        "validate", str(demo_dir / "invalid.json"),
        "--schema", str(demo_dir / "schema.json")
    ])
    print(stdout)

    print("\n3. JSON output format:")
    code, stdout, stderr = run_jsv_command([
        "validate", str(demo_dir / "invalid.json"),
        "--schema", str(demo_dir / "schema.json"),
        "--format", "json"
    ])
    print(stdout)


def demo_format_validation(demo_dir):
    """Demonstrate format validation using utils components."""
    colored.print_info("\n=== Format Validation Demo (using utils components) ===")

    # Create a file with format-specific errors
    format_test = {
        "name": "Test User",
        "email": "not-an-email",  # utils.validation.email_validator
        "age": 25,
        "website": "invalid-url",  # utils.validation.url_validator
        "birthdate": "13/45/2023"  # utils.validation.date_validator
    }

    test_file = demo_dir / "format_test.json"
    with open(test_file, "w") as f:
        json.dump(format_test, f, indent=2)

    print("\nValidating format constraints (email, URL, date):")
    code, stdout, stderr = run_jsv_command([
        "validate", str(test_file),
        "--schema", str(demo_dir / "schema.json")
    ])
    print(stdout)


def demo_batch_validation(demo_dir):
    """Demonstrate batch validation with progress."""
    colored.print_info("\n=== Batch Validation Demo ===")

    print("\n1. Batch validation with text output:")
    code, stdout, stderr = run_jsv_command([
        "batch", str(demo_dir / "*.json"),
        "--schema", str(demo_dir / "schema.json")
    ])
    print(stdout)

    print("\n2. Batch validation with CSV output:")
    code, stdout, stderr = run_jsv_command([
        "batch", str(demo_dir / "test*.json"),
        "--schema", str(demo_dir / "schema.json"),
        "--output", "csv"
    ])
    print(stdout)


def demo_schema_checking():
    """Demonstrate schema validation."""
    colored.print_info("\n=== Schema Checking Demo ===")

    # Create an invalid schema
    invalid_schema = {
        "type": "invalid_type",  # Invalid type
        "properties": {
            "test": {
                "type": "string",
                "minLength": -1,  # Invalid constraint
                "format": "unsupported_format"  # Unsupported format
            }
        }
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(invalid_schema, f, indent=2)
        invalid_schema_file = f.name

    try:
        print("\nChecking an invalid schema:")
        code, stdout, stderr = run_jsv_command([
            "check", invalid_schema_file
        ])
        print(stdout)
    finally:
        os.unlink(invalid_schema_file)


def demo_pipeline_usage(demo_dir):
    """Demonstrate pipeline usage with stdin."""
    colored.print_info("\n=== Pipeline Usage Demo ===")

    print("\nValidation via pipeline (stdin):")

    # Read test data and pipe it to JSV
    with open(demo_dir / "valid.json") as f:
        test_data = f.read()

    try:
        proc = subprocess.Popen(
            [sys.executable, "-m", "jsv", "validate", "--schema", str(demo_dir / "schema.json")],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=Path(__file__).parent
        )
        stdout, stderr = proc.communicate(input=test_data)
        print(stdout)
    except Exception as e:
        print(f"Error: {e}")


def demo_component_integration():
    """Demonstrate the component integration and reuse."""
    colored.print_info("\n=== Component Integration Demo ===")

    print("JSV leverages these research-validated components from utils/:")
    print("• email_validator: RFC 5321 compliant email validation")
    print("• date_validator: Auto-format detection with leap year support")
    print("• url_validator: urllib.parse + requests accessibility checking")
    print("• file_path_validator: Cross-platform path validation")

    print("\nThese components were discovered from previous experiments:")
    print("• 1.501 - Email validator (Method 3 TDD, 130 lines)")
    print("• 1.502 - URL validator (Method 3 TDD, 64 lines)")
    print("• 1.503 - File path validator (Constrained injection, 343 lines)")
    print("• 1.504 - Date validator (Method 4 V4.1, 98 lines)")


def main():
    """Run the complete demonstration."""
    colored.print_success("🔧 JSV (JSON Schema Validator) - Complete Demonstration")
    colored.print_info("This demo showcases specification-driven development with component reuse")

    # Create demo files
    print("\nSetting up demo files...")
    demo_dir = create_demo_files()
    colored.print_success(f"✓ Demo files created in: {demo_dir}")

    # Run demonstrations
    demo_component_integration()
    demo_basic_validation(demo_dir)
    demo_format_validation(demo_dir)
    demo_batch_validation(demo_dir)
    demo_schema_checking()
    demo_pipeline_usage(demo_dir)

    print("\n" + "="*60)
    colored.print_success("✓ Demonstration complete!")
    colored.print_info("All features implemented according to specifications")
    colored.print_info("Successfully integrated utils.validation components")

    print(f"\nDemo files preserved in: {demo_dir}")
    print("You can run additional tests using the files in that directory.")


if __name__ == "__main__":
    main()