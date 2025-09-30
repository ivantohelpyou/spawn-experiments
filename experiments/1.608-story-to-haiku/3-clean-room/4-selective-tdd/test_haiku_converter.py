"""
Test suite for story_to_haiku converter - Strategic TDD approach.

Focus on critical paths:
- JSON parsing (high risk)
- Validation logic (complex)
- Error handling (edge cases)
"""

import unittest
from unittest.mock import Mock
from haiku_converter import story_to_haiku


class TestJSONParsing(unittest.TestCase):
    """Critical: JSON parsing is error-prone"""

    def test_valid_json_response(self):
        """Valid JSON should parse correctly"""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '{"lines": ["Line one here", "Line two is longer now", "Line three is short"], "syllables": [5, 7, 5], "essence": "Test theme"}'
            }
        }

        result = story_to_haiku("test story", llm_client=mock_client)

        self.assertEqual(result['lines'], ["Line one here", "Line two is longer now", "Line three is short"])
        self.assertEqual(result['syllables'], [5, 7, 5])
        self.assertEqual(result['essence'], "Test theme")
        self.assertTrue(result['valid'])
        self.assertEqual(result['haiku'], "Line one here\nLine two is longer now\nLine three is short")

    def test_malformed_json_response(self):
        """Malformed JSON should fail gracefully"""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {'content': 'Not valid JSON at all'}
        }

        result = story_to_haiku("test story", llm_client=mock_client)

        self.assertFalse(result['valid'])
        self.assertIn('error', result)

    def test_missing_keys_in_json(self):
        """Missing required keys should fail gracefully"""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {'content': '{"lines": ["a", "b", "c"]}'}
        }

        result = story_to_haiku("test story", llm_client=mock_client)

        self.assertFalse(result['valid'])


class TestSyllableValidation(unittest.TestCase):
    """Critical: Core business logic"""

    def test_valid_syllable_pattern(self):
        """5-7-5 pattern should be valid"""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '{"lines": ["a", "b", "c"], "syllables": [5, 7, 5], "essence": "test"}'
            }
        }

        result = story_to_haiku("test", llm_client=mock_client)
        self.assertTrue(result['valid'])

    def test_invalid_syllable_pattern(self):
        """Non 5-7-5 pattern should be invalid"""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '{"lines": ["a", "b", "c"], "syllables": [4, 7, 5], "essence": "test"}'
            }
        }

        result = story_to_haiku("test", llm_client=mock_client)
        self.assertFalse(result['valid'])

    def test_wrong_number_of_syllables(self):
        """Wrong count of syllables should be invalid"""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '{"lines": ["a", "b", "c"], "syllables": [5, 7], "essence": "test"}'
            }
        }

        result = story_to_haiku("test", llm_client=mock_client)
        self.assertFalse(result['valid'])


class TestEdgeCases(unittest.TestCase):
    """Critical: Error conditions"""

    def test_empty_input(self):
        """Empty text should handle gracefully"""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '{"lines": ["a", "b", "c"], "syllables": [5, 7, 5], "essence": "empty"}'
            }
        }

        result = story_to_haiku("", llm_client=mock_client)
        self.assertIn('haiku', result)

    def test_llm_client_called_correctly(self):
        """Verify Ollama is called with correct parameters"""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '{"lines": ["a", "b", "c"], "syllables": [5, 7, 5], "essence": "test"}'
            }
        }

        story_to_haiku("test story", llm_client=mock_client)

        mock_client.chat.assert_called_once()
        call_args = mock_client.chat.call_args
        self.assertEqual(call_args[1]['model'], 'llama3.2')
        self.assertIn('haiku', call_args[1]['messages'][0]['content'].lower())
        self.assertIn('json', call_args[1]['messages'][0]['content'].lower())


class TestHaikuFormatting(unittest.TestCase):
    """Simple but important: output format"""

    def test_haiku_string_with_newlines(self):
        """Haiku string should join lines with newlines"""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '{"lines": ["First line", "Second line here", "Third line"], "syllables": [5, 7, 5], "essence": "test"}'
            }
        }

        result = story_to_haiku("test", llm_client=mock_client)

        self.assertEqual(result['haiku'], "First line\nSecond line here\nThird line")
        self.assertEqual(result['haiku'].count('\n'), 2)


if __name__ == '__main__':
    unittest.main()
