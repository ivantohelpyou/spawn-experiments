"""
Test suite for story_to_haiku function - Method 3: Pure TDD / Test-First Development

Following TDD principles:
1. Write tests FIRST (before implementation)
2. Tests define expected behavior
3. Use mocks for LLM to enable fast, predictable testing
4. Red-Green-Refactor cycle

Run 4 Focus: Testing with optimized prompts
"""

import pytest
from unittest.mock import Mock, MagicMock
import json


class MockLLMResponse:
    """Mock response object that mimics ollama.chat() response structure"""
    def __init__(self, content):
        self.message = {'content': content}


class TestStoryToHaikuBasicFunctionality:
    """Test basic function behavior with valid inputs"""

    def test_returns_dict_with_required_keys(self):
        """Test that function returns a dict with all required keys"""
        from haiku_converter import story_to_haiku

        # Mock LLM client
        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"],
            "syllables": [5, 7, 5],
            "essence": "Spring's gentle transition"
        }))
        mock_client.chat.return_value = mock_response

        # Call function
        result = story_to_haiku("A story about spring", llm_client=mock_client)

        # Assert structure
        assert isinstance(result, dict)
        assert 'haiku' in result
        assert 'lines' in result
        assert 'syllables' in result
        assert 'essence' in result
        assert 'valid' in result

    def test_valid_haiku_structure(self):
        """Test that valid 5-7-5 haiku is marked as valid"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Morning dew glistens", "On petals of cherry blooms", "Nature's art unfolds"],
            "syllables": [5, 7, 5],
            "essence": "Beauty of nature awakening"
        }))
        mock_client.chat.return_value = mock_response

        result = story_to_haiku("Nature story", llm_client=mock_client)

        assert result['valid'] is True
        assert result['syllables'] == [5, 7, 5]

    def test_haiku_string_formatting(self):
        """Test that haiku string is properly formatted with newlines"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["First line here", "Second line goes here now", "Third line is last"],
            "syllables": [5, 7, 5],
            "essence": "Test essence"
        }))
        mock_client.chat.return_value = mock_response

        result = story_to_haiku("Test story", llm_client=mock_client)

        expected_haiku = "First line here\nSecond line goes here now\nThird line is last"
        assert result['haiku'] == expected_haiku

    def test_lines_array_has_three_elements(self):
        """Test that lines array contains exactly 3 lines"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Line one text", "Line two has more text", "Line three ends it"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        }))
        mock_client.chat.return_value = mock_response

        result = story_to_haiku("Story", llm_client=mock_client)

        assert len(result['lines']) == 3
        assert isinstance(result['lines'], list)

    def test_essence_is_extracted(self):
        """Test that essence field is properly extracted"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Winter wind blows cold", "Through barren trees and dead leaves", "Life awaits the spring"],
            "syllables": [5, 7, 5],
            "essence": "The cycle of seasons and renewal"
        }))
        mock_client.chat.return_value = mock_response

        result = story_to_haiku("Winter story", llm_client=mock_client)

        assert result['essence'] == "The cycle of seasons and renewal"
        assert len(result['essence']) > 0


class TestStoryToHaikuInvalidSyllables:
    """Test validation of syllable counts"""

    def test_invalid_syllables_first_line(self):
        """Test that invalid first line syllables are detected"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Too many syllables here", "This line is correct", "Five syllables here"],
            "syllables": [7, 7, 5],  # First line is wrong
            "essence": "Test"
        }))
        mock_client.chat.return_value = mock_response

        result = story_to_haiku("Story", llm_client=mock_client)

        assert result['valid'] is False

    def test_invalid_syllables_second_line(self):
        """Test that invalid second line syllables are detected"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Five syllables here", "Too short", "Five more syllables"],
            "syllables": [5, 3, 5],  # Second line is wrong
            "essence": "Test"
        }))
        mock_client.chat.return_value = mock_response

        result = story_to_haiku("Story", llm_client=mock_client)

        assert result['valid'] is False

    def test_invalid_syllables_third_line(self):
        """Test that invalid third line syllables are detected"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Five syllables here", "Seven syllables in line", "Too many syllables now"],
            "syllables": [5, 7, 8],  # Third line is wrong
            "essence": "Test"
        }))
        mock_client.chat.return_value = mock_response

        result = story_to_haiku("Story", llm_client=mock_client)

        assert result['valid'] is False


class TestStoryToHaikuEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_input_raises_error(self):
        """Test that empty input raises ValueError"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()

        with pytest.raises(ValueError, match="Input text cannot be empty"):
            story_to_haiku("", llm_client=mock_client)

    def test_whitespace_only_input_raises_error(self):
        """Test that whitespace-only input raises ValueError"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()

        with pytest.raises(ValueError, match="Input text cannot be empty"):
            story_to_haiku("   \n  \t  ", llm_client=mock_client)

    def test_malformed_json_raises_error(self):
        """Test that malformed JSON from LLM raises appropriate error"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse("This is not valid JSON at all!")
        mock_client.chat.return_value = mock_response

        with pytest.raises(ValueError, match="Failed to parse LLM response as JSON"):
            story_to_haiku("Story", llm_client=mock_client)

    def test_missing_required_keys_raises_error(self):
        """Test that missing required JSON keys raises appropriate error"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Line 1", "Line 2", "Line 3"]
            # Missing syllables and essence
        }))
        mock_client.chat.return_value = mock_response

        with pytest.raises(ValueError, match="Missing required keys"):
            story_to_haiku("Story", llm_client=mock_client)

    def test_wrong_number_of_lines_raises_error(self):
        """Test that wrong number of lines raises error"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Only two lines", "Not enough lines"],  # Only 2 lines
            "syllables": [5, 7],
            "essence": "Test"
        }))
        mock_client.chat.return_value = mock_response

        with pytest.raises(ValueError, match="Expected 3 lines"):
            story_to_haiku("Story", llm_client=mock_client)

    def test_wrong_number_of_syllable_counts_raises_error(self):
        """Test that wrong number of syllable counts raises error"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Line 1", "Line 2", "Line 3"],
            "syllables": [5, 7],  # Only 2 counts
            "essence": "Test"
        }))
        mock_client.chat.return_value = mock_response

        with pytest.raises(ValueError, match="Expected 3 syllable counts"):
            story_to_haiku("Story", llm_client=mock_client)


class TestStoryToHaikuPromptOptimization:
    """Test that optimized prompts are being used (Run 4 specific)"""

    def test_prompt_includes_explicit_syllable_instructions(self):
        """Test that the prompt sent to LLM includes explicit syllable counting instructions"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Test line one here", "Test line two is longer now", "Test line three end"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        }))
        mock_client.chat.return_value = mock_response

        story_to_haiku("Test story", llm_client=mock_client)

        # Get the call arguments
        call_args = mock_client.chat.call_args

        # Extract the prompt (should be in messages parameter)
        messages = call_args[1]['messages']
        prompt = messages[0]['content']

        # Verify optimized prompt elements are present
        assert "5 syllables" in prompt
        assert "7 syllables" in prompt
        assert "Count" in prompt or "count" in prompt
        assert "exactly" in prompt.lower() or "must have" in prompt.lower()

    def test_prompt_includes_example_format(self):
        """Test that prompt includes example JSON format"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Test", "Test", "Test"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        }))
        mock_client.chat.return_value = mock_response

        story_to_haiku("Test story", llm_client=mock_client)

        call_args = mock_client.chat.call_args
        messages = call_args[1]['messages']
        prompt = messages[0]['content']

        # Verify example is present
        assert "example" in prompt.lower() or "format" in prompt.lower()
        assert "lines" in prompt
        assert "syllables" in prompt
        assert "essence" in prompt

    def test_prompt_includes_essence_guidance(self):
        """Test that prompt includes guidance on extracting essence"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Test", "Test", "Test"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        }))
        mock_client.chat.return_value = mock_response

        story_to_haiku("Test story", llm_client=mock_client)

        call_args = mock_client.chat.call_args
        messages = call_args[1]['messages']
        prompt = messages[0]['content']

        # Verify essence guidance is present
        assert "essence" in prompt.lower() or "core" in prompt.lower() or "theme" in prompt.lower()


class TestStoryToHaikuLLMIntegration:
    """Test LLM client integration and dependency injection"""

    def test_accepts_custom_llm_client(self):
        """Test that function accepts and uses custom LLM client"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Test", "Test", "Test"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        }))
        mock_client.chat.return_value = mock_response

        story_to_haiku("Story", llm_client=mock_client)

        # Verify the mock was called
        mock_client.chat.assert_called_once()

    def test_llm_called_with_correct_model(self):
        """Test that LLM is called with llama3.2 model"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Test", "Test", "Test"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        }))
        mock_client.chat.return_value = mock_response

        story_to_haiku("Story", llm_client=mock_client)

        # Check that model parameter is llama3.2
        call_args = mock_client.chat.call_args
        assert call_args[1]['model'] == 'llama3.2'

    def test_llm_called_with_json_format(self):
        """Test that LLM is instructed to return JSON format"""
        from haiku_converter import story_to_haiku

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Test", "Test", "Test"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        }))
        mock_client.chat.return_value = mock_response

        story_to_haiku("Story", llm_client=mock_client)

        # Check that format parameter is json
        call_args = mock_client.chat.call_args
        assert call_args[1]['format'] == 'json'


class TestStoryToHaikuRealWorldScenarios:
    """Test realistic usage scenarios"""

    def test_long_story_input(self):
        """Test with a longer story input"""
        from haiku_converter import story_to_haiku

        long_story = """
        Once upon a time in a small village nestled in the mountains,
        there lived an old woman who tended a beautiful garden. Every morning
        she would wake before dawn and water her flowers, speaking softly to
        each plant as if it were her child. The villagers thought her strange,
        but her garden was the most beautiful in all the land.
        """

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Dawn breaks on gardens", "Old hands tend blooming flowers", "Love nurtures beauty"],
            "syllables": [5, 7, 5],
            "essence": "Devotion to nature and beauty through patient care"
        }))
        mock_client.chat.return_value = mock_response

        result = story_to_haiku(long_story, llm_client=mock_client)

        assert result['valid'] is True
        assert len(result['lines']) == 3
        assert 'garden' in result['essence'].lower() or 'flower' in result['essence'].lower() or 'care' in result['essence'].lower()

    def test_short_story_input(self):
        """Test with a very short story input"""
        from haiku_converter import story_to_haiku

        short_story = "The sun set over the ocean."

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Sun melts in ocean", "Waves catch the fading daylight", "Evening calm descends"],
            "syllables": [5, 7, 5],
            "essence": "The peaceful transition from day to night"
        }))
        mock_client.chat.return_value = mock_response

        result = story_to_haiku(short_story, llm_client=mock_client)

        assert result['valid'] is True
        assert len(result['lines']) == 3

    def test_story_with_strong_emotion(self):
        """Test with an emotionally charged story"""
        from haiku_converter import story_to_haiku

        emotional_story = "After years apart, she saw him at the train station. Their eyes met, and all the pain melted away."

        mock_client = Mock()
        mock_response = MockLLMResponse(json.dumps({
            "lines": ["Eyes meet on platform", "Years of pain dissolve at once", "Love remembers all"],
            "syllables": [5, 7, 5],
            "essence": "The enduring power of love and reunion"
        }))
        mock_client.chat.return_value = mock_response

        result = story_to_haiku(emotional_story, llm_client=mock_client)

        assert result['valid'] is True
        assert 'love' in result['essence'].lower() or 'reunion' in result['essence'].lower() or 'emotion' in result['essence'].lower()
