#!/usr/bin/env python3
"""
Simple File Path Validator
A focused, reliable path validation utility matching market demands.
"""

import os
import platform
from pathlib import Path
from typing import Dict, List, Set, Union, Any


class PathValidator:
    """Simple, reliable file path validator."""

    def __init__(self):
        self.system = platform.system()

    def validate_path(self, path: Union[str, Path]) -> Dict[str, Any]:
        """
        Validate a path and return comprehensive results.

        Args:
            path: The path to validate (string or Path object)

        Returns:
            Dictionary with validation results:
            {
                'is_valid': bool,           # Overall validity
                'exists': bool,             # Path exists on filesystem
                'is_file': bool,            # Is a file
                'is_directory': bool,       # Is a directory
                'is_absolute': bool,        # Is absolute path
                'normalized_path': str,     # Normalized path
                'parent_exists': bool,      # Parent directory exists
                'errors': List[str],        # Error messages
                'warnings': List[str]       # Warning messages
            }
        """
        result = {
            'is_valid': False,
            'exists': False,
            'is_file': False,
            'is_directory': False,
            'is_absolute': False,
            'normalized_path': None,
            'parent_exists': False,
            'errors': [],
            'warnings': []
        }

        try:
            # Input validation
            if not self._validate_input(path, result):
                return result

            path_str = str(path)
            path_obj = Path(path_str)

            # Format validation
            if not self._validate_format(path_str, result):
                return result

            # Platform-specific validation
            if not self._validate_platform_constraints(path_str, result):
                return result

            # Length validation
            self._validate_length(path_str, result)

            # If we get here, basic validation passed
            result['is_valid'] = True

            # Path type checks
            result['is_absolute'] = path_obj.is_absolute()

            # Existence checks (with error handling)
            self._check_existence(path_obj, result)

            # Normalization
            result['normalized_path'] = str(path_obj.resolve() if result['exists'] else path_obj)

        except Exception as e:
            result['errors'].append(f"Validation error: {str(e)}")

        return result

    def is_valid_path(self, path: Union[str, Path]) -> bool:
        """
        Simple boolean check if path is valid.

        Args:
            path: The path to validate

        Returns:
            True if path is valid, False otherwise
        """
        return self.validate_path(path)['is_valid']

    def normalize_path(self, path: Union[str, Path]) -> str:
        """
        Normalize a path with validation.

        Args:
            path: The path to normalize

        Returns:
            Normalized path string

        Raises:
            ValueError: If path is invalid
        """
        result = self.validate_path(path)
        if not result['is_valid']:
            raise ValueError(f"Invalid path: {', '.join(result['errors'])}")
        return result['normalized_path']

    def _validate_input(self, path: Union[str, Path], result: Dict[str, Any]) -> bool:
        """Validate basic input requirements."""
        if path is None:
            result['errors'].append("Path cannot be None")
            return False

        if isinstance(path, str):
            if not path:
                result['errors'].append("Path cannot be empty")
                return False
        elif isinstance(path, Path):
            if not str(path):
                result['errors'].append("Path cannot be empty")
                return False
        else:
            result['errors'].append("Path must be a string or Path object")
            return False

        return True

    def _validate_format(self, path: str, result: Dict[str, Any]) -> bool:
        """Validate path format and characters."""
        # Check for null bytes (forbidden on all platforms)
        if '\x00' in path:
            result['errors'].append("Path contains null bytes")
            return False

        # Platform-specific character validation
        forbidden_chars = self._get_forbidden_characters()
        invalid_chars = [char for char in path if char in forbidden_chars]
        if invalid_chars:
            result['errors'].append(f"Path contains invalid characters: {''.join(set(invalid_chars))}")
            return False

        # Check for reserved names
        if self._contains_reserved_names(path):
            return False

        # Check for traversal patterns (add warnings, don't fail)
        self._check_traversal_patterns(path, result)

        return True

    def _validate_platform_constraints(self, path: str, result: Dict[str, Any]) -> bool:
        """Validate platform-specific constraints."""
        if self.system == 'Windows':
            return self._validate_windows_constraints(path, result)
        else:
            return self._validate_posix_constraints(path, result)

    def _validate_windows_constraints(self, path: str, result: Dict[str, Any]) -> bool:
        """Validate Windows-specific constraints."""
        # Check for reserved names in path components
        path_obj = Path(path)
        reserved_names = self._get_reserved_names()

        for part in path_obj.parts:
            # Remove extension for reserved name check
            base_name = part.split('.')[0].upper()
            if base_name in reserved_names:
                result['errors'].append(f"Reserved name not allowed: {part}")
                return False

        return True

    def _validate_posix_constraints(self, path: str, result: Dict[str, Any]) -> bool:
        """Validate POSIX-specific constraints."""
        # POSIX is generally more permissive
        # Main restriction is null bytes (already checked)
        return True

    def _validate_length(self, path: str, result: Dict[str, Any]) -> None:
        """Validate path length constraints."""
        max_length = self._get_max_path_length()

        if len(path) > max_length:
            if self.system == 'Windows' and len(path) > 260:
                result['warnings'].append(f"Path exceeds Windows MAX_PATH limit (260 characters)")
            result['warnings'].append(f"Path exceeds maximum length ({max_length} characters)")

        # Check component lengths
        path_obj = Path(path)
        for part in path_obj.parts:
            if part and len(part) > 255:  # Standard component limit
                result['warnings'].append(f"Path component too long: {part[:50]}...")

    def _check_existence(self, path_obj: Path, result: Dict[str, Any]) -> None:
        """Check path existence with error handling."""
        try:
            result['exists'] = path_obj.exists()
            if result['exists']:
                result['is_file'] = path_obj.is_file()
                result['is_directory'] = path_obj.is_dir()

            # Check parent directory
            try:
                result['parent_exists'] = path_obj.parent.exists()
            except OSError:
                result['parent_exists'] = False
                result['warnings'].append("Cannot check parent directory")

        except OSError as e:
            result['warnings'].append(f"Cannot check existence: {str(e)}")

    def _check_traversal_patterns(self, path: str, result: Dict[str, Any]) -> None:
        """Check for directory traversal patterns."""
        if '../' in path or '..\\' in path:
            result['warnings'].append("Path contains directory traversal patterns")

        # Count traversal attempts
        up_count = path.count('../') + path.count('..\\')
        if up_count > 3:
            result['warnings'].append(f"Path traverses up {up_count} directory levels")

    def _contains_reserved_names(self, path: str) -> bool:
        """Check if path contains reserved names."""
        if self.system != 'Windows':
            return False

        reserved_names = self._get_reserved_names()
        path_obj = Path(path)

        for part in path_obj.parts:
            base_name = part.split('.')[0].upper()
            if base_name in reserved_names:
                return True

        return False

    def _get_forbidden_characters(self) -> Set[str]:
        """Get forbidden characters for current platform."""
        if self.system == 'Windows':
            return set('<>:"|?*\x00')
        else:
            return set('\x00')

    def _get_reserved_names(self) -> Set[str]:
        """Get reserved names for current platform."""
        if self.system == 'Windows':
            return {
                'CON', 'PRN', 'AUX', 'NUL',
                'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
            }
        else:
            return set()

    def _get_max_path_length(self) -> int:
        """Get maximum path length for current platform."""
        if self.system == 'Windows':
            return 260  # MAX_PATH
        else:
            return 4096  # Typical POSIX limit


# Convenience functions for the public API
def validate_path(path: Union[str, Path]) -> Dict[str, Any]:
    """
    Validate a path using default validator.

    Args:
        path: The path to validate

    Returns:
        Validation result dictionary
    """
    validator = PathValidator()
    return validator.validate_path(path)


def is_valid_path(path: Union[str, Path]) -> bool:
    """
    Quick boolean check if path is valid.

    Args:
        path: The path to validate

    Returns:
        True if path is valid, False otherwise
    """
    validator = PathValidator()
    return validator.is_valid_path(path)


def demo():
    """Demonstration of the simplified path validator."""
    validator = PathValidator()

    test_paths = [
        "/home/user/document.txt",
        "relative/path/file.txt",
        "../parent/file.txt",
        "/nonexistent/path/file.txt",
        "",
        "/home/user/",
        ".",
        "..",
        "/tmp",
        "file with spaces.txt",
        "CON.txt",  # Windows reserved name
        "path<with>invalid|chars.txt",  # Invalid characters
        "very/long/path" + "/part" * 30,  # Long path
    ]

    print("Simple File Path Validator Demo")
    print("=" * 50)

    for path in test_paths:
        result = validator.validate_path(path)
        print(f"\nPath: '{path}'")
        print(f"Valid: {result['is_valid']}")

        if result['is_valid']:
            print(f"Exists: {result['exists']}")
            print(f"Type: {'File' if result['is_file'] else 'Directory' if result['is_directory'] else 'N/A'}")
            print(f"Absolute: {result['is_absolute']}")
            print(f"Normalized: {result['normalized_path']}")

        if result['errors']:
            print(f"Errors: {', '.join(result['errors'])}")
        if result['warnings']:
            print(f"Warnings: {', '.join(result['warnings'])}")


if __name__ == "__main__":
    demo()