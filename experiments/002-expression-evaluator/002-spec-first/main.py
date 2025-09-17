#!/usr/bin/env python3
"""
Main entry point for the Expression Evaluator application.

This script provides a convenient way to run the expression evaluator
in different modes: CLI, examples, or tests.
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from cli import main as cli_main
import examples
import subprocess


def run_tests():
    """Run the test suite."""
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "test_expression_evaluator.py",
            "-v"
        ], cwd=Path(__file__).parent)
        return result.returncode
    except FileNotFoundError:
        print("pytest not found. Please install pytest to run tests:")
        print("pip install pytest")
        return 1


def run_examples():
    """Run the examples."""
    examples.main()
    return 0


def run_cli(args):
    """Run the CLI with given arguments."""
    return cli_main(args)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Expression Evaluator - Main Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available modes:
  cli         - Run command line interface (default)
  examples    - Run example demonstrations
  tests       - Run test suite

Examples:
  python main.py                          # Start CLI in interactive mode
  python main.py "2 + 3 * 4"             # Evaluate expression
  python main.py examples                 # Run examples
  python main.py tests                    # Run tests
  python main.py cli --help               # Show CLI help
        """
    )

    parser.add_argument(
        'mode',
        nargs='?',
        default='cli',
        choices=['cli', 'examples', 'tests'],
        help='Mode to run (default: cli)'
    )

    parser.add_argument(
        'args',
        nargs=argparse.REMAINDER,
        help='Arguments to pass to the selected mode'
    )

    parsed_args = parser.parse_args()

    if parsed_args.mode == 'examples':
        return run_examples()
    elif parsed_args.mode == 'tests':
        return run_tests()
    else:  # cli mode
        # If no args provided and mode is cli, start interactive mode
        if not parsed_args.args:
            cli_args = ['--interactive']
        else:
            cli_args = parsed_args.args
        return run_cli(cli_args)


if __name__ == "__main__":
    sys.exit(main())