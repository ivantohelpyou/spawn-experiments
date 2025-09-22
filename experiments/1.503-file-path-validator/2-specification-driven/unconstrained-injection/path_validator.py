#!/usr/bin/env python3
"""
File Path Validator - Minimal Working Implementation
Validates file and directory paths with basic validation rules.
"""

import os
import re
import pathlib
from typing import Union, List, Optional, Dict, Any


class ValidationResult:
    """Simple validation result container."""

    def __init__(self, is_valid: bool, path: str, errors: List[str] = None):
        self.is_valid = is_valid
        self.path = path
        self.errors = errors or []

    def __str__(self):
        if self.is_valid:
            return f"✓ Valid: {self.path}"
        else:
            return f"✗ Invalid: {self.path} - {', '.join(self.errors)}"


class PathValidator:
    """Core file path validator with essential validation rules."""

    # OS-specific invalid characters
    WINDOWS_INVALID_CHARS = '<>:"|?*\x00'
    POSIX_INVALID_CHARS = '\x00'

    # Windows reserved names
    WINDOWS_RESERVED = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }

    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self.is_windows = os.name == 'nt'

    def validate(self, path: Union[str, pathlib.Path]) -> ValidationResult:
        """Validate a single path."""
        path_str = str(path)
        errors = []

        # Basic checks
        if not path_str or not path_str.strip():
            errors.append("Path cannot be empty")
            return ValidationResult(False, path_str, errors)

        # Length checks
        if len(path_str) > (260 if self.is_windows else 4096):
            errors.append(f"Path too long (max {260 if self.is_windows else 4096} chars)")

        # Character validation
        invalid_chars = self._get_invalid_chars()
        found_invalid = []
        for char in path_str:
            if char in invalid_chars:
                found_invalid.append(char)

        if found_invalid:
            errors.append(f"Invalid characters: {', '.join(repr(c) for c in set(found_invalid))}")

        # Component validation
        try:
            components = pathlib.Path(path_str).parts
        except (ValueError, OSError):
            errors.append("Invalid path format")
            return ValidationResult(False, path_str, errors)

        for component in components:
            if not component or component in ('.', '..') or component == '/' or component.endswith(':'):
                continue

            # Check component length
            if len(component.encode('utf-8')) > 255:
                errors.append(f"Component too long: {component}")

            # Windows reserved names
            if self.is_windows or self.strict_mode:
                name_without_ext = component.split('.')[0].upper()
                if name_without_ext in self.WINDOWS_RESERVED:
                    errors.append(f"Reserved name: {component}")

            # Leading/trailing spaces and dots (Windows)
            if (self.is_windows or self.strict_mode) and (
                component.endswith(' ') or component.endswith('.') or
                component.startswith(' ')
            ):
                errors.append(f"Invalid component format: {component}")

        return ValidationResult(len(errors) == 0, path_str, errors)

    def validate_batch(self, paths: List[Union[str, pathlib.Path]]) -> List[ValidationResult]:
        """Validate multiple paths."""
        return [self.validate(path) for path in paths]

    def is_valid(self, path: Union[str, pathlib.Path]) -> bool:
        """Simple boolean validation check."""
        return self.validate(path).is_valid

    def exists(self, path: Union[str, pathlib.Path]) -> bool:
        """Check if path exists on filesystem."""
        return pathlib.Path(path).exists()

    def normalize(self, path: Union[str, pathlib.Path]) -> str:
        """Normalize path for current OS."""
        return str(pathlib.Path(path).resolve())

    def _get_invalid_chars(self) -> str:
        """Get invalid characters for current OS."""
        if self.is_windows or self.strict_mode:
            return self.WINDOWS_INVALID_CHARS
        return self.POSIX_INVALID_CHARS


# Convenience functions for quick usage
def validate_path(path: Union[str, pathlib.Path], strict: bool = True) -> ValidationResult:
    """Quick path validation function."""
    validator = PathValidator(strict_mode=strict)
    return validator.validate(path)


def is_valid_path(path: Union[str, pathlib.Path], strict: bool = True) -> bool:
    """Quick boolean path validation."""
    return validate_path(path, strict).is_valid


def validate_paths(paths: List[Union[str, pathlib.Path]], strict: bool = True) -> List[ValidationResult]:
    """Quick batch path validation."""
    validator = PathValidator(strict_mode=strict)
    return validator.validate_batch(paths)


if __name__ == "__main__":
    # Quick demo
    validator = PathValidator()

    test_paths = [
        "/valid/path/file.txt",
        "C:\\valid\\windows\\path.doc",
        "/path/with/invalid<char",
        "CON.txt",  # Windows reserved
        "",  # Empty path
        "valid_file.py",
        "/very/long/path/" + "x" * 300,  # Too long
    ]

    print("File Path Validator - Quick Demo")
    print("=" * 40)

    for path in test_paths:
        result = validator.validate(path)
        print(result)