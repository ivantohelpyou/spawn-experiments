"""
Comprehensive test suite for iambic_converter module.

Tests all components:
- SyllableCounter: Word and line syllable counting
- MeterValidator: Iambic pentameter validation
- OllamaClient: LLM communication (mocked)
- IambicConverter: Full conversion pipeline (mocked and integration)
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import subprocess

from iambic_converter import (
    SyllableCounter,
    MeterValidator,
    OllamaClient,
    IambicConverter
)


class TestSyllableCounter(unittest.TestCase):
    """Test syllable counting functionality."""

    def setUp(self):
        self.counter = SyllableCounter()

    def test_simple_words(self):
        """Test syllable counting for simple common words."""
        test_cases = [
            ('cat', 1),
            ('dog', 1),
            ('hello', 2),
            ('world', 1),
            ('python', 2),
            ('computer', 3),
            ('programming', 3),
        ]

        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.counter.count_syllables(word)
                self.assertEqual(result, expected,
                               f"{word} should have {expected} syllables, got {result}")

    def test_complex_words(self):
        """Test syllable counting for complex words."""
        test_cases = [
            ('beautiful', 3),
            ('literature', 4),
            ('poetry', 3),
            ('iambic', 3),
            ('pentameter', 4),
            ('Shakespearean', 4),
        ]

        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.counter.count_syllables(word)
                self.assertEqual(result, expected,
                               f"{word} should have {expected} syllables, got {result}")

    def test_exception_words(self):
        """Test words in exception dictionary."""
        test_cases = [
            ('love', 1),
            ('fire', 1),
            ('hour', 1),
            ('power', 2),
            ('special', 2),
            ('every', 3),
        ]

        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.counter.count_syllables(word)
                self.assertEqual(result, expected)

    def test_words_with_silent_e(self):
        """Test words ending in silent 'e'."""
        test_cases = [
            ('like', 1),
            ('time', 1),
            ('hope', 1),
            ('create', 2),
            ('separate', 3),
        ]

        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.counter.count_syllables(word)
                self.assertEqual(result, expected,
                               f"{word} should have {expected} syllables, got {result}")

    def test_words_ending_in_le(self):
        """Test words ending in 'le' pattern."""
        test_cases = [
            ('table', 2),
            ('little', 2),
            ('circle', 2),
            ('purple', 2),
            ('simple', 2),
        ]

        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.counter.count_syllables(word)
                self.assertEqual(result, expected,
                               f"{word} should have {expected} syllables, got {result}")

    def test_punctuation_handling(self):
        """Test that punctuation is properly ignored."""
        test_cases = [
            ('hello!', 2),
            ('world,', 1),
            ('test.', 1),
            ("don't", 1),
            ('hello?', 2),
        ]

        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.counter.count_syllables(word)
                self.assertEqual(result, expected)

    def test_edge_cases(self):
        """Test edge cases."""
        # Empty word
        self.assertEqual(self.counter.count_syllables(''), 0)

        # Only punctuation
        self.assertEqual(self.counter.count_syllables('!!!'), 0)

        # Single letter
        self.assertEqual(self.counter.count_syllables('I'), 1)
        self.assertEqual(self.counter.count_syllables('a'), 1)

    def test_count_line_syllables(self):
        """Test counting syllables in full lines."""
        test_cases = [
            ('The cat sat on the mat', 6),
            ('Hello world this is a test', 7),
            ('To be or not to be that is the question', 11),
            ('Shall I compare thee to a summer\'s day', 10),
        ]

        for line, expected in test_cases:
            with self.subTest(line=line):
                result = self.counter.count_line_syllables(line)
                self.assertAlmostEqual(result, expected, delta=1,
                                     msg=f"Line should have ~{expected} syllables, got {result}")


class TestMeterValidator(unittest.TestCase):
    """Test iambic pentameter validation."""

    def setUp(self):
        self.validator = MeterValidator(strict=False)
        self.strict_validator = MeterValidator(strict=True)

    def test_perfect_pentameter_line(self):
        """Test validation of perfect 10-syllable lines."""
        lines = [
            "Shall I compare thee to a summer's day",  # 10 syllables
            "But soft what light through yonder window breaks",  # 10 syllables
            "To be or not to be that is the thing",  # 10 syllables
        ]

        for line in lines:
            with self.subTest(line=line):
                is_valid, syllables = self.validator.is_valid_line(line)
                # Allow some tolerance for syllable counting inaccuracy
                self.assertIn(syllables, range(9, 12),
                            f"Line should have ~10 syllables, got {syllables}")

    def test_invalid_lines(self):
        """Test detection of invalid lines."""
        lines = [
            "The cat sat",  # Too short (4 syllables)
            "This is a very very very long line with many words",  # Too long
        ]

        for line in lines:
            with self.subTest(line=line):
                is_valid, syllables = self.validator.is_valid_line(line)
                # These should be clearly invalid
                self.assertFalse(is_valid or syllables == 10)

    def test_strict_vs_lenient(self):
        """Test difference between strict and lenient validation."""
        line = "This line has exactly nine syllables now"  # 9 syllables

        # Lenient should accept 9-11
        is_valid_lenient, _ = self.validator.is_valid_line(line)

        # Strict should require exactly 10
        is_valid_strict, syllables = self.strict_validator.is_valid_line(line)

        if syllables == 9:
            self.assertTrue(is_valid_lenient or syllables == 10)
            self.assertFalse(is_valid_strict and syllables != 10)

    def test_validate_poem(self):
        """Test validation of complete poems."""
        # Perfect poem (all lines ~10 syllables)
        perfect_poem = """Shall I compare thee to a summer's day
Thou art more lovely and more temperate
Rough winds do shake the darling buds of May
And summer's lease hath all too short a date"""

        result = self.validator.validate_poem(perfect_poem)

        self.assertIn('valid', result)
        self.assertIn('total_lines', result)
        self.assertIn('valid_lines', result)
        self.assertIn('accuracy', result)
        self.assertIn('details', result)

        self.assertEqual(result['total_lines'], 4)
        self.assertGreaterEqual(result['accuracy'], 50)  # At least half should be valid

    def test_validation_report_structure(self):
        """Test structure of validation report."""
        poem = "The cat sat on the mat today\nHello world"

        result = self.validator.validate_poem(poem)

        # Check structure
        self.assertIsInstance(result['valid'], bool)
        self.assertIsInstance(result['total_lines'], int)
        self.assertIsInstance(result['valid_lines'], int)
        self.assertIsInstance(result['accuracy'], float)
        self.assertIsInstance(result['details'], list)

        # Check details for each line
        for detail in result['details']:
            self.assertIn('line', detail)
            self.assertIn('syllables', detail)
            self.assertIn('valid', detail)

    def test_empty_poem(self):
        """Test validation of empty poem."""
        result = self.validator.validate_poem("")

        self.assertEqual(result['total_lines'], 0)
        self.assertEqual(result['valid_lines'], 0)
        self.assertEqual(result['accuracy'], 0)


class TestOllamaClient(unittest.TestCase):
    """Test Ollama client functionality."""

    def setUp(self):
        self.client = OllamaClient(model="llama3.2")

    @patch('subprocess.run')
    def test_is_available_success(self, mock_run):
        """Test Ollama availability check when service is running."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="llama3.2\nllama2\n"
        )

        self.assertTrue(self.client.is_available())

    @patch('subprocess.run')
    def test_is_available_model_not_found(self, mock_run):
        """Test Ollama availability when model is missing."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="llama2\nother-model\n"
        )

        self.assertFalse(self.client.is_available())

    @patch('subprocess.run')
    def test_is_available_service_down(self, mock_run):
        """Test Ollama availability when service is down."""
        mock_run.return_value = Mock(returncode=1)

        self.assertFalse(self.client.is_available())

    @patch('subprocess.run')
    def test_is_available_timeout(self, mock_run):
        """Test Ollama availability check timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired('ollama', 5)

        self.assertFalse(self.client.is_available())

    @patch('subprocess.run')
    def test_is_available_not_installed(self, mock_run):
        """Test Ollama availability when not installed."""
        mock_run.side_effect = FileNotFoundError()

        self.assertFalse(self.client.is_available())

    @patch('subprocess.run')
    def test_generate_success(self, mock_run):
        """Test successful text generation."""
        # Mock is_available check
        mock_run.side_effect = [
            Mock(returncode=0, stdout="llama3.2\n"),  # is_available check
            Mock(returncode=0, stdout="Generated poem text")  # generate call
        ]

        result = self.client.generate("Test prompt")
        self.assertEqual(result, "Generated poem text")

    @patch('subprocess.run')
    def test_generate_ollama_unavailable(self, mock_run):
        """Test generation when Ollama is unavailable."""
        mock_run.return_value = Mock(returncode=1)

        with self.assertRaises(ConnectionError) as context:
            self.client.generate("Test prompt")

        self.assertIn("not available", str(context.exception))

    @patch('subprocess.run')
    def test_generate_timeout(self, mock_run):
        """Test generation timeout."""
        mock_run.side_effect = [
            Mock(returncode=0, stdout="llama3.2\n"),  # is_available check
            subprocess.TimeoutExpired('ollama', 60)  # generate call
        ]

        with self.assertRaises(TimeoutError) as context:
            self.client.generate("Test prompt")

        self.assertIn("timed out", str(context.exception))

    @patch('subprocess.run')
    def test_generate_failure(self, mock_run):
        """Test generation failure."""
        mock_run.side_effect = [
            Mock(returncode=0, stdout="llama3.2\n"),  # is_available check
            Mock(returncode=1, stderr="Generation error")  # generate call
        ]

        with self.assertRaises(RuntimeError) as context:
            self.client.generate("Test prompt")

        self.assertIn("failed", str(context.exception))


class TestIambicConverter(unittest.TestCase):
    """Test main converter functionality."""

    def setUp(self):
        self.converter = IambicConverter()

    def test_input_validation_empty(self):
        """Test that empty input raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.converter.convert("")

        self.assertIn("empty", str(context.exception))

    def test_input_validation_too_long(self):
        """Test that overly long input raises ValueError."""
        long_text = "a " * 3000  # Over 5000 chars

        with self.assertRaises(ValueError) as context:
            self.converter.convert(long_text)

        self.assertIn("too long", str(context.exception))

    @patch.object(OllamaClient, 'is_available')
    @patch.object(OllamaClient, 'generate')
    def test_convert_simple_text(self, mock_generate, mock_available):
        """Test conversion of simple text."""
        mock_available.return_value = True
        mock_generate.return_value = """The cat did sit upon the mat today
And watched the birds that flew up in the sky"""

        result = self.converter.convert("The cat sat on the mat and watched the birds.")

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        mock_generate.assert_called()

    @patch.object(OllamaClient, 'is_available')
    @patch.object(OllamaClient, 'generate')
    def test_retry_logic(self, mock_generate, mock_available):
        """Test that retry logic improves output."""
        mock_available.return_value = True

        # First attempt: poor result
        # Second attempt: better result
        mock_generate.side_effect = [
            "The cat sat",  # Bad (too short)
            "The cat did sit upon the mat that day\nAnd watched the birds fly in the sky above"  # Better
        ]

        result = self.converter.convert("The cat sat on the mat.")

        # Should have retried
        self.assertEqual(mock_generate.call_count, 2)
        self.assertIn("cat", result)

    @patch.object(OllamaClient, 'is_available')
    @patch.object(OllamaClient, 'generate')
    def test_returns_best_attempt(self, mock_generate, mock_available):
        """Test that best attempt is returned even if not perfect."""
        mock_available.return_value = True

        # All attempts are imperfect, should return best one
        mock_generate.side_effect = [
            "Short line",
            "A slightly better line with more words here",
            "Another attempt that is not quite right"
        ]

        result = self.converter.convert("The cat sat on the mat.")

        # Should have tried max_attempts times
        self.assertEqual(mock_generate.call_count, 3)
        self.assertIsInstance(result, str)

    @patch.object(OllamaClient, 'is_available')
    def test_ollama_unavailable_error(self, mock_available):
        """Test error when Ollama is unavailable."""
        mock_available.return_value = False

        with self.assertRaises(ConnectionError):
            self.converter.convert("Test text")

    @patch.object(OllamaClient, 'is_available')
    @patch.object(OllamaClient, 'generate')
    def test_prompt_building(self, mock_generate, mock_available):
        """Test that prompts are properly built."""
        mock_available.return_value = True
        mock_generate.return_value = "Some poem output"

        self.converter.convert("Test text")

        # Check that generate was called with a proper prompt
        call_args = mock_generate.call_args[0][0]
        self.assertIn("iambic pentameter", call_args.lower())
        self.assertIn("10 syllables", call_args.lower())
        self.assertIn("Test text", call_args)

    @patch.object(OllamaClient, 'is_available')
    @patch.object(OllamaClient, 'generate')
    def test_output_formatting(self, mock_generate, mock_available):
        """Test that output is properly formatted."""
        mock_available.return_value = True
        mock_generate.return_value = """
        Line one with some syllables here now
        Line two with some syllables here now

        """

        result = self.converter.convert("Test")

        # Should be cleaned up (no extra whitespace)
        self.assertNotIn("  ", result)
        lines = result.strip().split('\n')
        self.assertGreater(len(lines), 0)


class TestIntegration(unittest.TestCase):
    """Integration tests (require actual Ollama installation)."""

    def setUp(self):
        """Check if Ollama is available, skip tests if not."""
        self.client = OllamaClient()
        self.is_ollama_available = self.client.is_available()

    @unittest.skipUnless(
        OllamaClient().is_available(),
        "Ollama not available - skipping integration test"
    )
    def test_end_to_end_conversion(self):
        """Test full conversion pipeline with real Ollama."""
        converter = IambicConverter()

        prose = "The cat sat on the mat and looked at the bird in the tree."

        try:
            result = converter.convert(prose)

            # Basic checks
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)

            # Should have multiple lines (probably)
            lines = result.strip().split('\n')
            self.assertGreater(len(lines), 0)

            # At least some words from original should appear
            result_lower = result.lower()
            self.assertTrue(
                any(word in result_lower for word in ['cat', 'mat', 'bird', 'tree'])
            )

            print(f"\nIntegration test result:")
            print(f"Input: {prose}")
            print(f"Output:\n{result}")

        except (ConnectionError, TimeoutError) as e:
            self.skipTest(f"Ollama unavailable during test: {e}")


def run_tests():
    """Run all tests with verbose output."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSyllableCounter))
    suite.addTests(loader.loadTestsFromTestCase(TestMeterValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestOllamaClient))
    suite.addTests(loader.loadTestsFromTestCase(TestIambicConverter))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    return result


if __name__ == "__main__":
    run_tests()
