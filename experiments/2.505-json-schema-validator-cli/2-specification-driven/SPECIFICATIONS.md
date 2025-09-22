# JSON Schema Validator CLI - Implementation Specifications

## 1. PROJECT OVERVIEW

### 1.1 Purpose
A command-line JSON Schema Validator tool (jsv) that validates JSON data against JSON Schema specifications, supporting single file validation, batch operations, and pipeline integration.

### 1.2 Core Requirements
- Validate JSON data against JSON Schema (Draft 7 subset)
- Support single file and batch validation
- Multiple output formats (text, JSON, CSV)
- Pipeline support via stdin
- Detailed error reporting with location information
- Progress indicators for batch operations
- Colored output for readability

## 2. FUNCTIONAL SPECIFICATIONS

### 2.1 Command Interface Design

#### 2.1.1 Primary Commands
```bash
# Single file validation
jsv validate data.json --schema=schema.json

# Batch validation
jsv batch *.json --schema=schema.json --output=csv

# Pipeline validation
cat data.json | jsv validate --schema=schema.json

# Schema verification
jsv check schema.json
```

#### 2.1.2 Command Arguments and Options

**Global Options:**
- `--help, -h`: Show help message
- `--version`: Show version information
- `--quiet, -q`: Quiet mode (exit codes only)
- `--output, -o`: Output format (text|json|csv)
- `--no-color`: Disable colored output

**validate command:**
- `file`: JSON file to validate (optional if using stdin)
- `--schema, -s`: Schema file (required)
- `--strict`: Enable strict validation mode

**batch command:**
- `files`: JSON files to validate (glob patterns supported)
- `--schema, -s`: Schema file (required)
- `--continue-on-error`: Continue validation even if some files fail
- `--max-workers`: Number of parallel validation workers

**check command:**
- `schema_file`: Schema file to verify

### 2.2 Output Formats

#### 2.2.1 Text Output (Default)
```
✓ data.json: Valid
✗ invalid.json: Invalid
  - Line 5: Required property 'name' is missing
  - Line 10: Value 'invalid-email' is not a valid email format

Summary: 1 valid, 1 invalid
```

#### 2.2.2 JSON Output
```json
{
  "summary": {
    "total": 2,
    "valid": 1,
    "invalid": 1
  },
  "results": [
    {
      "file": "data.json",
      "valid": true,
      "errors": []
    },
    {
      "file": "invalid.json",
      "valid": false,
      "errors": [
        {
          "path": "$.name",
          "message": "Required property 'name' is missing",
          "line": 5
        }
      ]
    }
  ]
}
```

#### 2.2.3 CSV Output
```csv
file,valid,error_count,errors
data.json,true,0,""
invalid.json,false,2,"Required property 'name' missing; Invalid email format"
```

### 2.3 JSON Schema Support

#### 2.3.1 Supported Schema Features
- Basic types: string, number, integer, boolean, object, array, null
- Property validation: required, properties, additionalProperties
- String constraints: minLength, maxLength, pattern
- Number constraints: minimum, maximum, multipleOf
- Array constraints: minItems, maxItems, items
- Format validation: email, date, uri, date-time
- Conditional validation: if/then/else (basic support)

#### 2.3.2 Error Reporting Requirements
- JSON Path to error location
- Line number in source file (when possible)
- Clear error message
- Context information for complex errors

## 3. TECHNICAL SPECIFICATIONS

### 3.1 Architecture Design

#### 3.1.1 Core Components
```
jsv/
├── __init__.py
├── cli.py              # Command-line interface
├── validator.py        # Core validation logic
├── schema_checker.py   # Schema verification
├── formatters/         # Output formatters
│   ├── __init__.py
│   ├── text.py
│   ├── json.py
│   └── csv.py
├── utils/
│   ├── __init__.py
│   ├── file_utils.py   # File handling utilities
│   ├── color.py        # Terminal color support
│   └── progress.py     # Progress indicators
└── exceptions.py       # Custom exceptions
```

#### 3.1.2 Class Design

**Validator Class:**
```python
class JSONValidator:
    def __init__(self, schema_path: str, strict: bool = False)
    def validate_file(self, file_path: str) -> ValidationResult
    def validate_data(self, data: str) -> ValidationResult
    def validate_batch(self, file_paths: List[str]) -> List[ValidationResult]
```

**ValidationResult Class:**
```python
class ValidationResult:
    file_path: str
    is_valid: bool
    errors: List[ValidationError]
    schema_path: str
    validation_time: float
```

**ValidationError Class:**
```python
class ValidationError:
    path: str
    message: str
    line_number: Optional[int]
    error_type: str
```

### 3.2 Dependencies

#### 3.2.1 Required Libraries
- `jsonschema`: JSON Schema validation
- `click`: Command-line interface framework
- `colorama`: Cross-platform colored terminal output
- `tqdm`: Progress bars

#### 3.2.2 Standard Library Dependencies
- `json`: JSON parsing
- `pathlib`: File path handling
- `concurrent.futures`: Parallel processing
- `sys`: System interface
- `re`: Regular expressions

### 3.3 Error Handling

#### 3.3.1 Exception Hierarchy
```python
class JSVError(Exception): pass
class SchemaError(JSVError): pass
class ValidationError(JSVError): pass
class FileError(JSVError): pass
```

#### 3.3.2 Exit Codes
- 0: Success (all validations passed)
- 1: Validation failed (one or more files invalid)
- 2: Schema error (invalid schema file)
- 3: File error (missing files, permission issues)
- 4: Usage error (invalid command-line arguments)

## 4. IMPLEMENTATION REQUIREMENTS

### 4.1 Performance Requirements
- Handle files up to 100MB efficiently
- Support batch validation of 1000+ files
- Parallel processing for batch operations
- Memory-efficient streaming for large files

### 4.2 Quality Requirements
- 95%+ test coverage
- Type hints throughout codebase
- Comprehensive error messages
- Cross-platform compatibility (Windows, macOS, Linux)

### 4.3 Usability Requirements
- Clear help documentation with examples
- Intuitive command structure
- Meaningful error messages
- Progress feedback for long operations

## 5. TESTING SPECIFICATIONS

### 5.1 Test Categories
- Unit tests for all core components
- Integration tests for CLI commands
- Performance tests for large files/batches
- Error condition tests

### 5.2 Test Data Requirements
- Valid JSON files with various schemas
- Invalid JSON files with different error types
- Complex nested schemas
- Large files for performance testing
- Edge cases (empty files, malformed JSON)

## 6. DEPLOYMENT SPECIFICATIONS

### 6.1 Installation
- Installable via pip
- Self-contained executable option
- Requirements.txt for dependencies

### 6.2 Distribution
- Python package structure
- Entry point configuration
- Version management

This specification serves as the complete blueprint for implementing the JSON Schema Validator CLI tool.