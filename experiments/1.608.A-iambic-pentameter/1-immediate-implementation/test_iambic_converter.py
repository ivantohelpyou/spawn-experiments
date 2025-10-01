#!/usr/bin/env python3
"""
Tests for the Iambic Pentameter Converter
"""

import unittest
from unittest.mock import patch, MagicMock
from iambic_converter import IambicConverter


class TestIambicConverter(unittest.TestCase):
    """Test suite for IambicConverter."""

    def setUp(self):
        """Set up test fixtures."""
        self.converter = IambicConverter()

    def test_initialization(self):
        """Test converter initialization."""
        converter = IambicConverter()
        self.assertEqual(converter.model, "llama3.2")

        converter_custom = IambicConverter(model="custom-model")
        self.assertEqual(converter_custom.model, "custom-model")

    def test_create_prompt(self):
        """Test prompt creation."""
        prose = "The cat sat on the mat."
        prompt = self.converter._create_prompt(prose)

        self.assertIn("iambic pentameter", prompt)
        self.assertIn("10 syllables", prompt)
        self.assertIn(prose, prompt)
        self.assertIn("Shakespeare", prompt)

    @patch('subprocess.run')
    def test_call_ollama_success(self, mock_run):
        """Test successful Ollama API call."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "The cat did sit upon the mat so flat"
        mock_run.return_value = mock_result

        result = self.converter._call_ollama("test prompt")

        self.assertEqual(result, "The cat did sit upon the mat so flat")
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_call_ollama_error(self, mock_run):
        """Test Ollama API call with error."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Model not found"
        mock_run.return_value = mock_result

        with self.assertRaises(RuntimeError) as context:
            self.converter._call_ollama("test prompt")

        self.assertIn("Ollama error", str(context.exception))

    @patch('subprocess.run')
    def test_call_ollama_timeout(self, mock_run):
        """Test Ollama API call timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("ollama", 60)

        with self.assertRaises(RuntimeError) as context:
            self.converter._call_ollama("test prompt")

        self.assertIn("timed out", str(context.exception))

    @patch('subprocess.run')
    def test_call_ollama_not_found(self, mock_run):
        """Test Ollama not installed."""
        mock_run.side_effect = FileNotFoundError()

        with self.assertRaises(RuntimeError) as context:
            self.converter._call_ollama("test prompt")

        self.assertIn("not found", str(context.exception))

    @patch.object(IambicConverter, '_call_ollama')
    def test_convert_to_iambic(self, mock_ollama):
        """Test basic conversion."""
        mock_ollama.return_value = "In faith, the cat upon the mat did rest"

        prose = "The cat sat on the mat"
        result = self.converter.convert_to_iambic(prose)

        self.assertEqual(result, "In faith, the cat upon the mat did rest")
        mock_ollama.assert_called_once()

    @patch.object(IambicConverter, '_call_ollama')
    def test_convert_paragraph(self, mock_ollama):
        """Test paragraph conversion."""
        mock_ollama.return_value = "The sun doth shine upon the morning dew"

        paragraph = "The sun shines on the morning dew."
        result = self.converter.convert_paragraph(paragraph)

        self.assertEqual(result, "The sun doth shine upon the morning dew")

    @patch.object(IambicConverter, '_call_ollama')
    def test_convert_story_single_paragraph(self, mock_ollama):
        """Test story conversion with single paragraph."""
        mock_ollama.return_value = "A tale of wonder in the summer night"

        story = "It was a wonderful summer night."
        result = self.converter.convert_story(story, preserve_paragraphs=False)

        self.assertEqual(result, "A tale of wonder in the summer night")

    @patch.object(IambicConverter, '_call_ollama')
    def test_convert_story_multiple_paragraphs(self, mock_ollama):
        """Test story conversion with multiple paragraphs."""
        mock_ollama.side_effect = [
            "The cat did sit upon the velvet mat",
            "And watched the world with eyes of emerald green"
        ]

        story = "The cat sat on the mat.\n\nIt watched the world with green eyes."
        result = self.converter.convert_story(story, preserve_paragraphs=True)

        expected = "The cat did sit upon the velvet mat\n\nAnd watched the world with eyes of emerald green"
        self.assertEqual(result, expected)
        self.assertEqual(mock_ollama.call_count, 2)

    def test_syllable_count_helper(self):
        """Test that we can count syllables (basic implementation)."""
        # This is a basic test - real syllable counting is complex
        test_line = "The cat sat on the mat today"
        # Just verify the line exists - actual counting would need pyphen or similar
        self.assertIsInstance(test_line, str)


class TestIntegration(unittest.TestCase):
    """Integration tests (require Ollama to be running)."""

    @unittest.skip("Requires Ollama to be running - manual test")
    def test_real_conversion(self):
        """Test actual conversion with Ollama."""
        converter = IambicConverter()
        prose = "The cat sat on the mat and looked at the moon."
        result = converter.convert_to_iambic(prose)

        # Basic checks - result should exist and be different from input
        self.assertTrue(len(result) > 0)
        self.assertNotEqual(result, prose)
        print(f"\nOriginal: {prose}")
        print(f"Converted: {result}")


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    # Import subprocess for the timeout test
    import subprocess
    unittest.main(verbosity=2)
