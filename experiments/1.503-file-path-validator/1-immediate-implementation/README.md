# File Path Validator

A comprehensive Python file path validator using `os.path` and `pathlib` libraries.

## Features

- **Path Format Validation**: Checks if paths are properly formatted for the current OS
- **Existence Verification**: Verifies if paths exist and determines file vs directory
- **Edge Case Handling**: Handles common edge cases like:
  - Empty strings and null values
  - Very long paths (Windows MAX_PATH limit)
  - Paths with trailing spaces
  - Hidden files and directories
  - Network paths
  - Reserved names (Windows)
  - Invalid characters (Windows)
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Multiple Validation Modes**: Single path, batch validation, programmatic usage
- **Command-Line Interface**: Easy CLI for quick validation

## Quick Start

### Basic Usage

```python
from path_validator import PathValidator

validator = PathValidator()
result = validator.validate_path("/home/user/document.txt")

print(f"Valid: {result['is_valid']}")
print(f"Exists: {result['exists']}")
print(f"Type: {'File' if result['is_file'] else 'Directory' if result['is_directory'] else 'N/A'}")
```

### Batch Validation

```python
from path_validator import validate_paths

paths = ["/tmp", "relative/file.txt", "/nonexistent"]
results = validate_paths(paths)

for path, result in results.items():
    print(f"{path}: {'Valid' if result['is_valid'] else 'Invalid'}")
```

### Command Line Interface

```bash
# Basic validation
python cli.py /tmp file.txt /nonexistent

# Verbose output
python cli.py --verbose /home/user/document.pdf

# JSON output
python cli.py --json /tmp relative/path.txt

# Quiet mode (just valid/invalid)
python cli.py --quiet /tmp "" /nonexistent
```

## Files

- `path_validator.py` - Main validator implementation
- `test_validator.py` - Comprehensive test suite
- `example_usage.py` - Usage examples and demonstrations
- `cli.py` - Command-line interface

## Testing

Run the comprehensive test suite:

```bash
python test_validator.py
```

Run the examples:

```bash
python example_usage.py
```

## Validation Results

The `validate_path()` method returns a dictionary with:

```python
{
    'is_valid': bool,           # Overall validity
    'exists': bool,             # Path exists on filesystem
    'is_file': bool,            # Is an existing file
    'is_directory': bool,       # Is an existing directory
    'is_absolute': bool,        # Is absolute path
    'is_relative': bool,        # Is relative path
    'normalized_path': str,     # Normalized/resolved path
    'parent_exists': bool,      # Parent directory exists
    'errors': [str],            # Validation errors
    'warnings': [str]           # Validation warnings
}
```

## Edge Cases Handled

1. **Empty strings and None values**
2. **Very long paths** (>260 chars, Windows MAX_PATH limit)
3. **Trailing spaces** in paths
4. **Hidden files** (Unix-style dot files)
5. **Network paths** (UNC paths)
6. **Reserved names** (Windows: CON, PRN, AUX, etc.)
7. **Invalid characters** (Windows: <, >, :, ", |, ?, *)
8. **Filesystem errors** (permissions, file name too long, etc.)

## Cross-Platform Support

- **Windows**: Validates against Windows-specific restrictions
- **Unix/Linux/macOS**: More permissive validation following Unix conventions
- **Automatic detection** of current platform for appropriate validation

## Dependencies

- Python 3.6+
- Standard library only (`os`, `pathlib`, `platform`)

## Implementation Details

Uses both `os.path` and `pathlib` for comprehensive validation:
- `pathlib.Path` for modern, object-oriented path handling
- `os.path` for legacy compatibility and specific operations
- Platform detection for OS-specific validation rules
- Error handling for filesystem operations that may fail