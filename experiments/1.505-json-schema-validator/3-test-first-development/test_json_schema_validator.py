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

    def test_validate_email_format_valid(self):
        """Test validating a valid email against email format schema"""
        schema = {"type": "string", "format": "email"}
        data = "test@example.com"
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validate_email_format_invalid(self):
        """Test validating an invalid email against email format schema"""
        schema = {"type": "string", "format": "email"}
        data = "not-an-email"
        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)
        self.assertTrue(len(result.errors) > 0)

    def test_validate_with_empty_schema(self):
        """Test validating data with empty schema"""
        schema = {}
        data = "anything"
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validate_null_data(self):
        """Test validating null data"""
        schema = {"type": "null"}
        data = None
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validate_boolean_type(self):
        """Test validating boolean type"""
        schema = {"type": "boolean"}
        data = True
        result = self.validator.validate(data, schema)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validate_number_type(self):
        """Test validating number type (accepts both int and float)"""
        schema = {"type": "number"}

        # Test integer
        result1 = self.validator.validate(42, schema)
        self.assertTrue(result1.is_valid)

        # Test float
        result2 = self.validator.validate(3.14, schema)
        self.assertTrue(result2.is_valid)


if __name__ == '__main__':
    unittest.main()