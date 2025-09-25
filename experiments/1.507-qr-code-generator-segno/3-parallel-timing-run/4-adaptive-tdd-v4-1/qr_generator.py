"""
QR Code Generator - Fully Evolved Implementation
Design emerged through Adaptive TDD V4.1 methodology

Final architecture discovered through test evolution:
- Input validation with specification compliance
- Error correction level M (medium) as default
- Scale 8 for readability
- PNG output format
- UTF-8 text encoding support
- 2000 character limit per specification
"""

import segno


def generate_qr(text, filename):
    """
    Generate QR code from text and save to PNG file.

    Args:
        text (str): Text to encode in QR code
        filename (str): Output PNG filename

    Returns:
        bool: True if successful, False if validation fails

    Features evolved through TDD:
    - Input validation integration
    - UTF-8 character support
    - Error correction level M (medium)
    - Scale 8 for optimal readability
    """
    # Validate input before processing
    if not validate_input(text):
        return False

    try:
        # Create QR code with specification-compliant settings
        qr = segno.make(text, error='m')  # Medium error correction
        qr.save(filename, scale=8)  # Scale 8 as per spec
        return True
    except Exception:
        # Handle any segno library errors gracefully
        return False


def validate_input(text):
    """
    Validate input text for QR code generation.

    Args:
        text: Input text to validate

    Returns:
        bool: True if valid, False otherwise

    Validation rules evolved through testing:
    - Reject None input
    - Reject empty strings
    - Reject text longer than 2000 characters (spec limit)
    - Accept whitespace-only strings (valid QR content)
    - Support full UTF-8 character set
    """
    if text is None:
        return False
    if text == "":
        return False
    if len(text) > 2000:  # Specification limit
        return False
    return True