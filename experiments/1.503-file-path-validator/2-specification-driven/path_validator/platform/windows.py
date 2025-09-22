"""
Windows-specific path operations and validation.
"""

import os
import re
from typing import Set, List, Optional

from .base import PlatformOperations
from ..exceptions.errors import PathPlatformError, PathSyntaxError


class WindowsOperations(PlatformOperations):
    """Windows-specific path operations and validation."""

    # Windows forbidden characters
    FORBIDDEN_CHARS = set('<>:"|?*\x00')

    # Windows reserved device names
    RESERVED_NAMES = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }

    # Compiled regex patterns for efficiency
    _drive_letter_pattern = re.compile(r'^[A-Za-z]:')
    _unc_pattern = re.compile(r'^\\\\[^\\]+\\[^\\]+')
    _long_path_pattern = re.compile(r'^\\\\?\\.+')

    def __init__(self):
        # Add control characters to forbidden set
        self.forbidden_chars = self.FORBIDDEN_CHARS.copy()
        self.forbidden_chars.update(chr(i) for i in range(32))

    def validate_platform_constraints(self, path: str) -> None:
        """Validate Windows-specific path constraints."""
        # Basic character validation
        self.validate_characters(path)

        # Reserved name validation
        self.validate_reserved_names(path)

        # Length constraints
        self.validate_length_constraints(path)

        # Windows-specific format validation
        self._validate_windows_format(path)

    def _validate_windows_format(self, path: str) -> None:
        """Validate Windows-specific path format requirements."""
        if not path:
            return

        # Check for invalid path starts
        if path.startswith(' ') or path.startswith('.'):
            # Leading spaces and dots can cause issues
            pass  # Warning rather than error in some cases

        # Check for invalid path endings
        if path.endswith(' ') or path.endswith('.'):
            raise PathSyntaxError(
                "Windows paths cannot end with space or dot",
                path=path
            )

        # Validate UNC paths
        if path.startswith('\\\\'):
            self._validate_unc_path(path)

        # Validate drive letter paths
        elif len(path) >= 2 and path[1] == ':':
            self._validate_drive_path(path)

    def _validate_unc_path(self, path: str) -> None:
        """Validate UNC path format."""
        if not self._unc_pattern.match(path) and not self._long_path_pattern.match(path):
            raise PathSyntaxError(
                "Invalid UNC path format",
                path=path
            )

    def _validate_drive_path(self, path: str) -> None:
        """Validate drive letter path format."""
        if not self._drive_letter_pattern.match(path):
            raise PathSyntaxError(
                "Invalid drive letter format",
                path=path
            )

        # Check for valid drive letter
        drive_letter = path[0].upper()
        if not ('A' <= drive_letter <= 'Z'):
            raise PathSyntaxError(
                f"Invalid drive letter: {drive_letter}",
                path=path
            )

    def normalize_separators(self, path: str) -> str:
        """Normalize path separators to Windows backslashes."""
        return path.replace('/', '\\')

    def get_max_path_length(self) -> int:
        """Get maximum path length for Windows."""
        # Traditional Windows limit is 260, but with long path support it's 32767
        # We use the conservative limit by default
        return 260

    def get_max_component_length(self) -> int:
        """Get maximum component length for Windows."""
        return 255

    def get_forbidden_characters(self) -> Set[str]:
        """Get Windows forbidden characters."""
        return self.forbidden_chars

    def is_reserved_name(self, name: str) -> bool:
        """Check if name is a Windows reserved device name."""
        # Remove extension and check base name
        base_name = name.split('.')[0].upper()
        return base_name in self.RESERVED_NAMES

    def is_case_sensitive(self) -> bool:
        """Windows filesystem is case-insensitive by default."""
        return False

    def supports_symlinks(self) -> bool:
        """Windows supports symlinks with appropriate permissions."""
        return hasattr(os, 'symlink')

    def normalize_case(self, path: str) -> str:
        """Normalize case for Windows (convert to lowercase)."""
        return path.lower()

    def split_path(self, path: str) -> List[str]:
        """Split Windows path into components."""
        # Normalize separators first
        normalized = self.normalize_separators(path)

        # Handle UNC paths specially
        if normalized.startswith('\\\\'):
            if normalized.startswith('\\\\?\\'):
                # Long path format
                remainder = normalized[4:]
                parts = ['\\\\?\\'] + remainder.split('\\')
            else:
                # Regular UNC path
                parts = normalized.split('\\')
                # Combine first two empty parts with server name
                if len(parts) >= 3:
                    parts = ['\\\\' + parts[2]] + parts[3:]
        else:
            parts = normalized.split('\\')

        # Filter out empty parts except for the first one (which might be a drive)
        result = []
        for i, part in enumerate(parts):
            if part or i == 0:
                result.append(part)

        return result

    def join_path(self, *components: str) -> str:
        """Join path components using Windows backslashes."""
        if not components:
            return ''

        # Handle special cases for first component
        result = components[0]

        for component in components[1:]:
            if component:
                if not result.endswith('\\') and component:
                    result += '\\'
                result += component

        return result

    def is_absolute(self, path: str) -> bool:
        """Check if Windows path is absolute."""
        if not path:
            return False

        # UNC paths
        if path.startswith('\\\\'):
            return True

        # Drive letter paths
        if len(path) >= 3 and path[1] == ':' and path[2] == '\\':
            return True

        return False

    def get_root(self, path: str) -> Optional[str]:
        """Get the root part of a Windows path."""
        if not path:
            return None

        # UNC paths
        if path.startswith('\\\\'):
            if path.startswith('\\\\?\\'):
                # Long path format - extract the actual root after the prefix
                remainder = path[4:]
                if len(remainder) >= 3 and remainder[1] == ':':
                    return '\\\\?\\' + remainder[:3]
                else:
                    # UNC within long path format
                    parts = remainder.split('\\')
                    if len(parts) >= 2:
                        return '\\\\?\\\\' + parts[0] + '\\' + parts[1]
            else:
                # Regular UNC path
                parts = path.split('\\')
                if len(parts) >= 4:  # \\server\share
                    return '\\\\' + parts[2] + '\\' + parts[3]

        # Drive letter paths
        elif len(path) >= 2 and path[1] == ':':
            if len(path) >= 3 and path[2] == '\\':
                return path[:3]  # C:\
            else:
                return path[:2]  # C:

        return None

    def supports_long_paths(self) -> bool:
        """Check if the system supports long paths (>260 characters)."""
        # This would need to check Windows version and registry settings
        # For now, return False as conservative default
        return False

    def validate_characters(self, path: str) -> None:
        """Override to add Windows-specific character validation."""
        super().validate_characters(path)

        # Additional Windows-specific checks
        # Check for trailing spaces or dots in components
        components = self.split_path(path)
        for component in components:
            if component and (component.endswith(' ') or component.endswith('.')):
                raise PathSyntaxError(
                    f"Windows path component cannot end with space or dot: '{component}'",
                    path=path
                )