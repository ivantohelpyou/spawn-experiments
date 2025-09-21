#!/usr/bin/env python3
"""
Simplified Multilingual Word Counter for CLI-only environments
A lightweight version that works without GUI dependencies.
"""

import re
import sys
import argparse
import json
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional

try:
    from langdetect import detect, detect_langs, DetectorFactory
    DetectorFactory.seed = 0  # For consistent results
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    print("Warning: langdetect not available. Language detection will be limited.")

class MultilingualWordCounter:
    """Main class for multilingual word counting with language detection."""

    def __init__(self):
        self.language_patterns = {
            'chinese': r'[\u4e00-\u9fff]+',
            'japanese': r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]+',
            'korean': r'[\uac00-\ud7af]+',
            'arabic': r'[\u0600-\u06ff]+',
            'hebrew': r'[\u0590-\u05ff]+',
            'cyrillic': r'[\u0400-\u04ff]+',
            'thai': r'[\u0e00-\u0e7f]+',
            'devanagari': r'[\u0900-\u097f]+',
            'latin': r'[a-zA-ZÀ-ÿ]+',
        }

        self.language_word_separators = {
            'chinese': '',  # No spaces between words
            'japanese': '',  # No spaces between words
            'korean': ' ',  # Space separated
            'thai': '',     # No spaces between words
            'default': ' '  # Space separated for most languages
        }

    def detect_language(self, text: str) -> Dict[str, float]:
        """Detect language(s) in the text with confidence scores."""
        if not LANGDETECT_AVAILABLE:
            return {'unknown': 1.0}

        try:
            # Clean text for language detection
            clean_text = re.sub(r'[^\w\s]', ' ', text)
            if len(clean_text.strip()) < 3:
                return {'unknown': 1.0}

            detected_langs = detect_langs(clean_text)
            result = {}
            for lang in detected_langs:
                result[lang.lang] = lang.prob
            return result
        except:
            return {'unknown': 1.0}

    def count_words_by_script(self, text: str) -> Dict[str, int]:
        """Count words by script type (Latin, CJK, Arabic, etc.)."""
        script_counts = {}

        for script, pattern in self.language_patterns.items():
            matches = re.findall(pattern, text)
            if script in ['chinese', 'japanese', 'thai']:
                # For languages without spaces, count characters as approximate words
                char_count = sum(len(match) for match in matches)
                # Approximate word count (varies by language)
                if script == 'chinese':
                    word_count = char_count  # Chinese characters ≈ words
                elif script == 'japanese':
                    word_count = char_count // 2  # Japanese mix of kanji/kana
                else:
                    word_count = char_count // 3  # Thai approximation
                script_counts[script] = word_count
            else:
                # For space-separated languages
                script_counts[script] = len(matches)

        return script_counts

    def count_words_standard(self, text: str) -> int:
        """Standard word count (space-separated tokens)."""
        # Remove punctuation and split by whitespace
        words = re.findall(r'\b\w+\b', text)
        return len(words)

    def count_characters(self, text: str) -> Dict[str, int]:
        """Count various character types."""
        return {
            'total_chars': len(text),
            'letters': len(re.findall(r'[a-zA-ZÀ-ÿ\u0400-\u04ff\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af\u0600-\u06ff\u0590-\u05ff\u0e00-\u0e7f\u0900-\u097f]', text)),
            'digits': len(re.findall(r'\d', text)),
            'whitespace': len(re.findall(r'\s', text)),
            'punctuation': len(re.findall(r'[^\w\s]', text))
        }

    def get_word_frequency(self, text: str, top_n: int = 20) -> List[Tuple[str, int]]:
        """Get most frequent words."""
        words = re.findall(r'\b\w+\b', text.lower())
        return Counter(words).most_common(top_n)

    def analyze_text(self, text: str) -> Dict:
        """Comprehensive text analysis."""
        if not text.strip():
            return {'error': 'Empty text provided'}

        analysis = {
            'text_length': len(text),
            'language_detection': self.detect_language(text),
            'word_count_standard': self.count_words_standard(text),
            'words_by_script': self.count_words_by_script(text),
            'character_analysis': self.count_characters(text),
            'word_frequency': self.get_word_frequency(text),
            'sentences': len(re.findall(r'[.!?]+', text)),
            'paragraphs': len([p for p in text.split('\n\n') if p.strip()]),
            'lines': len(text.split('\n'))
        }

        return analysis

def create_cli():
    """Create command-line interface."""
    parser = argparse.ArgumentParser(description="Multilingual Word Counter with Language Detection")
    parser.add_argument("text", nargs="?", help="Text to analyze")
    parser.add_argument("-f", "--file", help="File to analyze")
    parser.add_argument("-o", "--output", help="Output file for results")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    return parser

def format_cli_output(analysis: Dict) -> str:
    """Format analysis results for CLI output."""
    lines = []
    lines.append("MULTILINGUAL TEXT ANALYSIS")
    lines.append("=" * 50)

    lines.append(f"Text Length: {analysis['text_length']} characters")
    lines.append(f"Word Count: {analysis['word_count_standard']}")
    lines.append(f"Sentences: {analysis['sentences']}")
    lines.append(f"Paragraphs: {analysis['paragraphs']}")
    lines.append("")

    lines.append("Detected Languages:")
    for lang, conf in analysis['language_detection'].items():
        lines.append(f"  {lang}: {conf:.2%}")
    lines.append("")

    lines.append("Words by Script:")
    for script, count in analysis['words_by_script'].items():
        if count > 0:
            lines.append(f"  {script}: {count}")
    lines.append("")

    lines.append("Character Analysis:")
    for char_type, count in analysis['character_analysis'].items():
        lines.append(f"  {char_type}: {count}")
    lines.append("")

    lines.append("Top Words:")
    for word, count in analysis['word_frequency'][:10]:
        lines.append(f"  {word}: {count}")

    return '\n'.join(lines)

def main():
    """Main entry point."""
    parser = create_cli()
    args = parser.parse_args()

    # CLI mode
    counter = MultilingualWordCounter()

    # Get text input
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    elif args.text:
        text = args.text
    else:
        # Interactive mode
        print("Multilingual Word Counter")
        print("Enter your text (press Ctrl+D on Unix/Linux or Ctrl+Z on Windows when finished):")
        try:
            text = sys.stdin.read()
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return

    # Analyze text
    try:
        analysis = counter.analyze_text(text)

        # Output results
        if args.json:
            output = json.dumps(analysis, indent=2, ensure_ascii=False)
        else:
            output = format_cli_output(analysis)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Results saved to {args.output}")
        else:
            print(output)

    except Exception as e:
        print(f"Analysis failed: {e}")

if __name__ == "__main__":
    main()