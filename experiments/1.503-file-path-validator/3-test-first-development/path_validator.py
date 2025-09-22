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

    def exists(self, path):
        """Check if a path exists using os.path."""
        return os.path.exists(path)

    def is_file(self, path):
        """Check if a path is a file using os.path."""
        return os.path.isfile(path)

    def is_directory(self, path):
        """Check if a path is a directory using os.path."""
        return os.path.isdir(path)