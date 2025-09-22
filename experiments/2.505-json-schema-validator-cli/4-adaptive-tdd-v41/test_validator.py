#!/usr/bin/env python3
"""
Tests for JSON Schema Validator CLI tool.
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add the current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from validator import JSONSchemaValidator, ValidationResult


class TestJSONSchemaValidator(unittest.TestCase):
    """Test the core JSON Schema Validator functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = JSONSchemaValidator()

        # Sample valid schema
        self.valid_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0},
                "email": {"type": "string", "format": "email"}
            },
            "required": ["name"]
        }

        # Sample valid data
        self.valid_data = {
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com"
        }

        # Sample invalid data
        self.invalid_data = {
            "age": -5,
            "email": "not-an-email"
        }

    def test_validate_valid_data(self):
        """Test validation of valid data against schema."""
        result = self.validator.validate(self.valid_data, self.valid_schema)

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    def test_validate_invalid_data(self):
        """Test validation of invalid data against schema."""
        result = self.validator.validate(self.invalid_data, self.valid_schema)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

    def test_validate_file_valid(self):
        """Test validation of valid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_data, f)
            f.flush()

            result = self.validator.validate_file(f.name, self.valid_schema)
            self.assertTrue(result.is_valid)

            # Clean up
            os.unlink(f.name)

    def test_validate_file_invalid_json(self):
        """Test validation of file with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json")
            f.flush()

            result = self.validator.validate_file(f.name, self.valid_schema)
            self.assertFalse(result.is_valid)
            self.assertIn("JSON parse error", str(result.errors[0]))

            # Clean up
            os.unlink(f.name)

    def test_validate_file_nonexistent(self):
        """Test validation of non-existent file."""
        result = self.validator.validate_file("/nonexistent/file.json", self.valid_schema)
        self.assertFalse(result.is_valid)
        self.assertIn("File not found", str(result.errors[0]))

    def test_schema_validation(self):
        """Test schema validation functionality."""
        # Valid schema
        result = self.validator.validate_schema(self.valid_schema)
        self.assertTrue(result.is_valid)

        # Invalid schema
        invalid_schema = {"type": "invalid_type"}
        result = self.validator.validate_schema(invalid_schema)
        self.assertFalse(result.is_valid)


class TestValidationResult(unittest.TestCase):
    """Test the ValidationResult class."""

    def test_valid_result(self):
        """Test creating a valid result."""
        result = ValidationResult(True, [])
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    def test_invalid_result(self):
        """Test creating an invalid result."""
        errors = ["Error 1", "Error 2"]
        result = ValidationResult(False, errors)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors, errors)


if __name__ == '__main__':
    unittest.main()