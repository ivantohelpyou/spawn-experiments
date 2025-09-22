#!/usr/bin/env python3
"""
Fallback JSON Schema Validator - Basic implementation without external dependencies
Provides basic validation for when jsonschema library is not available.
"""

import json
import re
from typing import Dict, Any, List, Tuple, Union


class BasicJSONSchemaValidator:
    """
    A basic JSON Schema validator that works without external dependencies.
    Supports a subset of JSON Schema Draft 7 features.
    """

    def __init__(self):
        self.errors = []

    def validate_json_data(self, data: Any, schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate JSON data against a basic JSON schema.

        Args:
            data: The JSON data to validate
            schema: The JSON schema dictionary

        Returns:
            Tuple of (is_valid: bool, errors: List[str])
        """
        self.errors = []
        self._validate_value(data, schema, "root")
        return len(self.errors) == 0, self.errors.copy()

    def _validate_value(self, value: Any, schema: Dict[str, Any], path: str):
        """Validate a value against a schema."""

        # Type validation
        if "type" in schema:
            if not self._validate_type(value, schema["type"], path):
                return

        # Type-specific validations
        if schema.get("type") == "string":
            self._validate_string(value, schema, path)
        elif schema.get("type") in ("number", "integer"):
            self._validate_number(value, schema, path)
        elif schema.get("type") == "array":
            self._validate_array(value, schema, path)
        elif schema.get("type") == "object":
            self._validate_object(value, schema, path)

    def _validate_type(self, value: Any, expected_type: str, path: str) -> bool:
        """Validate the type of a value."""
        valid = False

        if expected_type == "string":
            valid = isinstance(value, str)
        elif expected_type == "number":
            valid = isinstance(value, (int, float))
        elif expected_type == "integer":
            valid = isinstance(value, int) and not isinstance(value, bool)
        elif expected_type == "boolean":
            valid = isinstance(value, bool)
        elif expected_type == "array":
            valid = isinstance(value, list)
        elif expected_type == "object":
            valid = isinstance(value, dict)
        elif expected_type == "null":
            valid = value is None
        else:
            self.errors.append(f"Path '{path}': Unknown type '{expected_type}'")
            return False

        if not valid:
            actual_type = type(value).__name__
            self.errors.append(f"Path '{path}': Expected type '{expected_type}' but got '{actual_type}'")

        return valid

    def _validate_string(self, value: str, schema: Dict[str, Any], path: str):
        """Validate string-specific constraints."""
        if not isinstance(value, str):
            return

        # minLength
        if "minLength" in schema:
            min_len = schema["minLength"]
            if len(value) < min_len:
                self.errors.append(f"Path '{path}': String too short (min {min_len})")

        # maxLength
        if "maxLength" in schema:
            max_len = schema["maxLength"]
            if len(value) > max_len:
                self.errors.append(f"Path '{path}': String too long (max {max_len})")

        # pattern
        if "pattern" in schema:
            pattern = schema["pattern"]
            if not re.match(pattern, value):
                self.errors.append(f"Path '{path}': String does not match pattern '{pattern}'")

        # format (basic validation)
        if "format" in schema:
            format_type = schema["format"]
            if format_type == "email":
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, value):
                    self.errors.append(f"Path '{path}': Invalid email format")
            elif format_type == "date":
                date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                if not re.match(date_pattern, value):
                    self.errors.append(f"Path '{path}': Invalid date format (expected YYYY-MM-DD)")
            elif format_type == "uri":
                uri_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
                if not re.match(uri_pattern, value):
                    self.errors.append(f"Path '{path}': Invalid URI format")

    def _validate_number(self, value: Union[int, float], schema: Dict[str, Any], path: str):
        """Validate number-specific constraints."""
        if not isinstance(value, (int, float)):
            return

        # minimum
        if "minimum" in schema:
            minimum = schema["minimum"]
            if value < minimum:
                self.errors.append(f"Path '{path}': {value} is less than minimum {minimum}")

        # maximum
        if "maximum" in schema:
            maximum = schema["maximum"]
            if value > maximum:
                self.errors.append(f"Path '{path}': {value} is greater than maximum {maximum}")

    def _validate_array(self, value: List[Any], schema: Dict[str, Any], path: str):
        """Validate array-specific constraints."""
        if not isinstance(value, list):
            return

        # minItems
        if "minItems" in schema:
            min_items = schema["minItems"]
            if len(value) < min_items:
                self.errors.append(f"Path '{path}': Array too short (min {min_items} items)")

        # maxItems
        if "maxItems" in schema:
            max_items = schema["maxItems"]
            if len(value) > max_items:
                self.errors.append(f"Path '{path}': Array too long (max {max_items} items)")

        # uniqueItems
        if schema.get("uniqueItems", False):
            if len(value) != len(set(str(item) for item in value)):
                self.errors.append(f"Path '{path}': Array items must be unique")

        # items
        if "items" in schema:
            item_schema = schema["items"]
            for i, item in enumerate(value):
                item_path = f"{path}[{i}]"
                self._validate_value(item, item_schema, item_path)

    def _validate_object(self, value: Dict[str, Any], schema: Dict[str, Any], path: str):
        """Validate object-specific constraints."""
        if not isinstance(value, dict):
            return

        # required
        if "required" in schema:
            for required_prop in schema["required"]:
                if required_prop not in value:
                    self.errors.append(f"Path '{path}': Missing required property '{required_prop}'")

        # properties
        if "properties" in schema:
            properties = schema["properties"]
            for prop_name, prop_value in value.items():
                if prop_name in properties:
                    prop_path = f"{path} -> {prop_name}" if path != "root" else prop_name
                    self._validate_value(prop_value, properties[prop_name], prop_path)

        # additionalProperties
        if "additionalProperties" in schema:
            if schema["additionalProperties"] is False:
                properties = schema.get("properties", {})
                for prop_name in value:
                    if prop_name not in properties:
                        self.errors.append(f"Path '{path}': Additional property '{prop_name}' not allowed")

    def validate_json_string(self, json_string: str, schema_string: str) -> Tuple[bool, List[str]]:
        """Validate JSON string against schema string."""
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON data: {str(e)}"]

        try:
            schema = json.loads(schema_string)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON schema: {str(e)}"]

        return self.validate_json_data(data, schema)

    def validate_file(self, data_file: str, schema_file: str) -> Tuple[bool, List[str]]:
        """Validate JSON file against schema file."""
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


def demo_fallback():
    """Demo the fallback validator."""
    print("=== Fallback JSON Schema Validator Demo ===\n")

    validator = BasicJSONSchemaValidator()

    # Test basic validation
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "age": {"type": "integer", "minimum": 0},
            "email": {"type": "string", "format": "email"}
        },
        "required": ["name", "age"]
    }

    valid_data = {"name": "John", "age": 30, "email": "john@example.com"}
    invalid_data = {"name": "", "age": -5, "email": "not-email"}

    print("Valid data test:")
    is_valid, errors = validator.validate_json_data(valid_data, schema)
    print(f"Result: {'✓ VALID' if is_valid else '✗ INVALID'}")

    print("\nInvalid data test:")
    is_valid, errors = validator.validate_json_data(invalid_data, schema)
    print(f"Result: {'✓ VALID' if is_valid else '✗ INVALID'}")
    for error in errors:
        print(f"  - {error}")


if __name__ == "__main__":
    demo_fallback()