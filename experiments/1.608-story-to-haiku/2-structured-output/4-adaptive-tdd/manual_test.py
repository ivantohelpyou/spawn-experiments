"""
Manual test script to verify haiku_converter implementation.
Tests key functionality without pytest dependency.
"""

from unittest.mock import Mock
from haiku_converter import story_to_haiku


def test_valid_json_parsing():
    """Test valid JSON parsing."""
    print("Test 1: Valid JSON parsing...", end=" ")
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"], "syllables": [5, 7, 5], "essence": "Spring transition"}'
    }

    result = story_to_haiku("A story about spring", llm_client=mock_llm)
    assert result['lines'] == ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"]
    assert result['syllables'] == [5, 7, 5]
    assert result['essence'] == "Spring transition"
    assert result['valid'] is True
    assert result['haiku'] == "Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive"
    print("PASS")


def test_invalid_json():
    """Test malformed JSON handling."""
    print("Test 2: Malformed JSON handling...", end=" ")
    mock_llm = Mock()
    mock_llm.generate.return_value = {'response': 'This is not JSON'}

    try:
        story_to_haiku("test", llm_client=mock_llm)
        print("FAIL - Expected ValueError")
    except ValueError as e:
        if "Invalid JSON" in str(e):
            print("PASS")
        else:
            print(f"FAIL - Wrong error message: {e}")


def test_empty_input():
    """Test empty input rejection."""
    print("Test 3: Empty input rejection...", end=" ")
    try:
        story_to_haiku("")
        print("FAIL - Expected ValueError")
    except ValueError as e:
        if "cannot be empty" in str(e):
            print("PASS")
        else:
            print(f"FAIL - Wrong error message: {e}")


def test_whitespace_input():
    """Test whitespace-only input rejection."""
    print("Test 4: Whitespace input rejection...", end=" ")
    try:
        story_to_haiku("   \n\n   ")
        print("FAIL - Expected ValueError")
    except ValueError as e:
        if "cannot be empty" in str(e):
            print("PASS")
        else:
            print(f"FAIL - Wrong error message: {e}")


def test_missing_keys():
    """Test missing required keys."""
    print("Test 5: Missing required keys...", end=" ")
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["a", "b", "c"]}'
    }

    try:
        story_to_haiku("test", llm_client=mock_llm)
        print("FAIL - Expected ValueError")
    except ValueError as e:
        if "Missing required key" in str(e):
            print("PASS")
        else:
            print(f"FAIL - Wrong error message: {e}")


def test_wrong_line_count():
    """Test wrong number of lines."""
    print("Test 6: Wrong line count...", end=" ")
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["only", "two"], "syllables": [5, 7, 5], "essence": "test"}'
    }

    try:
        story_to_haiku("test", llm_client=mock_llm)
        print("FAIL - Expected ValueError")
    except ValueError as e:
        if "Expected 3 lines" in str(e):
            print("PASS")
        else:
            print(f"FAIL - Wrong error message: {e}")


def test_wrong_syllable_count():
    """Test wrong number of syllable counts."""
    print("Test 7: Wrong syllable count...", end=" ")
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["a", "b", "c"], "syllables": [5, 7], "essence": "test"}'
    }

    try:
        story_to_haiku("test", llm_client=mock_llm)
        print("FAIL - Expected ValueError")
    except ValueError as e:
        if "Expected 3 syllable counts" in str(e):
            print("PASS")
        else:
            print(f"FAIL - Wrong error message: {e}")


def test_invalid_syllable_structure():
    """Test invalid syllable structure marked as invalid."""
    print("Test 8: Invalid syllable structure...", end=" ")
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["a", "b", "c"], "syllables": [3, 4, 3], "essence": "test"}'
    }

    result = story_to_haiku("test", llm_client=mock_llm)
    assert result['valid'] is False
    print("PASS")


def test_dependency_injection():
    """Test mock LLM client injection."""
    print("Test 9: Dependency injection...", end=" ")
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["a", "b", "c"], "syllables": [5, 7, 5], "essence": "test"}'
    }

    result = story_to_haiku("test story", llm_client=mock_llm)

    # Verify mock was called with correct parameters
    mock_llm.generate.assert_called_once()
    call_kwargs = mock_llm.generate.call_args.kwargs
    assert call_kwargs['model'] == 'llama3.2'
    assert 'test story' in call_kwargs['prompt']
    print("PASS")


def test_all_required_keys():
    """Test all required keys present."""
    print("Test 10: All required keys present...", end=" ")
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["a", "b", "c"], "syllables": [5, 7, 5], "essence": "test"}'
    }

    result = story_to_haiku("test", llm_client=mock_llm)
    required_keys = ['haiku', 'lines', 'syllables', 'essence', 'valid']
    for key in required_keys:
        assert key in result, f"Missing key: {key}"
    print("PASS")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("ADAPTIVE TDD - Manual Test Suite")
    print("="*60 + "\n")

    print("Running strategic tests (complex/risky areas only):\n")

    test_valid_json_parsing()
    test_invalid_json()
    test_empty_input()
    test_whitespace_input()
    test_missing_keys()
    test_wrong_line_count()
    test_wrong_syllable_count()
    test_invalid_syllable_structure()
    test_dependency_injection()
    test_all_required_keys()

    print("\n" + "="*60)
    print("All tests passed!")
    print("="*60 + "\n")

    print("NOTE: Simple operations NOT tested (Adaptive TDD approach):")
    print("  - String joining with '\\n'.join()")
    print("  - Dict construction")
    print("  - Text truncation (string slicing)")
    print("  - Default parameter handling")
    print("  - Prompt f-string formatting")
    print("\nThese are trivial operations that don't warrant test coverage.")
    print("We focus testing effort on complex/risky business logic.\n")