"""
Tests for language detection functionality.
Following TDD - these tests will fail initially.
"""
import pytest
from core.language_detector import LanguageDetector
from models.word_count_result import LanguageInfo


class TestLanguageDetection:
    """Test language detection functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = LanguageDetector()

    def test_detect_english_text(self):
        """Test detection of English text."""
        text = "Hello world, this is a test of English language detection."
        result = self.detector.detect_language(text)

        assert isinstance(result, LanguageInfo)
        assert result.code == "en"
        assert result.name == "English"
        assert result.confidence > 0.8

    def test_detect_spanish_text(self):
        """Test detection of Spanish text."""
        text = "Hola mundo, esta es una prueba de detección de idioma español."
        result = self.detector.detect_language(text)

        assert result.code == "es"
        assert result.name == "Spanish"
        assert result.confidence > 0.8

    def test_detect_french_text(self):
        """Test detection of French text."""
        text = "Bonjour le monde, ceci est un test de détection de langue française."
        result = self.detector.detect_language(text)

        assert result.code == "fr"
        assert result.name == "French"
        assert result.confidence > 0.8

    def test_detect_german_text(self):
        """Test detection of German text."""
        text = "Hallo Welt, dies ist ein Test der deutschen Spracherkennung."
        result = self.detector.detect_language(text)

        assert result.code == "de"
        assert result.name == "German"
        assert result.confidence > 0.8

    def test_detect_short_text_fallback(self):
        """Test fallback for very short text."""
        text = "Hi"
        result = self.detector.detect_language(text)

        # Should fallback to English for short text
        assert result.code == "en"
        assert result.confidence >= 0.0

    def test_detect_empty_text(self):
        """Test detection with empty text."""
        text = ""
        result = self.detector.detect_language(text)

        assert result.code == "en"  # Default fallback
        assert result.confidence == 0.0

    def test_detect_multiple_languages(self):
        """Test detection of multiple languages in text."""
        text = "Hello world. Hola mundo. Bonjour le monde."
        results = self.detector.detect_languages(text)

        assert isinstance(results, list)
        assert len(results) >= 1
        # Should detect at least English
        language_codes = [lang.code for lang in results]
        assert "en" in language_codes

    def test_is_supported_language(self):
        """Test checking if language is supported."""
        assert self.detector.is_supported_language("en") is True
        assert self.detector.is_supported_language("es") is True
        assert self.detector.is_supported_language("fr") is True
        assert self.detector.is_supported_language("de") is True
        assert self.detector.is_supported_language("xx") is False


class TestLanguageDetectionErrors:
    """Test error handling for language detection."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = LanguageDetector()

    def test_detect_none_input(self):
        """Test handling of None input."""
        with pytest.raises(ValueError, match="Input text cannot be None"):
            self.detector.detect_language(None)

    def test_detect_languages_none_input(self):
        """Test handling of None input for multiple language detection."""
        with pytest.raises(ValueError, match="Input text cannot be None"):
            self.detector.detect_languages(None)