"""Simple test runner without pytest dependency"""

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


def run_test(test_name, test_func):
    """Run a single test and report result"""
    try:
        test_func()
        print(f"✓ {test_name}")
        return True
    except AssertionError as e:
        print(f"✗ {test_name}: {e}")
        return False
    except Exception as e:
        print(f"✗ {test_name}: ERROR - {e}")
        return False


def test_returns_three_lines():
    mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['spring'])
    result = story_to_haiku("A story about spring", llm_client=mock_llm)
    assert len(result['lines']) == 3


def test_validates_syllable_structure():
    mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['winter'])
    result = story_to_haiku("A story about winter", llm_client=mock_llm)
    assert len(result['syllable_counts']) == 3
    assert all(isinstance(count, int) for count in result['syllable_counts'])


def test_includes_complete_haiku_string():
    mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['autumn'])
    result = story_to_haiku("A story about autumn", llm_client=mock_llm)
    assert '\n' in result['haiku']
    assert result['haiku'].count('\n') == 2


def test_empty_input_raises_error():
    try:
        story_to_haiku("")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_whitespace_only_raises_error():
    try:
        story_to_haiku("   \n\n   ")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_very_long_input_truncated():
    mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['coding'])
    long_story = "word " * 1000
    result = story_to_haiku(long_story, llm_client=mock_llm)
    assert len(result['lines']) == 3


def test_uses_provided_llm_client():
    mock_llm = create_mock_llm(MOCK_HAIKU_RESPONSES['spring'])
    story_to_haiku("test story", llm_client=mock_llm)
    mock_llm.generate.assert_called_once()


def test_syllable_counter():
    assert count_syllables("hello") == 2
    assert count_syllables("world") == 1
    assert count_syllables("beautiful") == 3  # beau-ti-ful
    assert count_syllables("code") == 1


def test_line_syllable_counter():
    assert count_line_syllables("hello world") == 3
    assert count_line_syllables("code lines flow") == 4  # code(1) lines(1) flow(2)


def test_result_structure():
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


if __name__ == '__main__':
    print("Running Story-to-Haiku Converter Tests (Method 1)\n")

    tests = [
        ("Returns three lines", test_returns_three_lines),
        ("Validates syllable structure", test_validates_syllable_structure),
        ("Includes complete haiku string", test_includes_complete_haiku_string),
        ("Empty input raises error", test_empty_input_raises_error),
        ("Whitespace only raises error", test_whitespace_only_raises_error),
        ("Very long input truncated", test_very_long_input_truncated),
        ("Uses provided LLM client", test_uses_provided_llm_client),
        ("Syllable counter", test_syllable_counter),
        ("Line syllable counter", test_line_syllable_counter),
        ("Result structure", test_result_structure),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*50}")

    if failed > 0:
        exit(1)