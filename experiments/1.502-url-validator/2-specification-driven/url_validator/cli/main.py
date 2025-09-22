"""Command line interface for URL validation."""

import argparse
import sys
import os
from typing import List, Optional, TextIO
import logging

from ..models.config import ValidationConfig
from ..core.validator import URLValidator
from .formatter import OutputFormatter


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create command line argument parser.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog="url-validator",
        description="Validate URLs for format correctness and accessibility",
        epilog="Examples:\n"
               "  url-validator https://example.com\n"
               "  url-validator -f urls.txt -o json\n"
               "  url-validator --batch url1 url2 url3\n"
               "  url-validator https://example.com --no-accessibility\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "url",
        nargs="?",
        help="Single URL to validate"
    )
    input_group.add_argument(
        "--batch",
        nargs="+",
        metavar="URL",
        help="Multiple URLs to validate"
    )
    input_group.add_argument(
        "-f", "--file",
        type=str,
        metavar="FILE",
        help="File containing URLs (one per line)"
    )

    # Output options
    output_group = parser.add_argument_group("output options")
    output_group.add_argument(
        "-o", "--output-format",
        choices=["text", "json", "csv", "xml"],
        default="text",
        help="Output format (default: text)"
    )
    output_group.add_argument(
        "--output-file",
        type=str,
        metavar="FILE",
        help="Write output to file instead of stdout"
    )
    output_group.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output with detailed information"
    )
    output_group.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode (minimal output)"
    )

    # Validation options
    validation_group = parser.add_argument_group("validation options")
    validation_group.add_argument(
        "--no-accessibility",
        action="store_true",
        help="Skip accessibility checking (format validation only)"
    )
    validation_group.add_argument(
        "--timeout",
        type=int,
        default=10,
        metavar="SECONDS",
        help="Request timeout in seconds (default: 10)"
    )
    validation_group.add_argument(
        "--max-redirects",
        type=int,
        default=5,
        metavar="N",
        help="Maximum redirects to follow (default: 5)"
    )
    validation_group.add_argument(
        "--no-ssl-verify",
        action="store_true",
        help="Disable SSL certificate verification"
    )
    validation_group.add_argument(
        "--user-agent",
        type=str,
        default="URLValidator/1.0",
        metavar="STRING",
        help="Custom User-Agent header"
    )
    validation_group.add_argument(
        "--allowed-schemes",
        nargs="+",
        default=["http", "https"],
        metavar="SCHEME",
        help="Allowed URL schemes (default: http https)"
    )

    # Performance options
    perf_group = parser.add_argument_group("performance options")
    perf_group.add_argument(
        "--max-workers",
        type=int,
        default=10,
        metavar="N",
        help="Maximum concurrent workers for batch processing (default: 10)"
    )
    perf_group.add_argument(
        "--retry-attempts",
        type=int,
        default=3,
        metavar="N",
        help="Number of retry attempts for failed requests (default: 3)"
    )

    # Security options
    security_group = parser.add_argument_group("security options")
    security_group.add_argument(
        "--block-private-ips",
        action="store_true",
        help="Block private IP addresses"
    )

    # Logging options
    log_group = parser.add_argument_group("logging options")
    log_group.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="Logging level (default: WARNING)"
    )
    log_group.add_argument(
        "--log-file",
        type=str,
        metavar="FILE",
        help="Write logs to file"
    )

    # Utility options
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    parser.add_argument(
        "--config-file",
        type=str,
        metavar="FILE",
        help="Load configuration from JSON file"
    )

    return parser


def load_urls_from_file(file_path: str) -> List[str]:
    """
    Load URLs from file.

    Args:
        file_path: Path to file containing URLs

    Returns:
        List of URLs

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file can't be read
    """
    urls = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#'):  # Skip empty lines and comments
                    urls.append(line)
    except FileNotFoundError:
        raise FileNotFoundError(f"URL file not found: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading URL file {file_path}: {e}")

    if not urls:
        raise ValueError(f"No URLs found in file: {file_path}")

    return urls


def load_config_from_file(file_path: str) -> ValidationConfig:
    """
    Load configuration from JSON file.

    Args:
        file_path: Path to configuration file

    Returns:
        ValidationConfig object

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is invalid
    """
    import json

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        return ValidationConfig.from_dict(config_data)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file {file_path}: {e}")
    except Exception as e:
        raise ValueError(f"Error loading configuration from {file_path}: {e}")


def setup_logging(level: str, log_file: Optional[str] = None) -> None:
    """
    Set up logging configuration.

    Args:
        level: Logging level
        log_file: Optional log file path
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    if log_file:
        logging.basicConfig(
            level=getattr(logging, level),
            format=log_format,
            filename=log_file,
            filemode='a'
        )
    else:
        logging.basicConfig(
            level=getattr(logging, level),
            format=log_format
        )


def main() -> int:
    """
    Main CLI entry point.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_cli_parser()
    args = parser.parse_args()

    try:
        # Setup logging
        setup_logging(args.log_level, args.log_file)

        # Load configuration
        if args.config_file:
            config = load_config_from_file(args.config_file)
        else:
            config = ValidationConfig()

        # Update config with command line arguments
        config = config.update(
            timeout=args.timeout,
            max_redirects=args.max_redirects,
            verify_ssl=not args.no_ssl_verify,
            user_agent=args.user_agent,
            allowed_schemes=set(args.allowed_schemes),
            block_private_ips=args.block_private_ips,
            retry_attempts=args.retry_attempts,
            log_level=args.log_level
        )

        # Determine URLs to validate
        urls = []
        if args.url:
            urls = [args.url]
        elif args.batch:
            urls = args.batch
        elif args.file:
            urls = load_urls_from_file(args.file)

        if not urls:
            parser.error("No URLs provided for validation")

        # Setup output formatter
        formatter = OutputFormatter(
            format_type=args.output_format,
            verbose=args.verbose and not args.quiet
        )

        # Setup output file
        output_file = None
        if args.output_file:
            try:
                output_file = open(args.output_file, 'w', encoding='utf-8')
            except IOError as e:
                print(f"Error opening output file {args.output_file}: {e}", file=sys.stderr)
                return 1

        try:
            # Perform validation
            with URLValidator(config) as validator:
                if not args.quiet and len(urls) > 1:
                    print(f"Validating {len(urls)} URLs...", file=sys.stderr)

                if len(urls) == 1:
                    # Single URL validation
                    result = validator.validate(urls[0], not args.no_accessibility)
                    results = [result]
                else:
                    # Batch validation
                    results = validator.validate_batch(
                        urls,
                        not args.no_accessibility,
                        args.max_workers
                    )

                # Output results
                formatter.write_results(results, output_file)

                # Return appropriate exit code
                if all(r.is_valid and (r.is_accessible or args.no_accessibility) for r in results):
                    return 0
                else:
                    return 1

        finally:
            if output_file:
                output_file.close()

    except KeyboardInterrupt:
        print("\nValidation interrupted by user", file=sys.stderr)
        return 130
    except FileNotFoundError as e:
        print(f"File error: {e}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        return 3
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.log_level == "DEBUG":
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())