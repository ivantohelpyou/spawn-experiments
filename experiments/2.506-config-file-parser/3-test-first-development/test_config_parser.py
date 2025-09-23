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


    def test_parse_yaml_file(self):
        """Test parsing a valid YAML file."""
        yaml_content = """
database:
  host: localhost
  port: 5432
  credentials:
    username: admin
    password: secret
app:
  name: myapp
  debug: true
"""
        # Create temporary YAML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            yaml_file = f.name

        try:
            result = self.parser.parse_file(yaml_file)

            # Verify structure
            self.assertIn('database', result)
            self.assertIn('app', result)
            self.assertEqual(result['database']['host'], 'localhost')
            self.assertEqual(result['database']['port'], 5432)
            self.assertEqual(result['database']['credentials']['username'], 'admin')
            self.assertEqual(result['app']['name'], 'myapp')
            self.assertTrue(result['app']['debug'])
        finally:
            os.unlink(yaml_file)

    def test_parse_json_file(self):
        """Test parsing a valid JSON file."""
        json_content = """{
    "database": {
        "host": "localhost",
        "port": 5432,
        "credentials": {
            "username": "admin",
            "password": "secret"
        }
    },
    "app": {
        "name": "myapp",
        "debug": true
    }
}"""
        # Create temporary JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(json_content)
            json_file = f.name

        try:
            result = self.parser.parse_file(json_file)

            # Verify structure
            self.assertIn('database', result)
            self.assertIn('app', result)
            self.assertEqual(result['database']['host'], 'localhost')
            self.assertEqual(result['database']['port'], 5432)
            self.assertEqual(result['database']['credentials']['username'], 'admin')
            self.assertEqual(result['app']['name'], 'myapp')
            self.assertTrue(result['app']['debug'])
        finally:
            os.unlink(json_file)

    def test_parse_ini_file(self):
        """Test parsing a valid INI file."""
        ini_content = """[database]
host = localhost
port = 5432

[database.credentials]
username = admin
password = secret

[app]
name = myapp
debug = true
"""
        # Create temporary INI file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write(ini_content)
            ini_file = f.name

        try:
            result = self.parser.parse_file(ini_file)

            # Verify structure (INI files are flatter)
            self.assertIn('database', result)
            self.assertIn('app', result)
            self.assertEqual(result['database']['host'], 'localhost')
            self.assertEqual(result['database']['port'], '5432')  # INI values are strings
            self.assertEqual(result['app']['name'], 'myapp')
            self.assertEqual(result['app']['debug'], 'true')  # INI values are strings
        finally:
            os.unlink(ini_file)

    def test_parse_toml_file(self):
        """Test parsing a valid TOML file."""
        toml_content = """[database]
host = "localhost"
port = 5432

[database.credentials]
username = "admin"
password = "secret"

[app]
name = "myapp"
debug = true
"""
        # Create temporary TOML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(toml_content)
            toml_file = f.name

        try:
            result = self.parser.parse_file(toml_file)

            # Verify structure
            self.assertIn('database', result)
            self.assertIn('app', result)
            self.assertEqual(result['database']['host'], 'localhost')
            self.assertEqual(result['database']['port'], 5432)
            self.assertEqual(result['database']['credentials']['username'], 'admin')
            self.assertEqual(result['app']['name'], 'myapp')
            self.assertTrue(result['app']['debug'])
        finally:
            os.unlink(toml_file)


if __name__ == '__main__':
    unittest.main()