#!/usr/bin/env python3
"""
Multilingual Word Counter Demo Script

This script demonstrates the functionality of the multilingual word counter
built using Test-Driven Development principles.
"""

import tempfile
import os
from core.word_counter import MultilingualWordCounter
from utils.file_handler import FileHandler


def print_separator():
    """Print a visual separator."""
    print("=" * 60)


def print_result(title: str, result):
    """Print word count result in a formatted way."""
    print(f"\n{title}")
    print(f"Text: {result.text[:50]}..." if len(result.text) > 50 else f"Text: {result.text}")
    print(f"Total Words: {result.total_words}")
    print(f"Detected Languages: {[lang.code for lang in result.detected_languages]}")
    print(f"Language Breakdown: {result.language_breakdown}")
    print(f"Processing Time: {result.processing_time:.4f} seconds")
    if 'file_path' in result.metadata:
        print(f"File Size: {result.metadata['file_size']} bytes")
        print(f"Encoding: {result.metadata['encoding']}")


def demo_basic_word_counting():
    """Demonstrate basic word counting functionality."""
    print_separator()
    print("DEMO 1: Basic Word Counting")
    print_separator()

    counter = MultilingualWordCounter()

    # Test cases with different languages
    test_cases = [
        ("English", "Hello world! This is a test of the multilingual word counter."),
        ("Spanish", "Hola mundo! Esta es una prueba del contador de palabras multiidioma."),
        ("French", "Bonjour le monde! Ceci est un test du compteur de mots multilingue."),
        ("German", "Hallo Welt! Dies ist ein Test des mehrsprachigen Wortzählers."),
        ("Mixed", "Hello world! Hola mundo! Bonjour le monde!")
    ]

    for language, text in test_cases:
        result = counter.count_words(text)
        print_result(f"🔤 {language} Text:", result)


def demo_file_processing():
    """Demonstrate file processing functionality."""
    print_separator()
    print("DEMO 2: File Processing")
    print_separator()

    file_handler = FileHandler()

    # Create temporary files with different content
    test_files = [
        ("english_sample.txt", "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet."),
        ("spanish_sample.txt", "El rápido zorro marrón salta sobre el perro perezoso. Esta es una traducción del texto en inglés."),
        ("mixed_sample.txt", "This is English text. Este es texto en español. Ceci est du texte français.")
    ]

    for filename, content in test_files:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_file = f.name

        try:
            # Process the file
            result = file_handler.process_file(temp_file)
            print_result(f"📄 {filename}:", result)

        finally:
            # Clean up temporary file
            os.unlink(temp_file)


def demo_edge_cases():
    """Demonstrate edge case handling."""
    print_separator()
    print("DEMO 3: Edge Cases")
    print_separator()

    counter = MultilingualWordCounter()

    edge_cases = [
        ("Empty string", ""),
        ("Whitespace only", "   \t\n  "),
        ("Single word", "Hello"),
        ("Punctuation heavy", "Hello, world! How are you? I'm fine, thanks."),
        ("Numbers and symbols", "Test123 with symbols @#$% and numbers 42."),
        ("Very short text", "Hi")
    ]

    for description, text in edge_cases:
        result = counter.count_words(text)
        print_result(f"⚠️  {description}:", result)


def demo_error_handling():
    """Demonstrate error handling."""
    print_separator()
    print("DEMO 4: Error Handling")
    print_separator()

    counter = MultilingualWordCounter()
    file_handler = FileHandler()

    print("🚫 Testing error handling:")

    # Test None input
    try:
        counter.count_words(None)
    except ValueError as e:
        print(f"✓ None input handled: {e}")

    # Test non-existent file
    try:
        file_handler.process_file("/path/that/does/not/exist.txt")
    except FileNotFoundError as e:
        print(f"✓ Non-existent file handled: {e}")

    # Test empty file path
    try:
        file_handler.process_file("")
    except ValueError as e:
        print(f"✓ Empty file path handled: {e}")


def main():
    """Run all demos."""
    print("🌍 MULTILINGUAL WORD COUNTER DEMO")
    print("Built with Test-Driven Development")
    print_separator()

    demo_basic_word_counting()
    demo_file_processing()
    demo_edge_cases()
    demo_error_handling()

    print_separator()
    print("✅ Demo completed successfully!")
    print("All functionality implemented using strict TDD principles:")
    print("  1. RED: Write failing tests first")
    print("  2. GREEN: Write minimal code to pass tests")
    print("  3. REFACTOR: Clean up code while keeping tests green")
    print_separator()


if __name__ == "__main__":
    main()