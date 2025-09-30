"""
Strategic tests for haiku converter - Adaptive TDD approach.

TESTING STRATEGY:
- Test complex/risky parts: JSON parsing, error handling, validation
- Skip obvious parts: string joining, dict construction, simple getters

This is pragmatic TDD: focus testing effort where it matters most.
"""

import pytest
from unittest.mock import Mock
from haiku_converter import story_to_haiku


# -------------------------------------------------------------------
# STRATEGIC TEST AREA 1: JSON Parsing (RISKY - LLM might be malformed)
# -------------------------------------------------------------------

def test_parses_valid_json_response():
    """Test that valid JSON from LLM is correctly parsed."""
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"], "syllables": [5, 7, 5], "essence": "Spring transition"}'
    }

    result = story_to_haiku("A story about spring", llm_client=mock_llm)

    assert result['lines'] == ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"]
    assert result['syllables'] == [5, 7, 5]
    assert result['essence'] == "Spring transition"


def test_handles_malformed_json():
    """Test that malformed JSON raises appropriate error."""
    mock_llm = Mock()
    mock_llm.generate.return_value = {'response': 'This is not JSON at all'}

    with pytest.raises(ValueError, match="Invalid JSON"):
        story_to_haiku("test", llm_client=mock_llm)


def test_handles_missing_required_keys():
    """Test that missing JSON keys raise appropriate errors."""
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["a", "b", "c"]}'  # Missing syllables and essence
    }

    with pytest.raises(ValueError, match="Missing required key"):
        story_to_haiku("test", llm_client=mock_llm)


def test_handles_json_with_extra_whitespace():
    """Test that JSON with extra whitespace is handled correctly."""
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '  \n  {"lines": ["a", "b", "c"], "syllables": [5, 7, 5], "essence": "test"}  \n  '
    }

    result = story_to_haiku("test", llm_client=mock_llm)
    assert result['lines'] == ["a", "b", "c"]


# -------------------------------------------------------------------
# STRATEGIC TEST AREA 2: Error Handling (COMPLEX - edge cases)
# -------------------------------------------------------------------

def test_empty_input_raises_error():
    """Test that empty input is rejected."""
    with pytest.raises(ValueError, match="cannot be empty"):
        story_to_haiku("")


def test_whitespace_only_input_raises_error():
    """Test that whitespace-only input is rejected."""
    with pytest.raises(ValueError, match="cannot be empty"):
        story_to_haiku("   \n\n   ")


def test_wrong_number_of_lines_raises_error():
    """Test that wrong number of lines raises error."""
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["only", "two lines"], "syllables": [5, 7, 5], "essence": "test"}'
    }

    with pytest.raises(ValueError, match="Expected 3 lines"):
        story_to_haiku("test", llm_client=mock_llm)


def test_wrong_number_of_syllable_counts_raises_error():
    """Test that wrong number of syllable counts raises error."""
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["a", "b", "c"], "syllables": [5, 7], "essence": "test"}'
    }

    with pytest.raises(ValueError, match="Expected 3 syllable counts"):
        story_to_haiku("test", llm_client=mock_llm)


# -------------------------------------------------------------------
# STRATEGIC TEST AREA 3: Validation Logic (COMPLEX - core business rule)
# -------------------------------------------------------------------

def test_validates_correct_syllable_structure():
    """Test that correct 5-7-5 structure is marked as valid."""
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["a", "b", "c"], "syllables": [5, 7, 5], "essence": "test"}'
    }

    result = story_to_haiku("test", llm_client=mock_llm)
    assert result['valid'] is True


def test_validates_incorrect_syllable_structure():
    """Test that incorrect syllable structure is marked as invalid."""
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["a", "b", "c"], "syllables": [3, 4, 3], "essence": "test"}'
    }

    result = story_to_haiku("test", llm_client=mock_llm)
    assert result['valid'] is False


def test_creates_haiku_string_with_newlines():
    """Test that haiku string is created with newlines (simple but important for output)."""
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["Line one here", "Line two is here", "Line three here"], "syllables": [5, 7, 5], "essence": "test"}'
    }

    result = story_to_haiku("test", llm_client=mock_llm)
    assert result['haiku'] == "Line one here\nLine two is here\nLine three here"


# -------------------------------------------------------------------
# STRATEGIC TEST AREA 4: Dependency Injection (CRITICAL for testability)
# -------------------------------------------------------------------

def test_accepts_mock_llm_client():
    """Test that mock LLM client can be injected."""
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["a", "b", "c"], "syllables": [5, 7, 5], "essence": "test"}'
    }

    result = story_to_haiku("test", llm_client=mock_llm)

    # Verify the mock was called
    mock_llm.generate.assert_called_once()
    call_args = mock_llm.generate.call_args
    assert call_args.kwargs['model'] == 'llama3.2'
    assert 'test' in call_args.kwargs['prompt']


def test_returns_all_required_keys():
    """Test that all required keys are present in the result."""
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["a", "b", "c"], "syllables": [5, 7, 5], "essence": "test"}'
    }

    result = story_to_haiku("test", llm_client=mock_llm)

    required_keys = ['haiku', 'lines', 'syllables', 'essence', 'valid']
    for key in required_keys:
        assert key in result, f"Missing required key: {key}"


# -------------------------------------------------------------------
# SKIPPED TESTS (too simple/obvious to warrant testing):
# -------------------------------------------------------------------
# - Text truncation logic (basic string slicing)
# - Dict construction (trivial assignment)
# - String joining with '\n'.join() (Python stdlib)
# - Default llm_client=None handling (trivial if/else)
# - Prompt string formatting (straightforward f-string)
#
# These are all straightforward operations that don't warrant test coverage
# in an Adaptive TDD approach. We trust Python's built-in operations and
# focus testing effort on the complex/risky business logic.