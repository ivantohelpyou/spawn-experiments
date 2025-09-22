"""Tests for the JSON validator functionality."""

import json
import tempfile
import pytest
from pathlib import Path

from jsv.validator import JSONValidator, ValidationResult, ValidationError
from jsv.exceptions import SchemaError, FileError


class TestJSONValidator:
    """Test cases for JSONValidator class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create a simple test schema
        self.test_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "email": {"type": "string", "format": "email"},
                "age": {"type": "integer", "minimum": 0}
            },
            "required": ["name", "email"],
            "additionalProperties": False
        }

        # Create temporary schema file
        self.schema_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.test_schema, self.schema_file)
        self.schema_file.close()

        # Create validator
        self.validator = JSONValidator(self.schema_file.name)

    def teardown_method(self):
        """Clean up test fixtures."""
        Path(self.schema_file.name).unlink(missing_ok=True)

    def test_validator_initialization(self):
        """Test validator initialization with valid schema."""
        assert self.validator.schema_path == self.schema_file.name
        assert not self.validator.strict

    def test_validator_initialization_with_invalid_schema(self):
        """Test validator initialization with invalid schema."""
        # Create invalid schema file
        invalid_schema_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump({"invalid": "schema", "$schema": "invalid"}, invalid_schema_file)
        invalid_schema_file.close()

        try:
            with pytest.raises(SchemaError):
                JSONValidator(invalid_schema_file.name)
        finally:
            Path(invalid_schema_file.name).unlink(missing_ok=True)

    def test_validate_valid_data(self):
        """Test validation of valid JSON data."""
        valid_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }

        result = self.validator.validate_data(valid_data, "test.json")

        assert isinstance(result, ValidationResult)
        assert result.is_valid
        assert result.error_count == 0
        assert len(result.errors) == 0
        assert result.file_path == "test.json"

    def test_validate_invalid_data(self):
        """Test validation of invalid JSON data."""
        invalid_data = {
            "name": "",  # Too short
            "email": "not-an-email",  # Invalid format
            "age": -5,  # Below minimum
            "extra": "not allowed"  # Additional property
        }

        result = self.validator.validate_data(invalid_data, "test.json")

        assert isinstance(result, ValidationResult)
        assert not result.is_valid
        assert result.error_count > 0
        assert len(result.errors) > 0

        # Check that we have expected error types
        error_types = [error.error_type for error in result.errors]
        assert "constraint_violation" in error_types or "format_validation" in error_types

    def test_validate_missing_required_fields(self):
        """Test validation with missing required fields."""
        incomplete_data = {
            "age": 25
        }

        result = self.validator.validate_data(incomplete_data, "test.json")

        assert not result.is_valid
        assert result.error_count >= 2  # Missing name and email

        # Check for required field errors
        required_errors = [error for error in result.errors if error.error_type == "required_field"]
        assert len(required_errors) >= 2

    def test_validate_file_valid(self):
        """Test validation of valid JSON file."""
        valid_data = {
            "name": "Jane Doe",
            "email": "jane@example.com"
        }

        # Create temporary JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(valid_data, f)
            temp_file = f.name

        try:
            result = self.validator.validate_file(temp_file)

            assert result.is_valid
            assert result.file_path == temp_file
            assert result.file_size is not None
            assert result.validation_time >= 0
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_validate_file_invalid_json(self):
        """Test validation of malformed JSON file."""
        # Create file with invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json}')  # Missing quotes around json
            temp_file = f.name

        try:
            result = self.validator.validate_file(temp_file)

            assert not result.is_valid
            assert len(result.errors) >= 1
            assert any(error.error_type == "file_error" for error in result.errors)
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_validate_nonexistent_file(self):
        """Test validation of non-existent file."""
        result = self.validator.validate_file("nonexistent.json")

        assert not result.is_valid
        assert len(result.errors) == 1
        assert result.errors[0].error_type == "file_error"
        assert "not found" in result.errors[0].message.lower()

    def test_validate_batch_empty(self):
        """Test batch validation with empty file list."""
        results = self.validator.validate_batch([])
        assert results == []

    def test_validate_batch_multiple_files(self):
        """Test batch validation with multiple files."""
        # Create multiple test files
        test_files = []
        test_data = [
            {"name": "User 1", "email": "user1@example.com"},
            {"name": "User 2", "email": "user2@example.com"},
            {"name": "", "email": "invalid-email"}  # Invalid
        ]

        try:
            for i, data in enumerate(test_data):
                with tempfile.NamedTemporaryFile(mode='w', suffix=f'_{i}.json', delete=False) as f:
                    json.dump(data, f)
                    test_files.append(f.name)

            results = self.validator.validate_batch(test_files)

            assert len(results) == 3
            assert results[0].is_valid
            assert results[1].is_valid
            assert not results[2].is_valid

            # Check that results are in the same order as input
            for i, result in enumerate(results):
                assert result.file_path == test_files[i]

        finally:
            for file_path in test_files:
                Path(file_path).unlink(missing_ok=True)

    def test_json_path_building(self):
        """Test JSON path building for nested errors."""
        nested_data = {
            "name": "Test User",
            "email": "test@example.com",
            "profile": {
                "settings": {
                    "theme": "invalid-theme"
                }
            }
        }

        # Create schema with nested validation
        nested_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "profile": {
                    "type": "object",
                    "properties": {
                        "settings": {
                            "type": "object",
                            "properties": {
                                "theme": {"type": "string", "enum": ["light", "dark"]}
                            }
                        }
                    }
                }
            }
        }

        # Create temporary schema file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(nested_schema, f)
            schema_file = f.name

        try:
            validator = JSONValidator(schema_file)
            result = validator.validate_data(nested_data, "test.json")

            if not result.is_valid:
                # Should have errors with proper JSON paths
                paths = [error.path for error in result.errors]
                assert any("profile" in path for path in paths)
        finally:
            Path(schema_file).unlink(missing_ok=True)


class TestValidationResult:
    """Test cases for ValidationResult class."""

    def test_validation_result_creation(self):
        """Test ValidationResult creation and properties."""
        errors = [
            ValidationError(path="$.name", message="Required field missing"),
            ValidationError(path="$.email", message="Invalid format")
        ]

        result = ValidationResult(
            file_path="test.json",
            is_valid=False,
            errors=errors,
            schema_path="schema.json",
            validation_time=0.05,
            file_size=1024
        )

        assert result.file_path == "test.json"
        assert not result.is_valid
        assert result.error_count == 2
        assert len(result.errors) == 2
        assert result.schema_path == "schema.json"
        assert result.validation_time == 0.05
        assert result.file_size == 1024

    def test_validation_result_string_representation(self):
        """Test string representation of ValidationResult."""
        valid_result = ValidationResult(
            file_path="valid.json",
            is_valid=True,
            errors=[],
            schema_path="schema.json",
            validation_time=0.01
        )

        invalid_result = ValidationResult(
            file_path="invalid.json",
            is_valid=False,
            errors=[ValidationError(path="$", message="Error")],
            schema_path="schema.json",
            validation_time=0.01
        )

        assert str(valid_result) == "valid.json: Valid"
        assert str(invalid_result) == "invalid.json: Invalid"


class TestValidationError:
    """Test cases for ValidationError class."""

    def test_validation_error_creation(self):
        """Test ValidationError creation."""
        error = ValidationError(
            path="$.user.email",
            message="Invalid email format",
            line_number=15,
            error_type="format_validation",
            schema_path="#/properties/user/properties/email"
        )

        assert error.path == "$.user.email"
        assert error.message == "Invalid email format"
        assert error.line_number == 15
        assert error.error_type == "format_validation"
        assert error.schema_path == "#/properties/user/properties/email"

    def test_validation_error_minimal(self):
        """Test ValidationError with minimal required fields."""
        error = ValidationError(
            path="$",
            message="General error"
        )

        assert error.path == "$"
        assert error.message == "General error"
        assert error.line_number is None
        assert error.error_type == "validation"
        assert error.schema_path is None