"""
Comprehensive tests for limerick converter using Adaptive TDD.
Test quality is validated for complex logic.
"""

import pytest
import json
from limerick_converter import (
    LimerickConverter,
    validate_story_input,
    count_syllables,
    validate_limerick_structure,
    extract_rhyme_sounds,
    check_rhyme_scheme
)


class TestStoryInputValidation:
    """Test story input validation - simple logic, standard TDD."""

    def test_empty_string_raises_error(self):
        """Empty strings should be rejected."""
        with pytest.raises(ValueError, match="Story cannot be empty"):
            validate_story_input("")

    def test_whitespace_only_raises_error(self):
        """Whitespace-only strings should be rejected."""
        with pytest.raises(ValueError, match="Story cannot be empty"):
            validate_story_input("   \n\t  ")

    def test_too_short_story_raises_error(self):
        """Stories under 10 characters should be rejected."""
        with pytest.raises(ValueError, match="Story too short"):
            validate_story_input("Hi there")

    def test_valid_story_returns_cleaned_text(self):
        """Valid stories should return cleaned text."""
        story = "  Once upon a time, there was a programmer.  "
        result = validate_story_input(story)
        assert result == "Once upon a time, there was a programmer."
        assert result == result.strip()

    def test_multiline_story_preserved(self):
        """Multiline stories should preserve structure."""
        story = "Line one.\nLine two.\nLine three."
        result = validate_story_input(story)
        assert "Line one" in result
        assert "Line two" in result
        assert "Line three" in result


class TestSyllableCounting:
    """
    Test syllable counting - COMPLEX LOGIC requiring ADAPTIVE VALIDATION.
    This is critical for limerick structure validation.
    """

    def test_single_syllable_words(self):
        """Single syllable words should return 1."""
        assert count_syllables("cat") == 1
        assert count_syllables("dog") == 1
        assert count_syllables("sun") == 1
        assert count_syllables("moon") == 1

    def test_two_syllable_words(self):
        """Two syllable words should return 2."""
        assert count_syllables("happy") == 2
        assert count_syllables("table") == 2
        assert count_syllables("person") == 2
        assert count_syllables("coding") == 2

    def test_three_syllable_words(self):
        """Three syllable words should return 3."""
        assert count_syllables("beautiful") == 3
        assert count_syllables("computer") == 3
        assert count_syllables("amazing") == 3

    def test_silent_e_handling(self):
        """Silent 'e' should not count as syllable."""
        assert count_syllables("code") == 1
        assert count_syllables("time") == 1
        assert count_syllables("life") == 1

    def test_consecutive_vowels_count_as_one(self):
        """Consecutive vowels should count as one syllable."""
        assert count_syllables("beat") == 1
        assert count_syllables("team") == 1

    def test_empty_string_returns_zero(self):
        """Empty strings should return 0 syllables."""
        assert count_syllables("") == 0

    def test_phrase_syllable_count(self):
        """Phrases should count total syllables."""
        # "A cat sat on a mat" = 1+1+1+1+1+1 = 6
        assert count_syllables("A cat sat on a mat") == 6
        # "The programmer stayed up at night" = 1+3+1+1+1+1 = 8
        assert count_syllables("The programmer stayed up at night") == 8

    def test_punctuation_ignored(self):
        """Punctuation should be ignored in counting."""
        assert count_syllables("Don't") == 1
        assert count_syllables("it's") == 1
        assert count_syllables("Hello, world!") == 3


class TestRhymeDetection:
    """
    Test rhyme detection - COMPLEX LOGIC requiring ADAPTIVE VALIDATION.
    Critical for AABBA scheme validation.
    """

    def test_extract_rhyme_sound_basic(self):
        """Extract rhyme sound from simple words."""
        assert extract_rhyme_sounds("cat") == "at"
        assert extract_rhyme_sounds("dog") == "og"
        assert extract_rhyme_sounds("night") == "ight"

    def test_extract_rhyme_sound_from_line(self):
        """Extract rhyme sound from last word of line."""
        line = "The programmer stayed up at night"
        assert extract_rhyme_sounds(line) == "ight"

        line2 = "Debugging was quite the fight"
        assert extract_rhyme_sounds(line2) == "ight"

    def test_rhyme_matching_basic(self):
        """Basic rhyme matching should work."""
        assert check_rhyme_scheme("cat", "bat") == True
        assert check_rhyme_scheme("night", "fight") == True
        assert check_rhyme_scheme("cat", "dog") == False

    def test_rhyme_matching_from_lines(self):
        """Rhyme matching from full lines."""
        line1 = "A programmer stayed up at night"
        line2 = "Debugging code was their fight"
        assert check_rhyme_scheme(line1, line2) == True

        line3 = "They found a missing mark"
        assert check_rhyme_scheme(line1, line3) == False

    def test_case_insensitive_rhyming(self):
        """Rhyme detection should be case insensitive."""
        assert check_rhyme_scheme("NIGHT", "fight") == True
        assert check_rhyme_scheme("Night", "FIGHT") == True


class TestLimerickStructureValidation:
    """
    Test limerick structure validation - COMPLEX LOGIC requiring ADAPTIVE VALIDATION.
    This is the core business logic that must be rigorously tested.
    """

    def test_correct_line_count_required(self):
        """Limerick must have exactly 5 lines."""
        # Too few lines
        lines = ["Line 1", "Line 2", "Line 3"]
        result = validate_limerick_structure(lines)
        assert result["valid"] == False
        assert "5 lines" in result["errors"][0]

        # Too many lines
        lines = ["L1", "L2", "L3", "L4", "L5", "L6"]
        result = validate_limerick_structure(lines)
        assert result["valid"] == False

    def test_valid_limerick_structure(self):
        """Valid limerick should pass all checks."""
        lines = [
            "A programmer stayed up at night",  # 9 syllables, A
            "Debugging code was their fight",    # 8 syllables, A
            "Found one missing mark",            # 5 syllables, B
            "A semicolon stark",                 # 6 syllables, B
            "Then slept with relief and delight" # 9 syllables, A
        ]
        result = validate_limerick_structure(lines)
        assert result["valid"] == True
        assert len(result["errors"]) == 0
        assert result["syllable_counts"] == [9, 8, 5, 6, 9]

    def test_syllable_count_validation_lines_1_2_5(self):
        """Lines 1, 2, 5 should have 8-9 syllables."""
        lines = [
            "A cat",  # Too few syllables (2)
            "Debugging code was their fight",
            "Found one missing mark",
            "A semicolon stark",
            "Then slept with relief and delight"
        ]
        result = validate_limerick_structure(lines)
        assert result["valid"] == False
        assert any("Line 1" in err and "syllable" in err.lower() for err in result["errors"])

    def test_syllable_count_validation_lines_3_4(self):
        """Lines 3, 4 should have 5-6 syllables."""
        lines = [
            "A programmer stayed up at night",
            "Debugging code was their fight",
            "Found",  # Too few syllables (1)
            "A semicolon stark",
            "Then slept with relief and delight"
        ]
        result = validate_limerick_structure(lines)
        assert result["valid"] == False
        assert any("Line 3" in err and "syllable" in err.lower() for err in result["errors"])

    def test_rhyme_scheme_aabba_validation(self):
        """AABBA rhyme scheme must be validated."""
        lines = [
            "A programmer stayed up at night",
            "Debugging code was their fight",
            "Found one missing mark",
            "A semicolon stark",
            "Then slept with relief and delight"
        ]
        result = validate_limerick_structure(lines)
        assert result["valid"] == True

        # Break the rhyme scheme
        lines_bad = [
            "A programmer stayed up at night",
            "Debugging code was their day",  # Doesn't rhyme with night
            "Found one missing mark",
            "A semicolon stark",
            "Then slept with relief and delight"
        ]
        result_bad = validate_limerick_structure(lines_bad)
        assert result_bad["valid"] == False
        assert any("rhyme" in err.lower() for err in result_bad["errors"])


class TestLimerickConverter:
    """Test the main LimerickConverter class."""

    def test_converter_initialization(self):
        """Converter should initialize with default model."""
        converter = LimerickConverter()
        assert converter.model_name == "llama3.2"
        assert converter.ollama_url == "http://localhost:11434"

    def test_converter_custom_model(self):
        """Converter should accept custom model name."""
        converter = LimerickConverter(model_name="llama3.1")
        assert converter.model_name == "llama3.1"

    def test_build_prompt_includes_story(self):
        """Prompt should include the story."""
        converter = LimerickConverter()
        story = "A programmer debugged code all night long."
        prompt = converter._build_prompt(story)
        assert story in prompt
        assert "limerick" in prompt.lower()
        assert "AABBA" in prompt

    def test_build_prompt_includes_rules(self):
        """Prompt should include limerick rules."""
        converter = LimerickConverter()
        prompt = converter._build_prompt("Test story")
        assert "5 lines" in prompt or "5-line" in prompt
        assert "syllable" in prompt.lower()
        assert "rhyme" in prompt.lower()

    def test_parse_response_extracts_lines(self):
        """Parse response should extract 5 lines."""
        converter = LimerickConverter()
        response = """Line 1 here
Line 2 here
Line 3 here
Line 4 here
Line 5 here"""
        lines = converter._parse_response(response)
        assert len(lines) == 5
        assert lines[0] == "Line 1 here"

    def test_parse_response_handles_extra_text(self):
        """Parser should handle extra text before/after limerick."""
        converter = LimerickConverter()
        response = """Here's your limerick:

Line 1 here
Line 2 here
Line 3 here
Line 4 here
Line 5 here

Hope you like it!"""
        lines = converter._parse_response(response)
        assert len(lines) == 5

    def test_format_output_json_structure(self):
        """Output should be valid JSON with required fields."""
        converter = LimerickConverter()
        lines = [
            "A programmer stayed up at night",
            "Debugging code was their fight",
            "Found one missing mark",
            "A semicolon stark",
            "Then slept with relief and delight"
        ]
        story = "A programmer debugged all night."

        output = converter._format_output(lines, story)
        parsed = json.loads(output)

        assert "limerick" in parsed
        assert "lines" in parsed["limerick"]
        assert "text" in parsed["limerick"]
        assert "story" in parsed
        assert "validation" in parsed
        assert len(parsed["limerick"]["lines"]) == 5

    def test_format_output_includes_validation(self):
        """Output should include validation results."""
        converter = LimerickConverter()
        lines = [
            "A programmer stayed up at night",
            "Debugging code was their fight",
            "Found one missing mark",
            "A semicolon stark",
            "Then slept with relief and delight"
        ]

        output = converter._format_output(lines, "Test story")
        parsed = json.loads(output)

        assert "valid" in parsed["validation"]
        assert "syllable_counts" in parsed["validation"]
        assert parsed["validation"]["valid"] == True
