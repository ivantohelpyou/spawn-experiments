"""
Tests for Story to Haiku Converter - Method 1
Uses mocks for fast parallel execution.
"""

import pytest
from unittest.mock import Mock
from haiku_converter import story_to_haiku


class TestHaikuConverter:
    """Test suite for story_to_haiku function."""

    def test_basic_haiku_generation(self):
        """Test basic haiku generation with valid response."""
        # Mock LLM client
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '''{
  "lines": [
    "Cherry blossoms fall",
    "Softly on the quiet pond",
    "Spring whispers arrive"
  ],
  "syllables": [5, 7, 5],
  "essence": "Spring's gentle transition from winter to renewal"
}'''
            }
        }

        result = story_to_haiku("A story about spring", llm_client=mock_client)

        assert result['haiku'] == "Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive"
        assert result['lines'] == [
            "Cherry blossoms fall",
            "Softly on the quiet pond",
            "Spring whispers arrive"
        ]
        assert result['syllables'] == [5, 7, 5]
        assert result['essence'] == "Spring's gentle transition from winter to renewal"
        assert result['valid'] is True

    def test_invalid_syllable_count(self):
        """Test handling of invalid syllable counts."""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '''{
  "lines": [
    "Wrong count here",
    "This line has wrong syllables",
    "Not five seven five"
  ],
  "syllables": [4, 8, 6],
  "essence": "Testing invalid syllables"
}'''
            }
        }

        result = story_to_haiku("Test story", llm_client=mock_client)

        assert result['valid'] is False
        assert result['syllables'] == [4, 8, 6]

    def test_empty_input(self):
        """Test handling of empty input."""
        result = story_to_haiku("")

        assert result['haiku'] == ""
        assert result['lines'] == []
        assert result['syllables'] == []
        assert result['essence'] == ""
        assert result['valid'] is False

    def test_whitespace_only_input(self):
        """Test handling of whitespace-only input."""
        result = story_to_haiku("   \n\t  ")

        assert result['haiku'] == ""
        assert result['valid'] is False

    def test_malformed_json_response(self):
        """Test handling of malformed JSON."""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': 'This is not valid JSON { broken'
            }
        }

        result = story_to_haiku("Test story", llm_client=mock_client)

        assert result['valid'] is False
        assert "Error parsing response" in result['essence']

    def test_missing_required_keys(self):
        """Test handling of JSON missing required keys."""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '{"lines": ["One", "Two", "Three"]}'
            }
        }

        result = story_to_haiku("Test story", llm_client=mock_client)

        assert result['valid'] is False
        assert "Error parsing response" in result['essence']

    def test_json_with_extra_text(self):
        """Test extraction of JSON from response with extra text."""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '''Here is your haiku:
{
  "lines": [
    "Moon shines bright above",
    "Silent night embraces all",
    "Peace descends on earth"
  ],
  "syllables": [5, 7, 5],
  "essence": "Nighttime serenity"
}
I hope you like it!'''
            }
        }

        result = story_to_haiku("Night story", llm_client=mock_client)

        assert result['valid'] is True
        assert result['lines'][0] == "Moon shines bright above"

    def test_invalid_lines_structure(self):
        """Test handling of invalid lines structure."""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '''{
  "lines": ["Only", "Two lines"],
  "syllables": [5, 7, 5],
  "essence": "Invalid structure"
}'''
            }
        }

        result = story_to_haiku("Test story", llm_client=mock_client)

        assert result['valid'] is False
        assert "Error parsing response" in result['essence']

    def test_invalid_syllables_structure(self):
        """Test handling of invalid syllables structure."""
        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '''{
  "lines": ["One", "Two", "Three"],
  "syllables": [5, 7],
  "essence": "Invalid syllable count"
}'''
            }
        }

        result = story_to_haiku("Test story", llm_client=mock_client)

        assert result['valid'] is False

    def test_long_story_input(self):
        """Test with longer story input."""
        long_story = """
        In a small village nestled between mountains, there lived an old woman
        who spent her days tending to a beautiful garden. Every morning, she
        would wake before dawn to water her flowers and vegetables, talking
        to them as if they were old friends.
        """

        mock_client = Mock()
        mock_client.chat.return_value = {
            'message': {
                'content': '''{
  "lines": [
    "Dawn garden whispers",
    "Old hands nurture patient blooms",
    "Mountains watch in peace"
  ],
  "syllables": [5, 7, 5],
  "essence": "The daily ritual of tending a garden in mountain solitude"
}'''
            }
        }

        result = story_to_haiku(long_story, llm_client=mock_client)

        assert result['valid'] is True
        assert len(result['lines']) == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
