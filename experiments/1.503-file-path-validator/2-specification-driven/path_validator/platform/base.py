"""
Abstract base class for platform-specific operations.
"""

from abc import ABC, abstractmethod
from typing import Set, List, Optional


class PlatformOperations(ABC):
    """Abstract base class for platform-specific path operations."""

    @abstractmethod
    def validate_platform_constraints(self, path: str) -> None:
        """
        Validate platform-specific path constraints.

        Args:
            path: Path to validate

        Raises:
            PathValidationError: If path violates platform constraints
        """
        pass

    @abstractmethod
    def normalize_separators(self, path: str) -> str:
        """
        Normalize path separators for the platform.

        Args:
            path: Path with potentially mixed separators

        Returns:
            str: Path with normalized separators
        """
        pass

    @abstractmethod
    def get_max_path_length(self) -> int:
        """
        Get maximum path length for the platform.

        Returns:
            int: Maximum path length in characters
        """
        pass

    @abstractmethod
    def get_max_component_length(self) -> int:
        """
        Get maximum filename component length for the platform.

        Returns:
            int: Maximum component length in characters/bytes
        """
        pass

    @abstractmethod
    def get_forbidden_characters(self) -> Set[str]:
        """
        Get set of forbidden characters for the platform.

        Returns:
            set: Set of characters that cannot appear in paths
        """
        pass

    @abstractmethod
    def is_reserved_name(self, name: str) -> bool:
        """
        Check if name is reserved on the platform.

        Args:
            name: Filename or directory name to check

        Returns:
            bool: True if name is reserved
        """
        pass

    @abstractmethod
    def is_case_sensitive(self) -> bool:
        """
        Check if the platform filesystem is case-sensitive.

        Returns:
            bool: True if case-sensitive, False otherwise
        """
        pass

    @abstractmethod
    def supports_symlinks(self) -> bool:
        """
        Check if the platform supports symbolic links.

        Returns:
            bool: True if symlinks are supported
        """
        pass

    @abstractmethod
    def normalize_case(self, path: str) -> str:
        """
        Normalize case for the platform if needed.

        Args:
            path: Path to normalize

        Returns:
            str: Case-normalized path
        """
        pass

    @abstractmethod
    def split_path(self, path: str) -> List[str]:
        """
        Split path into components for the platform.

        Args:
            path: Path to split

        Returns:
            list: List of path components
        """
        pass

    @abstractmethod
    def join_path(self, *components: str) -> str:
        """
        Join path components using platform-appropriate separator.

        Args:
            *components: Path components to join

        Returns:
            str: Joined path
        """
        pass

    @abstractmethod
    def is_absolute(self, path: str) -> bool:
        """
        Check if path is absolute for the platform.

        Args:
            path: Path to check

        Returns:
            bool: True if path is absolute
        """
        pass

    @abstractmethod
    def get_root(self, path: str) -> Optional[str]:
        """
        Get the root part of the path (drive letter, UNC prefix, etc.).

        Args:
            path: Path to analyze

        Returns:
            str or None: Root part of path, or None if relative
        """
        pass

    def validate_length_constraints(self, path: str) -> None:
        """
        Validate path length constraints for the platform.

        Args:
            path: Path to validate

        Raises:
            PathLengthError: If path exceeds length limits
        """
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

        # Check individual component lengths
        max_component_length = self.get_max_component_length()
        components = self.split_path(path)

        for component in components:
            if component and len(component) > max_component_length:
                raise PathLengthError(
                    f"Component '{component}' length {len(component)} exceeds maximum {max_component_length}",
                    path=path,
                    actual_length=len(component),
                    max_length=max_component_length
                )

    def validate_characters(self, path: str) -> None:
        """
        Validate that path contains only allowed characters.

        Args:
            path: Path to validate

        Raises:
            PathSyntaxError: If path contains forbidden characters
        """
        from ..exceptions.errors import PathSyntaxError

        forbidden_chars = self.get_forbidden_characters()
        invalid_chars = []

        for char in path:
            if char in forbidden_chars:
                invalid_chars.append(char)

        if invalid_chars:
            # Format invalid characters for display
            formatted_chars = []
            for char in invalid_chars:
                if char == '\x00':
                    formatted_chars.append('\\0')
                elif ord(char) < 32:
                    formatted_chars.append(f'\\x{ord(char):02x}')
                else:
                    formatted_chars.append(repr(char))

            raise PathSyntaxError(
                f"Path contains forbidden characters: {', '.join(formatted_chars)}",
                path=path,
                invalid_chars=invalid_chars
            )

    def validate_reserved_names(self, path: str) -> None:
        """
        Validate that path components are not reserved names.

        Args:
            path: Path to validate

        Raises:
            PathPlatformError: If path contains reserved names
        """
        from ..exceptions.errors import PathPlatformError

        components = self.split_path(path)

        for component in components:
            if component and self.is_reserved_name(component):
                raise PathPlatformError(
                    f"Reserved name not allowed: '{component}'",
                    path=path,
                    platform=self.__class__.__name__
                )