"""
Test suite for Iambic Pentameter Converter - Adaptive/Validated TDD
"""

import unittest
from unittest.mock import patch, MagicMock
from iambic_converter import SyllableCounter, OllamaClient, IambicConverter


class TestSyllableCounter(unittest.TestCase):
    """Tests for syllable counting - COMPLEX ALGORITHM - VALIDATED"""

    def setUp(self):
        self.counter = SyllableCounter()

    def test_single_syllable_words(self):
        """Test counting single syllable words"""
        self.assertEqual(self.counter.count("cat"), 1)
        self.assertEqual(self.counter.count("dog"), 1)
        self.assertEqual(self.counter.count("run"), 1)
        self.assertEqual(self.counter.count("jump"), 1)

    def test_two_syllable_words(self):
        """Test counting two syllable words"""
        self.assertEqual(self.counter.count("happy"), 2)
        self.assertEqual(self.counter.count("running"), 2)
        self.assertEqual(self.counter.count("table"), 2)
        self.assertEqual(self.counter.count("water"), 2)

    def test_three_syllable_words(self):
        """Test counting three syllable words"""
        self.assertEqual(self.counter.count("beautiful"), 3)
        self.assertEqual(self.counter.count("wonderful"), 3)
        self.assertEqual(self.counter.count("energy"), 3)

    def test_multi_syllable_words(self):
        """Test counting words with 4+ syllables"""
        self.assertEqual(self.counter.count("incredible"), 4)
        self.assertEqual(self.counter.count("understanding"), 4)

    def test_silent_e(self):
        """Test words with silent 'e' at the end"""
        self.assertEqual(self.counter.count("make"), 1)
        self.assertEqual(self.counter.count("time"), 1)
        self.assertEqual(self.counter.count("wine"), 1)
        self.assertEqual(self.counter.count("fire"), 1)

    def test_vowel_groups(self):
        """Test words with vowel groups (diphthongs)"""
        self.assertEqual(self.counter.count("rain"), 1)
        self.assertEqual(self.counter.count("boat"), 1)
        self.assertEqual(self.counter.count("coin"), 1)

    def test_empty_string(self):
        """Test empty string returns 0"""
        self.assertEqual(self.counter.count(""), 0)

    def test_capitalization(self):
        """Test that capitalization doesn't affect count"""
        self.assertEqual(self.counter.count("Hello"), 2)
        self.assertEqual(self.counter.count("HELLO"), 2)
        self.assertEqual(self.counter.count("hello"), 2)

    def test_punctuation(self):
        """Test that punctuation is handled correctly"""
        self.assertEqual(self.counter.count("hello!"), 2)
        self.assertEqual(self.counter.count("world,"), 1)
        self.assertEqual(self.counter.count("it's"), 1)


class TestOllamaClient(unittest.TestCase):
    """Tests for Ollama client - SIMPLE INTEGRATION - NO VALIDATION NEEDED"""

    @patch('subprocess.run')
    def test_generate_success(self, mock_run):
        """Test successful generation"""
        mock_run.return_value = MagicMock(stdout="Generated text\n")
        client = OllamaClient()
        result = client.generate("test prompt")
        self.assertEqual(result, "Generated text")

    @patch('subprocess.run')
    def test_generate_timeout(self, mock_run):
        """Test timeout handling"""
        from subprocess import TimeoutExpired
        mock_run.side_effect = TimeoutExpired("cmd", 30)
        client = OllamaClient()
        result = client.generate("test prompt")
        self.assertEqual(result, "")

    @patch('subprocess.run')
    def test_generate_ollama_not_found(self, mock_run):
        """Test handling when Ollama is not installed"""
        mock_run.side_effect = FileNotFoundError()
        client = OllamaClient()
        with self.assertRaises(RuntimeError):
            client.generate("test prompt")


class TestIambicConverter(unittest.TestCase):
    """Tests for main converter - BUSINESS LOGIC - VALIDATED"""

    def setUp(self):
        self.converter = IambicConverter()

    def test_count_syllables_simple(self):
        """Test syllable counting in sentences"""
        self.assertEqual(self.converter.count_syllables("the cat"), 2)
        self.assertEqual(self.converter.count_syllables("hello world"), 3)

    def test_count_syllables_with_punctuation(self):
        """Test syllable counting with punctuation"""
        self.assertEqual(self.converter.count_syllables("Hello, world!"), 3)

    @patch.object(OllamaClient, 'generate')
    def test_convert_calls_ollama(self, mock_generate):
        """Test that convert properly calls Ollama"""
        mock_generate.return_value = "The cat doth sit upon the mat so fine"
        result = self.converter.convert("The cat sat on the mat")
        mock_generate.assert_called_once()
        self.assertIn("The cat", result)


if __name__ == '__main__':
    unittest.main()
