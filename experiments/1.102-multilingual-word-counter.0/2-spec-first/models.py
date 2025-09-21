"""
Data models for the Multilingual Word Counter application.
Defines the core data structures used throughout the application.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any


@dataclass
class LanguageResult:
    """Result of language detection for a text."""
    language: str           # ISO 639-1 language code
    confidence: float       # Confidence score (0.0 - 1.0)
    name: str              # Human-readable language name


@dataclass
class WordCountResult:
    """Result of word counting analysis."""
    total_words: int
    words_by_language: Dict[str, int]
    word_list: List[str]
    language_distribution: Dict[str, float]


@dataclass
class TextStatistics:
    """Comprehensive text statistics."""
    character_count: int
    character_count_no_spaces: int
    sentence_count: int
    paragraph_count: int
    average_words_per_sentence: float
    most_frequent_words: List[Tuple[str, int]]


@dataclass
class AnalysisResult:
    """Complete analysis result for a text."""
    text: str
    detected_languages: List[LanguageResult]
    word_count: WordCountResult
    statistics: TextStatistics
    processing_time: float
    metadata: Dict[str, Any]


@dataclass
class ProcessingConfig:
    """Configuration for text processing."""
    min_confidence_threshold: float = 0.8
    supported_languages: List[str] = field(default_factory=lambda: [
        'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko',
        'ar', 'hi', 'nl', 'sv', 'tr'
    ])
    enable_mixed_language: bool = True
    max_text_length: int = 1_000_000
    output_format: str = "json"


# Language code to name mapping
LANGUAGE_NAMES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'tr': 'Turkish',
    'ca': 'Catalan',
    'da': 'Danish',
    'fi': 'Finnish',
    'no': 'Norwegian',
    'pl': 'Polish',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'el': 'Greek',
    'he': 'Hebrew',
    'cs': 'Czech',
    'hu': 'Hungarian',
    'ro': 'Romanian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'bg': 'Bulgarian',
    'hr': 'Croatian',
    'et': 'Estonian',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'mt': 'Maltese',
    'uk': 'Ukrainian',
}