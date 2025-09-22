"""
Utility functions for file handling and data processing.
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional, Tuple


def read_json_file(file_path: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Read and parse a JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Tuple of (success, data, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return True, data, None
    except FileNotFoundError:
        return False, None, f"File not found: {file_path}"
    except json.JSONDecodeError as e:
        return False, None, f"Invalid JSON: {e}"
    except Exception as e:
        return False, None, f"Error reading file: {e}"


def read_json_stdin() -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Read and parse JSON from stdin.

    Returns:
        Tuple of (success, data, error_message)
    """
    try:
        data = json.load(sys.stdin)
        return True, data, None
    except json.JSONDecodeError as e:
        return False, None, f"Invalid JSON from stdin: {e}"
    except Exception as e:
        return False, None, f"Error reading from stdin: {e}"


def is_valid_json_file(file_path: str) -> bool:
    """
    Check if a file contains valid JSON.

    Args:
        file_path: Path to file

    Returns:
        True if file contains valid JSON, False otherwise
    """
    success, _, _ = read_json_file(file_path)
    return success


def get_file_list(patterns: List[str], recursive: bool = False) -> List[str]:
    """
    Expand file patterns to actual file paths.

    Args:
        patterns: List of file patterns (can include globs)
        recursive: Whether to search recursively

    Returns:
        List of actual file paths
    """
    import glob

    files = []
    for pattern in patterns:
        if recursive:
            matches = glob.glob(pattern, recursive=True)
        else:
            matches = glob.glob(pattern)

        if matches:
            files.extend(matches)
        else:
            # Keep pattern as-is if no matches (let caller handle error)
            files.append(pattern)

    # Filter to existing files and remove duplicates
    existing_files = []
    seen = set()
    for f in files:
        if os.path.isfile(f) and f not in seen:
            existing_files.append(f)
            seen.add(f)

    return existing_files


def validate_file_access(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a file exists and is readable.

    Args:
        file_path: Path to file

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not os.path.exists(file_path):
        return False, f"File does not exist: {file_path}"

    if not os.path.isfile(file_path):
        return False, f"Path is not a file: {file_path}"

    if not os.access(file_path, os.R_OK):
        return False, f"File is not readable: {file_path}"

    return True, None


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Get information about a file.

    Args:
        file_path: Path to file

    Returns:
        Dictionary with file information
    """
    try:
        stat = os.stat(file_path)
        return {
            'path': file_path,
            'size': stat.st_size,
            'size_formatted': format_file_size(stat.st_size),
            'exists': True,
            'readable': os.access(file_path, os.R_OK),
            'is_json': file_path.lower().endswith('.json'),
            'modified_time': stat.st_mtime
        }
    except Exception:
        return {
            'path': file_path,
            'exists': False,
            'readable': False,
            'is_json': file_path.lower().endswith('.json')
        }


class FileProcessor:
    """Helper class for processing multiple files."""

    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        self.total_size = 0

    def process_files(self, file_paths: List[str], processor_func, *args, **kwargs):
        """
        Process multiple files with a given function.

        Args:
            file_paths: List of file paths to process
            processor_func: Function to call for each file
            *args, **kwargs: Additional arguments for processor function

        Returns:
            List of results from processor function
        """
        results = []
        for file_path in file_paths:
            try:
                result = processor_func(file_path, *args, **kwargs)
                results.append(result)
                self.processed_count += 1

                # Track file size if accessible
                try:
                    self.total_size += os.path.getsize(file_path)
                except Exception:
                    pass

            except Exception as e:
                self.error_count += 1
                # Return error result in expected format
                from .core.validator import ValidationError
                error = ValidationError("$", f"Processing error: {e}")
                results.append((False, [error]))

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            'processed_count': self.processed_count,
            'error_count': self.error_count,
            'total_size': self.total_size,
            'total_size_formatted': format_file_size(self.total_size)
        }