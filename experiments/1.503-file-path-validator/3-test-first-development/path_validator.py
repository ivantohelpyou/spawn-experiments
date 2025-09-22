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

    def normalize(self, path):
        """Normalize path using os.path.normpath."""
        return os.path.normpath(path)

    def is_valid_pathlib(self, path_obj):
        """Check if a pathlib.Path object is valid."""
        if not isinstance(path_obj, Path):
            return False
        return self.is_valid(str(path_obj))

    def exists_pathlib(self, path_obj):
        """Check if a pathlib.Path object exists."""
        return path_obj.exists()

    def get_parent(self, path):
        """Get parent directory using pathlib."""
        return str(Path(path).parent)

    def get_extension(self, path):
        """Get file extension using pathlib."""
        return Path(path).suffix

    def validate_comprehensive(self, path):
        """Perform comprehensive path validation and return detailed information."""
        result = {
            'is_valid': self.is_valid(path),
            'exists': self.exists(path),
            'is_file': self.is_file(path),
            'is_directory': self.is_directory(path),
            'is_absolute': self.is_absolute(path),
            'is_relative': self.is_relative(path),
            'normalized_path': self.normalize(path),
            'parent': self.get_parent(path),
            'extension': self.get_extension(path)
        }
        return result