"""
Language detection implementation.
Refactored for better structure and maintainability.
"""
from typing import List
from langdetect import detect, detect_langs, LangDetectException
from models.word_count_result import LanguageInfo


class LanguageDetector:
    """
    Language detector using langdetect library.

    Provides functionality to detect single or multiple languages
    in text with confidence scores.
    """

    # Constants for better maintainability
    MIN_TEXT_LENGTH_FOR_DETECTION = 3
    DEFAULT_LANGUAGE = "en"
    DEFAULT_LANGUAGE_NAME = "English"
    HIGH_CONFIDENCE = 0.9
    LOW_CONFIDENCE = 0.5
    NO_CONFIDENCE = 0.0

    # Language code to name mapping
    LANGUAGE_NAMES = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "ar": "Arabic",
        "hi": "Hindi",
        "nl": "Dutch",
        "sv": "Swedish",
        "no": "Norwegian",
        "da": "Danish",
        "fi": "Finnish",
        "pl": "Polish",
        "tr": "Turkish",
        "he": "Hebrew"
    }

    SUPPORTED_LANGUAGES = set(LANGUAGE_NAMES.keys())

    def __init__(self):
        """Initialize the language detector."""
        pass

    def detect_language(self, text: str) -> LanguageInfo:
        """
        Detect the primary language of the given text.

        Args:
            text: Input text to analyze

        Returns:
            LanguageInfo: Information about detected language

        Raises:
            ValueError: If input text is None
        """
        self._validate_input(text)

        cleaned_text = text.strip()

        # Handle empty text
        if not cleaned_text:
            return self._create_fallback_language_info(self.NO_CONFIDENCE)

        # Handle very short text
        if len(cleaned_text) < self.MIN_TEXT_LENGTH_FOR_DETECTION:
            return self._create_fallback_language_info(self.LOW_CONFIDENCE)

        try:
            # Detect language using langdetect
            detected_code = detect(text)
            language_name = self._get_language_name(detected_code)

            return LanguageInfo(
                code=detected_code,
                name=language_name,
                confidence=self.HIGH_CONFIDENCE,
                word_count=0  # Will be filled by word counter
            )

        except LangDetectException:
            # Fallback to default language if detection fails
            return self._create_fallback_language_info(self.LOW_CONFIDENCE)

    def detect_languages(self, text: str) -> List[LanguageInfo]:
        """
        Detect multiple languages in the given text.

        Args:
            text: Input text to analyze

        Returns:
            List[LanguageInfo]: List of detected languages with confidence scores

        Raises:
            ValueError: If input text is None
        """
        self._validate_input(text)

        # Handle empty text
        if not text.strip():
            return [self._create_fallback_language_info(self.NO_CONFIDENCE)]

        try:
            # Detect multiple languages with confidence scores
            detected_langs = detect_langs(text)

            results = []
            for lang in detected_langs:
                language_name = self._get_language_name(lang.lang)
                results.append(LanguageInfo(
                    code=lang.lang,
                    name=language_name,
                    confidence=lang.prob,
                    word_count=0  # Will be filled by word counter
                ))

            return results

        except LangDetectException:
            # Fallback to default language if detection fails
            return [self._create_fallback_language_info(self.LOW_CONFIDENCE)]

    def is_supported_language(self, language_code: str) -> bool:
        """
        Check if a language code is supported.

        Args:
            language_code: ISO 639-1 language code

        Returns:
            bool: True if language is supported, False otherwise
        """
        return language_code in self.SUPPORTED_LANGUAGES

    def _validate_input(self, text: str) -> None:
        """Validate the input text."""
        if text is None:
            raise ValueError("Input text cannot be None")

    def _get_language_name(self, language_code: str) -> str:
        """Get the full language name from the language code."""
        return self.LANGUAGE_NAMES.get(language_code, language_code.title())

    def _create_fallback_language_info(self, confidence: float) -> LanguageInfo:
        """Create fallback language info for default language."""
        return LanguageInfo(
            code=self.DEFAULT_LANGUAGE,
            name=self.DEFAULT_LANGUAGE_NAME,
            confidence=confidence,
            word_count=0
        )