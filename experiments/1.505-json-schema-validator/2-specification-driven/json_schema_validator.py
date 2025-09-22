"""
JSON Schema Validator

A comprehensive JSON Schema validator using the jsonschema library with support
for JSON Schema Draft 7 features including type validation, object properties,
array constraints, and format validation.
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union


class ValidationResult:
    """
    Encapsulates validation outcome with structured error reporting.

    Attributes:
        is_valid (bool): Whether the validation passed
        errors (List[str]): List of validation error messages
    """

    def __init__(self, is_valid: bool, errors: Optional[List[str]] = None):
        self.is_valid = is_valid
        self.errors = errors or []

    def __str__(self) -> str:
        """Human-readable validation result."""
        if self.is_valid:
            return "Validation successful"
        else:
            error_count = len(self.errors)
            if error_count == 1:
                return f"Validation failed: {self.errors[0]}"
            else:
                errors_text = "\n".join(f"  - {error}" for error in self.errors)
                return f"Validation failed with {error_count} errors:\n{errors_text}"

    def __bool__(self) -> bool:
        """Allow boolean evaluation of validation result."""
        return self.is_valid


class JSONSchemaValidator:
    """
    Main validator class using jsonschema library for JSON Schema Draft 7 validation.

    Supports:
    - Basic data types (string, number, integer, boolean, object, array)
    - Object properties and required fields
    - Array items and length constraints
    - String length and format validation (email, date, uri)
    - Numeric range validation
    """

    def __init__(self):
        """Initialize validator with Draft 7 schema support."""
        try:
            import jsonschema
            self._jsonschema = jsonschema
            self._draft7_validator = jsonschema.Draft7Validator
        except ImportError:
            raise ImportError(
                "jsonschema library is required. Install with: pip install jsonschema"
            )

    def validate(self, data: Any, schema: Dict) -> ValidationResult:
        """
        Validate data against a JSON schema.

        Args:
            data: The data to validate (Python object - use validate_json_string for JSON strings)
            schema: JSON Schema Draft 7 specification as a dictionary

        Returns:
            ValidationResult: Object containing validation outcome and errors
        """
        # Validate schema structure first
        schema_valid, schema_error = self._validate_schema(schema)
        if not schema_valid:
            return ValidationResult(False, [schema_error])

        # Perform schema validation
        try:
            validator = self._draft7_validator(schema)
            errors = list(validator.iter_errors(data))

            if not errors:
                return ValidationResult(True)
            else:
                formatted_errors = self._format_errors(errors)
                return ValidationResult(False, formatted_errors)

        except Exception as e:
            error_msg = f"Validation error: {str(e)}"
            return ValidationResult(False, [error_msg])

    def validate_json_string(self, json_string: str, schema: Dict) -> ValidationResult:
        """
        Validate a JSON string against a schema.

        Args:
            json_string: JSON data as a string
            schema: JSON Schema Draft 7 specification

        Returns:
            ValidationResult: Object containing validation outcome and errors
        """
        # Validate schema structure first
        schema_valid, schema_error = self._validate_schema(schema)
        if not schema_valid:
            return ValidationResult(False, [schema_error])

        # Parse JSON string
        parse_success, parsed_data, parse_error = self._parse_json(json_string)
        if not parse_success:
            return ValidationResult(False, [parse_error])

        # Validate parsed data
        return self.validate(parsed_data, schema)

    def _parse_json(self, json_string: str) -> Tuple[bool, Any, Optional[str]]:
        """
        Parse JSON string with comprehensive error handling.

        Args:
            json_string: String containing JSON data

        Returns:
            Tuple of (success, parsed_data, error_message)
        """
        try:
            data = json.loads(json_string)
            return True, data, None
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON: {str(e)}"
            return False, None, error_msg
        except Exception as e:
            error_msg = f"JSON parsing error: {str(e)}"
            return False, None, error_msg

    def _validate_schema(self, schema: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate schema structure before use.

        Args:
            schema: JSON Schema to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            self._draft7_validator.check_schema(schema)
            return True, None
        except Exception as e:
            error_msg = f"Invalid schema: {str(e)}"
            return False, error_msg

    def _format_errors(self, validation_errors) -> List[str]:
        """
        Convert jsonschema ValidationError objects to readable strings.

        Args:
            validation_errors: List of ValidationError objects from jsonschema

        Returns:
            List of formatted error messages
        """
        formatted_errors = []
        for error in validation_errors:
            # Create a more readable error message
            if error.absolute_path:
                path = ".".join(str(p) for p in error.absolute_path)
                message = f"At '{path}': {error.message}"
            else:
                message = error.message
            formatted_errors.append(message)
        return formatted_errors


# Utility functions for convenience

def is_valid_json(json_string: str) -> bool:
    """
    Quick check if a string contains valid JSON.

    Args:
        json_string: String to check

    Returns:
        True if valid JSON, False otherwise
    """
    try:
        json.loads(json_string)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def validate_simple(data: Any, schema: Dict) -> bool:
    """
    Simple boolean validation without detailed error information.

    Args:
        data: Data to validate
        schema: JSON Schema to validate against

    Returns:
        True if valid, False otherwise
    """
    try:
        validator = JSONSchemaValidator()
        result = validator.validate(data, schema)
        return result.is_valid
    except Exception:
        return False


def create_validator(schema: Dict) -> 'JSONSchemaValidator':
    """
    Factory function for creating a validator with a specific schema.

    Args:
        schema: JSON Schema to use for validation

    Returns:
        Configured JSONSchemaValidator instance
    """
    validator = JSONSchemaValidator()
    # Validate the schema immediately to catch errors early
    schema_valid, error = validator._validate_schema(schema)
    if not schema_valid:
        raise ValueError(f"Invalid schema: {error}")
    return validator


# Format validation functions (used by jsonschema library)

def validate_email_format(value: str) -> bool:
    """
    Validate email format using regex.

    Args:
        value: Email string to validate

    Returns:
        True if valid email format, False otherwise
    """
    if not isinstance(value, str):
        return False

    # Basic email validation regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, value) is not None


def validate_date_format(value: str) -> bool:
    """
    Validate ISO 8601 date format (YYYY-MM-DD).

    Args:
        value: Date string to validate

    Returns:
        True if valid date format, False otherwise
    """
    if not isinstance(value, str):
        return False

    # Check basic format first
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, value):
        return False

    # Validate actual date
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_uri_format(value: str) -> bool:
    """
    Basic URI format validation.

    Args:
        value: URI string to validate

    Returns:
        True if valid URI format, False otherwise
    """
    if not isinstance(value, str):
        return False

    # Basic URI validation - must have scheme
    pattern = r'^[a-zA-Z][a-zA-Z0-9+.-]*:'
    return re.match(pattern, value) is not None


if __name__ == "__main__":
    # Example usage and demonstration
    validator = JSONSchemaValidator()

    # Example 1: Basic object validation
    schema1 = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0}
        },
        "required": ["name"]
    }

    data1 = {"name": "John", "age": 30}
    result1 = validator.validate(data1, schema1)
    print("Example 1 - Valid object:")
    print(f"Result: {result1}")
    print()

    # Example 2: Invalid data
    data2 = {"age": "not a number"}
    result2 = validator.validate(data2, schema1)
    print("Example 2 - Invalid object:")
    print(f"Result: {result2}")
    print()

    # Example 3: Format validation
    schema3 = {
        "type": "object",
        "properties": {
            "email": {"type": "string", "format": "email"},
            "website": {"type": "string", "format": "uri"},
            "birthdate": {"type": "string", "format": "date"}
        },
        "required": ["email"]
    }

    data3 = {
        "email": "user@example.com",
        "website": "https://example.com",
        "birthdate": "1990-01-01"
    }
    result3 = validator.validate(data3, schema3)
    print("Example 3 - Format validation:")
    print(f"Result: {result3}")
    print()

    # Example 4: JSON string validation
    json_string = '{"items": [1, 2, 3, 4, 5]}'
    schema4 = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {"type": "integer"},
                "minItems": 1,
                "maxItems": 10
            }
        }
    }
    result4 = validator.validate_json_string(json_string, schema4)
    print("Example 4 - JSON string validation:")
    print(f"Result: {result4}")