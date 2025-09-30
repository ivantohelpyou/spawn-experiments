"""
Test suite for story-to-haiku converter
Method 5: Adaptive/Validated TDD

Following full TDD with selective test validation.
All code is tested, but only complex tests get validation step.
"""

import unittest
from unittest.mock import Mock
import json


class TestHaikuConverter(unittest.TestCase):

    def test_basic_haiku_conversion(self):
        """Test basic happy path with valid haiku."""
        from haiku_converter import story_to_haiku

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

        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })

        result = story_to_haiku("A beautiful spring story.", mock_client)

        # Verify structure
        self.assertIn('haiku', result)
        self.assertIn('lines', result)
        self.assertIn('syllables', result)
        self.assertIn('essence', result)
        self.assertIn('valid', result)

        # Verify content
        self.assertEqual(result['lines'], mock_response['lines'])
        self.assertEqual(result['syllables'], [5, 7, 5])
        self.assertTrue(result['valid'])
        self.assertIn('\n', result['haiku'])

    def test_invalid_syllable_pattern(self):
        """Test detection of invalid syllable patterns."""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = {
            "lines": ["Bad line", "Another bad one", "Wrong syllables"],
            "syllables": [3, 4, 5],
            "essence": "Wrong pattern"
        }

        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })

        result = story_to_haiku("Test text", mock_client)

        self.assertFalse(result['valid'])
        self.assertEqual(result['syllables'], [3, 4, 5])

    def test_malformed_json(self):
        """Test handling of malformed JSON from LLM.

        VALIDATION CANDIDATE: JSON parsing is error-prone
        Will validate this test catches bugs properly.
        """
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_client.chat = Mock(return_value={
            'message': {'content': 'This is not valid JSON at all!'}
        })

        with self.assertRaises(json.JSONDecodeError):
            story_to_haiku("Test text", mock_client)

    def test_missing_json_keys(self):
        """Test handling of incomplete JSON response.

        VALIDATION CANDIDATE: Key validation is critical
        Will validate this test catches missing keys properly.
        """
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = {
            "lines": ["Line one", "Line two", "Line three"]
            # Missing syllables and essence
        }

        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })

        with self.assertRaises(KeyError):
            story_to_haiku("Test text", mock_client)

    def test_wrong_types_in_json(self):
        """Test handling of wrong types in JSON.

        VALIDATION CANDIDATE: Type checking is complex
        Will validate this test catches type errors properly.
        """
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = {
            "lines": "not a list",  # Wrong type!
            "syllables": [5, 7, 5],
            "essence": "Test"
        }

        mock_client.chat = Mock(return_value={
            'message': {'content': json.dumps(mock_response)}
        })

        with self.assertRaises(TypeError):
            story_to_haiku("Test text", mock_client)

    def test_empty_input(self):
        """Test handling of empty input text."""
        from haiku_converter import story_to_haiku

        with self.assertRaises(ValueError):
            story_to_haiku("", None)

    def test_whitespace_only_input(self):
        """Test handling of whitespace-only input."""
        from haiku_converter import story_to_haiku

        with self.assertRaises(ValueError):
            story_to_haiku("   ", None)

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


if __name__ == '__main__':
    unittest.main()
