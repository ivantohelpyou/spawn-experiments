# JSON Schema Validator CLI - Implementation Specifications

## Component Discovery Analysis

### Available Reusable Components (utils/validation/)
- **email_validator**: RFC 5321 compliant, 130 lines, pre-compiled regex optimization
- **date_validator**: Auto-format detection, leap year handling, 98 lines optimal
- **url_validator**: urllib.parse + requests accessibility checking, 64 lines clean
- **file_path_validator**: Cross-platform, comprehensive validation, 343 lines robust

### Reuse Strategy Decision
**LEVERAGE ALL COMPONENTS** - These are research-validated, production-ready implementations that directly support JSON Schema format validation requirements.

## Core Architecture

### CLI Tool Structure
```
jsv/
├── __main__.py              # Entry point with argument parsing
├── core/
│   ├── __init__.py
│   ├── validator.py         # Main JSON Schema validation engine
│   ├── schema_checker.py    # Schema validation and verification
│   └── format_validators.py # Format validation using utils components
├── cli/
│   ├── __init__.py
│   ├── commands.py          # Command implementations (validate, batch, check)
│   ├── output.py            # Output formatters (text, json, csv)
│   └── progress.py          # Progress indicators and colored output
├── utils.py                 # File handling, stdin processing
└── tests/
    ├── test_validator.py
    ├── test_commands.py
    └── test_formats.py
```

## Functional Specifications

### 1. Command Interface

#### Single File Validation
```bash
jsv validate data.json --schema=schema.json
jsv validate data.json --schema=schema.json --format=json
jsv validate data.json --schema=schema.json --quiet
```

#### Batch Validation
```bash
jsv batch *.json --schema=schema.json
jsv batch file1.json file2.json --schema=schema.json --output=csv
jsv batch --directory=/path/to/files --schema=schema.json --progress
```

#### Pipeline Validation
```bash
cat data.json | jsv validate --schema=schema.json
echo '{"name":"test"}' | jsv validate --schema=schema.json --format=json
```

#### Schema Verification
```bash
jsv check schema.json
jsv check schema.json --strict
```

### 2. JSON Schema Support (Draft 7 Subset)

#### Basic Types
- **string**: minLength, maxLength, pattern, format
- **number/integer**: minimum, maximum, multipleOf
- **boolean**: exact true/false validation
- **object**: properties, required, additionalProperties
- **array**: items, minItems, maxItems, uniqueItems
- **null**: exact null validation

#### Format Validation (using utils components)
- **email**: `utils.validation.email_validator.is_valid_email()`
- **date**: `utils.validation.date_validator.validate_date()`
- **uri**: `utils.validation.url_validator.URLValidator.is_valid()`
- **Custom formats**: Extensible framework for additional formats

#### Validation Features
- Required field validation
- Property existence and type checking
- Nested object/array validation
- Format-specific validation with detailed error messages

### 3. Output Formats

#### Text Output (Default)
```
✓ data.json: Valid
✗ invalid.json: 2 errors
  - Line 5: Property 'email' format validation failed: Invalid email format
  - Line 12: Required property 'name' is missing
```

#### JSON Output
```json
{
  "valid": false,
  "files": [
    {
      "file": "data.json",
      "valid": true,
      "errors": []
    },
    {
      "file": "invalid.json",
      "valid": false,
      "errors": [
        {"line": 5, "path": "email", "message": "Invalid email format"},
        {"line": 12, "path": "name", "message": "Required property missing"}
      ]
    }
  ]
}
```

#### CSV Output
```csv
file,valid,error_count,errors
data.json,true,0,""
invalid.json,false,2,"Line 5: Invalid email format; Line 12: Required property missing"
```

#### Quiet Mode
- Exit code 0: All files valid
- Exit code 1: One or more validation failures
- No stdout output

### 4. Quality Features

#### Progress Indicators
```
Validating files... [████████████████████] 100% (25/25) - 2.3s
```

#### Colored Output
- Green checkmarks for valid files
- Red X marks for invalid files
- Yellow warnings for schema issues
- Cyan for informational messages

#### Error Reporting
- File name and line number context
- JSONPath to error location
- Human-readable error descriptions
- Validation rule that failed

## Implementation Strategy

### Phase 1: Core Validation Engine
1. JSON Schema parser with Draft 7 subset support
2. Integration with utils.validation components for format validation
3. Error collection and reporting system
4. Basic validation logic for all supported types

### Phase 2: CLI Interface
1. Argument parsing with click/argparse
2. Command implementations (validate, batch, check)
3. File handling and stdin processing
4. Output format selection

### Phase 3: Quality Polish
1. Progress indicators for batch operations
2. Colored terminal output with fallback
3. Comprehensive error messages with context
4. Help text and usage examples

## Technical Requirements

### Dependencies
- **jsonschema**: Core JSON Schema validation (fallback for complex cases)
- **click**: CLI framework for clean argument parsing
- **colorama**: Cross-platform colored terminal output
- **requests**: HTTP validation for URI formats (via utils)

### Component Integration
```python
# Leverage existing validation components
from utils.validation import validate_email, validate_date, validate_url

# Format validator registry
FORMAT_VALIDATORS = {
    'email': validate_email,
    'date': lambda x: validate_date(x, format_type='auto'),
    'uri': lambda x: URLValidator().is_valid(x)
}
```

### Error Handling
- Graceful handling of malformed JSON
- Clear error messages for schema validation failures
- File access error handling with helpful messages
- Network timeout handling for URI validation

### Performance Considerations
- Stream processing for large files where possible
- Efficient batch processing with progress reporting
- Minimal memory footprint for large file sets
- Fast-fail validation for early error detection

## Testing Strategy

### Unit Tests
- Core validation engine with comprehensive schema coverage
- Format validator integration tests
- Output formatter tests
- CLI command parsing tests

### Integration Tests
- End-to-end CLI command execution
- File processing with various input formats
- Pipeline processing (stdin/stdout)
- Batch processing with mixed valid/invalid files

### Quality Assurance
- Cross-platform testing (Windows, macOS, Linux)
- Performance benchmarking for large files
- Memory usage profiling for batch operations
- CLI usability testing with realistic scenarios

## Success Metrics

### Functional Compliance
- [ ] All JSON Schema Draft 7 subset features implemented
- [ ] All output formats working correctly
- [ ] All CLI commands operational
- [ ] Pipeline and batch processing functional

### Quality Standards
- [ ] Colored output with graceful fallback
- [ ] Progress indicators for long operations
- [ ] Comprehensive error reporting with context
- [ ] Help text and usage examples

### Component Integration
- [ ] Successfully leveraged all utils.validation components
- [ ] Clean integration without duplication
- [ ] Maintained component API compatibility
- [ ] Demonstrated effective component discovery

This specification-driven approach ensures we build exactly what's required while maximizing reuse of the research-validated components available in the utils library.