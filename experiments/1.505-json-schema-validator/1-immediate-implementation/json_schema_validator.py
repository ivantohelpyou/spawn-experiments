#!/usr/bin/env python3
"""
JSON Schema Validator - Python implementation using jsonschema library
Supports JSON Schema Draft 7 subset for basic validation tasks.
"""

import json
import sys
from typing import Dict, Any, Tuple, List, Optional

try:
    import jsonschema
    from jsonschema import validate, ValidationError, Draft7Validator
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False


class JSONSchemaValidator:
    """
    A JSON Schema validator that supports basic Draft 7 features.
    """

    def __init__(self):
        self.errors = []
        self.last_validation_errors = []

    def validate_json_data(self, data: Any, schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate JSON data against a JSON schema.

        Args:
            data: The JSON data to validate (already parsed)
            schema: The JSON schema dictionary

        Returns:
            Tuple of (is_valid: bool, errors: List[str])
        """
        self.last_validation_errors = []

        if not JSONSCHEMA_AVAILABLE:
            return False, ["jsonschema library not available"]

        try:
            # Validate the schema itself first
            Draft7Validator.check_schema(schema)

            # Create validator instance
            validator = Draft7Validator(schema)

            # Validate the data
            errors = list(validator.iter_errors(data))

            if errors:
                error_messages = []
                for error in errors:
                    # Build a more readable error message
                    path = " -> ".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
                    error_messages.append(f"Path '{path}': {error.message}")

                self.last_validation_errors = error_messages
                return False, error_messages
            else:
                return True, []

        except jsonschema.SchemaError as e:
            error_msg = f"Invalid schema: {e.message}"
            self.last_validation_errors = [error_msg]
            return False, [error_msg]
        except Exception as e:
            error_msg = f"Validation error: {str(e)}"
            self.last_validation_errors = [error_msg]
            return False, [error_msg]

    def validate_json_string(self, json_string: str, schema_string: str) -> Tuple[bool, List[str]]:
        """
        Validate JSON string against a JSON schema string.

        Args:
            json_string: JSON data as string
            schema_string: JSON schema as string

        Returns:
            Tuple of (is_valid: bool, errors: List[str])
        """
        try:
            # Parse JSON data
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON data: {str(e)}"
            return False, [error_msg]

        try:
            # Parse schema
            schema = json.loads(schema_string)
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON schema: {str(e)}"
            return False, [error_msg]

        return self.validate_json_data(data, schema)

    def validate_file(self, data_file: str, schema_file: str) -> Tuple[bool, List[str]]:
        """
        Validate JSON file against a schema file.

        Args:
            data_file: Path to JSON data file
            schema_file: Path to JSON schema file

        Returns:
            Tuple of (is_valid: bool, errors: List[str])
        """
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return False, [f"Error reading data file: {str(e)}"]

        try:
            with open(schema_file, 'r') as f:
                schema = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return False, [f"Error reading schema file: {str(e)}"]

        return self.validate_json_data(data, schema)


def main():
    """Command line interface for the validator."""
    if len(sys.argv) < 3:
        print("Usage: python json_schema_validator.py <data_file> <schema_file>")
        print("   or: python json_schema_validator.py --test")
        sys.exit(1)

    if sys.argv[1] == "--test":
        run_tests()
        return

    data_file = sys.argv[1]
    schema_file = sys.argv[2]

    validator = JSONSchemaValidator()
    is_valid, errors = validator.validate_file(data_file, schema_file)

    if is_valid:
        print("✓ Validation successful: Data is valid according to the schema")
        sys.exit(0)
    else:
        print("✗ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


def run_tests():
    """Run basic tests to verify functionality."""
    validator = JSONSchemaValidator()

    print("Running JSON Schema Validator tests...")

    # Test 1: Valid simple object
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0}
        },
        "required": ["name"]
    }

    data = {"name": "John", "age": 30}
    is_valid, errors = validator.validate_json_data(data, schema)
    assert is_valid, f"Test 1 failed: {errors}"
    print("✓ Test 1 passed: Valid object validation")

    # Test 2: Invalid object (missing required field)
    data = {"age": 30}
    is_valid, errors = validator.validate_json_data(data, schema)
    assert not is_valid, "Test 2 failed: Should be invalid"
    print("✓ Test 2 passed: Invalid object validation (missing required)")

    # Test 3: Invalid type
    data = {"name": 123, "age": 30}
    is_valid, errors = validator.validate_json_data(data, schema)
    assert not is_valid, "Test 3 failed: Should be invalid"
    print("✓ Test 3 passed: Invalid type validation")

    # Test 4: Array validation
    array_schema = {
        "type": "array",
        "items": {"type": "string"},
        "minItems": 1
    }

    data = ["hello", "world"]
    is_valid, errors = validator.validate_json_data(data, array_schema)
    assert is_valid, f"Test 4 failed: {errors}"
    print("✓ Test 4 passed: Valid array validation")

    # Test 5: Format validation (email)
    email_schema = {
        "type": "object",
        "properties": {
            "email": {"type": "string", "format": "email"}
        }
    }

    data = {"email": "test@example.com"}
    is_valid, errors = validator.validate_json_data(data, email_schema)
    assert is_valid, f"Test 5 failed: {errors}"
    print("✓ Test 5 passed: Valid email format")

    # Test 6: Invalid email format
    data = {"email": "not-an-email"}
    is_valid, errors = validator.validate_json_data(data, email_schema)
    assert not is_valid, "Test 6 failed: Should be invalid email"
    print("✓ Test 6 passed: Invalid email format validation")

    print("\nAll tests passed! JSON Schema Validator is working correctly.")


if __name__ == "__main__":
    main()