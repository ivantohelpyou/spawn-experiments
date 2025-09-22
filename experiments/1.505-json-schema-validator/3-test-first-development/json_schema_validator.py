class ValidationResult:
    """Result object for validation operations"""

    def __init__(self, is_valid=True, errors=None):
        self.is_valid = is_valid
        self.errors = errors or []


class JSONSchemaValidator:
    """JSON Schema validator implementing Draft 7 subset"""

    def validate(self, data, schema):
        """
        Validate JSON data against a JSON schema

        Args:
            data: The data to validate
            schema: The JSON schema to validate against

        Returns:
            ValidationResult: Object containing validation result and errors
        """
        try:
            errors = []

            # Validate type
            if 'type' in schema:
                expected_type = schema['type']
                if not self._validate_type(data, expected_type):
                    errors.append(f"Expected type '{expected_type}', got '{type(data).__name__}'")

            return ValidationResult(is_valid=len(errors) == 0, errors=errors)

        except Exception as e:
            return ValidationResult(is_valid=False, errors=[str(e)])

    def _validate_type(self, data, expected_type):
        """Validate data type matches expected JSON Schema type"""
        type_mapping = {
            'string': str,
            'number': (int, float),
            'integer': int,
            'boolean': bool,
            'object': dict,
            'array': list,
            'null': type(None)
        }

        expected_python_type = type_mapping.get(expected_type)
        if expected_python_type is None:
            return False

        return isinstance(data, expected_python_type)