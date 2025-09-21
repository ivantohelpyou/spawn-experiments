"""
File processing implementation.
Refactored for better structure and maintainability.
"""
import os
import chardet
from typing import Optional
from models.word_count_result import WordCountResult
from core.word_counter import MultilingualWordCounter


class FileHandler:
    """
    File handler for processing text files.

    Provides functionality to read files, detect encoding,
    and process text content for word counting.
    """

    # Constants for better maintainability
    DEFAULT_ENCODING = 'utf-8'
    ENCODING_DETECTION_SAMPLE_SIZE = 10000  # 10KB
    LOW_CONFIDENCE_THRESHOLD = 0.9

    def __init__(self):
        """Initialize the file handler."""
        self.word_counter = MultilingualWordCounter()

    def process_file(self, file_path: str) -> WordCountResult:
        """
        Process a text file and return word count results.

        Args:
            file_path: Path to the text file to process

        Returns:
            WordCountResult: Detailed result including word count and metadata

        Raises:
            ValueError: If file path is None, empty, or points to a directory
            FileNotFoundError: If file doesn't exist
        """
        self._validate_file_path(file_path)
        self._check_file_exists_and_is_file(file_path)

        # Read file content with proper encoding
        content, encoding = self._read_file_content(file_path)

        # Process the content using word counter
        result = self.word_counter.count_words(content)

        # Add file processing metadata
        self._add_file_metadata(result, file_path, encoding)

        return result

    def get_file_encoding(self, file_path: str) -> str:
        """
        Detect the encoding of a file.

        Args:
            file_path: Path to the file

        Returns:
            str: Detected encoding name
        """
        try:
            with open(file_path, 'rb') as f:
                # Read a sample of the file for encoding detection
                raw_data = f.read(self.ENCODING_DETECTION_SAMPLE_SIZE)

            result = chardet.detect(raw_data)

            if result and result['encoding']:
                return self._normalize_encoding(result)
            else:
                return self.DEFAULT_ENCODING

        except Exception:
            return self.DEFAULT_ENCODING

    def _validate_file_path(self, file_path: str) -> None:
        """Validate the file path input."""
        if file_path is None:
            raise ValueError("File path cannot be None")

        if not file_path or file_path.strip() == "":
            raise ValueError("File path cannot be empty")

    def _check_file_exists_and_is_file(self, file_path: str) -> None:
        """Check if file exists and is actually a file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if not os.path.isfile(file_path):
            raise ValueError("Path is not a file")

    def _read_file_content(self, file_path: str) -> tuple[str, str]:
        """Read file content with proper encoding detection."""
        encoding = self.get_file_encoding(file_path)

        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content, encoding
        except UnicodeDecodeError:
            # Fallback to utf-8 if detection fails
            encoding = self.DEFAULT_ENCODING
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()
            return content, encoding

    def _add_file_metadata(self, result: WordCountResult, file_path: str, encoding: str) -> None:
        """Add file processing metadata to the result."""
        result.metadata.update({
            "file_path": file_path,
            "file_size": os.path.getsize(file_path),
            "encoding": encoding
        })

    def _normalize_encoding(self, detection_result: dict) -> str:
        """Normalize detected encoding to preferred values."""
        detected_encoding = detection_result['encoding'].lower()
        confidence = detection_result['confidence']

        # Prefer UTF-8 over ASCII for better compatibility
        if detected_encoding in ['ascii', 'us-ascii']:
            return self.DEFAULT_ENCODING

        # Handle MacRoman encoding issues for UTF-8 files
        elif detected_encoding == 'macroman' and confidence < self.LOW_CONFIDENCE_THRESHOLD:
            return self.DEFAULT_ENCODING

        else:
            return detection_result['encoding']