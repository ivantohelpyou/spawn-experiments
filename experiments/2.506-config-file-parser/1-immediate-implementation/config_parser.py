#!/usr/bin/env python3
"""
Configuration File Parser CLI

A CLI tool that supports parsing, validation, and conversion between
YAML, JSON, INI, and TOML configuration file formats.
"""

import json
import configparser
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional

import yaml
import toml
import click


class ConfigParser:
    """Main configuration parser class supporting multiple formats."""

    SUPPORTED_FORMATS = ['json', 'yaml', 'yml', 'ini', 'toml']

    def __init__(self):
        self.data: Optional[Dict[str, Any]] = None
        self.format: Optional[str] = None

    def detect_format(self, file_path: str) -> str:
        """Auto-detect file format based on extension."""
        ext = Path(file_path).suffix.lower().lstrip('.')
        if ext in self.SUPPORTED_FORMATS:
            # Normalize yml to yaml
            return 'yaml' if ext == 'yml' else ext
        raise ValueError(f"Unsupported file format: .{ext}. Supported: {self.SUPPORTED_FORMATS}")

    def parse_file(self, file_path: str, format_override: Optional[str] = None) -> Dict[str, Any]:
        """Parse configuration file and return data."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        # Determine format
        self.format = format_override or self.detect_format(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if self.format == 'json':
                    self.data = json.load(f)
                elif self.format == 'yaml':
                    self.data = yaml.safe_load(f)
                elif self.format == 'toml':
                    self.data = toml.load(f)
                elif self.format == 'ini':
                    parser = configparser.ConfigParser()
                    parser.read(file_path)
                    # Convert ConfigParser to dict
                    self.data = {section: dict(parser[section]) for section in parser.sections()}
                else:
                    raise ValueError(f"Unsupported format: {self.format}")

        except Exception as e:
            raise ValueError(f"Error parsing {self.format.upper()} file: {str(e)}")

        return self.data

    def convert_to_format(self, target_format: str) -> str:
        """Convert loaded data to target format string."""
        if self.data is None:
            raise ValueError("No data loaded. Parse a file first.")

        target_format = target_format.lower()
        if target_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported target format: {target_format}")

        try:
            if target_format == 'json':
                return json.dumps(self.data, indent=2, ensure_ascii=False)
            elif target_format in ['yaml', 'yml']:
                return yaml.dump(self.data, default_flow_style=False, allow_unicode=True)
            elif target_format == 'toml':
                return toml.dumps(self.data)
            elif target_format == 'ini':
                # INI format has limitations with nested data
                if any(isinstance(v, (dict, list)) for v in self.data.values()):
                    raise ValueError("INI format doesn't support nested data structures")

                parser = configparser.ConfigParser()
                for section, values in self.data.items():
                    parser.add_section(str(section))
                    if isinstance(values, dict):
                        for key, value in values.items():
                            parser.set(str(section), str(key), str(value))
                    else:
                        parser.set(str(section), 'value', str(values))

                # Convert to string
                from io import StringIO
                output = StringIO()
                parser.write(output)
                return output.getvalue()
            else:
                raise ValueError(f"Unsupported format: {target_format}")

        except Exception as e:
            raise ValueError(f"Error converting to {target_format.upper()}: {str(e)}")

    def validate_structure(self) -> Dict[str, Any]:
        """Validate and analyze the configuration structure."""
        if self.data is None:
            raise ValueError("No data loaded. Parse a file first.")

        def analyze_value(value, path=""):
            """Recursively analyze configuration values."""
            if isinstance(value, dict):
                return {
                    "type": "object",
                    "keys": list(value.keys()),
                    "nested_count": len([k for k, v in value.items() if isinstance(v, (dict, list))]),
                    "children": {k: analyze_value(v, f"{path}.{k}" if path else k) for k, v in value.items()}
                }
            elif isinstance(value, list):
                return {
                    "type": "array",
                    "length": len(value),
                    "item_types": list(set(type(item).__name__ for item in value))
                }
            else:
                return {"type": type(value).__name__, "value": value}

        return {
            "format": self.format,
            "structure": analyze_value(self.data),
            "total_keys": len(self.data) if isinstance(self.data, dict) else 0,
            "is_valid": True
        }


# CLI Interface
@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Configuration File Parser CLI - Parse, validate, and convert config files."""
    pass


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--format', '-f', help='Override format detection')
@click.option('--pretty', '-p', is_flag=True, help='Pretty print output')
def parse(file_path: str, format: Optional[str], pretty: bool):
    """Parse and display a configuration file."""
    try:
        parser = ConfigParser()
        data = parser.parse_file(file_path, format)

        if pretty:
            click.echo(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            click.echo(json.dumps(data))

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--to', '-t', 'target_format', required=True,
              type=click.Choice(['json', 'yaml', 'yml', 'ini', 'toml'], case_sensitive=False),
              help='Target format for conversion')
@click.option('--force', '-f', is_flag=True, help='Overwrite output file if it exists')
def convert(input_file: str, output_file: str, target_format: str, force: bool):
    """Convert configuration file between formats."""
    try:
        # Check if output file exists
        if os.path.exists(output_file) and not force:
            click.echo(f"Error: Output file '{output_file}' already exists. Use --force to overwrite.", err=True)
            sys.exit(1)

        parser = ConfigParser()
        parser.parse_file(input_file)
        converted_data = parser.convert_to_format(target_format)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(converted_data)

        click.echo(f"Successfully converted {input_file} to {output_file} ({target_format.upper()} format)")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--format', '-f', help='Override format detection')
def validate(file_path: str, format: Optional[str]):
    """Validate configuration file structure."""
    try:
        parser = ConfigParser()
        parser.parse_file(file_path, format)
        validation_result = parser.validate_structure()

        click.echo("✅ Configuration file is valid!")
        click.echo(f"Format: {validation_result['format'].upper()}")
        click.echo(f"Total keys: {validation_result['total_keys']}")

        # Show structure summary
        structure = validation_result['structure']
        if structure['type'] == 'object':
            click.echo(f"Nested objects: {structure['nested_count']}")
            click.echo(f"Top-level keys: {', '.join(structure['keys'][:5])}")
            if len(structure['keys']) > 5:
                click.echo(f"... and {len(structure['keys']) - 5} more")

    except Exception as e:
        click.echo(f"❌ Validation failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--format', '-f', help='Override format detection')
def info(file_path: str, format: Optional[str]):
    """Show detailed information about configuration file."""
    try:
        parser = ConfigParser()
        parser.parse_file(file_path, format)
        validation_result = parser.validate_structure()

        click.echo(f"📄 File: {file_path}")
        click.echo(f"📋 Format: {validation_result['format'].upper()}")
        click.echo(f"🔑 Total keys: {validation_result['total_keys']}")
        click.echo(f"📏 File size: {os.path.getsize(file_path)} bytes")

        # Show detailed structure
        def print_structure(struct, indent=0):
            prefix = "  " * indent
            if struct['type'] == 'object':
                click.echo(f"{prefix}📁 Object ({len(struct['keys'])} keys)")
                for key, child in struct['children'].items():
                    click.echo(f"{prefix}  🔸 {key}:")
                    print_structure(child, indent + 2)
            elif struct['type'] == 'array':
                click.echo(f"{prefix}📋 Array (length: {struct['length']}, types: {', '.join(struct['item_types'])})")
            else:
                value_preview = str(struct['value'])[:50]
                if len(str(struct['value'])) > 50:
                    value_preview += "..."
                click.echo(f"{prefix}🔸 {struct['type']}: {value_preview}")

        click.echo("\n📊 Structure:")
        print_structure(validation_result['structure'])

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()