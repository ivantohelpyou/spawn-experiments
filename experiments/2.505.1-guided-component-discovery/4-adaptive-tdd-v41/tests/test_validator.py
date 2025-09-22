"""
Tests for core JSON Schema validation functionality.
Following TDD approach - tests written first.
"""

import pytest
import json
from jsv.validator import JSONSchemaValidator


class TestJSONSchemaValidator:
    """Test cases for core JSON Schema validation."""

    def test_validate_simple_string_type(self):
        """Test validation of simple string type constraint."""
        schema = {"type": "string"}
        validator = JSONSchemaValidator(schema)

        assert validator.validate("hello") == True
        assert validator.validate(123) == False
        assert validator.validate(None) == False

    def test_validate_simple_number_type(self):
        """Test validation of simple number type constraint."""
        schema = {"type": "number"}
        validator = JSONSchemaValidator(schema)

        assert validator.validate(123) == True
        assert validator.validate(123.45) == True
        assert validator.validate("123") == False

    def test_validate_integer_type(self):
        """Test validation of integer type constraint."""
        schema = {"type": "integer"}
        validator = JSONSchemaValidator(schema)

        assert validator.validate(123) == True
        assert validator.validate(123.0) == True  # JSON integers can be floats with .0
        assert validator.validate(123.45) == False
        assert validator.validate("123") == False

    def test_validate_boolean_type(self):
        """Test validation of boolean type constraint."""
        schema = {"type": "boolean"}
        validator = JSONSchemaValidator(schema)

        assert validator.validate(True) == True
        assert validator.validate(False) == True
        assert validator.validate(1) == False
        assert validator.validate("true") == False

    def test_validate_null_type(self):
        """Test validation of null type constraint."""
        schema = {"type": "null"}
        validator = JSONSchemaValidator(schema)

        assert validator.validate(None) == True
        assert validator.validate("null") == False
        assert validator.validate(0) == False

    def test_validate_object_type(self):
        """Test validation of object type constraint."""
        schema = {"type": "object"}
        validator = JSONSchemaValidator(schema)

        assert validator.validate({}) == True
        assert validator.validate({"key": "value"}) == True
        assert validator.validate([]) == False
        assert validator.validate("{}") == False

    def test_validate_array_type(self):
        """Test validation of array type constraint."""
        schema = {"type": "array"}
        validator = JSONSchemaValidator(schema)

        assert validator.validate([]) == True
        assert validator.validate([1, 2, 3]) == True
        assert validator.validate({}) == False
        assert validator.validate("[]") == False

    def test_validate_required_fields(self):
        """Test validation of required object properties."""
        schema = {
            "type": "object",
            "required": ["name", "age"]
        }
        validator = JSONSchemaValidator(schema)

        assert validator.validate({"name": "John", "age": 30}) == True
        assert validator.validate({"name": "John"}) == False
        assert validator.validate({"age": 30}) == False
        assert validator.validate({}) == False

    def test_validate_object_properties(self):
        """Test validation of object property types."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        validator = JSONSchemaValidator(schema)

        assert validator.validate({"name": "John", "age": 30}) == True
        assert validator.validate({"name": "John", "age": "30"}) == False
        assert validator.validate({"name": 123, "age": 30}) == False

    def test_validate_string_constraints(self):
        """Test validation of string length constraints."""
        schema = {
            "type": "string",
            "minLength": 2,
            "maxLength": 10
        }
        validator = JSONSchemaValidator(schema)

        assert validator.validate("hello") == True
        assert validator.validate("hi") == True
        assert validator.validate("h") == False
        assert validator.validate("this is too long") == False

    def test_validate_number_constraints(self):
        """Test validation of number range constraints."""
        schema = {
            "type": "number",
            "minimum": 0,
            "maximum": 100
        }
        validator = JSONSchemaValidator(schema)

        assert validator.validate(50) == True
        assert validator.validate(0) == True
        assert validator.validate(100) == True
        assert validator.validate(-1) == False
        assert validator.validate(101) == False

    def test_validate_with_errors(self):
        """Test that validator provides detailed error information."""
        schema = {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string"}
            }
        }
        validator = JSONSchemaValidator(schema)

        result = validator.validate_with_errors({"name": 123})
        assert result['valid'] == False
        assert len(result['errors']) > 0
        assert 'name' in str(result['errors'][0])

    def test_validate_json_from_string(self):
        """Test validation of JSON data from string format."""
        schema = {"type": "object"}
        validator = JSONSchemaValidator(schema)

        result = validator.validate_json_string('{"key": "value"}')
        assert result == True

        result = validator.validate_json_string('invalid json')
        assert result == False