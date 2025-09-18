"""
Multilingual word counter implementation.
Refactored for better structure and maintainability.
"""
import time
import re
from typing import Dict, List, Any
from models.word_count_result import WordCountResult, LanguageInfo
from core.language_detector import LanguageDetector


class MultilingualWordCounter:
    """
    A multilingual word counter that can process text in various languages.

    Currently supports basic word counting with English language detection.
    Designed to be extended for full multilingual support.
    """

    # Constants for better maintainability
    DEFAULT_LANGUAGE = "en"
    DEFAULT_LANGUAGE_NAME = "English"
    WORD_PATTERN = r'\b\w+\b'

    def __init__(self):
        """Initialize the word counter."""
        self.language_detector = LanguageDetector()

    def count_words(self, text: str) -> WordCountResult:
        """
        Count words in the given text.

        Args:
            text: The input text to count words in

        Returns:
            WordCountResult: Detailed result including word count and metadata

        Raises:
            ValueError: If input text is None
        """
        self._validate_input(text)

        start_time = time.time()
        cleaned_text = self._clean_text(text)

        if not cleaned_text:
            return self._create_empty_result(text, start_time)

        # Detect the language first
        language_info = self.language_detector.detect_language(cleaned_text)

        # Count words
        word_count = self._count_words_basic(cleaned_text)

        # Update language info with word count
        language_info.word_count = word_count

        processing_time = time.time() - start_time

        return WordCountResult(
            text=text,
            total_words=word_count,
            language_breakdown={language_info.code: word_count},
            detected_languages=[language_info] if word_count > 0 else [],
            processing_time=processing_time,
            metadata=self._create_metadata()
        )

    def _validate_input(self, text: str) -> None:
        """Validate the input text."""
        if text is None:
            raise ValueError("Input text cannot be None")

    def _clean_text(self, text: str) -> str:
        """Clean and normalize the input text."""
        return text.strip()

    def _count_words_basic(self, text: str) -> int:
        """Count words using basic regex pattern."""
        words = re.findall(self.WORD_PATTERN, text)
        return len(words)

    def _create_empty_result(self, text: str, start_time: float) -> WordCountResult:
        """Create result for empty or whitespace-only text."""
        processing_time = time.time() - start_time
        return WordCountResult(
            text=text,
            total_words=0,
            language_breakdown={self.DEFAULT_LANGUAGE: 0},
            detected_languages=[],
            processing_time=processing_time,
            metadata=self._create_metadata()
        )

    def _create_metadata(self) -> Dict[str, Any]:
        """Create metadata for the result."""
        return {"method": "basic_regex", "version": "1.0"}