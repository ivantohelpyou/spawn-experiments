"""
Configuration file parser that supports YAML, JSON, INI, and TOML formats.
"""

from pathlib import Path


class ConfigParser:
    """A configuration file parser supporting multiple formats."""

    SUPPORTED_FORMATS = {
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.json': 'json',
        '.ini': 'ini',
        '.toml': 'toml'
    }

    def detect_format(self, filepath):
        """
        Detect the configuration format based on file extension.

        Args:
            filepath (str): Path to the configuration file

        Returns:
            str: The detected format ('yaml', 'json', 'ini', 'toml')

        Raises:
            ValueError: If the file extension is not supported
        """
        path = Path(filepath)
        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file extension: {extension}")

        return self.SUPPORTED_FORMATS[extension]