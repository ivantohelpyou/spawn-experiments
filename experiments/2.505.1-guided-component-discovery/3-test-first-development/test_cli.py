import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from cli import cli, validate_command, batch_command, check_command


class TestCLI:
    """Test cases for CLI interface using TDD approach."""

    def test_validate_command_with_schema_file_success(self):
        """Test: jsv validate data.json --schema=schema.json - RED"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }

        data = {
            "name": "John Doe"
        }

        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as schema_file:
            json.dump(schema, schema_file)
            schema_path = schema_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as data_file:
            json.dump(data, data_file)
            data_path = data_file.name

        try:
            runner = CliRunner()

            # Act
            result = runner.invoke(validate_command, [data_path, '--schema', schema_path])

            # Assert
            assert result.exit_code == 0
            assert "Valid" in result.output or "SUCCESS" in result.output

        finally:
            # Cleanup
            os.unlink(schema_path)
            os.unlink(data_path)

    def test_validate_command_with_schema_file_failure(self):
        """Test: jsv validate should fail with invalid data - RED"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }

        data = {
            "age": 30  # Missing required "name" field
        }

        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as schema_file:
            json.dump(schema, schema_file)
            schema_path = schema_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as data_file:
            json.dump(data, data_file)
            data_path = data_file.name

        try:
            runner = CliRunner()

            # Act
            result = runner.invoke(validate_command, [data_path, '--schema', schema_path])

            # Assert
            assert result.exit_code == 1
            assert "Invalid" in result.output or "ERROR" in result.output
            assert "name" in result.output

        finally:
            # Cleanup
            os.unlink(schema_path)
            os.unlink(data_path)

    def test_validate_command_from_stdin(self):
        """Test: cat data.json | jsv validate --schema=schema.json - RED"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }

        data = {
            "name": "John Doe"
        }

        # Create temporary schema file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as schema_file:
            json.dump(schema, schema_file)
            schema_path = schema_file.name

        try:
            runner = CliRunner()

            # Act - simulate piped input
            result = runner.invoke(validate_command, ['--schema', schema_path],
                                 input=json.dumps(data))

            # Assert
            assert result.exit_code == 0
            assert "Valid" in result.output or "SUCCESS" in result.output

        finally:
            # Cleanup
            os.unlink(schema_path)

    def test_batch_command_multiple_files(self):
        """Test: jsv batch *.json --schema=schema.json - RED"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }

        valid_data = {"name": "John"}
        invalid_data = {"age": 30}  # Missing name

        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as schema_file:
            json.dump(schema, schema_file)
            schema_path = schema_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as valid_file:
            json.dump(valid_data, valid_file)
            valid_path = valid_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as invalid_file:
            json.dump(invalid_data, invalid_file)
            invalid_path = invalid_file.name

        try:
            runner = CliRunner()

            # Act
            result = runner.invoke(batch_command, [valid_path, invalid_path, '--schema', schema_path])

            # Assert
            assert result.exit_code == 1  # Should exit with error if any file is invalid
            assert Path(valid_path).name in result.output
            assert Path(invalid_path).name in result.output

        finally:
            # Cleanup
            os.unlink(schema_path)
            os.unlink(valid_path)
            os.unlink(invalid_path)

    def test_batch_command_with_csv_output(self):
        """Test: jsv batch *.json --schema=schema.json --output=csv - RED"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }

        valid_data = {"name": "John"}
        invalid_data = {"age": 30}

        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as schema_file:
            json.dump(schema, schema_file)
            schema_path = schema_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as valid_file:
            json.dump(valid_data, valid_file)
            valid_path = valid_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as invalid_file:
            json.dump(invalid_data, invalid_file)
            invalid_path = invalid_file.name

        try:
            runner = CliRunner()

            # Act
            result = runner.invoke(batch_command, [valid_path, invalid_path, '--schema', schema_path, '--output', 'csv'])

            # Assert
            # Should output CSV format with headers
            assert "filename,valid,errors" in result.output.lower() or "file" in result.output.lower()
            assert "," in result.output  # CSV format

        finally:
            # Cleanup
            os.unlink(schema_path)
            os.unlink(valid_path)
            os.unlink(invalid_path)

    def test_batch_command_with_json_output(self):
        """Test: jsv batch *.json --schema=schema.json --output=json - RED"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }

        valid_data = {"name": "John"}

        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as schema_file:
            json.dump(schema, schema_file)
            schema_path = schema_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as valid_file:
            json.dump(valid_data, valid_file)
            valid_path = valid_file.name

        try:
            runner = CliRunner()

            # Act
            result = runner.invoke(batch_command, [valid_path, '--schema', schema_path, '--output', 'json'])

            # Assert
            # Should output valid JSON
            output_data = json.loads(result.output)
            assert isinstance(output_data, (list, dict))

        finally:
            # Cleanup
            os.unlink(schema_path)
            os.unlink(valid_path)

    def test_check_command_valid_schema(self):
        """Test: jsv check schema.json - valid schema - RED"""
        # Arrange
        valid_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }

        # Create temporary schema file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as schema_file:
            json.dump(valid_schema, schema_file)
            schema_path = schema_file.name

        try:
            runner = CliRunner()

            # Act
            result = runner.invoke(check_command, [schema_path])

            # Assert
            assert result.exit_code == 0
            assert "Valid schema" in result.output or "SUCCESS" in result.output

        finally:
            # Cleanup
            os.unlink(schema_path)

    def test_check_command_invalid_schema(self):
        """Test: jsv check schema.json - invalid schema - RED"""
        # Arrange
        invalid_schema = {
            "type": "invalid_type",  # Invalid type
            "properties": {
                "name": {"type": "string"}
            }
        }

        # Create temporary schema file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as schema_file:
            json.dump(invalid_schema, schema_file)
            schema_path = schema_file.name

        try:
            runner = CliRunner()

            # Act
            result = runner.invoke(check_command, [schema_path])

            # Assert
            assert result.exit_code == 1
            assert "Invalid schema" in result.output or "ERROR" in result.output

        finally:
            # Cleanup
            os.unlink(schema_path)

    def test_quiet_mode_returns_only_exit_codes(self):
        """Test: --quiet mode should only return exit codes - RED"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }

        data = {"name": "John"}

        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as schema_file:
            json.dump(schema, schema_file)
            schema_path = schema_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as data_file:
            json.dump(data, data_file)
            data_path = data_file.name

        try:
            runner = CliRunner()

            # Act
            result = runner.invoke(validate_command, [data_path, '--schema', schema_path, '--quiet'])

            # Assert
            assert result.exit_code == 0
            assert result.output.strip() == ""  # No output in quiet mode

        finally:
            # Cleanup
            os.unlink(schema_path)
            os.unlink(data_path)