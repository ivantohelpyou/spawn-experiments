"""
Adaptive TDD Tests for Story-to-Haiku Converter

Testing Strategy:
- TEST: Structure (3 lines, proper format)
- TEST: Error handling (empty input, edge cases)
- TEST: Integration pattern (dependency injection works)
- SKIP: Haiku quality (non-deterministic)
- SKIP: Syllable accuracy (LLM-dependent)
- USE MOCKS: All LLM interactions
"""

import pytest
from unittest.mock import Mock
from haiku_converter import story_to_haiku


# Mock responses for testing structure
MOCK_VALID_HAIKU = "Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive"
MOCK_INVALID_TWO_LINES = "Too short haiku\nOnly has two lines"
MOCK_INVALID_FOUR_LINES = "Too long haiku\nHas four lines total\nInstead of three lines\nExtra line here"


class TestStructureValidation:
    """Test what matters: structure and format"""

    def test_returns_three_lines(self):
        """CRITICAL: Must return exactly 3 lines"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}

        result = story_to_haiku("A story about spring", llm_client=mock_llm)

        assert len(result['lines']) == 3
        assert result['lines'][0] == "Cherry blossoms fall"
        assert result['lines'][1] == "Softly on the quiet pond"
        assert result['lines'][2] == "Spring whispers arrive"

    def test_haiku_string_has_newlines(self):
        """CRITICAL: Complete haiku string must have newlines"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}

        result = story_to_haiku("Test story", llm_client=mock_llm)

        assert '\n' in result['haiku']
        assert result['haiku'].count('\n') == 2
        assert result['haiku'] == MOCK_VALID_HAIKU

    def test_returns_required_keys(self):
        """CRITICAL: Response dict must have all required keys"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}

        result = story_to_haiku("Test", llm_client=mock_llm)

        assert 'haiku' in result
        assert 'lines' in result
        assert 'syllable_counts' in result
        assert 'essence' in result


class TestErrorHandling:
    """Test what matters: graceful error handling"""

    def test_empty_input_raises_error(self):
        """CRITICAL: Must reject empty input"""
        with pytest.raises(ValueError, match="cannot be empty"):
            story_to_haiku("")

    def test_whitespace_only_raises_error(self):
        """CRITICAL: Must reject whitespace-only input"""
        with pytest.raises(ValueError, match="cannot be empty"):
            story_to_haiku("   \n\n   ")

    def test_invalid_two_line_response_raises_error(self):
        """CRITICAL: Must validate LLM returned 3 lines"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {'response': MOCK_INVALID_TWO_LINES}

        with pytest.raises(ValueError, match="Expected 3 lines"):
            story_to_haiku("Test", llm_client=mock_llm)

    def test_invalid_four_line_response_raises_error(self):
        """CRITICAL: Must validate LLM returned 3 lines"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {'response': MOCK_INVALID_FOUR_LINES}

        with pytest.raises(ValueError, match="Expected 3 lines"):
            story_to_haiku("Test", llm_client=mock_llm)


class TestDependencyInjection:
    """Test what matters: proper integration pattern"""

    def test_uses_provided_mock_client(self):
        """CRITICAL: Must use injected client"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}

        story_to_haiku("Test story", llm_client=mock_llm)

        mock_llm.generate.assert_called_once()
        call_args = mock_llm.generate.call_args
        assert call_args.kwargs['model'] == 'llama3.2'
        assert 'Test story' in call_args.kwargs['prompt']

    def test_truncates_long_input(self):
        """IMPORTANT: Should truncate very long input"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}

        long_story = "word " * 1000  # 5000 chars
        story_to_haiku(long_story, llm_client=mock_llm)

        call_args = mock_llm.generate.call_args
        prompt = call_args.kwargs['prompt']
        # Should truncate to 500 chars
        assert len(prompt) < len(long_story)


class TestSyllableCounting:
    """Test syllable counting - but with realistic expectations"""

    def test_returns_syllable_counts(self):
        """Test that syllable counts are returned (not accuracy)"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}

        result = story_to_haiku("Test", llm_client=mock_llm)

        # Just verify it returns a list of 3 integers
        assert isinstance(result['syllable_counts'], list)
        assert len(result['syllable_counts']) == 3
        assert all(isinstance(count, int) for count in result['syllable_counts'])
        assert all(count > 0 for count in result['syllable_counts'])


class TestEssenceExtraction:
    """Test essence field - minimal validation"""

    def test_returns_essence_string(self):
        """Test that essence is returned"""
        mock_llm = Mock()
        mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}

        result = story_to_haiku("A story about spring flowers", llm_client=mock_llm)

        # Just verify it's a non-empty string
        assert isinstance(result['essence'], str)
        assert len(result['essence']) > 0


# DELIBERATELY SKIPPED TESTS:
# - Haiku quality (subjective, non-deterministic)
# - Exact syllable accuracy (depends on syllable counter library)
# - Poetic meter and rhythm (not in requirements)
# - Semantic meaning preservation (too subjective)
# - Real Ollama integration (tested in comparison script)