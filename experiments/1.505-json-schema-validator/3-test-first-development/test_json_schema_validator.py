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


if __name__ == '__main__':
    unittest.main()