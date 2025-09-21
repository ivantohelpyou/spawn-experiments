"""
Tests for the basic word counter functionality.
Following TDD - these tests will fail initially.
"""
import pytest
from core.word_counter import MultilingualWordCounter
from models.word_count_result import WordCountResult


class TestBasicWordCounting:
    """Test basic word counting functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.counter = MultilingualWordCounter()

    def test_count_simple_english_sentence(self):
        """Test counting words in a simple English sentence."""
        text = "Hello world this is a test"
        result = self.counter.count_words(text)

        assert isinstance(result, WordCountResult)
        assert result.total_words == 6
        assert result.text == text

    def test_count_single_word(self):
        """Test counting a single word."""
        text = "Hello"
        result = self.counter.count_words(text)

        assert result.total_words == 1
        assert result.text == text

    def test_count_empty_string(self):
        """Test counting words in empty string."""
        text = ""
        result = self.counter.count_words(text)

        assert result.total_words == 0
        assert result.text == text

    def test_count_whitespace_only(self):
        """Test counting words in whitespace-only string."""
        text = "   \t\n  "
        result = self.counter.count_words(text)

        assert result.total_words == 0

    def test_count_words_with_punctuation(self):
        """Test counting words with punctuation."""
        text = "Hello, world! This is a test."
        result = self.counter.count_words(text)

        assert result.total_words == 6

    def test_count_words_with_extra_spaces(self):
        """Test counting words with multiple spaces."""
        text = "Hello    world   this  is    a     test"
        result = self.counter.count_words(text)

        assert result.total_words == 6

    def test_result_contains_metadata(self):
        """Test that result contains expected metadata."""
        text = "Hello world"
        result = self.counter.count_words(text)

        assert hasattr(result, 'processing_time')
        assert hasattr(result, 'metadata')
        assert hasattr(result, 'language_breakdown')
        assert hasattr(result, 'detected_languages')
        assert isinstance(result.processing_time, float)
        assert result.processing_time >= 0


class TestMultilingualWordCounting:
    """Test multilingual word counting functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.counter = MultilingualWordCounter()

    def test_count_spanish_text(self):
        """Test counting words in Spanish text."""
        text = "Hola mundo, esta es una prueba"
        result = self.counter.count_words(text)

        assert result.total_words == 6
        assert "es" in result.language_breakdown
        assert result.detected_languages[0].code == "es"

    def test_count_french_text(self):
        """Test counting words in French text."""
        text = "Bonjour le monde, ceci est un test"
        result = self.counter.count_words(text)

        assert result.total_words == 7
        assert "fr" in result.language_breakdown
        assert result.detected_languages[0].code == "fr"

    def test_count_mixed_language_text(self):
        """Test counting words in mixed language text."""
        text = "Hello world. Hola mundo."
        result = self.counter.count_words(text)

        assert result.total_words == 4
        # Should detect primary language
        assert len(result.detected_languages) >= 1


class TestErrorHandling:
    """Test error handling for word counter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.counter = MultilingualWordCounter()

    def test_count_none_input(self):
        """Test handling of None input."""
        with pytest.raises(ValueError, match="Input text cannot be None"):
            self.counter.count_words(None)