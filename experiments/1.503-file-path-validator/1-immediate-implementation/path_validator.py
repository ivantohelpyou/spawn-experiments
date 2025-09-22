#!/usr/bin/env python3
"""
File Path Validator
A comprehensive path validation utility using os.path and pathlib libraries.
"""

import os
import os.path
from pathlib import Path, PurePath
import platform
from typing import Dict, List, Optional, Tuple


class PathValidator:
    """A comprehensive file path validator using os.path and pathlib."""

    def __init__(self):
        self.system = platform.system()

    def validate_path(self, path: str) -> Dict[str, any]:
        """
        Comprehensive path validation.

        Args:
            path: The path string to validate

        Returns:
            Dictionary with validation results and details
        """
        result = {
            'is_valid': False,
            'exists': False,
            'is_file': False,
            'is_directory': False,
            'is_absolute': False,
            'is_relative': False,
            'normalized_path': None,
            'parent_exists': False,
            'errors': [],
            'warnings': []
        }

        try:
            # Basic format validation
            if not path or not isinstance(path, str):
                result['errors'].append("Path must be a non-empty string")
                return result

            # Create Path objects
            path_obj = Path(path)

            # Check if path is properly formatted
            if not self._is_properly_formatted(path):
                result['errors'].append("Path contains invalid characters or format")
                return result

            result['is_valid'] = True
            result['normalized_path'] = str(path_obj.resolve()) if path_obj.exists() else str(path_obj)

            # Path type checks
            result['is_absolute'] = path_obj.is_absolute()
            result['is_relative'] = not path_obj.is_absolute()

            # Existence checks
            result['exists'] = path_obj.exists()
            if result['exists']:
                result['is_file'] = path_obj.is_file()
                result['is_directory'] = path_obj.is_dir()

            # Parent directory check
            try:
                result['parent_exists'] = path_obj.parent.exists()
            except OSError:
                result['parent_exists'] = False
                result['warnings'].append("Cannot check parent directory")

            # Additional validations
            self._check_edge_cases(path, path_obj, result)

        except Exception as e:
            result['errors'].append(f"Validation error: {str(e)}")

        return result

    def _is_properly_formatted(self, path: str) -> bool:
        """Check if path is properly formatted for the current OS."""
        try:
            # Check for null bytes (not allowed in any OS)
            if '\x00' in path:
                return False

            # System-specific checks
            if self.system == 'Windows':
                return self._validate_windows_path(path)
            else:
                return self._validate_unix_path(path)

        except Exception:
            return False

    def _validate_windows_path(self, path: str) -> bool:
        """Validate Windows-specific path format."""
        # Invalid characters for Windows
        invalid_chars = '<>:"|?*'
        for char in invalid_chars:
            if char in path:
                return False

        # Check for reserved names
        reserved_names = {
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        }

        path_parts = Path(path).parts
        for part in path_parts:
            if part.upper() in reserved_names:
                return False

        return True

    def _validate_unix_path(self, path: str) -> bool:
        """Validate Unix/Linux-specific path format."""
        # Unix paths are generally more permissive
        # Main restriction is null bytes (already checked)
        return True

    def _check_edge_cases(self, path: str, path_obj: Path, result: Dict):
        """Check for common edge cases and add warnings."""

        # Very long paths
        if len(path) > 260:  # Windows MAX_PATH limitation
            result['warnings'].append("Path exceeds Windows MAX_PATH limit (260 characters)")

        # Paths with spaces at the end
        if path.endswith(' '):
            result['warnings'].append("Path ends with space character")

        # Hidden files/directories (Unix-style)
        if any(part.startswith('.') and len(part) > 1 for part in path_obj.parts):
            result['warnings'].append("Path contains hidden files/directories")

        # Case sensitivity warnings
        if self.system == 'Windows' and any(c.isupper() and c.islower() for c in path):
            result['warnings'].append("Mixed case in path (Windows is case-insensitive)")

        # Network paths
        if path.startswith('\\\\') or path.startswith('//'):
            result['warnings'].append("Network path detected")

        # Relative path going up too many levels
        if '../' in path or '..\\' in path:
            up_count = path.count('../') + path.count('..\\')
            if up_count > 3:
                result['warnings'].append(f"Path goes up {up_count} directory levels")


def validate_paths(paths: List[str]) -> Dict[str, Dict]:
    """Validate multiple paths at once."""
    validator = PathValidator()
    results = {}

    for path in paths:
        results[path] = validator.validate_path(path)

    return results


def demo():
    """Demonstration of the path validator."""
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
        "very/long/path" + "/part" * 50,
    ]

    print("File Path Validator Demo")
    print("=" * 50)

    for path in test_paths:
        result = validator.validate_path(path)
        print(f"\nPath: '{path}'")
        print(f"Valid: {result['is_valid']}")
        print(f"Exists: {result['exists']}")
        print(f"Type: {'File' if result['is_file'] else 'Directory' if result['is_directory'] else 'N/A'}")
        print(f"Absolute: {result['is_absolute']}")

        if result['errors']:
            print(f"Errors: {', '.join(result['errors'])}")
        if result['warnings']:
            print(f"Warnings: {', '.join(result['warnings'])}")


if __name__ == "__main__":
    demo()