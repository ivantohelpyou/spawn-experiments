#!/usr/bin/env python3
"""
Quick demo of the haiku converter (for manual testing).
"""

from haiku_converter import story_to_haiku

# Test with mock
from unittest.mock import Mock

def demo_with_mock():
    """Demonstrate with mock client"""
    print("=== Demo with Mock Client ===\n")

    mock_client = Mock()
    mock_client.chat.return_value = {
        'message': {
            'content': '{"lines": ["Autumn leaves falling", "Gently dancing in the wind", "Nature\'s art displayed"], "syllables": [5, 7, 5], "essence": "The beauty of autumn"}'
        }
    }

    result = story_to_haiku(
        "The autumn leaves fell from the trees, dancing in the gentle wind.",
        llm_client=mock_client
    )

    print(f"Valid: {result['valid']}")
    print(f"Syllables: {result['syllables']}")
    print(f"Essence: {result['essence']}")
    print(f"\nHaiku:\n{result['haiku']}")
    print()

def demo_error_handling():
    """Demonstrate error handling"""
    print("=== Demo Error Handling ===\n")

    mock_client = Mock()
    mock_client.chat.return_value = {
        'message': {'content': 'This is not valid JSON!'}
    }

    result = story_to_haiku("Test story", llm_client=mock_client)

    print(f"Valid: {result['valid']}")
    print(f"Error: {result.get('error', 'No error')}")
    print()

if __name__ == '__main__':
    demo_with_mock()
    demo_error_handling()
    print("Note: To test with real Ollama, run without llm_client parameter")
    print("      (requires ollama package and running Ollama service)")
