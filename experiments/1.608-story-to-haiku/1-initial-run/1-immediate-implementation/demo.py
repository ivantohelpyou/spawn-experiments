"""Demo script for Story-to-Haiku Converter (Method 1)"""

from haiku_converter import story_to_haiku

TEST_STORIES = [
    """In a small village nestled between mountains, an old woman
    tended her garden every morning. She spoke to each plant as
    if they were old friends, sharing stories of seasons past.""",

    """A young programmer sat late at night, debugging code that refused to work.
    Line by line, she traced the logic, until suddenly the pattern emerged
    and everything clicked into place.""",

    """The ocean waves crashed against ancient cliffs, carved by millennia
    of relentless tides. Seabirds wheeled overhead, their cries echoing
    through the salt-spray air."""
]


def main():
    print("=" * 60)
    print("Story-to-Haiku Converter - Method 1 Demo")
    print("=" * 60)

    for i, story in enumerate(TEST_STORIES, 1):
        print(f"\n--- Story {i} ---")
        print(f"Input: {story[:60]}...")

        try:
            result = story_to_haiku(story)

            print("\nHaiku:")
            print(result['haiku'])
            print(f"\nSyllables: {result['syllable_counts']}")
            print(f"Essence: {result['essence']}")

        except Exception as e:
            print(f"\nError: {e}")
            print("Note: This requires Ollama to be running with llama3.2 model")

        print()


if __name__ == '__main__':
    main()