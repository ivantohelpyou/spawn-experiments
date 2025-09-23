#!/usr/bin/env python3
"""
Configuration File Parser CLI
Supports YAML, JSON, INI, and TOML formats with auto-detection and conversion.
"""

import json
import configparser
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union
from enum import Enum

import yaml
import toml
import click
from pydantic import BaseModel, ValidationError


class ConfigFormat(Enum):
    """Supported configuration formats."""
    JSON = "json"
    YAML = "yaml"
    INI = "ini"
    TOML = "toml"


class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""
    pass


class ConfigParser:
    """Main configuration parser with format detection and conversion capabilities."""

    def __init__(self):
        self.format_parsers = {
            ConfigFormat.JSON: self._parse_json,
            ConfigFormat.YAML: self._parse_yaml,
            ConfigFormat.INI: self._parse_ini,
            ConfigFormat.TOML: self._parse_toml,
        }

        self.format_writers = {
            ConfigFormat.JSON: self._write_json,
            ConfigFormat.YAML: self._write_yaml,
            ConfigFormat.INI: self._write_ini,
            ConfigFormat.TOML: self._write_toml,
        }

    def detect_format(self, file_path: Union[str, Path]) -> ConfigFormat:
        """
        Auto-detect configuration format based on file extension.

        Args:
            file_path: Path to the configuration file

        Returns:
            Detected configuration format

        Raises:
            ConfigValidationError: If format cannot be detected
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()

        format_mapping = {
            '.json': ConfigFormat.JSON,
            '.yaml': ConfigFormat.YAML,
            '.yml': ConfigFormat.YAML,
            '.ini': ConfigFormat.INI,
            '.cfg': ConfigFormat.INI,
            '.toml': ConfigFormat.TOML,
        }

        if extension in format_mapping:
            return format_mapping[extension]

        # Fallback: try to detect by content
        return self._detect_format_by_content(file_path)

    def _detect_format_by_content(self, file_path: Path) -> ConfigFormat:
        """
        Attempt to detect format by analyzing file content.

        Args:
            file_path: Path to the configuration file

        Returns:
            Detected configuration format

        Raises:
            ConfigValidationError: If format cannot be detected
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
        except Exception as e:
            raise ConfigValidationError(f"Cannot read file {file_path}: {e}")

        # Try parsing with each format
        for fmt in ConfigFormat:
            try:
                self.format_parsers[fmt](content)
                return fmt
            except:
                continue

        raise ConfigValidationError(f"Cannot detect format for file: {file_path}")

    def parse_file(self, file_path: Union[str, Path], format_hint: Optional[ConfigFormat] = None) -> Dict[str, Any]:
        """
        Parse configuration file with optional format hint.

        Args:
            file_path: Path to the configuration file
            format_hint: Optional format hint to override auto-detection

        Returns:
            Parsed configuration as dictionary

        Raises:
            ConfigValidationError: If parsing fails
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise ConfigValidationError(f"File not found: {file_path}")

        # Detect format if not provided
        config_format = format_hint or self.detect_format(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return self.format_parsers[config_format](content)

        except Exception as e:
            raise ConfigValidationError(f"Failed to parse {config_format.value} file {file_path}: {e}")

    def convert_format(self, input_path: Union[str, Path], output_path: Union[str, Path],
                      target_format: ConfigFormat, source_format: Optional[ConfigFormat] = None) -> None:
        """
        Convert configuration file from one format to another.

        Args:
            input_path: Source file path
            output_path: Target file path
            target_format: Target configuration format
            source_format: Optional source format hint

        Raises:
            ConfigValidationError: If conversion fails
        """
        # Parse source file
        config_data = self.parse_file(input_path, source_format)

        # Write in target format
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            content = self.format_writers[target_format](config_data)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise ConfigValidationError(f"Failed to write {target_format.value} file {output_path}: {e}")

    def pretty_print(self, config_data: Dict[str, Any], format_type: ConfigFormat) -> str:
        """
        Pretty-print configuration data in specified format.

        Args:
            config_data: Configuration data dictionary
            format_type: Target format for pretty-printing

        Returns:
            Formatted configuration string
        """
        return self.format_writers[format_type](config_data)

    # Format-specific parsing methods
    def _parse_json(self, content: str) -> Dict[str, Any]:
        """Parse JSON content."""
        return json.loads(content)

    def _parse_yaml(self, content: str) -> Dict[str, Any]:
        """Parse YAML content."""
        return yaml.safe_load(content) or {}

    def _parse_ini(self, content: str) -> Dict[str, Any]:
        """Parse INI content."""
        parser = configparser.ConfigParser()
        parser.read_string(content)

        result = {}
        for section_name in parser.sections():
            result[section_name] = dict(parser[section_name])

        # Handle files without sections
        if parser.defaults():
            result['DEFAULT'] = dict(parser.defaults())

        return result

    def _parse_toml(self, content: str) -> Dict[str, Any]:
        """Parse TOML content."""
        return toml.loads(content)

    # Format-specific writing methods
    def _write_json(self, data: Dict[str, Any]) -> str:
        """Write data as JSON."""
        return json.dumps(data, indent=2, ensure_ascii=False)

    def _write_yaml(self, data: Dict[str, Any]) -> str:
        """Write data as YAML."""
        return yaml.dump(data, default_flow_style=False, allow_unicode=True, indent=2)

    def _write_ini(self, data: Dict[str, Any]) -> str:
        """Write data as INI."""
        parser = configparser.ConfigParser()

        for section_name, section_data in data.items():
            if isinstance(section_data, dict):
                parser.add_section(section_name)
                for key, value in section_data.items():
                    parser.set(section_name, key, str(value))

        import io
        output = io.StringIO()
        parser.write(output)
        return output.getvalue()

    def _write_toml(self, data: Dict[str, Any]) -> str:
        """Write data as TOML."""
        return toml.dumps(data)


# CLI Interface
@click.group()
@click.version_option()
def cli():
    """Configuration file parser and converter supporting YAML, JSON, INI, and TOML formats."""
    pass


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--format', 'format_hint', type=click.Choice(['json', 'yaml', 'ini', 'toml']),
              help='Override format auto-detection')
@click.option('--pretty', is_flag=True, help='Pretty-print output')
def parse(file_path, format_hint, pretty):
    """Parse and display configuration file."""
    parser = ConfigParser()

    try:
        format_enum = ConfigFormat(format_hint) if format_hint else None
        config_data = parser.parse_file(file_path, format_enum)

        if pretty:
            detected_format = format_enum or parser.detect_format(file_path)
            output = parser.pretty_print(config_data, detected_format)
            click.echo(output)
        else:
            click.echo(json.dumps(config_data, indent=2))

    except ConfigValidationError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.ClickException(str(e))


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--to', 'target_format', required=True,
              type=click.Choice(['json', 'yaml', 'ini', 'toml']),
              help='Target format for conversion')
@click.option('--from', 'source_format',
              type=click.Choice(['json', 'yaml', 'ini', 'toml']),
              help='Source format (auto-detected if not specified)')
def convert(input_file, output_file, target_format, source_format):
    """Convert configuration file between formats."""
    parser = ConfigParser()

    try:
        source_enum = ConfigFormat(source_format) if source_format else None
        target_enum = ConfigFormat(target_format)

        parser.convert_format(input_file, output_file, target_enum, source_enum)
        click.echo(f"Successfully converted {input_file} to {output_file} ({target_format})")

    except ConfigValidationError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.ClickException(str(e))


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def validate(file_path):
    """Validate configuration file structure and format."""
    parser = ConfigParser()

    try:
        detected_format = parser.detect_format(file_path)
        config_data = parser.parse_file(file_path)

        click.echo(f"✓ File format: {detected_format.value}")
        click.echo(f"✓ Structure: Valid")
        click.echo(f"✓ Sections: {len(config_data)}")

        # Show basic structure info
        for key, value in config_data.items():
            if isinstance(value, dict):
                click.echo(f"  - {key}: {len(value)} items")
            else:
                click.echo(f"  - {key}: {type(value).__name__}")

    except ConfigValidationError as e:
        click.echo(f"✗ Validation failed: {e}", err=True)
        raise click.ClickException(str(e))


if __name__ == '__main__':
    cli()