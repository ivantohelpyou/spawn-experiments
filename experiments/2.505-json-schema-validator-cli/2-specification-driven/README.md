# JSON Schema Validator CLI (jsv)

A powerful command-line JSON Schema Validator tool that validates JSON data against JSON Schema specifications with support for batch operations, multiple output formats, and pipeline integration.

## Features

- ✅ **Single file validation** - Validate individual JSON files
- ✅ **Batch validation** - Process multiple files with glob patterns
- ✅ **Pipeline support** - Read from stdin for integration with other tools
- ✅ **Multiple output formats** - Text, JSON, and CSV output
- ✅ **Colored output** - Enhanced readability with terminal colors
- ✅ **Progress indicators** - Visual feedback for batch operations
- ✅ **Detailed error reporting** - Line numbers and JSON path information
- ✅ **Schema verification** - Validate schema files themselves
- ✅ **Format validation** - Email, date, URI format checking
- ✅ **Parallel processing** - Fast batch validation with configurable workers

## Installation

### From Source

```bash
git clone <repository-url>
cd json-schema-validator-cli
pip install -r requirements.txt
pip install -e .
```

### Dependencies

- Python 3.8+
- jsonschema >= 4.0.0
- click >= 8.0.0
- colorama >= 0.4.0
- tqdm >= 4.60.0

## Usage

### Basic Commands

#### Single File Validation

```bash
# Validate a JSON file against a schema
jsv validate data.json --schema=schema.json

# Enable strict validation mode
jsv validate data.json --schema=schema.json --strict
```

#### Batch Validation

```bash
# Validate multiple files
jsv batch *.json --schema=schema.json

# Use glob patterns
jsv batch data/*.json config/*.json --schema=schema.json

# Output results as CSV
jsv batch *.json --schema=schema.json --output=csv

# Continue validation even if some files fail
jsv batch *.json --schema=schema.json --continue-on-error
```

#### Pipeline Validation

```bash
# Read JSON from stdin
cat data.json | jsv validate --schema=schema.json

# Chain with other commands
curl -s https://api.example.com/data | jsv validate --schema=api-schema.json
```

#### Schema Verification

```bash
# Check if a schema file is valid
jsv check schema.json

# Get detailed schema information
jsv check schema.json --output=json
```

### Output Formats

#### Text Output (Default)

```
✓ data.json: Valid
✗ invalid.json: Invalid
  Line 5, Path $.name: Required property 'name' is missing
  Line 10, Path $.email: Value 'invalid-email' is not a valid email format

Summary: 1 valid, 1 invalid (2 total errors) in 0.15s
```

#### JSON Output

```bash
jsv batch *.json --schema=schema.json --output=json
```

```json
{
  "summary": {
    "total": 2,
    "valid": 1,
    "invalid": 1,
    "total_errors": 2,
    "total_time": 0.150
  },
  "results": [
    {
      "file": "data.json",
      "valid": true,
      "error_count": 0,
      "validation_time": 0.075,
      "schema": "schema.json",
      "errors": []
    },
    {
      "file": "invalid.json",
      "valid": false,
      "error_count": 2,
      "validation_time": 0.075,
      "schema": "schema.json",
      "errors": [
        {
          "path": "$.name",
          "message": "Required property 'name' is missing",
          "type": "required_field",
          "line": 5
        }
      ]
    }
  ]
}
```

#### CSV Output

```bash
jsv batch *.json --schema=schema.json --output=csv
```

```csv
file,valid,error_count,errors,validation_time,schema
data.json,true,0,,0.075,schema.json
invalid.json,false,2,"Line 5: Required property 'name' missing; Line 10: Invalid email format",0.075,schema.json
```

### Global Options

- `--quiet, -q`: Quiet mode - only return exit codes
- `--output, -o`: Output format (text|json|csv)
- `--no-color`: Disable colored output
- `--help`: Show help message
- `--version`: Show version information

### Command-Specific Options

#### validate

- `--schema, -s`: Schema file (required)
- `--strict`: Enable strict validation mode

#### batch

- `--schema, -s`: Schema file (required)
- `--strict`: Enable strict validation mode
- `--continue-on-error`: Continue validation even if some files fail
- `--max-workers`: Number of parallel validation workers (default: 4)

## Exit Codes

- `0`: Success (all validations passed)
- `1`: Validation failed (one or more files invalid)
- `2`: Schema error (invalid schema file)
- `3`: File error (missing files, permission issues)
- `4`: Usage error (invalid command-line arguments)

## Supported JSON Schema Features

### Core Types
- string, number, integer, boolean, object, array, null

### Validation Keywords
- `required`: Required properties
- `properties`: Object property definitions
- `additionalProperties`: Additional property handling
- `type`: Type constraints
- `enum`: Enumeration values

### String Constraints
- `minLength`, `maxLength`: String length limits
- `pattern`: Regular expression patterns
- `format`: Format validation (email, date, uri, date-time)

### Number Constraints
- `minimum`, `maximum`: Numeric range limits
- `multipleOf`: Multiple constraints

### Array Constraints
- `minItems`, `maxItems`: Array length limits
- `items`: Item schema definitions

## Examples

### Example Schema (user-schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "User Profile",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 150
    },
    "preferences": {
      "type": "object",
      "properties": {
        "theme": {
          "type": "string",
          "enum": ["light", "dark"]
        }
      }
    }
  },
  "required": ["name", "email"],
  "additionalProperties": false
}
```

### Example Valid Data (user-valid.json)

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "preferences": {
    "theme": "dark"
  }
}
```

### Example Invalid Data (user-invalid.json)

```json
{
  "name": "",
  "email": "not-an-email",
  "age": -5,
  "invalid_property": "not allowed"
}
```

### Validation Examples

```bash
# Validate single file
jsv validate user-valid.json --schema=user-schema.json
# Output: ✓ user-valid.json: Valid

# Validate invalid file with detailed errors
jsv validate user-invalid.json --schema=user-schema.json
# Output:
# ✗ user-invalid.json: Invalid
#   Line 2, Path $.name: String is too short (minimum 1)
#   Line 3, Path $.email: 'not-an-email' is not a valid email
#   Line 4, Path $.age: -5 is less than the minimum of 0
#   Line 5: Additional property 'invalid_property' is not allowed

# Batch validate with progress
jsv batch user-*.json --schema=user-schema.json
# Output:
# Validating files: 100%|████████| 2/2 [00:00<00:00, 150.00file/s] valid=1 invalid=1
# ✓ user-valid.json: Valid
# ✗ user-invalid.json: Invalid
#   [error details...]
# Summary: 1 valid, 1 invalid (4 total errors) in 0.02s

# Check schema validity
jsv check user-schema.json
# Output:
# ✓ user-schema.json: Valid Schema
#
# Schema Information:
#   Title: User Profile
#   Type: object
#   Properties: 4 total, 2 required
#   Validation rules: minLength, maxLength, format, minimum, maximum, enum
```

## Performance

- Handles files up to 100MB efficiently
- Supports batch validation of 1000+ files
- Parallel processing for improved throughput
- Memory-efficient streaming for large files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details.