#!/usr/bin/env python3
"""
Test configuration files and basic functionality test.
"""

import os
import tempfile
import pytest
from config_parser import ConfigParser


def test_json_parsing():
    """Test JSON file parsing."""
    json_content = '''
    {
        "app": {
            "name": "TestApp",
            "version": "1.0.0",
            "debug": true
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        },
        "features": ["auth", "api", "web"]
    }
    '''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write(json_content)
        f.flush()

        parser = ConfigParser()
        data = parser.parse_file(f.name)

        assert data['app']['name'] == 'TestApp'
        assert data['app']['debug'] is True
        assert len(data['features']) == 3
        assert parser.format == 'json'

        os.unlink(f.name)


def test_yaml_parsing():
    """Test YAML file parsing."""
    yaml_content = '''
app:
  name: TestApp
  version: "1.0.0"
  debug: true

database:
  host: localhost
  port: 5432
  name: testdb

features:
  - auth
  - api
  - web
'''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        f.flush()

        parser = ConfigParser()
        data = parser.parse_file(f.name)

        assert data['app']['name'] == 'TestApp'
        assert data['app']['debug'] is True
        assert len(data['features']) == 3
        assert parser.format == 'yaml'

        os.unlink(f.name)


def test_toml_parsing():
    """Test TOML file parsing."""
    toml_content = '''
[app]
name = "TestApp"
version = "1.0.0"
debug = true

[database]
host = "localhost"
port = 5432
name = "testdb"

features = ["auth", "api", "web"]
'''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(toml_content)
        f.flush()

        parser = ConfigParser()
        data = parser.parse_file(f.name)

        assert data['app']['name'] == 'TestApp'
        assert data['app']['debug'] is True
        assert len(data['features']) == 3
        assert parser.format == 'toml'

        os.unlink(f.name)


def test_ini_parsing():
    """Test INI file parsing."""
    ini_content = '''
[app]
name = TestApp
version = 1.0.0
debug = true

[database]
host = localhost
port = 5432
name = testdb
'''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
        f.write(ini_content)
        f.flush()

        parser = ConfigParser()
        data = parser.parse_file(f.name)

        assert data['app']['name'] == 'TestApp'
        assert data['app']['debug'] == 'true'  # INI values are strings
        assert parser.format == 'ini'

        os.unlink(f.name)


def test_format_conversion():
    """Test conversion between formats."""
    # Create JSON data
    json_content = '{"app": {"name": "TestApp", "version": "1.0.0"}, "debug": true}'

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write(json_content)
        f.flush()

        parser = ConfigParser()
        parser.parse_file(f.name)

        # Convert to YAML
        yaml_output = parser.convert_to_format('yaml')
        assert 'app:' in yaml_output
        assert 'name: TestApp' in yaml_output

        # Convert to TOML
        toml_output = parser.convert_to_format('toml')
        assert '[app]' in toml_output
        assert 'name = "TestApp"' in toml_output

        os.unlink(f.name)


if __name__ == '__main__':
    # Run basic functionality tests
    test_json_parsing()
    test_yaml_parsing()
    test_toml_parsing()
    test_ini_parsing()
    test_format_conversion()
    print("✅ All tests passed!")