"""
Test suite for Iambic Pentameter Converter
Following TDD methodology - tests written FIRST
"""

import unittest
from unittest.mock import Mock, patch
from iambic_converter import (
    count_syllables,
    count_line_syllables,
    is_valid_iambic_pentameter,
    convert_prose_to_iambic,
    convert_story_to_iambic
)


class TestSyllableCounter(unittest.TestCase):
    """Test syllable counting functionality"""

    def test_count_syllables_single_syllable(self):
        """Test counting syllables in single-syllable words"""
        self.assertEqual(count_syllables("cat"), 1)
        self.assertEqual(count_syllables("dog"), 1)
        self.assertEqual(count_syllables("the"), 1)

    def test_count_syllables_two_syllables(self):
        """Test counting syllables in two-syllable words"""
        self.assertEqual(count_syllables("hello"), 2)
        self.assertEqual(count_syllables("water"), 2)
        self.assertEqual(count_syllables("summer"), 2)

    def test_count_syllables_multiple_syllables(self):
        """Test counting syllables in multi-syllable words"""
        self.assertEqual(count_syllables("beautiful"), 3)
        self.assertEqual(count_syllables("temperature"), 4)
        self.assertEqual(count_syllables("necessary"), 4)


class TestLineSyllableCounter(unittest.TestCase):
    """Test line syllable counting functionality"""

    def test_count_line_syllables_simple(self):
        """Test counting syllables in simple line"""
        self.assertEqual(count_line_syllables("The cat sat on the mat"), 6)

    def test_count_line_syllables_iambic_pentameter(self):
        """Test counting syllables in iambic pentameter line (10 syllables)"""
        # "Shall I compare thee to a summer's day?" - Shakespeare
        self.assertEqual(count_line_syllables("Shall I compare thee to a summer's day"), 10)

    def test_count_line_syllables_empty(self):
        """Test counting syllables in empty line"""
        self.assertEqual(count_line_syllables(""), 0)


class TestIambicPentameterValidator(unittest.TestCase):
    """Test iambic pentameter validation"""

    def test_valid_iambic_pentameter(self):
        """Test valid iambic pentameter lines"""
        self.assertTrue(is_valid_iambic_pentameter("Shall I compare thee to a summer's day"))

    def test_invalid_too_few_syllables(self):
        """Test line with too few syllables"""
        self.assertFalse(is_valid_iambic_pentameter("The cat sat"))

    def test_invalid_too_many_syllables(self):
        """Test line with too many syllables"""
        self.assertFalse(is_valid_iambic_pentameter("The beautiful cat sat on the comfortable mat"))


class TestProseToIambicConverter(unittest.TestCase):
    """Test prose to iambic pentameter conversion"""

    @patch('iambic_converter.requests.post')
    def test_convert_prose_to_iambic_single_line(self, mock_post):
        """Test converting prose to single iambic pentameter line"""
        # Mock Ollama API response
        mock_response = Mock()
        mock_response.json.return_value = {"response": "Upon the mat the feline took its rest"}
        mock_post.return_value = mock_response

        result = convert_prose_to_iambic("The cat sat on the mat")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    @patch('iambic_converter.requests.post')
    def test_convert_prose_handles_empty_input(self, mock_post):
        """Test handling of empty input"""
        result = convert_prose_to_iambic("")
        self.assertEqual(result, "")


class TestStoryConverter(unittest.TestCase):
    """Test full story conversion"""

    @patch('iambic_converter.convert_prose_to_iambic')
    def test_convert_story_multiple_lines(self, mock_convert):
        """Test converting multi-line story"""
        mock_convert.return_value = "The verse conversion of this line\nAnother line in iambic form"

        story = "Once upon a time, there was a cat. The cat sat on a mat."
        result = convert_story_to_iambic(story)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        mock_convert.assert_called_once()

    @patch('iambic_converter.convert_prose_to_iambic')
    def test_convert_story_empty(self, mock_convert):
        """Test converting empty story"""
        result = convert_story_to_iambic("")
        self.assertEqual(result, "")
        mock_convert.assert_not_called()


if __name__ == '__main__':
    unittest.main()
