"""
QR Code Generator - Minimal implementation using segno
"""

import segno


def validate_input(text, max_length=2000):
    """Validate input text for QR code generation."""
    if text is None:
        return False
    if not isinstance(text, str):
        return False
    if len(text.strip()) == 0:
        return False
    if len(text) > max_length:
        return False
    return True


def generate_qr(text, filename):
    """Generate a QR code from text and save to file."""
    return generate_qr_advanced(text, filename)


def generate_qr_advanced(text, filename, error='M', scale=8):
    """Generate a QR code with configurable options."""
    if not validate_input(text):
        return False

    try:
        qr = segno.make(text, error=error)
        qr.save(filename, scale=scale)
        return True
    except Exception:
        return False