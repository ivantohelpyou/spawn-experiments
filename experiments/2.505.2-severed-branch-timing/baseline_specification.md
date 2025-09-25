# Baseline Specification: JSON Schema Validator CLI Tool

## Core Requirements

Build a command-line JSON Schema Validator tool that:

1. **Accepts JSON data and schema files as input**
2. **Validates data against schema with detailed error reporting**
3. **Supports batch validation of multiple files**
4. **Provides output in multiple formats (text, JSON, CSV)**
5. **Includes progress indicators for large batch operations**
6. **Offers dry-run mode to check schemas without validation**

## Usage Examples

```bash
# Single file validation
jsv validate data.json schema.json

# Batch validation with CSV output
jsv batch validate *.json --schema=schema.json --output=csv

# Schema dry-run check
jsv check-schema schema.json --dry-run

# Validate from stdin
jsv validate --data=stdin --schema=schema.json
```

## Technical Requirements

- **JSON Schema Draft 7 support**
- **Comprehensive format validation** including email, date, and uri formats
- **Command-line interface** with proper argument parsing
- **Error handling** with meaningful error messages
- **Progress indicators** for batch operations
- **Multiple output formats** (text, JSON, CSV)

## Implementation Constraints

- **No access to existing components** (clean slate implementation)
- **Standard libraries preferred** but external dependencies allowed if needed
- **CLI tool should be production-ready** with proper help text and usage
- **Cross-platform compatibility** (Windows, macOS, Linux)

## Expected Deliverables

1. **Main CLI script** (e.g., `jsv.py` or `jsv`)
2. **Core validation logic**
3. **Output formatters** for different formats
4. **Test suite** demonstrating functionality
5. **README** with installation and usage instructions
6. **Requirements file** if external dependencies used

---

*This specification is identical to the original 2.505 experiment to enable direct timing comparison between normal development context and severed branch isolation.*