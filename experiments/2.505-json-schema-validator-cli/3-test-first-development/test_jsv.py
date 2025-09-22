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
import shutil
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


class TestFileValidation(unittest.TestCase):
    """Test cases for file-based validation functionality."""

    def setUp(self):
        """Set up test fixtures with temporary files."""
        self.test_dir = tempfile.mkdtemp()

        # Create test schema file
        self.schema_data = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0}
            },
            "required": ["name"]
        }
        self.schema_file = os.path.join(self.test_dir, 'schema.json')
        with open(self.schema_file, 'w') as f:
            json.dump(self.schema_data, f)

        # Create valid test data file
        self.valid_data = {"name": "John Doe", "age": 30}
        self.valid_file = os.path.join(self.test_dir, 'valid.json')
        with open(self.valid_file, 'w') as f:
            json.dump(self.valid_data, f)

        # Create invalid test data file
        self.invalid_data = {"age": -5}  # Missing name, negative age
        self.invalid_file = os.path.join(self.test_dir, 'invalid.json')
        with open(self.invalid_file, 'w') as f:
            json.dump(self.invalid_data, f)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir)

    def test_validate_file_with_valid_data(self):
        """Test file validation with valid data."""
        # This test will fail initially (RED) because validate_file doesn't exist yet
        from jsv import validate_file

        result = validate_file(self.valid_file, self.schema_file)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(result.file_path, self.valid_file)

    def test_validate_file_with_invalid_data(self):
        """Test file validation with invalid data."""
        from jsv import validate_file

        result = validate_file(self.invalid_file, self.schema_file)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertEqual(result.file_path, self.invalid_file)

    def test_validate_file_with_nonexistent_data_file(self):
        """Test file validation with non-existent data file."""
        from jsv import validate_file

        nonexistent_file = os.path.join(self.test_dir, 'nonexistent.json')
        result = validate_file(nonexistent_file, self.schema_file)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("not found", result.errors[0].lower())

    def test_validate_file_with_nonexistent_schema_file(self):
        """Test file validation with non-existent schema file."""
        from jsv import validate_file

        nonexistent_schema = os.path.join(self.test_dir, 'nonexistent_schema.json')
        result = validate_file(self.valid_file, nonexistent_schema)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("schema", result.errors[0].lower())

    def test_validate_file_with_malformed_json(self):
        """Test file validation with malformed JSON."""
        from jsv import validate_file

        malformed_file = os.path.join(self.test_dir, 'malformed.json')
        with open(malformed_file, 'w') as f:
            f.write('{"name": "John", "age":}')  # Invalid JSON

        result = validate_file(malformed_file, self.schema_file)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("json", result.errors[0].lower())


class TestBatchValidation(unittest.TestCase):
    """Test cases for batch validation functionality."""

    def setUp(self):
        """Set up test fixtures with multiple files."""
        self.test_dir = tempfile.mkdtemp()

        # Create test schema file
        self.schema_data = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0}
            },
            "required": ["name"]
        }
        self.schema_file = os.path.join(self.test_dir, 'schema.json')
        with open(self.schema_file, 'w') as f:
            json.dump(self.schema_data, f)

        # Create multiple valid test data files
        self.valid_files = []
        for i in range(3):
            valid_data = {"name": f"Person {i}", "age": 20 + i}
            valid_file = os.path.join(self.test_dir, f'valid_{i}.json')
            with open(valid_file, 'w') as f:
                json.dump(valid_data, f)
            self.valid_files.append(valid_file)

        # Create multiple invalid test data files
        self.invalid_files = []
        for i in range(2):
            invalid_data = {"age": -i}  # Missing name, negative age
            invalid_file = os.path.join(self.test_dir, f'invalid_{i}.json')
            with open(invalid_file, 'w') as f:
                json.dump(invalid_data, f)
            self.invalid_files.append(invalid_file)

        self.all_files = self.valid_files + self.invalid_files

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_batch_validate_files_mixed_results(self):
        """Test batch validation with mixed valid and invalid files."""
        # This test will fail initially (RED) because batch_validate doesn't exist yet
        from jsv import batch_validate

        results = batch_validate(self.all_files, self.schema_file)
        self.assertEqual(len(results), 5)  # 3 valid + 2 invalid

        # Check that we have 3 valid results
        valid_results = [r for r in results if r.is_valid]
        self.assertEqual(len(valid_results), 3)

        # Check that we have 2 invalid results
        invalid_results = [r for r in results if not r.is_valid]
        self.assertEqual(len(invalid_results), 2)

    def test_batch_validate_with_glob_pattern(self):
        """Test batch validation using glob pattern."""
        from jsv import batch_validate_pattern

        results = batch_validate_pattern(os.path.join(self.test_dir, '*.json'), self.schema_file)
        # Should find 5 JSON files (3 valid + 2 invalid), excluding schema.json
        data_files = [r for r in results if not r.file_path.endswith('schema.json')]
        self.assertEqual(len(data_files), 5)

    def test_batch_validate_empty_file_list(self):
        """Test batch validation with empty file list."""
        from jsv import batch_validate

        results = batch_validate([], self.schema_file)
        self.assertEqual(len(results), 0)

    def test_batch_validate_with_nonexistent_files(self):
        """Test batch validation with some non-existent files."""
        from jsv import batch_validate

        files_with_missing = self.valid_files + [os.path.join(self.test_dir, 'missing.json')]
        results = batch_validate(files_with_missing, self.schema_file)
        self.assertEqual(len(results), 4)

        # Check that missing file result is invalid
        missing_result = [r for r in results if 'missing.json' in r.file_path][0]
        self.assertFalse(missing_result.is_valid)
        self.assertIn("not found", missing_result.errors[0].lower())


class TestOutputFormats(unittest.TestCase):
    """Test cases for output formatting functionality."""

    def setUp(self):
        """Set up test fixtures."""
        from jsv import ValidationResult

        self.valid_result = ValidationResult(
            is_valid=True,
            errors=[],
            file_path="/test/valid.json"
        )
        self.invalid_result = ValidationResult(
            is_valid=False,
            errors=["Required field 'name' is missing", "Value -5 is less than minimum 0"],
            file_path="/test/invalid.json"
        )
        self.results = [self.valid_result, self.invalid_result]

    def test_format_text_output_single_result(self):
        """Test text output formatting for single result."""
        # This test will fail initially (RED) because format_text doesn't exist yet
        from jsv import format_text

        output = format_text([self.valid_result])
        self.assertIn("valid.json", output)
        self.assertIn("VALID", output)

        output = format_text([self.invalid_result])
        self.assertIn("invalid.json", output)
        self.assertIn("INVALID", output)
        self.assertIn("Required field 'name' is missing", output)

    def test_format_json_output_multiple_results(self):
        """Test JSON output formatting for multiple results."""
        from jsv import format_json

        output = format_json(self.results)
        parsed = json.loads(output)

        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]['file_path'], '/test/valid.json')
        self.assertTrue(parsed[0]['is_valid'])
        self.assertEqual(len(parsed[0]['errors']), 0)

        self.assertEqual(parsed[1]['file_path'], '/test/invalid.json')
        self.assertFalse(parsed[1]['is_valid'])
        self.assertEqual(len(parsed[1]['errors']), 2)

    def test_format_csv_output_multiple_results(self):
        """Test CSV output formatting for multiple results."""
        from jsv import format_csv

        output = format_csv(self.results)
        lines = output.strip().split('\n')

        # Check header
        self.assertIn("file_path", lines[0])
        self.assertIn("is_valid", lines[0])
        self.assertIn("error_count", lines[0])

        # Check data rows
        self.assertEqual(len(lines), 3)  # Header + 2 data rows
        self.assertIn("valid.json", lines[1])
        self.assertIn("True", lines[1])
        self.assertIn("invalid.json", lines[2])
        self.assertIn("False", lines[2])

    def test_format_quiet_output(self):
        """Test quiet mode formatting (no output, just return codes)."""
        from jsv import format_quiet

        # Valid results should return empty string and indicate success
        output, exit_code = format_quiet([self.valid_result])
        self.assertEqual(output, "")
        self.assertEqual(exit_code, 0)

        # Invalid results should return empty string and indicate failure
        output, exit_code = format_quiet([self.invalid_result])
        self.assertEqual(output, "")
        self.assertEqual(exit_code, 1)

        # Mixed results should indicate failure
        output, exit_code = format_quiet(self.results)
        self.assertEqual(output, "")
        self.assertEqual(exit_code, 1)


class TestSchemaVerification(unittest.TestCase):
    """Test cases for schema verification functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

        # Valid JSON Schema
        self.valid_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0}
            },
            "required": ["name"]
        }
        self.valid_schema_file = os.path.join(self.test_dir, 'valid_schema.json')
        with open(self.valid_schema_file, 'w') as f:
            json.dump(self.valid_schema, f)

        # Invalid JSON Schema (missing type)
        self.invalid_schema = {
            "properties": {
                "name": {"type": "unknown_type"}  # Invalid type
            }
        }
        self.invalid_schema_file = os.path.join(self.test_dir, 'invalid_schema.json')
        with open(self.invalid_schema_file, 'w') as f:
            json.dump(self.invalid_schema, f)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_verify_valid_schema(self):
        """Test schema verification with valid schema."""
        # This test will fail initially (RED) because verify_schema doesn't exist yet
        from jsv import verify_schema

        result = verify_schema(self.valid_schema_file)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    def test_verify_invalid_schema(self):
        """Test schema verification with invalid schema."""
        from jsv import verify_schema

        result = verify_schema(self.invalid_schema_file)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

    def test_verify_nonexistent_schema(self):
        """Test schema verification with non-existent file."""
        from jsv import verify_schema

        nonexistent_file = os.path.join(self.test_dir, 'nonexistent.json')
        result = verify_schema(nonexistent_file)
        self.assertFalse(result.is_valid)
        self.assertIn("not found", result.errors[0].lower())


class TestMainCLI(unittest.TestCase):
    """Test cases for main CLI functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

        # Create test files
        self.schema_data = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0}
            },
            "required": ["name"]
        }
        self.schema_file = os.path.join(self.test_dir, 'schema.json')
        with open(self.schema_file, 'w') as f:
            json.dump(self.schema_data, f)

        self.valid_data = {"name": "John", "age": 30}
        self.valid_file = os.path.join(self.test_dir, 'valid.json')
        with open(self.valid_file, 'w') as f:
            json.dump(self.valid_data, f)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_main_validate_command(self):
        """Test main CLI with validate command."""
        # This test will fail initially (RED) because main doesn't exist yet
        from jsv import main

        # Mock sys.argv for validate command
        test_args = ['jsv', 'validate', self.valid_file, '--schema', self.schema_file]

        with patch('sys.argv', test_args):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()
                self.assertEqual(result, 0)  # Success exit code
                output = mock_stdout.getvalue()
                self.assertIn("VALID", output)

    def test_main_check_command(self):
        """Test main CLI with check command."""
        from jsv import main

        test_args = ['jsv', 'check', self.schema_file]

        with patch('sys.argv', test_args):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()
                self.assertEqual(result, 0)  # Success exit code

    def test_main_quiet_mode(self):
        """Test main CLI in quiet mode."""
        from jsv import main

        test_args = ['jsv', 'validate', self.valid_file, '--schema', self.schema_file, '--quiet']

        with patch('sys.argv', test_args):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()
                self.assertEqual(result, 0)  # Success exit code
                output = mock_stdout.getvalue()
                self.assertEqual(output, "")  # No output in quiet mode


class TestStdinOperations(unittest.TestCase):
    """Test cases for stdin pipeline operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

        # Create test schema file
        self.schema_data = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0}
            },
            "required": ["name"]
        }
        self.schema_file = os.path.join(self.test_dir, 'schema.json')
        with open(self.schema_file, 'w') as f:
            json.dump(self.schema_data, f)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_validate_from_stdin_valid_data(self):
        """Test validation from stdin with valid data."""
        # This test will fail initially (RED) because validate_stdin doesn't exist yet
        from jsv import validate_stdin

        valid_data = {"name": "John", "age": 30}
        json_input = json.dumps(valid_data)

        result = validate_stdin(json_input, self.schema_file)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(result.file_path, "stdin")

    def test_validate_from_stdin_invalid_data(self):
        """Test validation from stdin with invalid data."""
        from jsv import validate_stdin

        invalid_data = {"age": -5}  # Missing name, negative age
        json_input = json.dumps(invalid_data)

        result = validate_stdin(json_input, self.schema_file)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

    def test_validate_from_stdin_malformed_json(self):
        """Test validation from stdin with malformed JSON."""
        from jsv import validate_stdin

        malformed_input = '{"name": "John", "age":}'

        result = validate_stdin(malformed_input, self.schema_file)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("json", result.errors[0].lower())

    def test_main_cli_with_stdin(self):
        """Test main CLI reading from stdin."""
        from jsv import main

        valid_data = {"name": "John", "age": 30}
        json_input = json.dumps(valid_data)

        test_args = ['jsv', 'validate', '-', '--schema', self.schema_file]

        with patch('sys.argv', test_args):
            with patch('sys.stdin.read', return_value=json_input):
                with patch('sys.stdout', new=StringIO()) as mock_stdout:
                    result = main()
                    self.assertEqual(result, 0)  # Success exit code
                    output = mock_stdout.getvalue()
                    self.assertIn("VALID", output)


if __name__ == '__main__':
    unittest.main()