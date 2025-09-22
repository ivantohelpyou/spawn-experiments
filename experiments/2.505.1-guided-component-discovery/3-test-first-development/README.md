# JSON Schema Validator CLI Tool - TDD Implementation

This experiment builds a command-line JSON Schema Validator using strict Test-Driven Development (TDD) methodology.

## Available Components

The project leverages pre-built validation components from `utils/`:
- `email_validator`: Robust email validation (112 lines, TDD from 1.501)
- `url_validator`: Clean URL validation (187 lines, TDD from 1.502)
- `date_validator`: Optimal date validation (98 lines, V4.1 from 1.504)
- `file_path_validator`: Comprehensive file path validation (687 lines, from 1.503)

## Requirements

Core functionality:
- Single file validation: `jsv validate data.json --schema=schema.json`
- Batch validation: `jsv batch *.json --schema=schema.json --output=csv`
- Pipeline validation: `cat data.json | jsv validate --schema=schema.json`
- Schema verification: `jsv check schema.json`

Output formats: text (default), JSON, CSV, quiet mode
Format support: basic types, format validation, required fields, constraints
Quality: progress indicators, colored output, proper exit codes

## TDD Approach

Following Red-Green-Refactor with atomic commit protocol:
- `Test: [feature] - RED`
- `Impl: [feature] with components - GREEN`
- `COMPLETE: All tests passing`