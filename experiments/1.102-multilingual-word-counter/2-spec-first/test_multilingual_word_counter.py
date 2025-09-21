"""
Comprehensive test suite for the Multilingual Word Counter.
Tests all major components and functionality.
"""

import pytest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock

from models import (
    LanguageResult, WordCountResult, TextStatistics, AnalysisResult,
    ProcessingConfig, LANGUAGE_NAMES
)
from language_detector import LanguageDetector
from word_counter import WordCounter
from text_analyzer import TextAnalyzer
from input_handler import InputHandler
from output_formatter import OutputFormatter
from multilingual_word_counter import MultilingualWordCounter


class TestModels:
    """Test the data models."""

    def test_language_result_creation(self):
        """Test LanguageResult creation."""
        result = LanguageResult(
            language='en',
            confidence=0.95,
            name='English'
        )
        assert result.language == 'en'
        assert result.confidence == 0.95
        assert result.name == 'English'

    def test_processing_config_defaults(self):
        """Test ProcessingConfig default values."""
        config = ProcessingConfig()
        assert config.min_confidence_threshold == 0.8
        assert config.enable_mixed_language is True
        assert config.max_text_length == 1_000_000
        assert config.output_format == "json"
        assert len(config.supported_languages) >= 15

    def test_language_names_mapping(self):
        """Test language names mapping."""
        assert LANGUAGE_NAMES['en'] == 'English'
        assert LANGUAGE_NAMES['zh'] == 'Chinese'
        assert LANGUAGE_NAMES['ar'] == 'Arabic'


class TestLanguageDetector:
    """Test the language detection functionality."""

    def setup_method(self):
        """Setup test fixtures."""
        self.detector = LanguageDetector()

    def test_detect_english_text(self):
        """Test English text detection."""
        text = "Hello world, this is a test in English language."
        result = self.detector.detect_language(text)

        assert result.language == 'en'
        assert result.confidence > 0.8
        assert result.name == 'English'

    def test_detect_empty_text(self):
        """Test empty text handling."""
        result = self.detector.detect_language("")
        assert result.language == 'unknown'
        assert result.confidence == 0.0

    def test_detect_short_text(self):
        """Test short text handling."""
        result = self.detector.detect_language("Hi")
        assert result.language == 'unknown'
        assert result.confidence == 0.0

    @patch('language_detector.detect_langs')
    def test_detect_languages_multiple(self, mock_detect_langs):
        """Test multiple language detection."""
        # Mock langdetect response
        mock_lang1 = Mock()
        mock_lang1.lang = 'en'
        mock_lang1.prob = 0.9

        mock_lang2 = Mock()
        mock_lang2.lang = 'es'
        mock_lang2.prob = 0.85

        mock_detect_langs.return_value = [mock_lang1, mock_lang2]

        text = "Hello world. Hola mundo."
        results = self.detector.detect_languages(text)

        assert len(results) == 2
        assert results[0].language == 'en'
        assert results[1].language == 'es'

    def test_clean_text(self):
        """Test text cleaning functionality."""
        text = "Hello https://example.com and test@email.com   with  extra  spaces"
        cleaned = self.detector._clean_text(text)
        assert "https://example.com" not in cleaned
        assert "test@email.com" not in cleaned
        assert "  " not in cleaned


class TestWordCounter:
    """Test the word counting functionality."""

    def setup_method(self):
        """Setup test fixtures."""
        self.counter = WordCounter()

    def test_count_english_words(self):
        """Test counting English words."""
        text = "Hello world, this is a test with five words."
        count = self.counter.count_words(text, 'en')
        assert count == 10  # Counting all words including articles

    def test_count_empty_text(self):
        """Test counting empty text."""
        count = self.counter.count_words("", 'en')
        assert count == 0

    def test_get_word_list(self):
        """Test getting word list."""
        text = "Hello world test"
        words = self.counter.get_word_list(text, 'en')
        assert 'Hello' in words or 'hello' in [w.lower() for w in words]
        assert 'world' in words or 'world' in [w.lower() for w in words]
        assert 'test' in words or 'test' in [w.lower() for w in words]

    def test_frequency_distribution(self):
        """Test word frequency distribution."""
        text = "hello world hello test hello"
        freq = self.counter.get_frequency_distribution(text, 'en')
        assert len(freq) > 0
        # 'hello' should be the most frequent
        assert freq[0][0] == 'hello'
        assert freq[0][1] == 3

    @pytest.mark.skipif(not hasattr(pytest, 'importorskip'), reason="Optional test")
    def test_chinese_word_counting(self):
        """Test Chinese word counting (if jieba is available)."""
        text = "你好世界，这是一个测试。"
        count = self.counter.count_words(text, 'zh')
        assert count > 0  # Should count some words

    def test_count_by_language(self):
        """Test counting by language."""
        language_segments = {
            'en': ['Hello world', 'This is English'],
            'es': ['Hola mundo', 'Esto es español']
        }
        counts = self.counter.count_by_language("", language_segments)
        assert 'en' in counts
        assert 'es' in counts
        assert counts['en'] > 0
        assert counts['es'] > 0


class TestTextAnalyzer:
    """Test the text analysis functionality."""

    def setup_method(self):
        """Setup test fixtures."""
        self.analyzer = TextAnalyzer()

    def test_analyze_english_text(self):
        """Test analyzing English text."""
        text = "Hello world. This is a test sentence. And another one!"
        result = self.analyzer.analyze(text)

        assert isinstance(result, AnalysisResult)
        assert result.word_count.total_words > 0
        assert result.statistics.sentence_count == 3
        assert result.statistics.character_count == len(text)
        assert len(result.detected_languages) > 0

    def test_analyze_empty_text(self):
        """Test analyzing empty text."""
        result = self.analyzer.analyze("")
        assert result.word_count.total_words == 0
        assert result.statistics.sentence_count == 0
        assert len(result.detected_languages) == 0

    def test_analyze_with_metadata(self):
        """Test analyzing with metadata."""
        text = "Hello world"
        metadata = {"source": "test", "author": "tester"}
        result = self.analyzer.analyze(text, metadata)

        assert result.metadata == metadata

    def test_count_sentences(self):
        """Test sentence counting."""
        text = "Hello! How are you? Fine."
        count = self.analyzer._count_sentences(text)
        assert count == 3

    def test_count_paragraphs(self):
        """Test paragraph counting."""
        text = "First paragraph.\\n\\nSecond paragraph.\\n\\nThird paragraph."
        count = self.analyzer._count_paragraphs(text)
        assert count == 3


class TestInputHandler:
    """Test the input handling functionality."""

    def setup_method(self):
        """Setup test fixtures."""
        self.handler = InputHandler()

    def test_detect_input_type_file(self):
        """Test file input type detection."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_path = f.name

        try:
            input_type = self.handler.detect_input_type(temp_path)
            assert input_type == 'file'
        finally:
            os.unlink(temp_path)

    def test_detect_input_type_url(self):
        """Test URL input type detection."""
        input_type = self.handler.detect_input_type("https://example.com")
        assert input_type == 'url'

    def test_detect_input_type_text(self):
        """Test text input type detection."""
        input_type = self.handler.detect_input_type("Hello world")
        assert input_type == 'text'

    def test_read_text_file(self):
        """Test reading text file."""
        content = "Hello world\\nSecond line"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_path = f.name

        try:
            text = self.handler.read_file(temp_path)
            assert text == content
        finally:
            os.unlink(temp_path)

    def test_read_nonexistent_file(self):
        """Test reading nonexistent file."""
        with pytest.raises(FileNotFoundError):
            self.handler.read_file("/nonexistent/path.txt")

    @patch('requests.get')
    def test_fetch_url_success(self, mock_get):
        """Test successful URL fetching."""
        mock_response = Mock()
        mock_response.text = "Hello from web"
        mock_response.headers = {'content-type': 'text/plain'}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        text = self.handler.fetch_url("https://example.com")
        assert text == "Hello from web"

    @patch('requests.get')
    def test_fetch_url_html(self, mock_get):
        """Test fetching HTML URL."""
        mock_response = Mock()
        mock_response.text = "<html><body>Hello web</body></html>"
        mock_response.headers = {'content-type': 'text/html'}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        text = self.handler.fetch_url("https://example.com")
        assert "Hello web" in text

    def test_process_input_text(self):
        """Test processing text input."""
        text, metadata = self.handler.process_input("Hello world", "text")
        assert text == "Hello world"
        assert metadata['input_type'] == 'text'

    def test_get_file_metadata(self):
        """Test getting file metadata."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test")
            temp_path = f.name

        try:
            metadata = self.handler.get_file_metadata(temp_path)
            assert 'file_path' in metadata
            assert 'file_size' in metadata
            assert metadata['file_name'] == os.path.basename(temp_path)
        finally:
            os.unlink(temp_path)


class TestOutputFormatter:
    """Test the output formatting functionality."""

    def setup_method(self):
        """Setup test fixtures."""
        self.formatter = OutputFormatter()
        # Create a sample result for testing
        self.sample_result = self._create_sample_result()

    def _create_sample_result(self):
        """Create a sample AnalysisResult for testing."""
        language_result = LanguageResult('en', 0.95, 'English')
        word_count = WordCountResult(
            total_words=10,
            words_by_language={'en': 10},
            word_list=['hello', 'world', 'test'],
            language_distribution={'en': 1.0}
        )
        statistics = TextStatistics(
            character_count=50,
            character_count_no_spaces=42,
            sentence_count=2,
            paragraph_count=1,
            average_words_per_sentence=5.0,
            most_frequent_words=[('hello', 2), ('world', 1)]
        )
        return AnalysisResult(
            text="Hello world test",
            detected_languages=[language_result],
            word_count=word_count,
            statistics=statistics,
            processing_time=0.1,
            metadata={'source': 'test'}
        )

    def test_to_json(self):
        """Test JSON formatting."""
        json_output = self.formatter.to_json(self.sample_result)
        assert isinstance(json_output, str)
        assert 'total_words' in json_output
        assert 'English' in json_output

    def test_to_csv(self):
        """Test CSV formatting."""
        csv_output = self.formatter.to_csv(self.sample_result)
        assert isinstance(csv_output, str)
        assert 'Metric,Value' in csv_output
        assert 'Total Words,10' in csv_output

    def test_to_human_readable(self):
        """Test human-readable formatting."""
        text_output = self.formatter.to_human_readable(self.sample_result)
        assert isinstance(text_output, str)
        assert 'MULTILINGUAL WORD COUNTER' in text_output
        assert 'Total Words: 10' in text_output
        assert 'English' in text_output

    def test_to_summary(self):
        """Test summary formatting."""
        summary = self.formatter.to_summary(self.sample_result)
        assert isinstance(summary, str)
        assert '10 words' in summary
        assert 'English' in summary

    def test_format_for_batch(self):
        """Test batch formatting."""
        results = [self.sample_result, self.sample_result]
        batch_output = self.formatter.format_for_batch(results, 'summary')
        assert isinstance(batch_output, str)
        assert 'BATCH PROCESSING SUMMARY' in batch_output


class TestMultilingualWordCounter:
    """Test the main application class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.app = MultilingualWordCounter()

    def test_process_single_text(self):
        """Test processing single text input."""
        result = self.app.process_single("Hello world test", "text")
        assert result['success'] is True
        assert 'result' in result
        assert result['result'].word_count.total_words > 0

    def test_process_single_empty(self):
        """Test processing empty input."""
        result = self.app.process_single("", "text")
        assert result['success'] is True
        assert result['result'].word_count.total_words == 0

    def test_process_batch(self):
        """Test batch processing."""
        inputs = ["Hello world", "Test sentence", "Another test"]
        result = self.app.process_batch(inputs)
        assert result['total_processed'] == 3
        assert result['successful'] == 3
        assert len(result['results']) == 3

    def test_format_output_json(self):
        """Test JSON output formatting."""
        result = self.app.process_single("Hello world", "text")['result']
        output = self.app.format_output(result, 'json')
        assert isinstance(output, str)
        assert 'total_words' in output

    def test_format_output_text(self):
        """Test text output formatting."""
        result = self.app.process_single("Hello world", "text")['result']
        output = self.app.format_output(result, 'text')
        assert isinstance(output, str)
        assert 'MULTILINGUAL WORD COUNTER' in output


class TestIntegration:
    """Integration tests for the complete system."""

    def setup_method(self):
        """Setup test fixtures."""
        self.app = MultilingualWordCounter()

    def test_end_to_end_processing(self):
        """Test complete end-to-end processing."""
        text = "Hello world! This is a test sentence. How are you today?"

        # Process the text
        result = self.app.process_single(text, "text")
        assert result['success'] is True

        analysis = result['result']
        assert analysis.word_count.total_words > 0
        assert analysis.statistics.sentence_count == 3
        assert len(analysis.detected_languages) > 0
        assert analysis.detected_languages[0].language == 'en'

        # Test different output formats
        json_output = self.app.format_output(analysis, 'json')
        assert 'total_words' in json_output

        csv_output = self.app.format_output(analysis, 'csv')
        assert 'Metric,Value' in csv_output

        text_output = self.app.format_output(analysis, 'text')
        assert 'Total Words:' in text_output

    def test_multilingual_text_processing(self):
        """Test processing multilingual text."""
        # Mixed English and pseudo-foreign text
        text = "Hello world. Bonjour le monde."

        result = self.app.process_single(text, "text")
        assert result['success'] is True

        analysis = result['result']
        assert analysis.word_count.total_words > 0
        # Should detect some language (might not be perfect due to short text)
        assert len(analysis.detected_languages) > 0

    def test_file_processing_integration(self):
        """Test file processing integration."""
        content = "This is a test file.\\nWith multiple lines.\\nAnd sentences!"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_path = f.name

        try:
            result = self.app.process_single(temp_path, "file")
            assert result['success'] is True

            analysis = result['result']
            assert analysis.word_count.total_words > 0
            assert analysis.statistics.sentence_count == 3
            assert 'file_path' in analysis.metadata
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])