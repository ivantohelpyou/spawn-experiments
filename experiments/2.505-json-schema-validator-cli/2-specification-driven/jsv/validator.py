"""Core JSON Schema validation functionality."""

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import jsonschema
from jsonschema import ValidationError as JsonSchemaValidationError

from .exceptions import SchemaError, FileError, ValidationError
from .utils.file_utils import read_json_file, read_json_from_stdin, get_line_number


@dataclass
class ValidationError:
    """Represents a validation error with location and context information."""
    path: str
    message: str
    line_number: Optional[int] = None
    error_type: str = "validation"
    schema_path: Optional[str] = None


@dataclass
class ValidationResult:
    """Contains the result of validating a JSON file against a schema."""
    file_path: str
    is_valid: bool
    errors: List[ValidationError]
    schema_path: str
    validation_time: float
    file_size: Optional[int] = None

    @property
    def error_count(self) -> int:
        """Number of validation errors."""
        return len(self.errors)

    def __str__(self) -> str:
        """String representation of validation result."""
        status = "Valid" if self.is_valid else "Invalid"
        return f"{self.file_path}: {status}"


class JSONValidator:
    """JSON Schema validator with support for various validation modes."""

    def __init__(self, schema_path: str, strict: bool = False):
        """Initialize the validator with a schema.

        Args:
            schema_path: Path to the JSON Schema file
            strict: Whether to use strict validation mode

        Raises:
            SchemaError: If schema file is invalid
        """
        self.schema_path = schema_path
        self.strict = strict
        self._schema = self._load_schema()
        self._validator = self._create_validator()

    def _load_schema(self) -> Dict[str, Any]:
        """Load and validate the JSON schema.

        Returns:
            Loaded schema as dictionary

        Raises:
            SchemaError: If schema cannot be loaded or is invalid
        """
        try:
            schema = read_json_file(self.schema_path)

            # Validate that the schema itself is valid
            jsonschema.Draft7Validator.check_schema(schema)

            return schema
        except FileError as e:
            raise SchemaError(f"Cannot load schema file: {e}")
        except jsonschema.SchemaError as e:
            raise SchemaError(f"Invalid schema: {e}")

    def _create_validator(self) -> jsonschema.protocols.Validator:
        """Create a JSON schema validator instance.

        Returns:
            Configured validator instance
        """
        # Use Draft 7 validator as specified in requirements
        validator_class = jsonschema.Draft7Validator

        # Add format checkers for email, date, uri validation
        format_checker = jsonschema.FormatChecker()

        return validator_class(
            self._schema,
            format_checker=format_checker
        )

    def validate_file(self, file_path: str) -> ValidationResult:
        """Validate a JSON file against the schema.

        Args:
            file_path: Path to the JSON file to validate

        Returns:
            ValidationResult containing validation outcome and details
        """
        start_time = time.time()
        errors: List[ValidationError] = []
        file_size = None

        try:
            # Get file size for metrics
            path = Path(file_path)
            if path.exists():
                file_size = path.stat().st_size

            # Load and validate the JSON data
            data = read_json_file(file_path)
            errors = self._validate_data(data, file_path)

        except FileError as e:
            errors = [ValidationError(
                path="$",
                message=str(e),
                error_type="file_error"
            )]
        except Exception as e:
            errors = [ValidationError(
                path="$",
                message=f"Unexpected error: {e}",
                error_type="internal_error"
            )]

        validation_time = time.time() - start_time

        return ValidationResult(
            file_path=file_path,
            is_valid=len(errors) == 0,
            errors=errors,
            schema_path=self.schema_path,
            validation_time=validation_time,
            file_size=file_size
        )

    def validate_data(self, data: Union[str, Dict[str, Any]], source_name: str = "<stdin>") -> ValidationResult:
        """Validate JSON data against the schema.

        Args:
            data: JSON data as string or already parsed dictionary
            source_name: Name of the data source for error reporting

        Returns:
            ValidationResult containing validation outcome and details
        """
        start_time = time.time()
        errors: List[ValidationError] = []

        try:
            # Parse JSON if it's a string
            if isinstance(data, str):
                parsed_data = json.loads(data)
            else:
                parsed_data = data

            errors = self._validate_data(parsed_data, source_name)

        except json.JSONDecodeError as e:
            errors = [ValidationError(
                path="$",
                message=f"Invalid JSON: {e}",
                line_number=getattr(e, 'lineno', None),
                error_type="json_error"
            )]
        except Exception as e:
            errors = [ValidationError(
                path="$",
                message=f"Unexpected error: {e}",
                error_type="internal_error"
            )]

        validation_time = time.time() - start_time

        return ValidationResult(
            file_path=source_name,
            is_valid=len(errors) == 0,
            errors=errors,
            schema_path=self.schema_path,
            validation_time=validation_time
        )

    def validate_stdin(self) -> ValidationResult:
        """Validate JSON data from stdin.

        Returns:
            ValidationResult containing validation outcome and details
        """
        try:
            data = read_json_from_stdin()
            return self.validate_data(data, "<stdin>")
        except FileError as e:
            return ValidationResult(
                file_path="<stdin>",
                is_valid=False,
                errors=[ValidationError(
                    path="$",
                    message=str(e),
                    error_type="stdin_error"
                )],
                schema_path=self.schema_path,
                validation_time=0.0
            )

    def validate_batch(self, file_paths: List[str], max_workers: int = 4) -> List[ValidationResult]:
        """Validate multiple JSON files in parallel.

        Args:
            file_paths: List of file paths to validate
            max_workers: Maximum number of parallel workers

        Returns:
            List of ValidationResult objects in the same order as input
        """
        if not file_paths:
            return []

        # For small batches, use sequential processing
        if len(file_paths) <= 3:
            return [self.validate_file(path) for path in file_paths]

        # Use parallel processing for larger batches
        results: Dict[str, ValidationResult] = {}

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all validation tasks
            future_to_path = {
                executor.submit(self.validate_file, path): path
                for path in file_paths
            }

            # Collect results as they complete
            for future in as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    result = future.result()
                    results[path] = result
                except Exception as e:
                    # Create error result for failed validation
                    results[path] = ValidationResult(
                        file_path=path,
                        is_valid=False,
                        errors=[ValidationError(
                            path="$",
                            message=f"Validation failed: {e}",
                            error_type="internal_error"
                        )],
                        schema_path=self.schema_path,
                        validation_time=0.0
                    )

        # Return results in original order
        return [results[path] for path in file_paths]

    def _validate_data(self, data: Dict[str, Any], file_path: str) -> List[ValidationError]:
        """Internal method to validate parsed JSON data.

        Args:
            data: Parsed JSON data
            file_path: File path for error reporting

        Returns:
            List of validation errors
        """
        errors: List[ValidationError] = []

        try:
            # Validate against schema
            schema_errors = list(self._validator.iter_errors(data))

            for error in schema_errors:
                # Convert JSON schema path to a readable format
                json_path = self._build_json_path(error.absolute_path)

                # Try to get line number for the error
                line_number = get_line_number(file_path, json_path) if file_path != "<stdin>" else None

                # Create our validation error
                validation_error = ValidationError(
                    path=json_path,
                    message=error.message,
                    line_number=line_number,
                    error_type=self._categorize_error(error),
                    schema_path=self._build_schema_path(error.schema_path)
                )

                errors.append(validation_error)

        except Exception as e:
            # Catch any unexpected errors during validation
            errors.append(ValidationError(
                path="$",
                message=f"Validation error: {e}",
                error_type="validation_error"
            ))

        return errors

    def _build_json_path(self, path_deque) -> str:
        """Build a JSON path string from a validation path.

        Args:
            path_deque: Path from jsonschema validation error

        Returns:
            JSON path string (e.g., "$.properties.name")
        """
        if not path_deque:
            return "$"

        path_parts = ["$"]
        for part in path_deque:
            if isinstance(part, int):
                path_parts.append(f"[{part}]")
            else:
                path_parts.append(f".{part}")

        return "".join(path_parts).replace("$.", "$")

    def _build_schema_path(self, path_deque) -> str:
        """Build a schema path string from a validation schema path.

        Args:
            path_deque: Schema path from jsonschema validation error

        Returns:
            Schema path string
        """
        if not path_deque:
            return "#"

        return "#/" + "/".join(str(part) for part in path_deque)

    def _categorize_error(self, error: JsonSchemaValidationError) -> str:
        """Categorize a validation error by type.

        Args:
            error: JSON schema validation error

        Returns:
            Error category string
        """
        validator = error.validator

        # Map common validators to categories
        category_map = {
            'required': 'required_field',
            'type': 'type_mismatch',
            'format': 'format_validation',
            'minLength': 'constraint_violation',
            'maxLength': 'constraint_violation',
            'minimum': 'constraint_violation',
            'maximum': 'constraint_violation',
            'pattern': 'pattern_mismatch',
            'enum': 'enum_violation',
            'additionalProperties': 'additional_properties',
        }

        return category_map.get(validator, 'validation_error')