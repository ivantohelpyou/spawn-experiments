"""
QR Code Generator using segno library
Specification-driven implementation

This module provides QR code generation functionality with input validation
and configurable parameters as specified in the baseline requirements.
"""

import segno
from pathlib import Path
from typing import Optional, Union


class QRGenerator:
    """
    QR Code generator with configurable error correction and scaling.

    Implements the baseline specification requirements:
    - Text to QR code conversion
    - PNG file output
    - Input validation
    - UTF-8 support
    - Configurable error correction and scaling
    """

    def __init__(self, error_correction: str = 'M', scale: int = 8):
        """
        Initialize QR generator with specified parameters.

        Args:
            error_correction: Error correction level ('L', 'M', 'Q', 'H')
                            Default: 'M' (medium) as per specification
            scale: Scaling factor for output image
                  Default: 8 as per specification

        Raises:
            ValueError: If error_correction or scale parameters are invalid
        """
        # Validate error correction level
        valid_error_levels = {'L', 'M', 'Q', 'H'}
        if error_correction not in valid_error_levels:
            raise ValueError(f"Error correction must be one of {valid_error_levels}")

        # Validate scale parameter
        if not isinstance(scale, int) or scale < 1:
            raise ValueError("Scale must be a positive integer")

        self.error_correction = error_correction
        self.scale = scale

    def validate_input(self, text: Union[str, None]) -> bool:
        """
        Validate input text according to specification requirements.

        Args:
            text: Input text to validate

        Returns:
            bool: True if text is valid, False otherwise
        """
        # Handle None/null input
        if text is None:
            return False

        # Handle empty string
        if not isinstance(text, str) or len(text.strip()) == 0:
            return False

        # Check maximum length constraint (2000 characters as per spec)
        if len(text) > 2000:
            return False

        # Validate UTF-8 encoding
        try:
            text.encode('utf-8')
        except UnicodeEncodeError:
            return False

        return True

    def generate_qr(self, text: str, filename: str) -> bool:
        """
        Generate QR code from text and save as PNG file.

        Args:
            text: Text string to encode in QR code
            filename: Output filename for PNG file

        Returns:
            bool: True if QR code was generated successfully, False otherwise
        """
        # Validate input text
        if not self.validate_input(text):
            return False

        # Validate filename
        if not isinstance(filename, str) or len(filename.strip()) == 0:
            return False

        try:
            # Generate QR code using segno
            qr_code = segno.make(
                text,
                error=self.error_correction,
                boost_error=False
            )

            # Save as PNG file
            return self._save_qr_code(qr_code, filename)

        except Exception:
            # Handle any segno library errors
            return False

    def _save_qr_code(self, qr_code, filename: str) -> bool:
        """
        Save QR code object to PNG file.

        Args:
            qr_code: segno QR code object
            filename: Output filename

        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            # Ensure filename has .png extension if not provided
            file_path = Path(filename)
            if file_path.suffix.lower() != '.png':
                file_path = file_path.with_suffix('.png')

            # Save QR code as PNG with specified scale
            qr_code.save(
                str(file_path),
                scale=self.scale,
                kind='png'
            )

            # Verify file was created
            return file_path.exists()

        except Exception:
            # Handle file system errors
            return False


# Convenience functions for direct usage as per specification interface
def generate_qr(text: str, filename: str) -> bool:
    """
    Convenience function to generate QR code with default settings.

    Args:
        text: Text string to encode
        filename: Output filename

    Returns:
        bool: True if successful, False otherwise
    """
    generator = QRGenerator()
    return generator.generate_qr(text, filename)


def validate_input(text: Union[str, None]) -> bool:
    """
    Convenience function to validate input text.

    Args:
        text: Text to validate

    Returns:
        bool: True if valid, False otherwise
    """
    generator = QRGenerator()
    return generator.validate_input(text)