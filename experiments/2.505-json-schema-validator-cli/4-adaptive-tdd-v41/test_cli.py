#!/usr/bin/env python3
"""
Tests for JSON Schema Validator CLI functionality.
"""

import json
import tempfile
import unittest
import subprocess
import sys
import os
from pathlib import Path

# Add the current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestCLI(unittest.TestCase):
    """Test the CLI interface functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = Path(__file__).parent / "test_data"
        self.schema_file = self.test_dir / "schema.json"
        self.valid_file = self.test_dir / "valid_person.json"
        self.invalid_file = self.test_dir / "invalid_person.json"
        self.minimal_valid_file = self.test_dir / "minimal_valid.json"
        self.invalid_json_file = self.test_dir / "invalid_json.json"

    def run_jsv(self, args, input_data=None):
        """Run the jsv CLI tool and return result."""
        cmd = [sys.executable, "jsv.py"] + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            input=input_data,
            cwd=Path(__file__).parent
        )
        return result

    def test_help(self):
        """Test help output."""
        result = self.run_jsv(["--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("JSON Schema Validator", result.stdout)
        self.assertIn("validate", result.stdout)
        self.assertIn("batch", result.stdout)
        self.assertIn("check", result.stdout)

    def test_validate_valid_file(self):
        """Test validating a valid file."""
        result = self.run_jsv([
            "validate", str(self.valid_file),
            f"--schema={self.schema_file}"
        ])
        self.assertEqual(result.returncode, 0)
        self.assertIn("✓ VALID", result.stdout)

    def test_validate_invalid_file(self):
        """Test validating an invalid file."""
        result = self.run_jsv([
            "validate", str(self.invalid_file),
            f"--schema={self.schema_file}"
        ])
        self.assertEqual(result.returncode, 1)
        self.assertIn("✗ INVALID", result.stdout)
        self.assertIn("Error:", result.stdout)

    def test_validate_from_stdin(self):
        """Test validating from stdin."""
        valid_data = '{"name": "Test User", "age": 25}'
        result = self.run_jsv([
            "validate", f"--schema={self.schema_file}"
        ], input_data=valid_data)
        self.assertEqual(result.returncode, 0)
        self.assertIn("✓ VALID", result.stdout)

    def test_validate_invalid_stdin(self):
        """Test validating invalid data from stdin."""
        invalid_data = '{"age": -1}'
        result = self.run_jsv([
            "validate", f"--schema={self.schema_file}"
        ], input_data=invalid_data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("✗ INVALID", result.stdout)

    def test_validate_json_output(self):
        """Test JSON output format."""
        result = self.run_jsv([
            "validate", str(self.valid_file),
            f"--schema={self.schema_file}",
            "--output=json"
        ])
        self.assertEqual(result.returncode, 0)
        output_data = json.loads(result.stdout)
        self.assertTrue(output_data["valid"])
        self.assertEqual(len(output_data["errors"]), 0)

    def test_validate_quiet_mode(self):
        """Test quiet mode."""
        # Valid file should return 0 with no output
        result = self.run_jsv([
            "validate", str(self.valid_file),
            f"--schema={self.schema_file}",
            "--quiet"
        ])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "")

        # Invalid file should return 1 with no output
        result = self.run_jsv([
            "validate", str(self.invalid_file),
            f"--schema={self.schema_file}",
            "--quiet"
        ])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.strip(), "")

    def test_batch_validation(self):
        """Test batch validation."""
        result = self.run_jsv([
            "batch", str(self.valid_file), str(self.invalid_file),
            f"--schema={self.schema_file}"
        ])
        self.assertEqual(result.returncode, 1)  # Mixed results
        self.assertIn("Validation Summary", result.stdout)
        self.assertIn("✓ VALID", result.stdout)
        self.assertIn("✗ INVALID", result.stdout)

    def test_batch_csv_output(self):
        """Test batch validation with CSV output."""
        result = self.run_jsv([
            "batch", str(self.valid_file), str(self.invalid_file),
            f"--schema={self.schema_file}",
            "--output=csv"
        ])
        self.assertEqual(result.returncode, 1)
        self.assertIn("file,valid,error_count,errors", result.stdout)
        self.assertIn("True", result.stdout)
        self.assertIn("False", result.stdout)

    def test_check_schema(self):
        """Test schema validation."""
        result = self.run_jsv(["check", str(self.schema_file)])
        self.assertEqual(result.returncode, 0)
        self.assertIn("✓ VALID", result.stdout)

    def test_check_invalid_schema(self):
        """Test checking an invalid schema."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"type": "invalid_type"}, f)
            f.flush()

            result = self.run_jsv(["check", f.name])
            self.assertEqual(result.returncode, 1)
            self.assertIn("✗ INVALID", result.stdout)

            # Clean up
            os.unlink(f.name)

    def test_missing_schema_file(self):
        """Test with missing schema file."""
        result = self.run_jsv([
            "validate", str(self.valid_file),
            "--schema=/nonexistent/schema.json"
        ])
        self.assertEqual(result.returncode, 1)
        self.assertIn("Error loading schema", result.stderr)

    def test_missing_input_file(self):
        """Test with missing input file."""
        result = self.run_jsv([
            "validate", "/nonexistent/file.json",
            f"--schema={self.schema_file}"
        ])
        self.assertEqual(result.returncode, 1)
        self.assertIn("File not found", result.stdout)

    def test_invalid_json_file(self):
        """Test with invalid JSON file."""
        result = self.run_jsv([
            "validate", str(self.invalid_json_file),
            f"--schema={self.schema_file}"
        ])
        self.assertEqual(result.returncode, 1)
        self.assertIn("JSON parse error", result.stdout)


if __name__ == '__main__':
    unittest.main()