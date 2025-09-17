#!/usr/bin/env python3
"""
Calculator CLI - Command Line Interface for Expression Evaluator

A user-friendly command-line interface for the expression evaluator.
"""

import sys
import os
from typing import Optional
from expression_evaluator import ExpressionEvaluator


class CalculatorCLI:
    """Command-line interface for the expression evaluator."""

    def __init__(self):
        """Initialize the CLI with an expression evaluator."""
        self.evaluator = ExpressionEvaluator()
        self.history = []
        self.running = True

    def display_welcome(self):
        """Display welcome message and basic usage instructions."""
        print("=" * 60)
        print("  EXPRESSION EVALUATOR - Naive Direct Approach")
        print("=" * 60)
        print()
        print("Welcome to the Expression Calculator!")
        print("Enter mathematical expressions to evaluate them.")
        print()
        print("Examples:")
        print("  2 + 3 * 4")
        print("  (1 + 2) * 3")
        print("  sqrt(16)")
        print("  sin(pi/2)")
        print("  2**3")
        print()
        print("Commands:")
        print("  help     - Show this help message")
        print("  funcs    - Show available functions")
        print("  consts   - Show available constants")
        print("  history  - Show calculation history")
        print("  clear    - Clear history")
        print("  quit     - Exit the calculator")
        print()

    def display_help(self):
        """Display detailed help information."""
        print("\nHELP - Expression Evaluator")
        print("=" * 40)
        print()
        print("OPERATORS:")
        print("  +       Addition")
        print("  -       Subtraction")
        print("  *       Multiplication")
        print("  /       Division")
        print("  %       Modulo")
        print("  **      Exponentiation")
        print("  ()      Parentheses for grouping")
        print()
        print("Enter 'funcs' to see available functions.")
        print("Enter 'consts' to see available constants.")
        print()

    def display_functions(self):
        """Display available functions."""
        print("\nAVAILABLE FUNCTIONS:")
        print("=" * 40)
        functions = self.evaluator.get_available_functions()
        for func, desc in functions.items():
            print(f"  {func:15} - {desc}")
        print()

    def display_constants(self):
        """Display available constants."""
        print("\nAVAILABLE CONSTANTS:")
        print("=" * 40)
        constants = self.evaluator.get_available_constants()
        for name, value in constants.items():
            print(f"  {name:10} = {value}")
        print()

    def display_history(self):
        """Display calculation history."""
        print("\nCALCULATION HISTORY:")
        print("=" * 40)
        if not self.history:
            print("  No calculations yet.")
        else:
            for i, (expr, result) in enumerate(self.history, 1):
                print(f"  {i:2d}. {expr} = {result}")
        print()

    def clear_history(self):
        """Clear the calculation history."""
        self.history.clear()
        print("History cleared.")

    def process_command(self, command: str) -> bool:
        """
        Process special commands.

        Args:
            command: The command to process

        Returns:
            True if command was processed, False otherwise
        """
        command = command.lower().strip()

        if command in ['quit', 'exit', 'q']:
            self.running = False
            print("Goodbye!")
            return True
        elif command in ['help', 'h', '?']:
            self.display_help()
            return True
        elif command in ['funcs', 'functions']:
            self.display_functions()
            return True
        elif command in ['consts', 'constants']:
            self.display_constants()
            return True
        elif command in ['history', 'hist']:
            self.display_history()
            return True
        elif command in ['clear', 'cls']:
            self.clear_history()
            return True

        return False

    def evaluate_expression(self, expression: str) -> Optional[float]:
        """
        Evaluate an expression and handle errors.

        Args:
            expression: The expression to evaluate

        Returns:
            The result if successful, None if there was an error
        """
        try:
            result = self.evaluator.evaluate(expression)
            self.history.append((expression, result))
            return result
        except ValueError as e:
            print(f"Error: {e}")
            return None
        except ZeroDivisionError:
            print("Error: Division by zero")
            return None
        except OverflowError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def format_result(self, result: float) -> str:
        """
        Format the result for display.

        Args:
            result: The numerical result

        Returns:
            Formatted string representation
        """
        # If it's a whole number, display as integer
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        else:
            # Format float with reasonable precision
            return f"{result:.10g}"

    def run(self):
        """Run the interactive calculator."""
        self.display_welcome()

        try:
            while self.running:
                try:
                    # Get user input
                    user_input = input("calc> ").strip()

                    if not user_input:
                        continue

                    # Check if it's a command
                    if self.process_command(user_input):
                        continue

                    # Evaluate expression
                    result = self.evaluate_expression(user_input)
                    if result is not None:
                        print(f"= {self.format_result(result)}")

                except KeyboardInterrupt:
                    print("\nUse 'quit' to exit.")
                    continue
                except EOFError:
                    print("\nGoodbye!")
                    break

        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)


def main():
    """Main entry point for the calculator CLI."""
    cli = CalculatorCLI()
    cli.run()


if __name__ == "__main__":
    main()