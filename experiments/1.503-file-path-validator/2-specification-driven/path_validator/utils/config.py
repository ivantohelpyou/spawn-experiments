"""
Configuration management for path validation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
import json
import os


class SymlinkPolicy(Enum):
    """Policy for handling symbolic links during validation."""
    FORBID = "forbid"           # Reject all symlinks
    ALLOW_SAFE = "allow_safe"   # Allow only safe symlinks
    FOLLOW = "follow"           # Follow all symlinks (less secure)
    NO_FOLLOW = "no_follow"     # Don't follow, treat as regular files


@dataclass
class SecurityPolicy:
    """Security policy configuration for path validation."""

    # Path traversal prevention
    prevent_traversal: bool = True
    max_traversal_depth: int = 0  # 0 = no traversal allowed

    # Symlink handling
    symlink_policy: SymlinkPolicy = SymlinkPolicy.ALLOW_SAFE
    max_symlink_depth: int = 5

    # Input sanitization
    sanitize_input: bool = True
    max_path_length: int = 4096
    max_component_length: int = 255

    # Access control
    sandbox_roots: Optional[List[str]] = None
    forbidden_paths: Optional[List[str]] = None

    # Rate limiting
    enable_rate_limiting: bool = False
    max_validations_per_minute: int = 100

    # Logging and monitoring
    log_security_events: bool = True
    alert_on_suspicious_activity: bool = True


@dataclass
class ValidationConfig:
    """Main configuration for path validation behavior."""

    # Validation mode
    strict_mode: bool = True
    target_platform: Optional[str] = None

    # Length limits
    max_path_length: int = 4096
    max_component_length: int = 255

    # Path handling
    allow_traversal: bool = False
    follow_symlinks: bool = True
    case_sensitive: Optional[bool] = None

    # Extension validation
    allowed_extensions: Optional[List[str]] = None
    forbidden_extensions: Optional[List[str]] = None

    # Security policy
    security_policy: Optional[SecurityPolicy] = None

    # Performance settings
    enable_caching: bool = True
    cache_size: int = 1000
    cache_ttl_seconds: int = 3600

    # Validation options
    check_existence: bool = False
    require_absolute: bool = False
    normalize_unicode: bool = True

    def __post_init__(self):
        """Initialize default security policy if not provided."""
        if self.security_policy is None:
            self.security_policy = SecurityPolicy()


class ConfigurationManager:
    """Manages validator configuration from various sources."""

    def __init__(self):
        self._config_cache: Dict[str, tuple] = {}

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
        content = config_path.read_text(encoding='utf-8')
        if config_path.suffix.lower() == '.json':
            config_dict = json.loads(content)
        else:
            raise ValueError(f"Unsupported config format: {config_path.suffix}")

        config = self._dict_to_config(config_dict)

        # Cache the result
        self._config_cache[cache_key] = (config, config_path.stat().st_mtime)

        return config

    def _dict_to_config(self, config_dict: Dict[str, Any]) -> ValidationConfig:
        """Convert dictionary to ValidationConfig object."""
        config_dict = config_dict.copy()

        # Handle nested security policy
        security_policy = None
        if 'security_policy' in config_dict:
            security_dict = config_dict.pop('security_policy')

            # Convert symlink_policy string to enum
            if 'symlink_policy' in security_dict:
                symlink_policy_str = security_dict['symlink_policy']
                security_dict['symlink_policy'] = SymlinkPolicy(symlink_policy_str)

            security_policy = SecurityPolicy(**security_dict)

        # Create main config
        config = ValidationConfig(**config_dict)
        config.security_policy = security_policy

        return config

    def save_config(self, config: ValidationConfig, config_path: Path) -> None:
        """Save configuration to file."""
        config_dict = self._config_to_dict(config)

        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)

        # Update cache
        cache_key = str(config_path.absolute())
        self._config_cache[cache_key] = (config, config_path.stat().st_mtime)

    def _config_to_dict(self, config: ValidationConfig) -> Dict[str, Any]:
        """Convert ValidationConfig to dictionary."""
        config_dict = {
            'strict_mode': config.strict_mode,
            'target_platform': config.target_platform,
            'max_path_length': config.max_path_length,
            'max_component_length': config.max_component_length,
            'allow_traversal': config.allow_traversal,
            'follow_symlinks': config.follow_symlinks,
            'case_sensitive': config.case_sensitive,
            'allowed_extensions': config.allowed_extensions,
            'forbidden_extensions': config.forbidden_extensions,
            'enable_caching': config.enable_caching,
            'cache_size': config.cache_size,
            'cache_ttl_seconds': config.cache_ttl_seconds,
            'check_existence': config.check_existence,
            'require_absolute': config.require_absolute,
            'normalize_unicode': config.normalize_unicode,
        }

        # Handle security policy
        if config.security_policy:
            security_dict = {
                'prevent_traversal': config.security_policy.prevent_traversal,
                'max_traversal_depth': config.security_policy.max_traversal_depth,
                'symlink_policy': config.security_policy.symlink_policy.value,
                'max_symlink_depth': config.security_policy.max_symlink_depth,
                'sanitize_input': config.security_policy.sanitize_input,
                'max_path_length': config.security_policy.max_path_length,
                'max_component_length': config.security_policy.max_component_length,
                'sandbox_roots': config.security_policy.sandbox_roots,
                'forbidden_paths': config.security_policy.forbidden_paths,
                'enable_rate_limiting': config.security_policy.enable_rate_limiting,
                'max_validations_per_minute': config.security_policy.max_validations_per_minute,
                'log_security_events': config.security_policy.log_security_events,
                'alert_on_suspicious_activity': config.security_policy.alert_on_suspicious_activity,
            }
            config_dict['security_policy'] = security_dict

        return config_dict

    @classmethod
    def from_environment(cls) -> ValidationConfig:
        """Create configuration from environment variables."""
        config_dict = {}

        # Map environment variables to config fields
        env_mapping = {
            'PATH_VALIDATOR_STRICT_MODE': ('strict_mode', bool),
            'PATH_VALIDATOR_TARGET_PLATFORM': ('target_platform', str),
            'PATH_VALIDATOR_MAX_PATH_LENGTH': ('max_path_length', int),
            'PATH_VALIDATOR_MAX_COMPONENT_LENGTH': ('max_component_length', int),
            'PATH_VALIDATOR_ALLOW_TRAVERSAL': ('allow_traversal', bool),
            'PATH_VALIDATOR_FOLLOW_SYMLINKS': ('follow_symlinks', bool),
            'PATH_VALIDATOR_CASE_SENSITIVE': ('case_sensitive', bool),
            'PATH_VALIDATOR_CHECK_EXISTENCE': ('check_existence', bool),
            'PATH_VALIDATOR_REQUIRE_ABSOLUTE': ('require_absolute', bool),
            'PATH_VALIDATOR_NORMALIZE_UNICODE': ('normalize_unicode', bool),
        }

        for env_var, (config_key, value_type) in env_mapping.items():
            env_value = os.environ.get(env_var)
            if env_value is not None:
                if value_type == bool:
                    config_dict[config_key] = env_value.lower() in ('true', '1', 'yes', 'on')
                elif value_type == int:
                    config_dict[config_key] = int(env_value)
                else:
                    config_dict[config_key] = env_value

        manager = cls()
        return manager._dict_to_config(config_dict)