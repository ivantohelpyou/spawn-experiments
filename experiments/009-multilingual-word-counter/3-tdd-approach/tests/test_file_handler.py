"""
Tests for file processing functionality.
Following TDD - these tests will fail initially.
"""
import pytest
import tempfile
import os
from utils.file_handler import FileHandler
from models.word_count_result import WordCountResult


class TestFileProcessing:
    """Test file processing functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.file_handler = FileHandler()

    def test_process_text_file_english(self):
        """Test processing a simple English text file."""
        content = "Hello world. This is a test file with multiple sentences."

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_file = f.name

        try:
            result = self.file_handler.process_file(temp_file)

            assert isinstance(result, WordCountResult)
            assert result.total_words == 10
            assert result.text == content
            assert "en" in result.language_breakdown

        finally:
            os.unlink(temp_file)

    def test_process_text_file_spanish(self):
        """Test processing a Spanish text file."""
        content = "Hola mundo. Este es un archivo de prueba con múltiples oraciones."

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_file = f.name

        try:
            result = self.file_handler.process_file(temp_file)

            assert isinstance(result, WordCountResult)
            assert result.total_words == 11
            assert result.text == content
            assert "es" in result.language_breakdown

        finally:
            os.unlink(temp_file)

    def test_process_empty_file(self):
        """Test processing an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("")
            temp_file = f.name

        try:
            result = self.file_handler.process_file(temp_file)

            assert result.total_words == 0
            assert result.text == ""

        finally:
            os.unlink(temp_file)

    def test_process_file_with_encoding_detection(self):
        """Test processing a file with automatic encoding detection."""
        content = "This is a test with special characters: café, naïve, résumé"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_file = f.name

        try:
            result = self.file_handler.process_file(temp_file)

            assert isinstance(result, WordCountResult)
            assert result.total_words == 10
            assert "café" in result.text
            assert "naïve" in result.text

        finally:
            os.unlink(temp_file)

    def test_get_file_encoding(self):
        """Test automatic file encoding detection."""
        content = "Hello world with special chars: café"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_file = f.name

        try:
            encoding = self.file_handler.get_file_encoding(temp_file)
            assert encoding is not None
            assert isinstance(encoding, str)

        finally:
            os.unlink(temp_file)


class TestFileProcessingErrors:
    """Test error handling for file processing."""

    def setup_method(self):
        """Set up test fixtures."""
        self.file_handler = FileHandler()

    def test_process_nonexistent_file(self):
        """Test handling of non-existent file."""
        with pytest.raises(FileNotFoundError):
            self.file_handler.process_file("/path/that/does/not/exist.txt")

    def test_process_none_file_path(self):
        """Test handling of None file path."""
        with pytest.raises(ValueError, match="File path cannot be None"):
            self.file_handler.process_file(None)

    def test_process_empty_file_path(self):
        """Test handling of empty file path."""
        with pytest.raises(ValueError, match="File path cannot be empty"):
            self.file_handler.process_file("")

    def test_process_directory_instead_of_file(self):
        """Test handling when directory is passed instead of file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(ValueError, match="Path is not a file"):
                self.file_handler.process_file(temp_dir)