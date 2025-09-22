# Security Requirements and Path Traversal Prevention

## Security Threat Model

### Primary Security Concerns
1. **Path Traversal Attacks**: Prevention of directory traversal using `../` sequences
2. **Symbolic Link Attacks**: Malicious symlink exploitation
3. **File System Injection**: Injection of malicious path components
4. **Resource Exhaustion**: DoS through extremely long paths or deep recursion
5. **Information Disclosure**: Unauthorized access to sensitive file system areas
6. **TOCTOU Attacks**: Time-of-check to time-of-use vulnerabilities

## Path Traversal Prevention

### Directory Traversal Detection
```python
TRAVERSAL_PATTERNS = [
    '../',      # Basic traversal
    '..\\',     # Windows traversal
    '..%2f',    # URL encoded forward slash
    '..%5c',    # URL encoded backslash
    '..%252f',  # Double URL encoded
    '..../',    # Double dot variant
    '....\\',   # Double dot Windows variant
]

NORMALIZED_TRAVERSAL = [
    '..',       # After normalization
    '.',        # Current directory
]
```

### Traversal Prevention Algorithms
```python
def detect_path_traversal(path: str) -> bool:
    """
    Detect various forms of path traversal attempts.
    Returns True if traversal detected, False otherwise.
    """
    # URL decode the path first
    decoded_path = url_decode(path)

    # Check for obvious traversal patterns
    for pattern in TRAVERSAL_PATTERNS:
        if pattern in decoded_path.lower():
            return True

    # Normalize and check resolved path
    normalized = os.path.normpath(decoded_path)
    components = normalized.split(os.sep)

    for component in components:
        if component in NORMALIZED_TRAVERSAL:
            return True

    return False
```

### Secure Path Resolution
```python
def resolve_secure_path(base_path: str, user_path: str) -> Optional[str]:
    """
    Safely resolve a user-provided path against a base directory.
    Returns None if the resolved path escapes the base directory.
    """
    # Normalize both paths
    base = os.path.abspath(base_path)
    full_path = os.path.abspath(os.path.join(base, user_path))

    # Check if resolved path is within base directory
    if not full_path.startswith(base + os.sep) and full_path != base:
        return None

    return full_path
```

## Symbolic Link Security

### Symlink Attack Prevention
```python
def validate_symlink_safety(path: str, max_depth: int = 5) -> bool:
    """
    Validate that symlinks don't create security vulnerabilities.
    Prevents infinite loops and ensures links stay within safe boundaries.
    """
    if not os.path.islink(path):
        return True

    visited = set()
    current = path
    depth = 0

    while os.path.islink(current) and depth < max_depth:
        if current in visited:
            return False  # Infinite loop detected

        visited.add(current)
        target = os.readlink(current)

        # Resolve relative symlinks
        if not os.path.isabs(target):
            target = os.path.join(os.path.dirname(current), target)

        current = os.path.normpath(target)
        depth += 1

    return depth < max_depth
```

### Symlink Resolution Policies
```python
class SymlinkPolicy(Enum):
    FORBID = "forbid"           # Reject all symlinks
    ALLOW_SAFE = "allow_safe"   # Allow only safe symlinks
    FOLLOW = "follow"           # Follow all symlinks (less secure)
    NO_FOLLOW = "no_follow"     # Don't follow, treat as regular files
```

## Input Sanitization

### Path Sanitization Rules
```python
def sanitize_path_input(path: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    """
    # Remove null bytes
    path = path.replace('\0', '')

    # Remove or escape dangerous characters
    dangerous_chars = {
        '\r': '',  # Carriage return
        '\n': '',  # Line feed
        '\t': '',  # Tab
    }

    for char, replacement in dangerous_chars.items():
        path = path.replace(char, replacement)

    # Limit path length to prevent resource exhaustion
    max_length = 4096  # Configurable
    if len(path) > max_length:
        raise ValueError(f"Path too long: {len(path)} > {max_length}")

    return path
```

### Character Validation
```python
def validate_safe_characters(path: str, platform: str = None) -> bool:
    """
    Validate that path contains only safe characters for the target platform.
    """
    if platform is None:
        platform = get_current_platform()

    if platform == 'windows':
        forbidden = set('<>:"|?*\0')
        # Check for forbidden Windows characters
        if any(char in forbidden for char in path):
            return False

        # Check for control characters (ASCII 0-31)
        if any(ord(char) < 32 for char in path):
            return False

    # Universal checks
    if '\0' in path:  # Null byte injection
        return False

    return True
```

## Access Control Integration

### Sandbox Path Validation
```python
class PathSandbox:
    """
    Define and enforce path access boundaries.
    """
    def __init__(self, allowed_roots: List[str], forbidden_paths: List[str] = None):
        self.allowed_roots = [os.path.abspath(root) for root in allowed_roots]
        self.forbidden_paths = [os.path.abspath(path) for path in (forbidden_paths or [])]

    def is_path_allowed(self, path: str) -> bool:
        """Check if path is within allowed boundaries."""
        abs_path = os.path.abspath(path)

        # Check forbidden paths first
        for forbidden in self.forbidden_paths:
            if abs_path.startswith(forbidden):
                return False

        # Check allowed roots
        for root in self.allowed_roots:
            if abs_path.startswith(root):
                return True

        return False
```

### Permission Validation
```python
def validate_required_permissions(path: str, required_perms: List[str]) -> bool:
    """
    Validate that the current user has required permissions for the path.
    required_perms: List of 'read', 'write', 'execute'
    """
    if not os.path.exists(path):
        # Check parent directory for write permission if creating new file
        parent = os.path.dirname(path)
        if 'write' in required_perms:
            return os.access(parent, os.W_OK)
        return False

    perm_map = {
        'read': os.R_OK,
        'write': os.W_OK,
        'execute': os.X_OK
    }

    for perm in required_perms:
        if perm in perm_map and not os.access(path, perm_map[perm]):
            return False

    return True
```

## Resource Protection

### Path Complexity Limits
```python
class PathComplexityLimits:
    MAX_DEPTH = 32          # Maximum directory depth
    MAX_COMPONENTS = 256    # Maximum path components
    MAX_COMPONENT_LENGTH = 255  # Maximum single component length
    MAX_TOTAL_LENGTH = 4096 # Maximum total path length

def validate_path_complexity(path: str, limits: PathComplexityLimits = None) -> bool:
    """
    Validate path complexity to prevent resource exhaustion attacks.
    """
    if limits is None:
        limits = PathComplexityLimits()

    # Check total length
    if len(path) > limits.MAX_TOTAL_LENGTH:
        return False

    # Split into components
    components = path.split(os.sep)

    # Check component count
    if len(components) > limits.MAX_COMPONENTS:
        return False

    # Check depth (excluding empty components from absolute paths)
    actual_components = [c for c in components if c]
    if len(actual_components) > limits.MAX_DEPTH:
        return False

    # Check individual component lengths
    for component in actual_components:
        if len(component) > limits.MAX_COMPONENT_LENGTH:
            return False

    return True
```

### Rate Limiting and DoS Prevention
```python
from collections import defaultdict
from time import time

class ValidationRateLimiter:
    """
    Rate limiter to prevent DoS attacks through excessive validation requests.
    """
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check if client is within rate limits."""
        now = time()
        client_requests = self.requests[client_id]

        # Remove old requests outside window
        client_requests[:] = [req_time for req_time in client_requests
                            if now - req_time <= self.window_seconds]

        # Check if under limit
        if len(client_requests) >= self.max_requests:
            return False

        # Record this request
        client_requests.append(now)
        return True
```

## Security Configuration

### Security Policy Configuration
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class SecurityPolicy:
    """Configuration for security validation policies."""

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
```

## Security Testing Requirements

### Security Test Categories
1. **Path Traversal Tests**
   - Various encoding schemes
   - Multiple traversal patterns
   - Deep directory traversals
   - Cross-platform traversal attempts

2. **Input Fuzzing**
   - Random character injection
   - Buffer overflow attempts
   - Unicode normalization attacks
   - Encoding confusion attacks

3. **Symlink Security Tests**
   - Symlink loops
   - Symlink escape attempts
   - TOCTOU race conditions
   - Privilege escalation attempts

4. **Resource Exhaustion Tests**
   - Extremely long paths
   - Deep directory structures
   - High-frequency validation requests
   - Memory exhaustion attempts

### Penetration Testing Scenarios
```python
def security_test_suite():
    """
    Comprehensive security test cases for path validation.
    """
    test_cases = [
        # Path traversal attempts
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\config\\sam",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",

        # Null byte injection
        "valid_file.txt\x00.exe",
        "safe_path\x00../../../sensitive",

        # Unicode attacks
        "\u002e\u002e\u002fconfig",
        "\uff0e\uff0e\uff0fconfig",

        # Long path attacks
        "A" * 10000,
        "/".join(["component"] * 1000),

        # Special character injection
        "file|rm -rf /",
        "file;cat /etc/passwd",
        "file`whoami`",
    ]

    return test_cases
```