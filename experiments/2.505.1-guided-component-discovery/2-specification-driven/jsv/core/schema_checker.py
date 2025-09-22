"""
Schema validation and verification utilities.
Validates JSON Schema files themselves for correctness.
"""

import json
from typing import Dict, List, Any, Union
from .validator import ValidationError


class SchemaChecker:
    """Validates JSON Schema files for correctness."""

    def __init__(self):
        self.errors = []

    def check_schema(self, schema: Dict[str, Any], path: str = "$") -> List[ValidationError]:
        """
        Check if a schema is valid JSON Schema Draft 7 subset.

        Args:
            schema: The schema to validate
            path: Current path in schema (for error reporting)

        Returns:
            List of validation errors
        """
        self.errors = []
        self._check_schema_node(schema, path)
        return self.errors

    def _check_schema_node(self, schema: Any, path: str):
        """Check a single schema node."""
        if not isinstance(schema, dict):
            self.errors.append(ValidationError(path, "Schema must be an object"))
            return

        # Check type property
        if "type" in schema:
            self._check_type_property(schema["type"], path)

        # Check format property
        if "format" in schema:
            self._check_format_property(schema["format"], path)

        # Check string constraints
        self._check_string_constraints(schema, path)

        # Check number constraints
        self._check_number_constraints(schema, path)

        # Check object constraints
        self._check_object_constraints(schema, path)

        # Check array constraints
        self._check_array_constraints(schema, path)

    def _check_type_property(self, type_value: Any, path: str):
        """Validate type property."""
        valid_types = {"string", "number", "integer", "boolean", "object", "array", "null"}

        if isinstance(type_value, str):
            if type_value not in valid_types:
                self.errors.append(ValidationError(f"{path}.type", f"Invalid type: {type_value}"))
        elif isinstance(type_value, list):
            for i, t in enumerate(type_value):
                if not isinstance(t, str) or t not in valid_types:
                    self.errors.append(ValidationError(f"{path}.type[{i}]", f"Invalid type: {t}"))
        else:
            self.errors.append(ValidationError(f"{path}.type", "Type must be string or array of strings"))

    def _check_format_property(self, format_value: Any, path: str):
        """Validate format property."""
        if not isinstance(format_value, str):
            self.errors.append(ValidationError(f"{path}.format", "Format must be a string"))
            return

        # We support these formats via utils components
        supported_formats = {"email", "date", "uri", "url"}
        if format_value not in supported_formats:
            self.errors.append(ValidationError(
                f"{path}.format",
                f"Unsupported format: {format_value}. Supported: {', '.join(supported_formats)}"
            ))

    def _check_string_constraints(self, schema: Dict[str, Any], path: str):
        """Check string-specific constraints."""
        if "minLength" in schema:
            if not isinstance(schema["minLength"], int) or schema["minLength"] < 0:
                self.errors.append(ValidationError(f"{path}.minLength", "Must be non-negative integer"))

        if "maxLength" in schema:
            if not isinstance(schema["maxLength"], int) or schema["maxLength"] < 0:
                self.errors.append(ValidationError(f"{path}.maxLength", "Must be non-negative integer"))

        if "minLength" in schema and "maxLength" in schema:
            if schema["minLength"] > schema["maxLength"]:
                self.errors.append(ValidationError(path, "minLength cannot be greater than maxLength"))

        if "pattern" in schema:
            if not isinstance(schema["pattern"], str):
                self.errors.append(ValidationError(f"{path}.pattern", "Pattern must be a string"))

    def _check_number_constraints(self, schema: Dict[str, Any], path: str):
        """Check number-specific constraints."""
        if "minimum" in schema:
            if not isinstance(schema["minimum"], (int, float)):
                self.errors.append(ValidationError(f"{path}.minimum", "Must be a number"))

        if "maximum" in schema:
            if not isinstance(schema["maximum"], (int, float)):
                self.errors.append(ValidationError(f"{path}.maximum", "Must be a number"))

        if "minimum" in schema and "maximum" in schema:
            if schema["minimum"] > schema["maximum"]:
                self.errors.append(ValidationError(path, "minimum cannot be greater than maximum"))

        if "multipleOf" in schema:
            if not isinstance(schema["multipleOf"], (int, float)) or schema["multipleOf"] <= 0:
                self.errors.append(ValidationError(f"{path}.multipleOf", "Must be a positive number"))

    def _check_object_constraints(self, schema: Dict[str, Any], path: str):
        """Check object-specific constraints."""
        if "properties" in schema:
            if not isinstance(schema["properties"], dict):
                self.errors.append(ValidationError(f"{path}.properties", "Must be an object"))
            else:
                for prop, prop_schema in schema["properties"].items():
                    self._check_schema_node(prop_schema, f"{path}.properties.{prop}")

        if "required" in schema:
            if not isinstance(schema["required"], list):
                self.errors.append(ValidationError(f"{path}.required", "Must be an array"))
            else:
                for i, prop in enumerate(schema["required"]):
                    if not isinstance(prop, str):
                        self.errors.append(ValidationError(f"{path}.required[{i}]", "Must be a string"))

        if "additionalProperties" in schema:
            if not isinstance(schema["additionalProperties"], bool):
                self.errors.append(ValidationError(f"{path}.additionalProperties", "Must be boolean"))

    def _check_array_constraints(self, schema: Dict[str, Any], path: str):
        """Check array-specific constraints."""
        if "items" in schema:
            if isinstance(schema["items"], dict):
                self._check_schema_node(schema["items"], f"{path}.items")
            else:
                self.errors.append(ValidationError(f"{path}.items", "Must be a schema object"))

        if "minItems" in schema:
            if not isinstance(schema["minItems"], int) or schema["minItems"] < 0:
                self.errors.append(ValidationError(f"{path}.minItems", "Must be non-negative integer"))

        if "maxItems" in schema:
            if not isinstance(schema["maxItems"], int) or schema["maxItems"] < 0:
                self.errors.append(ValidationError(f"{path}.maxItems", "Must be non-negative integer"))

        if "minItems" in schema and "maxItems" in schema:
            if schema["minItems"] > schema["maxItems"]:
                self.errors.append(ValidationError(path, "minItems cannot be greater than maxItems"))

        if "uniqueItems" in schema:
            if not isinstance(schema["uniqueItems"], bool):
                self.errors.append(ValidationError(f"{path}.uniqueItems", "Must be boolean"))


def check_schema_file(file_path: str) -> tuple[bool, List[ValidationError]]:
    """
    Check if a JSON Schema file is valid.

    Args:
        file_path: Path to schema file

    Returns:
        Tuple of (is_valid, error_list)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except FileNotFoundError:
        error = ValidationError("$", f"Schema file not found: {file_path}")
        return False, [error]
    except json.JSONDecodeError as e:
        error = ValidationError("$", f"Invalid JSON in schema: {str(e)}", getattr(e, 'lineno', None))
        return False, [error]
    except Exception as e:
        error = ValidationError("$", f"Error reading schema file: {str(e)}")
        return False, [error]

    checker = SchemaChecker()
    errors = checker.check_schema(schema)
    return len(errors) == 0, errors


def check_schema_data(schema_data: str) -> tuple[bool, List[ValidationError]]:
    """
    Check if a JSON Schema string is valid.

    Args:
        schema_data: JSON Schema as string

    Returns:
        Tuple of (is_valid, error_list)
    """
    try:
        schema = json.loads(schema_data)
    except json.JSONDecodeError as e:
        error = ValidationError("$", f"Invalid JSON in schema: {str(e)}", getattr(e, 'lineno', None))
        return False, [error]

    checker = SchemaChecker()
    errors = checker.check_schema(schema)
    return len(errors) == 0, errors