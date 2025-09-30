"""Tests for haiku converter using mocks."""
import pytest
from unittest.mock import Mock
from haiku_converter import story_to_haiku


def test_basic_haiku_conversion():
    """Test basic story to haiku conversion."""
    mock_client = Mock()
    mock_client.chat.return_value = {
        'message': {
            'content': '{"lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"], "syllables": [5, 7, 5], "essence": "Spring transition"}'
        }
    }

    result = story_to_haiku("A story about spring", llm_client=mock_client)

    assert 'haiku' in result
    assert 'lines' in result
    assert 'syllables' in result
    assert 'essence' in result
    assert 'valid' in result
    assert result['valid'] == True
    assert result['syllables'] == [5, 7, 5]
    assert len(result['lines']) == 3


def test_invalid_syllable_pattern():
    """Test with invalid syllable pattern."""
    mock_client = Mock()
    mock_client.chat.return_value = {
        'message': {
            'content': '{"lines": ["Too many syllables here", "Short", "Also wrong"], "syllables": [8, 2, 3], "essence": "Bad haiku"}'
        }
    }

    result = story_to_haiku("Some text", llm_client=mock_client)

    assert result['valid'] == False
    assert result['syllables'] == [8, 2, 3]


def test_empty_text_raises_error():
    """Test that empty text raises ValueError."""
    with pytest.raises(ValueError):
        story_to_haiku("")


def test_malformed_json_raises_error():
    """Test that malformed JSON raises ValueError."""
    mock_client = Mock()
    mock_client.chat.return_value = {
        'message': {
            'content': 'not valid json'
        }
    }

    with pytest.raises(ValueError, match="Failed to parse JSON"):
        story_to_haiku("Some text", llm_client=mock_client)


def test_missing_keys_raises_error():
    """Test that missing required keys raises ValueError."""
    mock_client = Mock()
    mock_client.chat.return_value = {
        'message': {
            'content': '{"lines": ["line1", "line2", "line3"]}'
        }
    }

    with pytest.raises(ValueError, match="Missing required keys"):
        story_to_haiku("Some text", llm_client=mock_client)


def test_haiku_string_formatting():
    """Test that haiku string is properly formatted with newlines."""
    mock_client = Mock()
    mock_client.chat.return_value = {
        'message': {
            'content': '{"lines": ["Line one here", "Line two is longer now", "Line three is short"], "syllables": [5, 7, 5], "essence": "Test"}'
        }
    }

    result = story_to_haiku("Test", llm_client=mock_client)

    assert result['haiku'] == "Line one here\nLine two is longer now\nLine three is short"
    assert '\n' in result['haiku']


def test_wrong_line_count_raises_error():
    """Test that wrong number of lines raises ValueError."""
    mock_client = Mock()
    mock_client.chat.return_value = {
        'message': {
            'content': '{"lines": ["Line one", "Line two"], "syllables": [5, 7], "essence": "Too short"}'
        }
    }

    with pytest.raises(ValueError, match="Expected 3 lines"):
        story_to_haiku("Test", llm_client=mock_client)
