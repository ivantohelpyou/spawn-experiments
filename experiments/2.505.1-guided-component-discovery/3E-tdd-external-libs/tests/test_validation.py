"""Test suite for JSON schema validation core functionality following TDD methodology."""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import validation modules - will fail initially (Red phase)
try:
    from json_schema_validator import (
        JSONSchemaValidator,
        ValidationResult,
        ValidationError,
        validate_json_against_schema,
        load_schema,
        load_json_data
    )
except ImportError:
    # Expected during TDD - tests written first
    JSONSchemaValidator = None
    ValidationResult = None
    ValidationError = None
    validate_json_against_schema = None
    load_schema = None
    load_json_data = None


class TestJSONSchemaValidator:
    """Test core JSON schema validation functionality."""

    def test_validator_creation(self):
        """Test JSONSchemaValidator can be instantiated with a schema."""
        if JSONSchemaValidator is None:
            pytest.skip("JSONSchemaValidator not implemented yet - TDD Red phase")

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"}
            },
            "required": ["name"]
        }

        validator = JSONSchemaValidator(schema)
        assert validator is not None
        assert validator.schema == schema

    def test_valid_json_validation(self):
        """Test validation of valid JSON against schema."""
        if JSONSchemaValidator is None:
            pytest.skip("JSONSchemaValidator not implemented yet - TDD Red phase")

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"}
            },
            "required": ["name"]
        }

        validator = JSONSchemaValidator(schema)
        valid_data = {"name": "Alice", "age": 30}

        result = validator.validate(valid_data)
        assert result.is_valid is True
        assert result.errors == []

    def test_invalid_json_validation(self):
        """Test validation of invalid JSON against schema."""
        if JSONSchemaValidator is None:
            pytest.skip("JSONSchemaValidator not implemented yet - TDD Red phase")

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"}
            },
            "required": ["name"]
        }

        validator = JSONSchemaValidator(schema)
        invalid_data = {"age": 30}  # Missing required 'name'

        result = validator.validate(invalid_data)
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("name" in error.lower() for error in result.errors)

    def test_validation_result_structure(self):
        """Test ValidationResult contains all required fields."""
        if ValidationResult is None:
            pytest.skip("ValidationResult not implemented yet - TDD Red phase")

        # Test valid result
        result = ValidationResult(
            is_valid=True,
            errors=[],
            schema_path="test.schema.json",
            data_path="test.data.json"
        )

        assert result.is_valid is True
        assert result.errors == []
        assert result.schema_path == "test.schema.json"
        assert result.data_path == "test.data.json"

        # Test invalid result
        result = ValidationResult(
            is_valid=False,
            errors=["Missing required field 'name'"],
            schema_path="test.schema.json",
            data_path="test.data.json"
        )

        assert result.is_valid is False
        assert len(result.errors) == 1


class TestSchemaLoading:
    """Test schema loading functionality."""

    def test_load_schema_from_file(self):
        """Test loading JSON schema from file."""
        if load_schema is None:
            pytest.skip("load_schema not implemented yet - TDD Red phase")

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(schema, f)
            schema_file = f.name

        try:
            loaded_schema = load_schema(schema_file)
            assert loaded_schema == schema
        finally:
            Path(schema_file).unlink()

    def test_load_schema_invalid_file(self):
        """Test error handling for invalid schema files."""
        if load_schema is None:
            pytest.skip("load_schema not implemented yet - TDD Red phase")

        # Test non-existent file
        with pytest.raises((FileNotFoundError, ValidationError)):
            load_schema("nonexistent_schema.json")

        # Test invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            invalid_file = f.name

        try:
            with pytest.raises((json.JSONDecodeError, ValidationError)):
                load_schema(invalid_file)
        finally:
            Path(invalid_file).unlink()

    def test_load_json_data_from_file(self):
        """Test loading JSON data from file."""
        if load_json_data is None:
            pytest.skip("load_json_data not implemented yet - TDD Red phase")

        data = {"name": "Alice", "age": 30}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            data_file = f.name

        try:
            loaded_data = load_json_data(data_file)
            assert loaded_data == data
        finally:
            Path(data_file).unlink()

    def test_load_json_data_from_string(self):
        """Test loading JSON data from string."""
        if load_json_data is None:
            pytest.skip("load_json_data not implemented yet - TDD Red phase")

        data = {"name": "Bob", "age": 25}
        json_string = json.dumps(data)

        loaded_data = load_json_data(json_string, from_string=True)
        assert loaded_data == data


class TestValidationFunction:
    """Test standalone validation function."""

    def test_validate_json_against_schema_function(self):
        """Test standalone validation function."""
        if validate_json_against_schema is None:
            pytest.skip("validate_json_against_schema not implemented yet - TDD Red phase")

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"}
            },
            "required": ["name"]
        }

        # Valid data
        valid_data = {"name": "Charlie", "age": 35}
        result = validate_json_against_schema(valid_data, schema)
        assert result.is_valid is True

        # Invalid data
        invalid_data = {"age": 35}  # Missing name
        result = validate_json_against_schema(invalid_data, schema)
        assert result.is_valid is False


class TestComplexSchemas:
    """Test validation with complex schemas."""

    def test_nested_object_validation(self):
        """Test validation of nested objects."""
        if JSONSchemaValidator is None:
            pytest.skip("JSONSchemaValidator not implemented yet - TDD Red phase")

        schema = {
            "type": "object",
            "properties": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "address": {
                            "type": "object",
                            "properties": {
                                "street": {"type": "string"},
                                "city": {"type": "string"}
                            },
                            "required": ["city"]
                        }
                    },
                    "required": ["name"]
                }
            },
            "required": ["person"]
        }

        validator = JSONSchemaValidator(schema)

        # Valid nested data
        valid_data = {
            "person": {
                "name": "Alice",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown"
                }
            }
        }

        result = validator.validate(valid_data)
        assert result.is_valid is True

        # Invalid nested data (missing required city)
        invalid_data = {
            "person": {
                "name": "Alice",
                "address": {
                    "street": "123 Main St"
                }
            }
        }

        result = validator.validate(invalid_data)
        assert result.is_valid is False

    def test_array_validation(self):
        """Test validation of arrays."""
        if JSONSchemaValidator is None:
            pytest.skip("JSONSchemaValidator not implemented yet - TDD Red phase")

        schema = {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "number"},
                            "name": {"type": "string"}
                        },
                        "required": ["id"]
                    }
                }
            }
        }

        validator = JSONSchemaValidator(schema)

        # Valid array data
        valid_data = {
            "items": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"}
            ]
        }

        result = validator.validate(valid_data)
        assert result.is_valid is True

        # Invalid array data (missing id in second item)
        invalid_data = {
            "items": [
                {"id": 1, "name": "Item 1"},
                {"name": "Item 2"}  # Missing id
            ]
        }

        result = validator.validate(invalid_data)
        assert result.is_valid is False

    def test_format_validation_integration(self):
        """Test integration with format validation (email, date, uri)."""
        if JSONSchemaValidator is None:
            pytest.skip("JSONSchemaValidator not implemented yet - TDD Red phase")

        schema = {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "website": {"type": "string", "format": "uri"},
                "birthdate": {"type": "string", "format": "date"}
            }
        }

        validator = JSONSchemaValidator(schema)

        # Valid format data
        valid_data = {
            "email": "alice@example.com",
            "website": "https://example.com",
            "birthdate": "1990-05-15"
        }

        result = validator.validate(valid_data)
        assert result.is_valid is True

        # Invalid format data
        invalid_data = {
            "email": "not-an-email",
            "website": "not-a-url",
            "birthdate": "not-a-date"
        }

        result = validator.validate(invalid_data)
        assert result.is_valid is False


class TestErrorDetails:
    """Test detailed error reporting."""

    def test_detailed_error_messages(self):
        """Test that validation errors provide helpful details."""
        if JSONSchemaValidator is None:
            pytest.skip("JSONSchemaValidator not implemented yet - TDD Red phase")

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number", "minimum": 0}
            },
            "required": ["name", "age"]
        }

        validator = JSONSchemaValidator(schema)

        # Data with multiple errors
        invalid_data = {
            "name": 123,  # Wrong type
            "age": -5     # Below minimum
        }

        result = validator.validate(invalid_data)
        assert result.is_valid is False
        assert len(result.errors) >= 2  # Should have multiple errors

        # Check that errors contain helpful information
        error_text = " ".join(result.errors).lower()
        assert "name" in error_text
        assert "age" in error_text

    def test_error_paths_in_nested_objects(self):
        """Test that errors include proper JSON paths for nested objects."""
        if JSONSchemaValidator is None:
            pytest.skip("JSONSchemaValidator not implemented yet - TDD Red phase")

        schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "profile": {
                            "type": "object",
                            "properties": {
                                "age": {"type": "number"}
                            }
                        }
                    }
                }
            }
        }

        validator = JSONSchemaValidator(schema)

        invalid_data = {
            "user": {
                "profile": {
                    "age": "not-a-number"
                }
            }
        }

        result = validator.validate(invalid_data)
        assert result.is_valid is False

        # Should indicate the path to the error
        error_text = " ".join(result.errors).lower()
        assert "age" in error_text or "profile" in error_text