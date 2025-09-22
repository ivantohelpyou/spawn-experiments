# JSON Schema Validator

A comprehensive JSON Schema validator using Python with the jsonschema library, supporting JSON Schema Draft 7 features including type validation, object properties, array constraints, and format validation.

## Features

### Core Functionality
- ✅ Validate JSON data against JSON Schema Draft 7 specifications
- ✅ Support for all basic JSON data types (string, number, integer, boolean, object, array, null)
- ✅ Structured error reporting with detailed error messages
- ✅ Handle both Python objects and JSON strings
- ✅ Graceful error handling for malformed JSON and invalid schemas

### Object Validation
- ✅ Object property type validation
- ✅ Required property enforcement
- ✅ Nested object support
- ✅ Complex object hierarchies

### Array Validation
- ✅ Array item type validation
- ✅ Array length constraints (minItems, maxItems)
- ✅ Homogeneous and heterogeneous arrays

### String Validation
- ✅ String length constraints (minLength, maxLength)
- ✅ Format validation for common patterns:
  - Email addresses (RFC 5322 compliant)
  - Dates (ISO 8601 format: YYYY-MM-DD)
  - URIs (RFC 3986 compliant)

### Numeric Validation
- ✅ Range constraints (minimum, maximum)
- ✅ Integer vs number type distinction
- ✅ Exclusive and inclusive boundaries

## Installation

This validator requires Python 3.6+ and the `jsonschema` library:

```bash
pip install jsonschema
```

## Quick Start

```python
from json_schema_validator import JSONSchemaValidator

# Create validator instance
validator = JSONSchemaValidator()

# Define a schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "email"]
}

# Validate data
data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
result = validator.validate(data, schema)

if result.is_valid:
    print("Validation successful!")
else:
    print("Validation failed:")
    for error in result.errors:
        print(f"  - {error}")
```

## API Reference

### JSONSchemaValidator Class

#### `validate(data, schema) -> ValidationResult`
Validates Python data against a JSON schema.
- `data`: Python object to validate
- `schema`: JSON Schema Draft 7 specification as dictionary
- Returns: `ValidationResult` object

#### `validate_json_string(json_string, schema) -> ValidationResult`
Validates a JSON string against a schema.
- `json_string`: JSON data as string
- `schema`: JSON Schema Draft 7 specification as dictionary
- Returns: `ValidationResult` object

### ValidationResult Class

#### Properties
- `is_valid`: Boolean indicating validation success
- `errors`: List of error messages (empty if valid)

#### Methods
- `__str__()`: Human-readable validation result
- `__bool__()`: Allows boolean evaluation

### Utility Functions

#### `is_valid_json(json_string) -> bool`
Quick check if a string contains valid JSON.

#### `validate_simple(data, schema) -> bool`
Simple boolean validation without detailed error information.

#### `create_validator(schema) -> JSONSchemaValidator`
Factory function for creating a validator with schema validation.

## Examples

### Basic Type Validation
```python
# String validation
result = validator.validate("hello", {"type": "string"})
print(result.is_valid)  # True

# Integer validation
result = validator.validate(42, {"type": "integer"})
print(result.is_valid)  # True

# Type mismatch
result = validator.validate("hello", {"type": "integer"})
print(result.is_valid)  # False
print(result.errors)    # ["'hello' is not of type 'integer'"]
```

### Object Validation
```python
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0}
    },
    "required": ["name"]
}

# Valid object
data = {"name": "Bob", "age": 25}
result = validator.validate(data, schema)
print(result.is_valid)  # True

# Missing required field
data = {"age": 25}
result = validator.validate(data, schema)
print(result.is_valid)  # False
print(result.errors)    # ["'name' is a required property"]
```

### Array Validation
```python
schema = {
    "type": "array",
    "items": {"type": "integer"},
    "minItems": 1,
    "maxItems": 5
}

# Valid array
result = validator.validate([1, 2, 3], schema)
print(result.is_valid)  # True

# Invalid item type
result = validator.validate([1, "two", 3], schema)
print(result.is_valid)  # False
```

### Format Validation
```python
# Email validation
schema = {"type": "string", "format": "email"}
result = validator.validate("user@example.com", schema)
print(result.is_valid)  # True

result = validator.validate("not-an-email", schema)
print(result.is_valid)  # False

# Date validation
schema = {"type": "string", "format": "date"}
result = validator.validate("2023-12-25", schema)
print(result.is_valid)  # True

result = validator.validate("2023-13-01", schema)  # Invalid month
print(result.is_valid)  # False

# URI validation
schema = {"type": "string", "format": "uri"}
result = validator.validate("https://example.com", schema)
print(result.is_valid)  # True
```

### JSON String Validation
```python
# Valid JSON string
json_data = '{"name": "Alice", "age": 30}'
schema = {"type": "object", "properties": {"name": {"type": "string"}}}
result = validator.validate_json_string(json_data, schema)
print(result.is_valid)  # True

# Invalid JSON syntax
json_data = '{"invalid": json}'
result = validator.validate_json_string(json_data, schema)
print(result.is_valid)  # False
print(result.errors)    # ["Invalid JSON: Expecting value: line 1 column 13"]
```

## Supported Schema Features

### Type Keywords
- `type`: Data type specification (string, number, integer, boolean, object, array, null)

### Object Keywords
- `properties`: Property schemas for objects
- `required`: Required property names
- `additionalProperties`: Control of extra properties (follows jsonschema defaults)

### Array Keywords
- `items`: Schema for array items
- `minItems`: Minimum array length
- `maxItems`: Maximum array length

### String Keywords
- `minLength`: Minimum string length
- `maxLength`: Maximum string length
- `format`: Format validation (email, date, uri)

### Numeric Keywords
- `minimum`: Minimum value (inclusive)
- `maximum`: Maximum value (inclusive)
- `exclusiveMinimum`: Minimum value (exclusive)
- `exclusiveMaximum`: Maximum value (exclusive)

## Limitations

This validator implements a subset of JSON Schema Draft 7:

### Not Supported
- Schema composition (`allOf`, `oneOf`, `anyOf`)
- Conditional logic (`if`/`then`/`else`)
- Remote schema references (`$ref` URLs)
- Custom keyword extensions
- Schema transformation or modification
- Advanced pattern matching beyond basic formats

### Format Validation Notes
- Email validation follows the jsonschema library's implementation (RFC 5322 compliant)
- Date validation requires ISO 8601 format (YYYY-MM-DD)
- URI validation is permissive and follows RFC 3986 standards
- Empty strings may be considered valid for some formats depending on RFC interpretation

## Error Handling

The validator provides comprehensive error handling:

1. **JSON Parse Errors**: Clear messages for malformed JSON
2. **Schema Validation Errors**: Validation of schema structure before use
3. **Data Validation Errors**: Detailed error messages with path information
4. **Type Errors**: Clear indication of type mismatches
5. **Constraint Violations**: Specific messages for failed constraints

Error messages include:
- Path information for nested structures
- Clear description of the validation failure
- Expected vs actual values where applicable

## Testing

Run the comprehensive test suite:

```bash
python test_json_schema_validator.py
```

Run example demonstrations:

```bash
python example_usage.py
```

## Performance Considerations

- Uses the jsonschema library for core validation (well-optimized)
- Efficient error collection and formatting
- Memory usage scales with document size
- No performance optimization for very large datasets
- Single-threaded validation only

## Dependencies

- Python 3.6+
- `jsonschema` library (4.x recommended)
- Standard library modules: `json`, `re`, `datetime`