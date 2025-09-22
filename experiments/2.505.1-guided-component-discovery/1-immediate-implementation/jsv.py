#!/usr/bin/env python3
"""
JSON Schema Validator (JSV) - Command Line Tool

A comprehensive JSON schema validation tool supporting:
- Single file validation
- Batch validation of multiple files
- Pipeline operations (stdin)
- Multiple output formats (text, JSON, CSV)
- Format validation (email, date, URI)
- Progress indicators and colored output
"""

import sys
import json
import argparse
import csv
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
import re
from urllib.parse import urlparse

# Import validation components from utils if available
try:
    sys.path.append('/home/ivan/projects/spawn-experiments')
    from utils.validation import validate_email, validate_date
    from utils.validation.url_validator import URLValidator
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

# Import jsonschema library
try:
    import jsonschema
    from jsonschema import Draft7Validator
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    print("Warning: jsonschema library not found. Install with: pip install jsonschema", file=sys.stderr)

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

@dataclass
class ValidationResult:
    """Result of a single validation operation"""
    file_path: str
    is_valid: bool
    errors: List[str]
    schema_path: Optional[str] = None
    line_numbers: Optional[List[int]] = None

class FormatValidator:
    """Custom format validator leveraging utils components when available"""

    def __init__(self):
        self.url_validator = URLValidator() if UTILS_AVAILABLE else None

    def validate_email(self, value: str) -> bool:
        """Validate email format"""
        if UTILS_AVAILABLE:
            return validate_email(value)
        else:
            # Basic email validation fallback
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, value))

    def validate_date(self, value: str) -> bool:
        """Validate date format"""
        if UTILS_AVAILABLE:
            return validate_date(value)
        else:
            # Basic date validation fallback (ISO format)
            try:
                from datetime import datetime
                datetime.fromisoformat(value.replace('Z', '+00:00'))
                return True
            except (ValueError, AttributeError):
                return False

    def validate_uri(self, value: str) -> bool:
        """Validate URI format"""
        if UTILS_AVAILABLE and self.url_validator:
            return self.url_validator.is_valid(value)
        else:
            # Basic URI validation fallback
            try:
                result = urlparse(value)
                return all([result.scheme, result.netloc])
            except Exception:
                return False

class JSONSchemaValidator:
    """Main JSON Schema Validator class"""

    def __init__(self, quiet: bool = False, use_colors: bool = True):
        self.quiet = quiet
        self.use_colors = use_colors and sys.stdout.isatty()
        self.format_validator = FormatValidator()

        if not JSONSCHEMA_AVAILABLE:
            raise ImportError("jsonschema library is required. Install with: pip install jsonschema")

    def colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled"""
        if self.use_colors:
            return f"{color}{text}{Colors.END}"
        return text

    def load_json_file(self, file_path: str) -> Dict[str, Any]:
        """Load and parse JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Error reading {file_path}: {e}")

    def load_schema(self, schema_path: str) -> Dict[str, Any]:
        """Load JSON schema file"""
        schema = self.load_json_file(schema_path)

        # Validate that the schema itself is valid
        try:
            Draft7Validator.check_schema(schema)
        except jsonschema.SchemaError as e:
            raise ValueError(f"Invalid schema in {schema_path}: {e}")

        return schema

    def validate_format(self, format_name: str, value: str) -> bool:
        """Validate format using custom format validators"""
        if format_name == "email":
            return self.format_validator.validate_email(value)
        elif format_name == "date":
            return self.format_validator.validate_date(value)
        elif format_name == "uri":
            return self.format_validator.validate_uri(value)
        else:
            # For other formats, rely on jsonschema's built-in validators
            return True

    def validate_json(self, data: Dict[str, Any], schema: Dict[str, Any], file_path: str = "data") -> ValidationResult:
        """Validate JSON data against schema"""
        errors = []

        try:
            # Create validator with custom format checker
            format_checker = jsonschema.FormatChecker()

            # Add custom format validators
            format_checker.checks('email')(lambda instance: self.format_validator.validate_email(instance))
            format_checker.checks('date')(lambda instance: self.format_validator.validate_date(instance))
            format_checker.checks('uri')(lambda instance: self.format_validator.validate_uri(instance))

            validator = Draft7Validator(schema, format_checker=format_checker)

            # Collect all validation errors
            validation_errors = list(validator.iter_errors(data))

            for error in validation_errors:
                # Build error message with path information
                path = " -> ".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
                errors.append(f"Path '{path}': {error.message}")

            return ValidationResult(
                file_path=file_path,
                is_valid=len(errors) == 0,
                errors=errors
            )

        except Exception as e:
            errors.append(f"Validation error: {e}")
            return ValidationResult(
                file_path=file_path,
                is_valid=False,
                errors=errors
            )

    def validate_file(self, file_path: str, schema: Dict[str, Any]) -> ValidationResult:
        """Validate a single JSON file"""
        try:
            data = self.load_json_file(file_path)
            result = self.validate_json(data, schema, file_path)
            result.schema_path = getattr(schema, 'path', None)
            return result
        except Exception as e:
            return ValidationResult(
                file_path=file_path,
                is_valid=False,
                errors=[str(e)]
            )

    def validate_batch(self, file_patterns: List[str], schema: Dict[str, Any], show_progress: bool = True) -> List[ValidationResult]:
        """Validate multiple files matching the given patterns"""
        files = []
        for pattern in file_patterns:
            files.extend(glob.glob(pattern))

        if not files:
            return []

        results = []
        total_files = len(files)

        for i, file_path in enumerate(files):
            if show_progress and not self.quiet:
                progress = f"({i+1}/{total_files})"
                print(f"Validating {progress} {file_path}...", end='\r', file=sys.stderr)

            result = self.validate_file(file_path, schema)
            results.append(result)

        if show_progress and not self.quiet:
            print(" " * 80, end='\r', file=sys.stderr)  # Clear progress line

        return results

    def check_schema(self, schema_path: str) -> ValidationResult:
        """Check if a schema file is valid"""
        try:
            schema = self.load_schema(schema_path)
            return ValidationResult(
                file_path=schema_path,
                is_valid=True,
                errors=[]
            )
        except Exception as e:
            return ValidationResult(
                file_path=schema_path,
                is_valid=False,
                errors=[str(e)]
            )

class OutputFormatter:
    """Handle different output formats"""

    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors and sys.stdout.isatty()

    def colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled"""
        if self.use_colors:
            return f"{color}{text}{Colors.END}"
        return text

    def format_text(self, results: List[ValidationResult]) -> str:
        """Format results as human-readable text"""
        output = []

        valid_count = sum(1 for r in results if r.is_valid)
        total_count = len(results)

        # Summary
        if total_count > 1:
            summary = f"Validation Summary: {valid_count}/{total_count} files valid"
            if valid_count == total_count:
                output.append(self.colorize(summary, Colors.GREEN))
            else:
                output.append(self.colorize(summary, Colors.RED))
            output.append("")

        # Individual results
        for result in results:
            if result.is_valid:
                status = self.colorize("✓ VALID", Colors.GREEN)
                output.append(f"{status}: {result.file_path}")
            else:
                status = self.colorize("✗ INVALID", Colors.RED)
                output.append(f"{status}: {result.file_path}")
                for error in result.errors:
                    output.append(f"  • {self.colorize(error, Colors.YELLOW)}")
                output.append("")

        return "\n".join(output)

    def format_json(self, results: List[ValidationResult]) -> str:
        """Format results as JSON"""
        output = {
            "summary": {
                "total_files": len(results),
                "valid_files": sum(1 for r in results if r.is_valid),
                "invalid_files": sum(1 for r in results if not r.is_valid)
            },
            "results": []
        }

        for result in results:
            output["results"].append({
                "file_path": result.file_path,
                "is_valid": result.is_valid,
                "errors": result.errors,
                "schema_path": result.schema_path
            })

        return json.dumps(output, indent=2)

    def format_csv(self, results: List[ValidationResult]) -> str:
        """Format results as CSV"""
        import io
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(["file_path", "is_valid", "error_count", "errors"])

        # Data rows
        for result in results:
            writer.writerow([
                result.file_path,
                result.is_valid,
                len(result.errors),
                "; ".join(result.errors) if result.errors else ""
            ])

        return output.getvalue()

def read_stdin() -> str:
    """Read JSON data from stdin"""
    if sys.stdin.isatty():
        raise ValueError("No input provided via stdin")
    return sys.stdin.read()

def main():
    parser = argparse.ArgumentParser(
        description="JSON Schema Validator - Validate JSON files against JSON Schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate single file
  jsv validate data.json --schema=schema.json

  # Batch validation
  jsv batch *.json --schema=schema.json --output=csv

  # Pipeline validation
  cat data.json | jsv validate --schema=schema.json

  # Schema verification
  jsv check schema.json
        """
    )

    parser.add_argument('--version', action='version', version='JSV 1.0.0')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode - only return exit codes')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a single JSON file')
    validate_parser.add_argument('file', nargs='?', help='JSON file to validate (use - for stdin)')
    validate_parser.add_argument('--schema', '-s', required=True, help='JSON schema file')
    validate_parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text', help='Output format')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Validate multiple JSON files')
    batch_parser.add_argument('files', nargs='+', help='JSON files or patterns to validate')
    batch_parser.add_argument('--schema', '-s', required=True, help='JSON schema file')
    batch_parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text', help='Output format')
    batch_parser.add_argument('--no-progress', action='store_true', help='Disable progress indicators')

    # Check command
    check_parser = subparsers.add_parser('check', help='Check if a JSON schema is valid')
    check_parser.add_argument('schema', help='JSON schema file to check')
    check_parser.add_argument('--output', '-o', choices=['text', 'json'], default='text', help='Output format')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        validator = JSONSchemaValidator(quiet=args.quiet, use_colors=not args.no_color)
        formatter = OutputFormatter(use_colors=not args.no_color)

        if args.command == 'validate':
            # Load schema
            schema = validator.load_schema(args.schema)

            if args.file == '-' or args.file is None:
                # Read from stdin
                try:
                    json_data = json.loads(read_stdin())
                    result = validator.validate_json(json_data, schema, "stdin")
                    results = [result]
                except Exception as e:
                    if not args.quiet:
                        print(f"Error reading from stdin: {e}", file=sys.stderr)
                    return 1
            else:
                # Validate single file
                result = validator.validate_file(args.file, schema)
                results = [result]

        elif args.command == 'batch':
            # Load schema
            schema = validator.load_schema(args.schema)

            # Validate multiple files
            show_progress = not args.no_progress
            results = validator.validate_batch(args.files, schema, show_progress)

            if not results:
                if not args.quiet:
                    print("No files found matching the given patterns", file=sys.stderr)
                return 1

        elif args.command == 'check':
            # Check schema validity
            result = validator.check_schema(args.schema)
            results = [result]

        # Format and output results
        if not args.quiet:
            if args.output == 'json':
                print(formatter.format_json(results))
            elif args.output == 'csv':
                print(formatter.format_csv(results))
            else:
                print(formatter.format_text(results))

        # Return appropriate exit code
        if all(r.is_valid for r in results):
            return 0
        else:
            return 1

    except Exception as e:
        if not args.quiet:
            print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())