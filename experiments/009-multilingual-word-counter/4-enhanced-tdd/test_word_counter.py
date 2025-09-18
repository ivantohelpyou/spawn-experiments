"""
Test-Driven Development for Multilingual Word Counter
Starting with the simplest feature: Basic English word counting
"""

import unittest
from typing import Dict, List
from word_counter import MultilingualWordCounter, WordCountResult, LanguageDetection


class TestBasicWordCounting(unittest.TestCase):
    """Test basic English word counting functionality"""

    def setUp(self):
        self.counter = MultilingualWordCounter()

    def test_empty_string_returns_zero_words(self):
        """
        Test: Empty string should return zero word count

        This test verifies that our word counter correctly handles
        the edge case of empty input. If implementation incorrectly
        counts empty strings as having words, this test will catch it.
        """
        result = self.counter.count_words("")
        self.assertEqual(result.total_words, 0)
        self.assertEqual(result.total_chars, 0)

    def test_single_word_returns_one(self):
        """
        Test: Single word should return count of 1

        This is the most basic positive case. If implementation
        has fundamental issues (like counting characters instead of words,
        or not recognizing word boundaries), this will catch it.
        """
        result = self.counter.count_words("hello")
        self.assertEqual(result.total_words, 1)
        self.assertEqual(result.total_chars, 5)

    def test_multiple_words_separated_by_spaces(self):
        """
        Test: Multiple words separated by single spaces

        This tests basic word boundary detection using spaces.
        If implementation doesn't properly split on whitespace,
        or counts spaces as words, this test will fail.
        """
        result = self.counter.count_words("hello world test")
        self.assertEqual(result.total_words, 3)
        self.assertEqual(result.total_chars, 14)  # excluding spaces

    def test_multiple_spaces_between_words(self):
        """
        Test: Multiple spaces between words should still work

        This tests that excessive whitespace doesn't create phantom words.
        If implementation naively splits on single spaces or doesn't
        handle multiple consecutive spaces, this will catch it.
        """
        result = self.counter.count_words("hello    world")
        self.assertEqual(result.total_words, 2)
        self.assertEqual(result.total_chars, 10)

    def test_words_with_punctuation(self):
        """
        Test: Words with punctuation should be counted as words

        This tests that punctuation attached to words doesn't break
        word recognition. If implementation incorrectly excludes
        punctuated words or counts punctuation separately, this catches it.
        """
        result = self.counter.count_words("Hello, world! How are you?")
        self.assertEqual(result.total_words, 5)  # Hello, world, How, are, you
        # Characters: Hello(5) + world(5) + How(3) + are(3) + you(3) = 19
        self.assertEqual(result.total_chars, 19)


class TestLanguageDetection(unittest.TestCase):
    """Test language detection functionality"""

    def setUp(self):
        self.counter = MultilingualWordCounter()

    def test_detect_english_language(self):
        """
        Test: English text should be detected as English

        This tests basic language detection for English text.
        If implementation doesn't detect languages or defaults
        to wrong language, this will catch it.
        """
        text = "Hello world this is English text"
        result = self.counter.detect_language(text)

        # Should return list of LanguageDetection objects
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        # Primary language should be English
        primary = result[0]
        self.assertEqual(primary.language_code, "en")
        self.assertGreater(primary.confidence, 0.5)

    def test_detect_short_text_low_confidence(self):
        """
        Test: Very short text should have lower confidence

        This tests that confidence scoring works properly.
        Short texts should have lower confidence than long ones.
        """
        short_text = "Hello"
        long_text = "Hello world this is a much longer English text with many words"

        short_result = self.counter.detect_language(short_text)
        long_result = self.counter.detect_language(long_text)

        # Both should detect English but long text should have higher confidence
        self.assertEqual(short_result[0].language_code, "en")
        self.assertEqual(long_result[0].language_code, "en")
        self.assertLess(short_result[0].confidence, long_result[0].confidence)

    def test_detect_empty_text(self):
        """
        Test: Empty text should return empty detection results

        Edge case: empty input should not crash but return
        empty results gracefully.
        """
        result = self.counter.detect_language("")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


class TestIntegratedWordCountingWithLanguage(unittest.TestCase):
    """Test integrated word counting with language detection"""

    def setUp(self):
        self.counter = MultilingualWordCounter()

    def test_count_words_includes_language_detection(self):
        """
        Test: Word counting should include language detection in results

        This tests the integration of word counting and language detection.
        The result should include both word counts and detected language info.
        """
        text = "Hello world this is a test"
        result = self.counter.count_words(text)

        # Basic word counting should work
        self.assertEqual(result.total_words, 6)

        # Language detection should be integrated
        self.assertEqual(result.primary_language, "en")
        self.assertGreater(result.primary_confidence, 0.5)

    def test_count_words_with_detailed_language_stats(self):
        """
        Test: Word counting should provide detailed language statistics

        This tests that the result includes language-specific statistics
        when multiple language features are detected.
        """
        text = "Hello world how are you today"
        result = self.counter.count_words(text)

        # Should have language-specific stats
        self.assertIsNotNone(result.languages)
        self.assertIn("en", result.languages)

        english_stats = result.languages["en"]
        self.assertEqual(english_stats.language_code, "en")
        self.assertEqual(english_stats.word_count, 6)
        self.assertGreater(english_stats.confidence, 0.5)

    def test_short_text_affects_both_counting_and_detection(self):
        """
        Test: Short text should have appropriate handling in both systems

        This tests that short text is handled consistently across
        word counting and language detection.
        """
        text = "Hi"
        result = self.counter.count_words(text)

        # Basic counts should work
        self.assertEqual(result.total_words, 1)
        self.assertEqual(result.total_chars, 2)

        # Language detection should work but with lower confidence
        self.assertEqual(result.primary_language, "en")
        self.assertLess(result.primary_confidence, 0.8)  # Should be lower confidence for short text


if __name__ == '__main__':
    unittest.main()