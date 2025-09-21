"""
Output formatting module for the Multilingual Word Counter.
Formats analysis results in various output formats (JSON, CSV, text).
"""

import json
import csv
from io import StringIO
from typing import Dict, Any

from models import AnalysisResult


class OutputFormatter:
    """Formats analysis results in various output formats."""

    def to_json(self, result: AnalysisResult, pretty: bool = True) -> str:
        """
        Format result as JSON.

        Args:
            result: Analysis result to format
            pretty: Whether to use pretty printing

        Returns:
            JSON-formatted string
        """
        # Convert result to dictionary
        result_dict = self._result_to_dict(result)

        if pretty:
            return json.dumps(result_dict, indent=2, ensure_ascii=False)
        else:
            return json.dumps(result_dict, ensure_ascii=False)

    def to_csv(self, result: AnalysisResult) -> str:
        """
        Format result as CSV.

        Args:
            result: Analysis result to format

        Returns:
            CSV-formatted string
        """
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['Metric', 'Value'])

        # Basic metrics
        writer.writerow(['Total Words', result.word_count.total_words])
        writer.writerow(['Total Characters', result.statistics.character_count])
        writer.writerow(['Characters (No Spaces)', result.statistics.character_count_no_spaces])
        writer.writerow(['Sentences', result.statistics.sentence_count])
        writer.writerow(['Paragraphs', result.statistics.paragraph_count])
        writer.writerow(['Avg Words/Sentence', result.statistics.average_words_per_sentence])
        writer.writerow(['Processing Time (s)', f"{result.processing_time:.3f}"])

        # Languages
        if result.detected_languages:
            primary_lang = result.detected_languages[0]
            writer.writerow(['Primary Language', primary_lang.name])
            writer.writerow(['Language Confidence', f"{primary_lang.confidence:.2f}"])

        # Language distribution
        for lang, count in result.word_count.words_by_language.items():
            writer.writerow([f'Words ({lang})', count])

        # Most frequent words
        writer.writerow(['', ''])  # Empty row
        writer.writerow(['Most Frequent Words', 'Count'])
        for word, count in result.statistics.most_frequent_words:
            writer.writerow([word, count])

        return output.getvalue()

    def to_human_readable(self, result: AnalysisResult, verbose: bool = False) -> str:
        """
        Format result in human-readable text format.

        Args:
            result: Analysis result to format
            verbose: Whether to include verbose details

        Returns:
            Human-readable formatted string
        """
        lines = []
        lines.append("=" * 50)
        lines.append("MULTILINGUAL WORD COUNTER - ANALYSIS RESULTS")
        lines.append("=" * 50)

        # Basic statistics
        lines.append("")
        lines.append("📊 TEXT STATISTICS")
        lines.append("-" * 20)
        lines.append(f"Total Words: {result.word_count.total_words:,}")
        lines.append(f"Characters: {result.statistics.character_count:,}")
        lines.append(f"Characters (no spaces): {result.statistics.character_count_no_spaces:,}")
        lines.append(f"Sentences: {result.statistics.sentence_count:,}")
        lines.append(f"Paragraphs: {result.statistics.paragraph_count:,}")
        lines.append(f"Average words per sentence: {result.statistics.average_words_per_sentence}")

        # Language information
        if result.detected_languages:
            lines.append("")
            lines.append("🌍 LANGUAGE ANALYSIS")
            lines.append("-" * 20)

            if len(result.detected_languages) == 1:
                lang = result.detected_languages[0]
                lines.append(f"Detected Language: {lang.name} ({lang.language})")
                lines.append(f"Confidence: {lang.confidence:.2%}")
            else:
                lines.append("Multiple languages detected:")
                for i, lang in enumerate(result.detected_languages, 1):
                    lines.append(f"  {i}. {lang.name} ({lang.language}) - {lang.confidence:.2%}")

            # Word count by language
            if len(result.word_count.words_by_language) > 1:
                lines.append("")
                lines.append("Words by language:")
                for lang, count in result.word_count.words_by_language.items():
                    percentage = result.word_count.language_distribution.get(lang, 0) * 100
                    lines.append(f"  {lang}: {count:,} words ({percentage:.1f}%)")

        # Most frequent words
        if result.statistics.most_frequent_words:
            lines.append("")
            lines.append("🔤 MOST FREQUENT WORDS")
            lines.append("-" * 20)
            for i, (word, count) in enumerate(result.statistics.most_frequent_words, 1):
                lines.append(f"  {i:2d}. {word}: {count}")

        # Performance info
        lines.append("")
        lines.append("⚡ PERFORMANCE")
        lines.append("-" * 20)
        lines.append(f"Processing time: {result.processing_time:.3f} seconds")

        # Verbose information
        if verbose:
            lines.append("")
            lines.append("🔍 DETAILED INFORMATION")
            lines.append("-" * 20)

            if result.metadata:
                lines.append("Metadata:")
                for key, value in result.metadata.items():
                    lines.append(f"  {key}: {value}")

            if hasattr(result, 'word_list') and result.word_count.word_list and len(result.word_count.word_list) <= 100:
                lines.append("")
                lines.append("Word list (first 100):")
                words_display = result.word_count.word_list[:100]
                lines.append("  " + ", ".join(words_display))

        lines.append("")
        lines.append("=" * 50)

        return "\\n".join(lines)

    def to_summary(self, result: AnalysisResult) -> str:
        """
        Format result as a brief summary.

        Args:
            result: Analysis result to format

        Returns:
            Brief summary string
        """
        if result.detected_languages:
            primary_lang = result.detected_languages[0]
            lang_info = f" in {primary_lang.name}"
        else:
            lang_info = ""

        return (
            f"{result.word_count.total_words} words, "
            f"{result.statistics.character_count} characters, "
            f"{result.statistics.sentence_count} sentences{lang_info}"
        )

    def format_for_batch(self, results: list[AnalysisResult], format_type: str = 'summary') -> str:
        """
        Format multiple results for batch processing.

        Args:
            results: List of analysis results
            format_type: Format type ('summary', 'detailed', 'csv')

        Returns:
            Formatted string for batch results
        """
        if format_type == 'csv':
            return self._batch_to_csv(results)
        elif format_type == 'detailed':
            return self._batch_to_detailed(results)
        else:  # summary
            return self._batch_to_summary(results)

    def _result_to_dict(self, result: AnalysisResult) -> Dict[str, Any]:
        """Convert AnalysisResult to dictionary for JSON serialization."""
        return {
            "summary": {
                "total_words": result.word_count.total_words,
                "total_characters": result.statistics.character_count,
                "sentences": result.statistics.sentence_count,
                "paragraphs": result.statistics.paragraph_count,
                "processing_time": result.processing_time
            },
            "languages": [
                {
                    "code": lang.language,
                    "name": lang.name,
                    "confidence": lang.confidence
                }
                for lang in result.detected_languages
            ],
            "word_count": {
                "total": result.word_count.total_words,
                "by_language": result.word_count.words_by_language,
                "language_distribution": result.word_count.language_distribution
            },
            "statistics": {
                "characters": result.statistics.character_count,
                "characters_no_spaces": result.statistics.character_count_no_spaces,
                "sentences": result.statistics.sentence_count,
                "paragraphs": result.statistics.paragraph_count,
                "average_words_per_sentence": result.statistics.average_words_per_sentence,
                "most_frequent_words": [
                    {"word": word, "count": count}
                    for word, count in result.statistics.most_frequent_words
                ]
            },
            "metadata": result.metadata
        }

    def _batch_to_csv(self, results: list[AnalysisResult]) -> str:
        """Format batch results as CSV."""
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            'Source', 'Words', 'Characters', 'Sentences', 'Paragraphs',
            'Primary Language', 'Confidence', 'Processing Time'
        ])

        # Write data
        for result in results:
            source = result.metadata.get('input_source', 'Unknown')
            primary_lang = result.detected_languages[0] if result.detected_languages else None

            writer.writerow([
                source,
                result.word_count.total_words,
                result.statistics.character_count,
                result.statistics.sentence_count,
                result.statistics.paragraph_count,
                primary_lang.name if primary_lang else 'Unknown',
                f"{primary_lang.confidence:.2f}" if primary_lang else 'N/A',
                f"{result.processing_time:.3f}"
            ])

        return output.getvalue()

    def _batch_to_detailed(self, results: list[AnalysisResult]) -> str:
        """Format batch results with detailed information."""
        lines = []
        lines.append("BATCH PROCESSING RESULTS")
        lines.append("=" * 50)

        for i, result in enumerate(results, 1):
            lines.append("")
            lines.append(f"FILE {i}: {result.metadata.get('input_source', 'Unknown')}")
            lines.append("-" * 30)
            lines.append(self.to_summary(result))
            if result.detected_languages:
                lang = result.detected_languages[0]
                lines.append(f"Language: {lang.name} ({lang.confidence:.1%})")

        # Summary
        lines.append("")
        lines.append("BATCH SUMMARY")
        lines.append("-" * 30)
        total_words = sum(r.word_count.total_words for r in results)
        total_chars = sum(r.statistics.character_count for r in results)
        avg_processing_time = sum(r.processing_time for r in results) / len(results)

        lines.append(f"Total files processed: {len(results)}")
        lines.append(f"Total words: {total_words:,}")
        lines.append(f"Total characters: {total_chars:,}")
        lines.append(f"Average processing time: {avg_processing_time:.3f}s")

        return "\\n".join(lines)

    def _batch_to_summary(self, results: list[AnalysisResult]) -> str:
        """Format batch results as summary."""
        lines = []
        lines.append("BATCH PROCESSING SUMMARY")
        lines.append("=" * 40)

        for i, result in enumerate(results, 1):
            source = result.metadata.get('input_source', 'Unknown')
            summary = self.to_summary(result)
            lines.append(f"{i:2d}. {source}: {summary}")

        return "\\n".join(lines)