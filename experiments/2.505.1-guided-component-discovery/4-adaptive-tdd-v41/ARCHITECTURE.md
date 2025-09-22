# JSON Schema Validator CLI - Architecture Plan

## Component Reuse Strategy

### Leveraged Components from utils/validation/
- `email_validator.is_valid_email()` - For "email" format validation
- `url_validator.URLValidator()` - For "uri" format validation
- `date_validator.validate_date()` - For "date" format validation

### Core Architecture

```
jsv/
├── __init__.py
├── cli.py              # Main CLI interface with argparse
├── validator.py        # Core JSON Schema validation logic
├── formats.py          # Format validators (integrates utils/ components)
├── output.py           # Output formatters (text, JSON, CSV)
├── batch.py            # Batch validation with progress
└── utils.py            # Helper utilities

tests/
├── test_validator.py   # Core validation tests
├── test_formats.py     # Format validation tests
├── test_output.py      # Output formatting tests
├── test_batch.py       # Batch operation tests
└── test_cli.py         # CLI integration tests

examples/
├── sample_schema.json
├── valid_data.json
└── invalid_data.json
```

## CLI Commands

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

## Development Approach: TDD with Strategic Integration

1. **Test-First Development**: Write tests before implementation
2. **Component Integration**: Integrate utils/ components where applicable
3. **Progressive Enhancement**: Start with core functionality, add features incrementally
4. **Validation Points**: Ensure each component works correctly before moving to next

## Technology Stack

- **Core**: Python 3.8+ with jsonschema library
- **CLI**: argparse for command-line interface
- **Formats**: utils/validation components + custom implementations
- **Output**: Native Python (json, csv modules) + colorama for colors
- **Testing**: pytest with comprehensive coverage

## Success Criteria

- All JSON Schema Draft 7 subset features working
- All output formats (text, JSON, CSV, quiet) implemented
- Batch processing with progress indicators
- Pipeline support (stdin/stdout)
- Colored output for better UX
- 90%+ test coverage
- Clear documentation and examples