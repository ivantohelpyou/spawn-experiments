"""
Word counting module for the Multilingual Word Counter.
Implements language-specific word counting algorithms.
"""

import re
from typing import Dict, List
from collections import Counter

try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False

try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

from models import WordCountResult, ProcessingConfig


class WordCounter:
    """Counts words using language-specific algorithms."""

    def __init__(self, config: ProcessingConfig = None):
        """Initialize the word counter with configuration."""
        self.config = config or ProcessingConfig()
        self._setup_dependencies()

    def _setup_dependencies(self):
        """Setup required language processing dependencies."""
        if NLTK_AVAILABLE:
            try:
                # Download required NLTK data if not present
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                try:
                    nltk.download('punkt', quiet=True)
                except:
                    pass  # Continue without NLTK if download fails

    def count_words(self, text: str, language: str = None) -> int:
        """
        Count words in text using appropriate algorithm for language.

        Args:
            text: Input text to count
            language: Language code (if known)

        Returns:
            Number of words in the text
        """
        if not text or not text.strip():
            return 0

        # Clean text
        cleaned_text = self._clean_text(text)

        if not language:
            # Use default algorithm
            return self._count_words_default(cleaned_text)

        # Use language-specific algorithm
        if language in ['zh', 'zh-cn', 'zh-tw']:
            return self._count_words_chinese(cleaned_text)
        elif language in ['ja']:
            return self._count_words_japanese(cleaned_text)
        elif language in ['ar', 'he']:
            return self._count_words_rtl(cleaned_text)
        elif language in ['ko']:
            return self._count_words_korean(cleaned_text)
        else:
            return self._count_words_latin(cleaned_text)

    def get_word_list(self, text: str, language: str = None) -> List[str]:
        """
        Get list of words from text using language-appropriate tokenization.

        Args:
            text: Input text to tokenize
            language: Language code (if known)

        Returns:
            List of words
        """
        if not text or not text.strip():
            return []

        cleaned_text = self._clean_text(text)

        if not language:
            return self._get_words_default(cleaned_text)

        # Use language-specific tokenization
        if language in ['zh', 'zh-cn', 'zh-tw']:
            return self._get_words_chinese(cleaned_text)
        elif language in ['ja']:
            return self._get_words_japanese(cleaned_text)
        elif language in ['ar', 'he']:
            return self._get_words_rtl(cleaned_text)
        elif language in ['ko']:
            return self._get_words_korean(cleaned_text)
        else:
            return self._get_words_latin(cleaned_text)

    def count_by_language(self, text: str, language_segments: Dict[str, List[str]]) -> Dict[str, int]:
        """
        Count words by language for mixed-language texts.

        Args:
            text: Full text
            language_segments: Dictionary mapping languages to text segments

        Returns:
            Dictionary mapping language codes to word counts
        """
        counts = {}

        for language, segments in language_segments.items():
            total_count = 0
            for segment in segments:
                total_count += self.count_words(segment, language)
            counts[language] = total_count

        return counts

    def get_frequency_distribution(self, text: str, language: str = None, top_n: int = 10) -> List[tuple]:
        """
        Get frequency distribution of words.

        Args:
            text: Input text
            language: Language code
            top_n: Number of top words to return

        Returns:
            List of (word, count) tuples sorted by frequency
        """
        words = self.get_word_list(text, language)

        # Filter out very short words and common stop patterns
        filtered_words = [
            word.lower() for word in words
            if len(word) > 2 and word.isalpha()
        ]

        counter = Counter(filtered_words)
        return counter.most_common(top_n)

    def _clean_text(self, text: str) -> str:
        """Clean text for word counting."""
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _count_words_default(self, text: str) -> int:
        """Default word counting using simple tokenization."""
        words = self._get_words_default(text)
        return len([word for word in words if word.strip()])

    def _get_words_default(self, text: str) -> List[str]:
        """Default word extraction using simple tokenization."""
        # Split on whitespace and common punctuation
        words = re.findall(r'\b\w+\b', text, re.UNICODE)
        return words

    def _count_words_latin(self, text: str) -> int:
        """Count words for Latin-script languages (English, Spanish, French, etc.)."""
        if NLTK_AVAILABLE:
            try:
                words = word_tokenize(text)
                return len([word for word in words if word.isalpha()])
            except:
                pass  # Fall back to default if NLTK fails

        return self._count_words_default(text)

    def _get_words_latin(self, text: str) -> List[str]:
        """Get words for Latin-script languages."""
        if NLTK_AVAILABLE:
            try:
                words = word_tokenize(text)
                return [word for word in words if word.isalpha()]
            except:
                pass

        return self._get_words_default(text)

    def _count_words_chinese(self, text: str) -> int:
        """Count words for Chinese text using jieba segmentation."""
        if JIEBA_AVAILABLE:
            try:
                words = jieba.lcut(text)
                # Filter out whitespace and single characters
                return len([word for word in words if word.strip() and len(word) > 1])
            except:
                pass

        # Fallback: treat each character as a word (rough approximation)
        return len([char for char in text if char.strip() and not char.isspace()])

    def _get_words_chinese(self, text: str) -> List[str]:
        """Get words for Chinese text."""
        if JIEBA_AVAILABLE:
            try:
                words = jieba.lcut(text)
                return [word for word in words if word.strip() and len(word) > 1]
            except:
                pass

        # Fallback: return individual characters
        return [char for char in text if char.strip() and not char.isspace()]

    def _count_words_japanese(self, text: str) -> int:
        """Count words for Japanese text."""
        # For now, use character-based counting as approximation
        # In a full implementation, would use MeCab or similar
        japanese_chars = re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', text)
        latin_words = re.findall(r'\b[A-Za-z]+\b', text)

        # Rough approximation: 2 characters per word for Japanese text
        return len(japanese_chars) // 2 + len(latin_words)

    def _get_words_japanese(self, text: str) -> List[str]:
        """Get words for Japanese text."""
        # Simple implementation - in practice would use proper Japanese tokenizer
        words = []

        # Extract Latin words
        latin_words = re.findall(r'\b[A-Za-z]+\b', text)
        words.extend(latin_words)

        # Extract Japanese character sequences (rough approximation)
        japanese_sequences = re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]+', text)
        for seq in japanese_sequences:
            # Split into chunks of 2-3 characters as rough word approximation
            for i in range(0, len(seq), 2):
                word = seq[i:i+2]
                if word:
                    words.append(word)

        return words

    def _count_words_rtl(self, text: str) -> int:
        """Count words for Right-to-Left languages (Arabic, Hebrew)."""
        # Use Unicode word boundaries
        words = re.findall(r'\b\w+\b', text, re.UNICODE)
        return len([word for word in words if word.strip()])

    def _get_words_rtl(self, text: str) -> List[str]:
        """Get words for RTL languages."""
        words = re.findall(r'\b\w+\b', text, re.UNICODE)
        return [word for word in words if word.strip()]

    def _count_words_korean(self, text: str) -> int:
        """Count words for Korean text."""
        # Korean uses spaces between words, so can use space-based counting
        # but also handle Hangul syllables
        hangul_words = re.findall(r'[\uAC00-\uD7AF]+', text)
        latin_words = re.findall(r'\b[A-Za-z]+\b', text)

        return len(hangul_words) + len(latin_words)

    def _get_words_korean(self, text: str) -> List[str]:
        """Get words for Korean text."""
        words = []

        # Extract Hangul words
        hangul_words = re.findall(r'[\uAC00-\uD7AF]+', text)
        words.extend(hangul_words)

        # Extract Latin words
        latin_words = re.findall(r'\b[A-Za-z]+\b', text)
        words.extend(latin_words)

        return words