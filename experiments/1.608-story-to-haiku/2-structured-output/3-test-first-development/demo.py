#!/usr/bin/env python3
"""
Demo script for Method 3: Test-First Development (TDD)
Demonstrates the haiku converter with real Ollama integration.
"""

from haiku_converter import story_to_haiku
import json


def main():
    print("=" * 70)
    print("Method 3: Test-First Development (TDD)")
    print("Story-to-Haiku Converter with Structured JSON Output")
    print("=" * 70)
    print()

    # Test story
    story = """
    In a small village nestled between mountains, an old woman
    tended her garden every morning. She spoke to each plant as
    if they were old friends, sharing stories of seasons past.
    """

    print("Input Story:")
    print("-" * 70)
    print(story.strip())
    print()

    print("Generating haiku with Ollama (llama3.2)...")
    print()

    try:
        result = story_to_haiku(story)

        print("=" * 70)
        print("HAIKU OUTPUT")
        print("=" * 70)
        print()
        print(result['haiku'])
        print()
        print("-" * 70)
        print(f"Syllables: {result['syllables']}")
        print(f"Valid 5-7-5: {result['valid']}")
        print(f"Essence: {result['essence']}")
        print("-" * 70)
        print()

        # Show full JSON structure
        print("Full JSON Structure:")
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {e}")
        print()
        print("Note: Make sure Ollama is running and llama3.2 model is available.")
        print("Install with: ollama pull llama3.2")


if __name__ == "__main__":
    main()