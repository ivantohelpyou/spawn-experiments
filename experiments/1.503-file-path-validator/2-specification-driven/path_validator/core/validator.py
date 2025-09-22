"""
Core validation engine for file paths.
"""

import os
import os.path
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from ..exceptions.errors import PathValidationError, PathSyntaxError
from ..platform.detection import get_platform_specific_validator
from ..utils.config import ValidationConfig
from .normalizer import PathNormalizer
from .security import SecurityValidator


@dataclass
class ExistenceInfo:
    """Information about path existence and properties."""
    exists: bool = False
    is_file: bool = False
    is_directory: bool = False
    is_symlink: bool = False
    is_readable: bool = False
    is_writable: bool = False
    is_executable: bool = False
    size: Optional[int] = None
    modified_time: Optional[datetime] = None
    created_time: Optional[datetime] = None


@dataclass
class ValidationResult:
    """Result of path validation operation."""
    valid: bool
    original_path: str
    normalized_path: Optional[str] = None
    error: Optional[PathValidationError] = None
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    existence_info: Optional[ExistenceInfo] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    validation_time: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for serialization."""
        result = {
            "valid": self.valid,
            "original_path": self.original_path,
            "normalized_path": self.normalized_path,
        }

        if self.error:
            result["error"] = {
                "code": self.error.error_code,
                "message": str(self.error),
                "type": self.error.__class__.__name__,
            }

        if self.warnings:
            result["warnings"] = self.warnings

        if self.suggestions:
            result["suggestions"] = self.suggestions

        if self.existence_info:
            result["existence_info"] = {
                "exists": self.existence_info.exists,
                "is_file": self.existence_info.is_file,
                "is_directory": self.existence_info.is_directory,
                "is_symlink": self.existence_info.is_symlink,
                "is_readable": self.existence_info.is_readable,
                "is_writable": self.existence_info.is_writable,
                "is_executable": self.existence_info.is_executable,
                "size": self.existence_info.size,
            }

        if self.metadata:
            result["metadata"] = self.metadata

        if self.validation_time is not None:
            result["validation_time_ms"] = self.validation_time * 1000

        return result


class ValidationCore:
    """Core path validation engine."""

    def __init__(self, config: Optional[ValidationConfig] = None):
        self.config = config or ValidationConfig()
        self.platform_ops = self._init_platform_operations()
        self.security_validator = SecurityValidator(self.config.security_policy)
        self.normalizer = PathNormalizer(self.config)

    def _init_platform_operations(self):
        """Initialize platform-specific operations."""
        if self.config.target_platform:
            # Use specific platform operations
            if self.config.target_platform.lower() == 'windows':
                from ..platform.windows import WindowsOperations
                return WindowsOperations()
            elif self.config.target_platform.lower() in ('posix', 'linux', 'macos'):
                from ..platform.posix import PosixOperations
                return PosixOperations()
            else:
                raise ValueError(f"Unsupported target platform: {self.config.target_platform}")
        else:
            # Auto-detect current platform
            platform_class = get_platform_specific_validator()
            return platform_class()

    def validate(self, path: str) -> ValidationResult:
        """Main validation entry point."""
        import time
        start_time = time.perf_counter()

        try:
            # Input sanitization
            sanitized_path = self._sanitize_input(path)

            # Basic syntax validation
            self._validate_syntax(sanitized_path)

            # Security validation
            self.security_validator.validate(sanitized_path)

            # Platform-specific validation
            self.platform_ops.validate_platform_constraints(sanitized_path)

            # Extension validation
            self._validate_extensions(sanitized_path)

            # Normalization
            normalized_path = self.normalizer.normalize(sanitized_path)

            # Existence checks (if configured)
            existence_info = None
            if self.config.check_existence:
                existence_info = self._check_existence(normalized_path)

            # Additional validation based on config
            self._validate_config_constraints(normalized_path)

            validation_time = time.perf_counter() - start_time

            return ValidationResult(
                valid=True,
                original_path=path,
                normalized_path=normalized_path,
                existence_info=existence_info,
                validation_time=validation_time
            )

        except PathValidationError as e:
            validation_time = time.perf_counter() - start_time

            # Generate suggestions for fixing the error
            suggestions = self._generate_error_suggestions(e, path)

            return ValidationResult(
                valid=False,
                original_path=path,
                error=e,
                suggestions=suggestions,
                validation_time=validation_time
            )

    def _sanitize_input(self, path: str) -> str:
        """Sanitize and validate input path."""
        if not isinstance(path, str):
            raise PathSyntaxError(f"Path must be a string, got {type(path).__name__}")

        if not path:
            raise PathSyntaxError("Path cannot be empty")

        # Remove null bytes
        if '\x00' in path:
            raise PathSyntaxError("Path contains null bytes")

        # Basic length check
        if len(path) > self.config.max_path_length:
            from ..exceptions.errors import PathLengthError
            raise PathLengthError(
                f"Path length {len(path)} exceeds maximum {self.config.max_path_length}",
                path=path,
                actual_length=len(path),
                max_length=self.config.max_path_length
            )

        return path.strip()

    def _validate_syntax(self, path: str) -> None:
        """Validate basic path syntax."""
        # Check for obviously invalid patterns
        if '..' in path and not self.config.allow_traversal:
            from ..exceptions.errors import PathTraversalError
            raise PathTraversalError("Path traversal detected", path=path)

        # Check for repeated separators (might indicate issues)
        if '//' in path or '\\\\' in path.replace('\\\\?\\', ''):  # Exclude UNC prefix
            # This is often valid, so just warn
            pass

    def _validate_extensions(self, path: str) -> None:
        """Validate file extensions if configured."""
        if not (self.config.allowed_extensions or self.config.forbidden_extensions):
            return

        # Extract extension
        path_obj = Path(path)
        extension = path_obj.suffix.lower()

        if self.config.forbidden_extensions and extension in self.config.forbidden_extensions:
            raise PathSyntaxError(
                f"Forbidden file extension: {extension}",
                path=path
            )

        if self.config.allowed_extensions and extension not in self.config.allowed_extensions:
            raise PathSyntaxError(
                f"File extension not in allowed list: {extension}",
                path=path
            )

    def _validate_config_constraints(self, path: str) -> None:
        """Validate additional constraints from configuration."""
        if self.config.require_absolute and not self.platform_ops.is_absolute(path):
            raise PathSyntaxError(
                "Absolute path required",
                path=path
            )

    def _check_existence(self, path: str) -> ExistenceInfo:
        """Check path existence and gather information."""
        existence_info = ExistenceInfo()

        try:
            stat_info = os.stat(path)
            existence_info.exists = True
            existence_info.is_file = os.path.isfile(path)
            existence_info.is_directory = os.path.isdir(path)
            existence_info.is_symlink = os.path.islink(path)
            existence_info.size = stat_info.st_size
            existence_info.modified_time = datetime.fromtimestamp(stat_info.st_mtime)
            existence_info.created_time = datetime.fromtimestamp(stat_info.st_ctime)

            # Check permissions
            existence_info.is_readable = os.access(path, os.R_OK)
            existence_info.is_writable = os.access(path, os.W_OK)
            existence_info.is_executable = os.access(path, os.X_OK)

        except (OSError, FileNotFoundError):
            # Path doesn't exist or can't be accessed
            existence_info.exists = False

        return existence_info

    def _generate_error_suggestions(self, error: PathValidationError, path: str) -> List[str]:
        """Generate helpful suggestions for fixing validation errors."""
        suggestions = []

        if isinstance(error, PathSyntaxError):
            if "forbidden characters" in str(error).lower():
                suggestions.append("Remove or replace forbidden characters in the path")
                suggestions.append("Use only alphanumeric characters, hyphens, and underscores")

            if "empty" in str(error).lower():
                suggestions.append("Provide a non-empty path")

        elif hasattr(error, '__class__') and 'Traversal' in error.__class__.__name__:
            suggestions.extend([
                "Remove '../' sequences from the path",
                "Use absolute paths instead of relative paths",
                "Validate path against allowed directories"
            ])

        elif hasattr(error, '__class__') and 'Length' in error.__class__.__name__:
            if hasattr(error, 'max_length'):
                suggestions.append(f"Reduce path length to under {error.max_length} characters")
            suggestions.extend([
                "Use shorter directory or file names",
                "Consider using symbolic links to reduce path depth"
            ])

        elif hasattr(error, '__class__') and 'Platform' in error.__class__.__name__:
            if "reserved name" in str(error).lower():
                suggestions.append("Choose a different filename (avoid CON, PRN, AUX, etc.)")

        return suggestions

    def validate_batch(self, paths: List[str]) -> List[ValidationResult]:
        """Validate multiple paths efficiently."""
        results = []
        for path in paths:
            results.append(self.validate(path))
        return results

    def is_valid(self, path: str) -> bool:
        """Quick boolean validation check."""
        return self.validate(path).valid

    def normalize_path(self, path: str) -> str:
        """Normalize path with validation."""
        result = self.validate(path)
        if not result.valid:
            raise result.error
        return result.normalized_path