"""
Data models for the multilingual word counter.
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from datetime import datetime


@dataclass
class LanguageInfo:
    """Information about a detected language."""
    code: str           # ISO 639-1 language code
    name: str           # Full language name
    confidence: float   # Detection confidence (0.0-1.0)
    word_count: int     # Words in this language


@dataclass
class WordCountResult:
    """Result of word counting operation."""
    text: str
    total_words: int
    language_breakdown: Dict[str, int]
    detected_languages: List[LanguageInfo]
    processing_time: float
    metadata: Dict[str, Any]


@dataclass
class WordCountError:
    """Error information for word counting operations."""
    error_type: str
    message: str
    suggestion: str
    timestamp: datetime