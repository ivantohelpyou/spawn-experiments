"""
POSIX-specific path operations and validation (Linux, macOS, Unix).
"""

import os
from typing import Set, List, Optional

from .base import PlatformOperations
from ..exceptions.errors import PathSyntaxError


class PosixOperations(PlatformOperations):
    """POSIX-specific path operations and validation."""

    # POSIX systems only forbid null bytes in filenames
    FORBIDDEN_CHARS = {'\x00'}

    def validate_platform_constraints(self, path: str) -> None:
        """Validate POSIX-specific path constraints."""
        # Basic character validation
        self.validate_characters(path)

        # Length constraints
        self.validate_length_constraints(path)

        # POSIX-specific validation
        self._validate_posix_format(path)

    def _validate_posix_format(self, path: str) -> None:
        """Validate POSIX-specific path format requirements."""
        if not path:
            return

        # Check for extremely long components (filesystem-dependent)
        components = self.split_path(path)
        for component in components:
            if component:
                # Check byte length for UTF-8 encoding
                byte_length = len(component.encode('utf-8'))
                if byte_length > self.get_max_component_length():
                    raise PathSyntaxError(
                        f"Component byte length {byte_length} exceeds maximum {self.get_max_component_length()}",
                        path=path
                    )

    def normalize_separators(self, path: str) -> str:
        """Normalize path separators to POSIX forward slashes."""
        return path.replace('\\', '/')

    def get_max_path_length(self) -> int:
        """Get maximum path length for POSIX systems."""
        # Try to get from system configuration
        try:
            if hasattr(os, 'pathconf') and hasattr(os, 'pathconf_names'):
                path_max = os.pathconf_names.get('PC_PATH_MAX')
                if path_max is not None:
                    return os.pathconf('/', path_max)
        except (OSError, AttributeError):
            pass

        # Default POSIX limit
        return 4096

    def get_max_component_length(self) -> int:
        """Get maximum component length for POSIX systems."""
        # Try to get from system configuration
        try:
            if hasattr(os, 'pathconf') and hasattr(os, 'pathconf_names'):
                name_max = os.pathconf_names.get('PC_NAME_MAX')
                if name_max is not None:
                    return os.pathconf('/', name_max)
        except (OSError, AttributeError):
            pass

        # Default limit (255 bytes for most filesystems)
        return 255

    def get_forbidden_characters(self) -> Set[str]:
        """Get POSIX forbidden characters (only null byte)."""
        return self.FORBIDDEN_CHARS

    def is_reserved_name(self, name: str) -> bool:
        """POSIX systems don't have reserved names at filesystem level."""
        return False

    def is_case_sensitive(self) -> bool:
        """Most POSIX filesystems are case-sensitive."""
        # This could be filesystem-dependent, but default to case-sensitive
        return True

    def supports_symlinks(self) -> bool:
        """POSIX systems support symbolic links."""
        return hasattr(os, 'symlink') and hasattr(os, 'readlink')

    def normalize_case(self, path: str) -> str:
        """POSIX systems are case-sensitive, so preserve original case."""
        return path

    def split_path(self, path: str) -> List[str]:
        """Split POSIX path into components."""
        # Normalize separators first
        normalized = self.normalize_separators(path)

        # Split on forward slashes
        parts = normalized.split('/')

        # Handle absolute paths (first part will be empty)
        result = []
        for i, part in enumerate(parts):
            if part or i == 0:  # Keep empty first part for absolute paths
                result.append(part)

        return result

    def join_path(self, *components: str) -> str:
        """Join path components using POSIX forward slashes."""
        if not components:
            return ''

        # Handle special case for absolute paths
        result = components[0]

        for component in components[1:]:
            if component:
                if not result.endswith('/') and result:
                    result += '/'
                result += component

        return result

    def is_absolute(self, path: str) -> bool:
        """Check if POSIX path is absolute."""
        return path.startswith('/')

    def get_root(self, path: str) -> Optional[str]:
        """Get the root part of a POSIX path."""
        if self.is_absolute(path):
            return '/'
        return None

    def validate_component_encoding(self, component: str) -> None:
        """Validate that a component can be properly encoded."""
        try:
            # Try to encode as UTF-8 (most common encoding)
            encoded = component.encode('utf-8')
            if len(encoded) > self.get_max_component_length():
                raise PathSyntaxError(
                    f"Component '{component}' is too long when encoded ({len(encoded)} bytes)",
                    path=component
                )
        except UnicodeEncodeError as e:
            raise PathSyntaxError(
                f"Component '{component}' cannot be encoded: {e}",
                path=component
            )

    def is_hidden_file(self, name: str) -> bool:
        """Check if a filename represents a hidden file (starts with dot)."""
        return name.startswith('.') and name not in ('.', '..')

    def validate_symlink_target(self, link_path: str, target_path: str) -> None:
        """Validate that a symlink target is safe."""
        # Basic validation - target shouldn't be null
        if not target_path:
            raise PathSyntaxError(
                "Symlink target cannot be empty",
                path=link_path
            )

        # Check for null bytes in target
        if '\x00' in target_path:
            raise PathSyntaxError(
                "Symlink target contains null byte",
                path=link_path
            )

    def get_filesystem_encoding(self) -> str:
        """Get the filesystem encoding for the system."""
        import sys
        return sys.getfilesystemencoding() or 'utf-8'

    def normalize_unicode(self, path: str) -> str:
        """Normalize Unicode in path for consistent comparison."""
        import unicodedata
        # Use NFC normalization (Canonical Decomposition followed by Canonical Composition)
        return unicodedata.normalize('NFC', path)

    def validate_length_constraints(self, path: str) -> None:
        """Override to use byte-based component length validation."""
        from ..exceptions.errors import PathLengthError

        # Check total path length
        max_path_length = self.get_max_path_length()
        if len(path) > max_path_length:
            raise PathLengthError(
                f"Path length {len(path)} exceeds maximum {max_path_length}",
                path=path,
                actual_length=len(path),
                max_length=max_path_length
            )

        # Check individual component lengths (byte-based for POSIX)
        max_component_length = self.get_max_component_length()
        components = self.split_path(path)

        for component in components:
            if component:
                # Use byte length for POSIX systems
                byte_length = len(component.encode('utf-8', errors='replace'))
                if byte_length > max_component_length:
                    raise PathLengthError(
                        f"Component '{component}' byte length {byte_length} exceeds maximum {max_component_length}",
                        path=path,
                        actual_length=byte_length,
                        max_length=max_component_length
                    )