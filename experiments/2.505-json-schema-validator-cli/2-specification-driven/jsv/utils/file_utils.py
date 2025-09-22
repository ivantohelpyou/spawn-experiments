"""File handling utilities for JSON Schema Validator CLI."""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import glob

from ..exceptions import FileError


def read_json_file(file_path: str) -> Dict[str, Any]:
    """Read and parse a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Parsed JSON data as dictionary

    Raises:
        FileError: If file cannot be read or parsed
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileError(f"File not found: {file_path}")

        if not path.is_file():
            raise FileError(f"Path is not a file: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    except json.JSONDecodeError as e:
        raise FileError(f"Invalid JSON in {file_path}: {e}")
    except PermissionError:
        raise FileError(f"Permission denied reading {file_path}")
    except Exception as e:
        raise FileError(f"Error reading {file_path}: {e}")


def read_json_from_stdin() -> Dict[str, Any]:
    """Read and parse JSON data from stdin.

    Returns:
        Parsed JSON data as dictionary

    Raises:
        FileError: If stdin cannot be read or parsed
    """
    try:
        data = sys.stdin.read()
        if not data.strip():
            raise FileError("No data received from stdin")
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise FileError(f"Invalid JSON from stdin: {e}")
    except Exception as e:
        raise FileError(f"Error reading from stdin: {e}")


def find_files(patterns: List[str]) -> List[str]:
    """Find files matching given glob patterns.

    Args:
        patterns: List of glob patterns

    Returns:
        List of file paths that match the patterns

    Raises:
        FileError: If no files found or patterns are invalid
    """
    all_files = []

    for pattern in patterns:
        try:
            matches = glob.glob(pattern, recursive=True)
            # Filter to only include files (not directories)
            files = [f for f in matches if Path(f).is_file()]
            all_files.extend(files)
        except Exception as e:
            raise FileError(f"Error processing pattern '{pattern}': {e}")

    if not all_files:
        raise FileError(f"No files found matching patterns: {patterns}")

    # Remove duplicates while preserving order
    seen = set()
    unique_files = []
    for f in all_files:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)

    return unique_files


def get_line_number(file_path: str, json_path: str) -> Optional[int]:
    """Get line number for a JSON path in a file.

    Args:
        file_path: Path to the JSON file
        json_path: JSON path (e.g., "$.properties.name")

    Returns:
        Line number if found, None otherwise

    Note:
        This is a simplified implementation that attempts to map
        JSON paths to line numbers. For complex cases, it may not
        be perfectly accurate.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Simple heuristic: look for property names in the JSON path
        if json_path.startswith('$.'):
            # Extract property names from the path
            parts = json_path[2:].split('.')

            for i, line in enumerate(lines, 1):
                for part in parts:
                    if f'"{part}"' in line:
                        return i

        return None
    except Exception:
        return None


def validate_file_access(file_path: str) -> None:
    """Validate that a file can be accessed for reading.

    Args:
        file_path: Path to validate

    Raises:
        FileError: If file cannot be accessed
    """
    path = Path(file_path)

    if not path.exists():
        raise FileError(f"File not found: {file_path}")

    if not path.is_file():
        raise FileError(f"Path is not a file: {file_path}")

    if not path.stat().st_size:
        raise FileError(f"File is empty: {file_path}")

    try:
        with open(path, 'r', encoding='utf-8'):
            pass
    except PermissionError:
        raise FileError(f"Permission denied reading {file_path}")
    except Exception as e:
        raise FileError(f"Cannot access {file_path}: {e}")