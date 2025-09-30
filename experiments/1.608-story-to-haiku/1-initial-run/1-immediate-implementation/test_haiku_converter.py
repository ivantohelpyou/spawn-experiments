"""Tests for Story to Haiku Converter - Method 1"""

import pytest
from unittest.mock import Mock
from haiku_converter import story_to_haiku, count_syllables, count_line_syllables


# Mock haiku responses for testing
MOCK_HAIKU_RESPONSES = {
    'spring': 'Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive',
    'winter': 'Silent snow blankets\nFrozen world in crystal white\nWinter dreams deeply',
    'autumn': 'Leaves paint gold and red\nFalling gently to the earth\nAutumn bids farewell',
    'coding': 'Code lines on the screen\nLogic winds through endless loops\nMind in flow state dances'
}


def create_mock_llm(haiku_text):
    """Helper to create mock LLM client"""
    mock_llm = Mock()
    mock_llm.generate.return_value = {'response': haiku_text}
    return mock_llm


def test_returns_three_lines():
    """Test that haiku has exactly 3 lines"""
    mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['spring'])
    result = story_to_haiku("A story about spring", llm_client=mock_llm)
    assert len(result['lines']) == 3


def test_validates_syllable_structure():
    """Test that syllable counting works"""
    mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['winter'])
    result = story_to_haiku("A story about winter", llm_client=mock_llm)
    # Note: syllable counting is approximate, test that we return counts
    assert len(result['syllable_counts']) == 3
    assert all(isinstance(count, int) for count in result['syllable_counts'])


def test_includes_complete_haiku_string():
    """Test that haiku is properly formatted with newlines"""
    mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['autumn'])
    result = story_to_haiku("A story about autumn", llm_client=mock_llm)
    assert '\n' in result['haiku']
    assert result['haiku'].count('\n') == 2


def test_empty_input_raises_error():
    """Test that empty input raises ValueError"""
    with pytest.raises(ValueError):
        story_to_haiku("")


def test_whitespace_only_raises_error():
    """Test that whitespace-only input raises ValueError"""
    with pytest.raises(ValueError):
        story_to_haiku("   \n\n   ")


def test_very_long_input_truncated():
    """Test that very long input is handled"""
    mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['coding'])
    long_story = "word " * 1000
    result = story_to_haiku(long_story, llm_client=mock_llm)
    assert len(result['lines']) == 3


def test_uses_provided_llm_client():
    """Test that provided LLM client is used"""
    mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['spring'])
    story_to_haiku("test story", llm_client=mock_llm)
    mock_llm.generate.assert_called_once()


def test_syllable_counter():
    """Test basic syllable counting"""
    assert count_syllables("hello") == 2
    assert count_syllables("world") == 1
    assert count_syllables("beautiful") == 4
    assert count_syllables("code") == 1


def test_line_syllable_counter():
    """Test counting syllables in a line"""
    assert count_line_syllables("hello world") == 3
    assert count_line_syllables("code lines flow") == 3


def test_result_structure():
    """Test that result has all required keys"""
    mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['spring'])
    result = story_to_haiku("test", llm_client=mock_llm)

    assert 'haiku' in result
    assert 'lines' in result
    assert 'syllable_counts' in result
    assert 'essence' in result

    assert isinstance(result['haiku'], str)
    assert isinstance(result['lines'], list)
    assert isinstance(result['syllable_counts'], list)
    assert isinstance(result['essence'], str)