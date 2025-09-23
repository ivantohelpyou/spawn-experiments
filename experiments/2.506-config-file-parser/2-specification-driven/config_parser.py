#!/usr/bin/env python3
"""
Configuration File Parser CLI Tool

A comprehensive tool for parsing, validating, and converting configuration files
across YAML, JSON, INI, and TOML formats.
"""

import json
import configparser
import os
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

import yaml
import toml
import click


class ConfigFormat(Enum):
    """Supported configuration formats."""
    YAML = "yaml"
    JSON = "json"
    INI = "ini"
    TOML = "toml"


@dataclass
class ParseResult:
    """Result of a parsing operation."""
    data: Any
    format: ConfigFormat
    file_path: Optional[str] = None
    errors: Optional[list] = None
    warnings: Optional[list] = None


class ConfigParserError(Exception):
    """Base exception for configuration parser errors."""
    pass


class FormatDetectionError(ConfigParserError):
    """Error in format detection."""
    pass


class ParseError(ConfigParserError):
    """Error in parsing configuration."""
    pass


class ValidationError(ConfigParserError):
    """Error in configuration validation."""
    pass


class ConversionError(ConfigParserError):
    """Error in format conversion."""
    pass


class FormatDetector:
    """Detects configuration file format based on file extension."""

    EXTENSION_MAP = {
        '.yaml': ConfigFormat.YAML,
        '.yml': ConfigFormat.YAML,
        '.json': ConfigFormat.JSON,
        '.ini': ConfigFormat.INI,
        '.cfg': ConfigFormat.INI,
        '.conf': ConfigFormat.INI,
        '.toml': ConfigFormat.TOML,
    }

    @classmethod
    def detect_format(cls, file_path: Union[str, Path]) -> ConfigFormat:
        """
        Detect configuration format from file extension.

        Args:
            file_path: Path to the configuration file

        Returns:
            Detected ConfigFormat

        Raises:
            FormatDetectionError: If format cannot be determined
        """
        path = Path(file_path)
        extension = path.suffix.lower()

        if extension in cls.EXTENSION_MAP:
            return cls.EXTENSION_MAP[extension]

        raise FormatDetectionError(f"Cannot determine format for file: {file_path}")


class BaseParser(ABC):
    """Abstract base class for configuration parsers."""

    @abstractmethod
    def parse(self, file_path: Union[str, Path]) -> Any:
        """Parse configuration file and return data."""
        pass

    @abstractmethod
    def serialize(self, data: Any, **kwargs) -> str:
        """Serialize data to format-specific string."""
        pass

    @abstractmethod
    def get_format(self) -> ConfigFormat:
        """Return the format this parser handles."""
        pass


class YAMLParser(BaseParser):
    """Parser for YAML configuration files."""

    def parse(self, file_path: Union[str, Path]) -> Any:
        """Parse YAML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ParseError(f"YAML parsing error in {file_path}: {e}")
        except (IOError, OSError) as e:
            raise ParseError(f"File error: {e}")

    def serialize(self, data: Any, **kwargs) -> str:
        """Serialize data to YAML string."""
        indent = kwargs.get('indent', 2)
        sort_keys = kwargs.get('sort_keys', False)

        return yaml.dump(
            data,
            default_flow_style=False,
            indent=indent,
            sort_keys=sort_keys,
            allow_unicode=True
        )

    def get_format(self) -> ConfigFormat:
        return ConfigFormat.YAML


class JSONParser(BaseParser):
    """Parser for JSON configuration files."""

    def parse(self, file_path: Union[str, Path]) -> Any:
        """Parse JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ParseError(f"JSON parsing error in {file_path}: {e}")
        except (IOError, OSError) as e:
            raise ParseError(f"File error: {e}")

    def serialize(self, data: Any, **kwargs) -> str:
        """Serialize data to JSON string."""
        indent = kwargs.get('indent', 2)
        sort_keys = kwargs.get('sort_keys', False)

        return json.dumps(
            data,
            indent=indent,
            sort_keys=sort_keys,
            ensure_ascii=False
        )

    def get_format(self) -> ConfigFormat:
        return ConfigFormat.JSON


class INIParser(BaseParser):
    """Parser for INI configuration files."""

    def parse(self, file_path: Union[str, Path]) -> Any:
        """Parse INI file."""
        try:
            parser = configparser.ConfigParser()
            parser.read(file_path, encoding='utf-8')

            # Convert to nested dictionary
            result = {}
            for section_name in parser.sections():
                result[section_name] = dict(parser[section_name])

            return result
        except configparser.Error as e:
            raise ParseError(f"INI parsing error in {file_path}: {e}")
        except (IOError, OSError) as e:
            raise ParseError(f"File error: {e}")

    def serialize(self, data: Any, **kwargs) -> str:
        """Serialize data to INI string."""
        if not isinstance(data, dict):
            raise ConversionError("INI format requires dictionary data")

        parser = configparser.ConfigParser()

        for section_name, section_data in data.items():
            if not isinstance(section_data, dict):
                raise ConversionError(f"INI section '{section_name}' must be a dictionary")

            parser.add_section(section_name)
            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        import io
        output = io.StringIO()
        parser.write(output)
        return output.getvalue()

    def get_format(self) -> ConfigFormat:
        return ConfigFormat.INI


class TOMLParser(BaseParser):
    """Parser for TOML configuration files."""

    def parse(self, file_path: Union[str, Path]) -> Any:
        """Parse TOML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return toml.load(f)
        except toml.TomlDecodeError as e:
            raise ParseError(f"TOML parsing error in {file_path}: {e}")
        except (IOError, OSError) as e:
            raise ParseError(f"File error: {e}")

    def serialize(self, data: Any, **kwargs) -> str:
        """Serialize data to TOML string."""
        if not isinstance(data, dict):
            raise ConversionError("TOML format requires dictionary data")

        return toml.dumps(data)

    def get_format(self) -> ConfigFormat:
        return ConfigFormat.TOML


class ParserRegistry:
    """Registry for configuration parsers."""

    def __init__(self):
        self._parsers = {
            ConfigFormat.YAML: YAMLParser(),
            ConfigFormat.JSON: JSONParser(),
            ConfigFormat.INI: INIParser(),
            ConfigFormat.TOML: TOMLParser(),
        }

    def get_parser(self, format: ConfigFormat) -> BaseParser:
        """Get parser for specified format."""
        if format not in self._parsers:
            raise ConfigParserError(f"No parser available for format: {format}")
        return self._parsers[format]


class ConfigValidator:
    """Validates parsed configuration data."""

    @staticmethod
    def validate_basic(data: Any, format: ConfigFormat) -> Tuple[bool, list]:
        """
        Perform basic validation on parsed data.

        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []

        if data is None:
            errors.append("Configuration data is empty")
            return False, errors

        # Format-specific validation
        if format == ConfigFormat.INI:
            if not isinstance(data, dict):
                errors.append("INI data must be a dictionary")
            else:
                for section_name, section_data in data.items():
                    if not isinstance(section_data, dict):
                        errors.append(f"INI section '{section_name}' must be a dictionary")

        elif format == ConfigFormat.TOML:
            if not isinstance(data, dict):
                errors.append("TOML data must be a dictionary")

        return len(errors) == 0, errors


class FormatConverter:
    """Handles conversion between configuration formats."""

    def __init__(self, registry: ParserRegistry):
        self.registry = registry

    def convert(self, data: Any, source_format: ConfigFormat,
                target_format: ConfigFormat, **kwargs) -> str:
        """
        Convert data from source format to target format.

        Args:
            data: Parsed configuration data
            source_format: Original format
            target_format: Desired format
            **kwargs: Formatting options

        Returns:
            Serialized data in target format
        """
        if source_format == target_format:
            # Same format, just serialize
            parser = self.registry.get_parser(target_format)
            return parser.serialize(data, **kwargs)

        # Handle format-specific conversions
        converted_data = self._convert_data(data, source_format, target_format)

        # Serialize to target format
        target_parser = self.registry.get_parser(target_format)
        return target_parser.serialize(converted_data, **kwargs)

    def _convert_data(self, data: Any, source_format: ConfigFormat,
                     target_format: ConfigFormat) -> Any:
        """Convert data between formats, handling incompatibilities."""

        # INI requires special handling due to limited nesting
        if target_format == ConfigFormat.INI:
            if not isinstance(data, dict):
                raise ConversionError("Cannot convert non-dictionary data to INI format")

            # Flatten nested structures for INI
            flattened = {}
            for key, value in data.items():
                if isinstance(value, dict):
                    flattened[key] = value
                else:
                    # Create a default section for non-dict top-level items
                    if 'DEFAULT' not in flattened:
                        flattened['DEFAULT'] = {}
                    flattened['DEFAULT'][key] = value

            return flattened

        # For other formats, data can generally be passed through
        return data


class ConfigParser:
    """Main configuration parser class."""

    def __init__(self):
        self.registry = ParserRegistry()
        self.converter = FormatConverter(self.registry)
        self.validator = ConfigValidator()

    def parse_file(self, file_path: Union[str, Path],
                   format: Optional[ConfigFormat] = None) -> ParseResult:
        """
        Parse configuration file.

        Args:
            file_path: Path to configuration file
            format: Override auto-detection with specific format

        Returns:
            ParseResult object
        """
        path = Path(file_path)

        if not path.exists():
            raise ParseError(f"File not found: {file_path}")

        # Detect format if not provided
        if format is None:
            format = FormatDetector.detect_format(path)

        # Get appropriate parser
        parser = self.registry.get_parser(format)

        # Parse file
        data = parser.parse(path)

        # Validate
        is_valid, errors = self.validator.validate_basic(data, format)

        return ParseResult(
            data=data,
            format=format,
            file_path=str(path),
            errors=errors if not is_valid else None
        )

    def convert_format(self, source_file: Union[str, Path],
                      target_format: ConfigFormat,
                      output_file: Optional[Union[str, Path]] = None,
                      **formatting_options) -> str:
        """
        Convert configuration file to different format.

        Args:
            source_file: Source configuration file
            target_format: Target format
            output_file: Optional output file path
            **formatting_options: Pretty-printing options

        Returns:
            Converted configuration as string
        """
        # Parse source file
        parse_result = self.parse_file(source_file)

        if parse_result.errors:
            raise ValidationError(f"Source file validation failed: {parse_result.errors}")

        # Convert to target format
        converted = self.converter.convert(
            parse_result.data,
            parse_result.format,
            target_format,
            **formatting_options
        )

        # Write to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(converted)

        return converted


# CLI Implementation
@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--format', 'input_format', type=click.Choice(['yaml', 'json', 'ini', 'toml']),
              help='Override auto-detection of input format')
@click.option('--convert-to', type=click.Choice(['yaml', 'json', 'ini', 'toml']),
              help='Convert to specified format')
@click.option('--output', type=click.Path(),
              help='Output file path (default: stdout)')
@click.option('--validate-only', is_flag=True,
              help='Only validate, do not output content')
@click.option('--indent', type=int, default=2,
              help='Indentation level for pretty-printing')
@click.option('--sort-keys', is_flag=True,
              help='Sort keys in output')
@click.option('--verbose', is_flag=True,
              help='Enable verbose error messages')
def main(file_path, input_format, convert_to, output, validate_only,
         indent, sort_keys, verbose):
    """
    Configuration File Parser CLI Tool

    Parse, validate, and convert configuration files between YAML, JSON, INI, and TOML formats.
    """
    try:
        # Initialize parser
        config_parser = ConfigParser()

        # Convert string format to enum if provided
        format_enum = None
        if input_format:
            format_enum = ConfigFormat(input_format)

        # Parse file
        result = config_parser.parse_file(file_path, format_enum)

        # Handle validation errors
        if result.errors:
            if verbose:
                click.echo(f"Validation errors in {file_path}:", err=True)
                for error in result.errors:
                    click.echo(f"  - {error}", err=True)
            else:
                click.echo(f"Validation failed: {len(result.errors)} error(s)", err=True)
            sys.exit(1)

        # Validation only mode
        if validate_only:
            click.echo(f"✓ {file_path} is valid {result.format.value.upper()}")
            return

        # Format conversion
        if convert_to:
            target_format = ConfigFormat(convert_to)
            converted = config_parser.convert_format(
                file_path,
                target_format,
                output,
                indent=indent,
                sort_keys=sort_keys
            )

            if not output:
                click.echo(converted)
            else:
                click.echo(f"Converted {result.format.value} to {target_format.value}: {output}")

        else:
            # Pretty-print in original format
            parser = config_parser.registry.get_parser(result.format)
            formatted = parser.serialize(
                result.data,
                indent=indent,
                sort_keys=sort_keys
            )

            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(formatted)
                click.echo(f"Output written to: {output}")
            else:
                click.echo(formatted)

    except (ConfigParserError, FormatDetectionError, ParseError,
            ValidationError, ConversionError) as e:
        if verbose:
            import traceback
            click.echo(f"Error: {e}", err=True)
            click.echo(traceback.format_exc(), err=True)
        else:
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()