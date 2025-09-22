#!/usr/bin/env python3
"""
Demo script showing JSON Schema Validator functionality
"""

from validator import JSONSchemaValidator
import json

def demo_basic_validation():
    """Demonstrate basic validation functionality."""
    print("=== JSON Schema Validator Demo ===\n")

    validator = JSONSchemaValidator()

    # Example 1: Simple object validation
    print("Example 1: Simple object validation")
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "age": {"type": "integer", "minimum": 0},
            "email": {"type": "string", "format": "email"}
        },
        "required": ["name", "age"]
    }

    # Valid data
    valid_data = {
        "name": "Alice Smith",
        "age": 25,
        "email": "alice@example.com"
    }

    print(f"Schema: {json.dumps(schema, indent=2)}")
    print(f"Data: {json.dumps(valid_data, indent=2)}")

    is_valid, errors = validator.validate_json_data(valid_data, schema)
    print(f"Result: {'✓ VALID' if is_valid else '✗ INVALID'}")
    if errors:
        for error in errors:
            print(f"  - {error}")
    print()

    # Example 2: Invalid data
    print("Example 2: Invalid data validation")
    invalid_data = {
        "name": "",  # Too short
        "age": -5,   # Negative
        "email": "not-an-email"  # Invalid format (might be lenient)
    }

    print(f"Data: {json.dumps(invalid_data, indent=2)}")
    is_valid, errors = validator.validate_json_data(invalid_data, schema)
    print(f"Result: {'✓ VALID' if is_valid else '✗ INVALID'}")
    if errors:
        for error in errors:
            print(f"  - {error}")
    print()

    # Example 3: Array validation
    print("Example 3: Array validation")
    array_schema = {
        "type": "array",
        "items": {"type": "string"},
        "minItems": 1,
        "uniqueItems": True
    }

    valid_array = ["apple", "banana", "cherry"]
    invalid_array = ["apple", "banana", "apple"]  # Not unique

    print(f"Schema: {json.dumps(array_schema, indent=2)}")
    print(f"Valid array: {json.dumps(valid_array)}")
    is_valid, errors = validator.validate_json_data(valid_array, array_schema)
    print(f"Result: {'✓ VALID' if is_valid else '✗ INVALID'}")

    print(f"Invalid array: {json.dumps(invalid_array)}")
    is_valid, errors = validator.validate_json_data(invalid_array, array_schema)
    print(f"Result: {'✓ VALID' if is_valid else '✗ INVALID'}")
    if errors:
        for error in errors:
            print(f"  - {error}")
    print()

    # Example 4: Nested object validation
    print("Example 4: Nested object validation")
    nested_schema = {
        "type": "object",
        "properties": {
            "user": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "minimum": 1},
                    "profile": {
                        "type": "object",
                        "properties": {
                            "firstName": {"type": "string"},
                            "lastName": {"type": "string"}
                        },
                        "required": ["firstName", "lastName"]
                    }
                },
                "required": ["id", "profile"]
            }
        },
        "required": ["user"]
    }

    nested_data = {
        "user": {
            "id": 123,
            "profile": {
                "firstName": "Bob",
                "lastName": "Johnson"
            }
        }
    }

    print(f"Nested data: {json.dumps(nested_data, indent=2)}")
    is_valid, errors = validator.validate_json_data(nested_data, nested_schema)
    print(f"Result: {'✓ VALID' if is_valid else '✗ INVALID'}")

    # Missing required field
    incomplete_data = {
        "user": {
            "id": 123,
            "profile": {
                "firstName": "Bob"
                # Missing lastName
            }
        }
    }

    print(f"Incomplete data: {json.dumps(incomplete_data, indent=2)}")
    is_valid, errors = validator.validate_json_data(incomplete_data, nested_schema)
    print(f"Result: {'✓ VALID' if is_valid else '✗ INVALID'}")
    if errors:
        for error in errors:
            print(f"  - {error}")


def demo_string_validation():
    """Demonstrate JSON string validation."""
    print("\n=== String Validation Demo ===\n")

    validator = JSONSchemaValidator()

    schema_str = '{"type": "number", "minimum": 0, "maximum": 100}'
    valid_data_str = '42'
    invalid_data_str = '150'

    print(f"Schema: {schema_str}")
    print(f"Valid data: {valid_data_str}")

    is_valid, errors = validator.validate_json_string(valid_data_str, schema_str)
    print(f"Result: {'✓ VALID' if is_valid else '✗ INVALID'}")

    print(f"Invalid data: {invalid_data_str}")
    is_valid, errors = validator.validate_json_string(invalid_data_str, schema_str)
    print(f"Result: {'✓ VALID' if is_valid else '✗ INVALID'}")
    if errors:
        for error in errors:
            print(f"  - {error}")


if __name__ == "__main__":
    demo_basic_validation()
    demo_string_validation()
    print("\n=== Demo Complete ===")