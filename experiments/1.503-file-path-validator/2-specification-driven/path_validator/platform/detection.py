"""
Platform detection and feature discovery for path validation.
"""

import os
import platform
import sys
from typing import Dict, Any, Optional


def get_current_platform() -> str:
    """
    Detect the current platform for path validation.

    Returns:
        str: Platform identifier ('windows', 'posix', 'macos', or 'unknown')
    """
    system = platform.system().lower()

    if system == 'windows':
        return 'windows'
    elif system == 'darwin':
        return 'macos'
    elif system in ('linux', 'freebsd', 'openbsd', 'netbsd', 'sunos', 'aix'):
        return 'posix'
    else:
        return 'unknown'


def detect_platform_features() -> Dict[str, Any]:
    """
    Detect platform-specific filesystem features and capabilities.

    Returns:
        dict: Dictionary containing feature flags and limits
    """
    features = {
        'platform': get_current_platform(),
        'python_version': sys.version_info[:3],
        'case_sensitive': _detect_case_sensitivity(),
        'supports_symlinks': _detect_symlink_support(),
        'supports_unicode_filenames': _detect_unicode_support(),
        'max_path_length': _get_max_path_length(),
        'max_component_length': _get_max_component_length(),
        'path_separator': os.sep,
        'alt_separator': os.altsep,
        'forbidden_chars': _get_forbidden_characters(),
        'reserved_names': _get_reserved_names(),
        'supports_long_paths': _detect_long_path_support(),
        'filesystem_encoding': sys.getfilesystemencoding(),
    }

    return features


def _detect_case_sensitivity() -> bool:
    """Detect if the filesystem is case-sensitive."""
    try:
        # Compare normalized case versions
        return os.path.normcase('A') != os.path.normcase('a')
    except Exception:
        # Default based on platform
        return get_current_platform() in ('posix', 'macos')


def _detect_symlink_support() -> bool:
    """Detect if the platform supports symbolic links."""
    return hasattr(os, 'symlink') and hasattr(os, 'readlink')


def _detect_unicode_support() -> bool:
    """Detect if the filesystem supports Unicode filenames."""
    # Most modern filesystems support Unicode
    try:
        return hasattr(os, 'supports_unicode_filenames')
    except Exception:
        return True  # Assume support for modern systems


def _get_max_path_length() -> int:
    """Get the maximum path length for the current platform."""
    current_platform = get_current_platform()

    if current_platform == 'windows':
        # Windows has different limits based on API used
        return 260  # Traditional limit, can be 32767 with long path support

    # POSIX systems
    try:
        # Try to get from pathconf if available
        if hasattr(os, 'pathconf') and hasattr(os, 'pathconf_names'):
            path_max = os.pathconf_names.get('PC_PATH_MAX')
            if path_max is not None:
                return os.pathconf('/', path_max)
    except (OSError, AttributeError):
        pass

    # Default POSIX limit
    return 4096


def _get_max_component_length() -> int:
    """Get the maximum filename component length."""
    try:
        # Try to get from pathconf if available
        if hasattr(os, 'pathconf') and hasattr(os, 'pathconf_names'):
            name_max = os.pathconf_names.get('PC_NAME_MAX')
            if name_max is not None:
                return os.pathconf('/', name_max)
    except (OSError, AttributeError):
        pass

    # Default limit (common for most filesystems)
    return 255


def _get_forbidden_characters() -> set:
    """Get the set of characters forbidden in filenames."""
    current_platform = get_current_platform()

    if current_platform == 'windows':
        # Windows forbidden characters
        forbidden = set('<>:"|?*\x00')
        # Add control characters (0-31)
        forbidden.update(chr(i) for i in range(32))
        return forbidden
    else:
        # POSIX systems - only null byte is universally forbidden
        return {'\x00'}


def _get_reserved_names() -> set:
    """Get the set of reserved filenames for the current platform."""
    current_platform = get_current_platform()

    if current_platform == 'windows':
        return {
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        }
    else:
        # POSIX systems generally don't have reserved names at the filesystem level
        return set()


def _detect_long_path_support() -> bool:
    """Detect if the platform supports long paths (>260 characters on Windows)."""
    current_platform = get_current_platform()

    if current_platform == 'windows':
        # On Windows, long path support depends on OS version and registry settings
        try:
            # Check Windows 10 version 1607+ which supports long paths
            version = platform.version()
            if version:
                # Parse version string to check if it's Windows 10 build 14393+
                parts = version.split('.')
                if len(parts) >= 3:
                    build = int(parts[2])
                    return build >= 14393
        except (ValueError, IndexError):
            pass

        # Fallback: assume no long path support
        return False
    else:
        # POSIX systems typically support long paths by default
        return True


def get_platform_specific_validator():
    """
    Get the appropriate platform-specific validator class.

    Returns:
        class: Platform-specific validator class
    """
    from .windows import WindowsOperations
    from .posix import PosixOperations

    current_platform = get_current_platform()

    if current_platform == 'windows':
        return WindowsOperations
    elif current_platform in ('posix', 'macos'):
        return PosixOperations
    else:
        # Default to POSIX for unknown platforms
        return PosixOperations


def is_platform_path_valid(path: str, target_platform: Optional[str] = None) -> bool:
    """
    Quick check if a path is valid for the specified platform.

    Args:
        path: Path to validate
        target_platform: Target platform ('windows', 'posix', 'macos'), or None for current

    Returns:
        bool: True if path appears valid for the platform
    """
    if target_platform is None:
        target_platform = get_current_platform()

    # Quick basic checks
    if not path or '\x00' in path:
        return False

    if target_platform == 'windows':
        # Check Windows-specific constraints
        forbidden = _get_forbidden_characters()
        if any(char in forbidden for char in path):
            return False

        # Check reserved names
        reserved = _get_reserved_names()
        components = path.replace('\\', '/').split('/')
        for component in components:
            if component.upper() in reserved:
                return False

        # Check length (basic check for traditional limit)
        if len(path) > 260:
            return False

    # For POSIX systems, most paths are valid if they don't contain null bytes
    return True