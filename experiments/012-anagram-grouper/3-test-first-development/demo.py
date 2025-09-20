#!/usr/bin/env python3
"""
Demo script showing the anagram grouper function in action.
"""
from anagram_grouper import group_anagrams


def print_result(words, result):
    """Pretty print the anagram grouping result."""
    print(f"Input:  {words}")
    print(f"Output: {result}")
    print("-" * 50)


def main():
    """Run various demonstrations of the anagram grouper."""
    print("=== Anagram Grouper Demo ===\n")

    # Basic anagram grouping
    words1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
    result1 = group_anagrams(words1)
    print_result(words1, result1)

    # Case sensitivity
    words2 = ["Eat", "tea", "Tea", "ATE"]
    result2 = group_anagrams(words2)
    print_result(words2, result2)

    # Empty and single word cases
    words3 = []
    result3 = group_anagrams(words3)
    print_result(words3, result3)

    words4 = ["hello"]
    result4 = group_anagrams(words4)
    print_result(words4, result4)

    # Edge cases with duplicates and empty strings
    words5 = ["", "", "hello", "hello", "world"]
    result5 = group_anagrams(words5)
    print_result(words5, result5)

    # Words with punctuation and spaces
    words6 = ["a!b", "b!a", "a b", "b a", "listen", "silent"]
    result6 = group_anagrams(words6)
    print_result(words6, result6)

    print("\n=== Performance Test ===")
    import time

    # Performance test with larger dataset
    large_words = ["eat", "tea", "ate"] * 1000 + ["hello", "world"] * 500
    start_time = time.time()
    large_result = group_anagrams(large_words)
    end_time = time.time()

    print(f"Processed {len(large_words)} words in {end_time - start_time:.4f} seconds")
    print(f"Result contains {len(large_result)} anagram groups")


if __name__ == "__main__":
    main()