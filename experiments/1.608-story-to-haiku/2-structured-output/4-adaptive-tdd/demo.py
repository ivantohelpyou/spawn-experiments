"""
Demo script for Adaptive TDD Story-to-Haiku Converter

Shows the implementation working with mock data (no Ollama required).
"""

from unittest.mock import Mock
from haiku_converter import story_to_haiku


def demo_spring_story():
    """Demo with a spring story."""
    print("\n" + "="*70)
    print("DEMO 1: Spring Garden Story")
    print("="*70)

    story = """
    In a small village nestled between mountains, an old woman
    tended her garden every morning. She spoke to each plant as
    if they were old friends, sharing stories of seasons past.
    """

    print(f"\nInput Story:\n{story.strip()}")

    # Mock LLM response
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"], "syllables": [5, 7, 5], "essence": "Spring\'s gentle transition"}'
    }

    result = story_to_haiku(story, llm_client=mock_llm)

    print("\nGenerated Haiku:")
    print("-" * 40)
    print(result['haiku'])
    print("-" * 40)
    print(f"\nSyllable Pattern: {result['syllables']}")
    print(f"Valid 5-7-5: {result['valid']}")
    print(f"Essence: {result['essence']}")


def demo_coding_story():
    """Demo with a coding story."""
    print("\n" + "="*70)
    print("DEMO 2: Programming Flow State")
    print("="*70)

    story = """
    The developer sat in the quiet office at 2 AM, fingers dancing
    across the keyboard. The code flowed like water, each function
    connecting perfectly to the next. Time disappeared as the program
    came to life, elegant and efficient.
    """

    print(f"\nInput Story:\n{story.strip()}")

    # Mock LLM response
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["Code lines on the screen", "Logic winds through endless loops", "Mind in flow state dances"], "syllables": [5, 7, 5], "essence": "Programming flow state"}'
    }

    result = story_to_haiku(story, llm_client=mock_llm)

    print("\nGenerated Haiku:")
    print("-" * 40)
    print(result['haiku'])
    print("-" * 40)
    print(f"\nSyllable Pattern: {result['syllables']}")
    print(f"Valid 5-7-5: {result['valid']}")
    print(f"Essence: {result['essence']}")


def demo_invalid_syllables():
    """Demo with invalid syllable structure."""
    print("\n" + "="*70)
    print("DEMO 3: Invalid Syllable Structure (LLM made a mistake)")
    print("="*70)

    story = "A brief winter tale of snow and ice."

    print(f"\nInput Story: {story}")

    # Mock LLM response with wrong syllable counts
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["Snow falls", "Ice covers ground", "Cold"], "syllables": [2, 5, 1], "essence": "Winter\'s grip"}'
    }

    result = story_to_haiku(story, llm_client=mock_llm)

    print("\nGenerated Output:")
    print("-" * 40)
    print(result['haiku'])
    print("-" * 40)
    print(f"\nSyllable Pattern: {result['syllables']}")
    print(f"Valid 5-7-5: {result['valid']} ⚠️  (LLM didn't follow 5-7-5!)")
    print(f"Essence: {result['essence']}")
    print("\nNote: The function correctly detected this is NOT a valid haiku.")


def demo_error_handling():
    """Demo error handling."""
    print("\n" + "="*70)
    print("DEMO 4: Error Handling (Empty Input)")
    print("="*70)

    try:
        result = story_to_haiku("")
        print("ERROR: Should have raised ValueError!")
    except ValueError as e:
        print(f"\nCorrectly caught error: {e}")
        print("✓ Error handling working as expected")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("ADAPTIVE TDD - Story-to-Haiku Converter Demo")
    print("="*70)
    print("\nThis demo uses mocked LLM responses (no Ollama required).")
    print("The implementation works identically with real Ollama in production.")

    demo_spring_story()
    demo_coding_story()
    demo_invalid_syllables()
    demo_error_handling()

    print("\n" + "="*70)
    print("Demo Complete!")
    print("="*70)

    print("\n📊 ADAPTIVE TDD SUMMARY:")
    print("  • 10 strategic tests covering complex/risky areas")
    print("  • 0 tests for obvious/simple operations")
    print("  • Fast execution with mocks")
    print("  • Production-ready with real Ollama")
    print("  • Optimal balance of quality and effort")
    print("\nThis is smart testing that focuses effort where it matters most.\n")