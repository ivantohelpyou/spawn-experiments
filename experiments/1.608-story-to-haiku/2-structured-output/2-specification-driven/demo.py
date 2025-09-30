"""
Quick demonstration of the Story-to-Haiku converter
Method 2: Specification-Driven Implementation
"""

from unittest.mock import Mock
from haiku_converter import story_to_haiku


def demo_with_mock():
    """Demonstrate the converter with a mock LLM (for quick testing)."""
    print("=" * 60)
    print("Story-to-Haiku Converter - Method 2: Specification-Driven")
    print("=" * 60)
    print()

    # Create mock LLM
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["Mountains cradle home", "Garden whispers ancient tales", "Seasons dance with time"], '
                   '"syllables": [5, 7, 5], "essence": "Timeless connection with nature"}'
    }

    # Input story
    story = """
    In a small village nestled between mountains, an old woman
    tended her garden every morning. She spoke to each plant as
    if they were old friends, sharing stories of seasons past.
    """

    print("Input Story:")
    print(story.strip())
    print()

    # Convert to haiku
    result = story_to_haiku(story, llm_client=mock_llm)

    # Display results
    print("Generated Haiku:")
    print("-" * 40)
    print(result['haiku'])
    print("-" * 40)
    print()

    print("Metadata:")
    print(f"  Syllables: {result['syllables']}")
    print(f"  Valid 5-7-5: {result['valid']}")
    print(f"  Essence: {result['essence']}")
    print()

    print("Individual Lines:")
    for i, line in enumerate(result['lines'], 1):
        syllables = result['syllables'][i-1]
        print(f"  Line {i}: \"{line}\" ({syllables} syllables)")
    print()

    print("=" * 60)
    print("✓ Demonstration complete!")
    print()
    print("Note: This demo uses a mock LLM for instant results.")
    print("For real haiku generation, use without llm_client parameter.")
    print("=" * 60)


if __name__ == '__main__':
    demo_with_mock()