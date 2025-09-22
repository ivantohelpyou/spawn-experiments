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


if __name__ == '__main__':
    unittest.main()