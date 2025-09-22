# JSON Schema Validator

A Python implementation of a JSON Schema Validator using the `jsonschema` library that supports JSON Schema Draft 7 subset features.

## Features

- ✅ Validate JSON data against JSON Schema Draft 7
- ✅ Support for basic data types: string, number, integer, boolean, object, array
- ✅ Required field validation
- ✅ Type validation with detailed error messages
- ✅ Format validation (email, date, uri patterns)
- ✅ Array validation (items, minItems, uniqueItems)
- ✅ Object validation (properties, required fields, additionalProperties)
- ✅ Nested object validation
- ✅ Min/max constraints for numbers and strings
- ✅ Pattern matching for strings
- ✅ Command line interface
- ✅ File-based validation
- ✅ String-based validation
- ✅ Comprehensive error reporting

## Requirements

- Python 3.6+
- `jsonschema` library

Install dependencies:
```bash
pip install jsonschema
```

## Usage

### Command Line Interface

Validate a JSON file against a schema file:
```bash
python validator.py data.json schema.json
```

Run built-in tests:
```bash
python validator.py --test
```

### Python API

```python
from validator import JSONSchemaValidator

validator = JSONSchemaValidator()

# Validate parsed JSON data
schema = {"type": "string", "minLength": 1}
data = "hello"
is_valid, errors = validator.validate_json_data(data, schema)

# Validate JSON strings
schema_str = '{"type": "number", "minimum": 0}'
data_str = '42'
is_valid, errors = validator.validate_json_string(data_str, schema_str)

# Validate files
is_valid, errors = validator.validate_file("data.json", "schema.json")
```

### Examples

See `demo.py` for comprehensive examples:
```bash
python demo.py
```

## Example Files

- `example_schema.json` - A comprehensive person schema
- `valid_data.json` - Valid data that passes the schema
- `invalid_data.json` - Invalid data that fails validation

## Supported JSON Schema Features

### Basic Types
- `string` with minLength, maxLength, pattern, format
- `number` and `integer` with minimum, maximum
- `boolean`
- `object` with properties, required, additionalProperties
- `array` with items, minItems, maxItems, uniqueItems

### Format Validation
- `email` - Email address format
- `date` - Date format (ISO 8601)
- `uri` - URI format

### Constraints
- Required fields
- Type validation
- Range validation (min/max)
- Length validation
- Pattern matching (regex)
- Array uniqueness

## Error Handling

The validator provides detailed error messages with:
- Path to the invalid property
- Description of the validation failure
- Support for nested object errors

Example error output:
```
✗ Validation failed:
  - Path 'name': '' is too short
  - Path 'age': -5 is less than the minimum of 0
  - Path 'address': 'city' is a required property
```

## Limitations

This implementation focuses on JSON Schema Draft 7 subset and does not support:
- Schema composition (allOf, oneOf, anyOf)
- Advanced conditional logic (if/then/else)
- Remote schema references ($ref URLs)
- Custom keyword extensions
- Complex dependencies

## Files

- `validator.py` - Main validator implementation
- `demo.py` - Demonstration script with examples
- `example_schema.json` - Example schema for testing
- `valid_data.json` - Valid test data
- `invalid_data.json` - Invalid test data
- `README.md` - This documentation

## Testing

Run the built-in tests:
```bash
python validator.py --test
```

The tests cover:
- Basic type validation
- Required field validation
- Array validation
- Format validation
- Nested object validation
- Error handling