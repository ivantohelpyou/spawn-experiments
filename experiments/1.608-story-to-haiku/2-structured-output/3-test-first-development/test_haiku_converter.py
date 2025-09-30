"""
Test-First Development (TDD) - Tests Written FIRST
These tests define the expected behavior before implementation.
"""

import pytest
from unittest.mock import Mock
from haiku_converter import story_to_haiku


# Mock response templates from spec
MOCK_HAIKU_RESPONSES = {
    'spring': {
        'response': '{"lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"], "syllables": [5, 7, 5], "essence": "Spring\'s gentle transition"}'
    },
    'winter': {
        'response': '{"lines": ["Silent snow blankets", "Frozen world in crystal white", "Winter dreams deeply"], "syllables": [5, 7, 5], "essence": "Winter\'s quiet beauty"}'
    },
    'autumn': {
        'response': '{"lines": ["Leaves paint gold and red", "Falling gently to the earth", "Autumn bids farewell"], "syllables": [5, 7, 5], "essence": "Autumn\'s colorful goodbye"}'
    },
    'coding': {
        'response': '{"lines": ["Code lines on the screen", "Logic winds through endless loops", "Mind in flow state dances"], "syllables": [5, 7, 5], "essence": "Programming flow state"}'
    }
}


class TestBasicFunctionality:
    """Tests for core haiku generation functionality."""

    def test_returns_three_lines(self):
        """Haiku must have exactly 3 lines."""
        mock_llm = Mock()
        mock_llm.generate.return_value = MOCK_HAIKU_RESPONSES['spring']

        result = story_to_haiku("A story about spring", llm_client=mock_llm)
        assert len(result['lines']) == 3

    def test_validates_syllable_structure(self):
        """Valid haiku should have [5, 7, 5] syllables and valid=True."""
        mock_llm = Mock()
        mock_llm.generate.return_value = MOCK_HAIKU_RESPONSES['winter']

        result = story_to_haiku("A story about winter", llm_client=mock_llm)
        assert result['syllables'] == [5, 7, 5]
        assert result['valid'] == True

    def test_parses_json_response(self):
        """Result must contain all required keys from JSON response."""
        mock_llm = Mock()
        mock_llm.generate.return_value = MOCK_HAIKU_RESPONSES['autumn']

        result = story_to_haiku("A story about autumn", llm_client=mock_llm)
        assert 'lines' in result
        assert 'syllables' in result
        assert 'essence' in result
        assert 'haiku' in result
        assert 'valid' in result

    def test_haiku_string_format(self):
        """Haiku string should join lines with newlines."""
        mock_llm = Mock()
        mock_llm.generate.return_value = MOCK_HAIKU_RESPONSES['coding']

        result = story_to_haiku("A story about coding", llm_client=mock_llm)
        assert result['haiku'] == "Code lines on the screen\nLogic winds through endless loops\nMind in flow state dances"
        assert result['haiku'].count('\n') == 2


class TestJSONParsing:
    """Tests for JSON parsing and error handling."""

    def test_handles_malformed_json(self):
        """Invalid JSON should raise ValueError with clear message."""
        mock_llm = Mock()
        mock_llm.generate.return_value = {'response': 'not json at all'}

        with pytest.raises(ValueError, match="Invalid JSON"):
            story_to_haiku("test", llm_client=mock_llm)

    def test_handles_invalid_syllables(self):
        """Wrong syllable counts should set valid=False."""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': '{"lines": ["a", "b", "c"], "syllables": [3, 4, 3], "essence": "test"}'
        }

        result = story_to_haiku("test", llm_client=mock_llm)
        assert result['valid'] == False
        assert result['syllables'] == [3, 4, 3]

    def test_handles_missing_keys(self):
        """Missing required keys in JSON should raise ValueError."""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': '{"lines": ["a", "b", "c"]}'  # Missing syllables and essence
        }

        with pytest.raises(ValueError, match="Missing required key"):
            story_to_haiku("test", llm_client=mock_llm)

    def test_handles_wrong_line_count(self):
        """JSON with wrong number of lines should raise ValueError."""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': '{"lines": ["a", "b"], "syllables": [5, 7], "essence": "test"}'  # Only 2 lines
        }

        with pytest.raises(ValueError, match="Expected 3 lines"):
            story_to_haiku("test", llm_client=mock_llm)

    def test_handles_wrong_syllable_count(self):
        """JSON with wrong number of syllable counts should raise ValueError."""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': '{"lines": ["a", "b", "c"], "syllables": [5, 7], "essence": "test"}'  # Only 2 counts
        }

        with pytest.raises(ValueError, match="Expected 3 syllable counts"):
            story_to_haiku("test", llm_client=mock_llm)


class TestEdgeCases:
    """Tests for edge cases and input validation."""

    def test_empty_input_raises_error(self):
        """Empty string should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            story_to_haiku("")

    def test_whitespace_only_raises_error(self):
        """Whitespace-only input should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            story_to_haiku("   \n\n   ")

    def test_very_long_input_truncated(self):
        """Very long input should be truncated to 500 chars."""
        mock_llm = Mock()
        mock_llm.generate.return_value = MOCK_HAIKU_RESPONSES['spring']

        long_story = "word " * 1000  # 5000 chars
        result = story_to_haiku(long_story, llm_client=mock_llm)

        # Check that mock was called
        mock_llm.generate.assert_called_once()

        # Check that the prompt passed to generate contains truncated text
        call_args = mock_llm.generate.call_args
        prompt = call_args.kwargs['prompt']

        # The story in the prompt should be truncated
        assert len(long_story) > 500
        # Result should still be valid
        assert result['valid'] == True

    def test_none_input_raises_error(self):
        """None input should raise appropriate error."""
        with pytest.raises((ValueError, TypeError)):
            story_to_haiku(None)


class TestDependencyInjection:
    """Tests for LLM client dependency injection."""

    def test_accepts_mock_client(self):
        """Function should accept and use injected mock client."""
        mock_llm = Mock()
        mock_llm.generate.return_value = MOCK_HAIKU_RESPONSES['spring']

        result = story_to_haiku("test story", llm_client=mock_llm)

        # Verify mock was called
        mock_llm.generate.assert_called_once()

        # Verify correct parameters passed
        call_args = mock_llm.generate.call_args
        assert call_args.kwargs['model'] == 'llama3.2'
        assert 'prompt' in call_args.kwargs
        assert 'test story' in call_args.kwargs['prompt']

    def test_prompt_format(self):
        """Prompt should request JSON format and include story."""
        mock_llm = Mock()
        mock_llm.generate.return_value = MOCK_HAIKU_RESPONSES['winter']

        story = "A winter tale"
        story_to_haiku(story, llm_client=mock_llm)

        call_args = mock_llm.generate.call_args
        prompt = call_args.kwargs['prompt']

        # Check prompt requirements from spec
        assert 'JSON' in prompt or 'json' in prompt
        assert '5-7-5' in prompt
        assert story in prompt
        assert 'lines' in prompt
        assert 'syllables' in prompt
        assert 'essence' in prompt