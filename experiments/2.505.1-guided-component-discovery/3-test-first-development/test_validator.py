import pytest
import json
import tempfile
import os
from pathlib import Path
from validator import JSONSchemaValidator


class TestJSONSchemaValidator:
    """Test cases for JSON Schema Validator using TDD approach."""

    def test_validate_simple_json_against_schema_success(self):
        """Test: Should validate valid JSON against schema successfully - RED"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }

        data = {
            "name": "John Doe",
            "age": 30
        }

        validator = JSONSchemaValidator()

        # Act
        result = validator.validate(data, schema)

        # Assert
        assert result.is_valid is True
        assert result.errors == []
        assert result.filename is None

    def test_validate_simple_json_against_schema_failure(self):
        """Test: Should detect invalid JSON against schema - RED"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }

        data = {
            "name": "John Doe"
            # Missing required "age" field
        }

        validator = JSONSchemaValidator()

        # Act
        result = validator.validate(data, schema)

        # Assert
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert "age" in str(result.errors[0])

    def test_validate_file_against_schema_success(self):
        """Test: Should validate JSON file against schema file - RED"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "website": {"type": "string", "format": "uri"},
                "birth_date": {"type": "string", "format": "date"}
            },
            "required": ["email"]
        }

        data = {
            "email": "test@example.com",
            "website": "https://example.com",
            "birth_date": "1990-01-01"
        }

        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as schema_file:
            json.dump(schema, schema_file)
            schema_path = schema_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as data_file:
            json.dump(data, data_file)
            data_path = data_file.name

        try:
            validator = JSONSchemaValidator()

            # Act
            result = validator.validate_file(data_path, schema_path)

            # Assert
            assert result.is_valid is True
            assert result.errors == []
            assert result.filename == data_path

        finally:
            # Cleanup
            os.unlink(schema_path)
            os.unlink(data_path)

    def test_format_validation_with_existing_components(self):
        """Test: Should use existing validation components for format validation - RED"""
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "website": {"type": "string", "format": "uri"},
                "birth_date": {"type": "string", "format": "date"}
            }
        }

        # Valid data
        valid_data = {
            "email": "user@example.com",
            "website": "https://example.com",
            "birth_date": "01/15/1990"
        }

        # Invalid data
        invalid_data = {
            "email": "invalid-email",
            "website": "not-a-url",
            "birth_date": "invalid-date"
        }

        validator = JSONSchemaValidator()

        # Act & Assert - Valid data
        valid_result = validator.validate(valid_data, schema)
        assert valid_result.is_valid is True

        # Act & Assert - Invalid data
        invalid_result = validator.validate(invalid_data, schema)
        assert invalid_result.is_valid is False
        assert len(invalid_result.errors) >= 3  # Should have errors for email, url, and date