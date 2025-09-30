"""
Simple test runner without pytest dependency.
Runs all tests from test_haiku_converter.py
"""

import json
import sys
import traceback
from haiku_converter import story_to_haiku


# Mock LLM Client for Testing
class MockLLMClient:
    """Mock LLM client that returns predefined JSON responses."""

    def __init__(self, response_json: str):
        self.response_json = response_json

    def chat(self, model: str, messages: list, format: str):
        class MockResponse:
            def __init__(self, content):
                self.message = {'content': content}
        return MockResponse(self.response_json)


class MockLLMClientError:
    """Mock LLM client that raises an exception."""

    def chat(self, model: str, messages: list, format: str):
        raise Exception("Simulated LLM failure")


# Test Runner
class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def run_test(self, test_name, test_func):
        """Run a single test function."""
        try:
            test_func()
            self.passed += 1
            print(f"✓ {test_name}")
            return True
        except AssertionError as e:
            self.failed += 1
            self.errors.append((test_name, str(e)))
            print(f"✗ {test_name}: {e}")
            return False
        except Exception as e:
            self.failed += 1
            self.errors.append((test_name, str(e)))
            print(f"✗ {test_name}: Unexpected error: {e}")
            return False

    def print_summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")
        if self.failed > 0:
            print(f"\nFailed tests ({self.failed}):")
            for name, error in self.errors:
                print(f"  - {name}: {error}")
        return self.failed == 0


# Test Functions
def test_empty_string_raises_error():
    """Empty string should raise ValueError."""
    try:
        story_to_haiku("")
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        assert "empty or whitespace" in str(e).lower()


def test_whitespace_only_raises_error():
    """Whitespace-only string should raise ValueError."""
    try:
        story_to_haiku("   ")
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        assert "empty or whitespace" in str(e).lower()


def test_valid_575_haiku():
    """Valid 5-7-5 haiku should return valid=True."""
    mock_response = json.dumps({
        "lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"],
        "syllables": [5, 7, 5],
        "essence": "Spring's gentle transition"
    })
    mock_client = MockLLMClient(mock_response)
    result = story_to_haiku("Any text here", llm_client=mock_client)

    assert result['valid'] is True
    assert result['syllables'] == [5, 7, 5]
    assert len(result['lines']) == 3
    assert result['haiku'] == "Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive"
    assert result['essence'] == "Spring's gentle transition"


def test_all_required_keys_present():
    """Response must contain all required keys."""
    mock_response = json.dumps({
        "lines": ["Line one", "Line two", "Line three"],
        "syllables": [5, 7, 5],
        "essence": "Test essence"
    })
    mock_client = MockLLMClient(mock_response)
    result = story_to_haiku("Test", llm_client=mock_client)

    required_keys = ['haiku', 'lines', 'syllables', 'essence', 'valid']
    for key in required_keys:
        assert key in result, f"Missing required key: {key}"


def test_invalid_pattern_485():
    """Invalid pattern [4,8,5] should return valid=False but still work."""
    mock_response = json.dumps({
        "lines": ["Four syllables", "Eight syllables in this line", "Five syllables"],
        "syllables": [4, 8, 5],
        "essence": "Invalid pattern"
    })
    mock_client = MockLLMClient(mock_response)
    result = story_to_haiku("Test", llm_client=mock_client)

    assert result['valid'] is False
    assert result['syllables'] == [4, 8, 5]


def test_malformed_json_raises_error():
    """Malformed JSON should raise JSONDecodeError."""
    mock_client = MockLLMClient("{invalid json")
    try:
        story_to_haiku("Test", llm_client=mock_client)
        raise AssertionError("Should have raised JSONDecodeError")
    except json.JSONDecodeError:
        pass


def test_missing_lines_key():
    """Missing 'lines' key should raise KeyError."""
    mock_response = json.dumps({
        "syllables": [5, 7, 5],
        "essence": "Test"
    })
    mock_client = MockLLMClient(mock_response)
    try:
        story_to_haiku("Test", llm_client=mock_client)
        raise AssertionError("Should have raised KeyError")
    except KeyError as e:
        assert "lines" in str(e).lower()


def test_lines_not_list():
    """'lines' must be a list."""
    mock_response = json.dumps({
        "lines": "not a list",
        "syllables": [5, 7, 5],
        "essence": "Test"
    })
    mock_client = MockLLMClient(mock_response)
    try:
        story_to_haiku("Test", llm_client=mock_client)
        raise AssertionError("Should have raised TypeError")
    except TypeError as e:
        assert "lines" in str(e).lower() and "list" in str(e).lower()


def test_lines_wrong_length():
    """'lines' must contain exactly 3 elements."""
    mock_response = json.dumps({
        "lines": ["One", "Two"],
        "syllables": [5, 7, 5],
        "essence": "Test"
    })
    mock_client = MockLLMClient(mock_response)
    try:
        story_to_haiku("Test", llm_client=mock_client)
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        assert "3" in str(e)


def test_syllables_contain_non_integers():
    """All elements in 'syllables' must be integers."""
    mock_response = json.dumps({
        "lines": ["One", "Two", "Three"],
        "syllables": [5, "seven", 5],
        "essence": "Test"
    })
    mock_client = MockLLMClient(mock_response)
    try:
        story_to_haiku("Test", llm_client=mock_client)
        raise AssertionError("Should have raised TypeError")
    except TypeError as e:
        assert "integer" in str(e).lower()


def test_llm_exception_raises_runtime_error():
    """LLM failure should raise RuntimeError."""
    mock_client = MockLLMClientError()
    try:
        story_to_haiku("Test", llm_client=mock_client)
        raise AssertionError("Should have raised RuntimeError")
    except RuntimeError as e:
        assert "llm invocation failed" in str(e).lower()


def test_haiku_constructed_with_newlines():
    """Haiku string should join lines with newlines."""
    mock_response = json.dumps({
        "lines": ["First", "Second", "Third"],
        "syllables": [5, 7, 5],
        "essence": "Numbers"
    })
    mock_client = MockLLMClient(mock_response)
    result = story_to_haiku("Test", llm_client=mock_client)

    assert result['haiku'] == "First\nSecond\nThird"
    assert '\n' in result['haiku']


def test_response_types():
    """Test that all response fields have correct types."""
    mock_response = json.dumps({
        "lines": ["Test", "Type", "Check"],
        "syllables": [5, 7, 5],
        "essence": "Type verification"
    })
    mock_client = MockLLMClient(mock_response)
    result = story_to_haiku("Test", llm_client=mock_client)

    assert isinstance(result, dict)
    assert isinstance(result['haiku'], str)
    assert isinstance(result['lines'], list)
    assert isinstance(result['syllables'], list)
    assert isinstance(result['essence'], str)
    assert isinstance(result['valid'], bool)


def test_special_characters():
    """Should handle special characters."""
    special_text = "Test with @#$% special *&^() characters!"
    mock_response = json.dumps({
        "lines": ["Special", "Characters", "Work"],
        "syllables": [5, 7, 5],
        "essence": "Special chars handled"
    })
    mock_client = MockLLMClient(mock_response)
    result = story_to_haiku(special_text, llm_client=mock_client)
    assert result is not None


def test_unicode_characters():
    """Should handle Unicode characters."""
    unicode_text = "Test with émojis 🌸 and ñoñó characters"
    mock_response = json.dumps({
        "lines": ["Unicode", "Characters", "Work"],
        "syllables": [5, 7, 5],
        "essence": "Unicode handled"
    })
    mock_client = MockLLMClient(mock_response)
    result = story_to_haiku(unicode_text, llm_client=mock_client)
    assert result is not None


# Main test execution
if __name__ == "__main__":
    runner = TestRunner()

    print("Running Story-to-Haiku Converter Tests")
    print("=" * 60)

    # Input Validation Tests
    print("\n[Input Validation]")
    runner.run_test("Empty string raises error", test_empty_string_raises_error)
    runner.run_test("Whitespace only raises error", test_whitespace_only_raises_error)

    # Valid Response Tests
    print("\n[Valid Haiku Response]")
    runner.run_test("Valid 5-7-5 haiku", test_valid_575_haiku)
    runner.run_test("All required keys present", test_all_required_keys_present)
    runner.run_test("Haiku with newlines", test_haiku_constructed_with_newlines)

    # Invalid Syllable Tests
    print("\n[Invalid Syllable Patterns]")
    runner.run_test("Invalid pattern 4-8-5", test_invalid_pattern_485)

    # JSON Parsing Tests
    print("\n[JSON Parsing]")
    runner.run_test("Malformed JSON raises error", test_malformed_json_raises_error)
    runner.run_test("Missing lines key", test_missing_lines_key)

    # Structure Validation Tests
    print("\n[Structure Validation]")
    runner.run_test("Lines not list", test_lines_not_list)
    runner.run_test("Lines wrong length", test_lines_wrong_length)
    runner.run_test("Syllables contain non-integers", test_syllables_contain_non_integers)

    # LLM Failure Tests
    print("\n[LLM Failures]")
    runner.run_test("LLM exception raises RuntimeError", test_llm_exception_raises_runtime_error)

    # Type Tests
    print("\n[Response Format]")
    runner.run_test("Response types correct", test_response_types)

    # Edge Cases
    print("\n[Edge Cases]")
    runner.run_test("Special characters", test_special_characters)
    runner.run_test("Unicode characters", test_unicode_characters)

    # Print summary
    success = runner.print_summary()
    sys.exit(0 if success else 1)
