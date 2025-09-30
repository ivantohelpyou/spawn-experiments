"""
Quick verification script to test implementation without pytest.
This demonstrates that the implementation works correctly with mocks.
"""

import json
from haiku_converter import story_to_haiku


class MockLLMClient:
    """Simple mock for testing."""
    def __init__(self, response_data):
        self.response_data = response_data

    def chat(self, model, messages, format):
        if isinstance(self.response_data, dict):
            content = json.dumps(self.response_data)
        else:
            content = self.response_data
        return {'message': {'content': content}}


def test_valid_haiku():
    """Test valid haiku generation."""
    mock_response = {
        "lines": [
            "Cherry blossoms fall",
            "Softly on the quiet pond",
            "Spring whispers arrive"
        ],
        "syllables": [5, 7, 5],
        "essence": "Spring's gentle transition"
    }
    mock = MockLLMClient(mock_response)
    result = story_to_haiku("Spring story", llm_client=mock)

    assert result['valid'] is True
    assert result['syllables'] == [5, 7, 5]
    assert len(result['lines']) == 3
    assert 'error' not in result
    print("✓ Valid haiku test passed")


def test_invalid_syllables():
    """Test invalid syllable counts."""
    mock_response = {
        "lines": ["Line 1", "Line 2", "Line 3"],
        "syllables": [4, 8, 5],
        "essence": "Test"
    }
    mock = MockLLMClient(mock_response)
    result = story_to_haiku("Test", llm_client=mock)

    assert result['valid'] is False
    assert result['syllables'] == [4, 8, 5]
    print("✓ Invalid syllables test passed")


def test_empty_input():
    """Test empty input validation."""
    mock = MockLLMClient({})
    result = story_to_haiku("", llm_client=mock)

    assert 'error' in result
    assert result['valid'] is False
    print("✓ Empty input test passed")


def test_malformed_json():
    """Test malformed JSON handling."""
    mock = MockLLMClient("{ invalid json }")
    result = story_to_haiku("Test", llm_client=mock)

    assert 'error' in result
    assert 'parse' in result['error'].lower()
    print("✓ Malformed JSON test passed")


def test_missing_keys():
    """Test missing JSON keys."""
    mock_response = {
        "lines": ["Line 1", "Line 2", "Line 3"],
        "syllables": [5, 7, 5]
        # Missing 'essence'
    }
    mock = MockLLMClient(mock_response)
    result = story_to_haiku("Test", llm_client=mock)

    assert 'error' in result
    assert 'essence' in result['error'].lower()
    print("✓ Missing keys test passed")


if __name__ == "__main__":
    print("Running verification tests...\n")

    try:
        test_valid_haiku()
        test_invalid_syllables()
        test_empty_input()
        test_malformed_json()
        test_missing_keys()

        print("\n✓ All verification tests passed!")
        print("\nImplementation is working correctly.")
        print("Note: Full test suite (24 tests) requires pytest.")

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        exit(1)
