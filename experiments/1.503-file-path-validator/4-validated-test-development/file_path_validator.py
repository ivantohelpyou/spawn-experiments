#!/usr/bin/env python3
"""
File path validator using os.path and pathlib libraries.
INTENTIONALLY INCORRECT IMPLEMENTATION for test validation.
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class ValidationResult:
    """Result of path validation"""
    is_valid: bool
    path_type: str = ""
    error_message: str = ""
    original_input_type: str = ""


@dataclass
class SecurityResult:
    """Result of security validation"""
    is_secure: bool
    error_message: str = ""


@dataclass
class ExistenceResult:
    """Result of path existence check"""
    exists: bool
    path_type: str = ""  # "file", "directory", or ""


@dataclass
class NormalizationResult:
    """Result of path normalization"""
    normalized_path: str
    original_path: str


class FilePathValidator:
    """
    File path validator with configurable options.
    INTENTIONALLY INCORRECT IMPLEMENTATION.
    """

    def __init__(self, allow_relative=True, allow_path_traversal=True, max_length=4096):
        """Initialize validator with configuration options"""
        self.allow_relative = allow_relative
        self.allow_path_traversal = allow_path_traversal
        self.max_length = max_length

    def is_valid_path(self, path: Union[str, Path]) -> ValidationResult:
        """
        Validate a file path.
        INTENTIONALLY INCORRECT: Always returns True for everything.
        """
        # Convert to string if Path object
        if isinstance(path, Path):
            original_type = "pathlib.Path"
            path_str = str(path)
        else:
            original_type = "str"
            path_str = path

        # WRONG: Always return valid regardless of input
        return ValidationResult(
            is_valid=True,  # This is wrong!
            path_type="absolute" if os.path.isabs(path_str) else "relative",
            original_input_type=original_type
        )

    def is_secure_path(self, path: str, base_directory: str) -> SecurityResult:
        """
        Check if path is secure (no path traversal).
        INTENTIONALLY INCORRECT: Always returns secure.
        """
        # WRONG: Always return secure
        return SecurityResult(is_secure=True)

    def path_exists(self, path: Union[str, Path]) -> ExistenceResult:
        """
        Check if path exists and determine its type.
        INTENTIONALLY INCORRECT: Random results.
        """
        # WRONG: Return random/incorrect results
        return ExistenceResult(
            exists=False,  # Always say it doesn't exist
            path_type=""
        )

    def normalize_path(self, path: str) -> NormalizationResult:
        """
        Normalize a file path.
        INTENTIONALLY INCORRECT: Don't normalize.
        """
        # WRONG: Don't actually normalize
        return NormalizationResult(
            normalized_path=path,  # Return unchanged
            original_path=path
        )