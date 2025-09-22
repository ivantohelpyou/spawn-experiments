"""Configuration management for URL validation."""

from dataclasses import dataclass, field
from typing import Set, Optional, Dict, Any
import logging


@dataclass
class ValidationConfig:
    """
    Configuration settings for URL validation.

    This class contains all configurable parameters for the URL validator,
    including timeouts, security settings, and behavior options.

    Attributes:
        timeout: Network request timeout in seconds
        max_redirects: Maximum number of redirects to follow
        verify_ssl: Whether to verify SSL certificates
        user_agent: User-Agent header for HTTP requests
        allowed_schemes: Set of allowed URL schemes
        block_private_ips: Whether to block private IP addresses
        retry_attempts: Number of retry attempts for failed requests
        retry_delay: Initial delay between retries in seconds
        max_response_size: Maximum response size in bytes
        follow_redirects: Whether to follow HTTP redirects
        custom_headers: Additional HTTP headers to include
        proxy_settings: Proxy configuration
        log_level: Logging level for validation operations
    """

    # Network settings
    timeout: int = 10
    max_redirects: int = 5
    verify_ssl: bool = True
    user_agent: str = "URLValidator/1.0 (Python urllib)"

    # Security settings
    allowed_schemes: Set[str] = field(default_factory=lambda: {"http", "https"})
    block_private_ips: bool = False

    # Retry settings
    retry_attempts: int = 3
    retry_delay: float = 1.0

    # Response settings
    max_response_size: int = 10 * 1024 * 1024  # 10MB
    follow_redirects: bool = True

    # Advanced settings
    custom_headers: Dict[str, str] = field(default_factory=dict)
    proxy_settings: Optional[Dict[str, str]] = None
    log_level: str = "INFO"

    def __post_init__(self):
        """Validate configuration after initialization."""
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate configuration parameters."""
        errors = []

        # Validate timeout
        if not isinstance(self.timeout, int) or self.timeout <= 0:
            errors.append("timeout must be a positive integer")

        # Validate max_redirects
        if not isinstance(self.max_redirects, int) or self.max_redirects < 0:
            errors.append("max_redirects must be a non-negative integer")

        # Validate retry_attempts
        if not isinstance(self.retry_attempts, int) or self.retry_attempts < 0:
            errors.append("retry_attempts must be a non-negative integer")

        # Validate retry_delay
        if not isinstance(self.retry_delay, (int, float)) or self.retry_delay < 0:
            errors.append("retry_delay must be a non-negative number")

        # Validate max_response_size
        if not isinstance(self.max_response_size, int) or self.max_response_size <= 0:
            errors.append("max_response_size must be a positive integer")

        # Validate allowed_schemes
        if not isinstance(self.allowed_schemes, set) or not self.allowed_schemes:
            errors.append("allowed_schemes must be a non-empty set")

        # Validate user_agent
        if not isinstance(self.user_agent, str) or not self.user_agent.strip():
            errors.append("user_agent must be a non-empty string")

        # Validate log_level
        valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.log_level.upper() not in valid_log_levels:
            errors.append(f"log_level must be one of {valid_log_levels}")

        if errors:
            raise ValueError(f"Invalid configuration: {'; '.join(errors)}")

    @classmethod
    def create_permissive(cls) -> "ValidationConfig":
        """
        Create a permissive configuration for development/testing.

        Returns:
            ValidationConfig with relaxed security settings
        """
        return cls(
            timeout=30,
            max_redirects=10,
            verify_ssl=False,
            block_private_ips=False,
            allowed_schemes={"http", "https", "ftp", "ftps"},
            retry_attempts=1,
            log_level="DEBUG"
        )

    @classmethod
    def create_strict(cls) -> "ValidationConfig":
        """
        Create a strict configuration for production use.

        Returns:
            ValidationConfig with enhanced security settings
        """
        return cls(
            timeout=5,
            max_redirects=2,
            verify_ssl=True,
            block_private_ips=True,
            allowed_schemes={"https"},
            retry_attempts=2,
            max_response_size=1024 * 1024,  # 1MB
            log_level="WARNING"
        )

    @classmethod
    def create_fast(cls) -> "ValidationConfig":
        """
        Create a fast configuration optimized for performance.

        Returns:
            ValidationConfig with settings optimized for speed
        """
        return cls(
            timeout=3,
            max_redirects=1,
            verify_ssl=True,
            retry_attempts=1,
            retry_delay=0.5,
            follow_redirects=False,
            log_level="ERROR"
        )

    def update(self, **kwargs) -> "ValidationConfig":
        """
        Create a new configuration with updated values.

        Args:
            **kwargs: Configuration parameters to update

        Returns:
            New ValidationConfig instance with updated values

        Raises:
            ValueError: If invalid configuration parameters are provided
        """
        # Get current values as dict
        current_values = {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }

        # Update with new values
        current_values.update(kwargs)

        # Create new instance
        return self.__class__(**current_values)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.

        Returns:
            Dictionary representation of the configuration
        """
        return {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "ValidationConfig":
        """
        Create configuration from dictionary.

        Args:
            config_dict: Dictionary containing configuration values

        Returns:
            ValidationConfig instance

        Raises:
            ValueError: If invalid configuration is provided
        """
        # Handle allowed_schemes conversion from list to set
        if "allowed_schemes" in config_dict:
            if isinstance(config_dict["allowed_schemes"], list):
                config_dict["allowed_schemes"] = set(config_dict["allowed_schemes"])

        return cls(**config_dict)

    def get_requests_kwargs(self) -> Dict[str, Any]:
        """
        Get configuration parameters for requests library.

        Returns:
            Dictionary of parameters suitable for requests.Session
        """
        return {
            "timeout": self.timeout,
            "verify": self.verify_ssl,
            "allow_redirects": self.follow_redirects,
            "headers": {
                "User-Agent": self.user_agent,
                **self.custom_headers
            },
            "proxies": self.proxy_settings,
        }

    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger configured for this validation config.

        Args:
            name: Logger name

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, self.log_level.upper()))
        return logger