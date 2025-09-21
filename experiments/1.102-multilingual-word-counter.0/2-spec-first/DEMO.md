# Multilingual Word Counter - Demo

This file demonstrates the capabilities of the Multilingual Word Counter application.

## Quick Test

To test the application, you can run:

```bash
# Basic text analysis
python multilingual_word_counter.py "Hello world! This is a test sentence."

# JSON output
python multilingual_word_counter.py "Hello world" --format json

# Create a test file and analyze it
echo "This is a test file with multiple sentences. It contains various words for analysis." > test.txt
python multilingual_word_counter.py test.txt --verbose

# Test multilingual text (if you have the dependencies)
python multilingual_word_counter.py "Hello world. Bonjour le monde. Hola mundo."
```

## Sample Test Files

Here are some sample texts you can test with:

### English Text
```
"The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet at least once."
```

### Mixed Language Text
```
"Hello world. Bonjour le monde. Hola mundo. Guten Tag Welt."
```

### Longer Text Sample
```
"Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language. In particular, it focuses on how to program computers to process and analyze large amounts of natural language data. The result is a computer capable of understanding the contents of documents, including the contextual nuances of the language within them."
```

## Testing Different Features

1. **Language Detection**:
   ```bash
   python multilingual_word_counter.py "Ceci est un texte en français."
   ```

2. **Verbose Output**:
   ```bash
   python multilingual_word_counter.py "Sample text" --verbose
   ```

3. **CSV Format**:
   ```bash
   python multilingual_word_counter.py "Sample text" --format csv
   ```

4. **Summary Format**:
   ```bash
   python multilingual_word_counter.py "Sample text" --format summary
   ```

## Expected Output Example

For the input "Hello world, this is a test!", you should see output similar to:

```
==================================================
MULTILINGUAL WORD COUNTER - ANALYSIS RESULTS
==================================================

📊 TEXT STATISTICS
--------------------
Total Words: 7
Characters: 32
Characters (no spaces): 26
Sentences: 1
Paragraphs: 1
Average words per sentence: 7.0

🌍 LANGUAGE ANALYSIS
--------------------
Detected Language: English (en)
Confidence: 99.9%

🔤 MOST FREQUENT WORDS
--------------------
   1. hello: 1
   2. world: 1
   3. this: 1
   4. test: 1

⚡ PERFORMANCE
--------------------
Processing time: 0.045 seconds
```

## Installation Notes

Before running the demo, make sure you have installed the required dependencies:

```bash
pip install langdetect nltk requests beautifulsoup4
```

For full functionality (including Chinese, Word docs, PDF support):

```bash
pip install spacy jieba python-docx PyPDF2
```

## Troubleshooting

If you encounter issues:

1. **ImportError**: Install missing dependencies with pip
2. **NLTK Data Error**: The application will attempt to download required NLTK data automatically
3. **Language Detection Errors**: Very short texts may not be detected accurately

The application is designed to be robust and will fall back to basic functionality if optional dependencies are missing.