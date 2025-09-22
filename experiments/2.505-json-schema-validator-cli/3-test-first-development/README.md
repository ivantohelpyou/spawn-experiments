# JSON Schema Validator CLI (TDD Implementation)

A command-line JSON Schema Validator tool built using strict Test-Driven Development principles.

## Features

- ✅ Validate JSON data against JSON Schema (Draft 7 subset)
- ✅ Support for single file validation
- ✅ Batch validation of multiple JSON files using glob patterns
- ✅ Pipeline operations with stdin support
- ✅ Multiple output formats: text, JSON, CSV
- ✅ Quiet mode for scripting
- ✅ Schema file verification
- ✅ Detailed error reporting with file names and line information
- ✅ Proper exit codes for scripting integration

## Usage

### Single File Validation
```bash
python jsv.py validate data.json --schema=schema.json
```

### Batch Validation
```bash
python jsv.py batch *.json --schema=schema.json --output=csv
```

### Pipeline Validation
```bash
cat data.json | python jsv.py validate - --schema=schema.json
```

### Schema Verification
```bash
python jsv.py check schema.json
```

### Output Formats

#### Text Output (default)
```bash
python jsv.py validate data.json --schema=schema.json
```

#### JSON Output
```bash
python jsv.py validate data.json --schema=schema.json --output=json
```

#### CSV Output
```bash
python jsv.py batch *.json --schema=schema.json --output=csv
```

#### Quiet Mode
```bash
python jsv.py validate data.json --schema=schema.json --quiet
echo $?  # Check exit code
```

## Supported JSON Schema Features

- Basic types: string, number, integer, boolean, object, array, null
- Required fields validation
- Property validation
- Numeric constraints: minimum, maximum
- String constraints: minLength, maxLength

## Testing

This implementation was built using strict Test-Driven Development (TDD):

```bash
python test_jsv.py
```

## Exit Codes

- `0`: All validations passed
- `1`: One or more validations failed or error occurred

## TDD Development Process

This tool was developed following the Red-Green-Refactor cycle:

1. **RED**: Write failing tests for each feature
2. **GREEN**: Implement minimal code to make tests pass
3. **REFACTOR**: Clean up and improve code while keeping tests green

Each feature was developed in atomic commits following this pattern:
- `Test: [feature] - RED`
- `Impl: [feature] - GREEN`
- `Refactor: [improvement]` (when needed)

## Implementation Notes

- Built with Python standard library only (no external dependencies)
- Comprehensive test coverage with 29 test cases
- Proper error handling and user feedback
- Clean separation of concerns with focused functions
- Extensible design for future enhancements