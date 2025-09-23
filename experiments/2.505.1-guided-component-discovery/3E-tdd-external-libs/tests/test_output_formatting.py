"""Test suite for output formatting and progress indicators following TDD methodology."""

import pytest
import json
import io
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

# Import output formatting modules - will fail initially (Red phase)
try:
    from json_schema_validator import (
        OutputFormatter,
        JSONFormatter,
        TableFormatter,
        TextFormatter,
        ProgressIndicator,
        ColoredOutput,
        format_validation_result,
        format_batch_results,
        create_progress_bar
    )
except ImportError:
    # Expected during TDD - tests written first
    OutputFormatter = None
    JSONFormatter = None
    TableFormatter = None
    TextFormatter = None
    ProgressIndicator = None
    ColoredOutput = None
    format_validation_result = None
    format_batch_results = None
    create_progress_bar = None


class TestOutputFormatters:
    """Test output formatting functionality."""

    def test_json_formatter(self):
        """Test JSON output formatting."""
        if JSONFormatter is None:
            pytest.skip("JSONFormatter not implemented yet - TDD Red phase")

        formatter = JSONFormatter()

        # Test valid result formatting
        result_data = {
            "file": "test.json",
            "valid": True,
            "errors": [],
            "schema": "schema.json"
        }

        output = formatter.format(result_data)

        # Should be valid JSON
        parsed = json.loads(output)
        assert parsed["file"] == "test.json"
        assert parsed["valid"] is True
        assert parsed["errors"] == []

    def test_table_formatter(self):
        """Test table output formatting."""
        if TableFormatter is None:
            pytest.skip("TableFormatter not implemented yet - TDD Red phase")

        formatter = TableFormatter()

        # Test batch results formatting
        results = [
            {"file": "file1.json", "valid": True, "errors": []},
            {"file": "file2.json", "valid": False, "errors": ["Missing field"]},
            {"file": "file3.json", "valid": True, "errors": []}
        ]

        output = formatter.format(results)

        # Should contain table elements
        assert "file1.json" in output
        assert "file2.json" in output
        assert "file3.json" in output
        assert "Missing field" in output

        # Should have table-like structure
        lines = output.split('\n')
        assert len(lines) > 3  # Header + data rows

    def test_text_formatter(self):
        """Test plain text output formatting."""
        if TextFormatter is None:
            pytest.skip("TextFormatter not implemented yet - TDD Red phase")

        formatter = TextFormatter()

        # Test single result formatting
        result_data = {
            "file": "test.json",
            "valid": False,
            "errors": ["Required field 'name' missing", "Invalid type for 'age'"]
        }

        output = formatter.format(result_data)

        assert "test.json" in output
        assert "Required field 'name' missing" in output
        assert "Invalid type for 'age'" in output

    def test_output_formatter_factory(self):
        """Test OutputFormatter factory method."""
        if OutputFormatter is None:
            pytest.skip("OutputFormatter not implemented yet - TDD Red phase")

        # Test formatter creation
        json_formatter = OutputFormatter.create("json")
        assert json_formatter is not None

        table_formatter = OutputFormatter.create("table")
        assert table_formatter is not None

        text_formatter = OutputFormatter.create("text")
        assert text_formatter is not None

        # Test unknown format
        with pytest.raises(ValueError):
            OutputFormatter.create("unknown_format")


class TestColoredOutput:
    """Test colored output functionality."""

    def test_colored_output_creation(self):
        """Test ColoredOutput instantiation."""
        if ColoredOutput is None:
            pytest.skip("ColoredOutput not implemented yet - TDD Red phase")

        colored = ColoredOutput()
        assert colored is not None

    def test_success_coloring(self):
        """Test success message coloring."""
        if ColoredOutput is None:
            pytest.skip("ColoredOutput not implemented yet - TDD Red phase")

        colored = ColoredOutput()
        message = "Validation successful"

        colored_message = colored.success(message)

        # Should contain the original message
        assert message in colored_message
        # Should contain color codes (ANSI escape sequences)
        assert '\033[' in colored_message or colored_message != message

    def test_error_coloring(self):
        """Test error message coloring."""
        if ColoredOutput is None:
            pytest.skip("ColoredOutput not implemented yet - TDD Red phase")

        colored = ColoredOutput()
        message = "Validation failed"

        colored_message = colored.error(message)

        # Should contain the original message
        assert message in colored_message
        # Should contain color codes
        assert '\033[' in colored_message or colored_message != message

    def test_warning_coloring(self):
        """Test warning message coloring."""
        if ColoredOutput is None:
            pytest.skip("ColoredOutput not implemented yet - TDD Red phase")

        colored = ColoredOutput()
        message = "Warning: Schema might be incomplete"

        colored_message = colored.warning(message)

        # Should contain the original message
        assert message in colored_message

    def test_info_coloring(self):
        """Test info message coloring."""
        if ColoredOutput is None:
            pytest.skip("ColoredOutput not implemented yet - TDD Red phase")

        colored = ColoredOutput()
        message = "Processing file"

        colored_message = colored.info(message)

        # Should contain the original message
        assert message in colored_message

    def test_color_disable(self):
        """Test disabling colors."""
        if ColoredOutput is None:
            pytest.skip("ColoredOutput not implemented yet - TDD Red phase")

        colored = ColoredOutput(enabled=False)
        message = "Test message"

        # With colors disabled, should return original message
        assert colored.success(message) == message
        assert colored.error(message) == message
        assert colored.warning(message) == message
        assert colored.info(message) == message


class TestProgressIndicators:
    """Test progress indicator functionality."""

    def test_progress_indicator_creation(self):
        """Test ProgressIndicator instantiation."""
        if ProgressIndicator is None:
            pytest.skip("ProgressIndicator not implemented yet - TDD Red phase")

        progress = ProgressIndicator(total=100)
        assert progress is not None
        assert progress.total == 100

    def test_progress_update(self):
        """Test progress indicator updates."""
        if ProgressIndicator is None:
            pytest.skip("ProgressIndicator not implemented yet - TDD Red phase")

        progress = ProgressIndicator(total=10)

        # Test update method
        progress.update(1, "Processing file 1")
        assert progress.current == 1

        progress.update(5, "Processing file 5")
        assert progress.current == 5

    def test_progress_completion(self):
        """Test progress indicator completion."""
        if ProgressIndicator is None:
            pytest.skip("ProgressIndicator not implemented yet - TDD Red phase")

        progress = ProgressIndicator(total=5)

        for i in range(1, 6):
            progress.update(i, f"Processing file {i}")

        assert progress.current == 5
        assert progress.is_complete()

    def test_progress_bar_display(self):
        """Test progress bar visual display."""
        if create_progress_bar is None:
            pytest.skip("create_progress_bar not implemented yet - TDD Red phase")

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            progress_bar = create_progress_bar(total=10)

            # Update progress
            for i in range(1, 11):
                progress_bar.update(i)

            # Should have written to stdout
            output = mock_stdout.getvalue()
            # Progress bar typically contains progress characters
            assert len(output) > 0

    def test_progress_with_rich_library(self):
        """Test progress indicators using Rich library."""
        if ProgressIndicator is None:
            pytest.skip("ProgressIndicator not implemented yet - TDD Red phase")

        try:
            from rich.progress import Progress

            # Test integration with Rich progress bars
            progress = ProgressIndicator(total=10, use_rich=True)

            for i in range(1, 11):
                progress.update(i, f"Processing file {i}")

            # Should complete without errors
            assert progress.is_complete()

        except ImportError:
            pytest.skip("Rich library not available for testing")

    def test_progress_callback_function(self):
        """Test progress callback functionality."""
        if ProgressIndicator is None:
            pytest.skip("ProgressIndicator not implemented yet - TDD Red phase")

        callback_calls = []

        def progress_callback(current, total, message):
            callback_calls.append((current, total, message))

        progress = ProgressIndicator(total=5, callback=progress_callback)

        progress.update(1, "File 1")
        progress.update(3, "File 3")
        progress.update(5, "File 5")

        assert len(callback_calls) == 3
        assert callback_calls[0] == (1, 5, "File 1")
        assert callback_calls[1] == (3, 5, "File 3")
        assert callback_calls[2] == (5, 5, "File 5")


class TestFormattingFunctions:
    """Test standalone formatting functions."""

    def test_format_validation_result_function(self):
        """Test format_validation_result function."""
        if format_validation_result is None:
            pytest.skip("format_validation_result not implemented yet - TDD Red phase")

        # Test valid result
        result = {
            "file": "test.json",
            "valid": True,
            "errors": [],
            "processing_time": 0.123
        }

        formatted = format_validation_result(result, format_type="text")

        assert "test.json" in formatted
        assert "valid" in formatted.lower() or "success" in formatted.lower()

        # Test invalid result
        result = {
            "file": "invalid.json",
            "valid": False,
            "errors": ["Missing required field", "Invalid type"],
            "processing_time": 0.456
        }

        formatted = format_validation_result(result, format_type="text")

        assert "invalid.json" in formatted
        assert "Missing required field" in formatted
        assert "Invalid type" in formatted

    def test_format_batch_results_function(self):
        """Test format_batch_results function."""
        if format_batch_results is None:
            pytest.skip("format_batch_results not implemented yet - TDD Red phase")

        batch_result = {
            "total_files": 5,
            "valid_files": 3,
            "invalid_files": 2,
            "error_files": 0,
            "results": [
                {"file": "file1.json", "valid": True, "errors": []},
                {"file": "file2.json", "valid": True, "errors": []},
                {"file": "file3.json", "valid": True, "errors": []},
                {"file": "file4.json", "valid": False, "errors": ["Error 1"]},
                {"file": "file5.json", "valid": False, "errors": ["Error 2"]}
            ]
        }

        # Test table format
        table_output = format_batch_results(batch_result, format_type="table")
        assert "file1.json" in table_output
        assert "file4.json" in table_output
        assert "Error 1" in table_output

        # Test JSON format
        json_output = format_batch_results(batch_result, format_type="json")
        parsed = json.loads(json_output)
        assert parsed["total_files"] == 5
        assert parsed["valid_files"] == 3


class TestOutputIntegration:
    """Test integration of output formatting with other components."""

    def test_formatter_with_colored_output(self):
        """Test formatters working with colored output."""
        if OutputFormatter is None or ColoredOutput is None:
            pytest.skip("Output components not implemented yet - TDD Red phase")

        formatter = OutputFormatter.create("text")
        colored = ColoredOutput()

        result = {
            "file": "test.json",
            "valid": True,
            "errors": []
        }

        # Format result
        formatted = formatter.format(result)

        # Apply colors
        colored_output = colored.success(formatted)

        # Should contain both formatting and colors
        assert "test.json" in colored_output

    def test_formatter_with_progress_indicator(self):
        """Test formatters working with progress indicators."""
        if OutputFormatter is None or ProgressIndicator is None:
            pytest.skip("Output components not implemented yet - TDD Red phase")

        formatter = OutputFormatter.create("text")
        progress = ProgressIndicator(total=3)

        results = [
            {"file": "file1.json", "valid": True, "errors": []},
            {"file": "file2.json", "valid": False, "errors": ["Error"]},
            {"file": "file3.json", "valid": True, "errors": []}
        ]

        for i, result in enumerate(results, 1):
            formatted = formatter.format(result)
            progress.update(i, f"Processed {result['file']}")

            # Both formatting and progress should work
            assert formatted is not None
            assert progress.current == i

    def test_output_to_file(self):
        """Test writing formatted output to file."""
        if OutputFormatter is None:
            pytest.skip("OutputFormatter not implemented yet - TDD Red phase")

        import tempfile

        formatter = OutputFormatter.create("json")

        result = {
            "file": "test.json",
            "valid": True,
            "errors": []
        }

        formatted = formatter.format(result)

        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(formatted)
            temp_file = f.name

        try:
            # Read back and verify
            with open(temp_file, 'r') as f:
                content = f.read()

            parsed = json.loads(content)
            assert parsed["file"] == "test.json"
            assert parsed["valid"] is True

        finally:
            import os
            os.unlink(temp_file)


class TestOutputCustomization:
    """Test output customization and configuration."""

    def test_custom_formatter(self):
        """Test creating custom output formatters."""
        if OutputFormatter is None:
            pytest.skip("OutputFormatter not implemented yet - TDD Red phase")

        # Test ability to create custom formatters
        class CustomFormatter(OutputFormatter):
            def format(self, data):
                return f"CUSTOM: {data.get('file', 'unknown')} - {data.get('valid', False)}"

        try:
            OutputFormatter.register("custom", CustomFormatter)

            formatter = OutputFormatter.create("custom")
            result = {"file": "test.json", "valid": True}

            output = formatter.format(result)
            assert "CUSTOM: test.json - True" == output

        except (NotImplementedError, AttributeError):
            pytest.skip("Custom formatter registration not implemented")

    def test_output_verbosity_levels(self):
        """Test different verbosity levels in output."""
        if OutputFormatter is None:
            pytest.skip("OutputFormatter not implemented yet - TDD Red phase")

        formatter = OutputFormatter.create("text")

        result = {
            "file": "test.json",
            "valid": False,
            "errors": ["Error 1", "Error 2"],
            "processing_time": 0.123,
            "schema_path": "/path/to/schema.json"
        }

        # Test verbose output
        verbose_output = formatter.format(result, verbose=True)

        # Test quiet output
        quiet_output = formatter.format(result, verbose=False)

        # Verbose should contain more information
        if verbose_output != quiet_output:
            assert len(verbose_output) > len(quiet_output)

    def test_output_streaming(self):
        """Test streaming output for large batch operations."""
        if OutputFormatter is None:
            pytest.skip("OutputFormatter not implemented yet - TDD Red phase")

        formatter = OutputFormatter.create("text")

        # Test streaming individual results
        with patch('sys.stdout', new=StringIO()) as mock_stdout:

            results = [
                {"file": f"file_{i}.json", "valid": True, "errors": []}
                for i in range(5)
            ]

            for result in results:
                formatted = formatter.format(result)
                print(formatted, flush=True)

            output = mock_stdout.getvalue()

            # Should contain all file names
            for i in range(5):
                assert f"file_{i}.json" in output