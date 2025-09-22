#!/usr/bin/env python3
"""
Example usage of the JSON Schema Validator

This script demonstrates the key features of the JSON Schema Validator
including basic type validation, object properties, array constraints,
and format validation.
"""

from json_schema_validator import JSONSchemaValidator, ValidationResult


def main():
    """Demonstrate JSON Schema Validator functionality."""
    print("JSON Schema Validator - Example Usage")
    print("=" * 50)

    validator = JSONSchemaValidator()

    # Example 1: Basic Type Validation
    print("\n1. Basic Type Validation")
    print("-" * 25)

    schemas_and_data = [
        ({"type": "string"}, "hello world", "Valid string"),
        ({"type": "string"}, 123, "Invalid string (number)"),
        ({"type": "integer"}, 42, "Valid integer"),
        ({"type": "integer"}, 42.5, "Invalid integer (float)"),
        ({"type": "boolean"}, True, "Valid boolean"),
        ({"type": "array"}, [1, 2, 3], "Valid array"),
        ({"type": "object"}, {"key": "value"}, "Valid object")
    ]

    for schema, data, description in schemas_and_data:
        result = validator.validate(data, schema)
        status = "✓ PASS" if result.is_valid else "✗ FAIL"
        print(f"{status} {description}: {data}")
        if not result.is_valid:
            print(f"      Error: {result.errors[0]}")

    # Example 2: Object with Properties and Required Fields
    print("\n2. Object Validation with Properties")
    print("-" * 35)

    user_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0},
            "email": {"type": "string", "format": "email"}
        },
        "required": ["name", "email"]
    }

    users = [
        ({"name": "Alice", "age": 30, "email": "alice@example.com"}, "Valid user"),
        ({"name": "Bob", "email": "bob@example.com"}, "Valid user (age optional)"),
        ({"name": "Charlie", "age": -5, "email": "charlie@example.com"}, "Invalid age"),
        ({"age": 25, "email": "missing@example.com"}, "Missing required name"),
        ({"name": "Dave", "email": "invalid-email"}, "Invalid email format")
    ]

    for user_data, description in users:
        result = validator.validate(user_data, user_schema)
        status = "✓ PASS" if result.is_valid else "✗ FAIL"
        print(f"{status} {description}: {user_data}")
        if not result.is_valid:
            for error in result.errors:
                print(f"      Error: {error}")

    # Example 3: Array Validation
    print("\n3. Array Validation")
    print("-" * 19)

    scores_schema = {
        "type": "array",
        "items": {"type": "integer", "minimum": 0, "maximum": 100},
        "minItems": 1,
        "maxItems": 5
    }

    score_data = [
        ([85, 92, 78], "Valid scores"),
        ([85, 92, 105], "Score too high"),
        ([], "Too few items"),
        ([85, 92, 78, 88, 90, 95], "Too many items"),
        ([85, "ninety", 78], "Invalid item type")
    ]

    for scores, description in score_data:
        result = validator.validate(scores, scores_schema)
        status = "✓ PASS" if result.is_valid else "✗ FAIL"
        print(f"{status} {description}: {scores}")
        if not result.is_valid:
            for error in result.errors:
                print(f"      Error: {error}")

    # Example 4: Format Validation
    print("\n4. Format Validation")
    print("-" * 20)

    contact_schema = {
        "type": "object",
        "properties": {
            "email": {"type": "string", "format": "email"},
            "website": {"type": "string", "format": "uri"},
            "birthdate": {"type": "string", "format": "date"}
        }
    }

    contacts = [
        ({
            "email": "user@example.com",
            "website": "https://example.com",
            "birthdate": "1990-01-01"
        }, "Valid contact info"),
        ({
            "email": "invalid-email",
            "website": "https://example.com",
            "birthdate": "1990-01-01"
        }, "Invalid email"),
        ({
            "email": "user@example.com",
            "website": "https://example.com",
            "birthdate": "1990-13-01"
        }, "Invalid date")
    ]

    for contact, description in contacts:
        result = validator.validate(contact, contact_schema)
        status = "✓ PASS" if result.is_valid else "✗ FAIL"
        print(f"{status} {description}")
        if not result.is_valid:
            for error in result.errors:
                print(f"      Error: {error}")

    # Example 5: JSON String Validation
    print("\n5. JSON String Validation")
    print("-" * 25)

    json_examples = [
        ('{"name": "John", "age": 30}', "Valid JSON object"),
        ('[1, 2, 3, 4, 5]', "Valid JSON array"),
        ('{"invalid": json}', "Invalid JSON syntax"),
        ('"simple string"', "Valid JSON string")
    ]

    simple_schema = {"type": "object"}

    for json_string, description in json_examples:
        result = validator.validate_json_string(json_string, simple_schema)
        status = "✓ PASS" if result.is_valid else "✗ FAIL"
        print(f"{status} {description}: {json_string}")
        if not result.is_valid:
            print(f"      Error: {result.errors[0]}")

    # Example 6: Complex Nested Structure
    print("\n6. Complex Nested Structure")
    print("-" * 28)

    complex_schema = {
        "type": "object",
        "properties": {
            "user": {
                "type": "object",
                "properties": {
                    "personal": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "age": {"type": "integer", "minimum": 0}
                        },
                        "required": ["name"]
                    },
                    "contacts": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string"},
                                "value": {"type": "string"}
                            },
                            "required": ["type", "value"]
                        }
                    }
                },
                "required": ["personal"]
            }
        },
        "required": ["user"]
    }

    complex_data = {
        "user": {
            "personal": {
                "name": "Alice Johnson",
                "age": 28
            },
            "contacts": [
                {"type": "email", "value": "alice@example.com"},
                {"type": "phone", "value": "+1234567890"}
            ]
        }
    }

    result = validator.validate(complex_data, complex_schema)
    status = "✓ PASS" if result.is_valid else "✗ FAIL"
    print(f"{status} Complex nested object validation")
    if not result.is_valid:
        for error in result.errors:
            print(f"      Error: {error}")

    print("\n" + "=" * 50)
    print("Examples completed!")


if __name__ == "__main__":
    main()