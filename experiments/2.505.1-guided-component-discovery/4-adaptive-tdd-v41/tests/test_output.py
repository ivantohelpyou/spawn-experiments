"""
Tests for output formatting functionality.
Tests different output formats: text, JSON, CSV.
"""

import pytest
import json
from jsv.output import OutputFormatter
from jsv.validator import ValidationError


class TestOutputFormatter:
    """Test cases for output formatting."""

    def setup_method(self):
        """Set up test fixtures."""
        self.formatter = OutputFormatter()

        # Sample validation results
        self.valid_result = {
            'valid': True,
            'file': 'test.json',
            'errors': []
        }

        self.invalid_result = {
            'valid': False,
            'file': 'invalid.json',
            'errors': [
                ValidationError("Required property 'name' is missing", "name"),
                ValidationError("Expected integer, got string", "age")
            ]
        }

        self.batch_results = [
            {
                'valid': True,
                'file': 'file1.json',
                'errors': []
            },
            {
                'valid': False,
                'file': 'file2.json',
                'errors': [ValidationError("Invalid email format", "email")]
            },
            {
                'valid': True,
                'file': 'file3.json',
                'errors': []
            }
        ]

    def test_format_single_result_text_valid(self):
        """Test text formatting for valid result."""
        output = self.formatter.format_single_result(self.valid_result, 'text')
        assert "test.json" in output
        assert "Valid" in output or "✓" in output

    def test_format_single_result_text_invalid(self):
        """Test text formatting for invalid result."""
        output = self.formatter.format_single_result(self.invalid_result, 'text')
        assert "invalid.json" in output
        assert "Invalid" in output or "✗" in output
        assert "name" in output
        assert "age" in output

    def test_format_single_result_json_valid(self):
        """Test JSON formatting for valid result."""
        output = self.formatter.format_single_result(self.valid_result, 'json')
        data = json.loads(output)
        assert data['valid'] == True
        assert data['file'] == 'test.json'
        assert data['errors'] == []

    def test_format_single_result_json_invalid(self):
        """Test JSON formatting for invalid result."""
        output = self.formatter.format_single_result(self.invalid_result, 'json')
        data = json.loads(output)
        assert data['valid'] == False
        assert data['file'] == 'invalid.json'
        assert len(data['errors']) == 2

    def test_format_batch_results_text(self):
        """Test text formatting for batch results."""
        output = self.formatter.format_batch_results(self.batch_results, 'text')
        assert "file1.json" in output
        assert "file2.json" in output
        assert "file3.json" in output
        assert "2/3" in output or "Summary" in output

    def test_format_batch_results_json(self):
        """Test JSON formatting for batch results."""
        output = self.formatter.format_batch_results(self.batch_results, 'json')
        data = json.loads(output)
        assert len(data) == 3
        assert data[0]['valid'] == True
        assert data[1]['valid'] == False
        assert data[2]['valid'] == True

    def test_format_batch_results_csv(self):
        """Test CSV formatting for batch results."""
        output = self.formatter.format_batch_results(self.batch_results, 'csv')
        lines = output.strip().split('\n')
        assert len(lines) == 4  # Header + 3 data rows
        assert "file" in lines[0].lower()
        assert "valid" in lines[0].lower()
        assert "file1.json" in lines[1]
        assert "file2.json" in lines[2]
        assert "file3.json" in lines[3]

    def test_colored_output_enabled(self):
        """Test colored output when enabled."""
        formatter = OutputFormatter(colored=True)
        output = formatter.format_single_result(self.valid_result, 'text')
        # Should contain ANSI escape codes for colors
        assert '\033[' in output or 'test.json' in output

    def test_colored_output_disabled(self):
        """Test colored output when disabled."""
        formatter = OutputFormatter(colored=False)
        output = formatter.format_single_result(self.valid_result, 'text')
        # Should not contain ANSI escape codes
        assert '\033[' not in output

    def test_format_errors_list(self):
        """Test formatting of error list."""
        errors = [
            ValidationError("Required property 'name' is missing", "name"),
            ValidationError("Expected integer, got string", "age")
        ]
        formatted = self.formatter._format_errors(errors)
        assert "name" in formatted
        assert "age" in formatted

    def test_format_unknown_output_type(self):
        """Test handling of unknown output format."""
        # Should fall back to text format
        output = self.formatter.format_single_result(self.valid_result, 'unknown')
        assert isinstance(output, str)
        assert "test.json" in output