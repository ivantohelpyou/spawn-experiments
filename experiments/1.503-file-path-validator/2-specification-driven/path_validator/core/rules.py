"""
Validation rules and rule engine.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass

from ..exceptions.errors import PathValidationError


@dataclass
class RuleResult:
    """Result of applying a validation rule."""
    passed: bool
    message: Optional[str] = None
    error_code: Optional[str] = None
    severity: str = "error"  # "error", "warning", "info"
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ValidationRule(ABC):
    """Abstract base class for validation rules."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    @abstractmethod
    def validate(self, path: str, context: Dict[str, Any] = None) -> RuleResult:
        """
        Validate a path against this rule.

        Args:
            path: Path to validate
            context: Additional context for validation

        Returns:
            RuleResult: Result of the validation
        """
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


class LengthRule(ValidationRule):
    """Rule to validate path length constraints."""

    def __init__(self, max_length: int, max_component_length: Optional[int] = None):
        super().__init__(
            name="length_validation",
            description=f"Validate path length (max: {max_length})"
        )
        self.max_length = max_length
        self.max_component_length = max_component_length

    def validate(self, path: str, context: Dict[str, Any] = None) -> RuleResult:
        # Check total path length
        if len(path) > self.max_length:
            return RuleResult(
                passed=False,
                message=f"Path length {len(path)} exceeds maximum {self.max_length}",
                error_code="E3002",
                metadata={"actual_length": len(path), "max_length": self.max_length}
            )

        # Check component lengths if specified
        if self.max_component_length:
            import os
            components = path.split(os.sep)
            for component in components:
                if component and len(component) > self.max_component_length:
                    return RuleResult(
                        passed=False,
                        message=f"Component '{component}' exceeds maximum length {self.max_component_length}",
                        error_code="E3003",
                        metadata={
                            "component": component,
                            "component_length": len(component),
                            "max_component_length": self.max_component_length
                        }
                    )

        return RuleResult(passed=True)


class CharacterRule(ValidationRule):
    """Rule to validate allowed/forbidden characters."""

    def __init__(self, forbidden_chars: set, name: str = "character_validation"):
        super().__init__(
            name=name,
            description=f"Validate characters (forbidden: {forbidden_chars})"
        )
        self.forbidden_chars = forbidden_chars

    def validate(self, path: str, context: Dict[str, Any] = None) -> RuleResult:
        invalid_chars = []
        for char in path:
            if char in self.forbidden_chars:
                invalid_chars.append(char)

        if invalid_chars:
            # Format characters for display
            formatted_chars = []
            for char in invalid_chars:
                if char == '\x00':
                    formatted_chars.append('\\0')
                elif ord(char) < 32:
                    formatted_chars.append(f'\\x{ord(char):02x}')
                else:
                    formatted_chars.append(repr(char))

            return RuleResult(
                passed=False,
                message=f"Path contains forbidden characters: {', '.join(formatted_chars)}",
                error_code="E1003",
                metadata={"invalid_chars": invalid_chars}
            )

        return RuleResult(passed=True)


class ExtensionRule(ValidationRule):
    """Rule to validate file extensions."""

    def __init__(self, allowed_extensions: Optional[List[str]] = None,
                 forbidden_extensions: Optional[List[str]] = None):
        super().__init__(
            name="extension_validation",
            description="Validate file extensions"
        )
        self.allowed_extensions = set(allowed_extensions) if allowed_extensions else None
        self.forbidden_extensions = set(forbidden_extensions) if forbidden_extensions else None

    def validate(self, path: str, context: Dict[str, Any] = None) -> RuleResult:
        import os
        _, extension = os.path.splitext(path)
        extension = extension.lower()

        if self.forbidden_extensions and extension in self.forbidden_extensions:
            return RuleResult(
                passed=False,
                message=f"Forbidden file extension: {extension}",
                error_code="E1003",
                metadata={"extension": extension, "forbidden_extensions": list(self.forbidden_extensions)}
            )

        if self.allowed_extensions and extension not in self.allowed_extensions:
            return RuleResult(
                passed=False,
                message=f"File extension not in allowed list: {extension}",
                error_code="E1003",
                metadata={"extension": extension, "allowed_extensions": list(self.allowed_extensions)}
            )

        return RuleResult(passed=True)


class PatternRule(ValidationRule):
    """Rule to validate paths against regex patterns."""

    def __init__(self, pattern: str, must_match: bool = True, name: str = "pattern_validation"):
        super().__init__(
            name=name,
            description=f"Validate against pattern: {pattern}"
        )
        import re
        self.pattern = re.compile(pattern)
        self.must_match = must_match
        self.pattern_str = pattern

    def validate(self, path: str, context: Dict[str, Any] = None) -> RuleResult:
        matches = bool(self.pattern.search(path))

        if self.must_match and not matches:
            return RuleResult(
                passed=False,
                message=f"Path does not match required pattern: {self.pattern_str}",
                error_code="E1001",
                metadata={"pattern": self.pattern_str, "must_match": True}
            )
        elif not self.must_match and matches:
            return RuleResult(
                passed=False,
                message=f"Path matches forbidden pattern: {self.pattern_str}",
                error_code="E1001",
                metadata={"pattern": self.pattern_str, "must_match": False}
            )

        return RuleResult(passed=True)


class CustomRule(ValidationRule):
    """Rule that uses a custom validation function."""

    def __init__(self, name: str, validator_func: Callable[[str], bool],
                 error_message: str = "Custom validation failed",
                 error_code: str = "E5001"):
        super().__init__(
            name=name,
            description="Custom validation rule"
        )
        self.validator_func = validator_func
        self.error_message = error_message
        self.error_code = error_code

    def validate(self, path: str, context: Dict[str, Any] = None) -> RuleResult:
        try:
            if self.validator_func(path):
                return RuleResult(passed=True)
            else:
                return RuleResult(
                    passed=False,
                    message=self.error_message,
                    error_code=self.error_code
                )
        except Exception as e:
            return RuleResult(
                passed=False,
                message=f"Custom validation error: {e}",
                error_code=self.error_code,
                metadata={"exception": str(e)}
            )


class ExistenceRule(ValidationRule):
    """Rule to validate path existence requirements."""

    def __init__(self, must_exist: bool = True, must_be_file: Optional[bool] = None,
                 must_be_directory: Optional[bool] = None):
        super().__init__(
            name="existence_validation",
            description="Validate path existence"
        )
        self.must_exist = must_exist
        self.must_be_file = must_be_file
        self.must_be_directory = must_be_directory

    def validate(self, path: str, context: Dict[str, Any] = None) -> RuleResult:
        import os

        exists = os.path.exists(path)

        if self.must_exist and not exists:
            return RuleResult(
                passed=False,
                message=f"Path does not exist: {path}",
                error_code="E4001"
            )

        if not self.must_exist and exists:
            return RuleResult(
                passed=False,
                message=f"Path must not exist: {path}",
                error_code="E4001"
            )

        if exists:
            if self.must_be_file is not None:
                is_file = os.path.isfile(path)
                if self.must_be_file and not is_file:
                    return RuleResult(
                        passed=False,
                        message=f"Path is not a file: {path}",
                        error_code="E4002"
                    )
                if not self.must_be_file and is_file:
                    return RuleResult(
                        passed=False,
                        message=f"Path must not be a file: {path}",
                        error_code="E4002"
                    )

            if self.must_be_directory is not None:
                is_dir = os.path.isdir(path)
                if self.must_be_directory and not is_dir:
                    return RuleResult(
                        passed=False,
                        message=f"Path is not a directory: {path}",
                        error_code="E4003"
                    )
                if not self.must_be_directory and is_dir:
                    return RuleResult(
                        passed=False,
                        message=f"Path must not be a directory: {path}",
                        error_code="E4003"
                    )

        return RuleResult(passed=True)


class ValidationRules:
    """Container and engine for validation rules."""

    def __init__(self):
        self.rules: List[ValidationRule] = []
        self.stop_on_first_error = True

    def add_rule(self, rule: ValidationRule) -> None:
        """Add a validation rule."""
        self.rules.append(rule)

    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name."""
        for i, rule in enumerate(self.rules):
            if rule.name == name:
                del self.rules[i]
                return True
        return False

    def get_rule(self, name: str) -> Optional[ValidationRule]:
        """Get a rule by name."""
        for rule in self.rules:
            if rule.name == name:
                return rule
        return None

    def validate_all(self, path: str, context: Dict[str, Any] = None) -> List[RuleResult]:
        """
        Validate path against all rules.

        Args:
            path: Path to validate
            context: Additional context for validation

        Returns:
            List[RuleResult]: Results from all applicable rules
        """
        results = []
        context = context or {}

        for rule in self.rules:
            try:
                result = rule.validate(path, context)
                results.append(result)

                # Stop on first error if configured
                if self.stop_on_first_error and not result.passed and result.severity == "error":
                    break

            except Exception as e:
                # Rule execution failed
                error_result = RuleResult(
                    passed=False,
                    message=f"Rule execution failed: {e}",
                    error_code="E5001",
                    metadata={"rule_name": rule.name, "exception": str(e)}
                )
                results.append(error_result)

                if self.stop_on_first_error:
                    break

        return results

    def is_valid(self, path: str, context: Dict[str, Any] = None) -> bool:
        """Check if path passes all validation rules."""
        results = self.validate_all(path, context)
        return all(result.passed or result.severity != "error" for result in results)

    def get_errors(self, path: str, context: Dict[str, Any] = None) -> List[RuleResult]:
        """Get only error results from validation."""
        results = self.validate_all(path, context)
        return [result for result in results if not result.passed and result.severity == "error"]

    def get_warnings(self, path: str, context: Dict[str, Any] = None) -> List[RuleResult]:
        """Get only warning results from validation."""
        results = self.validate_all(path, context)
        return [result for result in results if not result.passed and result.severity == "warning"]

    def clear_rules(self) -> None:
        """Remove all rules."""
        self.rules.clear()

    def rule_count(self) -> int:
        """Get the number of rules."""
        return len(self.rules)

    def create_standard_rules(self, platform: str = "auto") -> None:
        """Create a standard set of validation rules for the platform."""
        self.clear_rules()

        if platform == "auto":
            import os
            platform = "windows" if os.name == 'nt' else "posix"

        if platform == "windows":
            # Windows-specific rules
            self.add_rule(LengthRule(max_length=260, max_component_length=255))
            self.add_rule(CharacterRule(forbidden_chars=set('<>:"|?*\x00')))
            self.add_rule(PatternRule(
                pattern=r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)',
                must_match=False,
                name="windows_reserved_names"
            ))
        else:
            # POSIX-specific rules
            self.add_rule(LengthRule(max_length=4096, max_component_length=255))
            self.add_rule(CharacterRule(forbidden_chars=set('\x00')))

        # Common rules
        self.add_rule(PatternRule(
            pattern=r'\.\./|\.\.\.',
            must_match=False,
            name="path_traversal_prevention"
        ))

    def to_dict(self) -> Dict[str, Any]:
        """Export rules configuration to dictionary."""
        return {
            "stop_on_first_error": self.stop_on_first_error,
            "rule_count": len(self.rules),
            "rules": [
                {
                    "name": rule.name,
                    "description": rule.description,
                    "type": rule.__class__.__name__
                }
                for rule in self.rules
            ]
        }