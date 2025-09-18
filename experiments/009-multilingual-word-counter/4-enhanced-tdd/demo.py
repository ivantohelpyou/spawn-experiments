#!/usr/bin/env python3
"""
Demonstration of the Multilingual Word Counter
Built using Test-Driven Development with comprehensive test validation
"""

from word_counter import MultilingualWordCounter
import json


def demo_basic_functionality():
    """Demonstrate basic word counting functionality"""
    print("=== BASIC WORD COUNTING DEMO ===")

    counter = MultilingualWordCounter()

    test_cases = [
        "",
        "hello",
        "hello world",
        "hello    world",
        "Hello, world! How are you?",
        "This is a longer English text with multiple words to demonstrate confidence scaling",
        "Hi"
    ]

    for text in test_cases:
        result = counter.count_words(text)
        print(f"\nText: '{text}'")
        print(f"  Words: {result.total_words}")
        print(f"  Characters (no spaces): {result.total_chars}")
        print(f"  Characters (with spaces): {result.total_chars_with_spaces}")
        print(f"  Primary Language: {result.primary_language}")
        print(f"  Confidence: {result.primary_confidence:.3f}")

        if result.languages:
            for lang_code, stats in result.languages.items():
                print(f"  Language {lang_code}: {stats.word_count} words, confidence {stats.confidence:.3f}")


def demo_language_detection():
    """Demonstrate language detection functionality"""
    print("\n\n=== LANGUAGE DETECTION DEMO ===")

    counter = MultilingualWordCounter()

    test_texts = [
        "Hello world this is English text",
        "Hi",
        "The quick brown fox jumps over the lazy dog",
        ""
    ]

    for text in test_texts:
        detections = counter.detect_language(text)
        print(f"\nText: '{text}'")
        if detections:
            for detection in detections:
                print(f"  Language: {detection.language_name} ({detection.language_code})")
                print(f"  Confidence: {detection.confidence:.3f}")
        else:
            print("  No language detected")


def demo_integrated_functionality():
    """Demonstrate integrated word counting with language detection"""
    print("\n\n=== INTEGRATED FUNCTIONALITY DEMO ===")

    counter = MultilingualWordCounter()

    sample_texts = [
        "This is a comprehensive test of the multilingual word counter system",
        "Testing short text",
        "Hello world",
        ""
    ]

    for text in sample_texts:
        result = counter.count_words(text)
        print(f"\nAnalyzing: '{text}'")
        print(f"Results:")
        print(f"  Total words: {result.total_words}")
        print(f"  Total characters: {result.total_chars}")
        print(f"  Primary language: {result.primary_language} (confidence: {result.primary_confidence:.3f})")

        if result.languages:
            print(f"  Language breakdown:")
            for lang_code, stats in result.languages.items():
                print(f"    {stats.language_name}: {stats.word_count} words, {stats.char_count} chars")
                print(f"    Sample: {stats.sample_text}")


if __name__ == "__main__":
    print("MULTILINGUAL WORD COUNTER")
    print("Built using Enhanced Test-Driven Development")
    print("=" * 50)

    demo_basic_functionality()
    demo_language_detection()
    demo_integrated_functionality()

    print(f"\n{'=' * 50}")
    print("Demo completed successfully!")
    print("All functionality built through rigorous TDD with test validation.")