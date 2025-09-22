import unittest
import json
from json_schema_validator import JSONSchemaValidator


class TestJSONSchemaValidator(unittest.TestCase):

    def setUp(self):
        self.validator = JSONSchemaValidator()

    def test_validate_simple_string_type_valid(self):
        """Test validating a string against string type schema"""
        schema = {"type": "string"}
        data = "hello world"
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validate_simple_string_type_invalid(self):
        """Test validating a non-string against string type schema"""
        schema = {"type": "string"}
        data = 123
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)
        self.assertIn("Expected type 'string'", result.errors[0])

    def test_validate_integer_type_valid(self):
        """Test validating an integer against integer type schema"""
        schema = {"type": "integer"}
        data = 42
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validate_integer_type_invalid_float(self):
        """Test validating a float against integer type schema"""
        schema = {"type": "integer"}
        data = 42.5
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)
        self.assertIn("Expected type 'integer'", result.errors[0])

    def test_validate_object_with_properties_valid(self):
        """Test validating an object with properties schema"""
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
        self.assertEqual(result.errors, [])

    def test_validate_object_with_properties_invalid(self):
        """Test validating an object with invalid property types"""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        data = {"name": "John", "age": "thirty"}  # age should be integer, not string
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)
        self.assertTrue(len(result.errors) > 0)

    def test_validate_object_with_required_properties_valid(self):
        """Test validating an object with all required properties"""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }
        data = {"name": "John", "age": 30}
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validate_object_with_required_properties_missing(self):
        """Test validating an object missing required properties"""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }
        data = {"name": "John"}  # missing required 'age' property
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)
        self.assertIn("Required property 'age' is missing", result.errors[0])

    def test_validate_array_type_valid(self):
        """Test validating an array against array type schema"""
        schema = {"type": "array"}
        data = [1, 2, 3]
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validate_array_type_invalid(self):
        """Test validating a non-array against array type schema"""
        schema = {"type": "array"}
        data = "not an array"
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)
        self.assertIn("Expected type 'array'", result.errors[0])


if __name__ == '__main__':
    unittest.main()