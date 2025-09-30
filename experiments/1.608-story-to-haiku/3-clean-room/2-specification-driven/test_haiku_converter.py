"""
Comprehensive Test Suite for Story-to-Haiku Converter
Method 2: Specification-Driven Implementation

Tests use mocks for fast execution without requiring Ollama.
"""

import json
import pytest
from haiku_converter import story_to_haiku


# Mock LLM Client for Testing
class MockLLMClient:
    """Mock LLM client that returns predefined JSON responses."""

    def __init__(self, response_json: str):
        """
        Initialize mock client with a JSON response string.

        Args:
            response_json: JSON string to return when chat() is called
        """
        self.response_json = response_json

    def chat(self, model: str, messages: list, format: str):
        """
        Mock chat method that returns predefined response.

        Args:
            model: Model name (ignored in mock)
            messages: Messages list (ignored in mock)
            format: Output format (ignored in mock)

        Returns:
            Mock response object with message.content structure
        """
        class MockResponse:
            def __init__(self, content):
                self.message = {'content': content}

        return MockResponse(self.response_json)


class MockLLMClientError:
    """Mock LLM client that raises an exception."""

    def chat(self, model: str, messages: list, format: str):
        raise Exception("Simulated LLM failure")


# Test Cases

class TestInputValidation:
    """Test input validation requirements."""

    def test_empty_string_raises_error(self):
        """Empty string should raise ValueError."""
        with pytest.raises(ValueError, match="empty or whitespace"):
            story_to_haiku("")

    def test_whitespace_only_raises_error(self):
        """Whitespace-only string should raise ValueError."""
        with pytest.raises(ValueError, match="empty or whitespace"):
            story_to_haiku("   ")

    def test_whitespace_with_tabs_raises_error(self):
        """Tabs and spaces should raise ValueError."""
        with pytest.raises(ValueError, match="empty or whitespace"):
            story_to_haiku("\t\n  ")

    def test_valid_text_accepted(self):
        """Valid non-empty text should be accepted."""
        mock_response = json.dumps({
            "lines": ["Test line one here", "Test line two is longer", "Test line three here"],
            "syllables": [5, 7, 5],
            "essence": "Testing essence"
        })
        mock_client = MockLLMClient(mock_response)
        result = story_to_haiku("Valid input text", llm_client=mock_client)
        assert result is not None


class TestValidHaikuResponse:
    """Test handling of valid haiku responses."""

    def test_valid_575_haiku(self):
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

    def test_all_required_keys_present(self):
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

    def test_haiku_constructed_with_newlines(self):
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


class TestInvalidSyllablePattern:
    """Test handling of non-5-7-5 syllable patterns."""

    def test_invalid_pattern_485(self):
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
        assert len(result['lines']) == 3
        # Function should still return result, not raise error

    def test_invalid_pattern_666(self):
        """Pattern [6,6,6] should return valid=False."""
        mock_response = json.dumps({
            "lines": ["Six syllables here", "Another six syllables", "Six syllables again"],
            "syllables": [6, 6, 6],
            "essence": "Invalid pattern"
        })
        mock_client = MockLLMClient(mock_response)
        result = story_to_haiku("Test", llm_client=mock_client)

        assert result['valid'] is False
        assert result['syllables'] == [6, 6, 6]

    def test_zero_syllables(self):
        """Zero syllables should return valid=False."""
        mock_response = json.dumps({
            "lines": ["", "", ""],
            "syllables": [0, 0, 0],
            "essence": "Empty"
        })
        mock_client = MockLLMClient(mock_response)
        result = story_to_haiku("Test", llm_client=mock_client)

        assert result['valid'] is False


class TestJSONParsingErrors:
    """Test handling of malformed JSON responses."""

    def test_malformed_json_raises_error(self):
        """Malformed JSON should raise JSONDecodeError."""
        mock_client = MockLLMClient("{invalid json")
        with pytest.raises(json.JSONDecodeError):
            story_to_haiku("Test", llm_client=mock_client)

    def test_empty_json_raises_error(self):
        """Empty string should raise JSONDecodeError."""
        mock_client = MockLLMClient("")
        with pytest.raises(json.JSONDecodeError):
            story_to_haiku("Test", llm_client=mock_client)

    def test_non_json_text_raises_error(self):
        """Plain text response should raise JSONDecodeError."""
        mock_client = MockLLMClient("This is just plain text, not JSON")
        with pytest.raises(json.JSONDecodeError):
            story_to_haiku("Test", llm_client=mock_client)


class TestMissingJSONKeys:
    """Test handling of missing required JSON keys."""

    def test_missing_lines_key(self):
        """Missing 'lines' key should raise KeyError."""
        mock_response = json.dumps({
            "syllables": [5, 7, 5],
            "essence": "Test"
        })
        mock_client = MockLLMClient(mock_response)
        with pytest.raises(KeyError, match="lines"):
            story_to_haiku("Test", llm_client=mock_client)

    def test_missing_syllables_key(self):
        """Missing 'syllables' key should raise KeyError."""
        mock_response = json.dumps({
            "lines": ["One", "Two", "Three"],
            "essence": "Test"
        })
        mock_client = MockLLMClient(mock_response)
        with pytest.raises(KeyError, match="syllables"):
            story_to_haiku("Test", llm_client=mock_client)

    def test_missing_essence_key(self):
        """Missing 'essence' key should raise KeyError."""
        mock_response = json.dumps({
            "lines": ["One", "Two", "Three"],
            "syllables": [5, 7, 5]
        })
        mock_client = MockLLMClient(mock_response)
        with pytest.raises(KeyError, match="essence"):
            story_to_haiku("Test", llm_client=mock_client)

    def test_missing_all_keys(self):
        """Missing all keys should raise KeyError."""
        mock_response = json.dumps({})
        mock_client = MockLLMClient(mock_response)
        with pytest.raises(KeyError):
            story_to_haiku("Test", llm_client=mock_client)


class TestInvalidJSONStructure:
    """Test handling of incorrect JSON types and structures."""

    def test_lines_not_list(self):
        """'lines' must be a list."""
        mock_response = json.dumps({
            "lines": "not a list",
            "syllables": [5, 7, 5],
            "essence": "Test"
        })
        mock_client = MockLLMClient(mock_response)
        with pytest.raises(TypeError, match="lines.*must be a list"):
            story_to_haiku("Test", llm_client=mock_client)

    def test_lines_wrong_length(self):
        """'lines' must contain exactly 3 elements."""
        mock_response = json.dumps({
            "lines": ["One", "Two"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        })
        mock_client = MockLLMClient(mock_response)
        with pytest.raises(ValueError, match="exactly 3 elements"):
            story_to_haiku("Test", llm_client=mock_client)

    def test_lines_contain_non_strings(self):
        """All elements in 'lines' must be strings."""
        mock_response = json.dumps({
            "lines": ["One", 2, "Three"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        })
        mock_client = MockLLMClient(mock_response)
        with pytest.raises(TypeError, match="must be strings"):
            story_to_haiku("Test", llm_client=mock_client)

    def test_syllables_not_list(self):
        """'syllables' must be a list."""
        mock_response = json.dumps({
            "lines": ["One", "Two", "Three"],
            "syllables": "not a list",
            "essence": "Test"
        })
        mock_client = MockLLMClient(mock_response)
        with pytest.raises(TypeError, match="syllables.*must be a list"):
            story_to_haiku("Test", llm_client=mock_client)

    def test_syllables_wrong_length(self):
        """'syllables' must contain exactly 3 elements."""
        mock_response = json.dumps({
            "lines": ["One", "Two", "Three"],
            "syllables": [5, 7],
            "essence": "Test"
        })
        mock_client = MockLLMClient(mock_response)
        with pytest.raises(ValueError, match="exactly 3 elements"):
            story_to_haiku("Test", llm_client=mock_client)

    def test_syllables_contain_non_integers(self):
        """All elements in 'syllables' must be integers."""
        mock_response = json.dumps({
            "lines": ["One", "Two", "Three"],
            "syllables": [5, "seven", 5],
            "essence": "Test"
        })
        mock_client = MockLLMClient(mock_response)
        with pytest.raises(TypeError, match="must be integers"):
            story_to_haiku("Test", llm_client=mock_client)

    def test_essence_not_string(self):
        """'essence' must be a string."""
        mock_response = json.dumps({
            "lines": ["One", "Two", "Three"],
            "syllables": [5, 7, 5],
            "essence": 123
        })
        mock_client = MockLLMClient(mock_response)
        with pytest.raises(TypeError, match="essence.*must be a string"):
            story_to_haiku("Test", llm_client=mock_client)

    def test_essence_empty_string(self):
        """'essence' cannot be empty or whitespace."""
        mock_response = json.dumps({
            "lines": ["One", "Two", "Three"],
            "syllables": [5, 7, 5],
            "essence": "   "
        })
        mock_client = MockLLMClient(mock_response)
        with pytest.raises(ValueError, match="essence.*cannot be empty"):
            story_to_haiku("Test", llm_client=mock_client)


class TestLLMFailure:
    """Test handling of LLM invocation failures."""

    def test_llm_exception_raises_runtime_error(self):
        """LLM failure should raise RuntimeError."""
        mock_client = MockLLMClientError()
        with pytest.raises(RuntimeError, match="LLM invocation failed"):
            story_to_haiku("Test", llm_client=mock_client)


class TestDependencyInjection:
    """Test dependency injection for testability."""

    def test_accepts_custom_llm_client(self):
        """Should accept and use custom LLM client."""
        mock_response = json.dumps({
            "lines": ["Custom", "Client", "Test"],
            "syllables": [5, 7, 5],
            "essence": "Dependency injection works"
        })
        mock_client = MockLLMClient(mock_response)
        result = story_to_haiku("Test", llm_client=mock_client)

        assert result is not None
        assert result['essence'] == "Dependency injection works"

    def test_none_client_uses_default(self):
        """None llm_client should use default ollama client."""
        # This test would require actual Ollama running, so we skip it in unit tests
        # It's tested in integration tests instead
        pass


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_long_input_text(self):
        """Should handle very long input text."""
        long_text = "word " * 1000  # 1000 words
        mock_response = json.dumps({
            "lines": ["Long", "Text", "Test"],
            "syllables": [5, 7, 5],
            "essence": "Handles long input"
        })
        mock_client = MockLLMClient(mock_response)
        result = story_to_haiku(long_text, llm_client=mock_client)

        assert result is not None

    def test_special_characters_in_text(self):
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

    def test_unicode_characters(self):
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

    def test_newlines_in_input(self):
        """Should handle input with newlines."""
        multiline_text = "Line one\nLine two\nLine three"
        mock_response = json.dumps({
            "lines": ["Multi", "Line", "Input"],
            "syllables": [5, 7, 5],
            "essence": "Newlines handled"
        })
        mock_client = MockLLMClient(mock_response)
        result = story_to_haiku(multiline_text, llm_client=mock_client)

        assert result is not None


class TestResponseFormat:
    """Test the exact format of returned responses."""

    def test_response_is_dict(self):
        """Response must be a dictionary."""
        mock_response = json.dumps({
            "lines": ["Test", "Response", "Format"],
            "syllables": [5, 7, 5],
            "essence": "Type check"
        })
        mock_client = MockLLMClient(mock_response)
        result = story_to_haiku("Test", llm_client=mock_client)

        assert isinstance(result, dict)

    def test_haiku_is_string(self):
        """'haiku' field must be a string."""
        mock_response = json.dumps({
            "lines": ["Test", "Type", "Check"],
            "syllables": [5, 7, 5],
            "essence": "Type verification"
        })
        mock_client = MockLLMClient(mock_response)
        result = story_to_haiku("Test", llm_client=mock_client)

        assert isinstance(result['haiku'], str)

    def test_lines_is_list(self):
        """'lines' field must be a list."""
        mock_response = json.dumps({
            "lines": ["Test", "Type", "Check"],
            "syllables": [5, 7, 5],
            "essence": "Type verification"
        })
        mock_client = MockLLMClient(mock_response)
        result = story_to_haiku("Test", llm_client=mock_client)

        assert isinstance(result['lines'], list)

    def test_syllables_is_list(self):
        """'syllables' field must be a list."""
        mock_response = json.dumps({
            "lines": ["Test", "Type", "Check"],
            "syllables": [5, 7, 5],
            "essence": "Type verification"
        })
        mock_client = MockLLMClient(mock_response)
        result = story_to_haiku("Test", llm_client=mock_client)

        assert isinstance(result['syllables'], list)

    def test_essence_is_string(self):
        """'essence' field must be a string."""
        mock_response = json.dumps({
            "lines": ["Test", "Type", "Check"],
            "syllables": [5, 7, 5],
            "essence": "Type verification"
        })
        mock_client = MockLLMClient(mock_response)
        result = story_to_haiku("Test", llm_client=mock_client)

        assert isinstance(result['essence'], str)

    def test_valid_is_bool(self):
        """'valid' field must be a boolean."""
        mock_response = json.dumps({
            "lines": ["Test", "Type", "Check"],
            "syllables": [5, 7, 5],
            "essence": "Type verification"
        })
        mock_client = MockLLMClient(mock_response)
        result = story_to_haiku("Test", llm_client=mock_client)

        assert isinstance(result['valid'], bool)


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
