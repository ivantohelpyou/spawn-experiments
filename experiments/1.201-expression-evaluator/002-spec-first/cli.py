"""
Command Line Interface for the Expression Evaluator system.

This module provides an interactive command-line interface for evaluating
mathematical expressions, managing variables, and batch processing.
"""

import argparse
import sys
import os
from typing import Dict, List, Optional, TextIO
try:
    from .expression_manager import ExpressionManager
    from .models import EvaluationResult
    from .exceptions import ExpressionError
except ImportError:
    from expression_manager import ExpressionManager
    from models import EvaluationResult
    from exceptions import ExpressionError


class ExpressionCLI:
    """
    Command Line Interface for the Expression Evaluator.

    Provides interactive and batch modes for expression evaluation
    with comprehensive command-line options and user-friendly output.
    """

    def __init__(self):
        """Initialize the CLI."""
        self.manager = ExpressionManager()
        self.interactive_mode = False
        self.verbose = False
        self.precision = 6
        self.output_format = 'decimal'

    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Run the CLI with given arguments.

        Args:
            args: Command line arguments (uses sys.argv if None)

        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            parsed_args = self._parse_arguments(args)
            self._configure_from_args(parsed_args)

            if parsed_args.interactive:
                return self._run_interactive_mode()
            elif parsed_args.file:
                return self._run_batch_mode(parsed_args.file)
            elif parsed_args.expression:
                return self._evaluate_single_expression(parsed_args.expression)
            else:
                self._print_help()
                return 1

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return 1
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    def _parse_arguments(self, args: Optional[List[str]]) -> argparse.Namespace:
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(
            description="Mathematical Expression Evaluator",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  expr-eval "2 + 3 * 4"                    # Evaluate single expression
  expr-eval --interactive                  # Start interactive mode
  expr-eval --file expressions.txt        # Process file
  expr-eval "x + y" --variables x=5 y=10  # Use variables
  expr-eval "sin(pi/2)" --precision 10    # High precision output
            """
        )

        # Mutually exclusive group for input modes
        input_group = parser.add_mutually_exclusive_group(required=False)
        input_group.add_argument(
            'expression',
            nargs='?',
            help='Mathematical expression to evaluate'
        )
        input_group.add_argument(
            '--interactive', '-i',
            action='store_true',
            help='Start interactive mode'
        )
        input_group.add_argument(
            '--file', '-f',
            type=str,
            help='File containing expressions to evaluate'
        )

        # Variable definitions
        parser.add_argument(
            '--variables', '--vars', '-v',
            action='append',
            help='Define variables (format: VAR=VALUE, can be used multiple times)'
        )

        # Output formatting
        parser.add_argument(
            '--precision', '-p',
            type=int,
            default=6,
            help='Number of decimal places for output (default: 6)'
        )
        parser.add_argument(
            '--format',
            choices=['decimal', 'scientific', 'engineering'],
            default='decimal',
            help='Output format (default: decimal)'
        )

        # Other options
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose output'
        )
        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='Only validate expressions without evaluating'
        )
        parser.add_argument(
            '--show-ast',
            action='store_true',
            help='Show Abstract Syntax Tree'
        )
        parser.add_argument(
            '--version',
            action='version',
            version='Expression Evaluator 1.0.0'
        )

        return parser.parse_args(args)

    def _configure_from_args(self, args: argparse.Namespace) -> None:
        """Configure CLI from parsed arguments."""
        self.verbose = args.verbose
        self.precision = max(0, min(15, args.precision))  # Clamp between 0 and 15
        self.output_format = args.format

        # Parse variable definitions
        if args.variables:
            for var_def in args.variables:
                self._parse_variable_definition(var_def)

    def _parse_variable_definition(self, var_def: str) -> None:
        """Parse and set a variable definition."""
        if '=' not in var_def:
            raise ValueError(f"Invalid variable definition: {var_def}. Use format VAR=VALUE")

        name, value_str = var_def.split('=', 1)
        name = name.strip()
        value_str = value_str.strip()

        if not name or not name.isidentifier():
            raise ValueError(f"Invalid variable name: {name}")

        try:
            value = float(value_str)
            self.manager.set_variable(name, value)
            if self.verbose:
                print(f"Set variable {name} = {value}")
        except ValueError:
            raise ValueError(f"Invalid variable value: {value_str}")

    def _run_interactive_mode(self) -> int:
        """Run the CLI in interactive mode."""
        print("Expression Evaluator - Interactive Mode")
        print("Type expressions to evaluate, or use commands:")
        print("  :help      - Show help")
        print("  :vars      - Show variables")
        print("  :clear     - Clear variables")
        print("  :stats     - Show statistics")
        print("  :quit      - Exit")
        print()

        while True:
            try:
                expression = input(">>> ").strip()

                if not expression:
                    continue

                if expression.startswith(':'):
                    if self._handle_command(expression):
                        break
                    continue

                result = self.manager.evaluate_expression(expression)
                self._print_result(result, expression)

            except EOFError:
                print("\nGoodbye!")
                break
            except KeyboardInterrupt:
                print("\nUse :quit to exit or Ctrl+D")
                continue

        return 0

    def _handle_command(self, command: str) -> bool:
        """
        Handle interactive mode commands.

        Args:
            command: Command string starting with ':'

        Returns:
            True if should exit, False to continue
        """
        cmd = command[1:].lower()

        if cmd in ('quit', 'exit', 'q'):
            return True

        elif cmd in ('help', 'h'):
            self._print_interactive_help()

        elif cmd in ('vars', 'variables'):
            variables = self.manager.get_variables()
            constants = self.manager.get_constants()

            print("Variables:")
            if variables:
                for name, value in sorted(variables.items()):
                    print(f"  {name} = {self._format_number(value)}")
            else:
                print("  (none)")

            print("Constants:")
            for name, value in sorted(constants.items()):
                print(f"  {name} = {self._format_number(value)}")

        elif cmd in ('clear', 'reset'):
            self.manager.clear_variables()
            print("Variables cleared.")

        elif cmd in ('stats', 'statistics'):
            stats = self.manager.get_statistics()
            print("Statistics:")
            print(f"  Total evaluations: {stats['total_evaluations']}")
            print(f"  Total time: {stats['total_evaluation_time']:.3f}s")
            print(f"  Average time: {stats['average_evaluation_time']:.3f}s")
            print(f"  Cache size: {stats['cache_size']}")
            print(f"  Variables: {stats['variable_count']}")
            print(f"  Functions: {stats['function_count']}")

        elif cmd in ('functions', 'funcs'):
            functions = self.manager.get_functions()
            print("Available functions:")
            for func in sorted(functions):
                print(f"  {func}")

        else:
            print(f"Unknown command: {command}")
            print("Type :help for available commands")

        return False

    def _print_interactive_help(self) -> None:
        """Print help for interactive mode."""
        print("Interactive Mode Commands:")
        print("  :help, :h           - Show this help")
        print("  :vars, :variables   - Show all variables and constants")
        print("  :functions, :funcs  - Show available functions")
        print("  :clear, :reset      - Clear all variables")
        print("  :stats              - Show evaluation statistics")
        print("  :quit, :exit, :q    - Exit interactive mode")
        print()
        print("Examples:")
        print("  2 + 3 * 4")
        print("  x = 5")
        print("  sin(pi/2)")
        print("  sqrt(x^2 + 4)")

    def _run_batch_mode(self, filename: str) -> int:
        """Run the CLI in batch mode."""
        try:
            with open(filename, 'r') as f:
                expressions = [line.strip() for line in f if line.strip() and not line.startswith('#')]

            if not expressions:
                print(f"No expressions found in {filename}")
                return 1

            print(f"Processing {len(expressions)} expressions from {filename}...")

            success_count = 0
            for i, expression in enumerate(expressions, 1):
                if self.verbose:
                    print(f"\n[{i}] {expression}")

                result = self.manager.evaluate_expression(expression)

                if result.success:
                    success_count += 1
                    if self.verbose:
                        print(f"Result: {self._format_number(result.value)}")
                    else:
                        print(f"{i}: {self._format_number(result.value)}")
                else:
                    print(f"{i}: ERROR - {result.error_message}")

            print(f"\nCompleted: {success_count}/{len(expressions)} successful")
            return 0 if success_count == len(expressions) else 1

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            return 1
        except PermissionError:
            print(f"Error: Permission denied reading '{filename}'")
            return 1

    def _evaluate_single_expression(self, expression: str) -> int:
        """Evaluate a single expression."""
        result = self.manager.evaluate_expression(expression)
        self._print_result(result, expression)
        return 0 if result.success else 1

    def _print_result(self, result: EvaluationResult, expression: str = "") -> None:
        """Print evaluation result."""
        if result.success:
            formatted_value = self._format_number(result.value)
            print(formatted_value)

            if self.verbose:
                print(f"Execution time: {result.execution_time:.3f}s")
        else:
            print(f"Error: {result.error_message}")
            if result.position is not None and expression:
                print(f"Position: {result.position}")
                print(f"Expression: {expression}")
                print(f"           {' ' * result.position}^")

    def _format_number(self, value: float) -> str:
        """Format a number according to current settings."""
        if self.output_format == 'scientific':
            return f"{value:.{self.precision}e}"
        elif self.output_format == 'engineering':
            # Engineering notation (exponents in multiples of 3)
            if value == 0:
                return f"0.{'0' * self.precision}e+00"

            import math
            exponent = int(math.floor(math.log10(abs(value))))
            eng_exponent = exponent - (exponent % 3)
            mantissa = value / (10 ** eng_exponent)
            return f"{mantissa:.{self.precision}f}e{eng_exponent:+03d}"
        else:  # decimal
            # Remove trailing zeros and decimal point if not needed
            formatted = f"{value:.{self.precision}f}".rstrip('0').rstrip('.')
            return formatted if formatted else "0"

    def _print_help(self) -> None:
        """Print general help message."""
        print("Expression Evaluator")
        print("Usage: expr-eval [OPTIONS] EXPRESSION")
        print("       expr-eval [OPTIONS] --interactive")
        print("       expr-eval [OPTIONS] --file FILE")
        print()
        print("Use --help for detailed options.")


def main() -> int:
    """Main entry point for the CLI."""
    cli = ExpressionCLI()
    return cli.run()


if __name__ == '__main__':
    sys.exit(main())