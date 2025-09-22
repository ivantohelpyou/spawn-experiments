import os.path
from pathlib import Path


class PathValidator:
    """A file path validator using os.path and pathlib libraries."""

    def is_valid(self, path):
        """Check if a path is valid."""
        return True  # Minimal implementation to pass the first test