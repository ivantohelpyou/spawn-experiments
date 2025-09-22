"""
Tests for CLI interface functionality.
Following TDD approach for command-line interface.
"""

import pytest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

# Add the jsv module to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from jsv.cli import main, parse_args, CLIValidator


class TestCLIArgumentParsing:
    """Test command-line argument parsing."""

    def test_validate_command_basic(self):
        """Test basic validate command parsing."""
        args = parse_args(['validate', 'data.json', '--schema=schema.json'])
        assert args.command == 'validate'
        assert args.data_file == 'data.json'
        assert args.schema == 'schema.json'

    def test_validate_command_with_output_format(self):
        """Test validate command with output format."""
        args = parse_args(['validate', 'data.json', '--schema=schema.json', '--output=json'])
        assert args.output == 'json'

    def test_batch_command(self):
        """Test batch command parsing."""
        args = parse_args(['batch', '*.json', '--schema=schema.json', '--output=csv'])
        assert args.command == 'batch'
        assert args.pattern == '*.json'
        assert args.output == 'csv'

    def test_check_command(self):
        """Test schema check command parsing."""
        args = parse_args(['check', 'schema.json'])
        assert args.command == 'check'
        assert args.schema_file == 'schema.json'

    def test_quiet_mode(self):
        """Test quiet mode flag."""
        args = parse_args(['validate', 'data.json', '--schema=schema.json', '--quiet'])
        assert args.quiet == True

    def test_stdin_mode(self):
        """Test stdin mode detection."""
        args = parse_args(['validate', '--schema=schema.json'])
        assert args.data_file is None  # Should read from stdin


class TestCLIValidator:
    """Test CLI validator functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cli = CLIValidator()

        # Create temporary files for testing
        self.temp_dir = tempfile.mkdtemp()

        # Sample schema
        self.schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0}
            },
            "required": ["name"]
        }

        # Valid data
        self.valid_data = {"name": "John", "age": 30}

        # Invalid data
        self.invalid_data = {"age": "thirty"}  # Missing name, invalid age type

    def test_validate_file_success(self):
        """Test successful file validation."""
        schema_file = os.path.join(self.temp_dir, 'schema.json')
        data_file = os.path.join(self.temp_dir, 'valid.json')

        with open(schema_file, 'w') as f:
            json.dump(self.schema, f)
        with open(data_file, 'w') as f:
            json.dump(self.valid_data, f)

        result = self.cli.validate_file(data_file, schema_file)
        assert result['valid'] == True
        assert result['file'] == data_file

    def test_validate_file_failure(self):
        """Test failed file validation."""
        schema_file = os.path.join(self.temp_dir, 'schema.json')
        data_file = os.path.join(self.temp_dir, 'invalid.json')

        with open(schema_file, 'w') as f:
            json.dump(self.schema, f)
        with open(data_file, 'w') as f:
            json.dump(self.invalid_data, f)

        result = self.cli.validate_file(data_file, schema_file)
        assert result['valid'] == False
        assert len(result['errors']) > 0
        assert result['file'] == data_file

    def test_validate_stdin(self):
        """Test validation from stdin."""
        schema_file = os.path.join(self.temp_dir, 'schema.json')
        with open(schema_file, 'w') as f:
            json.dump(self.schema, f)

        json_input = json.dumps(self.valid_data)
        with patch('sys.stdin', StringIO(json_input)):
            result = self.cli.validate_stdin(schema_file)
            assert result['valid'] == True

    def test_check_schema_valid(self):
        """Test schema validation check."""
        schema_file = os.path.join(self.temp_dir, 'schema.json')
        with open(schema_file, 'w') as f:
            json.dump(self.schema, f)

        result = self.cli.check_schema(schema_file)
        assert result['valid'] == True

    def test_check_schema_invalid(self):
        """Test invalid schema check."""
        schema_file = os.path.join(self.temp_dir, 'invalid_schema.json')
        invalid_schema = {"type": "unknown_type"}  # Invalid type

        with open(schema_file, 'w') as f:
            json.dump(invalid_schema, f)

        result = self.cli.check_schema(schema_file)
        assert result['valid'] == False

    def test_batch_validation(self):
        """Test batch validation of multiple files."""
        schema_file = os.path.join(self.temp_dir, 'schema.json')
        with open(schema_file, 'w') as f:
            json.dump(self.schema, f)

        # Create multiple test files
        files = []
        for i in range(3):
            data_file = os.path.join(self.temp_dir, f'data{i}.json')
            data = {"name": f"Person{i}", "age": 20 + i}
            with open(data_file, 'w') as f:
                json.dump(data, f)
            files.append(data_file)

        results = self.cli.batch_validate(files, schema_file)
        assert len(results) == 3
        assert all(r['valid'] for r in results)


class TestCLIIntegration:
    """Integration tests for full CLI functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

        # Create test files
        self.schema = {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "website": {"type": "string", "format": "uri"}
            },
            "required": ["email"]
        }

        self.schema_file = os.path.join(self.temp_dir, 'schema.json')
        with open(self.schema_file, 'w') as f:
            json.dump(self.schema, f)

    def test_main_validate_command_success(self):
        """Test main function with validate command - success case."""
        data_file = os.path.join(self.temp_dir, 'data.json')
        data = {"email": "test@example.com", "website": "https://example.com"}
        with open(data_file, 'w') as f:
            json.dump(data, f)

        with patch('sys.argv', ['jsv', 'validate', data_file, f'--schema={self.schema_file}']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                exit_code = main()
                assert exit_code == 0
                output = mock_stdout.getvalue()
                assert "Valid" in output or "✓" in output

    def test_main_validate_command_failure(self):
        """Test main function with validate command - failure case."""
        data_file = os.path.join(self.temp_dir, 'data.json')
        data = {"email": "invalid-email"}  # Invalid email format
        with open(data_file, 'w') as f:
            json.dump(data, f)

        with patch('sys.argv', ['jsv', 'validate', data_file, f'--schema={self.schema_file}']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                exit_code = main()
                assert exit_code == 1
                output = mock_stdout.getvalue()
                assert "Invalid" in output or "✗" in output

    def test_main_quiet_mode(self):
        """Test main function in quiet mode."""
        data_file = os.path.join(self.temp_dir, 'data.json')
        data = {"email": "test@example.com"}
        with open(data_file, 'w') as f:
            json.dump(data, f)

        with patch('sys.argv', ['jsv', 'validate', data_file, f'--schema={self.schema_file}', '--quiet']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                exit_code = main()
                assert exit_code == 0
                output = mock_stdout.getvalue()
                assert output.strip() == ""  # No output in quiet mode