#!/usr/bin/env python3
"""
Test suite for JSON Schema Validator - TDD Implementation
Following JSON Schema Draft 7 subset requirements
"""

import unittest
import json
from json_schema_validator import JSONSchemaValidator


class TestJSONSchemaValidator(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.validator = JSONSchemaValidator()

    # Basic Type Validation Tests
    def test_string_validation_valid(self):
        """Test valid string against string schema"""
        schema = {"type": "string"}
        data = "hello world"
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    def test_string_validation_invalid(self):
        """Test invalid type against string schema"""
        schema = {"type": "string"}
        data = 123
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("type", result.errors[0].lower())

    def test_number_validation_valid(self):
        """Test valid number against number schema"""
        schema = {"type": "number"}
        data = 42.5
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)

    def test_integer_validation_valid(self):
        """Test valid integer against integer schema"""
        schema = {"type": "integer"}
        data = 42
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)

    def test_integer_validation_invalid_float(self):
        """Test float against integer schema should fail"""
        schema = {"type": "integer"}
        data = 42.5
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)

    def test_boolean_validation_valid(self):
        """Test valid boolean against boolean schema"""
        schema = {"type": "boolean"}
        data = True
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)

    def test_array_validation_valid(self):
        """Test valid array against array schema"""
        schema = {"type": "array", "items": {"type": "string"}}
        data = ["hello", "world"]
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)

    def test_array_validation_invalid_items(self):
        """Test array with invalid item types"""
        schema = {"type": "array", "items": {"type": "string"}}
        data = ["hello", 123]
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)

    # Object Validation Tests
    def test_object_validation_valid(self):
        """Test valid object against object schema"""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        data = {"name": "John", "age": 30}
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)

    def test_object_validation_required_fields(self):
        """Test object with required fields"""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name"]
        }
        data = {"age": 30}  # missing required "name"
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)
        self.assertIn("required", result.errors[0].lower())

    def test_object_validation_extra_properties(self):
        """Test object with extra properties (should be allowed by default)"""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }
        data = {"name": "John", "extra": "value"}
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)

    # Format Validation Tests
    def test_email_format_valid(self):
        """Test valid email format"""
        schema = {"type": "string", "format": "email"}
        data = "test@example.com"
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)

    def test_email_format_invalid(self):
        """Test invalid email format"""
        schema = {"type": "string", "format": "email"}
        data = "invalid-email"
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)
        self.assertIn("format", result.errors[0].lower())

    def test_date_format_valid(self):
        """Test valid date format (ISO 8601)"""
        schema = {"type": "string", "format": "date"}
        data = "2023-12-25"
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)

    def test_date_format_invalid(self):
        """Test invalid date format"""
        schema = {"type": "string", "format": "date"}
        data = "25-12-2023"
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)

    def test_uri_format_valid(self):
        """Test valid URI format"""
        schema = {"type": "string", "format": "uri"}
        data = "https://example.com/path"
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)

    def test_uri_format_invalid(self):
        """Test invalid URI format"""
        schema = {"type": "string", "format": "uri"}
        data = "not-a-uri"
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)

    # Error Handling Tests
    def test_malformed_json_data(self):
        """Test malformed JSON data handling"""
        schema = {"type": "string"}
        # This will be tested by passing a string that would be invalid JSON
        # if parsed from a JSON string
        result = self.validator.validate_json_string('{"invalid": json}', schema)
        self.assertFalse(result.is_valid)
        self.assertIn("parse", result.errors[0].lower())

    def test_invalid_schema_structure(self):
        """Test handling of invalid schema"""
        schema = {"type": "invalid_type"}
        data = "test"
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)
        self.assertIn("schema", result.errors[0].lower())

    def test_empty_data(self):
        """Test empty/null data handling"""
        schema = {"type": "string"}
        result = self.validator.validate(None, schema)
        self.assertFalse(result.is_valid)

    def test_empty_schema(self):
        """Test empty schema handling"""
        data = "test"
        result = self.validator.validate(data, {})
        # Empty schema should validate anything as true
        self.assertTrue(result.is_valid)

    # Edge Cases Tests
    def test_nested_object_validation(self):
        """Test nested object validation"""
        schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "profile": {
                            "type": "object",
                            "properties": {
                                "email": {"type": "string", "format": "email"}
                            },
                            "required": ["email"]
                        }
                    },
                    "required": ["name", "profile"]
                }
            },
            "required": ["user"]
        }

        data = {
            "user": {
                "name": "John",
                "profile": {
                    "email": "john@example.com"
                }
            }
        }
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)

    def test_array_of_objects_validation(self):
        """Test array of objects validation"""
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                },
                "required": ["id"]
            }
        }

        data = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"}
        ]
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)

    def test_mixed_type_array_validation(self):
        """Test array with mixed types (should fail with typed items)"""
        schema = {
            "type": "array",
            "items": {"type": "string"}
        }
        data = ["string", 123, True]
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)


class TestValidationResult(unittest.TestCase):
    """Test the ValidationResult class behavior"""

    def test_validation_result_structure(self):
        """Test that ValidationResult has required attributes"""
        from json_schema_validator import ValidationResult

        result = ValidationResult(True, [])
        self.assertTrue(hasattr(result, 'is_valid'))
        self.assertTrue(hasattr(result, 'errors'))
        self.assertIsInstance(result.errors, list)

    def test_validation_result_with_errors(self):
        """Test ValidationResult with error messages"""
        from json_schema_validator import ValidationResult

        errors = ["Type mismatch", "Required field missing"]
        result = ValidationResult(False, errors)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 2)
        self.assertEqual(result.errors, errors)


if __name__ == '__main__':
    unittest.main()