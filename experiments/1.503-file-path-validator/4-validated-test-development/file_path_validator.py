#!/usr/bin/env python3
"""
File path validator using os.path and pathlib libraries.
Correct implementation with comprehensive validation.
"""

import os
import re
from pathlib import Path, PurePath
from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class ValidationResult:
    """Result of path validation"""
    is_valid: bool
    path_type: str = ""
    error_message: str = ""
    original_input_type: str = ""


@dataclass
class SecurityResult:
    """Result of security validation"""
    is_secure: bool
    error_message: str = ""


@dataclass
class ExistenceResult:
    """Result of path existence check"""
    exists: bool
    path_type: str = ""  # "file", "directory", or ""


@dataclass
class NormalizationResult:
    """Result of path normalization"""
    normalized_path: str
    original_path: str


class FilePathValidator:
    """
    File path validator with configurable options using os.path and pathlib.
    """

    # Windows reserved names
    WINDOWS_RESERVED_NAMES = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }

    # Invalid characters for different platforms
    WINDOWS_INVALID_CHARS = set('<>:"|?*')
    UNIX_INVALID_CHARS = set('\x00')  # Null character

    def __init__(self, allow_relative=True, allow_path_traversal=True, max_length=4096):
        """Initialize validator with configuration options"""
        self.allow_relative = allow_relative
        self.allow_path_traversal = allow_path_traversal
        self.max_length = max_length

    def is_valid_path(self, path: Union[str, Path]) -> ValidationResult:
        """
        Validate a file path using comprehensive checks.
        """
        # Convert to string if Path object
        if isinstance(path, Path):
            original_type = "pathlib.Path"
            path_str = str(path)
        else:
            original_type = "str"
            path_str = path

        # Check if path is empty or only whitespace
        if not path_str or path_str.isspace():
            return ValidationResult(
                is_valid=False,
                error_message="Path cannot be empty or only whitespace",
                original_input_type=original_type
            )

        # Check path length
        if len(path_str) > self.max_length:
            return ValidationResult(
                is_valid=False,
                error_message=f"Path is too long (max {self.max_length} characters)",
                original_input_type=original_type
            )

        # Determine path type
        is_absolute = os.path.isabs(path_str)
        path_type = "absolute" if is_absolute else "relative"

        # Check if relative paths are allowed
        if not is_absolute and not self.allow_relative:
            return ValidationResult(
                is_valid=False,
                path_type=path_type,
                error_message="Relative paths are not allowed",
                original_input_type=original_type
            )

        # Check for invalid characters
        invalid_chars = self._get_invalid_characters()
        for char in path_str:
            if char in invalid_chars:
                return ValidationResult(
                    is_valid=False,
                    path_type=path_type,
                    error_message=f"Path contains invalid character: {repr(char)}",
                    original_input_type=original_type
                )

        # Check for Windows reserved names
        if os.name == 'nt':
            parts = Path(path_str).parts
            for part in parts:
                # Remove extension for checking
                name_only = part.split('.')[0].upper()
                if name_only in self.WINDOWS_RESERVED_NAMES:
                    return ValidationResult(
                        is_valid=False,
                        path_type=path_type,
                        error_message=f"Path contains reserved name: {part}",
                        original_input_type=original_type
                    )

        # Path is valid
        return ValidationResult(
            is_valid=True,
            path_type=path_type,
            original_input_type=original_type
        )

    def is_secure_path(self, path: str, base_directory: str) -> SecurityResult:
        """
        Check if path is secure (no path traversal outside base directory).
        """
        try:
            # Normalize both paths
            normalized_path = os.path.normpath(os.path.abspath(path))
            normalized_base = os.path.normpath(os.path.abspath(base_directory))

            # Check if the path is within the base directory
            common_path = os.path.commonpath([normalized_path, normalized_base])

            if common_path != normalized_base:
                return SecurityResult(
                    is_secure=False,
                    error_message="Path traversal detected: path escapes base directory"
                )

            # Additional check for explicit path traversal patterns
            if '..' in path or path.startswith('/'):
                # Use pathlib for more sophisticated checking
                try:
                    resolved_path = Path(base_directory, path).resolve()
                    base_path = Path(base_directory).resolve()

                    # Check if resolved path is within base directory
                    try:
                        resolved_path.relative_to(base_path)
                    except ValueError:
                        return SecurityResult(
                            is_secure=False,
                            error_message="Path traversal detected: resolved path outside base directory"
                        )
                except (OSError, RuntimeError):
                    return SecurityResult(
                        is_secure=False,
                        error_message="Path resolution failed"
                    )

            return SecurityResult(is_secure=True)

        except (ValueError, OSError) as e:
            return SecurityResult(
                is_secure=False,
                error_message=f"Security check failed: {str(e)}"
            )

    def path_exists(self, path: Union[str, Path]) -> ExistenceResult:
        """
        Check if path exists and determine its type using both os.path and pathlib.
        """
        path_str = str(path)

        # Use os.path for existence check
        exists = os.path.exists(path_str)

        if not exists:
            return ExistenceResult(exists=False)

        # Use pathlib for type determination
        path_obj = Path(path_str)

        if path_obj.is_file():
            path_type = "file"
        elif path_obj.is_dir():
            path_type = "directory"
        elif path_obj.is_symlink():
            path_type = "symlink"
        else:
            path_type = "other"

        return ExistenceResult(
            exists=True,
            path_type=path_type
        )

    def normalize_path(self, path: str) -> NormalizationResult:
        """
        Normalize a file path using both os.path and pathlib.
        """
        original_path = path

        # Use os.path.normpath for basic normalization
        normalized = os.path.normpath(path)

        # Use pathlib for additional normalization
        path_obj = Path(normalized)

        # Convert to string with proper separators
        final_normalized = str(path_obj)

        return NormalizationResult(
            normalized_path=final_normalized,
            original_path=original_path
        )

    def _get_invalid_characters(self) -> set:
        """Get set of invalid characters for current platform"""
        if os.name == 'nt':  # Windows
            return self.WINDOWS_INVALID_CHARS
        else:  # Unix-like systems
            return self.UNIX_INVALID_CHARS