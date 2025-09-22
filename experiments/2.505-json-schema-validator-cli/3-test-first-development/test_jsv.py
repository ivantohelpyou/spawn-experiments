#!/usr/bin/env python3
"""
Test suite for JSON Schema Validator CLI tool.
Following strict TDD principles with Red-Green-Refactor cycle.
"""

import unittest
import json
import os
import tempfile
import subprocess
import sys
from unittest.mock import patch, mock_open
from io import StringIO


class TestJSONSchemaValidator(unittest.TestCase):
    """Test cases for JSON Schema Validator core functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0}
            },
            "required": ["name"]
        }

        self.valid_data = {
            "name": "John Doe",
            "age": 30
        }

        self.invalid_data = {
            "age": -5  # Missing required "name" field and negative age
        }

    def test_basic_validation_valid_data(self):
        """Test basic validation with valid data should return True."""
        # This test will fail initially (RED) because jsv module doesn't exist yet
        from jsv import validate_json

        result = validate_json(self.valid_data, self.valid_schema)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    def test_basic_validation_invalid_data(self):
        """Test basic validation with invalid data should return False."""
        from jsv import validate_json

        result = validate_json(self.invalid_data, self.valid_schema)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)


if __name__ == '__main__':
    unittest.main()