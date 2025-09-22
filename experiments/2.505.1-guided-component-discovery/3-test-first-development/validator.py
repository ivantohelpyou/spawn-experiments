"""
JSON Schema Validator implementation using TDD approach.
Leverages existing validation components from utils/ directory.
"""

import json
import sys
import os
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path

# Import jsonschema for core validation
import jsonschema
from jsonschema import validate, ValidationError, FormatChecker

# Import existing validation components - import them directly due to naming inconsistencies
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'utils'))
from validation.email_validator import is_valid_email
from validation.url_validator import URLValidator
from validation.date_validator import validate_date


@dataclass
class ValidationResult:
    """Result of JSON schema validation."""
    is_valid: bool
    errors: List[str]
    filename: Optional[str] = None


class CustomFormatChecker:
    """Custom format checker that leverages existing validation components."""

    def __init__(self):
        self.format_checker = FormatChecker()
        self._register_custom_formats()

    def _register_custom_formats(self):
        """Register custom format validators using existing components."""

        @self.format_checker.checks('email')
        def check_email(instance):
            """Validate email format using existing email validator."""
            if not isinstance(instance, str):
                return True  # Let jsonschema handle type validation

            # Use existing email validator
            return is_valid_email(instance)

        @self.format_checker.checks('uri')
        def check_uri(instance):
            """Validate URI format using existing URL validator."""
            if not isinstance(instance, str):
                return True  # Let jsonschema handle type validation

            # Use existing URL validator
            url_validator = URLValidator()
            return url_validator.is_valid(instance)

        @self.format_checker.checks('date')
        def check_date(instance):
            """Validate date format using existing date validator."""
            if not isinstance(instance, str):
                return True  # Let jsonschema handle type validation

            # Use existing date validator
            return validate_date(instance)

    def get_checker(self):
        """Get the configured format checker."""
        return self.format_checker


class JSONSchemaValidator:
    """JSON Schema Validator that uses existing validation components."""

    def __init__(self):
        """Initialize validator with custom format checker."""
        self.custom_format_checker = CustomFormatChecker()

    def validate(self, data: Dict[Any, Any], schema: Dict[Any, Any]) -> ValidationResult:
        """
        Validate JSON data against a schema.

        Args:
            data: JSON data to validate
            schema: JSON schema to validate against

        Returns:
            ValidationResult with validation status and any errors
        """
        errors = []

        try:
            # Use jsonschema with our custom format checker
            validate(data, schema, format_checker=self.custom_format_checker.get_checker())
            return ValidationResult(is_valid=True, errors=[])

        except ValidationError as e:
            # Collect all validation errors, not just the first one
            from jsonschema import Draft7Validator
            validator = Draft7Validator(schema, format_checker=self.custom_format_checker.get_checker())

            for error in validator.iter_errors(data):
                errors.append(str(error.message))

            return ValidationResult(is_valid=False, errors=errors)

        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return ValidationResult(is_valid=False, errors=errors)

    def validate_file(self, data_file: str, schema_file: str) -> ValidationResult:
        """
        Validate JSON file against schema file.

        Args:
            data_file: Path to JSON data file
            schema_file: Path to JSON schema file

        Returns:
            ValidationResult with validation status and any errors
        """
        try:
            # Read schema file
            with open(schema_file, 'r') as f:
                schema = json.load(f)

            # Read data file
            with open(data_file, 'r') as f:
                data = json.load(f)

            # Validate and include filename in result
            result = self.validate(data, schema)
            result.filename = data_file
            return result

        except FileNotFoundError as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"File not found: {str(e)}"],
                filename=data_file
            )
        except json.JSONDecodeError as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Invalid JSON: {str(e)}"],
                filename=data_file
            )
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Error: {str(e)}"],
                filename=data_file
            )