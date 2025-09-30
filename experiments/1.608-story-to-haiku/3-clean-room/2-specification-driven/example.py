"""
Example usage of the story_to_haiku converter.
Demonstrates both mock-based testing and real LLM usage.
"""

import json
from haiku_converter import story_to_haiku


# Mock LLM Client for demonstration
class MockLLMClient:
    """Mock LLM client that returns predefined JSON responses."""

    def __init__(self, response_json: str):
        self.response_json = response_json

    def chat(self, model: str, messages: list, format: str):
        class MockResponse:
            def __init__(self, content):
                self.message = {'content': content}
        return MockResponse(self.response_json)


def example_with_mock():
    """Example using a mock LLM client."""
    print("=" * 60)
    print("Example 1: Using Mock LLM Client (for testing)")
    print("=" * 60)

    # Create mock response
    mock_response = json.dumps({
        "lines": [
            "Cherry blossoms fall",
            "Softly on the quiet pond",
            "Spring whispers arrive"
        ],
        "syllables": [5, 7, 5],
        "essence": "Spring's gentle transition"
    })

    # Create mock client
    mock_client = MockLLMClient(mock_response)

    # Convert story to haiku
    text = "In a quiet garden, cherry blossoms drift down like snow."
    result = story_to_haiku(text, llm_client=mock_client)

    # Display results
    print(f"\nInput Text: {text}")
    print(f"\nGenerated Haiku:")
    print(result['haiku'])
    print(f"\nSyllables: {result['syllables']}")
    print(f"Valid 5-7-5: {result['valid']}")
    print(f"Essence: {result['essence']}")
    print(f"\nAll Fields: {list(result.keys())}")


def example_invalid_syllables():
    """Example with invalid syllable pattern."""
    print("\n" + "=" * 60)
    print("Example 2: Invalid Syllable Pattern (still works)")
    print("=" * 60)

    # Create mock with invalid pattern
    mock_response = json.dumps({
        "lines": [
            "Four syllables",
            "Eight syllables in this line",
            "Five syllables"
        ],
        "syllables": [4, 8, 5],
        "essence": "Testing invalid pattern"
    })

    mock_client = MockLLMClient(mock_response)
    result = story_to_haiku("Test text", llm_client=mock_client)

    print(f"\nGenerated Haiku:")
    print(result['haiku'])
    print(f"\nSyllables: {result['syllables']}")
    print(f"Valid 5-7-5: {result['valid']} ⚠️")
    print(f"Note: Function still returns result even with invalid pattern")


def example_error_handling():
    """Example demonstrating error handling."""
    print("\n" + "=" * 60)
    print("Example 3: Error Handling")
    print("=" * 60)

    # Test 1: Empty input
    print("\n[Test 1] Empty Input:")
    try:
        story_to_haiku("")
    except ValueError as e:
        print(f"✓ Caught ValueError: {e}")

    # Test 2: Whitespace only
    print("\n[Test 2] Whitespace Only:")
    try:
        story_to_haiku("   ")
    except ValueError as e:
        print(f"✓ Caught ValueError: {e}")

    # Test 3: Malformed JSON
    print("\n[Test 3] Malformed JSON:")
    mock_client = MockLLMClient("{invalid json")
    try:
        story_to_haiku("Test", llm_client=mock_client)
    except json.JSONDecodeError as e:
        print(f"✓ Caught JSONDecodeError: Invalid JSON")

    # Test 4: Missing required keys
    print("\n[Test 4] Missing Required Keys:")
    mock_client = MockLLMClient('{"lines": ["a", "b", "c"]}')
    try:
        story_to_haiku("Test", llm_client=mock_client)
    except KeyError as e:
        print(f"✓ Caught KeyError: {e}")


def example_with_real_ollama():
    """Example using real Ollama (if available)."""
    print("\n" + "=" * 60)
    print("Example 4: Real Ollama LLM (if available)")
    print("=" * 60)

    try:
        import ollama

        text = "The old pond, a frog jumps in, water's sound."
        print(f"\nInput Text: {text}")
        print("\nCalling Ollama llama3.2...")

        result = story_to_haiku(text)

        print(f"\nGenerated Haiku:")
        print(result['haiku'])
        print(f"\nSyllables: {result['syllables']}")
        print(f"Valid 5-7-5: {result['valid']}")
        print(f"Essence: {result['essence']}")

    except ImportError:
        print("\n⚠️ Ollama not installed. Install with: pip install ollama")
    except Exception as e:
        print(f"\n⚠️ Error calling Ollama: {e}")
        print("Make sure Ollama is running and llama3.2 model is available.")


if __name__ == "__main__":
    print("\nStory-to-Haiku Converter - Usage Examples")
    print("Method 2: Specification-Driven Implementation\n")

    # Run examples
    example_with_mock()
    example_invalid_syllables()
    example_error_handling()
    example_with_real_ollama()

    print("\n" + "=" * 60)
    print("Examples Complete!")
    print("=" * 60)
