"""Test suite for CLI interface following TDD methodology."""

import pytest
import json
import tempfile
import os
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

# Import the CLI module - will fail initially (Red phase)
try:
    from json_schema_validator import cli, validate_file, validate_batch
except ImportError:
    # Expected during TDD - tests written first
    cli = None
    validate_file = None
    validate_batch = None


class TestCLIInterface:
    """Test CLI command interface and argument parsing."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_cli_command_exists(self):
        """Test that main CLI command exists and is callable."""
        if cli is None:
            pytest.skip("CLI not implemented yet - TDD Red phase")

        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'JSON Schema Validator' in result.output

    def test_cli_single_file_validation(self):
        """Test CLI validates single file with required arguments."""
        if cli is None:
            pytest.skip("CLI not implemented yet - TDD Red phase")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test", "age": 30}, f)
            data_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            schema = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "number"}
                },
                "required": ["name", "age"]
            }
            json.dump(schema, f)
            schema_file = f.name

        try:
            result = self.runner.invoke(cli, [
                '--file', data_file,
                '--schema', schema_file
            ])

            assert result.exit_code == 0
            assert 'valid' in result.output.lower()
        finally:
            os.unlink(data_file)
            os.unlink(schema_file)

    def test_cli_batch_processing(self):
        """Test CLI processes multiple files in batch mode."""
        if cli is None:
            pytest.skip("CLI not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            data1 = {"name": "Alice", "age": 30}
            data2 = {"name": "Bob", "age": 25}

            file1 = Path(temp_dir) / "data1.json"
            file2 = Path(temp_dir) / "data2.json"

            with open(file1, 'w') as f:
                json.dump(data1, f)
            with open(file2, 'w') as f:
                json.dump(data2, f)

            # Create schema
            schema = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "number"}
                },
                "required": ["name", "age"]
            }
            schema_file = Path(temp_dir) / "schema.json"
            with open(schema_file, 'w') as f:
                json.dump(schema, f)

            result = self.runner.invoke(cli, [
                '--batch', temp_dir,
                '--schema', str(schema_file),
                '--pattern', '*.json'
            ])

            assert result.exit_code == 0
            assert 'data1.json' in result.output
            assert 'data2.json' in result.output

    def test_cli_output_formats(self):
        """Test CLI supports different output formats."""
        if cli is None:
            pytest.skip("CLI not implemented yet - TDD Red phase")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test"}, f)
            data_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            schema = {"type": "object", "properties": {"name": {"type": "string"}}}
            json.dump(schema, f)
            schema_file = f.name

        try:
            # Test JSON output
            result = self.runner.invoke(cli, [
                '--file', data_file,
                '--schema', schema_file,
                '--output', 'json'
            ])
            assert result.exit_code == 0

            # Should be valid JSON
            output_data = json.loads(result.output)
            assert 'valid' in output_data

            # Test table output
            result = self.runner.invoke(cli, [
                '--file', data_file,
                '--schema', schema_file,
                '--output', 'table'
            ])
            assert result.exit_code == 0

        finally:
            os.unlink(data_file)
            os.unlink(schema_file)

    def test_cli_stdin_support(self):
        """Test CLI can read JSON from stdin."""
        if cli is None:
            pytest.skip("CLI not implemented yet - TDD Red phase")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            schema = {"type": "object", "properties": {"name": {"type": "string"}}}
            json.dump(schema, f)
            schema_file = f.name

        try:
            json_input = '{"name": "test from stdin"}'
            result = self.runner.invoke(cli, [
                '--schema', schema_file,
                '--stdin'
            ], input=json_input)

            assert result.exit_code == 0

        finally:
            os.unlink(schema_file)

    def test_cli_error_handling(self):
        """Test CLI handles errors gracefully with proper exit codes."""
        if cli is None:
            pytest.skip("CLI not implemented yet - TDD Red phase")

        # Test missing schema file
        result = self.runner.invoke(cli, [
            '--file', 'nonexistent.json',
            '--schema', 'nonexistent_schema.json'
        ])
        assert result.exit_code != 0

        # Test invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('invalid json content')
            invalid_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            schema = {"type": "object"}
            json.dump(schema, f)
            schema_file = f.name

        try:
            result = self.runner.invoke(cli, [
                '--file', invalid_file,
                '--schema', schema_file
            ])
            assert result.exit_code != 0

        finally:
            os.unlink(invalid_file)
            os.unlink(schema_file)

    def test_cli_verbose_output(self):
        """Test CLI verbose mode provides detailed output."""
        if cli is None:
            pytest.skip("CLI not implemented yet - TDD Red phase")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test"}, f)
            data_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            schema = {"type": "object", "properties": {"name": {"type": "string"}}}
            json.dump(schema, f)
            schema_file = f.name

        try:
            result = self.runner.invoke(cli, [
                '--file', data_file,
                '--schema', schema_file,
                '--verbose'
            ])

            assert result.exit_code == 0
            # Should contain more detailed information in verbose mode
            assert len(result.output) > 50  # Arbitrary threshold for "more detailed"

        finally:
            os.unlink(data_file)
            os.unlink(schema_file)

    def test_cli_progress_indicators(self):
        """Test CLI shows progress for batch operations."""
        if cli is None:
            pytest.skip("CLI not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create multiple test files
            for i in range(5):
                data = {"name": f"test_{i}", "value": i}
                file_path = Path(temp_dir) / f"data_{i}.json"
                with open(file_path, 'w') as f:
                    json.dump(data, f)

            schema = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "value": {"type": "number"}
                }
            }
            schema_file = Path(temp_dir) / "schema.json"
            with open(schema_file, 'w') as f:
                json.dump(schema, f)

            result = self.runner.invoke(cli, [
                '--batch', temp_dir,
                '--schema', str(schema_file),
                '--progress'
            ])

            assert result.exit_code == 0
            # Should contain progress indicators
            assert 'Processing' in result.output or 'Progress' in result.output