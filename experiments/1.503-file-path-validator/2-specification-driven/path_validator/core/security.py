"""
Security validation for path operations.
"""

import os
import os.path
import re
import urllib.parse
from typing import List, Set, Optional
from pathlib import Path

from ..utils.config import SecurityPolicy, SymlinkPolicy
from ..exceptions.errors import (
    PathSecurityError,
    PathTraversalError,
    PathPermissionError
)


class SecurityValidator:
    """Handles security-related path validation."""

    def __init__(self, policy: Optional[SecurityPolicy] = None):
        self.policy = policy or SecurityPolicy()
        self.traversal_detector = TraversalDetector()
        self.symlink_validator = SymlinkValidator(self.policy)
        self.sandbox_validator = SandboxValidator(self.policy)

    def validate(self, path: str) -> None:
        """
        Perform comprehensive security validation.

        Args:
            path: Path to validate

        Raises:
            PathSecurityError: If security validation fails
        """
        # Path traversal detection
        if self.policy.prevent_traversal:
            self.traversal_detector.detect_traversal(path)

        # Input sanitization
        if self.policy.sanitize_input:
            self._validate_input_safety(path)

        # Symlink validation
        if self.policy.symlink_policy != SymlinkPolicy.FOLLOW:
            self.symlink_validator.validate_symlinks(path)

        # Sandbox validation
        if self.policy.sandbox_roots:
            self.sandbox_validator.validate_sandbox_constraints(path)

    def _validate_input_safety(self, path: str) -> None:
        """Validate input for potential injection attacks."""
        # Check for null byte injection
        if '\x00' in path:
            raise PathSecurityError(
                "Null byte injection detected",
                path=path,
                threat_type="NULL_BYTE_INJECTION"
            )

        # Check for control characters
        control_chars = []
        for char in path:
            if ord(char) < 32 and char not in ('\t', '\n', '\r'):
                control_chars.append(char)

        if control_chars:
            raise PathSecurityError(
                f"Control characters detected: {control_chars}",
                path=path,
                threat_type="CONTROL_CHAR_INJECTION"
            )

        # Check for suspiciously long paths (potential buffer overflow)
        if len(path) > self.policy.max_path_length:
            raise PathSecurityError(
                f"Path length {len(path)} exceeds security limit {self.policy.max_path_length}",
                path=path,
                threat_type="BUFFER_OVERFLOW_ATTEMPT"
            )


class TraversalDetector:
    """Detects various forms of path traversal attacks."""

    # Common path traversal patterns
    TRAVERSAL_PATTERNS = [
        '../',          # Basic Unix traversal
        '..\\',         # Basic Windows traversal
        '..%2f',        # URL encoded forward slash
        '..%5c',        # URL encoded backslash
        '..%252f',      # Double URL encoded forward slash
        '..%255c',      # Double URL encoded backslash
        '..../',        # Double dot variant
        '....\\',       # Double dot Windows variant
        '%2e%2e%2f',    # Fully URL encoded ../
        '%2e%2e%5c',    # Fully URL encoded ..\
        '\u002e\u002e\u002f',  # Unicode encoded ../
        '\uff0e\uff0e\uff0f',   # Full-width Unicode ../
    ]

    def detect_traversal(self, path: str) -> None:
        """
        Detect path traversal attempts in various encodings.

        Args:
            path: Path to check

        Raises:
            PathTraversalError: If traversal pattern is detected
        """
        # URL decode the path to catch encoded traversal attempts
        decoded_path = self._url_decode_safely(path)

        # Check for obvious traversal patterns
        path_lower = decoded_path.lower()
        for pattern in self.TRAVERSAL_PATTERNS:
            if pattern in path_lower:
                raise PathTraversalError(
                    f"Path traversal pattern detected: {pattern}",
                    path=path,
                    pattern=pattern
                )

        # Check normalized path for remaining traversal attempts
        self._check_normalized_traversal(decoded_path, path)

        # Check for excessive directory traversal depth
        self._check_traversal_depth(decoded_path, path)

    def _url_decode_safely(self, path: str) -> str:
        """Safely URL decode a path, handling multiple encoding layers."""
        decoded = path
        max_iterations = 5  # Prevent infinite loops

        for _ in range(max_iterations):
            try:
                new_decoded = urllib.parse.unquote(decoded)
                if new_decoded == decoded:
                    break  # No more decoding needed
                decoded = new_decoded
            except Exception:
                break  # Stop if decoding fails

        return decoded

    def _check_normalized_traversal(self, decoded_path: str, original_path: str) -> None:
        """Check for traversal after path normalization."""
        try:
            # Normalize the path to resolve dots
            normalized = os.path.normpath(decoded_path)
            components = normalized.split(os.sep)

            # Check for remaining '..' components
            for component in components:
                if component == '..':
                    raise PathTraversalError(
                        "Path traversal detected after normalization",
                        path=original_path,
                        pattern=".."
                    )

        except Exception:
            # If normalization fails, it might be malicious
            raise PathTraversalError(
                "Path normalization failed (possible attack)",
                path=original_path
            )

    def _check_traversal_depth(self, path: str, original_path: str) -> None:
        """Check for excessive traversal depth."""
        # Count '../' patterns
        traversal_count = path.count('../') + path.count('..\\')

        # Also check for encoded versions
        traversal_count += path.lower().count('%2e%2e%2f')
        traversal_count += path.lower().count('%2e%2e%5c')

        # Arbitrary limit to prevent DoS through deep traversal
        max_traversal_depth = 10

        if traversal_count > max_traversal_depth:
            raise PathTraversalError(
                f"Excessive path traversal depth: {traversal_count} levels",
                path=original_path,
                pattern=f"{traversal_count} traversals"
            )


class SymlinkValidator:
    """Validates symbolic link safety."""

    def __init__(self, policy: SecurityPolicy):
        self.policy = policy

    def validate_symlinks(self, path: str) -> None:
        """
        Validate symbolic links according to policy.

        Args:
            path: Path to validate

        Raises:
            PathSecurityError: If symlink validation fails
        """
        if not os.path.exists(path):
            return  # Can't validate non-existent paths

        if self.policy.symlink_policy == SymlinkPolicy.FORBID:
            self._forbid_symlinks(path)
        elif self.policy.symlink_policy == SymlinkPolicy.ALLOW_SAFE:
            self._validate_safe_symlinks(path)
        elif self.policy.symlink_policy == SymlinkPolicy.NO_FOLLOW:
            # Don't follow symlinks, but allow them to exist
            pass

    def _forbid_symlinks(self, path: str) -> None:
        """Forbid all symbolic links."""
        if os.path.islink(path):
            raise PathSecurityError(
                "Symbolic links are forbidden",
                path=path,
                threat_type="SYMLINK_FORBIDDEN"
            )

        # Check parent directories for symlinks
        parent = os.path.dirname(path)
        while parent and parent != os.path.dirname(parent):
            if os.path.islink(parent):
                raise PathSecurityError(
                    f"Symbolic link in path hierarchy: {parent}",
                    path=path,
                    threat_type="SYMLINK_IN_HIERARCHY"
                )
            parent = os.path.dirname(parent)

    def _validate_safe_symlinks(self, path: str) -> None:
        """Validate that symlinks are safe (no loops, within bounds)."""
        if not os.path.islink(path):
            return

        # Check for symlink loops
        if self._has_symlink_loop(path):
            raise PathSecurityError(
                "Symbolic link loop detected",
                path=path,
                threat_type="SYMLINK_LOOP"
            )

        # Check symlink depth
        depth = self._get_symlink_depth(path)
        if depth > self.policy.max_symlink_depth:
            raise PathSecurityError(
                f"Symbolic link depth {depth} exceeds maximum {self.policy.max_symlink_depth}",
                path=path,
                threat_type="SYMLINK_DEPTH_EXCEEDED"
            )

    def _has_symlink_loop(self, path: str) -> bool:
        """Check if path contains a symbolic link loop."""
        visited = set()
        current = path

        while os.path.islink(current):
            real_path = os.path.realpath(current)
            if real_path in visited:
                return True
            visited.add(real_path)

            try:
                target = os.readlink(current)
                if not os.path.isabs(target):
                    # Relative symlink - resolve relative to symlink location
                    current = os.path.join(os.path.dirname(current), target)
                else:
                    current = target
            except OSError:
                break

        return False

    def _get_symlink_depth(self, path: str) -> int:
        """Get the depth of symbolic link resolution."""
        depth = 0
        current = path
        max_depth = 50  # Prevent infinite loops

        while os.path.islink(current) and depth < max_depth:
            try:
                target = os.readlink(current)
                if not os.path.isabs(target):
                    current = os.path.join(os.path.dirname(current), target)
                else:
                    current = target
                depth += 1
            except OSError:
                break

        return depth


class SandboxValidator:
    """Validates paths against sandbox constraints."""

    def __init__(self, policy: SecurityPolicy):
        self.policy = policy

    def validate_sandbox_constraints(self, path: str) -> None:
        """
        Validate that path stays within sandbox boundaries.

        Args:
            path: Path to validate

        Raises:
            PathSecurityError: If path violates sandbox constraints
        """
        if not self.policy.sandbox_roots:
            return

        # Convert to absolute path for comparison
        try:
            abs_path = os.path.abspath(path)
        except Exception:
            raise PathSecurityError(
                "Cannot resolve absolute path for sandbox validation",
                path=path,
                threat_type="SANDBOX_RESOLUTION_FAILED"
            )

        # Check forbidden paths first
        if self.policy.forbidden_paths:
            for forbidden in self.policy.forbidden_paths:
                try:
                    abs_forbidden = os.path.abspath(forbidden)
                    if self._path_is_under(abs_path, abs_forbidden):
                        raise PathSecurityError(
                            f"Path is within forbidden directory: {forbidden}",
                            path=path,
                            threat_type="FORBIDDEN_PATH_ACCESS"
                        )
                except Exception:
                    continue

        # Check allowed roots
        allowed = False
        for root in self.policy.sandbox_roots:
            try:
                abs_root = os.path.abspath(root)
                if self._path_is_under(abs_path, abs_root):
                    allowed = True
                    break
            except Exception:
                continue

        if not allowed:
            raise PathSecurityError(
                "Path is outside allowed sandbox boundaries",
                path=path,
                threat_type="SANDBOX_VIOLATION"
            )

    def _path_is_under(self, path: str, parent: str) -> bool:
        """Check if path is under parent directory."""
        try:
            # Normalize both paths
            path = os.path.normpath(path)
            parent = os.path.normpath(parent)

            # Check if path starts with parent
            if path == parent:
                return True

            # Ensure parent ends with separator for proper prefix check
            if not parent.endswith(os.sep):
                parent += os.sep

            return path.startswith(parent)
        except Exception:
            return False


class PermissionValidator:
    """Validates file system permissions."""

    @staticmethod
    def validate_required_permissions(path: str, required_perms: List[str]) -> None:
        """
        Validate that user has required permissions for path.

        Args:
            path: Path to check
            required_perms: List of required permissions ('read', 'write', 'execute')

        Raises:
            PathPermissionError: If required permissions are not available
        """
        if not os.path.exists(path):
            # For non-existent paths, check parent directory permissions
            parent = os.path.dirname(path)
            if not parent or not os.path.exists(parent):
                raise PathPermissionError(
                    "Cannot verify permissions: path and parent do not exist",
                    path=path
                )

            # Check parent directory write permission for file creation
            if 'write' in required_perms and not os.access(parent, os.W_OK):
                raise PathPermissionError(
                    "Insufficient write permission to create file",
                    path=path,
                    required_permission='write'
                )
            return

        # Check existing path permissions
        perm_map = {
            'read': os.R_OK,
            'write': os.W_OK,
            'execute': os.X_OK
        }

        for perm in required_perms:
            if perm in perm_map and not os.access(path, perm_map[perm]):
                raise PathPermissionError(
                    f"Insufficient {perm} permission",
                    path=path,
                    required_permission=perm
                )