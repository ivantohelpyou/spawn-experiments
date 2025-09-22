"""
Tests for batch validation with progress indicators.
Tests progress reporting and large-scale validation operations.
"""

import pytest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
from io import StringIO
import time

from jsv.batch import BatchValidator, ProgressIndicator


class TestProgressIndicator:
    """Test cases for progress indicator functionality."""

    def test_progress_indicator_creation(self):
        """Test progress indicator initialization."""
        progress = ProgressIndicator(total=100)
        assert progress.total == 100
        assert progress.current == 0
        assert progress.enabled == True

    def test_progress_indicator_disabled(self):
        """Test progress indicator when disabled."""
        progress = ProgressIndicator(total=100, enabled=False)
        assert progress.enabled == False

    def test_progress_update(self):
        """Test progress update functionality."""
        progress = ProgressIndicator(total=10, enabled=False)  # Disable for testing
        progress.update(5)
        assert progress.current == 5

        progress.update(3)
        assert progress.current == 8

    def test_progress_percentage(self):
        """Test progress percentage calculation."""
        progress = ProgressIndicator(total=100, enabled=False)
        progress.update(25)
        assert progress.percentage() == 25.0

        progress.update(25)
        assert progress.percentage() == 50.0

    def test_progress_display(self):
        """Test progress display output."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            progress = ProgressIndicator(total=10, enabled=True)
            progress.update(3)
            progress.display()
            output = mock_stdout.getvalue()
            assert "30%" in output or "3/10" in output


class TestBatchValidator:
    """Test cases for batch validation functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.batch_validator = BatchValidator()
        self.temp_dir = tempfile.mkdtemp()

        # Create test schema
        self.schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0}
            },
            "required": ["name"]
        }

        self.schema_file = os.path.join(self.temp_dir, 'schema.json')
        with open(self.schema_file, 'w') as f:
            json.dump(self.schema, f)

    def test_batch_validation_success(self):
        """Test successful batch validation."""
        # Create test files
        files = []
        for i in range(5):
            data_file = os.path.join(self.temp_dir, f'data{i}.json')
            data = {"name": f"Person{i}", "age": 20 + i}
            with open(data_file, 'w') as f:
                json.dump(data, f)
            files.append(data_file)

        results = self.batch_validator.validate_batch(files, self.schema_file, show_progress=False)
        assert len(results) == 5
        assert all(r['valid'] for r in results)

    def test_batch_validation_mixed_results(self):
        """Test batch validation with mixed valid/invalid files."""
        files = []

        # Valid file
        valid_file = os.path.join(self.temp_dir, 'valid.json')
        with open(valid_file, 'w') as f:
            json.dump({"name": "John", "age": 30}, f)
        files.append(valid_file)

        # Invalid file
        invalid_file = os.path.join(self.temp_dir, 'invalid.json')
        with open(invalid_file, 'w') as f:
            json.dump({"age": "thirty"}, f)  # Missing name, invalid age type
        files.append(invalid_file)

        results = self.batch_validator.validate_batch(files, self.schema_file, show_progress=False)
        assert len(results) == 2
        assert results[0]['valid'] == True
        assert results[1]['valid'] == False

    def test_batch_validation_with_progress(self):
        """Test batch validation with progress indicators."""
        # Create multiple test files
        files = []
        for i in range(10):
            data_file = os.path.join(self.temp_dir, f'data{i}.json')
            data = {"name": f"Person{i}", "age": 20 + i}
            with open(data_file, 'w') as f:
                json.dump(data, f)
            files.append(data_file)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            results = self.batch_validator.validate_batch(
                files, self.schema_file, show_progress=True
            )
            output = mock_stdout.getvalue()

            # Should show progress
            assert "%" in output or "Progress" in output or len(output) > 0

        assert len(results) == 10
        assert all(r['valid'] for r in results)

    def test_batch_validation_empty_list(self):
        """Test batch validation with empty file list."""
        results = self.batch_validator.validate_batch([], self.schema_file, show_progress=False)
        assert results == []

    def test_batch_validation_file_not_found(self):
        """Test batch validation with non-existent files."""
        files = [
            os.path.join(self.temp_dir, 'nonexistent.json'),
            os.path.join(self.temp_dir, 'another_missing.json')
        ]

        results = self.batch_validator.validate_batch(files, self.schema_file, show_progress=False)
        assert len(results) == 2
        assert not any(r['valid'] for r in results)
        assert all('not found' in str(r['errors']).lower() for r in results)

    def test_batch_validation_with_callback(self):
        """Test batch validation with progress callback."""
        files = []
        for i in range(3):
            data_file = os.path.join(self.temp_dir, f'data{i}.json')
            data = {"name": f"Person{i}", "age": 20 + i}
            with open(data_file, 'w') as f:
                json.dump(data, f)
            files.append(data_file)

        progress_calls = []
        def progress_callback(current, total, result):
            progress_calls.append((current, total, result['valid']))

        results = self.batch_validator.validate_batch(
            files, self.schema_file,
            show_progress=False,
            progress_callback=progress_callback
        )

        assert len(progress_calls) == 3
        assert progress_calls[0] == (1, 3, True)
        assert progress_calls[1] == (2, 3, True)
        assert progress_calls[2] == (3, 3, True)

    def test_batch_validation_performance(self):
        """Test batch validation performance with larger dataset."""
        # Create more files to test performance
        files = []
        for i in range(50):
            data_file = os.path.join(self.temp_dir, f'perf_data{i}.json')
            data = {"name": f"Person{i}", "age": 20 + i}
            with open(data_file, 'w') as f:
                json.dump(data, f)
            files.append(data_file)

        start_time = time.time()
        results = self.batch_validator.validate_batch(files, self.schema_file, show_progress=False)
        end_time = time.time()

        assert len(results) == 50
        assert all(r['valid'] for r in results)

        # Should complete reasonably quickly (less than 5 seconds for 50 files)
        assert (end_time - start_time) < 5.0

    def test_batch_summary_statistics(self):
        """Test batch validation summary statistics."""
        files = []

        # Create mix of valid and invalid files
        for i in range(3):
            valid_file = os.path.join(self.temp_dir, f'valid{i}.json')
            with open(valid_file, 'w') as f:
                json.dump({"name": f"Person{i}", "age": 20 + i}, f)
            files.append(valid_file)

        for i in range(2):
            invalid_file = os.path.join(self.temp_dir, f'invalid{i}.json')
            with open(invalid_file, 'w') as f:
                json.dump({"age": "invalid"}, f)  # Missing name, invalid age
            files.append(invalid_file)

        results = self.batch_validator.validate_batch(files, self.schema_file, show_progress=False)
        summary = self.batch_validator.get_summary_statistics(results)

        assert summary['total'] == 5
        assert summary['valid'] == 3
        assert summary['invalid'] == 2
        assert summary['success_rate'] == 0.6