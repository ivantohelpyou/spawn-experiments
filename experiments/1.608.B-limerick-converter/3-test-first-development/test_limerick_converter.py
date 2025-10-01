"""Test suite for limerick converter - TDD approach."""
import unittest
from limerick_converter import LimerickConverter


class TestLimerickConverter(unittest.TestCase):
    """Test cases for LimerickConverter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.converter = LimerickConverter()

    def test_validate_limerick_structure_correct(self):
        """Test that a valid limerick structure passes validation."""
        valid_limerick = [
            "A programmer stayed up at night,",
            "Debugging code was their fight,",
            "Found one missing mark,",
            "A semicolon stark,",
            "Then slept with relief and delight."
        ]

        result = self.converter.validate_limerick_structure(valid_limerick)
        self.assertTrue(result['valid'])
        self.assertEqual(result['line_count'], 5)
        self.assertEqual(len(result['issues']), 0)

    def test_validate_limerick_structure_wrong_line_count(self):
        """Test that wrong line count fails validation."""
        invalid_limerick = [
            "A programmer stayed up at night,",
            "Debugging code was their fight,",
            "Found one missing mark,"
        ]

        result = self.converter.validate_limerick_structure(invalid_limerick)
        self.assertFalse(result['valid'])
        self.assertIn('Must have exactly 5 lines', str(result['issues']))

    def test_count_syllables_simple_words(self):
        """Test syllable counting for simple words."""
        test_cases = [
            ("cat", 1),
            ("happy", 2),
            ("beautiful", 3),
            ("night", 1),
        ]

        for word, expected_count in test_cases:
            with self.subTest(word=word):
                count = self.converter.count_syllables(word)
                self.assertEqual(count, expected_count)

    def test_count_syllables_in_line(self):
        """Test counting syllables in a full line."""
        line = "A programmer stayed up at night,"
        count = self.converter.count_syllables_in_line(line)
        # Should be 8-9 syllables
        self.assertGreaterEqual(count, 8)
        self.assertLessEqual(count, 9)

    def test_generate_limerick_from_story(self):
        """Test that we can generate a limerick from a story using LLM."""
        story = "A young programmer stayed up all night debugging code, finally finding a missing semicolon at 3am."

        result = self.converter.generate_limerick(story)

        # Check result structure
        self.assertIn('limerick', result)
        self.assertIn('lines', result)
        self.assertIsInstance(result['lines'], list)
        self.assertEqual(len(result['lines']), 5)


if __name__ == '__main__':
    unittest.main()
