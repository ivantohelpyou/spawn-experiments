# Multilingual Word Counter - Usage Guide

## Overview

A comprehensive multilingual word counter that supports language detection and analysis of text in multiple scripts including Latin, Chinese, Japanese, Korean, Arabic, Cyrillic, and more.

## Files

- `multilingual_word_counter.py` - Full-featured version with GUI (requires tkinter, matplotlib)
- `simple_word_counter.py` - Lightweight CLI-only version
- `demo.py` - Comprehensive demonstration of all features
- `test_samples.py` - Test script for validation
- `sample_text.txt` - Multilingual sample text for testing
- `requirements.txt` - Python dependencies

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

#### Basic text analysis:
```bash
python simple_word_counter.py "Hello world! Hola mundo!"
```

#### Analyze a file:
```bash
python simple_word_counter.py -f sample_text.txt
```

#### Output to JSON:
```bash
python simple_word_counter.py -f sample_text.txt --json -o results.json
```

#### Interactive mode:
```bash
python simple_word_counter.py
# Then type or paste your text and press Ctrl+D (Unix) or Ctrl+Z (Windows)
```

### Graphical Interface

```bash
python multilingual_word_counter.py --gui
```

## Features

### Language Detection
- Automatic detection of text language with confidence scores
- Supports 55+ languages via langdetect library

### Multi-Script Word Counting
- **Latin scripts**: English, Spanish, French, German, etc.
- **Chinese**: Simplified and Traditional Chinese
- **Japanese**: Hiragana, Katakana, Kanji
- **Korean**: Hangul
- **Arabic**: Arabic script
- **Cyrillic**: Russian, Bulgarian, Serbian, etc.
- **Other scripts**: Hebrew, Thai, Devanagari

### Text Analysis
- Standard word count (space-separated)
- Script-specific word counting
- Character analysis (letters, digits, punctuation, whitespace)
- Word frequency analysis
- Sentence and paragraph counting
- Line counting

### Output Formats
- Human-readable text format
- JSON format for programmatic use
- File output support

## Example Output

```
MULTILINGUAL TEXT ANALYSIS
==================================================
Text Length: 82 characters
Word Count: 16
Sentences: 4
Paragraphs: 1

Detected Languages:
  en: 57.14%
  es: 42.86%

Words by Script:
  latin: 16

Character Analysis:
  total_chars: 82
  letters: 63
  digits: 0
  whitespace: 15
  punctuation: 4

Top Words:
  hello: 1
  world: 1
  hola: 1
  mundo: 1
```

## Supported Languages

The program can detect and analyze text in 55+ languages including:
- English, Spanish, French, German, Italian, Portuguese
- Russian, Ukrainian, Bulgarian, Serbian
- Chinese (Simplified/Traditional), Japanese, Korean
- Arabic, Hebrew, Persian
- Hindi, Bengali, Tamil, Telugu
- Thai, Vietnamese, Indonesian
- And many more...

## Testing

Run the demonstration:
```bash
python demo.py
```

This will show analysis of text samples in 9 different languages and demonstrate all program features.

## Technical Notes

- The program uses regex patterns to identify different scripts
- For languages without spaces (Chinese, Japanese, Thai), character-based approximations are used
- Language detection requires at least 3 characters of meaningful text
- The GUI version requires tkinter and matplotlib for visualization features
- The CLI version has minimal dependencies and works in server environments