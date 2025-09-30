"""Manual test runner for haiku converter (no pytest required)"""

from unittest.mock import Mock
from haiku_converter import story_to_haiku

# Mock responses
MOCK_VALID_HAIKU = "Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive"
MOCK_INVALID_TWO_LINES = "Too short haiku\nOnly has two lines"

def test_returns_three_lines():
    """Test: Returns exactly 3 lines"""
    mock_llm = Mock()
    mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}
    result = story_to_haiku("A story about spring", llm_client=mock_llm)
    assert len(result['lines']) == 3
    print("✓ test_returns_three_lines passed")

def test_haiku_string_has_newlines():
    """Test: Complete haiku has newlines"""
    mock_llm = Mock()
    mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}
    result = story_to_haiku("Test story", llm_client=mock_llm)
    assert '\n' in result['haiku']
    assert result['haiku'].count('\n') == 2
    print("✓ test_haiku_string_has_newlines passed")

def test_returns_required_keys():
    """Test: Response has all required keys"""
    mock_llm = Mock()
    mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}
    result = story_to_haiku("Test", llm_client=mock_llm)
    assert 'haiku' in result
    assert 'lines' in result
    assert 'syllable_counts' in result
    assert 'essence' in result
    print("✓ test_returns_required_keys passed")

def test_empty_input_raises_error():
    """Test: Empty input raises ValueError"""
    try:
        story_to_haiku("")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be empty" in str(e)
        print("✓ test_empty_input_raises_error passed")

def test_whitespace_only_raises_error():
    """Test: Whitespace-only input raises ValueError"""
    try:
        story_to_haiku("   \n\n   ")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be empty" in str(e)
        print("✓ test_whitespace_only_raises_error passed")

def test_invalid_two_line_response_raises_error():
    """Test: Invalid 2-line response raises error"""
    mock_llm = Mock()
    mock_llm.generate.return_value = {'response': MOCK_INVALID_TWO_LINES}
    try:
        story_to_haiku("Test", llm_client=mock_llm)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Expected 3 lines" in str(e)
        print("✓ test_invalid_two_line_response_raises_error passed")

def test_uses_provided_mock_client():
    """Test: Uses injected mock client"""
    mock_llm = Mock()
    mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}
    story_to_haiku("Test story", llm_client=mock_llm)
    mock_llm.generate.assert_called_once()
    call_args = mock_llm.generate.call_args
    assert call_args.kwargs['model'] == 'llama3.2'
    assert 'Test story' in call_args.kwargs['prompt']
    print("✓ test_uses_provided_mock_client passed")

def test_truncates_long_input():
    """Test: Truncates very long input"""
    mock_llm = Mock()
    mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}
    long_story = "word " * 1000  # 5000 chars
    story_to_haiku(long_story, llm_client=mock_llm)
    call_args = mock_llm.generate.call_args
    prompt = call_args.kwargs['prompt']
    assert len(prompt) < len(long_story)
    print("✓ test_truncates_long_input passed")

def test_returns_syllable_counts():
    """Test: Returns syllable counts"""
    mock_llm = Mock()
    mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}
    result = story_to_haiku("Test", llm_client=mock_llm)
    assert isinstance(result['syllable_counts'], list)
    assert len(result['syllable_counts']) == 3
    assert all(isinstance(count, int) for count in result['syllable_counts'])
    print("✓ test_returns_syllable_counts passed")

def test_returns_essence_string():
    """Test: Returns essence string"""
    mock_llm = Mock()
    mock_llm.generate.return_value = {'response': MOCK_VALID_HAIKU}
    result = story_to_haiku("A story about spring flowers", llm_client=mock_llm)
    assert isinstance(result['essence'], str)
    assert len(result['essence']) > 0
    print("✓ test_returns_essence_string passed")


if __name__ == '__main__':
    print("\nRunning Adaptive TDD Tests...\n")
    print("=" * 50)

    test_returns_three_lines()
    test_haiku_string_has_newlines()
    test_returns_required_keys()
    test_empty_input_raises_error()
    test_whitespace_only_raises_error()
    test_invalid_two_line_response_raises_error()
    test_uses_provided_mock_client()
    test_truncates_long_input()
    test_returns_syllable_counts()
    test_returns_essence_string()

    print("=" * 50)
    print("\n✓ All tests passed!\n")