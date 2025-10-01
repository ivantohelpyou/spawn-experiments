#!/usr/bin/env python3
"""
Tests for Story-to-Limerick Converter
"""

import unittest
from unittest.mock import patch, MagicMock
from limerick_converter import LimerickConverter


class TestSyllableCounter(unittest.TestCase):
    """Test syllable counting functionality."""

    def setUp(self):
        """Set up test converter."""
        with patch('limerick_converter.LimerickConverter._verify_ollama'):
            self.converter = LimerickConverter()

    def test_count_syllables_simple(self):
        """Test syllable counting for simple words."""
        test_cases = [
            ("cat", 1),
            ("hello", 2),
            ("computer", 3),
            ("programming", 3),
            ("night", 1),
            ("delight", 2),
        ]

        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.converter._count_syllables(word)
                self.assertEqual(result, expected, f"Expected {expected} syllables for '{word}', got {result}")

    def test_count_syllables_with_punctuation(self):
        """Test syllable counting strips punctuation."""
        self.assertEqual(self.converter._count_syllables("hello,"), 2)
        self.assertEqual(self.converter._count_syllables("world!"), 1)
        self.assertEqual(self.converter._count_syllables("'twas"), 1)

    def test_count_line_syllables(self):
        """Test counting syllables in a full line."""
        line = "A programmer stayed up at night"
        result = self.converter._count_line_syllables(line)
        # This should be around 9 syllables
        self.assertGreaterEqual(result, 7)
        self.assertLessEqual(result, 11)

    def test_count_syllables_empty(self):
        """Test syllable counting with empty string."""
        self.assertEqual(self.converter._count_syllables(""), 0)
        self.assertEqual(self.converter._count_syllables("   "), 0)


class TestLimerickValidation(unittest.TestCase):
    """Test limerick validation functionality."""

    def setUp(self):
        """Set up test converter."""
        with patch('limerick_converter.LimerickConverter._verify_ollama'):
            self.converter = LimerickConverter()

    def test_validate_correct_line_count(self):
        """Test validation accepts 5 lines."""
        lines = [
            "A programmer stayed up at night",
            "Debugging code was their fight",
            "Found one missing mark",
            "A semicolon stark",
            "Then slept with relief and delight"
        ]
        result = self.converter._validate_limerick(lines)
        self.assertIsNotNone(result)
        self.assertEqual(len(result["syllable_counts"]), 5)

    def test_validate_incorrect_line_count(self):
        """Test validation rejects wrong number of lines."""
        lines = [
            "Too few lines",
            "This won't work"
        ]
        result = self.converter._validate_limerick(lines)
        self.assertFalse(result["valid"])
        self.assertIn("Expected 5 lines", result["issues"][0])

    def test_validate_syllable_counts(self):
        """Test validation checks syllable counts."""
        lines = [
            "A programmer stayed up at night",  # ~9 syllables
            "Debugging code was their fight",    # ~8 syllables
            "Found one missing mark",            # ~5 syllables
            "A semicolon stark",                 # ~6 syllables
            "Then slept with relief and delight" # ~9 syllables
        ]
        result = self.converter._validate_limerick(lines)
        self.assertEqual(len(result["syllable_counts"]), 5)
        # Validate syllable counts are in expected ranges
        for i, count in enumerate(result["syllable_counts"]):
            if i in [0, 1, 4]:  # Long lines
                self.assertGreaterEqual(count, 7, f"Line {i+1} too short")
                self.assertLessEqual(count, 10, f"Line {i+1} too long")
            else:  # Short lines
                self.assertGreaterEqual(count, 4, f"Line {i+1} too short")
                self.assertLessEqual(count, 7, f"Line {i+1} too long")


class TestLimerickConverter(unittest.TestCase):
    """Test the main converter functionality."""

    def setUp(self):
        """Set up test converter."""
        with patch('limerick_converter.LimerickConverter._verify_ollama'):
            self.converter = LimerickConverter()

    def test_build_prompt(self):
        """Test prompt building."""
        story = "A cat sat on a mat."
        prompt = self.converter._build_prompt(story)

        self.assertIn("LIMERICK RULES", prompt)
        self.assertIn("AABBA", prompt)
        self.assertIn(story, prompt)
        self.assertIn("Return ONLY the 5 lines", prompt)

    def test_convert_empty_story(self):
        """Test conversion with empty story raises error."""
        with self.assertRaises(ValueError):
            self.converter.convert("")

        with self.assertRaises(ValueError):
            self.converter.convert("   ")

    @patch('limerick_converter.subprocess.run')
    def test_convert_success(self, mock_run):
        """Test successful conversion."""
        # Mock Ollama response
        mock_output = """A programmer stayed up at night,
Debugging code was their fight,
Found one missing mark,
A semicolon stark,
Then slept with relief and delight."""

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=mock_output,
            stderr=""
        )

        story = "A programmer stayed up late debugging and found a missing semicolon."
        result = self.converter.convert(story)

        self.assertIn("limerick", result)
        self.assertIn("lines", result)
        self.assertEqual(len(result["lines"]), 5)
        self.assertEqual(result["story"], story)
        self.assertEqual(result["model"], "llama3.2")

    @patch('limerick_converter.subprocess.run')
    def test_convert_with_validation(self, mock_run):
        """Test conversion includes validation."""
        mock_output = """A programmer stayed up at night,
Debugging code was their fight,
Found one missing mark,
A semicolon stark,
Then slept with relief and delight."""

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=mock_output,
            stderr=""
        )

        story = "Test story"
        result = self.converter.convert(story, validate=True)

        self.assertIn("validation", result)
        self.assertIsNotNone(result["validation"])
        self.assertIn("valid", result["validation"])
        self.assertIn("syllable_counts", result["validation"])

    @patch('limerick_converter.subprocess.run')
    def test_convert_without_validation(self, mock_run):
        """Test conversion can skip validation."""
        mock_output = """Line 1
Line 2
Line 3
Line 4
Line 5"""

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=mock_output,
            stderr=""
        )

        result = self.converter.convert("Test", validate=False)
        self.assertIsNone(result["validation"])

    @patch('limerick_converter.subprocess.run')
    def test_convert_to_json(self, mock_run):
        """Test JSON output."""
        mock_output = """Line 1
Line 2
Line 3
Line 4
Line 5"""

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=mock_output,
            stderr=""
        )

        result = self.converter.convert_to_json("Test story")
        self.assertIsInstance(result, str)
        # Should be valid JSON
        import json
        parsed = json.loads(result)
        self.assertIn("limerick", parsed)
        self.assertIn("lines", parsed)


class TestPromptTemplate(unittest.TestCase):
    """Test the prompt template structure."""

    def setUp(self):
        """Set up test converter."""
        with patch('limerick_converter.LimerickConverter._verify_ollama'):
            self.converter = LimerickConverter()

    def test_prompt_includes_all_required_elements(self):
        """Test prompt includes all required elements from spec."""
        story = "Test story"
        prompt = self.converter._build_prompt(story)

        required_elements = [
            "LIMERICK RULES",
            "Exactly 5 lines",
            "AABBA",
            "8-9 syllables",
            "5-6 syllables",
            "Anapestic",
            "EXAMPLE STRUCTURE",
            "STORY:",
            "INSTRUCTIONS:",
            "Return ONLY the 5 lines"
        ]

        for element in required_elements:
            with self.subTest(element=element):
                self.assertIn(element, prompt, f"Prompt missing required element: {element}")


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSyllableCounter))
    suite.addTests(loader.loadTestsFromTestCase(TestLimerickValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestLimerickConverter))
    suite.addTests(loader.loadTestsFromTestCase(TestPromptTemplate))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    import sys
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
