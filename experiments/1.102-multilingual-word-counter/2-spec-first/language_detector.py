"""
Language detection module for the Multilingual Word Counter.
Handles automatic detection of text language with confidence scoring.
"""

import re
from typing import List, Dict
from langdetect import detect, detect_langs, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

from models import LanguageResult, ProcessingConfig, LANGUAGE_NAMES


class LanguageDetector:
    """Detects the language of input text with confidence scoring."""

    def __init__(self, config: ProcessingConfig = None):
        """Initialize the language detector with configuration."""
        self.config = config or ProcessingConfig()
        # Set seed for consistent results
        DetectorFactory.seed = 0

    def detect_language(self, text: str) -> LanguageResult:
        """
        Detect the primary language of the input text.

        Args:
            text: Input text to analyze

        Returns:
            LanguageResult with detected language and confidence
        """
        if not text or not text.strip():
            return LanguageResult(
                language='unknown',
                confidence=0.0,
                name='Unknown'
            )

        # Clean text for better detection
        cleaned_text = self._clean_text(text)

        if len(cleaned_text) < 10:
            return LanguageResult(
                language='unknown',
                confidence=0.0,
                name='Text too short for reliable detection'
            )

        try:
            # Get the most likely language
            primary_lang = detect(cleaned_text)

            # Get confidence score
            confidence = self.get_confidence_score(cleaned_text, primary_lang)

            # Check if language is supported
            if primary_lang not in self.config.supported_languages:
                # Try to find a similar supported language
                primary_lang = self._find_supported_language(primary_lang)

            language_name = LANGUAGE_NAMES.get(primary_lang, primary_lang.upper())

            return LanguageResult(
                language=primary_lang,
                confidence=confidence,
                name=language_name
            )

        except LangDetectException as e:
            return LanguageResult(
                language='unknown',
                confidence=0.0,
                name=f'Detection failed: {str(e)}'
            )

    def detect_languages(self, text: str) -> List[LanguageResult]:
        """
        Detect all possible languages in the text with probabilities.

        Args:
            text: Input text to analyze

        Returns:
            List of LanguageResult objects sorted by confidence
        """
        if not text or not text.strip():
            return []

        cleaned_text = self._clean_text(text)

        if len(cleaned_text) < 10:
            return []

        try:
            detected_langs = detect_langs(cleaned_text)
            results = []

            for lang_obj in detected_langs:
                language_code = lang_obj.lang
                confidence = lang_obj.prob

                # Filter by confidence threshold
                if confidence >= self.config.min_confidence_threshold:
                    language_name = LANGUAGE_NAMES.get(language_code, language_code.upper())
                    results.append(LanguageResult(
                        language=language_code,
                        confidence=confidence,
                        name=language_name
                    ))

            return sorted(results, key=lambda x: x.confidence, reverse=True)

        except LangDetectException:
            return []

    def get_confidence_score(self, text: str, language: str) -> float:
        """
        Get confidence score for a specific language detection.

        Args:
            text: Input text
            language: Language code to check

        Returns:
            Confidence score between 0.0 and 1.0
        """
        try:
            detected_langs = detect_langs(text)
            for lang_obj in detected_langs:
                if lang_obj.lang == language:
                    return lang_obj.prob
            return 0.0
        except LangDetectException:
            return 0.0

    def is_mixed_language(self, text: str) -> bool:
        """
        Check if text contains multiple languages.

        Args:
            text: Input text to analyze

        Returns:
            True if multiple languages detected with sufficient confidence
        """
        if not self.config.enable_mixed_language:
            return False

        languages = self.detect_languages(text)
        # Consider mixed if we have more than one language with >30% confidence
        high_confidence_langs = [lang for lang in languages if lang.confidence > 0.3]
        return len(high_confidence_langs) > 1

    def detect_language_segments(self, text: str) -> Dict[str, List[str]]:
        """
        Segment text by language for mixed-language texts.

        Args:
            text: Input text to segment

        Returns:
            Dictionary mapping language codes to text segments
        """
        # Simple implementation - split by sentences and detect each
        sentences = re.split(r'[.!?]+', text)
        language_segments = {}

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Only process substantial sentences
                lang_result = self.detect_language(sentence)
                if lang_result.confidence > 0.5:
                    lang_code = lang_result.language
                    if lang_code not in language_segments:
                        language_segments[lang_code] = []
                    language_segments[lang_code].append(sentence)

        return language_segments

    def _clean_text(self, text: str) -> str:
        """Clean text for better language detection."""
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def _find_supported_language(self, detected_lang: str) -> str:
        """Find a supported language similar to the detected one."""
        # Language family mappings
        language_families = {
            'zh-cn': 'zh', 'zh-tw': 'zh',
            'pt-br': 'pt', 'pt-pt': 'pt',
            'es-mx': 'es', 'es-ar': 'es',
            'en-us': 'en', 'en-gb': 'en',
            'fr-ca': 'fr', 'fr-fr': 'fr',
        }

        # Check direct mapping
        if detected_lang in language_families:
            return language_families[detected_lang]

        # Check if base language is supported
        base_lang = detected_lang.split('-')[0]
        if base_lang in self.config.supported_languages:
            return base_lang

        # Return original if no mapping found
        return detected_lang