"""Tests for the CLI interface."""

import json
import tempfile
import pytest
from pathlib import Path
from click.testing import CliRunner

from jsv.cli import cli


class TestCLI:
    """Test cases for CLI commands."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create test schema
        self.test_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "email": {"type": "string", "format": "email"}
            },
            "required": ["name", "email"]
        }

        # Create temporary schema file
        self.schema_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.test_schema, self.schema_file)
        self.schema_file.close()

        self.runner = CliRunner()

    def teardown_method(self):
        """Clean up test fixtures."""
        Path(self.schema_file.name).unlink(missing_ok=True)

    def test_cli_help(self):
        """Test CLI help output."""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'JSON Schema Validator CLI' in result.output

    def test_cli_version(self):
        """Test CLI version output."""
        result = self.runner.invoke(cli, ['--version'])
        assert result.exit_code == 0

    def test_validate_command_help(self):
        """Test validate command help."""
        result = self.runner.invoke(cli, ['validate', '--help'])
        assert result.exit_code == 0
        assert 'Validate a JSON file against a schema' in result.output

    def test_validate_valid_file(self):
        """Test validating a valid JSON file."""
        # Create valid test data
        valid_data = {"name": "John Doe", "email": "john@example.com"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(valid_data, f)
            data_file = f.name

        try:
            result = self.runner.invoke(cli, [
                'validate', data_file,
                '--schema', self.schema_file.name
            ])

            assert result.exit_code == 0
            assert 'Valid' in result.output
            assert '✓' in result.output or 'Valid' in result.output

        finally:
            Path(data_file).unlink(missing_ok=True)

    def test_validate_invalid_file(self):
        """Test validating an invalid JSON file."""
        # Create invalid test data
        invalid_data = {"name": "", "email": "not-an-email"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(invalid_data, f)
            data_file = f.name

        try:
            result = self.runner.invoke(cli, [
                'validate', data_file,
                '--schema', self.schema_file.name
            ])

            assert result.exit_code == 1
            assert 'Invalid' in result.output

        finally:
            Path(data_file).unlink(missing_ok=True)

    def test_validate_missing_schema(self):
        """Test validate command without schema argument."""
        result = self.runner.invoke(cli, ['validate', 'test.json'])
        assert result.exit_code != 0
        assert 'Missing option' in result.output or 'required' in result.output.lower()

    def test_validate_nonexistent_file(self):
        """Test validating non-existent file."""
        result = self.runner.invoke(cli, [
            'validate', 'nonexistent.json',
            '--schema', self.schema_file.name
        ])

        assert result.exit_code == 3  # File error
        assert 'not found' in result.output.lower() or 'error' in result.output.lower()

    def test_validate_stdin(self):
        """Test validating JSON from stdin."""
        valid_data = {"name": "John Doe", "email": "john@example.com"}
        json_input = json.dumps(valid_data)

        result = self.runner.invoke(cli, [
            'validate',
            '--schema', self.schema_file.name
        ], input=json_input)

        assert result.exit_code == 0
        assert 'Valid' in result.output

    def test_validate_stdin_invalid(self):
        """Test validating invalid JSON from stdin."""
        invalid_data = {"name": "", "email": "not-an-email"}
        json_input = json.dumps(invalid_data)

        result = self.runner.invoke(cli, [
            'validate',
            '--schema', self.schema_file.name
        ], input=json_input)

        assert result.exit_code == 1
        assert 'Invalid' in result.output

    def test_validate_quiet_mode(self):
        """Test validate command in quiet mode."""
        valid_data = {"name": "John Doe", "email": "john@example.com"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(valid_data, f)
            data_file = f.name

        try:
            result = self.runner.invoke(cli, [
                '--quiet',
                'validate', data_file,
                '--schema', self.schema_file.name
            ])

            assert result.exit_code == 0
            assert result.output.strip() == ""

        finally:
            Path(data_file).unlink(missing_ok=True)

    def test_validate_json_output(self):
        """Test validate command with JSON output."""
        valid_data = {"name": "John Doe", "email": "john@example.com"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(valid_data, f)
            data_file = f.name

        try:
            result = self.runner.invoke(cli, [
                '--output', 'json',
                'validate', data_file,
                '--schema', self.schema_file.name
            ])

            assert result.exit_code == 0

            # Parse output as JSON to verify it's valid
            output_data = json.loads(result.output)
            assert 'summary' in output_data
            assert 'results' in output_data
            assert len(output_data['results']) == 1
            assert output_data['results'][0]['valid'] is True

        finally:
            Path(data_file).unlink(missing_ok=True)

    def test_batch_command_help(self):
        """Test batch command help."""
        result = self.runner.invoke(cli, ['batch', '--help'])
        assert result.exit_code == 0
        assert 'Validate multiple JSON files' in result.output

    def test_batch_valid_files(self):
        """Test batch validation with valid files."""
        # Create multiple valid test files
        test_files = []
        for i in range(3):
            valid_data = {"name": f"User {i}", "email": f"user{i}@example.com"}
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'_{i}.json', delete=False) as f:
                json.dump(valid_data, f)
                test_files.append(f.name)

        try:
            # Use file paths directly instead of glob patterns
            result = self.runner.invoke(cli, [
                'batch'] + test_files + [
                '--schema', self.schema_file.name
            ])

            assert result.exit_code == 0
            assert 'Summary' in result.output or 'valid' in result.output

        finally:
            for file_path in test_files:
                Path(file_path).unlink(missing_ok=True)

    def test_batch_mixed_files(self):
        """Test batch validation with mixed valid/invalid files."""
        test_files = []
        test_data = [
            {"name": "Valid User", "email": "valid@example.com"},
            {"name": "", "email": "invalid-email"}  # Invalid
        ]

        try:
            for i, data in enumerate(test_data):
                with tempfile.NamedTemporaryFile(mode='w', suffix=f'_{i}.json', delete=False) as f:
                    json.dump(data, f)
                    test_files.append(f.name)

            result = self.runner.invoke(cli, [
                'batch'] + test_files + [
                '--schema', self.schema_file.name
            ])

            assert result.exit_code == 1  # Should fail due to invalid file
            assert 'Valid' in result.output
            assert 'Invalid' in result.output

        finally:
            for file_path in test_files:
                Path(file_path).unlink(missing_ok=True)

    def test_batch_csv_output(self):
        """Test batch command with CSV output."""
        valid_data = {"name": "Test User", "email": "test@example.com"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(valid_data, f)
            data_file = f.name

        try:
            result = self.runner.invoke(cli, [
                '--output', 'csv',
                'batch', data_file,
                '--schema', self.schema_file.name
            ])

            assert result.exit_code == 0
            assert 'file,valid,error_count' in result.output
            assert 'true' in result.output

        finally:
            Path(data_file).unlink(missing_ok=True)

    def test_check_command_help(self):
        """Test check command help."""
        result = self.runner.invoke(cli, ['check', '--help'])
        assert result.exit_code == 0
        assert 'Verify that a JSON Schema file is valid' in result.output

    def test_check_valid_schema(self):
        """Test checking a valid schema."""
        result = self.runner.invoke(cli, ['check', self.schema_file.name])

        assert result.exit_code == 0
        assert 'Valid Schema' in result.output

    def test_check_invalid_schema(self):
        """Test checking an invalid schema."""
        # Create invalid schema
        invalid_schema = {"$schema": "invalid-schema-url", "type": "unknown-type"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(invalid_schema, f)
            invalid_schema_file = f.name

        try:
            result = self.runner.invoke(cli, ['check', invalid_schema_file])

            assert result.exit_code == 2  # Schema error
            assert 'Invalid Schema' in result.output or 'error' in result.output.lower()

        finally:
            Path(invalid_schema_file).unlink(missing_ok=True)

    def test_check_nonexistent_schema(self):
        """Test checking non-existent schema file."""
        result = self.runner.invoke(cli, ['check', 'nonexistent-schema.json'])

        assert result.exit_code == 3  # File error
        assert 'not found' in result.output.lower() or 'error' in result.output.lower()

    def test_global_no_color_option(self):
        """Test global --no-color option."""
        valid_data = {"name": "Test User", "email": "test@example.com"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(valid_data, f)
            data_file = f.name

        try:
            result = self.runner.invoke(cli, [
                '--no-color',
                'validate', data_file,
                '--schema', self.schema_file.name
            ])

            assert result.exit_code == 0
            # Should still have "Valid" but without color codes
            assert 'Valid' in result.output

        finally:
            Path(data_file).unlink(missing_ok=True)

    def test_invalid_output_format(self):
        """Test invalid output format."""
        result = self.runner.invoke(cli, [
            '--output', 'invalid-format',
            'check', self.schema_file.name
        ])

        assert result.exit_code != 0
        assert 'Invalid value' in result.output or 'not one of' in result.output