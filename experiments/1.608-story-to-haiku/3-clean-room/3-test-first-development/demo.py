"""
Demo script showing story_to_haiku function with mock.
"""

from unittest.mock import Mock
import json
from haiku_converter import story_to_haiku


def demo_with_mock():
    """Demonstrate function with mock LLM client."""

    print("=== Story to Haiku Demo (with Mock) ===\n")

    # Create mock client
    mock_client = Mock()
    mock_response = {
        "lines": [
            "Cherry blossoms fall",
            "Softly on the quiet pond",
            "Spring whispers arrive"
        ],
        "syllables": [5, 7, 5],
        "essence": "Spring's gentle transition"
    }

    mock_client.chat = Mock(return_value={
        'message': {'content': json.dumps(mock_response)}
    })

    # Test story
    story = "A beautiful spring day when cherry blossoms fall gently on the quiet pond."

    print(f"Input Story: {story}\n")

    # Convert to haiku
    result = story_to_haiku(story, mock_client)

    print(f"Haiku:\n{result['haiku']}\n")
    print(f"Syllables: {result['syllables']}")
    print(f"Valid: {result['valid']}")
    print(f"Essence: {result['essence']}")
    print(f"\n--- All tests passed! ---")


if __name__ == '__main__':
    demo_with_mock()
