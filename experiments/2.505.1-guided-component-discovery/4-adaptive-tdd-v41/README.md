# JSON Schema Validator CLI Tool

A command-line JSON Schema Validator tool built with adaptive TDD methodology and strategic component reuse.

## Overview

This project demonstrates **strategic component discovery and reuse** from the spawn-experiments methodology research. The tool integrates research-validated components from `utils/validation/` while implementing new functionality using Test-Driven Development.

## Strategic Component Reuse

### Discovered and Integrated Components:
- **Email Validator** (from experiment 1.501) - TDD Method 3, 112 lines, robust
- **URL Validator** (from experiment 1.502) - TDD Method 3, 187 lines, clean
- **Date Validator** (from experiment 1.504) - V4.1 Method 4, 98 lines, optimal

### Integration Strategy:
- Email validation for JSON Schema "email" format
- URL validation for JSON Schema "uri" format
- Date validation for JSON Schema "date" format

## Features

### Core Functionality
- ✅ JSON Schema Draft 7 subset validation
- ✅ Support for basic types: string, number, integer, boolean, object, array, null
- ✅ Format validation: email, date, uri
- ✅ Required fields and property validation
- ✅ String constraints: minLength, maxLength
- ✅ Number constraints: minimum, maximum

### CLI Commands
```bash
# Single file validation
python jsv.py validate data.json --schema=schema.json

# Batch validation with progress indicators
python jsv.py batch "*.json" --schema=schema.json --output=csv

# Pipeline validation from stdin
cat data.json | python jsv.py validate --schema=schema.json

# Schema verification
python jsv.py check schema.json
```

### Output Formats
- **Text** (default) - Human-readable with colored output
- **JSON** - Structured results for programmatic use
- **CSV** - Tabular format for batch validation results
- **Quiet mode** - Only return exit codes (0=valid, 1=invalid)

### Advanced Features
- 🎯 **Progress indicators** for batch operations
- 🌈 **Colored output** (errors in red, success in green)
- 📊 **Batch summary statistics**
- 🚀 **High performance** validation
- 🔧 **Proper exit codes** for scripting

## Quick Start

### Installation
```bash
# Clone and navigate to the project
cd experiments/2.505.1-guided-component-discovery/4-adaptive-tdd-v41

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install pytest jsonschema requests colorama
```

### Basic Usage
```bash
# Validate a single file
python jsv.py validate examples/valid_data.json --schema=examples/sample_schema.json

# Batch validate multiple files
python jsv.py batch "examples/data*.json" --schema=examples/sample_schema.json

# Get JSON output
python jsv.py validate examples/invalid_data.json --schema=examples/sample_schema.json --output=json

# Quiet mode for scripting
python jsv.py validate examples/valid_data.json --schema=examples/sample_schema.json --quiet
echo $? # Returns 0 for valid, 1 for invalid
```

## Architecture

### Component Integration
```
jsv/
├── validator.py     # Core JSON Schema validation (NEW)
├── formats.py       # Format validators (STRATEGIC REUSE)
├── cli.py           # CLI interface (NEW)
├── output.py        # Output formatters (NEW)
├── batch.py         # Batch processing with progress (NEW)
└── __init__.py      # Package initialization

tests/               # Comprehensive test suite (58 tests)
├── test_validator.py
├── test_formats.py
├── test_cli.py
├── test_output.py
└── test_batch.py

examples/            # Usage examples
├── sample_schema.json
├── valid_data.json
├── invalid_data.json
├── data1.json
└── data2.json
```

### Strategic Reuse Integration
The tool demonstrates **adaptive component discovery** by:
1. **Exploring** existing `utils/validation/` components
2. **Evaluating** their quality and applicability
3. **Integrating** strategically where appropriate
4. **Building new** functionality using TDD where needed

## Test Coverage

**58 comprehensive tests** covering:
- ✅ Core validation logic (13 tests)
- ✅ Format validation with component integration (6 tests)
- ✅ CLI argument parsing and commands (15 tests)
- ✅ Output formatting in all formats (11 tests)
- ✅ Batch processing with progress indicators (13 tests)

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=jsv --cov-report=term-missing
```

## Performance

### Batch Processing
- Progress indicators for user feedback
- Efficient file processing with detailed error reporting
- Summary statistics and success rate calculation
- Tested with 50+ files in under 5 seconds

### Memory Usage
- Streaming JSON parsing for large files
- Minimal memory footprint per validation
- Efficient error collection and reporting

## Examples

### Valid Data Example
```json
{
  "name": "John Smith",
  "email": "john.smith@example.com",
  "age": 30,
  "website": "https://johnsmith.dev",
  "birthdate": "12/25/1993"
}
```

### Schema Example
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string", "minLength": 1},
    "email": {"type": "string", "format": "email"},
    "age": {"type": "integer", "minimum": 0, "maximum": 150},
    "website": {"type": "string", "format": "uri"},
    "birthdate": {"type": "string", "format": "date"}
  },
  "required": ["name", "email", "age"]
}
```

### Validation Output
```bash
$ python jsv.py validate examples/invalid_data.json --schema=examples/sample_schema.json

examples/invalid_data.json: ✗ Invalid
  1. At 'name': Required property 'name' is missing
  2. At 'email': Invalid email format
  3. At 'age': Number too small (min: 0, actual: -5)
  4. At 'website': Invalid uri format
  5. At 'birthdate': Invalid date format
  6. At 'skills': Expected array, got str
  7. At 'address.city': Required property 'city' is missing
```

## Development Methodology

### Adaptive TDD Process
1. **Component Discovery** - Explored `utils/validation/` components
2. **Strategic Planning** - Evaluated reuse opportunities
3. **Test-First Development** - Wrote tests before implementation
4. **Component Integration** - Strategically reused validated components
5. **Progressive Enhancement** - Built features incrementally

### Quality Assurance
- **Research-validated components** from systematic methodology studies
- **Comprehensive test coverage** with 58 tests
- **Performance benchmarking** with batch operations
- **Multiple output formats** for different use cases

## Success Metrics

### Component Reuse Success
- ✅ **3 components discovered** and strategically integrated
- ✅ **High-quality implementations** reused (TDD Method 3, V4.1 Method 4)
- ✅ **Clean integration** without modification of source components
- ✅ **Fallback implementations** for graceful degradation

### Feature Completeness
- ✅ **All CLI requirements** implemented
- ✅ **All output formats** working (text, JSON, CSV, quiet)
- ✅ **Batch processing** with progress indicators
- ✅ **Pipeline support** via stdin/stdout
- ✅ **Colored output** for enhanced UX

### Development Quality
- ✅ **58 tests passing** (100% success rate)
- ✅ **TDD methodology** followed throughout
- ✅ **Strategic component reuse** demonstrated
- ✅ **Production-ready** implementation

## License

Part of the spawn-experiments methodology research framework.