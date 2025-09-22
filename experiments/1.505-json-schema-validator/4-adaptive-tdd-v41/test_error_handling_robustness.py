#!/usr/bin/env python3
"""
Adaptive Validation Tests for Error Handling
Testing robustness of error handling with edge cases
"""

import unittest
import sys
import os

# Add the current directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from json_schema_validator import JSONSchemaValidator


class TestErrorHandlingRobustness(unittest.TestCase):
    """
    Test error handling robustness by testing edge cases that could
    cause crashes or incorrect behavior
    """

    def setUp(self):
        self.validator = JSONSchemaValidator()

    def test_malformed_json_string_handling(self):
        """Test various malformed JSON strings"""
        schema = {"type": "string"}

        malformed_json_strings = [
            '{"incomplete": json}',  # Invalid JSON syntax
            '{"missing": "quote}',   # Missing closing quote
            '{incomplete object',    # Incomplete object
            '[incomplete array',     # Incomplete array
            '',                      # Empty string
            'undefined',             # Invalid literal
            '{"nested": {"incomplete": }',  # Nested incomplete
            '{broken',               # Truncated object
            'true false',            # Multiple values
        ]

        for json_string in malformed_json_strings:
            with self.subTest(json_string=json_string):
                result = self.validator.validate_json_string(json_string, schema)
                self.assertFalse(result.is_valid)
                self.assertGreater(len(result.errors), 0)
                # Should contain parse error message
                self.assertTrue(any("parse" in error.lower() for error in result.errors))

    def test_valid_json_wrong_type(self):
        """Test valid JSON that fails type validation"""
        schema = {"type": "string"}

        valid_json_wrong_types = [
            'null',                  # Valid JSON but null type
            '123',                   # Valid JSON but number type
            'true',                  # Valid JSON but boolean type
            '{"key": "value"}',      # Valid JSON but object type
            '[1, 2, 3]',            # Valid JSON but array type
        ]

        for json_string in valid_json_wrong_types:
            with self.subTest(json_string=json_string):
                result = self.validator.validate_json_string(json_string, schema)
                self.assertFalse(result.is_valid)
                # Should contain type error, not parse error
                self.assertTrue(any("type" in error.lower() for error in result.errors))

    def test_invalid_schema_structures(self):
        """Test various invalid schema structures"""
        data = "test string"

        invalid_schemas = [
            {"type": "nonexistent_type"},
            {"type": 123},  # Type should be string
            {"type": ["string", "number"]},  # Array types not supported in subset
            {"properties": "not_an_object"},  # Properties should be object
            {"required": "not_an_array"},  # Required should be array
            {"items": "not_an_object"},  # Items should be object
            {"format": 123},  # Format should be string
        ]

        for schema in invalid_schemas:
            with self.subTest(schema=schema):
                result = self.validator.validate(data, schema)
                # Should handle gracefully (either fail validation or ignore invalid parts)
                self.assertIsInstance(result.is_valid, bool)
                self.assertIsInstance(result.errors, list)

    def test_deeply_nested_structures(self):
        """Test deeply nested object and array structures"""
        # Create deeply nested schema
        nested_schema = {"type": "object"}
        current = nested_schema
        for i in range(10):  # 10 levels deep
            current["properties"] = {
                "nested": {
                    "type": "object"
                }
            }
            current = current["properties"]["nested"]
        current["properties"] = {"value": {"type": "string"}}

        # Create matching deeply nested data
        nested_data = {}
        current_data = nested_data
        for i in range(10):
            current_data["nested"] = {}
            current_data = current_data["nested"]
        current_data["value"] = "deep_value"

        result = self.validator.validate(nested_data, nested_schema)
        self.assertTrue(result.is_valid)

        # Test with incorrect deep value
        current_data["value"] = 123  # Wrong type
        result = self.validator.validate(nested_data, nested_schema)
        self.assertFalse(result.is_valid)

    def test_null_and_undefined_inputs(self):
        """Test null and undefined input handling"""
        schema = {"type": "string"}

        # Test None data
        result = self.validator.validate(None, schema)
        self.assertFalse(result.is_valid)

        # Test None schema (empty schema should allow anything)
        result = self.validator.validate("test", None)
        # Should handle gracefully - either error or allow
        self.assertIsInstance(result.is_valid, bool)

        # Test empty schema
        result = self.validator.validate("test", {})
        self.assertTrue(result.is_valid)  # Empty schema allows anything

    def test_circular_reference_data(self):
        """Test data with circular references (should not cause infinite loops)"""
        # Create circular reference
        data = {"key": "value"}
        data["self"] = data  # Circular reference

        schema = {
            "type": "object",
            "properties": {
                "key": {"type": "string"}
            }
        }

        # This should not cause infinite recursion
        result = self.validator.validate(data, schema)
        # Should handle gracefully
        self.assertIsInstance(result.is_valid, bool)

    def test_extremely_large_arrays(self):
        """Test handling of large arrays (within reason)"""
        schema = {
            "type": "array",
            "items": {"type": "integer"}
        }

        # Large array with valid data
        large_array = list(range(1000))
        result = self.validator.validate(large_array, schema)
        self.assertTrue(result.is_valid)

        # Large array with one invalid item
        large_array[500] = "invalid"
        result = self.validator.validate(large_array, schema)
        self.assertFalse(result.is_valid)

    def test_unicode_and_special_characters(self):
        """Test handling of unicode and special characters"""
        schema = {"type": "string"}

        special_strings = [
            "普通话",  # Chinese characters
            "🌟🚀💻",  # Emojis
            "test\nwith\nnewlines",  # Newlines
            "test\twith\ttabs",  # Tabs
            "test with 'single' and \"double\" quotes",  # Quotes
            "test\\with\\backslashes",  # Backslashes
            "",  # Empty string
            " ",  # Space only
            "\x00\x01\x02",  # Control characters
        ]

        for test_string in special_strings:
            with self.subTest(test_string=repr(test_string)):
                result = self.validator.validate(test_string, schema)
                self.assertTrue(result.is_valid)

    def test_error_message_quality(self):
        """Test that error messages are informative and helpful"""
        # Test type mismatch error
        schema = {"type": "string"}
        result = self.validator.validate(123, schema)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        # Error should mention type and path
        error_msg = result.errors[0].lower()
        self.assertIn("type", error_msg)
        self.assertIn("root", error_msg)

        # Test missing required field error
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }
        result = self.validator.validate({}, schema)
        self.assertFalse(result.is_valid)
        error_msg = result.errors[0].lower()
        self.assertIn("required", error_msg)
        self.assertIn("name", error_msg)

        # Test format error
        schema = {"type": "string", "format": "email"}
        result = self.validator.validate("invalid-email", schema)
        self.assertFalse(result.is_valid)
        error_msg = result.errors[0].lower()
        self.assertIn("format", error_msg)

    def test_multiple_errors_collection(self):
        """Test that multiple errors are collected properly"""
        schema = {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "age": {"type": "integer"},
                "name": {"type": "string"}
            },
            "required": ["name", "email"]
        }

        # Data with multiple errors
        data = {
            "email": "invalid-email",  # Format error
            "age": "not-a-number",     # Type error
            # Missing required "name"    # Required field error
        }

        result = self.validator.validate(data, schema)
        self.assertFalse(result.is_valid)
        # Should have multiple errors
        self.assertGreaterEqual(len(result.errors), 2)

        # Verify different types of errors are present
        error_text = " ".join(result.errors).lower()
        self.assertTrue(
            "required" in error_text or
            "format" in error_text or
            "type" in error_text
        )


class TestAdaptiveErrorHandlingValidation(unittest.TestCase):
    """
    Test wrong implementations to verify our error handling is robust
    """

    def test_crash_prevention(self):
        """Test that validator doesn't crash on problematic inputs"""
        validator = JSONSchemaValidator()

        # Inputs that might cause crashes in naive implementations
        problematic_inputs = [
            (None, None),
            ({}, None),
            ([], {}),
            ("", {"type": None}),
            ({"recursive": {}}, {"type": "object"}),
        ]

        for data, schema in problematic_inputs:
            with self.subTest(data=data, schema=schema):
                try:
                    result = validator.validate(data, schema)
                    # Should not crash and should return ValidationResult
                    self.assertIsInstance(result.is_valid, bool)
                    self.assertIsInstance(result.errors, list)
                except Exception as e:
                    self.fail(f"Validator crashed on input ({data}, {schema}): {e}")


if __name__ == '__main__':
    # Run the error handling robustness tests
    print("Running adaptive validation tests for error handling...")
    unittest.main(verbosity=2)