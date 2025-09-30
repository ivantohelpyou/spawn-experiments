"""
Test suite for story_to_haiku converter.
Following TDD approach - tests written FIRST.
"""

import unittest
from unittest.mock import Mock
import json


class TestHaikuConverter(unittest.TestCase):

    def test_basic_haiku_conversion(self):
        """Test basic happy path with valid haiku."""
        from haiku_converter import story_to_haiku

        # Mock LLM client
        mock_client = Mock()
        mock_response = {
            "lines": [
                "Cherry blossoms fall",
                "Softly on the quiet pond",
                "Spring whispers arrive"
            ],
            "syllables": [5, 7, 5],
            "essence": "Spring's gentle transition"
        }

        # Setup mock to return JSON string
        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })

        result = story_to_haiku("A beautiful spring story about cherry blossoms.", mock_client)

        # Verify structure
        self.assertIn('haiku', result)
        self.assertIn('lines', result)
        self.assertIn('syllables', result)
        self.assertIn('essence', result)
        self.assertIn('valid', result)

        # Verify content
        self.assertEqual(result['lines'], mock_response['lines'])
        self.assertEqual(result['syllables'], [5, 7, 5])
        self.assertEqual(result['essence'], mock_response['essence'])
        self.assertTrue(result['valid'])
        self.assertIn('\n', result['haiku'])

    def test_invalid_syllable_pattern(self):
        """Test detection of invalid syllable patterns."""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = {
            "lines": ["Bad line", "Another bad one", "Wrong syllables"],
            "syllables": [3, 4, 5],  # Invalid!
            "essence": "Wrong pattern"
        }

        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })

        result = story_to_haiku("Test text", mock_client)

        self.assertFalse(result['valid'])
        self.assertEqual(result['syllables'], [3, 4, 5])

    def test_malformed_json(self):
        """Test handling of malformed JSON from LLM."""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_client.chat = Mock(return_value={
            'message': {'content': 'This is not valid JSON at all!'}
        })

        result = story_to_haiku("Test text", mock_client)

        # Should return error structure
        self.assertFalse(result['valid'])
        self.assertTrue('error' in result or result['haiku'] == "")

    def test_missing_json_keys(self):
        """Test handling of incomplete JSON response."""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = {
            "lines": ["Line one", "Line two", "Line three"]
            # Missing syllables and essence
        }

        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })

        result = story_to_haiku("Test text", mock_client)

        self.assertFalse(result['valid'])

    def test_empty_input(self):
        """Test handling of empty input text."""
        from haiku_converter import story_to_haiku

        mock_client = Mock()

        result = story_to_haiku("", mock_client)

        # Should handle gracefully
        self.assertIn('valid', result)
        self.assertFalse(result['valid'])

    def test_dependency_injection(self):
        """Test that function accepts and uses injected client."""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = {
            "lines": ["Test", "Dependency injection", "Works"],
            "syllables": [5, 7, 5],
            "essence": "Testing"
        }

        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })

        result = story_to_haiku("Test", mock_client)

        # Verify mock was called
        self.assertTrue(mock_client.chat.called)
        self.assertTrue(result['valid'])

    def test_haiku_string_format(self):
        """Test that haiku string is properly formatted with newlines."""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = {
            "lines": ["First line here", "Second line is longer", "Third line ends"],
            "syllables": [5, 7, 5],
            "essence": "Format test"
        }

        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })

        result = story_to_haiku("Test", mock_client)

        expected_haiku = "First line here\nSecond line is longer\nThird line ends"
        self.assertEqual(result['haiku'], expected_haiku)

    def test_valid_syllable_check_exact(self):
        """Test that only exact [5, 7, 5] pattern is valid."""
        from haiku_converter import story_to_haiku

        mock_client = Mock()

        # Test [5, 7, 5] - valid
        mock_response = {
            "lines": ["A", "B", "C"],
            "syllables": [5, 7, 5],
            "essence": "Valid"
        }
        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })
        result = story_to_haiku("Test", mock_client)
        self.assertTrue(result['valid'])

        # Test [7, 5, 5] - invalid
        mock_response['syllables'] = [7, 5, 5]
        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })
        result = story_to_haiku("Test", mock_client)
        self.assertFalse(result['valid'])

        # Test [5, 5, 5] - invalid
        mock_response['syllables'] = [5, 5, 5]
        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })
        result = story_to_haiku("Test", mock_client)
        self.assertFalse(result['valid'])

    def test_prompt_structure(self):
        """Test that function sends proper prompt to LLM."""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = {
            "lines": ["Test", "Prompt structure", "Valid"],
            "syllables": [5, 7, 5],
            "essence": "Testing"
        }

        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })

        story_to_haiku("My test story", mock_client)

        # Check that chat was called with proper structure
        call_args = mock_client.chat.call_args
        self.assertIsNotNone(call_args)

        # Should have model and messages
        self.assertTrue('model' in call_args[1] or len(call_args[0]) > 0)


if __name__ == '__main__':
    unittest.main()
