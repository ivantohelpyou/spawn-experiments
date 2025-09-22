import os.path
from pathlib import Path


class PathValidator:
    """A file path validator using os.path and pathlib libraries."""

    def is_valid(self, path):
        """Check if a path is valid."""
        if path is None or path == "":
            return False
        return True

    def is_absolute(self, path):
        """Check if a path is absolute using os.path."""
        return os.path.isabs(path)

    def is_relative(self, path):
        """Check if a path is relative."""
        return not os.path.isabs(path)