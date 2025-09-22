# JSON Schema Validator - Technical Design

## Architecture Overview

### Core Components

#### 1. ValidationResult Class
```python
class ValidationResult:
    """Encapsulates validation outcome with structured error reporting"""

    def __init__(self, is_valid: bool, errors: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []

    def __str__(self) -> str:
        """Human-readable validation result"""

    def __bool__(self) -> bool:
        """Allow boolean evaluation"""
```

#### 2. JSONSchemaValidator Class
```python
class JSONSchemaValidator:
    """Main validator class using jsonschema library"""

    def __init__(self):
        """Initialize with Draft 7 schema support"""

    def validate(self, data, schema) -> ValidationResult:
        """Primary validation method"""

    def validate_json_string(self, json_string: str, schema: dict) -> ValidationResult:
        """Validate JSON string against schema"""

    def _parse_json(self, json_string: str) -> tuple:
        """Parse JSON with error handling"""

    def _validate_schema(self, schema: dict) -> tuple:
        """Validate schema structure"""

    def _format_errors(self, validation_errors) -> List[str]:
        """Convert jsonschema errors to readable messages"""
```

#### 3. Utility Functions
```python
def is_valid_json(json_string: str) -> bool:
    """Quick JSON validity check"""

def validate_simple(data, schema) -> bool:
    """Simple boolean validation without error details"""

def create_validator(schema: dict):
    """Factory function for creating schema validators"""
```

## Implementation Details

### 1. JSON Parsing Strategy
```python
def _parse_json(self, json_string: str) -> tuple:
    """
    Parse JSON string with comprehensive error handling

    Returns:
        (success: bool, data: any, error_message: str)
    """
    try:
        import json
        data = json.loads(json_string)
        return True, data, None
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON: {str(e)}"
        return False, None, error_msg
    except Exception as e:
        error_msg = f"JSON parsing error: {str(e)}"
        return False, None, error_msg
```

### 2. Schema Validation Strategy
```python
def _validate_schema(self, schema: dict) -> tuple:
    """
    Validate schema structure before use

    Returns:
        (is_valid: bool, error_message: str)
    """
    try:
        from jsonschema import Draft7Validator
        Draft7Validator.check_schema(schema)
        return True, None
    except Exception as e:
        error_msg = f"Invalid schema: {str(e)}"
        return False, error_msg
```

### 3. Core Validation Logic
```python
def validate(self, data, schema) -> ValidationResult:
    """
    Main validation workflow:
    1. Validate schema structure
    2. Handle string JSON input parsing
    3. Perform jsonschema validation
    4. Format and return results
    """
    # Schema validation
    schema_valid, schema_error = self._validate_schema(schema)
    if not schema_valid:
        return ValidationResult(False, [schema_error])

    # JSON parsing if needed
    if isinstance(data, str):
        parse_success, parsed_data, parse_error = self._parse_json(data)
        if not parse_success:
            return ValidationResult(False, [parse_error])
        data = parsed_data

    # Schema validation
    try:
        from jsonschema import validate as json_validate
        json_validate(data, schema)
        return ValidationResult(True)
    except Exception as e:
        errors = self._format_errors([e])
        return ValidationResult(False, errors)
```

### 4. Error Message Formatting
```python
def _format_errors(self, validation_errors) -> List[str]:
    """
    Convert jsonschema ValidationError objects to readable strings
    """
    formatted_errors = []
    for error in validation_errors:
        if hasattr(error, 'message'):
            formatted_errors.append(error.message)
        else:
            formatted_errors.append(str(error))
    return formatted_errors
```

## Supported Schema Features

### 1. Type Validation
```python
# Supported types
SUPPORTED_TYPES = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "object": dict,
    "array": list,
    "null": type(None)
}
```

### 2. Object Validation
- `properties`: Define object property schemas
- `required`: Specify required properties
- `additionalProperties`: Control extra properties (false by default)

### 3. Array Validation
- `items`: Schema for array items
- `minItems`/`maxItems`: Array length constraints

### 4. String Validation
- `minLength`/`maxLength`: String length constraints
- `format`: Built-in format validation (email, date, uri)

### 5. Numeric Validation
- `minimum`/`maximum`: Numeric range constraints
- `exclusiveMinimum`/`exclusiveMaximum`: Exclusive range constraints

## Format Validation Implementation

### Built-in Format Validators
```python
FORMAT_VALIDATORS = {
    "email": validate_email_format,
    "date": validate_date_format,
    "uri": validate_uri_format
}

def validate_email_format(value: str) -> bool:
    """Basic email validation using regex"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, value) is not None

def validate_date_format(value: str) -> bool:
    """ISO 8601 date validation (YYYY-MM-DD)"""
    import re
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, value):
        return False
    try:
        from datetime import datetime
        datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_uri_format(value: str) -> bool:
    """Basic URI validation"""
    import re
    pattern = r'^[a-zA-Z][a-zA-Z0-9+.-]*:'
    return re.match(pattern, value) is not None
```

## Error Handling Strategy

### 1. Input Validation Errors
- Malformed JSON strings
- Invalid schema structures
- Unsupported schema features

### 2. Data Validation Errors
- Type mismatches
- Missing required properties
- Format validation failures
- Range constraint violations

### 3. System Errors
- Missing jsonschema library
- Memory or performance issues
- Unexpected exceptions

## Testing Strategy

### 1. Unit Tests
```python
def test_basic_types():
    """Test validation of all supported basic types"""

def test_object_validation():
    """Test object properties and required fields"""

def test_array_validation():
    """Test array items and constraints"""

def test_format_validation():
    """Test email, date, and URI format validation"""

def test_error_handling():
    """Test malformed JSON and invalid schema handling"""
```

### 2. Integration Tests
```python
def test_complex_schemas():
    """Test nested objects and arrays"""

def test_real_world_scenarios():
    """Test with realistic JSON documents"""
```

### 3. Edge Case Tests
```python
def test_edge_cases():
    """Test null values, empty objects, boundary conditions"""
```

## Performance Considerations

### 1. Optimization Strategies
- Reuse compiled validators for repeated schema use
- Lazy loading of jsonschema library
- Efficient error message generation

### 2. Memory Management
- Avoid storing large error objects
- Clean up validator instances after use

### 3. Known Limitations
- No optimization for very large JSON documents
- Single-threaded validation only
- Memory usage scales with JSON document size

## Dependencies

### Required
- Python 3.6+
- `jsonschema` library (fallback to basic validation if unavailable)

### Optional
- `re` module for format validation
- `datetime` module for date validation
- `json` module for JSON parsing

## Usage Examples

### Basic Usage
```python
validator = JSONSchemaValidator()

# Validate JSON string
result = validator.validate_json_string(
    '{"name": "John", "age": 30}',
    {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        },
        "required": ["name"]
    }
)

print(f"Valid: {result.is_valid}")
if not result.is_valid:
    for error in result.errors:
        print(f"Error: {error}")
```

### Advanced Usage
```python
# Complex schema with format validation
schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email"},
        "birthdate": {"type": "string", "format": "date"},
        "website": {"type": "string", "format": "uri"},
        "scores": {
            "type": "array",
            "items": {"type": "integer", "minimum": 0, "maximum": 100},
            "minItems": 1,
            "maxItems": 10
        }
    },
    "required": ["email"]
}

data = {
    "email": "user@example.com",
    "birthdate": "1990-01-01",
    "website": "https://example.com",
    "scores": [85, 92, 78]
}

result = validator.validate(data, schema)
```