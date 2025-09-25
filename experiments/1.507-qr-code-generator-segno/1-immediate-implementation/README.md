# QR Code Generator

A simple and intuitive QR code generator using the segno library.

## Features

- Generate QR codes from text input
- Save QR codes as PNG files
- Configurable error correction levels
- Configurable scaling
- Input validation and error handling
- Support for Unicode text
- Automatic directory creation

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from qr_generator import generate_qr

# Generate a QR code
success = generate_qr("Hello World", "my_qr_code")
if success:
    print("QR code generated successfully!")
```

### Advanced Usage

```python
from qr_generator import generate_qr_with_options

# Generate QR code with custom options
success = generate_qr_with_options(
    text="Hello World",
    filename="custom_qr",
    error_correction='h',  # High error correction
    scale=4               # Smaller scale
)
```

### Command Line Interface

Run the script directly for interactive usage:

```bash
python qr_generator.py
```

## API Reference

### `generate_qr(text, filename)`

Generate a QR code with default settings.

**Parameters:**
- `text` (str): Text to encode in the QR code
- `filename` (str): Output filename (`.png` extension added automatically)

**Returns:**
- `bool`: True if successful, False otherwise

**Default Settings:**
- Error correction level: M (medium)
- Scale: 8

### `generate_qr_with_options(text, filename, error_correction='m', scale=8)`

Generate a QR code with custom options.

**Parameters:**
- `text` (str): Text to encode in the QR code
- `filename` (str): Output filename (`.png` extension added automatically)
- `error_correction` (str): Error correction level ('l', 'm', 'q', 'h')
- `scale` (int): Scale factor for the QR code (positive integer)

**Returns:**
- `bool`: True if successful, False otherwise

### `validate_input(text)`

Validate input text for QR code generation.

**Parameters:**
- `text` (str): Text to validate

**Returns:**
- `bool`: True if text is valid, False otherwise

## Error Correction Levels

- `'l'` - Low (~7% correction)
- `'m'` - Medium (~15% correction) - Default
- `'q'` - Quartile (~25% correction)
- `'h'` - High (~30% correction)

## Input Validation

The generator validates input text according to these rules:
- Text must be a string
- Text cannot be empty or None
- Text length must not exceed 2000 characters
- All Unicode characters are supported

## Examples

### Basic Text QR Code

```python
from qr_generator import generate_qr

generate_qr("Visit https://example.com", "website_qr")
```

### Unicode Text QR Code

```python
from qr_generator import generate_qr

generate_qr("Hello World! 你好世界!", "multilingual_qr")
```

### High Error Correction QR Code

```python
from qr_generator import generate_qr_with_options

generate_qr_with_options(
    "Important data that needs high reliability",
    "important_qr",
    error_correction='h',
    scale=10
)
```

### Contact Information QR Code

```python
from qr_generator import generate_qr

contact_info = """BEGIN:VCARD
VERSION:3.0
FN:John Doe
ORG:Example Company
TEL:+1-555-123-4567
EMAIL:john@example.com
END:VCARD"""

generate_qr(contact_info, "contact_qr")
```

## Testing

Run the test suite:

```bash
python -m unittest test_qr_generator.py -v
```

The test suite includes:
- Input validation tests
- Basic QR code generation
- Unicode and special character support
- Error handling
- Edge cases
- Different error correction levels
- Various scale values

## Requirements

- Python 3.6+
- segno library (>=1.6.0)

## Error Handling

The generator handles various error conditions gracefully:
- Invalid input text (empty, None, wrong type, too long)
- Invalid filenames
- File system errors
- QR code generation errors

All errors are reported with descriptive messages, and functions return False on failure.

## Implementation Notes

This implementation follows the "Immediate Implementation" methodology:
- Direct and intuitive approach
- Minimal upfront planning
- Focus on getting it working quickly
- Implementation-driven design
- Comprehensive testing after implementation

The code is structured around the core requirements from the baseline specification, with additional convenience functions and robust error handling added during development.