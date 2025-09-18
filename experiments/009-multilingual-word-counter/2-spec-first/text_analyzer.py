"""
Text analysis module for the Multilingual Word Counter.
Generates comprehensive text statistics and analysis.
"""

import re
import time
from typing import Dict, Any

from models import AnalysisResult, TextStatistics, ProcessingConfig
from language_detector import LanguageDetector
from word_counter import WordCounter


class TextAnalyzer:
    """Generates comprehensive text statistics and analysis."""

    def __init__(self, config: ProcessingConfig = None):
        """Initialize the text analyzer with configuration."""
        self.config = config or ProcessingConfig()
        self.language_detector = LanguageDetector(self.config)
        self.word_counter = WordCounter(self.config)

    def analyze(self, text: str, metadata: Dict[str, Any] = None) -> AnalysisResult:
        """
        Perform comprehensive analysis of input text.

        Args:
            text: Input text to analyze
            metadata: Optional metadata dictionary

        Returns:
            AnalysisResult with complete analysis
        """
        start_time = time.time()

        if not text or not text.strip():
            return self._create_empty_result(text, time.time() - start_time, metadata)

        # Check text length limit
        if len(text) > self.config.max_text_length:
            text = text[:self.config.max_text_length]

        # Detect languages
        detected_languages = self._detect_languages(text)

        # Analyze word counts
        word_count_result = self._analyze_word_counts(text, detected_languages)

        # Generate statistics
        statistics = self._generate_statistics(text, word_count_result)

        processing_time = time.time() - start_time

        return AnalysisResult(
            text=text,
            detected_languages=detected_languages,
            word_count=word_count_result,
            statistics=statistics,
            processing_time=processing_time,
            metadata=metadata or {}
        )

    def _detect_languages(self, text: str):
        """Detect languages in the text."""
        if self.config.enable_mixed_language:
            # Try to detect multiple languages
            all_languages = self.language_detector.detect_languages(text)
            if all_languages:
                return all_languages

        # Fall back to single language detection
        primary_language = self.language_detector.detect_language(text)
        return [primary_language] if primary_language.language != 'unknown' else []

    def _analyze_word_counts(self, text: str, detected_languages):
        """Analyze word counts for detected languages."""
        from models import WordCountResult

        if not detected_languages:
            # No language detected, use default counting
            total_words = self.word_counter.count_words(text)
            word_list = self.word_counter.get_word_list(text)
            return WordCountResult(
                total_words=total_words,
                words_by_language={'unknown': total_words},
                word_list=word_list,
                language_distribution={'unknown': 1.0}
            )

        primary_language = detected_languages[0]

        # Check if this is a mixed language text
        if len(detected_languages) > 1 and self.language_detector.is_mixed_language(text):
            return self._analyze_mixed_language_text(text, detected_languages)
        else:
            return self._analyze_single_language_text(text, primary_language.language)

    def _analyze_single_language_text(self, text: str, language: str):
        """Analyze text in a single language."""
        from models import WordCountResult

        total_words = self.word_counter.count_words(text, language)
        word_list = self.word_counter.get_word_list(text, language)

        return WordCountResult(
            total_words=total_words,
            words_by_language={language: total_words},
            word_list=word_list,
            language_distribution={language: 1.0}
        )

    def _analyze_mixed_language_text(self, text: str, detected_languages):
        """Analyze text containing multiple languages."""
        from models import WordCountResult

        # Segment text by language
        language_segments = self.language_detector.detect_language_segments(text)

        # Count words by language
        words_by_language = self.word_counter.count_by_language(text, language_segments)

        # Calculate total words
        total_words = sum(words_by_language.values())

        # Calculate language distribution
        language_distribution = {}
        if total_words > 0:
            for lang, count in words_by_language.items():
                language_distribution[lang] = count / total_words

        # Get combined word list
        word_list = []
        for lang, segments in language_segments.items():
            for segment in segments:
                word_list.extend(self.word_counter.get_word_list(segment, lang))

        return WordCountResult(
            total_words=total_words,
            words_by_language=words_by_language,
            word_list=word_list,
            language_distribution=language_distribution
        )

    def _generate_statistics(self, text: str, word_count_result) -> TextStatistics:
        """Generate comprehensive text statistics."""
        # Character counts
        character_count = len(text)
        character_count_no_spaces = len(text.replace(' ', '').replace('\t', '').replace('\n', ''))

        # Sentence count
        sentence_count = self._count_sentences(text)

        # Paragraph count
        paragraph_count = self._count_paragraphs(text)

        # Average words per sentence
        average_words_per_sentence = (
            word_count_result.total_words / sentence_count
            if sentence_count > 0 else 0.0
        )

        # Most frequent words
        most_frequent_words = self.word_counter.get_frequency_distribution(
            text,
            language=self._get_primary_language(word_count_result),
            top_n=10
        )

        return TextStatistics(
            character_count=character_count,
            character_count_no_spaces=character_count_no_spaces,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            average_words_per_sentence=round(average_words_per_sentence, 2),
            most_frequent_words=most_frequent_words
        )

    def _count_sentences(self, text: str) -> int:
        """Count sentences in text."""
        # Use regex to find sentence endings
        sentences = re.split(r'[.!?]+', text)
        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        return len(sentences)

    def _count_paragraphs(self, text: str) -> int:
        """Count paragraphs in text."""
        # Split by double newlines or more
        paragraphs = re.split(r'\n\s*\n', text)
        # Filter out empty paragraphs
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return len(paragraphs)

    def _get_primary_language(self, word_count_result) -> str:
        """Get the primary language from word count result."""
        if not word_count_result.words_by_language:
            return None

        # Return language with most words
        return max(
            word_count_result.words_by_language.items(),
            key=lambda x: x[1]
        )[0]

    def _create_empty_result(self, text: str, processing_time: float, metadata: Dict[str, Any]) -> AnalysisResult:
        """Create an empty analysis result for empty or invalid text."""
        from models import WordCountResult, TextStatistics

        return AnalysisResult(
            text=text or "",
            detected_languages=[],
            word_count=WordCountResult(
                total_words=0,
                words_by_language={},
                word_list=[],
                language_distribution={}
            ),
            statistics=TextStatistics(
                character_count=len(text) if text else 0,
                character_count_no_spaces=0,
                sentence_count=0,
                paragraph_count=0,
                average_words_per_sentence=0.0,
                most_frequent_words=[]
            ),
            processing_time=processing_time,
            metadata=metadata or {}
        )

    def get_readability_metrics(self, text: str, language: str = None) -> Dict[str, float]:
        """
        Calculate readability metrics for the text.

        Args:
            text: Input text
            language: Language code

        Returns:
            Dictionary with readability metrics
        """
        word_count = self.word_counter.count_words(text, language)
        sentence_count = self._count_sentences(text)

        if sentence_count == 0 or word_count == 0:
            return {
                'average_words_per_sentence': 0.0,
                'average_sentence_length': 0.0,
            }

        # Calculate average words per sentence
        avg_words_per_sentence = word_count / sentence_count

        # Calculate average sentence length in characters
        sentences = re.split(r'[.!?]+', text)
        sentence_lengths = [len(s.strip()) for s in sentences if s.strip()]
        avg_sentence_length = (
            sum(sentence_lengths) / len(sentence_lengths)
            if sentence_lengths else 0.0
        )

        return {
            'average_words_per_sentence': round(avg_words_per_sentence, 2),
            'average_sentence_length': round(avg_sentence_length, 2),
        }