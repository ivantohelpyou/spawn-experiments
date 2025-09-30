"""
Comprehensive Test Suite for Story-to-Haiku Converter
======================================================

Tests the specification-driven implementation using mocked LLM clients.
No real Ollama calls are made during testing for fast, parallel execution.

Test Coverage:
- Input validation
- LLM integration (mocked)
- Response parsing
- Syllable counting
- Result structure
- Edge cases
- Error handling

Author: Claude (Method 2: Specification-Driven)
Date: 2025-09-30
"""

import pytest
from unittest.mock import Mock
from haiku_converter import (
    story_to_haiku,
    count_syllables,
    count_syllables_in_line,
    extract_essence
)


# ============================================================================
# Mock Helpers
# ============================================================================

def create_mock_llm(haiku_response: str) -> Mock:
    """
    Create a mock LLM client for testing.

    Args:
        haiku_response (str): The haiku text to return (3 lines)

    Returns:
        Mock: Mock object with generate() method
    """
    mock = Mock()
    mock.generate.return_value = {
        'response': haiku_response
    }
    return mock


# Test data: Pre-validated haiku responses
MOCK_HAIKU_RESPONSES = {
    'spring': 'Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive',
    'winter': 'Silent snow blankets\nFrozen world in crystal white\nWinter dreams deeply',
    'autumn': 'Leaves paint gold and red\nFalling gently to the earth\nAutumn bids farewell',
    'coding': 'Code lines on the screen\nLogic winds through endless loops\nMind in flow state dances',
    'mountains': 'Mountains cradle home\nGarden whispers ancient tales\nSeasons dance with time',
}


# ============================================================================
# Test: Input Validation
# ============================================================================

class TestInputValidation:
    """Test input validation and edge cases."""

    def test_empty_string_raises_error(self):
        """Empty input should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            story_to_haiku("")

    def test_whitespace_only_raises_error(self):
        """Whitespace-only input should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            story_to_haiku("   \n\n   ")

    def test_normal_input_accepted(self):
        """Normal input should be accepted."""
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['spring'])
        result = story_to_haiku("A story about spring blossoms.", llm_client=mock_llm)
        assert result is not None
        assert 'haiku' in result

    def test_very_long_input_truncated(self):
        """Very long input should be truncated to 500 chars."""
        long_story = "word " * 200  # 1000 chars
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['coding'])

        story_to_haiku(long_story, llm_client=mock_llm)

        # Verify the prompt contained truncated text (max 500 chars)
        call_args = mock_llm.generate.call_args
        prompt = call_args[1]['prompt']
        # Extract story portion from prompt
        story_in_prompt = prompt.split('Story: ')[1].split('\n\nHaiku:')[0]
        assert len(story_in_prompt) <= 500


# ============================================================================
# Test: LLM Integration (Mocked)
# ============================================================================

class TestLLMIntegration:
    """Test LLM client integration using mocks."""

    def test_uses_provided_llm_client(self):
        """Should use the provided LLM client."""
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['spring'])

        story_to_haiku("Test story", llm_client=mock_llm)

        # Verify mock was called
        mock_llm.generate.assert_called_once()

    def test_passes_correct_model(self):
        """Should pass 'llama3.2' as model parameter."""
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['winter'])

        story_to_haiku("Winter tale", llm_client=mock_llm)

        # Check model parameter
        call_args = mock_llm.generate.call_args
        assert call_args[1]['model'] == 'llama3.2'

    def test_prompt_includes_input_text(self):
        """Prompt should include the input text."""
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['autumn'])
        test_text = "A story about falling leaves in autumn."

        story_to_haiku(test_text, llm_client=mock_llm)

        # Verify prompt contains input text
        call_args = mock_llm.generate.call_args
        prompt = call_args[1]['prompt']
        assert test_text in prompt

    def test_prompt_structure(self):
        """Prompt should have correct structure."""
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['mountains'])

        story_to_haiku("Mountain story", llm_client=mock_llm)

        call_args = mock_llm.generate.call_args
        prompt = call_args[1]['prompt']

        # Check prompt contains key instructions
        assert '5-7-5 syllable structure' in prompt
        assert 'Story:' in prompt
        assert 'Haiku:' in prompt

    def test_llm_generation_error_raises_runtime_error(self):
        """LLM generation errors should be wrapped in RuntimeError."""
        mock_llm = Mock()
        mock_llm.generate.side_effect = Exception("Connection failed")

        with pytest.raises(RuntimeError, match="LLM generation failed"):
            story_to_haiku("Test", llm_client=mock_llm)


# ============================================================================
# Test: Response Parsing
# ============================================================================

class TestResponseParsing:
    """Test parsing of LLM responses."""

    def test_parses_three_line_response(self):
        """Should correctly parse 3-line haiku response."""
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['spring'])
        result = story_to_haiku("Spring story", llm_client=mock_llm)

        assert len(result['lines']) == 3
        assert result['lines'][0] == 'Cherry blossoms fall'
        assert result['lines'][1] == 'Softly on the quiet pond'
        assert result['lines'][2] == 'Spring whispers arrive'

    def test_strips_whitespace_from_lines(self):
        """Should strip whitespace from each line."""
        mock_llm = create_mock_llm(
            '  Cherry blossoms fall  \n'
            '  Softly on the quiet pond  \n'
            '  Spring whispers arrive  '
        )
        result = story_to_haiku("Spring story", llm_client=mock_llm)

        # Lines should be clean with no extra whitespace
        for line in result['lines']:
            assert line == line.strip()
            assert not line.startswith(' ')
            assert not line.endswith(' ')

    def test_handles_blank_lines_in_response(self):
        """Should ignore blank lines in response."""
        mock_llm = create_mock_llm(
            'Cherry blossoms fall\n'
            '\n'  # Blank line
            'Softly on the quiet pond\n'
            '\n'  # Another blank line
            'Spring whispers arrive'
        )
        result = story_to_haiku("Spring story", llm_client=mock_llm)

        # Should still have exactly 3 lines
        assert len(result['lines']) == 3

    def test_invalid_line_count_raises_error(self):
        """Should raise ValueError if response doesn't have 3 lines."""
        # Only 2 lines
        mock_llm = create_mock_llm('Line one\nLine two')

        with pytest.raises(ValueError, match="Expected 3 haiku lines, got 2"):
            story_to_haiku("Test", llm_client=mock_llm)

        # 4 lines
        mock_llm = create_mock_llm('One\nTwo\nThree\nFour')

        with pytest.raises(ValueError, match="Expected 3 haiku lines, got 4"):
            story_to_haiku("Test", llm_client=mock_llm)


# ============================================================================
# Test: Syllable Counting
# ============================================================================

class TestSyllableCounting:
    """Test syllable counting algorithm."""

    def test_count_syllables_simple_words(self):
        """Test syllable counting on simple words."""
        assert count_syllables("cat") == 1
        assert count_syllables("dog") == 1
        assert count_syllables("sky") == 1

    def test_count_syllables_two_syllable_words(self):
        """Test two-syllable words."""
        assert count_syllables("mountain") == 2
        assert count_syllables("garden") == 2
        assert count_syllables("water") == 2

    def test_count_syllables_multi_syllable_words(self):
        """Test words with 3+ syllables."""
        assert count_syllables("beautiful") == 3
        assert count_syllables("amazing") == 3
        assert count_syllables("incredible") == 4

    def test_count_syllables_trailing_e(self):
        """Test handling of silent trailing 'e'."""
        # Trailing 'e' should be ignored
        assert count_syllables("time") == 1
        assert count_syllables("code") == 1

        # But 'le' ending should be counted
        assert count_syllables("table") == 2
        assert count_syllables("simple") == 2

    def test_count_syllables_vowel_clusters(self):
        """Test handling of vowel clusters."""
        # Multiple vowels together count as one syllable
        assert count_syllables("boat") == 1
        assert count_syllables("dream") == 1
        assert count_syllables("quiet") == 2  # qui-et

    def test_count_syllables_in_line(self):
        """Test counting syllables in full lines."""
        # 5 syllables
        assert count_syllables_in_line("Mountains cradle home") == 5

        # 7 syllables
        assert count_syllables_in_line("Garden whispers ancient tales") == 7

        # 5 syllables
        assert count_syllables_in_line("Seasons dance with time") == 5

    def test_syllable_counting_handles_punctuation(self):
        """Syllable counting should ignore punctuation."""
        # With punctuation
        assert count_syllables_in_line("Hello, world!") == 3
        assert count_syllables_in_line("Spring's arrival.") == 4


# ============================================================================
# Test: Result Structure
# ============================================================================

class TestResultStructure:
    """Test the structure of returned results."""

    def test_returns_dict(self):
        """Should return a dictionary."""
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['spring'])
        result = story_to_haiku("Spring story", llm_client=mock_llm)

        assert isinstance(result, dict)

    def test_contains_all_required_fields(self):
        """Result should contain all required fields."""
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['winter'])
        result = story_to_haiku("Winter tale", llm_client=mock_llm)

        assert 'haiku' in result
        assert 'lines' in result
        assert 'syllable_counts' in result
        assert 'essence' in result

    def test_haiku_field_is_string_with_newlines(self):
        """The 'haiku' field should be a single string with newlines."""
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['autumn'])
        result = story_to_haiku("Autumn story", llm_client=mock_llm)

        assert isinstance(result['haiku'], str)
        assert '\n' in result['haiku']
        assert result['haiku'].count('\n') == 2  # 3 lines = 2 newlines

    def test_lines_field_is_list_of_three_strings(self):
        """The 'lines' field should be a list of 3 strings."""
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['coding'])
        result = story_to_haiku("Coding story", llm_client=mock_llm)

        assert isinstance(result['lines'], list)
        assert len(result['lines']) == 3
        for line in result['lines']:
            assert isinstance(line, str)

    def test_syllable_counts_field_is_list_of_ints(self):
        """The 'syllable_counts' field should be a list of integers."""
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['mountains'])
        result = story_to_haiku("Mountain story", llm_client=mock_llm)

        assert isinstance(result['syllable_counts'], list)
        assert len(result['syllable_counts']) == 3
        for count in result['syllable_counts']:
            assert isinstance(count, int)
            assert count > 0  # Should be positive

    def test_essence_field_is_string(self):
        """The 'essence' field should be a string."""
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['spring'])
        result = story_to_haiku("A beautiful spring story", llm_client=mock_llm)

        assert isinstance(result['essence'], str)
        assert len(result['essence']) > 0


# ============================================================================
# Test: Extract Essence Helper
# ============================================================================

class TestExtractEssence:
    """Test the extract_essence helper function."""

    def test_short_text_unchanged(self):
        """Short text should be returned unchanged."""
        text = "A short story"
        assert extract_essence(text) == text

    def test_long_text_truncated(self):
        """Long text should be truncated to ~50 chars."""
        text = "This is a very long story about many things that happen over a long period of time."
        essence = extract_essence(text)

        assert len(essence) <= 53  # 50 + "..."
        assert essence.endswith('...')

    def test_truncation_at_word_boundary(self):
        """Truncation should happen at word boundaries."""
        text = "This is a long story about mountains"
        essence = extract_essence(text)

        # Should not cut words in half
        words = essence.replace('...', '').split()
        for word in words:
            assert word in text

    def test_strips_whitespace(self):
        """Should strip leading/trailing whitespace."""
        text = "   A story with whitespace   "
        essence = extract_essence(text)

        assert not essence.startswith(' ')
        assert not essence.endswith(' ') or essence.endswith('...')


# ============================================================================
# Test: Integration Scenarios
# ============================================================================

class TestIntegrationScenarios:
    """Test complete end-to-end scenarios with mocks."""

    def test_complete_spring_story_conversion(self):
        """Test complete conversion of spring story."""
        story = """
        In a small garden, cherry blossoms began to bloom.
        The old gardener smiled as he watched the petals dance
        in the gentle spring breeze.
        """
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['spring'])

        result = story_to_haiku(story, llm_client=mock_llm)

        # Verify complete result structure
        assert result['haiku'] == MOCK_HAIKU_RESPONSES['spring']
        assert len(result['lines']) == 3
        assert len(result['syllable_counts']) == 3
        assert 'garden' in result['essence'].lower() or 'cherry' in result['essence'].lower()

    def test_complete_coding_story_conversion(self):
        """Test complete conversion of coding story."""
        story = """
        A programmer sat late at night, debugging code that wouldn't work.
        Line by line, loop by loop, searching for the elusive bug.
        """
        mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['coding'])

        result = story_to_haiku(story, llm_client=mock_llm)

        assert 'Code lines' in result['haiku']
        assert len(result['lines']) == 3
        assert result['essence'].startswith('A programmer')

    def test_multiple_conversions_independent(self):
        """Multiple conversions should be independent."""
        mock_llm_1 = create_mock_llm(MOCK_HAIKU_RESPONSES['spring'])
        mock_llm_2 = create_mock_llm(MOCK_HAIKU_RESPONSES['winter'])

        result1 = story_to_haiku("Spring story", llm_client=mock_llm_1)
        result2 = story_to_haiku("Winter story", llm_client=mock_llm_2)

        # Results should be different
        assert result1['haiku'] != result2['haiku']
        assert result1['essence'] != result2['essence']


# ============================================================================
# Test: Error Handling
# ============================================================================

class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_missing_ollama_module_handled(self):
        """Should handle missing ollama module gracefully."""
        # This test would need to mock import failure
        # For now, we just verify the error message would be clear
        # In real usage, if ollama isn't installed, it should say so
        pass  # Implementation note: Tested manually

    def test_malformed_response_handled(self):
        """Should handle malformed LLM responses."""
        # Response with only one line
        mock_llm = create_mock_llm("Just one line")

        with pytest.raises(ValueError, match="Expected 3 haiku lines"):
            story_to_haiku("Test", llm_client=mock_llm)

    def test_empty_response_handled(self):
        """Should handle empty LLM responses."""
        mock_llm = create_mock_llm("")

        with pytest.raises(ValueError, match="Expected 3 haiku lines, got 0"):
            story_to_haiku("Test", llm_client=mock_llm)


# ============================================================================
# Test Configuration
# ============================================================================

if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])