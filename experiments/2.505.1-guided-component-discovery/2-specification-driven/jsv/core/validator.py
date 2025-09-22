"""
Core JSON Schema validation engine.
Implements Draft 7 subset with format validation using utils components.
"""

import json
import re
from typing import Any, Dict, List, Union, Optional
from .format_validators import format_registry


class ValidationError:
    """Represents a single validation error with context."""

    def __init__(self, path: str, message: str, line: Optional[int] = None):
        self.path = path
        self.message = message
        self.line = line

    def __str__(self):
        prefix = f"Line {self.line}: " if self.line else ""
        return f"{prefix}{self.path}: {self.message}"


class JSONSchemaValidator:
    """
    JSON Schema validator supporting Draft 7 subset.
    Leverages utils.validation components for format validation.
    """

    def __init__(self):
        self.errors = []

    def validate(self, data: Any, schema: Dict[str, Any], path: str = "$") -> List[ValidationError]:
        """
        Validate data against JSON schema.

        Args:
            data: The JSON data to validate
            schema: The JSON schema definition
            path: Current path in the data (for error reporting)

        Returns:
            List of validation errors
        """
        self.errors = []
        self._validate_value(data, schema, path)
        return self.errors

    def _validate_value(self, value: Any, schema: Dict[str, Any], path: str):
        """Validate a single value against schema constraints."""

        # Type validation
        if "type" in schema:
            if not self._validate_type(value, schema["type"], path):
                return

        # Format validation (for strings)
        if isinstance(value, str) and "format" in schema:
            self._validate_format(value, schema["format"], path)

        # String constraints
        if isinstance(value, str):
            self._validate_string_constraints(value, schema, path)

        # Number constraints
        if isinstance(value, (int, float)):
            self._validate_number_constraints(value, schema, path)

        # Object constraints
        if isinstance(value, dict):
            self._validate_object_constraints(value, schema, path)

        # Array constraints
        if isinstance(value, list):
            self._validate_array_constraints(value, schema, path)

    def _validate_type(self, value: Any, expected_type: Union[str, List[str]], path: str) -> bool:
        """Validate value type."""
        if isinstance(expected_type, list):
            return any(self._validate_type(value, t, path) for t in expected_type)

        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "object": dict,
            "array": list,
            "null": type(None)
        }

        if expected_type not in type_map:
            self.errors.append(ValidationError(path, f"Unknown type: {expected_type}"))
            return False

        expected_python_type = type_map[expected_type]

        if not isinstance(value, expected_python_type):
            actual_type = type(value).__name__
            self.errors.append(ValidationError(path, f"Expected {expected_type}, got {actual_type}"))
            return False

        return True

    def _validate_format(self, value: str, format_name: str, path: str):
        """Validate string format using utils components."""
        is_valid, error_message = format_registry.validate_format(value, format_name)
        if not is_valid:
            self.errors.append(ValidationError(path, f"Format validation failed: {error_message}"))

    def _validate_string_constraints(self, value: str, schema: Dict[str, Any], path: str):
        """Validate string-specific constraints."""

        # minLength
        if "minLength" in schema:
            min_len = schema["minLength"]
            if len(value) < min_len:
                self.errors.append(ValidationError(path, f"String too short (minimum {min_len} characters)"))

        # maxLength
        if "maxLength" in schema:
            max_len = schema["maxLength"]
            if len(value) > max_len:
                self.errors.append(ValidationError(path, f"String too long (maximum {max_len} characters)"))

        # pattern
        if "pattern" in schema:
            pattern = schema["pattern"]
            try:
                if not re.search(pattern, value):
                    self.errors.append(ValidationError(path, f"String does not match pattern: {pattern}"))
            except re.error as e:
                self.errors.append(ValidationError(path, f"Invalid regex pattern: {e}"))

    def _validate_number_constraints(self, value: Union[int, float], schema: Dict[str, Any], path: str):
        """Validate number-specific constraints."""

        # minimum
        if "minimum" in schema:
            minimum = schema["minimum"]
            if value < minimum:
                self.errors.append(ValidationError(path, f"Number too small (minimum {minimum})"))

        # maximum
        if "maximum" in schema:
            maximum = schema["maximum"]
            if value > maximum:
                self.errors.append(ValidationError(path, f"Number too large (maximum {maximum})"))

        # multipleOf
        if "multipleOf" in schema:
            multiple = schema["multipleOf"]
            if multiple != 0 and value % multiple != 0:
                self.errors.append(ValidationError(path, f"Number is not a multiple of {multiple}"))

    def _validate_object_constraints(self, value: Dict[str, Any], schema: Dict[str, Any], path: str):
        """Validate object-specific constraints."""

        # required properties
        if "required" in schema:
            for prop in schema["required"]:
                if prop not in value:
                    self.errors.append(ValidationError(f"{path}.{prop}", "Required property is missing"))

        # properties validation
        if "properties" in schema:
            for prop, prop_schema in schema["properties"].items():
                if prop in value:
                    self._validate_value(value[prop], prop_schema, f"{path}.{prop}")

        # additionalProperties
        if "additionalProperties" in schema and schema["additionalProperties"] is False:
            allowed_props = set(schema.get("properties", {}).keys())
            for prop in value:
                if prop not in allowed_props:
                    self.errors.append(ValidationError(f"{path}.{prop}", "Additional property not allowed"))

    def _validate_array_constraints(self, value: List[Any], schema: Dict[str, Any], path: str):
        """Validate array-specific constraints."""

        # minItems
        if "minItems" in schema:
            min_items = schema["minItems"]
            if len(value) < min_items:
                self.errors.append(ValidationError(path, f"Array too short (minimum {min_items} items)"))

        # maxItems
        if "maxItems" in schema:
            max_items = schema["maxItems"]
            if len(value) > max_items:
                self.errors.append(ValidationError(path, f"Array too long (maximum {max_items} items)"))

        # uniqueItems
        if schema.get("uniqueItems", False):
            if len(value) != len(set(json.dumps(item, sort_keys=True) for item in value)):
                self.errors.append(ValidationError(path, "Array items must be unique"))

        # items validation
        if "items" in schema:
            items_schema = schema["items"]
            for i, item in enumerate(value):
                self._validate_value(item, items_schema, f"{path}[{i}]")


def validate_json_data(data: str, schema: Dict[str, Any]) -> tuple[bool, List[ValidationError]]:
    """
    Validate JSON data string against schema.

    Args:
        data: JSON data as string
        schema: JSON schema dictionary

    Returns:
        Tuple of (is_valid, error_list)
    """
    try:
        parsed_data = json.loads(data)
    except json.JSONDecodeError as e:
        error = ValidationError("$", f"Invalid JSON: {str(e)}", getattr(e, 'lineno', None))
        return False, [error]

    validator = JSONSchemaValidator()
    errors = validator.validate(parsed_data, schema)
    return len(errors) == 0, errors


def validate_json_file(file_path: str, schema: Dict[str, Any]) -> tuple[bool, List[ValidationError]]:
    """
    Validate JSON file against schema.

    Args:
        file_path: Path to JSON file
        schema: JSON schema dictionary

    Returns:
        Tuple of (is_valid, error_list)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
        return validate_json_data(data, schema)
    except FileNotFoundError:
        error = ValidationError("$", f"File not found: {file_path}")
        return False, [error]
    except Exception as e:
        error = ValidationError("$", f"Error reading file: {str(e)}")
        return False, [error]