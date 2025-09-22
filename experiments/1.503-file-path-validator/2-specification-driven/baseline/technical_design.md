# Technical Design Documentation

## Architecture Overview

### High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client API    │ -> │  Core Validator  │ -> │ Platform Layer  │
│                 │    │                  │    │                 │
│ - PathValidator │    │ - ValidationCore │    │ - WindowsOps    │
│ - BatchValidator│    │ - SecurityCore   │    │ - PosixOps      │
│ - AsyncValidator│    │ - NormalizerCore │    │ - FilesystemOps │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌────────────────┐
                       │ Support Layer  │
                       │                │
                       │ - ErrorHandler │
                       │ - ConfigMgr    │
                       │ - PerformMon   │
                       │ - CacheManager │
                       └────────────────┘
```

### Module Structure
```
path_validator/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── validator.py       # Main validation logic
│   ├── security.py        # Security validation
│   ├── normalizer.py      # Path normalization
│   └── rules.py           # Validation rules
├── platform/
│   ├── __init__.py
│   ├── base.py           # Abstract platform interface
│   ├── windows.py        # Windows-specific operations
│   ├── posix.py          # POSIX-specific operations
│   └── detection.py      # Platform detection
├── exceptions/
│   ├── __init__.py
│   └── errors.py         # Exception hierarchy
├── utils/
│   ├── __init__.py
│   ├── cache.py          # Caching utilities
│   ├── performance.py    # Performance monitoring
│   └── config.py         # Configuration management
├── validators/
│   ├── __init__.py
│   ├── sync.py           # Synchronous validators
│   ├── batch.py          # Batch processing
│   └── async_validator.py # Asynchronous validators
└── tests/
    ├── __init__.py
    ├── test_core/
    ├── test_platform/
    ├── test_security/
    └── test_performance/
```

## Core Components Design

### 1. ValidationCore Class
```python
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import os.path

@dataclass
class ValidationConfig:
    """Configuration for path validation behavior."""
    strict_mode: bool = True
    target_platform: Optional[str] = None
    max_path_length: int = 4096
    max_component_length: int = 255
    allow_traversal: bool = False
    follow_symlinks: bool = True
    case_sensitive: Optional[bool] = None
    security_policy: Optional['SecurityPolicy'] = None

class ValidationCore:
    """Core path validation engine."""

    def __init__(self, config: ValidationConfig = None):
        self.config = config or ValidationConfig()
        self.platform_ops = self._init_platform_operations()
        self.security_validator = SecurityValidator(self.config.security_policy)
        self.normalizer = PathNormalizer(self.config)

    def validate(self, path: str) -> ValidationResult:
        """Main validation entry point."""
        try:
            # Input sanitization
            sanitized_path = self._sanitize_input(path)

            # Basic syntax validation
            self._validate_syntax(sanitized_path)

            # Security validation
            self.security_validator.validate(sanitized_path)

            # Platform-specific validation
            self.platform_ops.validate_platform_constraints(sanitized_path)

            # Normalization
            normalized_path = self.normalizer.normalize(sanitized_path)

            # Existence checks (if configured)
            existence_info = self._check_existence(normalized_path)

            return ValidationResult(
                valid=True,
                original_path=path,
                normalized_path=normalized_path,
                existence_info=existence_info
            )

        except PathValidationError as e:
            return ValidationResult(
                valid=False,
                original_path=path,
                error=e
            )
```

### 2. Platform Abstraction Layer
```python
from abc import ABC, abstractmethod

class PlatformOperations(ABC):
    """Abstract base class for platform-specific operations."""

    @abstractmethod
    def validate_platform_constraints(self, path: str) -> None:
        """Validate platform-specific path constraints."""
        pass

    @abstractmethod
    def normalize_separators(self, path: str) -> str:
        """Normalize path separators for the platform."""
        pass

    @abstractmethod
    def get_max_path_length(self) -> int:
        """Get maximum path length for the platform."""
        pass

    @abstractmethod
    def get_forbidden_characters(self) -> set:
        """Get set of forbidden characters for the platform."""
        pass

    @abstractmethod
    def is_reserved_name(self, name: str) -> bool:
        """Check if name is reserved on the platform."""
        pass

class WindowsOperations(PlatformOperations):
    """Windows-specific path operations."""

    FORBIDDEN_CHARS = set('<>:"|?*\x00')
    RESERVED_NAMES = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }

    def validate_platform_constraints(self, path: str) -> None:
        # Check forbidden characters
        if any(char in self.FORBIDDEN_CHARS for char in path):
            raise PathPlatformError("Path contains forbidden characters")

        # Check reserved names
        components = path.replace('\\', '/').split('/')
        for component in components:
            base_name = component.split('.')[0].upper()
            if base_name in self.RESERVED_NAMES:
                raise PathPlatformError(f"Reserved name not allowed: {component}")

        # Check length limits
        if len(path) > 260 and not path.startswith('\\\\?\\'):
            raise PathLengthError("Path exceeds Windows length limit")

class PosixOperations(PlatformOperations):
    """POSIX-specific path operations."""

    FORBIDDEN_CHARS = set('\x00')  # Only null byte forbidden

    def validate_platform_constraints(self, path: str) -> None:
        # Check forbidden characters (only null byte)
        if '\x00' in path:
            raise PathPlatformError("Path contains null byte")

        # Check component length limits
        components = path.split('/')
        for component in components:
            if len(component.encode('utf-8')) > 255:
                raise PathLengthError("Component name too long")
```

### 3. Security Validation System
```python
class SecurityValidator:
    """Handles all security-related path validation."""

    def __init__(self, policy: SecurityPolicy = None):
        self.policy = policy or SecurityPolicy()
        self.traversal_detector = TraversalDetector()
        self.symlink_validator = SymlinkValidator()

    def validate(self, path: str) -> None:
        """Perform comprehensive security validation."""
        # Path traversal detection
        if self.policy.prevent_traversal:
            self.traversal_detector.detect_traversal(path)

        # Symlink validation
        if self.policy.symlink_policy != SymlinkPolicy.FOLLOW:
            self.symlink_validator.validate_symlinks(path)

        # Sandbox validation
        if self.policy.sandbox_roots:
            self._validate_sandbox_constraints(path)

        # Input sanitization
        self._validate_input_safety(path)

    def _validate_sandbox_constraints(self, path: str) -> None:
        """Ensure path stays within allowed sandbox boundaries."""
        abs_path = os.path.abspath(path)

        for root in self.policy.sandbox_roots:
            if abs_path.startswith(os.path.abspath(root)):
                return

        raise PathSecurityError("Path outside allowed sandbox")

class TraversalDetector:
    """Detects various forms of path traversal attacks."""

    TRAVERSAL_PATTERNS = [
        '../', '..\\', '..%2f', '..%5c', '..%252f',
        '..../', '....\\', '%2e%2e%2f', '%2e%2e%5c'
    ]

    def detect_traversal(self, path: str) -> None:
        """Detect path traversal attempts."""
        # URL decode path first
        decoded = self._url_decode(path)

        # Check for obvious patterns
        for pattern in self.TRAVERSAL_PATTERNS:
            if pattern in decoded.lower():
                raise PathTraversalError(f"Traversal pattern detected: {pattern}")

        # Check normalized path
        normalized = os.path.normpath(decoded)
        if '..' in normalized.split(os.sep):
            raise PathTraversalError("Path traversal after normalization")
```

### 4. Configuration Management
```python
from typing import Union, Dict
import json
import yaml
from pathlib import Path

class ConfigurationManager:
    """Manages validator configuration from various sources."""

    def __init__(self):
        self._config_cache = {}
        self._config_watchers = {}

    def load_config(self, source: Union[str, Dict, Path]) -> ValidationConfig:
        """Load configuration from file, dict, or Path object."""
        if isinstance(source, dict):
            return self._dict_to_config(source)

        elif isinstance(source, (str, Path)):
            return self._load_from_file(Path(source))

        else:
            raise ValueError(f"Unsupported config source type: {type(source)}")

    def _load_from_file(self, config_path: Path) -> ValidationConfig:
        """Load configuration from file."""
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        # Check cache first
        cache_key = str(config_path.absolute())
        if cache_key in self._config_cache:
            cached_config, mtime = self._config_cache[cache_key]
            if config_path.stat().st_mtime <= mtime:
                return cached_config

        # Load and parse config
        content = config_path.read_text()
        if config_path.suffix.lower() == '.json':
            config_dict = json.loads(content)
        elif config_path.suffix.lower() in ('.yml', '.yaml'):
            config_dict = yaml.safe_load(content)
        else:
            raise ValueError(f"Unsupported config format: {config_path.suffix}")

        config = self._dict_to_config(config_dict)

        # Cache the result
        self._config_cache[cache_key] = (config, config_path.stat().st_mtime)

        return config

    def _dict_to_config(self, config_dict: Dict) -> ValidationConfig:
        """Convert dictionary to ValidationConfig object."""
        # Handle nested security policy
        security_policy = None
        if 'security_policy' in config_dict:
            security_policy = SecurityPolicy(**config_dict.pop('security_policy'))

        config = ValidationConfig(**config_dict)
        config.security_policy = security_policy

        return config
```

## Integration Points

### 1. os.path Integration
```python
class OsPathIntegration:
    """Integration layer with os.path module."""

    @staticmethod
    def validate_and_normalize(path: str) -> str:
        """Validate path and return normalized version using os.path."""
        validator = PathValidator()
        result = validator.validate(path)

        if not result.valid:
            raise result.error

        return os.path.normpath(result.normalized_path)

    @staticmethod
    def safe_join(*paths: str) -> str:
        """Safely join paths with validation."""
        joined = os.path.join(*paths)
        validator = PathValidator()
        result = validator.validate(joined)

        if not result.valid:
            raise result.error

        return result.normalized_path
```

### 2. pathlib Integration
```python
from pathlib import Path, PurePath

class PathlibIntegration:
    """Integration layer with pathlib module."""

    class ValidatedPath(Path):
        """Path subclass with built-in validation."""

        def __new__(cls, *args, **kwargs):
            validator = kwargs.pop('validator', None) or PathValidator()

            # Create path normally
            path_str = str(Path(*args))

            # Validate the path
            result = validator.validate(path_str)
            if not result.valid:
                raise result.error

            # Create instance with normalized path
            return super().__new__(cls, result.normalized_path)

        def joinpath(self, *args):
            """Override joinpath to include validation."""
            joined = super().joinpath(*args)
            validator = PathValidator()
            result = validator.validate(str(joined))

            if not result.valid:
                raise result.error

            return ValidatedPath(result.normalized_path)
```

### 3. API Design
```python
class PathValidator:
    """Main public API for path validation."""

    def __init__(self, config: ValidationConfig = None):
        self.core = ValidationCore(config)

    def validate(self, path: Union[str, Path]) -> ValidationResult:
        """Validate a single path."""
        return self.core.validate(str(path))

    def is_valid(self, path: Union[str, Path]) -> bool:
        """Quick boolean validation check."""
        return self.validate(path).valid

    def normalize(self, path: Union[str, Path]) -> str:
        """Normalize path with validation."""
        result = self.validate(path)
        if not result.valid:
            raise result.error
        return result.normalized_path

    def check_existence(self, path: Union[str, Path]) -> ExistenceInfo:
        """Check path existence with validation."""
        result = self.validate(path)
        if not result.valid:
            raise result.error

        return result.existence_info

    # Context manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# Convenience functions
def validate_path(path: Union[str, Path], config: ValidationConfig = None) -> ValidationResult:
    """Standalone function for single path validation."""
    validator = PathValidator(config)
    return validator.validate(path)

def is_valid_path(path: Union[str, Path], config: ValidationConfig = None) -> bool:
    """Standalone function for boolean path validation."""
    return validate_path(path, config).valid

# Decorator support
def validate_path_args(*path_arg_names):
    """Decorator to validate path arguments to functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            validator = PathValidator()

            # Validate positional path arguments
            for i, arg_name in enumerate(path_arg_names):
                if i < len(args):
                    result = validator.validate(args[i])
                    if not result.valid:
                        raise result.error

            # Validate keyword path arguments
            for arg_name in path_arg_names:
                if arg_name in kwargs:
                    result = validator.validate(kwargs[arg_name])
                    if not result.valid:
                        raise result.error

            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## Data Flow Design

### Validation Pipeline
```
Input Path
    │
    ▼
┌─────────────┐
│ Input       │ -> Sanitize, basic checks
│ Sanitization│
└─────────────┘
    │
    ▼
┌─────────────┐
│ Syntax      │ -> Format, characters, structure
│ Validation  │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Security    │ -> Traversal, injection, sandbox
│ Validation  │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Platform    │ -> OS-specific constraints
│ Validation  │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Path        │ -> Normalize separators, resolve
│ Normalization│
└─────────────┘
    │
    ▼
┌─────────────┐
│ Existence   │ -> Check filesystem (optional)
│ Validation  │
└─────────────┘
    │
    ▼
ValidationResult
```

### Error Propagation Flow
```
ValidationError
    │
    ▼
┌─────────────┐
│ Error       │ -> Classify, enrich context
│ Classification│
└─────────────┘
    │
    ▼
┌─────────────┐
│ Error       │ -> Add suggestions, format
│ Enhancement │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Logging &   │ -> Log, monitor, alert
│ Monitoring  │
└─────────────┘
    │
    ▼
Enhanced ValidationResult
```

This technical design provides a solid foundation for implementing the comprehensive file path validator with all the specified requirements while maintaining clean separation of concerns and extensibility.