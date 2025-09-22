"""
Platform-specific operations for path validation.
"""

from .detection import get_current_platform, detect_platform_features
from .base import PlatformOperations
from .windows import WindowsOperations
from .posix import PosixOperations

__all__ = [
    "get_current_platform",
    "detect_platform_features",
    "PlatformOperations",
    "WindowsOperations",
    "PosixOperations",
]