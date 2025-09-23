import unittest
import tempfile
import os
from pathlib import Path

# Import our module that doesn't exist yet - this will fail initially
from config_parser import ConfigParser


class TestConfigParser(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.parser = ConfigParser()

    def test_detect_yaml_format_from_extension(self):
        """Test that YAML format is detected from .yaml extension."""
        result = self.parser.detect_format("config.yaml")
        self.assertEqual(result, "yaml")

    def test_detect_yaml_format_from_yml_extension(self):
        """Test that YAML format is detected from .yml extension."""
        result = self.parser.detect_format("config.yml")
        self.assertEqual(result, "yaml")

    def test_detect_json_format_from_extension(self):
        """Test that JSON format is detected from .json extension."""
        result = self.parser.detect_format("config.json")
        self.assertEqual(result, "json")

    def test_detect_ini_format_from_extension(self):
        """Test that INI format is detected from .ini extension."""
        result = self.parser.detect_format("config.ini")
        self.assertEqual(result, "ini")

    def test_detect_toml_format_from_extension(self):
        """Test that TOML format is detected from .toml extension."""
        result = self.parser.detect_format("config.toml")
        self.assertEqual(result, "toml")

    def test_detect_format_raises_error_for_unsupported_extension(self):
        """Test that unsupported file extensions raise an error."""
        with self.assertRaises(ValueError):
            self.parser.detect_format("config.txt")


if __name__ == '__main__':
    unittest.main()