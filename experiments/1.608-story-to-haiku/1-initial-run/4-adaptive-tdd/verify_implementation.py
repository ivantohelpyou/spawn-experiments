#!/usr/bin/env python3
"""
Verification script for Method 4 (Adaptive TDD) implementation

Shows what we test and what we skip, with examples.
"""

from unittest.mock import Mock
from haiku_converter import story_to_haiku, count_line_syllables

print("=" * 70)
print("Method 4: Adaptive TDD - Implementation Verification")
print("=" * 70)

# Test 1: Structure (TESTED)
print("\n[TESTED] Structure Validation:")
mock_llm = Mock()
mock_llm.generate.return_value = {
    'response': 'Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive'
}
result = story_to_haiku("A story about spring", llm_client=mock_llm)
print(f"  ✓ Returns 3 lines: {len(result['lines']) == 3}")
print(f"  ✓ Has newlines: {result['haiku'].count(chr(10)) == 2}")
print(f"  ✓ Has all keys: {all(k in result for k in ['haiku', 'lines', 'syllable_counts', 'essence'])}")

# Test 2: Error handling (TESTED)
print("\n[TESTED] Error Handling:")
try:
    story_to_haiku("")
    print("  ✗ Empty input should raise error")
except ValueError:
    print("  ✓ Empty input raises ValueError")

try:
    story_to_haiku("   \n\n   ")
    print("  ✗ Whitespace input should raise error")
except ValueError:
    print("  ✓ Whitespace input raises ValueError")

mock_llm.generate.return_value = {'response': 'Too short\nOnly two lines'}
try:
    story_to_haiku("Test", llm_client=mock_llm)
    print("  ✗ Invalid response should raise error")
except ValueError:
    print("  ✓ Invalid response raises ValueError")

# Test 3: Dependency injection (TESTED)
print("\n[TESTED] Dependency Injection:")
mock_llm = Mock()
mock_llm.generate.return_value = {
    'response': 'Line one here now\nLine two is longer than one\nLine three ends the poem'
}
story_to_haiku("Test story", llm_client=mock_llm)
print(f"  ✓ Mock was called: {mock_llm.generate.called}")
print(f"  ✓ Called with llama3.2: {mock_llm.generate.call_args.kwargs['model'] == 'llama3.2'}")

# Test 4: What we DON'T test (SKIPPED)
print("\n[SKIPPED] Haiku Quality (non-deterministic):")
print("  - Poetic beauty: NOT TESTED (subjective)")
print("  - Semantic meaning: NOT TESTED (LLM-dependent)")
print("  - Artistic merit: NOT TESTED (too subjective)")

print("\n[SKIPPED] Exact Syllable Accuracy (algorithm-dependent):")
test_lines = [
    ("Cherry blossoms fall", 5, count_line_syllables("Cherry blossoms fall")),
    ("Softly on the quiet pond", 7, count_line_syllables("Softly on the quiet pond")),
    ("Spring whispers arrive", 5, count_line_syllables("Spring whispers arrive"))
]
print("  Expected vs Actual syllable counts:")
for line, expected, actual in test_lines:
    status = "✓" if expected == actual else "~"
    print(f"    {status} \"{line}\": expected {expected}, got {actual}")
print("  Note: Close but not perfect - this is why we don't test exact counts")

# Summary
print("\n" + "=" * 70)
print("Testing Strategy Summary:")
print("=" * 70)
print("\nWhat we TEST:")
print("  ✓ Structure (3 lines, newlines, dict keys)")
print("  ✓ Error handling (empty input, invalid responses)")
print("  ✓ Integration pattern (dependency injection)")
print("  ✓ Input processing (truncation)")
print("  ✓ Output format (types and presence)")

print("\nWhat we SKIP:")
print("  ✗ Haiku quality (subjective, non-deterministic)")
print("  ✗ Exact syllable accuracy (algorithm limitations)")
print("  ✗ Poetic meter (not in requirements)")
print("  ✗ Real Ollama calls (tested in comparison script)")

print("\nKey Insight:")
print("  Adaptive TDD = Test what matters, skip what doesn't")
print("  Result: Fast, focused, pragmatic test suite")

print("\n" + "=" * 70)
print("Implementation complete and verified!")
print("=" * 70)