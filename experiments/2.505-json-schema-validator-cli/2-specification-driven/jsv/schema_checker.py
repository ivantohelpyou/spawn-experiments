"""Schema verification functionality."""

from typing import Dict, Any, List
import jsonschema

from .exceptions import SchemaError
from .utils.file_utils import read_json_file


class SchemaChecker:
    """Validates JSON Schema files for correctness."""

    def __init__(self):
        """Initialize schema checker."""
        pass

    def check_schema(self, schema_path: str) -> Dict[str, Any]:
        """Check if a JSON schema file is valid.

        Args:
            schema_path: Path to the schema file to check

        Returns:
            Dictionary with validation results and schema info

        Raises:
            SchemaError: If schema file cannot be loaded
        """
        try:
            schema = read_json_file(schema_path)
        except Exception as e:
            raise SchemaError(f"Cannot load schema file: {e}")

        results = {
            'file_path': schema_path,
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'schema_info': self._analyze_schema(schema)
        }

        try:
            # Validate schema structure
            jsonschema.Draft7Validator.check_schema(schema)
        except jsonschema.SchemaError as e:
            results['is_valid'] = False
            results['errors'].append({
                'type': 'schema_error',
                'message': str(e),
                'path': getattr(e, 'path', 'unknown')
            })

        # Additional checks for common issues
        warnings = self._check_schema_best_practices(schema)
        results['warnings'].extend(warnings)

        return results

    def _analyze_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze schema structure and provide information.

        Args:
            schema: Parsed schema dictionary

        Returns:
            Dictionary with schema analysis
        """
        info = {
            'schema_version': schema.get('$schema', 'not specified'),
            'title': schema.get('title', 'not specified'),
            'description': schema.get('description', 'not specified'),
            'type': schema.get('type', 'not specified'),
            'has_properties': 'properties' in schema,
            'property_count': len(schema.get('properties', {})),
            'has_required': 'required' in schema,
            'required_count': len(schema.get('required', [])),
            'supports_additional_properties': schema.get('additionalProperties', True),
        }

        # Count validation rules
        validation_rules = []
        for key in schema:
            if key in ['minLength', 'maxLength', 'minimum', 'maximum', 'pattern', 'format', 'enum']:
                validation_rules.append(key)

        info['validation_rules'] = validation_rules
        info['validation_rule_count'] = len(validation_rules)

        return info

    def _check_schema_best_practices(self, schema: Dict[str, Any]) -> List[Dict[str, str]]:
        """Check schema against best practices and return warnings.

        Args:
            schema: Parsed schema dictionary

        Returns:
            List of warning dictionaries
        """
        warnings = []

        # Check for missing $schema
        if '$schema' not in schema:
            warnings.append({
                'type': 'best_practice',
                'message': 'Schema should include $schema property to specify JSON Schema version'
            })

        # Check for missing title/description
        if 'title' not in schema:
            warnings.append({
                'type': 'documentation',
                'message': 'Schema should include a title for better documentation'
            })

        if 'description' not in schema:
            warnings.append({
                'type': 'documentation',
                'message': 'Schema should include a description for better documentation'
            })

        # Check for overly permissive schemas
        if schema.get('additionalProperties', True) is True and 'properties' in schema:
            warnings.append({
                'type': 'strictness',
                'message': 'Consider setting additionalProperties to false for stricter validation'
            })

        # Check for missing type constraints
        if 'type' not in schema and 'properties' not in schema:
            warnings.append({
                'type': 'constraint',
                'message': 'Schema should specify type constraints for better validation'
            })

        # Check for properties without type
        properties = schema.get('properties', {})
        for prop_name, prop_schema in properties.items():
            if isinstance(prop_schema, dict) and 'type' not in prop_schema:
                warnings.append({
                    'type': 'property_constraint',
                    'message': f'Property "{prop_name}" should specify a type for better validation'
                })

        return warnings