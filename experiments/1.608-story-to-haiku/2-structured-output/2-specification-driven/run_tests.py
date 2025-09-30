"""
Simple test runner for haiku converter (no pytest required)
"""

from unittest.mock import Mock
from haiku_converter import story_to_haiku


# Mock Response Templates
MOCK_RESPONSES = {
    'spring_valid': {
        'response': '{"lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"], '
                   '"syllables": [5, 7, 5], "essence": "Spring\'s gentle transition"}'
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
}


def create_mock_llm(response_key: str) -> Mock:
    """Create a mock LLM client for testing."""
    mock = Mock()
    mock.generate.return_value = MOCK_RESPONSES[response_key]
    return mock


def run_tests():
    """Run all tests and report results."""
    tests_passed = 0
    tests_failed = 0

    print("Running Story-to-Haiku Converter Tests")
    print("=" * 60)

    # Test 1: Valid input
    try:
        mock_llm = create_mock_llm('spring_valid')
        result = story_to_haiku("A spring story", llm_client=mock_llm)
        assert result['lines'] == ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"]
        assert result['syllables'] == [5, 7, 5]
        assert result['valid'] is True
        print("✓ Test 1: Valid JSON parsing - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Test 1: Valid JSON parsing - FAILED: {e}")
        tests_failed += 1

    # Test 2: Empty input
    try:
        story_to_haiku("")
        print("✗ Test 2: Empty input validation - FAILED (should raise ValueError)")
        tests_failed += 1
    except ValueError:
        print("✓ Test 2: Empty input validation - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Test 2: Empty input validation - FAILED: {e}")
        tests_failed += 1

    # Test 3: Whitespace input
    try:
        story_to_haiku("   \n\n   ")
        print("✗ Test 3: Whitespace input validation - FAILED (should raise ValueError)")
        tests_failed += 1
    except ValueError:
        print("✓ Test 3: Whitespace input validation - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Test 3: Whitespace input validation - FAILED: {e}")
        tests_failed += 1

    # Test 4: Invalid syllables (but valid structure)
    try:
        mock_llm = create_mock_llm('invalid_syllables')
        result = story_to_haiku("A test story", llm_client=mock_llm)
        assert result['syllables'] == [8, 4, 3]
        assert result['valid'] is False  # Should be False, not raise error
        print("✓ Test 4: Invalid syllables flag - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Test 4: Invalid syllables flag - FAILED: {e}")
        tests_failed += 1

    # Test 5: Malformed JSON
    try:
        mock_llm = create_mock_llm('malformed_json')
        story_to_haiku("A test story", llm_client=mock_llm)
        print("✗ Test 5: Malformed JSON error - FAILED (should raise ValueError)")
        tests_failed += 1
    except ValueError as e:
        if "Invalid JSON" in str(e):
            print("✓ Test 5: Malformed JSON error - PASSED")
            tests_passed += 1
        else:
            print(f"✗ Test 5: Malformed JSON error - FAILED (wrong error message): {e}")
            tests_failed += 1
    except Exception as e:
        print(f"✗ Test 5: Malformed JSON error - FAILED: {e}")
        tests_failed += 1

    # Test 6: Missing required keys
    try:
        mock_llm = create_mock_llm('missing_lines')
        story_to_haiku("A test story", llm_client=mock_llm)
        print("✗ Test 6: Missing required keys - FAILED (should raise ValueError)")
        tests_failed += 1
    except ValueError as e:
        if "Missing required keys" in str(e):
            print("✓ Test 6: Missing required keys - PASSED")
            tests_passed += 1
        else:
            print(f"✗ Test 6: Missing required keys - FAILED (wrong error message): {e}")
            tests_failed += 1
    except Exception as e:
        print(f"✗ Test 6: Missing required keys - FAILED: {e}")
        tests_failed += 1

    # Test 7: Result structure
    try:
        mock_llm = create_mock_llm('spring_valid')
        result = story_to_haiku("A test story", llm_client=mock_llm)
        required_fields = ['haiku', 'lines', 'syllables', 'essence', 'valid']
        for field in required_fields:
            assert field in result
        assert isinstance(result['haiku'], str)
        assert '\n' in result['haiku']
        assert isinstance(result['lines'], list)
        assert len(result['lines']) == 3
        assert isinstance(result['syllables'], list)
        assert isinstance(result['valid'], bool)
        print("✓ Test 7: Result structure - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Test 7: Result structure - FAILED: {e}")
        tests_failed += 1

    # Test 8: LLM integration (mock)
    try:
        mock_llm = create_mock_llm('spring_valid')
        story_to_haiku("Test story", llm_client=mock_llm)
        assert mock_llm.generate.called
        call_args = mock_llm.generate.call_args
        assert call_args[1]['model'] == 'llama3.2'
        prompt = call_args[1]['prompt']
        assert 'JSON' in prompt
        assert '5-7-5' in prompt
        assert 'Test story' in prompt
        print("✓ Test 8: LLM integration - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Test 8: LLM integration - FAILED: {e}")
        tests_failed += 1

    # Test 9: Long input truncation
    try:
        mock_llm = create_mock_llm('spring_valid')
        long_text = "word " * 200  # 1000 chars
        result = story_to_haiku(long_text, llm_client=mock_llm)
        call_args = mock_llm.generate.call_args
        prompt = call_args[1]['prompt']
        # Should not contain all 200 "word" repetitions
        assert prompt.count("word") < 150  # Truncated
        print("✓ Test 9: Input truncation - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Test 9: Input truncation - FAILED: {e}")
        tests_failed += 1

    # Test 10: Haiku string formatting
    try:
        mock_llm = create_mock_llm('spring_valid')
        result = story_to_haiku("A test", llm_client=mock_llm)
        expected_haiku = '\n'.join(result['lines'])
        assert result['haiku'] == expected_haiku
        print("✓ Test 10: Haiku string formatting - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Test 10: Haiku string formatting - FAILED: {e}")
        tests_failed += 1

    # Summary
    print("=" * 60)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print(f"Total Tests: {tests_passed + tests_failed}")
    print("=" * 60)

    if tests_failed == 0:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n❌ {tests_failed} test(s) failed")
        return False


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)