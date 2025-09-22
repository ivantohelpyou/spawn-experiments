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

    # Control characters (0-31) that should be invalid on all platforms
    CONTROL_CHARS = set(chr(i) for i in range(0, 32))

    def __init__(self, allow_relative=True, allow_path_traversal=True, max_length=4096):
        """Initialize validator with configuration options"""
        self.allow_relative = allow_relative
        self.allow_path_traversal = allow_path_traversal
        self.max_length = max_length

    def is_valid_path(self, path: Union[str, Path]) -> ValidationResult:
        """
        Validate a file path using comprehensive checks.
        """
        # Convert to string and determine original type
        original_type, path_str = self._normalize_input(path)

        # Basic validation checks
        basic_validation = self._validate_basic_properties(path_str, original_type)
        if not basic_validation.is_valid:
            return basic_validation

        # Determine path type
        is_absolute = os.path.isabs(path_str)
        path_type = "absolute" if is_absolute else "relative"

        # Check path type restrictions
        if not is_absolute and not self.allow_relative:
            return self._create_error_result(
                "Relative paths are not allowed",
                path_type, original_type
            )

        # Character validation
        char_validation = self._validate_characters(path_str, path_type, original_type)
        if not char_validation.is_valid:
            return char_validation

        # Platform-specific validation
        platform_validation = self._validate_platform_specific(path_str, path_type, original_type)
        if not platform_validation.is_valid:
            return platform_validation

        # Path is valid
        return ValidationResult(
            is_valid=True,
            path_type=path_type,
            original_input_type=original_type
        )

    def _normalize_input(self, path: Union[str, Path]) -> tuple[str, str]:
        """Convert input to string and return original type."""
        if isinstance(path, Path):
            return "pathlib.Path", str(path)
        else:
            return "str", path

    def _validate_basic_properties(self, path_str: str, original_type: str) -> ValidationResult:
        """Validate basic path properties like emptiness and length."""
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

        return ValidationResult(is_valid=True, original_input_type=original_type)

    def _validate_characters(self, path_str: str, path_type: str, original_type: str) -> ValidationResult:
        """Validate characters in the path."""
        invalid_chars = self._get_invalid_characters()
        for char in path_str:
            if char in invalid_chars:
                return self._create_error_result(
                    f"Path contains invalid character: {repr(char)}",
                    path_type, original_type
                )
        return ValidationResult(is_valid=True, path_type=path_type, original_input_type=original_type)

    def _validate_platform_specific(self, path_str: str, path_type: str, original_type: str) -> ValidationResult:
        """Validate platform-specific rules like Windows reserved names."""
        if os.name == 'nt':
            parts = Path(path_str).parts
            for part in parts:
                # Remove extension for checking
                name_only = part.split('.')[0].upper()
                if name_only in self.WINDOWS_RESERVED_NAMES:
                    return self._create_error_result(
                        f"Path contains reserved name: {part}",
                        path_type, original_type
                    )
        return ValidationResult(is_valid=True, path_type=path_type, original_input_type=original_type)

    def _create_error_result(self, error_message: str, path_type: str, original_type: str) -> ValidationResult:
        """Create a standardized error result."""
        return ValidationResult(
            is_valid=False,
            path_type=path_type,
            error_message=error_message,
            original_input_type=original_type
        )

    def is_secure_path(self, path: str, base_directory: str) -> SecurityResult:
        """
        Check if path is secure (no path traversal outside base directory).
        """
        try:
            normalized_path = self._normalize_path_separators(path)

            # Check for path traversal patterns
            traversal_check = self._check_path_traversal_patterns(normalized_path)
            if not traversal_check.is_secure:
                return traversal_check

            # Check for absolute paths
            absolute_check = self._check_absolute_path_security(normalized_path)
            if not absolute_check.is_secure:
                return absolute_check

            # Perform final path resolution check
            return self._check_path_resolution_security(normalized_path, base_directory)

        except (ValueError, OSError) as e:
            return SecurityResult(
                is_secure=False,
                error_message=f"Security check failed: {str(e)}"
            )

    def _normalize_path_separators(self, path: str) -> str:
        """Normalize path separators for cross-platform compatibility."""
        return path.replace('\\', '/')

    def _check_path_traversal_patterns(self, path: str) -> SecurityResult:
        """Check for obvious path traversal patterns."""
        if '..' in path:
            return SecurityResult(
                is_secure=False,
                error_message="Path traversal detected: contains '..' components"
            )
        return SecurityResult(is_secure=True)

    def _check_absolute_path_security(self, path: str) -> SecurityResult:
        """Check if absolute paths are secure."""
        if path.startswith('/') or (len(path) > 1 and path[1] == ':'):
            return SecurityResult(
                is_secure=False,
                error_message="Absolute paths are not allowed for security"
            )
        return SecurityResult(is_secure=True)

    def _check_path_resolution_security(self, path: str, base_directory: str) -> SecurityResult:
        """Perform final path resolution security check using pathlib."""
        base_path = Path(base_directory).resolve()
        target_path = (base_path / path).resolve()

        try:
            target_path.relative_to(base_path)
            return SecurityResult(is_secure=True)
        except ValueError:
            return SecurityResult(
                is_secure=False,
                error_message="Path traversal detected: resolved path outside base directory"
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
        # Start with control characters that are invalid on all platforms
        invalid_chars = self.CONTROL_CHARS.copy()

        if os.name == 'nt':  # Windows
            invalid_chars.update(self.WINDOWS_INVALID_CHARS)
        else:  # Unix-like systems
            invalid_chars.update(self.UNIX_INVALID_CHARS)

        return invalid_chars