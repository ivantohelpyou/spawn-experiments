#!/usr/bin/env python3
"""
Multilingual Word Counter with Language Detection
A comprehensive tool for counting words in multiple languages with advanced features.
"""

import re
import sys
import argparse
import json
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

try:
    from langdetect import detect, detect_langs, DetectorFactory
    DetectorFactory.seed = 0  # For consistent results
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    print("Warning: langdetect not available. Language detection will be limited.")

try:
    import nltk
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("Warning: NLTK not available. Advanced text processing will be limited.")

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

class WordCounterGUI:
    """Graphical User Interface for the Multilingual Word Counter."""

    def __init__(self):
        self.counter = MultilingualWordCounter()
        self.root = tk.Tk()
        self.root.title("Multilingual Word Counter")
        self.root.geometry("1000x700")

        self.setup_gui()

    def setup_gui(self):
        """Set up the GUI components."""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Main analysis tab
        self.main_frame = ttk.Frame(notebook)
        notebook.add(self.main_frame, text="Text Analysis")

        # File processing tab
        self.file_frame = ttk.Frame(notebook)
        notebook.add(self.file_frame, text="File Processing")

        # Statistics tab
        self.stats_frame = ttk.Frame(notebook)
        notebook.add(self.stats_frame, text="Statistics")

        self.setup_main_tab()
        self.setup_file_tab()
        self.setup_stats_tab()

    def setup_main_tab(self):
        """Set up the main text analysis tab."""
        # Input section
        input_frame = ttk.LabelFrame(self.main_frame, text="Input Text")
        input_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.text_input = scrolledtext.ScrolledText(input_frame, height=15, wrap=tk.WORD)
        self.text_input.pack(fill='both', expand=True, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill='x', padx=5, pady=5)

        ttk.Button(button_frame, text="Analyze Text", command=self.analyze_text).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_text).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Load Sample", command=self.load_sample_text).pack(side='left', padx=5)

        # Results section
        results_frame = ttk.LabelFrame(self.main_frame, text="Analysis Results")
        results_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.results_text = scrolledtext.ScrolledText(results_frame, height=10, wrap=tk.WORD)
        self.results_text.pack(fill='both', expand=True, padx=5, pady=5)

    def setup_file_tab(self):
        """Set up the file processing tab."""
        # File selection
        file_frame = ttk.LabelFrame(self.file_frame, text="File Processing")
        file_frame.pack(fill='x', padx=5, pady=5)

        ttk.Button(file_frame, text="Select File", command=self.select_file).pack(side='left', padx=5, pady=5)
        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.pack(side='left', padx=5, pady=5)

        # File results
        file_results_frame = ttk.LabelFrame(self.file_frame, text="File Analysis Results")
        file_results_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.file_results = scrolledtext.ScrolledText(file_results_frame, wrap=tk.WORD)
        self.file_results.pack(fill='both', expand=True, padx=5, pady=5)

    def setup_stats_tab(self):
        """Set up the statistics visualization tab."""
        # Create matplotlib figure
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, self.stats_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)

    def analyze_text(self):
        """Analyze the text in the input field."""
        text = self.text_input.get('1.0', tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to analyze.")
            return

        try:
            analysis = self.counter.analyze_text(text)
            self.display_results(analysis)
            self.update_statistics(analysis)
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")

    def display_results(self, analysis: Dict):
        """Display analysis results in the results text area."""
        self.results_text.delete('1.0', tk.END)

        results = []
        results.append("MULTILINGUAL TEXT ANALYSIS RESULTS")
        results.append("=" * 50)
        results.append(f"Text Length: {analysis['text_length']} characters")
        results.append(f"Word Count (Standard): {analysis['word_count_standard']}")
        results.append(f"Sentences: {analysis['sentences']}")
        results.append(f"Paragraphs: {analysis['paragraphs']}")
        results.append(f"Lines: {analysis['lines']}")
        results.append("")

        # Language detection
        results.append("DETECTED LANGUAGES:")
        for lang, confidence in analysis['language_detection'].items():
            results.append(f"  {lang}: {confidence:.2%}")
        results.append("")

        # Words by script
        results.append("WORDS BY SCRIPT:")
        for script, count in analysis['words_by_script'].items():
            if count > 0:
                results.append(f"  {script.title()}: {count}")
        results.append("")

        # Character analysis
        results.append("CHARACTER ANALYSIS:")
        char_analysis = analysis['character_analysis']
        for char_type, count in char_analysis.items():
            results.append(f"  {char_type.replace('_', ' ').title()}: {count}")
        results.append("")

        # Word frequency
        results.append("TOP 10 MOST FREQUENT WORDS:")
        for word, count in analysis['word_frequency'][:10]:
            results.append(f"  {word}: {count}")

        self.results_text.insert('1.0', '\n'.join(results))

    def update_statistics(self, analysis: Dict):
        """Update the statistics visualizations."""
        self.ax1.clear()
        self.ax2.clear()

        # Script distribution pie chart
        script_data = {k: v for k, v in analysis['words_by_script'].items() if v > 0}
        if script_data:
            self.ax1.pie(script_data.values(), labels=script_data.keys(), autopct='%1.1f%%')
            self.ax1.set_title('Word Distribution by Script')

        # Top words bar chart
        words, counts = zip(*analysis['word_frequency'][:10])
        self.ax2.bar(range(len(words)), counts)
        self.ax2.set_xticks(range(len(words)))
        self.ax2.set_xticklabels(words, rotation=45)
        self.ax2.set_title('Top 10 Most Frequent Words')

        self.canvas.draw()

    def clear_text(self):
        """Clear the input text area."""
        self.text_input.delete('1.0', tk.END)
        self.results_text.delete('1.0', tk.END)

    def load_sample_text(self):
        """Load sample multilingual text."""
        sample_text = """Hello, this is a sample text in English.
Hola, este es un texto de muestra en español.
Bonjour, ceci est un exemple de texte en français.
Hallo, das ist ein Beispieltext auf Deutsch.
Привет, это образец текста на русском языке.
こんにちは、これは日本語のサンプルテキストです。
你好，这是中文示例文本。
안녕하세요, 이것은 한국어 샘플 텍스트입니다.
مرحبا، هذا نص عينة باللغة العربية."""

        self.text_input.delete('1.0', tk.END)
        self.text_input.insert('1.0', sample_text)

    def select_file(self):
        """Select and process a text file."""
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                self.file_label.config(text=f"File: {file_path}")
                analysis = self.counter.analyze_text(content)

                # Display file analysis
                self.file_results.delete('1.0', tk.END)
                results = self.format_analysis_for_display(analysis)
                self.file_results.insert('1.0', results)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to process file: {str(e)}")

    def format_analysis_for_display(self, analysis: Dict) -> str:
        """Format analysis results for display."""
        results = []
        results.append("FILE ANALYSIS RESULTS")
        results.append("=" * 50)

        for key, value in analysis.items():
            if isinstance(value, dict):
                results.append(f"{key.upper().replace('_', ' ')}:")
                for subkey, subvalue in value.items():
                    results.append(f"  {subkey}: {subvalue}")
                results.append("")
            elif isinstance(value, list):
                results.append(f"{key.upper().replace('_', ' ')}:")
                for item in value[:10]:  # Show top 10
                    if isinstance(item, tuple):
                        results.append(f"  {item[0]}: {item[1]}")
                    else:
                        results.append(f"  {item}")
                results.append("")
            else:
                results.append(f"{key.replace('_', ' ').title()}: {value}")

        return '\n'.join(results)

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

def create_cli():
    """Create command-line interface."""
    parser = argparse.ArgumentParser(description="Multilingual Word Counter with Language Detection")
    parser.add_argument("text", nargs="?", help="Text to analyze")
    parser.add_argument("-f", "--file", help="File to analyze")
    parser.add_argument("-o", "--output", help="Output file for results")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--gui", action="store_true", help="Launch GUI mode")

    return parser

def main():
    """Main entry point."""
    parser = create_cli()
    args = parser.parse_args()

    # Launch GUI if requested or no arguments provided
    if args.gui or len(sys.argv) == 1:
        app = WordCounterGUI()
        app.run()
        return

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
        print("Please provide text to analyze or use --gui for graphical interface")
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

if __name__ == "__main__":
    main()