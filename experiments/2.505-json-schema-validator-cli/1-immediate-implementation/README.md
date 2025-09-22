# JSON Schema Validator CLI Tool

A fast, lightweight command-line tool for validating JSON data against JSON Schema (Draft 7 subset).

## Features

- **Single file validation** - Validate individual JSON files
- **Batch validation** - Validate multiple files at once with glob pattern support
- **Pipeline support** - Read JSON from stdin for integration with other tools
- **Multiple output formats** - Text (default), JSON, and CSV output
- **Schema verification** - Check if schema files are valid JSON
- **Colored output** - Error messages in red, success in green
- **Progress indicators** - Progress bars for batch operations
- **Proper exit codes** - 0 for success, 1 for validation failures

## Installation

Simply download the `jsv.py` script and make it executable:

```bash
chmod +x jsv.py
```

## Usage

### Single File Validation

```bash
# Validate a single JSON file
./jsv.py validate data.json --schema=schema.json

# Use different output format
./jsv.py validate data.json --schema=schema.json --output=json
```

### Batch Validation

```bash
# Validate multiple files
./jsv.py batch file1.json file2.json --schema=schema.json

# Use glob patterns
./jsv.py batch *.json --schema=schema.json

# Show progress indicator
./jsv.py batch *.json --schema=schema.json --progress

# Output as CSV
./jsv.py batch *.json --schema=schema.json --output=csv
```

### Pipeline Operations

```bash
# Read from stdin
cat data.json | ./jsv.py validate --schema=schema.json

# Use in pipelines
curl -s https://api.example.com/data.json | ./jsv.py validate --schema=api-schema.json
```

### Schema Verification

```bash
# Check if schema file is valid JSON
./jsv.py check schema.json
```

### Quiet Mode

```bash
# Only return exit codes (useful for scripts)
./jsv.py validate data.json --schema=schema.json --quiet
if [ $? -eq 0 ]; then
    echo "Valid!"
else
    echo "Invalid!"
fi
```

## Supported JSON Schema Features

This tool supports a subset of JSON Schema Draft 7:

### Basic Types
- `string`, `number`, `integer`, `boolean`, `object`, `array`, `null`

### String Validation
- `minLength`, `maxLength`
- Format validation: `email`, `date` (YYYY-MM-DD), `uri`

### Number Validation
- `minimum`, `maximum`

### Object Validation
- `required` properties
- `properties` with nested validation

### Array Validation
- `items` schema for array elements

## Output Formats

### Text (Default)
Human-readable output with colors and detailed error messages.

### JSON
Structured JSON output suitable for programmatic processing:

```json
[
  {
    "filename": "data.json",
    "valid": false,
    "elapsed_time": 0.001,
    "errors": [
      {
        "message": "Invalid email format",
        "path": "email",
        "line": null
      }
    ]
  }
]
```

### CSV
Tabular format suitable for spreadsheet applications:

```csv
filename,valid,error_count,elapsed_time,errors
data.json,False,1,0.001,email: Invalid email format
```

## Exit Codes

- `0` - All validations passed
- `1` - One or more validations failed
- `130` - Operation cancelled by user (Ctrl+C)

## Examples

### Example Schema

```json
{
  "type": "object",
  "required": ["name", "age", "email"],
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
  }
}
```

### Example Valid Data

```json
{
  "name": "John Doe",
  "age": 30,
  "email": "john.doe@example.com"
}
```

### Example Invalid Data

```json
{
  "name": "",
  "age": -5,
  "email": "invalid-email"
}
```

### Validation Result

```
✗ INVALID invalid_data.json
  - String too short (min: 1) at name
  - Value too small (min: 0) at age
  - Invalid email format at email
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Implementation Notes

This is a lightweight implementation focused on the most commonly used JSON Schema features. It does not implement the full JSON Schema specification but covers the essential validation needs for most use cases.

The tool is designed to be fast, portable, and easy to integrate into existing workflows and CI/CD pipelines.