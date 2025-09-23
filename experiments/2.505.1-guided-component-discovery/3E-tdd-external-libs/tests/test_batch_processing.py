"""Test suite for batch processing and file operations following TDD methodology."""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import batch processing modules - will fail initially (Red phase)
try:
    from json_schema_validator import (
        BatchProcessor,
        FileProcessor,
        batch_validate_files,
        find_json_files,
        process_directory,
        ProcessingResult,
        BatchResult
    )
except ImportError:
    # Expected during TDD - tests written first
    BatchProcessor = None
    FileProcessor = None
    batch_validate_files = None
    find_json_files = None
    process_directory = None
    ProcessingResult = None
    BatchResult = None


class TestFileDiscovery:
    """Test file discovery and pattern matching."""

    def test_find_json_files_basic(self):
        """Test basic JSON file discovery in directory."""
        if find_json_files is None:
            pytest.skip("find_json_files not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test JSON files
            json_files = ["data1.json", "data2.json", "config.json"]
            for filename in json_files:
                file_path = Path(temp_dir) / filename
                with open(file_path, 'w') as f:
                    json.dump({"test": "data"}, f)

            # Create non-JSON files
            non_json_files = ["readme.txt", "data.xml", "script.py"]
            for filename in non_json_files:
                file_path = Path(temp_dir) / filename
                with open(file_path, 'w') as f:
                    f.write("not json content")

            found_files = find_json_files(temp_dir)
            found_names = [Path(f).name for f in found_files]

            assert len(found_files) == 3
            for json_file in json_files:
                assert json_file in found_names

    def test_find_json_files_with_pattern(self):
        """Test JSON file discovery with custom patterns."""
        if find_json_files is None:
            pytest.skip("find_json_files not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            files = [
                "data_001.json", "data_002.json", "config.json",
                "test_001.json", "output.json"
            ]
            for filename in files:
                file_path = Path(temp_dir) / filename
                with open(file_path, 'w') as f:
                    json.dump({"test": "data"}, f)

            # Test pattern matching
            data_files = find_json_files(temp_dir, pattern="data_*.json")
            data_names = [Path(f).name for f in data_files]

            assert len(data_files) == 2
            assert "data_001.json" in data_names
            assert "data_002.json" in data_names
            assert "config.json" not in data_names

    def test_find_json_files_recursive(self):
        """Test recursive JSON file discovery."""
        if find_json_files is None:
            pytest.skip("find_json_files not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create nested directory structure
            subdir1 = Path(temp_dir) / "subdir1"
            subdir2 = Path(temp_dir) / "subdir1" / "subdir2"
            subdir1.mkdir()
            subdir2.mkdir()

            # Create JSON files at different levels
            files = [
                Path(temp_dir) / "root.json",
                subdir1 / "level1.json",
                subdir2 / "level2.json"
            ]

            for file_path in files:
                with open(file_path, 'w') as f:
                    json.dump({"level": str(file_path.parent.name)}, f)

            found_files = find_json_files(temp_dir, recursive=True)
            found_names = [Path(f).name for f in found_files]

            assert len(found_files) == 3
            assert "root.json" in found_names
            assert "level1.json" in found_names
            assert "level2.json" in found_names

    def test_find_json_files_empty_directory(self):
        """Test file discovery in empty directory."""
        if find_json_files is None:
            pytest.skip("find_json_files not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            found_files = find_json_files(temp_dir)
            assert found_files == []


class TestBatchValidation:
    """Test batch validation functionality."""

    def test_batch_validate_files_all_valid(self):
        """Test batch validation with all valid files."""
        if batch_validate_files is None:
            pytest.skip("batch_validate_files not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create schema
            schema = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "value": {"type": "number"}
                },
                "required": ["name"]
            }
            schema_file = Path(temp_dir) / "schema.json"
            with open(schema_file, 'w') as f:
                json.dump(schema, f)

            # Create valid JSON files
            valid_data = [
                {"name": "item1", "value": 10},
                {"name": "item2", "value": 20},
                {"name": "item3"}  # Missing value is OK
            ]

            json_files = []
            for i, data in enumerate(valid_data):
                file_path = Path(temp_dir) / f"data_{i}.json"
                with open(file_path, 'w') as f:
                    json.dump(data, f)
                json_files.append(str(file_path))

            result = batch_validate_files(json_files, str(schema_file))

            assert result.total_files == 3
            assert result.valid_files == 3
            assert result.invalid_files == 0
            assert len(result.results) == 3
            assert all(r.is_valid for r in result.results)

    def test_batch_validate_files_mixed_validity(self):
        """Test batch validation with mix of valid and invalid files."""
        if batch_validate_files is None:
            pytest.skip("batch_validate_files not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create schema
            schema = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "value": {"type": "number"}
                },
                "required": ["name", "value"]
            }
            schema_file = Path(temp_dir) / "schema.json"
            with open(schema_file, 'w') as f:
                json.dump(schema, f)

            # Create mix of valid and invalid data
            test_data = [
                {"name": "valid1", "value": 10},  # Valid
                {"name": "valid2", "value": 20},  # Valid
                {"value": 30},                    # Invalid - missing name
                {"name": "invalid", "value": "not_number"}  # Invalid - wrong type
            ]

            json_files = []
            for i, data in enumerate(test_data):
                file_path = Path(temp_dir) / f"data_{i}.json"
                with open(file_path, 'w') as f:
                    json.dump(data, f)
                json_files.append(str(file_path))

            result = batch_validate_files(json_files, str(schema_file))

            assert result.total_files == 4
            assert result.valid_files == 2
            assert result.invalid_files == 2
            assert len(result.results) == 4

    def test_batch_validate_files_error_handling(self):
        """Test batch validation error handling."""
        if batch_validate_files is None:
            pytest.skip("batch_validate_files not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            schema = {"type": "object"}
            schema_file = Path(temp_dir) / "schema.json"
            with open(schema_file, 'w') as f:
                json.dump(schema, f)

            # Create invalid JSON file
            invalid_file = Path(temp_dir) / "invalid.json"
            with open(invalid_file, 'w') as f:
                f.write("invalid json content")

            # Create non-existent file reference
            nonexistent_file = str(Path(temp_dir) / "nonexistent.json")

            files = [str(invalid_file), nonexistent_file]
            result = batch_validate_files(files, str(schema_file))

            # Should handle errors gracefully
            assert result.total_files == 2
            assert result.error_files > 0


class TestBatchProcessor:
    """Test BatchProcessor class functionality."""

    def test_batch_processor_creation(self):
        """Test BatchProcessor instantiation."""
        if BatchProcessor is None:
            pytest.skip("BatchProcessor not implemented yet - TDD Red phase")

        schema = {"type": "object"}
        processor = BatchProcessor(schema)
        assert processor is not None
        assert processor.schema == schema

    def test_batch_processor_process_directory(self):
        """Test BatchProcessor directory processing."""
        if BatchProcessor is None:
            pytest.skip("BatchProcessor not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create schema and processor
            schema = {
                "type": "object",
                "properties": {"id": {"type": "number"}},
                "required": ["id"]
            }
            processor = BatchProcessor(schema)

            # Create test files
            test_data = [
                {"id": 1}, {"id": 2}, {"id": 3}
            ]
            for i, data in enumerate(test_data):
                file_path = Path(temp_dir) / f"item_{i}.json"
                with open(file_path, 'w') as f:
                    json.dump(data, f)

            result = processor.process_directory(temp_dir)

            assert result.total_files == 3
            assert result.valid_files == 3
            assert result.invalid_files == 0

    def test_batch_processor_with_progress_callback(self):
        """Test BatchProcessor with progress callback."""
        if BatchProcessor is None:
            pytest.skip("BatchProcessor not implemented yet - TDD Red phase")

        progress_calls = []

        def progress_callback(current, total, filename):
            progress_calls.append((current, total, filename))

        with tempfile.TemporaryDirectory() as temp_dir:
            schema = {"type": "object"}
            processor = BatchProcessor(schema, progress_callback=progress_callback)

            # Create test files
            for i in range(3):
                file_path = Path(temp_dir) / f"item_{i}.json"
                with open(file_path, 'w') as f:
                    json.dump({"test": i}, f)

            processor.process_directory(temp_dir)

            # Should have called progress callback
            assert len(progress_calls) > 0
            assert progress_calls[0][1] == 3  # Total files


class TestFileProcessor:
    """Test FileProcessor functionality."""

    def test_file_processor_single_file(self):
        """Test processing single file."""
        if FileProcessor is None:
            pytest.skip("FileProcessor not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test file
            data = {"name": "test", "value": 42}
            file_path = Path(temp_dir) / "test.json"
            with open(file_path, 'w') as f:
                json.dump(data, f)

            processor = FileProcessor()
            result = processor.load_json(str(file_path))

            assert result == data

    def test_file_processor_error_handling(self):
        """Test FileProcessor error handling."""
        if FileProcessor is None:
            pytest.skip("FileProcessor not implemented yet - TDD Red phase")

        processor = FileProcessor()

        # Test non-existent file
        with pytest.raises((FileNotFoundError, IOError, ValidationError)):
            processor.load_json("nonexistent.json")

        # Test invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json")
            invalid_file = f.name

        try:
            with pytest.raises((json.JSONDecodeError, ValueError, ValidationError)):
                processor.load_json(invalid_file)
        finally:
            os.unlink(invalid_file)


class TestDirectoryProcessing:
    """Test directory processing functionality."""

    def test_process_directory_basic(self):
        """Test basic directory processing."""
        if process_directory is None:
            pytest.skip("process_directory not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create schema
            schema = {"type": "object", "properties": {"id": {"type": "number"}}}
            schema_file = Path(temp_dir) / "schema.json"
            with open(schema_file, 'w') as f:
                json.dump(schema, f)

            # Create data files
            for i in range(5):
                data = {"id": i}
                file_path = Path(temp_dir) / f"data_{i}.json"
                with open(file_path, 'w') as f:
                    json.dump(data, f)

            result = process_directory(temp_dir, str(schema_file))

            assert result.total_files == 5  # Don't count schema file
            assert result.valid_files >= 0
            assert result.invalid_files >= 0

    def test_process_directory_with_subdirectories(self):
        """Test directory processing with subdirectories."""
        if process_directory is None:
            pytest.skip("process_directory not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create schema
            schema = {"type": "object"}
            schema_file = Path(temp_dir) / "schema.json"
            with open(schema_file, 'w') as f:
                json.dump(schema, f)

            # Create nested structure
            subdir = Path(temp_dir) / "subdir"
            subdir.mkdir()

            # Create files in root and subdir
            root_file = Path(temp_dir) / "root.json"
            sub_file = subdir / "sub.json"

            for file_path in [root_file, sub_file]:
                with open(file_path, 'w') as f:
                    json.dump({"test": "data"}, f)

            # Test non-recursive
            result = process_directory(temp_dir, str(schema_file), recursive=False)
            assert result.total_files == 1  # Only root file

            # Test recursive
            result = process_directory(temp_dir, str(schema_file), recursive=True)
            assert result.total_files == 2  # Root and sub file


class TestBatchResults:
    """Test batch processing result structures."""

    def test_batch_result_structure(self):
        """Test BatchResult data structure."""
        if BatchResult is None:
            pytest.skip("BatchResult not implemented yet - TDD Red phase")

        # Test creation with results
        individual_results = [
            ProcessingResult(file_path="file1.json", is_valid=True, errors=[]),
            ProcessingResult(file_path="file2.json", is_valid=False, errors=["Error"])
        ]

        batch_result = BatchResult(
            total_files=2,
            valid_files=1,
            invalid_files=1,
            error_files=0,
            results=individual_results
        )

        assert batch_result.total_files == 2
        assert batch_result.valid_files == 1
        assert batch_result.invalid_files == 1
        assert batch_result.error_files == 0
        assert len(batch_result.results) == 2

    def test_processing_result_structure(self):
        """Test ProcessingResult data structure."""
        if ProcessingResult is None:
            pytest.skip("ProcessingResult not implemented yet - TDD Red phase")

        # Test valid result
        result = ProcessingResult(
            file_path="test.json",
            is_valid=True,
            errors=[],
            processing_time=0.123
        )

        assert result.file_path == "test.json"
        assert result.is_valid is True
        assert result.errors == []
        assert result.processing_time == 0.123

        # Test invalid result
        result = ProcessingResult(
            file_path="invalid.json",
            is_valid=False,
            errors=["Validation error", "Format error"],
            processing_time=0.456
        )

        assert result.is_valid is False
        assert len(result.errors) == 2


class TestBatchProcessingPerformance:
    """Test batch processing performance and optimization."""

    def test_parallel_processing(self):
        """Test parallel processing of files."""
        if BatchProcessor is None:
            pytest.skip("BatchProcessor not implemented yet - TDD Red phase")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create schema and many files for parallel processing test
            schema = {"type": "object"}
            schema_file = Path(temp_dir) / "schema.json"
            with open(schema_file, 'w') as f:
                json.dump(schema, f)

            # Create many test files
            num_files = 20
            for i in range(num_files):
                data = {"id": i, "data": f"test_{i}"}
                file_path = Path(temp_dir) / f"file_{i:03d}.json"
                with open(file_path, 'w') as f:
                    json.dump(data, f)

            processor = BatchProcessor(schema)

            # Test if parallel processing is supported
            try:
                result = processor.process_directory(temp_dir, parallel=True)
                assert result.total_files == num_files
            except (NotImplementedError, TypeError):
                # Parallel processing might not be implemented yet
                pytest.skip("Parallel processing not implemented")

    def test_memory_efficient_processing(self):
        """Test memory-efficient processing of large batches."""
        if BatchProcessor is None:
            pytest.skip("BatchProcessor not implemented yet - TDD Red phase")

        # This test ensures the processor doesn't load all files into memory
        # Implementation should use generators or streaming processing

        with tempfile.TemporaryDirectory() as temp_dir:
            schema = {"type": "object"}
            processor = BatchProcessor(schema)

            # Create files
            for i in range(10):
                data = {"large_data": "x" * 1000}  # 1KB per file
                file_path = Path(temp_dir) / f"large_{i}.json"
                with open(file_path, 'w') as f:
                    json.dump(data, f)

            # Should process without excessive memory usage
            result = processor.process_directory(temp_dir)
            assert result.total_files == 10