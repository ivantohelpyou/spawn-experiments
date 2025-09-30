"""
Comprehensive test suite for Story-to-Haiku Converter
Method 2: Specification-Driven Implementation
Run 2: Structured Output

All tests use mocks - no real LLM calls during testing.
"""

import pytest
from unittest.mock import Mock
from haiku_converter import story_to_haiku


# Mock Response Templates
MOCK_RESPONSES = {
    'spring_valid': {
        'response': '{"lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"], '
                   '"syllables": [5, 7, 5], "essence": "Spring\'s gentle transition"}'
    },
    'winter_valid': {
        'response': '{"lines": ["Silent snow blankets", "Frozen world in crystal white", "Winter dreams deeply"], '
                   '"syllables": [5, 7, 5], "essence": "Winter\'s quiet beauty"}'
    },
    'coding_valid': {
        'response': '{"lines": ["Code lines on the screen", "Logic winds through endless loops", "Mind in flow state dances"], '
                   '"syllables": [5, 7, 5], "essence": "Programming flow state"}'
    },
    'invalid_syllables': {
        'response': '{"lines": ["This line is too long now", "Short line here", "Another short"], '
                   '"syllables": [8, 4, 3], "essence": "Imperfect structure"}'
    },
    'malformed_json': {
        'response': 'This is not JSON at all'
    },
    'missing_lines': {
        'response': '{"syllables": [5, 7, 5], "essence": "Missing lines"}'
    },
    'missing_syllables': {
        'response': '{"lines": ["Line 1", "Line 2", "Line 3"], "essence": "Missing syllables"}'
    },
    'missing_essence': {
        'response': '{"lines": ["Line 1", "Line 2", "Line 3"], "syllables": [5, 7, 5]}'
    },
    'wrong_line_count_2': {
        'response': '{"lines": ["Line 1", "Line 2"], "syllables": [5, 7], "essence": "Too few lines"}'
    },
    'wrong_line_count_4': {
        'response': '{"lines": ["Line 1", "Line 2", "Line 3", "Line 4"], '
                   '"syllables": [5, 7, 5, 5], "essence": "Too many lines"}'
    },
    'wrong_syllable_count': {
        'response': '{"lines": ["Line 1", "Line 2", "Line 3"], "syllables": [5, 7], "essence": "Wrong count"}'
    },
    'non_string_lines': {
        'response': '{"lines": ["Line 1", 123, "Line 3"], "syllables": [5, 7, 5], "essence": "Bad type"}'
    },
    'non_int_syllables': {
        'response': '{"lines": ["Line 1", "Line 2", "Line 3"], "syllables": [5, "seven", 5], "essence": "Bad type"}'
    },
    'extra_keys': {
        'response': '{"lines": ["Line 1", "Line 2", "Line 3"], "syllables": [5, 7, 5], '
                   '"essence": "Extra fields", "author": "Claude", "timestamp": "2025-09-30"}'
    },
}


def create_mock_llm(response_key: str) -> Mock:
    """Create a mock LLM client for testing."""
    mock = Mock()
    mock.generate.return_value = MOCK_RESPONSES[response_key]
    return mock


# =============================================================================
# INPUT VALIDATION TESTS
# =============================================================================

def test_empty_string_raises_error():
    """Test that empty string input raises ValueError."""
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        story_to_haiku("")


def test_whitespace_only_raises_error():
    """Test that whitespace-only input raises ValueError."""
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        story_to_haiku("   \n\n   \t  ")


def test_valid_input_accepted():
    """Test that valid input is accepted."""
    mock_llm = create_mock_llm('spring_valid')
    result = story_to_haiku("A story about spring", llm_client=mock_llm)
    assert result is not None


def test_long_input_truncated():
    """Test that very long input is truncated to 500 characters."""
    mock_llm = create_mock_llm('spring_valid')
    long_text = "word " * 200  # Creates 1000 character string

    result = story_to_haiku(long_text, llm_client=mock_llm)

    # Verify generate was called
    assert mock_llm.generate.called
    # Check that prompt doesn't contain full 1000 chars
    call_args = mock_llm.generate.call_args
    prompt = call_args[1]['prompt']
    # The story portion should be truncated
    assert len(prompt) < len(long_text) + 200  # +200 for prompt template


# =============================================================================
# JSON PARSING TESTS
# =============================================================================

def test_valid_json_parsed_successfully():
    """Test that valid JSON response is parsed correctly."""
    mock_llm = create_mock_llm('spring_valid')
    result = story_to_haiku("A spring story", llm_client=mock_llm)

    assert result['lines'] == ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"]
    assert result['syllables'] == [5, 7, 5]
    assert result['essence'] == "Spring's gentle transition"


def test_malformed_json_raises_error():
    """Test that malformed JSON raises ValueError with helpful message."""
    mock_llm = create_mock_llm('malformed_json')

    with pytest.raises(ValueError, match="Invalid JSON response from LLM"):
        story_to_haiku("A test story", llm_client=mock_llm)


def test_json_error_includes_preview():
    """Test that JSON error includes preview of malformed response."""
    mock_llm = create_mock_llm('malformed_json')

    with pytest.raises(ValueError, match="This is not JSON at all"):
        story_to_haiku("A test story", llm_client=mock_llm)


# =============================================================================
# STRUCTURE VALIDATION TESTS
# =============================================================================

def test_missing_lines_key_raises_error():
    """Test that missing 'lines' key raises ValueError."""
    mock_llm = create_mock_llm('missing_lines')

    with pytest.raises(ValueError, match="Missing required keys.*lines"):
        story_to_haiku("A test story", llm_client=mock_llm)


def test_missing_syllables_key_raises_error():
    """Test that missing 'syllables' key raises ValueError."""
    mock_llm = create_mock_llm('missing_syllables')

    with pytest.raises(ValueError, match="Missing required keys.*syllables"):
        story_to_haiku("A test story", llm_client=mock_llm)


def test_missing_essence_key_raises_error():
    """Test that missing 'essence' key raises ValueError."""
    mock_llm = create_mock_llm('missing_essence')

    with pytest.raises(ValueError, match="Missing required keys.*essence"):
        story_to_haiku("A test story", llm_client=mock_llm)


def test_extra_keys_allowed():
    """Test that extra keys in JSON are allowed (forward compatibility)."""
    mock_llm = create_mock_llm('extra_keys')

    # Should not raise error
    result = story_to_haiku("A test story", llm_client=mock_llm)
    assert result is not None


def test_two_lines_raises_error():
    """Test that 2 lines instead of 3 raises ValueError."""
    mock_llm = create_mock_llm('wrong_line_count_2')

    with pytest.raises(ValueError, match="Expected 3 lines.*got 2"):
        story_to_haiku("A test story", llm_client=mock_llm)


def test_four_lines_raises_error():
    """Test that 4 lines instead of 3 raises ValueError."""
    mock_llm = create_mock_llm('wrong_line_count_4')

    with pytest.raises(ValueError, match="Expected 3 lines.*got 4"):
        story_to_haiku("A test story", llm_client=mock_llm)


def test_wrong_syllable_count_raises_error():
    """Test that wrong number of syllable counts raises ValueError."""
    mock_llm = create_mock_llm('wrong_syllable_count')

    with pytest.raises(ValueError, match="Expected 3 syllable counts.*got 2"):
        story_to_haiku("A test story", llm_client=mock_llm)


def test_non_string_lines_raises_error():
    """Test that non-string lines raise ValueError."""
    mock_llm = create_mock_llm('non_string_lines')

    with pytest.raises(ValueError, match="All lines must be strings"):
        story_to_haiku("A test story", llm_client=mock_llm)


def test_non_int_syllables_raises_error():
    """Test that non-integer syllable counts raise ValueError."""
    mock_llm = create_mock_llm('non_int_syllables')

    with pytest.raises(ValueError, match="All syllable counts must be integers"):
        story_to_haiku("A test story", llm_client=mock_llm)


# =============================================================================
# VALIDITY FLAG TESTS
# =============================================================================

def test_valid_flag_true_for_5_7_5():
    """Test that valid flag is True when syllables are [5, 7, 5]."""
    mock_llm = create_mock_llm('spring_valid')
    result = story_to_haiku("A spring story", llm_client=mock_llm)

    assert result['syllables'] == [5, 7, 5]
    assert result['valid'] is True


def test_valid_flag_false_for_non_5_7_5():
    """Test that valid flag is False when syllables don't match [5, 7, 5]."""
    mock_llm = create_mock_llm('invalid_syllables')
    result = story_to_haiku("A test story", llm_client=mock_llm)

    assert result['syllables'] == [8, 4, 3]
    assert result['valid'] is False


def test_invalid_haiku_does_not_raise_error():
    """Test that invalid syllable pattern doesn't raise error, just sets flag."""
    mock_llm = create_mock_llm('invalid_syllables')

    # Should not raise - just return with valid=False
    result = story_to_haiku("A test story", llm_client=mock_llm)
    assert result['valid'] is False


# =============================================================================
# RESULT STRUCTURE TESTS
# =============================================================================

def test_result_has_all_required_fields():
    """Test that result dict contains all required fields."""
    mock_llm = create_mock_llm('winter_valid')
    result = story_to_haiku("A winter story", llm_client=mock_llm)

    required_fields = ['haiku', 'lines', 'syllables', 'essence', 'valid']
    for field in required_fields:
        assert field in result, f"Missing field: {field}"


def test_haiku_string_has_newlines():
    """Test that haiku field is a string with newline separators."""
    mock_llm = create_mock_llm('winter_valid')
    result = story_to_haiku("A winter story", llm_client=mock_llm)

    assert isinstance(result['haiku'], str)
    assert '\n' in result['haiku']
    assert result['haiku'].count('\n') == 2  # Two newlines for three lines


def test_lines_is_list():
    """Test that lines field is a list of strings."""
    mock_llm = create_mock_llm('winter_valid')
    result = story_to_haiku("A winter story", llm_client=mock_llm)

    assert isinstance(result['lines'], list)
    assert len(result['lines']) == 3
    assert all(isinstance(line, str) for line in result['lines'])


def test_syllables_is_list_of_ints():
    """Test that syllables field is a list of integers."""
    mock_llm = create_mock_llm('winter_valid')
    result = story_to_haiku("A winter story", llm_client=mock_llm)

    assert isinstance(result['syllables'], list)
    assert len(result['syllables']) == 3
    assert all(isinstance(count, int) for count in result['syllables'])


def test_essence_is_string():
    """Test that essence field is a non-empty string."""
    mock_llm = create_mock_llm('winter_valid')
    result = story_to_haiku("A winter story", llm_client=mock_llm)

    assert isinstance(result['essence'], str)
    assert len(result['essence']) > 0


def test_valid_is_boolean():
    """Test that valid field is a boolean."""
    mock_llm = create_mock_llm('winter_valid')
    result = story_to_haiku("A winter story", llm_client=mock_llm)

    assert isinstance(result['valid'], bool)


def test_haiku_string_matches_joined_lines():
    """Test that haiku string equals lines joined with newlines."""
    mock_llm = create_mock_llm('coding_valid')
    result = story_to_haiku("A coding story", llm_client=mock_llm)

    expected_haiku = '\n'.join(result['lines'])
    assert result['haiku'] == expected_haiku


# =============================================================================
# LLM INTEGRATION TESTS (MOCKED)
# =============================================================================

def test_mock_injection_works():
    """Test that mock LLM client can be injected."""
    mock_llm = create_mock_llm('spring_valid')
    result = story_to_haiku("Test", llm_client=mock_llm)

    assert mock_llm.generate.called
    assert result is not None


def test_correct_model_used():
    """Test that llama3.2 model is specified."""
    mock_llm = create_mock_llm('spring_valid')
    story_to_haiku("Test", llm_client=mock_llm)

    call_args = mock_llm.generate.call_args
    assert call_args[1]['model'] == 'llama3.2'


def test_prompt_contains_json_template():
    """Test that prompt includes JSON format template."""
    mock_llm = create_mock_llm('spring_valid')
    story_to_haiku("Test story", llm_client=mock_llm)

    call_args = mock_llm.generate.call_args
    prompt = call_args[1]['prompt']

    # Check for key prompt elements
    assert 'JSON' in prompt
    assert '"lines"' in prompt
    assert '"syllables"' in prompt
    assert '"essence"' in prompt
    assert 'Test story' in prompt


def test_prompt_has_5_7_5_instruction():
    """Test that prompt explicitly mentions 5-7-5 structure."""
    mock_llm = create_mock_llm('spring_valid')
    story_to_haiku("Test", llm_client=mock_llm)

    call_args = mock_llm.generate.call_args
    prompt = call_args[1]['prompt']

    assert '5-7-5' in prompt


# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================

def test_llm_generation_failure_raises_runtime_error():
    """Test that LLM generation failure raises RuntimeError."""
    mock_llm = Mock()
    mock_llm.generate.side_effect = Exception("Connection failed")

    with pytest.raises(RuntimeError, match="LLM generation failed"):
        story_to_haiku("Test", llm_client=mock_llm)


# =============================================================================
# EDGE CASES
# =============================================================================

def test_special_characters_in_input():
    """Test that special characters in input don't break processing."""
    mock_llm = create_mock_llm('spring_valid')
    text_with_special = "A story with \"quotes\" and 'apostrophes' and \nnewlines!"

    result = story_to_haiku(text_with_special, llm_client=mock_llm)
    assert result is not None


def test_unicode_characters_in_input():
    """Test that unicode characters are handled correctly."""
    mock_llm = create_mock_llm('spring_valid')
    unicode_text = "A story about cherry blossoms 桜 and tea 茶"

    result = story_to_haiku(unicode_text, llm_client=mock_llm)
    assert result is not None


def test_exact_500_character_input():
    """Test that exactly 500 character input is handled correctly."""
    mock_llm = create_mock_llm('spring_valid')
    text_500 = "a" * 500

    result = story_to_haiku(text_500, llm_client=mock_llm)
    assert result is not None


# =============================================================================
# INTEGRATION SCENARIO TESTS
# =============================================================================

def test_multiple_haiku_generation():
    """Test generating multiple haiku in sequence."""
    stories = [
        "A spring story",
        "A winter tale",
        "A coding adventure"
    ]

    for story in stories:
        mock_llm = create_mock_llm('spring_valid')
        result = story_to_haiku(story, llm_client=mock_llm)
        assert result['valid'] is True


def test_different_response_formats():
    """Test handling different valid response formats."""
    test_cases = ['spring_valid', 'winter_valid', 'coding_valid']

    for response_key in test_cases:
        mock_llm = create_mock_llm(response_key)
        result = story_to_haiku("Test", llm_client=mock_llm)
        assert result is not None
        assert len(result['lines']) == 3


if __name__ == '__main__':
    # Run tests with verbose output
    pytest.main([__file__, '-v'])