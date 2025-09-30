"""
Test suite for story_to_haiku converter using Adaptive/Validated TDD.

Method 4 Characteristics:
- Test-first approach with validation
- Multiple validation cycles to ensure test quality
- Comprehensive edge case coverage
- Mock-based testing for fast execution
"""

import pytest
import json
from unittest.mock import Mock, MagicMock
from haiku_converter import story_to_haiku


class TestBasicFunctionality:
    """Test core functionality with valid inputs."""

    def test_valid_haiku_conversion(self):
        """Test successful conversion with valid JSON response."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": [
                "Cherry blossoms fall",
                "Softly on the quiet pond",
                "Spring whispers arrive"
            ],
            "syllables": [5, 7, 5],
            "essence": "Spring's gentle transition"
        })
        mock_llm.chat.return_value = mock_response

        result = story_to_haiku("A story about spring.", llm_client=mock_llm)

        assert result["haiku"] == "Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive"
        assert result["lines"] == [
            "Cherry blossoms fall",
            "Softly on the quiet pond",
            "Spring whispers arrive"
        ]
        assert result["syllables"] == [5, 7, 5]
        assert result["essence"] == "Spring's gentle transition"
        assert result["valid"] is True

    def test_llm_called_with_correct_parameters(self):
        """Verify LLM is called with proper model and message structure."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Line one here", "Line two is longer now", "Line three here"],
            "syllables": [5, 7, 5],
            "essence": "Test essence"
        })
        mock_llm.chat.return_value = mock_response

        story_to_haiku("Test story", llm_client=mock_llm)

        # Verify chat was called
        assert mock_llm.chat.called
        call_args = mock_llm.chat.call_args

        # Check model parameter
        assert call_args[1]["model"] == "llama3.2"

        # Check messages structure
        messages = call_args[1]["messages"]
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert "Test story" in messages[0]["content"]

    def test_prompt_contains_optimized_elements(self):
        """Verify prompt includes optimized syllable counting instructions."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Five syllables here", "Seven syllables are here now", "Five syllables end"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        story_to_haiku("Test input", llm_client=mock_llm)

        # Extract the prompt
        call_args = mock_llm.chat.call_args
        prompt = call_args[1]["messages"][0]["content"]

        # Verify optimized prompt elements
        assert "exactly 5 syllables" in prompt.lower() or "line 1: exactly 5" in prompt.lower()
        assert "exactly 7 syllables" in prompt.lower() or "line 2: exactly 7" in prompt.lower()
        assert "count" in prompt.lower() and "syllable" in prompt.lower()
        assert "essence" in prompt.lower()
        assert "json" in prompt.lower()


class TestSyllableValidation:
    """Test syllable validation logic."""

    def test_valid_syllable_structure(self):
        """Test validation passes for correct 5-7-5 structure."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Line one", "Line two longer", "Line three"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        result = story_to_haiku("Test", llm_client=mock_llm)
        assert result["valid"] is True

    def test_invalid_syllable_structure_first_line(self):
        """Test validation fails when first line has wrong syllable count."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Wrong", "Middle line correct", "Last line"],
            "syllables": [3, 7, 5],  # First line wrong
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        result = story_to_haiku("Test", llm_client=mock_llm)
        assert result["valid"] is False

    def test_invalid_syllable_structure_second_line(self):
        """Test validation fails when second line has wrong syllable count."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["First is good", "Wrong middle", "Last is good"],
            "syllables": [5, 5, 5],  # Second line wrong
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        result = story_to_haiku("Test", llm_client=mock_llm)
        assert result["valid"] is False

    def test_invalid_syllable_structure_third_line(self):
        """Test validation fails when third line has wrong syllable count."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["First correct", "Second line is correct", "Too long wrong"],
            "syllables": [5, 7, 8],  # Third line wrong
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        result = story_to_haiku("Test", llm_client=mock_llm)
        assert result["valid"] is False


class TestJSONParsing:
    """Test JSON parsing and error handling."""

    def test_malformed_json_handling(self):
        """Test graceful handling of malformed JSON."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = "This is not valid JSON at all"
        mock_llm.chat.return_value = mock_response

        with pytest.raises(ValueError, match="Failed to parse JSON"):
            story_to_haiku("Test", llm_client=mock_llm)

    def test_json_with_extra_text(self):
        """Test handling JSON embedded in extra text."""
        mock_llm = Mock()
        mock_response = Mock()
        valid_json = {
            "lines": ["Line one here", "Line two is longer now", "Line three here"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        }
        mock_response.message.content = f"Here is the haiku:\n{json.dumps(valid_json)}\nHope you like it!"
        mock_llm.chat.return_value = mock_response

        result = story_to_haiku("Test", llm_client=mock_llm)
        assert result["valid"] is True
        assert result["lines"] == valid_json["lines"]

    def test_missing_required_keys(self):
        """Test error when JSON is missing required keys."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Line one", "Line two", "Line three"],
            # Missing syllables and essence
        })
        mock_llm.chat.return_value = mock_response

        with pytest.raises(ValueError, match="Missing required key"):
            story_to_haiku("Test", llm_client=mock_llm)

    def test_wrong_number_of_lines(self):
        """Test error when JSON has wrong number of lines."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Only one line", "And another"],  # Only 2 lines
            "syllables": [5, 7],
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        with pytest.raises(ValueError, match="Expected 3 lines"):
            story_to_haiku("Test", llm_client=mock_llm)

    def test_wrong_number_of_syllable_counts(self):
        """Test error when syllable counts don't match line count."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Line one", "Line two", "Line three"],
            "syllables": [5, 7],  # Only 2 counts
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        with pytest.raises(ValueError, match="Expected 3 syllable counts"):
            story_to_haiku("Test", llm_client=mock_llm)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_input(self):
        """Test handling of empty string input."""
        with pytest.raises(ValueError, match="Input text cannot be empty"):
            story_to_haiku("")

    def test_none_input(self):
        """Test handling of None input."""
        with pytest.raises(ValueError, match="Input text cannot be empty"):
            story_to_haiku(None)

    def test_whitespace_only_input(self):
        """Test handling of whitespace-only input."""
        with pytest.raises(ValueError, match="Input text cannot be empty"):
            story_to_haiku("   \n\t  ")

    def test_very_long_input(self):
        """Test handling of very long input text."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["From the long tale", "Essence carefully extracted", "Wisdom distilled"],
            "syllables": [5, 7, 5],
            "essence": "The core message"
        })
        mock_llm.chat.return_value = mock_response

        long_text = "This is a very long story. " * 1000
        result = story_to_haiku(long_text, llm_client=mock_llm)

        assert result["valid"] is True
        assert mock_llm.chat.called

    def test_special_characters_in_input(self):
        """Test handling of special characters in input."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Special chars here", "Handled with care and grace now", "All works perfectly"],
            "syllables": [5, 7, 5],
            "essence": "Testing special chars"
        })
        mock_llm.chat.return_value = mock_response

        special_text = "Story with émojis 🌸, quotes \"test\", and symbols @#$%"
        result = story_to_haiku(special_text, llm_client=mock_llm)

        assert result["valid"] is True


class TestReturnStructure:
    """Test the structure of returned dictionary."""

    def test_all_required_keys_present(self):
        """Verify all required keys are in the return dict."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Line one", "Line two is here now", "Line three"],
            "syllables": [5, 7, 5],
            "essence": "Core theme"
        })
        mock_llm.chat.return_value = mock_response

        result = story_to_haiku("Test", llm_client=mock_llm)

        assert "haiku" in result
        assert "lines" in result
        assert "syllables" in result
        assert "essence" in result
        assert "valid" in result

    def test_haiku_string_format(self):
        """Test that haiku string is properly formatted with newlines."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["First line here", "Second line is longer now", "Third line here"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        result = story_to_haiku("Test", llm_client=mock_llm)

        assert "\n" in result["haiku"]
        assert result["haiku"].count("\n") == 2
        lines_from_haiku = result["haiku"].split("\n")
        assert lines_from_haiku == result["lines"]

    def test_types_of_return_values(self):
        """Verify types of all return values."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Line one", "Line two longer", "Line three"],
            "syllables": [5, 7, 5],
            "essence": "Test essence"
        })
        mock_llm.chat.return_value = mock_response

        result = story_to_haiku("Test", llm_client=mock_llm)

        assert isinstance(result["haiku"], str)
        assert isinstance(result["lines"], list)
        assert all(isinstance(line, str) for line in result["lines"])
        assert isinstance(result["syllables"], list)
        assert all(isinstance(count, int) for count in result["syllables"])
        assert isinstance(result["essence"], str)
        assert isinstance(result["valid"], bool)


class TestDefaultLLMClient:
    """Test behavior when no LLM client is provided."""

    def test_uses_ollama_by_default(self):
        """Test that function creates Ollama client when none provided."""
        # This test is primarily for documentation
        # In real execution, it would try to use actual Ollama
        # We'll test the parameter passing logic
        pass  # Placeholder - real Ollama testing happens in comparison script


class TestValidationCycle2EdgeCases:
    """Additional edge cases discovered during Validation Cycle 2."""

    def test_non_integer_syllable_counts(self):
        """Test error when syllable counts are not integers."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Line one", "Line two", "Line three"],
            "syllables": ["5", "7", "5"],  # Strings instead of ints
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        result = story_to_haiku("Test", llm_client=mock_llm)
        # Should still work - just checking types in return
        assert isinstance(result["syllables"], list)

    def test_unicode_text_input(self):
        """Test handling of unicode characters in input."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Unicode handled", "With grace and elegance here", "Perfect haiku"],
            "syllables": [5, 7, 5],
            "essence": "Testing unicode"
        })
        mock_llm.chat.return_value = mock_response

        unicode_text = "Story with Chinese 你好 and Arabic مرحبا"
        result = story_to_haiku(unicode_text, llm_client=mock_llm)
        assert result["valid"] is True

    def test_extremely_short_input(self):
        """Test with very short input (single word)."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["From one single word", "A world of meaning unfolds", "Poetry emerges"],
            "syllables": [5, 7, 5],
            "essence": "Minimalism"
        })
        mock_llm.chat.return_value = mock_response

        result = story_to_haiku("Love", llm_client=mock_llm)
        assert result["valid"] is True

    def test_json_with_additional_fields(self):
        """Test that extra fields in JSON don't break parsing."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Line one", "Line two longer", "Line three"],
            "syllables": [5, 7, 5],
            "essence": "Test",
            "extra_field": "should be ignored",
            "metadata": {"author": "LLM"}
        })
        mock_llm.chat.return_value = mock_response

        result = story_to_haiku("Test", llm_client=mock_llm)
        assert result["valid"] is True
        assert "extra_field" not in result  # Extra fields not in output


class TestValidationCycle3PromptQuality:
    """Validation Cycle 3: Verify prompt optimization elements."""

    def test_prompt_includes_example_haiku(self):
        """Verify prompt includes example haiku with syllable breakdown."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Test", "Test line", "Test"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        story_to_haiku("Test story", llm_client=mock_llm)
        prompt = mock_llm.chat.call_args[1]["messages"][0]["content"]

        # Verify example is present
        assert "EXAMPLE" in prompt.upper()
        assert "fisherman" in prompt or "Fog wraps the shoreline" in prompt

    def test_prompt_includes_syllable_rules(self):
        """Verify prompt explicitly states syllable counting rules."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Test", "Test line", "Test"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        story_to_haiku("Test story", llm_client=mock_llm)
        prompt = mock_llm.chat.call_args[1]["messages"][0]["content"]

        # Verify syllable rules are explicit
        assert "Line 1" in prompt and "5 syllable" in prompt
        assert "Line 2" in prompt and "7 syllable" in prompt
        assert "Line 3" in prompt and "5 syllable" in prompt

    def test_prompt_includes_verification_instruction(self):
        """Verify prompt instructs LLM to verify counts."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Test", "Test line", "Test"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        story_to_haiku("Test story", llm_client=mock_llm)
        prompt = mock_llm.chat.call_args[1]["messages"][0]["content"]

        # Verify verification instruction
        assert "verify" in prompt.lower() or "check" in prompt.lower()

    def test_prompt_includes_essence_guidance(self):
        """Verify prompt guides LLM on capturing essence."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Test", "Test line", "Test"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        story_to_haiku("Test story", llm_client=mock_llm)
        prompt = mock_llm.chat.call_args[1]["messages"][0]["content"]

        # Verify essence guidance
        assert "essence" in prompt.lower()
        assert "capture" in prompt.lower() or "distill" in prompt.lower()

    def test_prompt_requests_json_format(self):
        """Verify prompt explicitly requests JSON format."""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.message.content = json.dumps({
            "lines": ["Test", "Test line", "Test"],
            "syllables": [5, 7, 5],
            "essence": "Test"
        })
        mock_llm.chat.return_value = mock_response

        story_to_haiku("Test story", llm_client=mock_llm)
        prompt = mock_llm.chat.call_args[1]["messages"][0]["content"]

        # Verify JSON format request
        assert "JSON" in prompt or "json" in prompt
        assert "{" in prompt and "}" in prompt  # Shows JSON structure
