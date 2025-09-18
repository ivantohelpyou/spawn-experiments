#!/usr/bin/env python3
"""
Demonstration script for the Multilingual Word Counter
Shows all features and capabilities of the program.
"""

from simple_word_counter import MultilingualWordCounter
import json

def main():
    print("MULTILINGUAL WORD COUNTER DEMONSTRATION")
    print("=" * 60)
    print()

    counter = MultilingualWordCounter()

    # Test cases with different languages and scripts
    test_cases = [
        {
            "name": "English Text",
            "text": "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet."
        },
        {
            "name": "Spanish Text",
            "text": "El zorro marrón rápido salta sobre el perro perezoso. Esta oración contiene muchas palabras españolas."
        },
        {
            "name": "French Text",
            "text": "Le renard brun rapide saute par-dessus le chien paresseux. Cette phrase contient de nombreux mots français."
        },
        {
            "name": "Chinese Text",
            "text": "你好世界！这是一个中文文本示例。中文没有空格分隔单词。"
        },
        {
            "name": "Japanese Text",
            "text": "こんにちは世界！これは日本語のテキストサンプルです。日本語にはひらがな、カタカナ、漢字があります。"
        },
        {
            "name": "Korean Text",
            "text": "안녕하세요 세계! 이것은 한국어 텍스트 샘플입니다. 한국어는 한글로 쓰여집니다."
        },
        {
            "name": "Arabic Text",
            "text": "مرحبا بالعالم! هذا مثال على النص العربي. العربية تُكتب من اليمين إلى اليسار."
        },
        {
            "name": "Russian Text",
            "text": "Привет мир! Это пример русского текста. Русский язык использует кириллический алфавит."
        },
        {
            "name": "Mixed Languages",
            "text": "Hello! Hola! Bonjour! 你好! こんにちは! 안녕하세요! مرحبا! Привет! This text mixes multiple languages and scripts."
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['name'].upper()}")
        print("-" * 50)
        print(f"Text: {test_case['text']}")
        print()

        analysis = counter.analyze_text(test_case['text'])

        # Basic statistics
        print(f"Length: {analysis['text_length']} characters")
        print(f"Word count: {analysis['word_count_standard']}")
        print(f"Sentences: {analysis['sentences']}")
        print()

        # Language detection
        print("Detected languages:")
        for lang, confidence in analysis['language_detection'].items():
            print(f"  {lang}: {confidence:.1%}")
        print()

        # Script analysis
        print("Words by script:")
        for script, count in analysis['words_by_script'].items():
            if count > 0:
                print(f"  {script.title()}: {count}")
        print()

        # Character breakdown
        chars = analysis['character_analysis']
        print(f"Characters: {chars['letters']} letters, {chars['digits']} digits, {chars['whitespace']} spaces, {chars['punctuation']} punctuation")
        print()

        # Top words
        if analysis['word_frequency']:
            print("Most frequent words:")
            for word, count in analysis['word_frequency'][:5]:
                print(f"  {word}: {count}")
        print()
        print("=" * 60)
        print()

    # Demonstrate file processing
    print("FILE PROCESSING DEMONSTRATION")
    print("=" * 60)
    print()

    try:
        with open('sample_text.txt', 'r', encoding='utf-8') as f:
            file_content = f.read()

        print("Analyzing sample_text.txt...")
        file_analysis = counter.analyze_text(file_content)

        print(f"File contains {file_analysis['text_length']} characters")
        print(f"Total words: {file_analysis['word_count_standard']}")
        print(f"Lines: {file_analysis['lines']}")
        print(f"Paragraphs: {file_analysis['paragraphs']}")
        print()

        print("Scripts detected in file:")
        for script, count in file_analysis['words_by_script'].items():
            if count > 0:
                print(f"  {script.title()}: {count} words")
        print()

    except FileNotFoundError:
        print("sample_text.txt not found. Skipping file demonstration.")
        print()

    print("FEATURES SUMMARY")
    print("=" * 60)
    print("✓ Language detection using langdetect library")
    print("✓ Multi-script word counting (Latin, CJK, Arabic, Cyrillic, etc.)")
    print("✓ Character analysis (letters, digits, punctuation, whitespace)")
    print("✓ Word frequency analysis")
    print("✓ Sentence and paragraph counting")
    print("✓ File input/output support")
    print("✓ JSON output format")
    print("✓ Command-line interface")
    print("✓ Comprehensive text statistics")
    print()
    print("The multilingual word counter successfully handles multiple languages")
    print("and writing systems, providing detailed analysis suitable for")
    print("linguistic research, content analysis, and text processing tasks.")

if __name__ == "__main__":
    main()