#!/usr/bin/env python3
"""
JSON Schema Validator - Draft 7 Subset Implementation
Supports basic types, properties, required fields, and format validation
"""

import json
import re
from typing import Any, Dict, List, Union
from urllib.parse import urlparse


class ValidationResult:
    """Container for validation results"""

    def __init__(self, is_valid: bool, errors: List[str]):
        self.is_valid = is_valid
        self.errors = errors

    def __str__(self):
        if self.is_valid:
            return "Valid"
        return f"Invalid: {'; '.join(self.errors)}"


class JSONSchemaValidator:
    """JSON Schema Validator supporting Draft 7 subset"""

    # Supported basic types
    SUPPORTED_TYPES = {
        'string', 'number', 'integer', 'boolean', 'object', 'array', 'null'
    }

    # Format validators
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]*[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$|^[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
    )

    DATE_PATTERN = re.compile(
        r'^\d{4}-\d{2}-\d{2}$'
    )

    def __init__(self):
        """Initialize the validator"""
        pass

    def validate(self, data: Any, schema: Dict[str, Any]) -> ValidationResult:
        """
        Validate data against JSON schema

        Args:
            data: The data to validate
            schema: The JSON schema to validate against

        Returns:
            ValidationResult with is_valid boolean and error list
        """
        try:
            errors = []
            self._validate_recursive(data, schema, errors, path="root")
            return ValidationResult(len(errors) == 0, errors)
        except Exception as e:
            return ValidationResult(False, [f"Schema validation error: {str(e)}"])

    def validate_json_string(self, json_string: str, schema: Dict[str, Any]) -> ValidationResult:
        """
        Validate JSON string against schema

        Args:
            json_string: JSON string to parse and validate
            schema: The JSON schema to validate against

        Returns:
            ValidationResult with is_valid boolean and error list
        """
        try:
            data = json.loads(json_string)
            return self.validate(data, schema)
        except json.JSONDecodeError as e:
            return ValidationResult(False, [f"JSON parse error: {str(e)}"])

    def _validate_recursive(self, data: Any, schema: Dict[str, Any], errors: List[str], path: str):
        """
        Recursively validate data against schema

        Args:
            data: Current data to validate
            schema: Current schema to validate against
            errors: List to accumulate errors
            path: Current path in data structure for error reporting
        """
        # Handle empty schema (validates anything)
        if not schema:
            return

        # Validate type
        if 'type' in schema:
            if not self._validate_type(data, schema['type'], errors, path):
                return  # Early return on type failure

        # Validate properties for objects
        if schema.get('type') == 'object' and isinstance(data, dict):
            self._validate_object(data, schema, errors, path)

        # Validate items for arrays
        elif schema.get('type') == 'array' and isinstance(data, list):
            self._validate_array(data, schema, errors, path)

        # Validate format for strings
        if schema.get('type') == 'string' and isinstance(data, str):
            self._validate_format(data, schema, errors, path)

    def _validate_type(self, data: Any, expected_type: str, errors: List[str], path: str) -> bool:
        """Validate data type"""
        if expected_type not in self.SUPPORTED_TYPES:
            errors.append(f"Schema error at {path}: Unsupported type '{expected_type}'")
            return False

        # Handle null
        if expected_type == 'null':
            if data is not None:
                errors.append(f"Type error at {path}: Expected null, got {type(data).__name__}")
                return False
            return True

        # Handle other types
        type_checks = {
            'string': lambda x: isinstance(x, str),
            'number': lambda x: isinstance(x, (int, float)),
            'integer': lambda x: isinstance(x, int) and not isinstance(x, bool),
            'boolean': lambda x: isinstance(x, bool),
            'object': lambda x: isinstance(x, dict),
            'array': lambda x: isinstance(x, list)
        }

        if expected_type in type_checks:
            if not type_checks[expected_type](data):
                errors.append(f"Type error at {path}: Expected {expected_type}, got {type(data).__name__}")
                return False

        return True

    def _validate_object(self, data: Dict[str, Any], schema: Dict[str, Any], errors: List[str], path: str):
        """Validate object properties and required fields"""
        # Check required fields
        if 'required' in schema:
            for required_field in schema['required']:
                if required_field not in data:
                    errors.append(f"Required field missing at {path}: '{required_field}'")

        # Validate properties
        if 'properties' in schema:
            for prop_name, prop_schema in schema['properties'].items():
                if prop_name in data:
                    self._validate_recursive(
                        data[prop_name],
                        prop_schema,
                        errors,
                        f"{path}.{prop_name}"
                    )

    def _validate_array(self, data: List[Any], schema: Dict[str, Any], errors: List[str], path: str):
        """Validate array items"""
        if 'items' in schema:
            item_schema = schema['items']
            for i, item in enumerate(data):
                self._validate_recursive(
                    item,
                    item_schema,
                    errors,
                    f"{path}[{i}]"
                )

    def _validate_format(self, data: str, schema: Dict[str, Any], errors: List[str], path: str):
        """Validate string format"""
        if 'format' not in schema:
            return

        format_type = schema['format']

        if format_type == 'email':
            if not self._validate_email(data):
                errors.append(f"Format error at {path}: Invalid email format")

        elif format_type == 'date':
            if not self._validate_date(data):
                errors.append(f"Format error at {path}: Invalid date format (expected YYYY-MM-DD)")

        elif format_type == 'uri':
            if not self._validate_uri(data):
                errors.append(f"Format error at {path}: Invalid URI format")

        else:
            # Unknown format - could be ignored or flagged
            pass

    def _validate_email(self, email: str) -> bool:
        """Validate email format with strict rules"""
        # Basic pattern check
        if not self.EMAIL_PATTERN.match(email):
            return False

        # Additional checks for edge cases
        local, domain = email.split('@', 1)

        # Check for consecutive dots
        if '..' in local or '..' in domain:
            return False

        # Check for leading/trailing dots in local part
        if local.startswith('.') or local.endswith('.'):
            return False

        # Check for leading/trailing dots in domain
        if domain.startswith('.') or domain.endswith('.'):
            return False

        return True

    def _validate_date(self, date: str) -> bool:
        """Validate date format with actual date validity checks"""
        # Basic pattern check
        if not self.DATE_PATTERN.match(date):
            return False

        try:
            year, month, day = map(int, date.split('-'))

            # Basic range checks
            if not (1 <= month <= 12):
                return False

            if not (1 <= day <= 31):
                return False

            # Days per month check
            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

            # Check for leap year
            if month == 2 and self._is_leap_year(year):
                days_in_month[1] = 29

            if day > days_in_month[month - 1]:
                return False

            return True

        except (ValueError, IndexError):
            return False

    def _is_leap_year(self, year: int) -> bool:
        """Check if year is a leap year"""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def _validate_uri(self, uri: str) -> bool:
        """Validate URI format"""
        try:
            result = urlparse(uri)
            # A valid URI should have at least a scheme and netloc (for http/https)
            # or scheme and path (for other schemes like file, mailto)
            if not result.scheme:
                return False

            # For http/https URIs, require netloc
            if result.scheme.lower() in ('http', 'https'):
                return bool(result.netloc)

            # For other schemes, require either netloc or path
            return bool(result.netloc or result.path)
        except Exception:
            return False


# Example usage and testing
if __name__ == '__main__':
    validator = JSONSchemaValidator()

    # Test basic string validation
    schema = {"type": "string"}
    result = validator.validate("hello", schema)
    print(f"String validation: {result}")

    # Test object validation
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        },
        "required": ["name"]
    }

    data = {"name": "John", "age": 30}
    result = validator.validate(data, schema)
    print(f"Object validation (valid): {result}")

    data = {"age": 30}  # missing required name
    result = validator.validate(data, schema)
    print(f"Object validation (invalid): {result}")

    # Test format validation
    schema = {"type": "string", "format": "email"}
    result = validator.validate("test@example.com", schema)
    print(f"Email validation (valid): {result}")

    result = validator.validate("invalid-email", schema)
    print(f"Email validation (invalid): {result}")