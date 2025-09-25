# QR Code Generator - Baseline Specification

## Overview
Create a QR Code generator that can create QR codes from text input using the segno library.

## Core Requirements

### Functional Requirements
1. **Text to QR Code**: Generate QR codes from plain text strings
2. **File Output**: Save QR codes as PNG files
3. **Basic Configuration**: Support basic error correction and scaling options
4. **Validation**: Validate input text before processing

### Interface Requirements
1. **generate_qr(text, filename)**: Main function to generate QR code
   - Input: text string and output filename
   - Output: saves QR code as PNG file
   - Returns: boolean indicating success

2. **validate_input(text)**: Validate input text
   - Input: text string
   - Output: boolean indicating if text is valid

### Technical Constraints
- Use segno library for QR code generation
- Support UTF-8 text encoding
- Default error correction level: M (medium)
- Default scale: 8
- Output format: PNG

### Quality Requirements
- Handle empty/null input gracefully
- Provide clear error messages
- Support reasonable text lengths (up to 2000 characters)

## Success Criteria
- Generate valid QR codes that can be scanned by standard QR readers
- Handle edge cases (empty input, special characters, long text)
- Clean, testable code with proper error handling