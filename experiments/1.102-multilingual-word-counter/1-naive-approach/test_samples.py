#!/usr/bin/env python3
"""
Test script for the Multilingual Word Counter
"""

from multilingual_word_counter import MultilingualWordCounter
import json

def test_multilingual_samples():
    """Test the word counter with various multilingual text samples."""
    counter = MultilingualWordCounter()

    # Test samples in different languages
    test_samples = {
        "English": "Hello world! This is a sample text in English with multiple words.",
        "Spanish": "Hola mundo! Este es un texto de muestra en español con múltiples palabras.",
        "French": "Bonjour le monde! Ceci est un exemple de texte en français avec plusieurs mots.",
        "German": "Hallo Welt! Das ist ein Beispieltext auf Deutsch mit mehreren Wörtern.",
        "Russian": "Привет мир! Это образец текста на русском языке с несколькими словами.",
        "Chinese": "你好世界！这是中文示例文本，包含多个词语。",
        "Japanese": "こんにちは世界！これは複数の単語を含む日本語のサンプルテキストです。",
        "Korean": "안녕하세요 세계! 이것은 여러 단어가 포함된 한국어 샘플 텍스트입니다.",
        "Arabic": "مرحبا بالعالم! هذا نص عينة باللغة العربية يحتوي على كلمات متعددة.",
        "Mixed": """Hello world! Hola mundo! Bonjour le monde!
                   你好世界！こんにちは世界！안녕하세요 세계!
                   مرحبا بالعالم! Привет мир!"""
    }

    print("MULTILINGUAL WORD COUNTER TEST RESULTS")
    print("=" * 60)

    for language, text in test_samples.items():
        print(f"\n{language.upper()} TEXT ANALYSIS:")
        print("-" * 40)
        print(f"Text: {text[:50]}...")

        try:
            analysis = counter.analyze_text(text)

            print(f"Standard Word Count: {analysis['word_count_standard']}")
            print(f"Character Count: {analysis['character_analysis']['total_chars']}")

            # Language detection
            detected = analysis['language_detection']
            print("Detected Languages:")
            for lang, confidence in detected.items():
                print(f"  {lang}: {confidence:.2%}")

            # Script analysis
            scripts = analysis['words_by_script']
            active_scripts = {k: v for k, v in scripts.items() if v > 0}
            if active_scripts:
                print("Words by Script:")
                for script, count in active_scripts.items():
                    print(f"  {script}: {count}")

            # Top words
            if analysis['word_frequency']:
                print("Top 5 Words:")
                for word, count in analysis['word_frequency'][:5]:
                    print(f"  {word}: {count}")

        except Exception as e:
            print(f"Error analyzing {language} text: {e}")

def test_cli_functionality():
    """Test the CLI functionality."""
    print("\n\nCLI FUNCTIONALITY TEST")
    print("=" * 60)

    # Test with sample text
    sample_text = "Hello world! This is a test. Hola mundo! Bonjour!"

    counter = MultilingualWordCounter()
    analysis = counter.analyze_text(sample_text)

    print("Sample text:", sample_text)
    print("Analysis results:")
    print(json.dumps(analysis, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_multilingual_samples()
    test_cli_functionality()