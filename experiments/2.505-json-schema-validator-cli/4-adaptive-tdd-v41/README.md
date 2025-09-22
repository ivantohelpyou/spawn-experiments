# JSON Schema Validator CLI (jsv)

A command-line tool for validating JSON data against JSON Schema (Draft 7 subset).

## Features

- **Single file validation** - Validate individual JSON files against a schema
- **Batch validation** - Validate multiple JSON files in one operation
- **Pipeline support** - Read JSON data from stdin for use in pipelines
- **Multiple output formats** - Text (human-readable), JSON (programmatic), CSV (tabular)
- **Schema verification** - Validate that schemas themselves are correct
- **Detailed error reporting** - Shows exact location and nature of validation errors
- **Progress indicators** - Visual feedback for large batch operations
- **Colored output** - Errors in red, success in green for better readability
- **Quiet mode** - Only return exit codes for scripting

## Installation

Requires Python 3.6+ and the `jsonschema` library:

```bash
pip install jsonschema
```

## Usage

### Basic Commands

```bash
# Validate a single file
python jsv.py validate data.json --schema=schema.json

# Batch validation with CSV output
python jsv.py batch *.json --schema=schema.json --output=csv

# Validate from stdin (pipeline)
cat data.json | python jsv.py validate --schema=schema.json

# Check if a schema is valid
python jsv.py check schema.json

# Quiet mode (only exit codes)
python jsv.py validate data.json --schema=schema.json --quiet
```

### Command Reference

#### `validate` - Validate single file or stdin

```bash
jsv validate [FILE] --schema=SCHEMA [OPTIONS]

Arguments:
  FILE                  JSON file to validate (omit to read from stdin)
  --schema=SCHEMA       JSON Schema file to validate against (required)

Options:
  --output=FORMAT       Output format: text, json, csv (default: text)
  --no-color           Disable colored output
  --quiet              Quiet mode - only return exit codes
```

#### `batch` - Validate multiple files

```bash
jsv batch FILES... --schema=SCHEMA [OPTIONS]

Arguments:
  FILES...             JSON files to validate (supports glob patterns)
  --schema=SCHEMA      JSON Schema file to validate against (required)

Options:
  --output=FORMAT      Output format: text, json, csv (default: text)
  --no-color          Disable colored output
  --quiet             Quiet mode - only return exit codes
```

#### `check` - Validate schema

```bash
jsv check SCHEMA_FILE [OPTIONS]

Arguments:
  SCHEMA_FILE         JSON Schema file to check

Options:
  --output=FORMAT     Output format: text, json (default: text)
  --no-color         Disable colored output
  --quiet            Quiet mode - only return exit codes
```

## Output Formats

### Text (default)
Human-readable output with colors:
```
✓ VALID: data.json
✗ INVALID: bad_data.json
  Error: At 'age': -5 is less than the minimum of 0
  Error: At 'root': 'name' is a required property
```

### JSON
Structured output for programmatic use:
```json
{
  "valid": false,
  "errors": [
    "At 'age': -5 is less than the minimum of 0",
    "At 'root': 'name' is a required property"
  ],
  "file": "bad_data.json"
}
```

### CSV
Tabular format for batch results:
```csv
file,valid,error_count,errors
data.json,True,0,
bad_data.json,False,2,"At 'age': -5 is less than the minimum of 0; At 'root': 'name' is a required property"
```

## Exit Codes

- `0` - All validations passed
- `1` - One or more validations failed
- `130` - Operation cancelled by user (Ctrl+C)

## JSON Schema Support

Supports JSON Schema Draft 7 subset including:

### Basic Types
- `string`, `number`, `integer`, `boolean`, `object`, `array`, `null`

### String Validation
- `minLength`, `maxLength`
- `pattern` (regular expressions)
- `format` validation for `email`, `date`, `uri`

### Numeric Validation
- `minimum`, `maximum`
- `exclusiveMinimum`, `exclusiveMaximum`

### Object Validation
- `properties`
- `required` fields
- `additionalProperties`

### Array Validation
- `items`
- `minItems`, `maxItems`

## Examples

### Example Schema (schema.json)
```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 150
    },
    "email": {
      "type": "string",
      "format": "email"
    }
  },
  "required": ["name", "age"]
}
```

### Example Valid Data (person.json)
```json
{
  "name": "John Doe",
  "age": 30,
  "email": "john@example.com"
}
```

### Validation Examples
```bash
# Basic validation
python jsv.py validate person.json --schema=schema.json

# Get structured output
python jsv.py validate person.json --schema=schema.json --output=json

# Validate multiple files
python jsv.py batch person1.json person2.json --schema=schema.json

# Use in a script with error checking
if python jsv.py validate data.json --schema=schema.json --quiet; then
    echo "Data is valid"
else
    echo "Data is invalid"
fi

# Pipeline usage
curl -s https://api.example.com/data.json | python jsv.py validate --schema=api_schema.json
```

## Testing

Run the test suites:

```bash
# Core functionality tests
python test_validator.py

# CLI interface tests
python test_cli.py
```

## Implementation Details

- **validator.py** - Core validation logic using jsonschema library
- **formatters.py** - Output formatting classes for different formats
- **jsv.py** - Main CLI interface with argument parsing
- **test_data/** - Sample schemas and data files for testing

The tool follows adaptive TDD principles with comprehensive test coverage for both core functionality and CLI interface.