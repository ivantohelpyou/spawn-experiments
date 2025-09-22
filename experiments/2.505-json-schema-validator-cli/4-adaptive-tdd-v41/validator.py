#!/usr/bin/env python3
"""
Core JSON Schema Validator functionality.
"""

import json
import os
from dataclasses import dataclass
from typing import List, Dict, Any, Union
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft7Validator, validators
except ImportError:
    print("Error: jsonschema library is required. Install with: pip install jsonschema")
    exit(1)


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    is_valid: bool
    errors: List[str]
    file_path: str = ""

    def __bool__(self):
        """Allow boolean evaluation of validation result."""
        return self.is_valid


class JSONSchemaValidator:
    """JSON Schema Validator with support for Draft 7 subset."""

    def __init__(self):
        """Initialize the validator."""
        self.format_checker = jsonschema.FormatChecker()

    def validate(self, data: Dict[Any, Any], schema: Dict[Any, Any]) -> ValidationResult:
        """
        Validate JSON data against a schema.

        Args:
            data: The JSON data to validate
            schema: The JSON schema to validate against

        Returns:
            ValidationResult containing validation status and any errors
        """
        try:
            validator = Draft7Validator(schema, format_checker=self.format_checker)
            errors = []

            for error in validator.iter_errors(data):
                error_msg = self._format_validation_error(error)
                errors.append(error_msg)

            return ValidationResult(len(errors) == 0, errors)

        except Exception as e:
            return ValidationResult(False, [f"Validation error: {str(e)}"])

    def validate_file(self, file_path: str, schema: Dict[Any, Any]) -> ValidationResult:
        """
        Validate a JSON file against a schema.

        Args:
            file_path: Path to the JSON file to validate
            schema: The JSON schema to validate against

        Returns:
            ValidationResult containing validation status and any errors
        """
        try:
            if not os.path.exists(file_path):
                return ValidationResult(False, [f"File not found: {file_path}"], file_path)

            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    return ValidationResult(
                        False,
                        [f"JSON parse error in {file_path}: {str(e)}"],
                        file_path
                    )

            result = self.validate(data, schema)
            result.file_path = file_path
            return result

        except Exception as e:
            return ValidationResult(False, [f"Error reading file {file_path}: {str(e)}"], file_path)

    def validate_schema(self, schema: Dict[Any, Any]) -> ValidationResult:
        """
        Validate that a schema is itself valid JSON Schema.

        Args:
            schema: The schema to validate

        Returns:
            ValidationResult containing validation status and any errors
        """
        try:
            Draft7Validator.check_schema(schema)
            return ValidationResult(True, [])
        except jsonschema.SchemaError as e:
            return ValidationResult(False, [f"Invalid schema: {str(e)}"])
        except Exception as e:
            return ValidationResult(False, [f"Schema validation error: {str(e)}"])

    def load_schema_file(self, schema_path: str) -> Dict[Any, Any]:
        """
        Load a JSON schema from a file.

        Args:
            schema_path: Path to the schema file

        Returns:
            The loaded schema as a dictionary

        Raises:
            FileNotFoundError: If the schema file doesn't exist
            json.JSONDecodeError: If the schema file contains invalid JSON
        """
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _format_validation_error(self, error: jsonschema.ValidationError) -> str:
        """
        Format a validation error into a human-readable string.

        Args:
            error: The validation error from jsonschema

        Returns:
            A formatted error message string
        """
        path = " -> ".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
        return f"At '{path}': {error.message}"

    def validate_batch(self, file_paths: List[str], schema: Dict[Any, Any]) -> List[ValidationResult]:
        """
        Validate multiple JSON files against a schema.

        Args:
            file_paths: List of paths to JSON files to validate
            schema: The JSON schema to validate against

        Returns:
            List of ValidationResult objects, one for each file
        """
        results = []
        for file_path in file_paths:
            result = self.validate_file(file_path, schema)
            results.append(result)
        return results