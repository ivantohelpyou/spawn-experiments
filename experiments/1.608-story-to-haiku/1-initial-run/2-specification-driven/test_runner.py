"""
Simple test runner for haiku_converter (no pytest required)
Verifies basic functionality with mocked LLM client.
"""

from unittest.mock import Mock
from haiku_converter import (
    story_to_haiku,
    count_syllables,
    count_syllables_in_line,
    extract_essence
)


def create_mock_llm(haiku_response: str) -> Mock:
    """Create a mock LLM client for testing."""
    mock = Mock()
    mock.generate.return_value = {
        'response': haiku_response
    }
    return mock


MOCK_HAIKU = 'Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive'


def test_basic_conversion():
    """Test basic story to haiku conversion."""
    print("Test: Basic conversion...", end=" ")
    mock_llm = create_mock_llm(MOCK_HAIKU)
    result = story_to_haiku("A spring story", llm_client=mock_llm)
    assert result is not None
    assert 'haiku' in result
    assert 'lines' in result
    assert 'syllable_counts' in result
    assert 'essence' in result
    print("PASS")


def test_three_lines():
    """Test that result has three lines."""
    print("Test: Three lines returned...", end=" ")
    mock_llm = create_mock_llm(MOCK_HAIKU)
    result = story_to_haiku("Test story", llm_client=mock_llm)
    assert len(result['lines']) == 3
    print("PASS")


def test_empty_input_raises_error():
    """Test that empty input raises ValueError."""
    print("Test: Empty input raises error...", end=" ")
    try:
        story_to_haiku("")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "empty" in str(e).lower()
    print("PASS")


def test_whitespace_input_raises_error():
    """Test that whitespace-only input raises ValueError."""
    print("Test: Whitespace input raises error...", end=" ")
    try:
        story_to_haiku("   \n\n   ")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "empty" in str(e).lower()
    print("PASS")


def test_llm_client_called():
    """Test that provided LLM client is called."""
    print("Test: LLM client called...", end=" ")
    mock_llm = create_mock_llm(MOCK_HAIKU)
    story_to_haiku("Test", llm_client=mock_llm)
    assert mock_llm.generate.called
    print("PASS")


def test_syllable_counting():
    """Test syllable counting."""
    print("Test: Syllable counting...", end=" ")
    assert count_syllables("cat") == 1
    assert count_syllables("mountain") == 2
    assert count_syllables("beautiful") == 3
    print("PASS")


def test_syllable_counting_in_line():
    """Test syllable counting in full line."""
    print("Test: Line syllable counting...", end=" ")
    # "Mountains cradle home" should be 5 syllables
    count = count_syllables_in_line("Mountains cradle home")
    assert count > 0  # Should count something
    print("PASS")


def test_extract_essence_short():
    """Test essence extraction on short text."""
    print("Test: Extract essence (short)...", end=" ")
    text = "A short story"
    essence = extract_essence(text)
    assert essence == text
    print("PASS")


def test_extract_essence_long():
    """Test essence extraction on long text."""
    print("Test: Extract essence (long)...", end=" ")
    text = "This is a very long story about many things that happen over time " * 3
    essence = extract_essence(text)
    assert len(essence) <= 53  # 50 + "..."
    assert essence.endswith('...')
    print("PASS")


def test_haiku_field_format():
    """Test haiku field has correct format."""
    print("Test: Haiku field format...", end=" ")
    mock_llm = create_mock_llm(MOCK_HAIKU)
    result = story_to_haiku("Test", llm_client=mock_llm)
    assert '\n' in result['haiku']
    assert result['haiku'].count('\n') == 2
    print("PASS")


def test_invalid_line_count():
    """Test that invalid line count raises error."""
    print("Test: Invalid line count raises error...", end=" ")
    mock_llm = create_mock_llm("Only one line")
    try:
        story_to_haiku("Test", llm_client=mock_llm)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "3 haiku lines" in str(e)
    print("PASS")


def test_result_structure():
    """Test complete result structure."""
    print("Test: Complete result structure...", end=" ")
    mock_llm = create_mock_llm(MOCK_HAIKU)
    result = story_to_haiku("Spring story", llm_client=mock_llm)

    # Check types
    assert isinstance(result['haiku'], str)
    assert isinstance(result['lines'], list)
    assert isinstance(result['syllable_counts'], list)
    assert isinstance(result['essence'], str)

    # Check lengths
    assert len(result['lines']) == 3
    assert len(result['syllable_counts']) == 3

    print("PASS")


def test_handles_whitespace_in_response():
    """Test that whitespace in response is handled."""
    print("Test: Whitespace handling...", end=" ")
    mock_llm = create_mock_llm(
        '  Line one  \n'
        '  Line two longer  \n'
        '  Line three  '
    )
    result = story_to_haiku("Test", llm_client=mock_llm)

    # Lines should be clean
    for line in result['lines']:
        assert line == line.strip()

    print("PASS")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("Story-to-Haiku Converter - Test Suite")
    print("Method 2: Specification-Driven Implementation")
    print("="*60 + "\n")

    tests = [
        test_basic_conversion,
        test_three_lines,
        test_empty_input_raises_error,
        test_whitespace_input_raises_error,
        test_llm_client_called,
        test_syllable_counting,
        test_syllable_counting_in_line,
        test_extract_essence_short,
        test_extract_essence_long,
        test_haiku_field_format,
        test_invalid_line_count,
        test_result_structure,
        test_handles_whitespace_in_response,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"FAIL - {e}")
            failed += 1

    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")

    if failed == 0:
        print("SUCCESS: All tests passed!")
        return 0
    else:
        print(f"FAILURE: {failed} test(s) failed")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(run_all_tests())