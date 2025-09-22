"""
Path normalization utilities.
"""

import os
import os.path
import unicodedata
from pathlib import Path
from typing import Optional

from ..utils.config import ValidationConfig
from ..exceptions.errors import PathUnicodeError


class PathNormalizer:
    """Handles path normalization operations."""

    def __init__(self, config: Optional[ValidationConfig] = None):
        self.config = config or ValidationConfig()

    def normalize(self, path: str) -> str:
        """
        Perform comprehensive path normalization.

        Args:
            path: Path to normalize

        Returns:
            str: Normalized path

        Raises:
            PathUnicodeError: If Unicode normalization fails
        """
        # Start with the original path
        normalized = path

        # Unicode normalization
        if self.config.normalize_unicode:
            normalized = self._normalize_unicode(normalized)

        # Platform-specific separator normalization
        normalized = self._normalize_separators(normalized)

        # Remove redundant separators and resolve dots
        normalized = self._normalize_structure(normalized)

        # Case normalization (platform-dependent)
        normalized = self._normalize_case(normalized)

        # Resolve relative paths to absolute if configured
        if self.config.require_absolute and not os.path.isabs(normalized):
            normalized = os.path.abspath(normalized)

        return normalized

    def _normalize_unicode(self, path: str) -> str:
        """Normalize Unicode characters in the path."""
        try:
            # Use NFC normalization (Canonical Decomposition followed by Canonical Composition)
            # This is the most compatible form for filesystem operations
            return unicodedata.normalize('NFC', path)
        except Exception as e:
            raise PathUnicodeError(
                f"Unicode normalization failed: {e}",
                path=path,
                encoding='utf-8'
            )

    def _normalize_separators(self, path: str) -> str:
        """Normalize path separators for the current platform."""
        if os.sep == '/':
            # POSIX systems - convert backslashes to forward slashes
            return path.replace('\\', '/')
        else:
            # Windows - convert forward slashes to backslashes, but preserve UNC prefixes
            if path.startswith('\\\\'):
                # UNC path - don't touch the leading double backslash
                return path
            else:
                return path.replace('/', '\\')

    def _normalize_structure(self, path: str) -> str:
        """Normalize path structure by resolving dots and redundant separators."""
        # Use os.path.normpath for basic normalization
        normalized = os.path.normpath(path)

        # Additional cleanup for multiple consecutive separators
        if os.sep == '/':
            # POSIX: Replace multiple slashes with single slash (except at start for absolute paths)
            if normalized.startswith('/'):
                # Preserve leading slash for absolute paths
                normalized = '/' + normalized[1:].replace('//', '/')
            else:
                normalized = normalized.replace('//', '/')
        else:
            # Windows: Handle UNC paths specially
            if normalized.startswith('\\\\'):
                # UNC path - preserve double backslash at start
                remainder = normalized[2:]
                cleaned = remainder.replace('\\\\', '\\')
                normalized = '\\\\' + cleaned
            else:
                # Regular Windows path
                normalized = normalized.replace('\\\\', '\\')

        return normalized

    def _normalize_case(self, path: str) -> str:
        """Normalize case based on platform conventions."""
        # Only normalize case if not explicitly preserving it
        if self.config.case_sensitive is False:
            # Force case-insensitive (typically for Windows)
            return path.lower()
        elif self.config.case_sensitive is True:
            # Preserve original case (typically for POSIX)
            return path
        else:
            # Auto-detect based on platform
            if os.name == 'nt':  # Windows
                return path.lower()
            else:  # POSIX
                return path

    def expand_user_path(self, path: str) -> str:
        """Expand user home directory references (~)."""
        try:
            return os.path.expanduser(path)
        except Exception:
            # If expansion fails, return original path
            return path

    def expand_variables(self, path: str) -> str:
        """Expand environment variables in the path."""
        try:
            return os.path.expandvars(path)
        except Exception:
            # If expansion fails, return original path
            return path

    def resolve_symlinks(self, path: str) -> str:
        """Resolve symbolic links in the path."""
        if not self.config.follow_symlinks:
            return path

        try:
            # Use realpath to resolve all symbolic links
            return os.path.realpath(path)
        except Exception:
            # If resolution fails, return original path
            return path

    def make_relative(self, path: str, start: Optional[str] = None) -> str:
        """
        Convert absolute path to relative path.

        Args:
            path: Path to make relative
            start: Starting directory (default: current directory)

        Returns:
            str: Relative path
        """
        try:
            if start is None:
                start = os.getcwd()
            return os.path.relpath(path, start)
        except Exception:
            # If conversion fails, return original path
            return path

    def make_absolute(self, path: str) -> str:
        """
        Convert relative path to absolute path.

        Args:
            path: Path to make absolute

        Returns:
            str: Absolute path
        """
        try:
            return os.path.abspath(path)
        except Exception:
            # If conversion fails, return original path
            return path

    def clean_path(self, path: str) -> str:
        """
        Clean path by removing unnecessary components.

        Args:
            path: Path to clean

        Returns:
            str: Cleaned path
        """
        # Remove trailing separators (except for root)
        cleaned = path.rstrip(os.sep)

        # Handle special cases
        if not cleaned:
            # Empty path after stripping
            return os.sep if path.endswith(os.sep) else '.'

        # Handle root paths
        if os.name == 'nt':
            # Windows root paths
            if len(cleaned) == 2 and cleaned.endswith(':'):
                return cleaned + os.sep
        else:
            # POSIX root path
            if cleaned == '':
                return os.sep

        return cleaned

    def is_normalized(self, path: str) -> bool:
        """
        Check if a path is already in normalized form.

        Args:
            path: Path to check

        Returns:
            bool: True if path is normalized
        """
        try:
            normalized = self.normalize(path)
            return path == normalized
        except Exception:
            return False

    def get_common_prefix(self, paths: list) -> str:
        """
        Get the common prefix of multiple paths.

        Args:
            paths: List of paths

        Returns:
            str: Common prefix path
        """
        if not paths:
            return ''

        try:
            # Normalize all paths first
            normalized_paths = [self.normalize(path) for path in paths]
            return os.path.commonpath(normalized_paths)
        except Exception:
            # If commonpath fails, fall back to commonprefix
            try:
                return os.path.commonprefix(paths)
            except Exception:
                return ''

    def split_extension(self, path: str) -> tuple:
        """
        Split path into base and extension.

        Args:
            path: Path to split

        Returns:
            tuple: (base_path, extension)
        """
        return os.path.splitext(path)

    def change_extension(self, path: str, new_extension: str) -> str:
        """
        Change the extension of a path.

        Args:
            path: Original path
            new_extension: New extension (with or without leading dot)

        Returns:
            str: Path with new extension
        """
        base, _ = self.split_extension(path)

        # Ensure extension starts with dot
        if new_extension and not new_extension.startswith('.'):
            new_extension = '.' + new_extension

        return base + new_extension

    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize a filename by removing/replacing invalid characters.

        Args:
            filename: Filename to sanitize

        Returns:
            str: Sanitized filename
        """
        # Remove null bytes
        sanitized = filename.replace('\x00', '')

        # Platform-specific sanitization
        if os.name == 'nt':
            # Windows - replace forbidden characters
            forbidden_chars = '<>:"|?*'
            for char in forbidden_chars:
                sanitized = sanitized.replace(char, '_')

            # Remove control characters
            sanitized = ''.join(char for char in sanitized if ord(char) >= 32)

            # Remove trailing spaces and dots
            sanitized = sanitized.rstrip(' .')

            # Check for reserved names
            reserved_names = {
                'CON', 'PRN', 'AUX', 'NUL',
                'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
            }

            base_name = sanitized.split('.')[0].upper()
            if base_name in reserved_names:
                sanitized = '_' + sanitized

        else:
            # POSIX - only remove null bytes (already done above)
            pass

        # Ensure filename is not empty
        if not sanitized:
            sanitized = 'unnamed'

        return sanitized