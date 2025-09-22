"""
Synchronous path validation interface.
"""

from typing import Union, Optional, List
from pathlib import Path

from ..core.validator import ValidationCore, ValidationResult
from ..utils.config import ValidationConfig
from ..exceptions.errors import PathValidationError


class PathValidator:
    """Main synchronous path validator interface."""

    def __init__(self, config: Optional[ValidationConfig] = None):
        """
        Initialize path validator.

        Args:
            config: Validation configuration. If None, uses default config.
        """
        self.core = ValidationCore(config)
        self.config = config or ValidationConfig()

    def validate(self, path: Union[str, Path]) -> ValidationResult:
        """
        Validate a single path.

        Args:
            path: Path to validate (string or Path object)

        Returns:
            ValidationResult: Detailed validation result
        """
        return self.core.validate(str(path))

    def is_valid(self, path: Union[str, Path]) -> bool:
        """
        Quick boolean validation check.

        Args:
            path: Path to validate

        Returns:
            bool: True if path is valid, False otherwise
        """
        return self.validate(path).valid

    def normalize(self, path: Union[str, Path]) -> str:
        """
        Normalize path with validation.

        Args:
            path: Path to normalize

        Returns:
            str: Normalized path

        Raises:
            PathValidationError: If path is invalid
        """
        result = self.validate(path)
        if not result.valid:
            raise result.error
        return result.normalized_path

    def check_existence(self, path: Union[str, Path]):
        """
        Check path existence with validation.

        Args:
            path: Path to check

        Returns:
            ExistenceInfo: Information about path existence and properties

        Raises:
            PathValidationError: If path is invalid
        """
        # Temporarily enable existence checking
        original_check = self.config.check_existence
        self.config.check_existence = True

        try:
            result = self.validate(path)
            if not result.valid:
                raise result.error
            return result.existence_info
        finally:
            self.config.check_existence = original_check

    def validate_batch(self, paths: List[Union[str, Path]]) -> List[ValidationResult]:
        """
        Validate multiple paths.

        Args:
            paths: List of paths to validate

        Returns:
            List[ValidationResult]: Results for each path
        """
        return [self.validate(path) for path in paths]

    def get_valid_paths(self, paths: List[Union[str, Path]]) -> List[str]:
        """
        Filter list to only valid paths.

        Args:
            paths: List of paths to filter

        Returns:
            List[str]: Only the valid paths (normalized)
        """
        valid_paths = []
        for path in paths:
            result = self.validate(path)
            if result.valid:
                valid_paths.append(result.normalized_path)
        return valid_paths

    def get_invalid_paths(self, paths: List[Union[str, Path]]) -> List[tuple]:
        """
        Get list of invalid paths with their errors.

        Args:
            paths: List of paths to check

        Returns:
            List[tuple]: List of (path, error) tuples for invalid paths
        """
        invalid_paths = []
        for path in paths:
            result = self.validate(path)
            if not result.valid:
                invalid_paths.append((str(path), result.error))
        return invalid_paths

    def validate_and_suggest(self, path: Union[str, Path]) -> dict:
        """
        Validate path and provide suggestions if invalid.

        Args:
            path: Path to validate

        Returns:
            dict: Validation result with suggestions
        """
        result = self.validate(path)
        return {
            'valid': result.valid,
            'path': str(path),
            'normalized_path': result.normalized_path,
            'error': str(result.error) if result.error else None,
            'error_code': result.error.error_code if result.error else None,
            'suggestions': result.suggestions,
            'warnings': result.warnings
        }

    # Context manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# Convenience functions for standalone use
def validate_path(path: Union[str, Path], config: Optional[ValidationConfig] = None) -> ValidationResult:
    """
    Standalone function for single path validation.

    Args:
        path: Path to validate
        config: Validation configuration

    Returns:
        ValidationResult: Detailed validation result
    """
    validator = PathValidator(config)
    return validator.validate(path)


def is_valid_path(path: Union[str, Path], config: Optional[ValidationConfig] = None) -> bool:
    """
    Standalone function for boolean path validation.

    Args:
        path: Path to validate
        config: Validation configuration

    Returns:
        bool: True if path is valid
    """
    return validate_path(path, config).valid


def normalize_path(path: Union[str, Path], config: Optional[ValidationConfig] = None) -> str:
    """
    Standalone function for path normalization with validation.

    Args:
        path: Path to normalize
        config: Validation configuration

    Returns:
        str: Normalized path

    Raises:
        PathValidationError: If path is invalid
    """
    result = validate_path(path, config)
    if not result.valid:
        raise result.error
    return result.normalized_path


# Decorator for validating function arguments
def validate_path_args(*path_arg_names):
    """
    Decorator to validate path arguments to functions.

    Args:
        *path_arg_names: Names of arguments that should be validated as paths

    Example:
        @validate_path_args('input_file', 'output_dir')
        def process_file(input_file, output_dir, options=None):
            # input_file and output_dir will be validated before function execution
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            validator = PathValidator()

            # Get function argument names
            import inspect
            sig = inspect.signature(func)
            param_names = list(sig.parameters.keys())

            # Validate positional arguments
            for i, arg_name in enumerate(path_arg_names):
                if i < len(args) and i < len(param_names) and param_names[i] == arg_name:
                    result = validator.validate(args[i])
                    if not result.valid:
                        raise result.error

            # Validate keyword arguments
            for arg_name in path_arg_names:
                if arg_name in kwargs:
                    result = validator.validate(kwargs[arg_name])
                    if not result.valid:
                        raise result.error

            return func(*args, **kwargs)
        return wrapper
    return decorator


class ValidatedPath(Path):
    """
    Path subclass with built-in validation.

    This class extends pathlib.Path to automatically validate paths on creation
    and provide validation-aware path operations.
    """

    def __new__(cls, *args, validator: Optional[PathValidator] = None, **kwargs):
        """
        Create a new ValidatedPath instance.

        Args:
            *args: Path components
            validator: Custom validator to use
            **kwargs: Additional arguments
        """
        # Create the path string
        if len(args) == 1 and isinstance(args[0], Path):
            path_str = str(args[0])
        else:
            path_str = str(Path(*args))

        # Validate the path
        if validator is None:
            validator = PathValidator()

        result = validator.validate(path_str)
        if not result.valid:
            raise result.error

        # Create the instance with the normalized path
        return super().__new__(cls, result.normalized_path)

    def __init__(self, *args, validator: Optional[PathValidator] = None, **kwargs):
        """Initialize the ValidatedPath."""
        self._validator = validator or PathValidator()

    def joinpath(self, *args) -> 'ValidatedPath':
        """
        Join path components with validation.

        Args:
            *args: Path components to join

        Returns:
            ValidatedPath: New validated path instance

        Raises:
            PathValidationError: If resulting path is invalid
        """
        # Use parent's joinpath to get the new path
        new_path = super().joinpath(*args)

        # Validate the result
        result = self._validator.validate(str(new_path))
        if not result.valid:
            raise result.error

        return ValidatedPath(result.normalized_path, validator=self._validator)

    def with_name(self, name: str) -> 'ValidatedPath':
        """
        Return a new path with the name changed.

        Args:
            name: New filename

        Returns:
            ValidatedPath: New validated path instance

        Raises:
            PathValidationError: If resulting path is invalid
        """
        new_path = super().with_name(name)
        result = self._validator.validate(str(new_path))
        if not result.valid:
            raise result.error

        return ValidatedPath(result.normalized_path, validator=self._validator)

    def with_suffix(self, suffix: str) -> 'ValidatedPath':
        """
        Return a new path with the suffix changed.

        Args:
            suffix: New file suffix

        Returns:
            ValidatedPath: New validated path instance

        Raises:
            PathValidationError: If resulting path is invalid
        """
        new_path = super().with_suffix(suffix)
        result = self._validator.validate(str(new_path))
        if not result.valid:
            raise result.error

        return ValidatedPath(result.normalized_path, validator=self._validator)

    def validate(self) -> ValidationResult:
        """
        Validate the current path.

        Returns:
            ValidationResult: Detailed validation result
        """
        return self._validator.validate(str(self))

    def is_valid(self) -> bool:
        """
        Check if the current path is valid.

        Returns:
            bool: True if path is valid
        """
        return self.validate().valid