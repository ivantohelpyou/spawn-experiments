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


class TestCLIArgumentParsing(unittest.TestCase):
    """Test cases for CLI argument parsing functionality."""

    def test_parse_validate_command_with_schema(self):
        """Test parsing validate command with schema argument."""
        # This test will fail initially (RED) because parse_args doesn't exist yet
        from jsv import parse_args

        args = parse_args(['validate', 'data.json', '--schema', 'schema.json'])
        self.assertEqual(args.command, 'validate')
        self.assertEqual(args.input_file, 'data.json')
        self.assertEqual(args.schema, 'schema.json')

    def test_parse_batch_command_with_output_format(self):
        """Test parsing batch command with output format."""
        from jsv import parse_args

        args = parse_args(['batch', '*.json', '--schema', 'schema.json', '--output', 'csv'])
        self.assertEqual(args.command, 'batch')
        self.assertEqual(args.pattern, '*.json')
        self.assertEqual(args.schema, 'schema.json')
        self.assertEqual(args.output, 'csv')

    def test_parse_check_command(self):
        """Test parsing schema check command."""
        from jsv import parse_args

        args = parse_args(['check', 'schema.json'])
        self.assertEqual(args.command, 'check')
        self.assertEqual(args.schema_file, 'schema.json')

    def test_parse_validate_with_quiet_mode(self):
        """Test parsing validate command with quiet flag."""
        from jsv import parse_args

        args = parse_args(['validate', 'data.json', '--schema', 'schema.json', '--quiet'])
        self.assertEqual(args.command, 'validate')
        self.assertTrue(args.quiet)


if __name__ == '__main__':
    unittest.main()