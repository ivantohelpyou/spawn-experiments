import re


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
                    return ValidationResult(is_valid=False, errors=errors)

            # Validate format for strings
            if 'format' in schema and isinstance(data, str):
                if not self._validate_format(data, schema['format']):
                    errors.append(f"Invalid format '{schema['format']}' for value '{data}'")

            # Validate object properties and required fields
            if isinstance(data, dict):
                if 'properties' in schema:
                    errors.extend(self._validate_properties(data, schema['properties']))
                if 'required' in schema:
                    errors.extend(self._validate_required(data, schema['required']))

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

    def _validate_properties(self, data, properties_schema):
        """Validate object properties against schema"""
        errors = []

        for property_name, property_schema in properties_schema.items():
            if property_name in data:
                # Validate the property value recursively
                property_result = self.validate(data[property_name], property_schema)
                if not property_result.is_valid:
                    for error in property_result.errors:
                        errors.append(f"Property '{property_name}': {error}")

        return errors

    def _validate_required(self, data, required_properties):
        """Validate that all required properties are present"""
        errors = []

        for required_prop in required_properties:
            if required_prop not in data:
                errors.append(f"Required property '{required_prop}' is missing")

        return errors

    def _validate_format(self, data, format_type):
        """Validate string format"""
        if format_type == 'email':
            return self._validate_email(data)
        elif format_type == 'date':
            return self._validate_date(data)
        elif format_type == 'uri':
            return self._validate_uri(data)
        else:
            # Unknown format, assume valid
            return True

    def _validate_email(self, email):
        """Validate email format"""
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return email_pattern.match(email) is not None

    def _validate_date(self, date):
        """Validate date format (YYYY-MM-DD)"""
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        return date_pattern.match(date) is not None

    def _validate_uri(self, uri):
        """Validate URI format (basic)"""
        uri_pattern = re.compile(r'^https?://[^\s/$.?#].[^\s]*$')
        return uri_pattern.match(uri) is not None