# JSON Schema Validator (JSV) - CLI Tool

A comprehensive command-line JSON Schema Validator built using the immediate implementation approach. This tool leverages existing validation components from the `utils/` directory for format validation.

## Features

### Core Functionality
- ✅ Validate JSON data against JSON Schema (Draft 7)
- ✅ Support single file validation
- ✅ Support batch validation of multiple JSON files
- ✅ Read from stdin for pipeline operations
- ✅ Schema verification

### Output Formats
- ✅ Text output (default) - human-readable with colors
- ✅ JSON output - structured results for automation
- ✅ CSV output - tabular format for batch results
- ✅ Quiet mode - exit codes only

### Format Validation
- ✅ Email validation (using utils/validation components)
- ✅ Date validation (MM/DD/YYYY and DD/MM/YYYY formats)
- ✅ URI validation
- ✅ Basic JSON Schema constraints (min/max, required fields, types)

### CLI Features
- ✅ Progress indicators for batch operations
- ✅ Colored output (can be disabled)
- ✅ Proper exit codes (0=valid, 1=invalid)
- ✅ Comprehensive help text

## Component Discovery

This implementation successfully discovered and integrated existing validation components:

- **Email Validator**: Used `is_valid_email` from `utils/validation/email_validator.py`
- **Date Validator**: Used `validate_date` from `utils/validation/date_validator.py`
- **URL Validator**: Used `URLValidator` class from `utils/validation/url_validator.py`

The immediate implementation approach naturally led to discovering these components while building format validation functionality.

## Usage Examples

```bash
# Single file validation
python3 jsv.py validate data.json --schema=schema.json

# Batch validation with CSV output
python3 jsv.py batch *.json --schema=schema.json --output=csv

# Pipeline validation
cat data.json | python3 jsv.py validate --schema=schema.json

# Schema verification
python3 jsv.py check schema.json

# Quiet mode for scripting
python3 jsv.py --quiet validate data.json --schema=schema.json
echo $?  # 0 for valid, 1 for invalid
```

## Testing

The implementation includes comprehensive test files:
- `test_schema.json` - JSON Schema with various validation rules
- `valid_data.json` - Valid test data
- `invalid_data.json` - Invalid test data with multiple errors
- `batch_test*.json` - Files for batch validation testing

## Dependencies

- `jsonschema>=4.0.0` - JSON Schema validation library
- `requests>=2.25.0` - For URL accessibility checks (via utils components)

## Implementation Notes

- Built using immediate implementation methodology
- Successfully integrated 3/4 available utils validation components
- Format validation leverages research-validated components
- Comprehensive error reporting with path information
- Cross-platform color support with fallback
- Robust error handling and validation