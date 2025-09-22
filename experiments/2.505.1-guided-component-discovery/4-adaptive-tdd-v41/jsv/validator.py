"""
Core JSON Schema validation functionality.
Implements JSON Schema Draft 7 subset with strategic component reuse.
"""

import json
from typing import Any, Dict, List, Union
from .formats import validate_format


class ValidationError:
    """Represents a validation error with context."""

    def __init__(self, message: str, path: str = "", value: Any = None):
        self.message = message
        self.path = path
        self.value = value

    def __str__(self):
        if self.path:
            return f"At '{self.path}': {self.message}"
        return self.message


class JSONSchemaValidator:
    """
    JSON Schema validator implementing Draft 7 subset.

    Supports:
    - Basic types: string, number, integer, boolean, object, array, null
    - Required fields and property validation
    - String constraints: minLength, maxLength
    - Number constraints: minimum, maximum
    - Format validation (integrates with utils/validation components)
    """

    def __init__(self, schema: Dict[str, Any]):
        """
        Initialize validator with JSON schema.

        Args:
            schema: JSON schema dictionary
        """
        self.schema = schema
        self.errors = []

    def validate(self, data: Any) -> bool:
        """
        Validate data against schema.

        Args:
            data: Data to validate

        Returns:
            bool: True if valid, False otherwise
        """
        self.errors = []
        return self._validate_value(data, self.schema, "")

    def validate_with_errors(self, data: Any) -> Dict[str, Any]:
        """
        Validate data and return detailed error information.

        Args:
            data: Data to validate

        Returns:
            dict: {'valid': bool, 'errors': List[ValidationError]}
        """
        self.errors = []
        is_valid = self._validate_value(data, self.schema, "")
        return {
            'valid': is_valid,
            'errors': self.errors.copy()
        }

    def validate_json_string(self, json_string: str) -> bool:
        """
        Validate JSON string against schema.

        Args:
            json_string: JSON data as string

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            data = json.loads(json_string)
            return self.validate(data)
        except json.JSONDecodeError:
            return False

    def _validate_value(self, value: Any, schema: Dict[str, Any], path: str) -> bool:
        """
        Internal method to validate a value against a schema.

        Args:
            value: Value to validate
            schema: Schema to validate against
            path: Current path in the data structure

        Returns:
            bool: True if valid, False otherwise
        """
        is_valid = True

        # Type validation
        if "type" in schema:
            if not self._validate_type(value, schema["type"], path):
                is_valid = False

        # Type-specific validations
        if isinstance(value, str):
            if not self._validate_string_constraints(value, schema, path):
                is_valid = False
            # Format validation for strings
            if "format" in schema:
                if not validate_format(value, schema["format"]):
                    self.errors.append(ValidationError(
                        f"Invalid {schema['format']} format", path, value
                    ))
                    is_valid = False
        elif isinstance(value, (int, float)):
            if not self._validate_number_constraints(value, schema, path):
                is_valid = False
        elif isinstance(value, dict):
            if not self._validate_object_constraints(value, schema, path):
                is_valid = False
        elif isinstance(value, list):
            if not self._validate_array_constraints(value, schema, path):
                is_valid = False

        return is_valid

    def _validate_type(self, value: Any, expected_type: str, path: str) -> bool:
        """Validate that value matches expected type."""
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "null": type(None),
            "object": dict,
            "array": list
        }

        # Special case for integer - JSON integers can be floats with .0
        if expected_type == "integer":
            if isinstance(value, float) and value.is_integer():
                return True
            elif not isinstance(value, int):
                self.errors.append(ValidationError(
                    f"Expected integer, got {type(value).__name__}", path, value
                ))
                return False
            return True

        expected_python_type = type_map.get(expected_type)
        if expected_python_type is None:
            self.errors.append(ValidationError(
                f"Unknown type: {expected_type}", path, value
            ))
            return False

        if not isinstance(value, expected_python_type):
            self.errors.append(ValidationError(
                f"Expected {expected_type}, got {type(value).__name__}", path, value
            ))
            return False

        return True

    def _validate_string_constraints(self, value: str, schema: Dict[str, Any], path: str) -> bool:
        """Validate string-specific constraints."""
        is_valid = True

        if "minLength" in schema:
            min_length = schema["minLength"]
            if len(value) < min_length:
                self.errors.append(ValidationError(
                    f"String too short (min: {min_length}, actual: {len(value)})", path, value
                ))
                is_valid = False

        if "maxLength" in schema:
            max_length = schema["maxLength"]
            if len(value) > max_length:
                self.errors.append(ValidationError(
                    f"String too long (max: {max_length}, actual: {len(value)})", path, value
                ))
                is_valid = False

        return is_valid

    def _validate_number_constraints(self, value: Union[int, float], schema: Dict[str, Any], path: str) -> bool:
        """Validate number-specific constraints."""
        is_valid = True

        if "minimum" in schema:
            minimum = schema["minimum"]
            if value < minimum:
                self.errors.append(ValidationError(
                    f"Number too small (min: {minimum}, actual: {value})", path, value
                ))
                is_valid = False

        if "maximum" in schema:
            maximum = schema["maximum"]
            if value > maximum:
                self.errors.append(ValidationError(
                    f"Number too large (max: {maximum}, actual: {value})", path, value
                ))
                is_valid = False

        return is_valid

    def _validate_object_constraints(self, value: dict, schema: Dict[str, Any], path: str) -> bool:
        """Validate object-specific constraints."""
        is_valid = True

        # Required properties
        if "required" in schema:
            for required_prop in schema["required"]:
                if required_prop not in value:
                    prop_path = f"{path}.{required_prop}" if path else required_prop
                    self.errors.append(ValidationError(
                        f"Required property '{required_prop}' is missing", prop_path
                    ))
                    is_valid = False

        # Property validation
        if "properties" in schema:
            for prop_name, prop_schema in schema["properties"].items():
                if prop_name in value:
                    prop_path = f"{path}.{prop_name}" if path else prop_name
                    if not self._validate_value(value[prop_name], prop_schema, prop_path):
                        is_valid = False

        return is_valid

    def _validate_array_constraints(self, value: list, schema: Dict[str, Any], path: str) -> bool:
        """Validate array-specific constraints."""
        # For now, just basic array type validation
        # Can be extended with items, minItems, maxItems, etc.
        return True