"""
QR Code Generator using segno library
Immediate Implementation - Direct and intuitive approach
"""
import segno
import os
from pathlib import Path


def validate_input(text):
    """
    Validate input text for QR code generation.

    Args:
        text (str): Input text to validate

    Returns:
        bool: True if text is valid, False otherwise
    """
    if text is None:
        return False

    if not isinstance(text, str):
        return False

    if len(text) == 0:
        return False

    # Check for reasonable length limit (2000 characters as per spec)
    if len(text) > 2000:
        return False

    return True


def generate_qr(text, filename):
    """
    Generate QR code from text and save as PNG file.

    Args:
        text (str): Text to encode in QR code
        filename (str): Output filename for PNG file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate input text
        if not validate_input(text):
            print("Error: Invalid input text")
            return False

        # Validate filename
        if not filename or not isinstance(filename, str):
            print("Error: Invalid filename")
            return False

        # Ensure filename has .png extension
        if not filename.lower().endswith('.png'):
            filename += '.png'

        # Create directory if it doesn't exist
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate QR code with default settings from spec
        # Error correction level M (medium), scale 8
        qr_code = segno.make(text, error='m')

        # Save as PNG with scale 8
        qr_code.save(filename, scale=8)

        print(f"QR code successfully generated: {filename}")
        return True

    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        return False


def generate_qr_with_options(text, filename, error_correction='m', scale=8):
    """
    Generate QR code with custom options.

    Args:
        text (str): Text to encode in QR code
        filename (str): Output filename for PNG file
        error_correction (str): Error correction level ('l', 'm', 'q', 'h')
        scale (int): Scale factor for the QR code

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate input text
        if not validate_input(text):
            print("Error: Invalid input text")
            return False

        # Validate filename
        if not filename or not isinstance(filename, str):
            print("Error: Invalid filename")
            return False

        # Validate error correction level
        valid_error_levels = ['l', 'm', 'q', 'h']
        if error_correction not in valid_error_levels:
            print(f"Error: Invalid error correction level. Must be one of: {valid_error_levels}")
            return False

        # Validate scale
        if not isinstance(scale, int) or scale < 1:
            print("Error: Scale must be a positive integer")
            return False

        # Ensure filename has .png extension
        if not filename.lower().endswith('.png'):
            filename += '.png'

        # Create directory if it doesn't exist
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate QR code with custom settings
        qr_code = segno.make(text, error=error_correction)

        # Save as PNG with custom scale
        qr_code.save(filename, scale=scale)

        print(f"QR code successfully generated: {filename}")
        return True

    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        return False


def main():
    """
    Simple CLI interface for testing the QR code generator.
    """
    print("QR Code Generator")
    print("=" * 20)

    # Get text input
    text = input("Enter text to encode: ").strip()
    if not text:
        print("Error: No text provided")
        return

    # Get filename
    filename = input("Enter output filename (without .png): ").strip()
    if not filename:
        filename = "qr_code"

    # Generate QR code
    success = generate_qr(text, filename)

    if success:
        print("QR code generated successfully!")
    else:
        print("Failed to generate QR code.")


if __name__ == "__main__":
    main()