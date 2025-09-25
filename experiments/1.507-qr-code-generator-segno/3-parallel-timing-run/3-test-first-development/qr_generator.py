#!/usr/bin/env python3
"""
QR Code Generator using segno library
Implementation driven by Test-First Development (TDD)

REFACTOR Phase: Enhanced structure and maintainability
Follows specification requirements with proper error handling
"""

import segno
import os
from pathlib import Path
from typing import Optional


# Configuration constants per specification
MAX_TEXT_LENGTH = 2000
DEFAULT_ERROR_CORRECTION = 'm'  # Medium error correction
DEFAULT_SCALE = 8
OUTPUT_FORMAT = 'PNG'


def validate_input(text: Optional[str]) -> bool:
    """
    Validate input text before processing

    According to specification:
    - Support UTF-8 text encoding
    - Handle empty/null input gracefully
    - Support reasonable text lengths (up to 2000 characters)

    Args:
        text: Input text to validate

    Returns:
        bool: True if text is valid, False otherwise
    """
    # Handle None input
    if text is None:
        return False

    # Handle empty string or whitespace-only input
    if not text or not text.strip():
        return False

    # Handle length limit per specification
    if len(text) > MAX_TEXT_LENGTH:
        return False

    return True


def _validate_filename(filename: Optional[str]) -> bool:
    """
    Validate filename parameter

    Args:
        filename: Output filename to validate

    Returns:
        bool: True if filename is valid, False otherwise
    """
    if not filename or filename is None:
        return False

    # Check if filename is just whitespace
    if not filename.strip():
        return False

    return True


def _ensure_directory_exists(filepath: str) -> bool:
    """
    Ensure the directory for the output file exists

    Args:
        filepath: Full path to the output file

    Returns:
        bool: True if directory exists or was created, False on error
    """
    try:
        directory = os.path.dirname(filepath)
        if directory:  # Only create if there's a directory component
            os.makedirs(directory, exist_ok=True)
        return True
    except (OSError, ValueError, TypeError):
        return False


def generate_qr(text: Optional[str], filename: Optional[str]) -> bool:
    """
    Generate QR code from text and save to file

    According to specification:
    - Generate QR codes from plain text strings
    - Save QR codes as PNG files
    - Use segno library for QR code generation
    - Default error correction level: M (medium)
    - Default scale: 8
    - Output format: PNG

    Args:
        text: Text to encode in QR code
        filename: Output filename for PNG file

    Returns:
        bool: True if successful, False otherwise
    """
    # Validate input text using our validation function
    if not validate_input(text):
        return False

    # Validate filename
    if not _validate_filename(filename):
        return False

    # Ensure output directory exists
    if not _ensure_directory_exists(filename):
        return False

    try:
        # Generate QR code with segno using specification defaults
        qr = segno.make(text, error=DEFAULT_ERROR_CORRECTION)

        # Save with specified scale and format
        qr.save(filename, scale=DEFAULT_SCALE)

        # Verify file was created successfully
        return _verify_output_file(filename)

    except Exception:
        # Handle any errors during QR generation or file operations
        # Per specification: provide clear error handling
        return False


def _verify_output_file(filename: str) -> bool:
    """
    Verify that the output file was created successfully

    Args:
        filename: Path to the output file

    Returns:
        bool: True if file exists and has content, False otherwise
    """
    try:
        return os.path.exists(filename) and os.path.getsize(filename) > 0
    except OSError:
        return False