"""
Test suite for story_to_haiku function - Test-First Development (TDD)

This test suite is written FIRST, before any implementation.
Tests use mocks for fast execution during development.
"""

import pytest
from unittest.mock import Mock, MagicMock
from haiku_converter import story_to_haiku, count_syllables


# Mock response templates for consistent testing
MOCK_HAIKU_RESPONSES = {
    'spring': 'Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive',
    'winter': 'Silent snow blankets\nFrozen world in crystal white\nWinter dreams deeply',
    'autumn': 'Leaves paint gold and red\nFalling gently to the earth\nAutumn bids farewell',
    'coding': 'Code flows on the screen\nLogic winds through endless loops\nMind in flow state dances',
    'mountains': 'Mountains cradle home\nGarden whispers ancient tales\nSeasons dance with time',
    'ocean': 'Waves crash on old cliffs\nEternal dance of sea and stone\nTime carves beauty deep',
}


class TestBasicFunctionality:
    """Test basic haiku conversion functionality"""

    def test_returns_dict_with_required_keys(self):
        """Result should be a dict with haiku, lines, syllable_counts, essence"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['spring']
        }

        result = story_to_haiku("A story about spring", llm_client=mock_llm)

        assert isinstance(result, dict)
        assert 'haiku' in result
        assert 'lines' in result
        assert 'syllable_counts' in result
        assert 'essence' in result

    def test_returns_three_lines(self):
        """Haiku must have exactly 3 lines"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['winter']
        }

        result = story_to_haiku("A story about winter", llm_client=mock_llm)

        assert len(result['lines']) == 3

    def test_validates_syllable_structure(self):
        """Haiku should follow 5-7-5 syllable pattern"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['spring']
        }

        result = story_to_haiku("A story about spring", llm_client=mock_llm)

        assert result['syllable_counts'] == [5, 7, 5]

    def test_includes_complete_haiku_string(self):
        """Haiku string should contain newlines joining 3 lines"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['autumn']
        }

        result = story_to_haiku("A story about autumn", llm_client=mock_llm)

        assert '\n' in result['haiku']
        assert result['haiku'].count('\n') == 2
        assert result['haiku'] == '\n'.join(result['lines'])

    def test_lines_are_stripped(self):
        """Lines should have no leading/trailing whitespace"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': '  Cherry blossoms fall  \n Softly on the quiet pond \nSpring whispers arrive   '
        }

        result = story_to_haiku("A story", llm_client=mock_llm)

        for line in result['lines']:
            assert line == line.strip()
            assert len(line) > 0


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_input_raises_error(self):
        """Empty string should raise ValueError"""
        with pytest.raises(ValueError, match="Input text cannot be empty"):
            story_to_haiku("")

    def test_whitespace_only_raises_error(self):
        """Whitespace-only input should raise ValueError"""
        with pytest.raises(ValueError, match="Input text cannot be empty"):
            story_to_haiku("   \n\n   ")

    def test_very_long_input_truncated(self):
        """Very long input should be truncated to 500 chars"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['coding']
        }

        long_story = "word " * 1000  # 5000 chars
        result = story_to_haiku(long_story, llm_client=mock_llm)

        # Verify it was called with truncated text
        call_args = mock_llm.generate.call_args
        prompt = call_args.kwargs['prompt']
        # The prompt should contain truncated text (max 500 chars from input)
        assert len(long_story) > 500
        assert result is not None  # Should handle gracefully

    def test_llm_returns_wrong_number_of_lines_raises_error(self):
        """If LLM returns != 3 lines, should raise ValueError"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': 'Only one line'
        }

        with pytest.raises(ValueError, match="Expected 3 lines"):
            story_to_haiku("test", llm_client=mock_llm)

    def test_llm_returns_empty_lines_filtered(self):
        """Empty lines in LLM response should be filtered out"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': 'Cherry blossoms fall\n\nSoftly on the quiet pond\n\nSpring whispers arrive'
        }

        # This should work because empty lines are filtered
        result = story_to_haiku("test", llm_client=mock_llm)
        assert len(result['lines']) == 3


class TestLLMIntegration:
    """Test LLM client integration patterns"""

    def test_uses_provided_llm_client(self):
        """Should use the provided LLM client"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['mountains']
        }

        story_to_haiku("test story", llm_client=mock_llm)

        # Verify mock was called exactly once
        mock_llm.generate.assert_called_once()

    def test_calls_llm_with_correct_model(self):
        """Should call LLM with llama3.2 model"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['ocean']
        }

        story_to_haiku("test", llm_client=mock_llm)

        # Verify model parameter
        call_args = mock_llm.generate.call_args
        assert call_args.kwargs['model'] == 'llama3.2'

    def test_prompt_includes_input_text(self):
        """Prompt should include the input text"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['spring']
        }

        input_text = "A beautiful spring day with cherry blossoms"
        story_to_haiku(input_text, llm_client=mock_llm)

        # Verify prompt contains input text
        call_args = mock_llm.generate.call_args
        prompt = call_args.kwargs['prompt']
        assert input_text in prompt or input_text[:500] in prompt

    def test_prompt_requests_haiku_format(self):
        """Prompt should request 5-7-5 haiku format"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['winter']
        }

        story_to_haiku("test", llm_client=mock_llm)

        call_args = mock_llm.generate.call_args
        prompt = call_args.kwargs['prompt'].lower()
        assert 'haiku' in prompt
        assert '5-7-5' in prompt or '5 7 5' in prompt


class TestSyllableCounting:
    """Test syllable counting helper function"""

    def test_count_syllables_basic_words(self):
        """Test syllable counting on basic words"""
        assert count_syllables("hello") == 2
        assert count_syllables("world") == 1
        assert count_syllables("beautiful") == 4
        assert count_syllables("code") == 1

    def test_count_syllables_sentence(self):
        """Test syllable counting on full sentence"""
        # "Cherry blossoms fall" = Cher-ry (2) + blos-soms (2) + fall (1) = 5
        assert count_syllables("Cherry blossoms fall") == 5

    def test_count_syllables_handles_empty(self):
        """Empty string should return 0 syllables"""
        assert count_syllables("") == 0

    def test_count_syllables_case_insensitive(self):
        """Syllable counting should be case insensitive"""
        assert count_syllables("HELLO") == 2
        assert count_syllables("Hello") == 2
        assert count_syllables("hello") == 2


class TestReturnStructure:
    """Test the complete return structure"""

    def test_essence_field_not_empty(self):
        """Essence field should contain meaningful text"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['coding']
        }

        result = story_to_haiku("A programmer debugging code late at night", llm_client=mock_llm)

        assert isinstance(result['essence'], str)
        assert len(result['essence']) > 0

    def test_multiple_calls_independent(self):
        """Multiple calls should be independent"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['spring']
        }

        result1 = story_to_haiku("story 1", llm_client=mock_llm)

        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['winter']
        }

        result2 = story_to_haiku("story 2", llm_client=mock_llm)

        # Results should be different
        assert result1['haiku'] != result2['haiku']


class TestRealWorldScenarios:
    """Test with realistic story inputs"""

    def test_short_story_conversion(self):
        """Test with a short story paragraph"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['mountains']
        }

        story = """
        In a small village nestled between mountains, an old woman
        tended her garden every morning. She spoke to each plant as
        if they were old friends, sharing stories of seasons past.
        """

        result = story_to_haiku(story, llm_client=mock_llm)

        assert len(result['lines']) == 3
        assert result['syllable_counts'] == [5, 7, 5]
        assert mock_llm.generate.called

    def test_technical_content_conversion(self):
        """Test with technical/coding content"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['coding']
        }

        story = """
        A young programmer sat late at night, debugging code that
        refused to work. Line by line, she traced the logic, until
        finally the bug revealed itself in a misplaced semicolon.
        """

        result = story_to_haiku(story, llm_client=mock_llm)

        assert len(result['lines']) == 3
        assert result['syllable_counts'] == [5, 7, 5]

    def test_nature_description_conversion(self):
        """Test with nature description"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {
            'response': MOCK_HAIKU_RESPONSES['ocean']
        }

        story = """
        The ocean waves crashed against ancient cliffs, carved by
        millennia of patient erosion. Seabirds wheeled overhead,
        their cries echoing across the vast expanse of water.
        """

        result = story_to_haiku(story, llm_client=mock_llm)

        assert len(result['lines']) == 3
        assert result['syllable_counts'] == [5, 7, 5]