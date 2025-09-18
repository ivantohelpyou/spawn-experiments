#!/usr/bin/env python3
"""
Multilingual Word Counter - Main CLI Application

A comprehensive tool for counting words in multiple languages with automatic
language detection and detailed text analysis.

Usage:
    python multilingual_word_counter.py [OPTIONS] INPUT

Examples:
    python multilingual_word_counter.py "Hello world, 你好世界"
    python multilingual_word_counter.py document.txt
    python multilingual_word_counter.py https://example.com/article
    python multilingual_word_counter.py --format json --verbose input.docx
    cat input.txt | python multilingual_word_counter.py --stdin
"""

import sys
import os
import argparse
from typing import Optional, List

from models import ProcessingConfig
from text_analyzer import TextAnalyzer
from input_handler import InputHandler
from output_formatter import OutputFormatter


class MultilingualWordCounter:
    """Main application class for the Multilingual Word Counter."""

    def __init__(self, config: ProcessingConfig = None):
        """Initialize the application with configuration."""
        self.config = config or ProcessingConfig()
        self.analyzer = TextAnalyzer(self.config)
        self.input_handler = InputHandler()
        self.formatter = OutputFormatter()

    def process_single(self, input_source: str, input_type: str = None) -> dict:
        """
        Process a single input source.

        Args:
            input_source: Input source (text, file path, or URL)
            input_type: Type of input ('text', 'file', 'url', 'stdin')

        Returns:
            Dictionary with processing results and any errors
        """
        try:
            # Get text and metadata from input
            text, metadata = self.input_handler.process_input(input_source, input_type)

            if not text and metadata.get('error'):
                return {
                    'success': False,
                    'error': metadata['error'],
                    'metadata': metadata
                }

            # Analyze the text
            result = self.analyzer.analyze(text, metadata)

            return {
                'success': True,
                'result': result,
                'metadata': metadata
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'metadata': {'input_source': input_source}
            }

    def process_batch(self, input_sources: List[str]) -> dict:
        """
        Process multiple input sources.

        Args:
            input_sources: List of input sources

        Returns:
            Dictionary with batch processing results
        """
        results = []
        errors = []

        for source in input_sources:
            result = self.process_single(source)
            if result['success']:
                results.append(result['result'])
            else:
                errors.append({
                    'source': source,
                    'error': result['error']
                })

        return {
            'success': len(errors) == 0,
            'results': results,
            'errors': errors,
            'total_processed': len(input_sources),
            'successful': len(results),
            'failed': len(errors)
        }

    def format_output(self, result, format_type: str, verbose: bool = False) -> str:
        """Format output based on the specified format."""
        if format_type == 'json':
            return self.formatter.to_json(result, pretty=verbose)
        elif format_type == 'csv':
            return self.formatter.to_csv(result)
        elif format_type == 'summary':
            return self.formatter.to_summary(result)
        else:  # human-readable
            return self.formatter.to_human_readable(result, verbose)


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Multilingual Word Counter - Count words in multiple languages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s "Hello world, 你好世界"
    %(prog)s document.txt --format json
    %(prog)s https://example.com/article --verbose
    %(prog)s --stdin < input.txt
    %(prog)s file1.txt file2.txt --batch --format csv
        """
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument(
        'input',
        nargs='*',
        help='Input text, file path(s), or URL(s)'
    )
    input_group.add_argument(
        '--stdin',
        action='store_true',
        help='Read input from standard input'
    )

    # Processing options
    parser.add_argument(
        '--format', '-f',
        choices=['text', 'json', 'csv', 'summary'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output with detailed information'
    )

    parser.add_argument(
        '--batch', '-b',
        action='store_true',
        help='Process multiple files in batch mode'
    )

    # Language options
    parser.add_argument(
        '--language', '-l',
        help='Force specific language (ISO 639-1 code)'
    )

    parser.add_argument(
        '--confidence-threshold',
        type=float,
        default=0.8,
        help='Minimum confidence threshold for language detection (default: 0.8)'
    )

    parser.add_argument(
        '--disable-mixed-language',
        action='store_true',
        help='Disable mixed language detection'
    )

    # Output options
    parser.add_argument(
        '--output', '-o',
        help='Output file (default: stdout)'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress progress messages'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Multilingual Word Counter 1.0.0'
    )

    return parser


def main():
    """Main entry point for the CLI application."""
    parser = create_argument_parser()
    args = parser.parse_args()

    # Validate arguments
    if not args.stdin and not args.input:
        parser.error("No input provided. Use INPUT argument or --stdin option.")

    # Create configuration
    config = ProcessingConfig(
        min_confidence_threshold=args.confidence_threshold,
        enable_mixed_language=not args.disable_mixed_language,
        output_format=args.format
    )

    # Create application instance
    app = MultilingualWordCounter(config)

    try:
        # Process input
        if args.stdin:
            # Read from stdin
            result_data = app.process_single('', 'stdin')
        elif len(args.input) == 1 and not args.batch:
            # Single input
            input_source = args.input[0]
            result_data = app.process_single(input_source)
        else:
            # Multiple inputs or batch mode
            batch_result = app.process_batch(args.input)

            if not batch_result['success'] and not args.quiet:
                for error in batch_result['errors']:
                    print(f"Error processing {error['source']}: {error['error']}", file=sys.stderr)

            if batch_result['results']:
                # Format batch output
                if args.format == 'json':
                    output = app.formatter.to_json({
                        'batch_summary': {
                            'total_processed': batch_result['total_processed'],
                            'successful': batch_result['successful'],
                            'failed': batch_result['failed']
                        },
                        'results': [app.formatter._result_to_dict(r) for r in batch_result['results']]
                    }, pretty=args.verbose)
                else:
                    output = app.formatter.format_for_batch(
                        batch_result['results'],
                        'detailed' if args.verbose else 'summary'
                    )

                # Write output
                if args.output:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(output)
                    if not args.quiet:
                        print(f"Results written to {args.output}")
                else:
                    print(output)

                return 0 if batch_result['successful'] > 0 else 1

        # Handle single result
        if not result_data['success']:
            print(f"Error: {result_data['error']}", file=sys.stderr)
            return 1

        result = result_data['result']

        # Format output
        output = app.format_output(result, args.format, args.verbose)

        # Write output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            if not args.quiet:
                print(f"Results written to {args.output}")
        else:
            print(output)

        return 0

    except KeyboardInterrupt:
        print("\\nOperation cancelled by user.", file=sys.stderr)
        return 130

    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())