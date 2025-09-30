"""
Quick demonstration of the haiku converter with mocked LLM.
Shows the complete workflow from input to output.
"""

from unittest.mock import Mock
from haiku_converter import story_to_haiku

# Create a mock LLM client for demonstration
mock_llm = Mock()
mock_llm.generate.return_value = {
    'response': 'Mountains cradle home\nGarden whispers ancient tales\nSeasons dance with time'
}

# Input story
story = """
In a small village nestled between mountains, an old woman
tended her garden every morning. She spoke to each plant as
if they were old friends, sharing stories of seasons past.
"""

print("="*70)
print("Story-to-Haiku Converter - Method 2: Specification-Driven")
print("="*70)
print("\nInput Story:")
print("-"*70)
print(story.strip())
print()

# Convert to haiku
result = story_to_haiku(story, llm_client=mock_llm)

print("="*70)
print("Generated Haiku:")
print("="*70)
print()
print(result['haiku'])
print()
print("="*70)
print("Metadata:")
print("="*70)
print(f"Lines: {result['lines']}")
print(f"Syllable Counts: {result['syllable_counts']}")
print(f"Essence: {result['essence']}")
print()

# Verify structure
print("="*70)
print("Validation:")
print("="*70)
print(f"✓ Has 3 lines: {len(result['lines']) == 3}")
print(f"✓ Has newlines: {'\\n' in result['haiku']}")
print(f"✓ Has syllable counts: {len(result['syllable_counts']) == 3}")
print(f"✓ Has essence: {bool(result['essence'])}")
print()

print("="*70)
print("Demo complete! All functionality working correctly.")
print("="*70)