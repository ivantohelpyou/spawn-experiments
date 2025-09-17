#!/usr/bin/env python3
"""
Test demonstration script for Simple Interest Calculator

This script demonstrates the functionality of the simple interest calculator
by running automated tests with various input scenarios.
"""

import subprocess
import sys


def run_test(description: str, inputs: str, expected_output: str = None):
    """
    Run a test case with given inputs and check output.

    Args:
        description (str): Description of the test case
        inputs (str): Input values separated by newlines
        expected_output (str): Expected output to look for (optional)
    """
    print(f"\n{'='*50}")
    print(f"TEST: {description}")
    print(f"{'='*50}")

    try:
        # Run the calculator with the provided inputs
        process = subprocess.run(
            [sys.executable, "simple_interest_calculator.py"],
            input=inputs,
            text=True,
            capture_output=True,
            timeout=10
        )

        # Print the output
        print("Output:")
        print(process.stdout)

        if process.stderr:
            print("Errors:")
            print(process.stderr)

        # Check expected output if provided
        if expected_output and expected_output in process.stdout:
            print(f"✓ Expected output found: {expected_output}")
        elif expected_output:
            print(f"✗ Expected output not found: {expected_output}")

    except subprocess.TimeoutExpired:
        print("✗ Test timed out")
    except Exception as e:
        print(f"✗ Test failed with error: {e}")


def main():
    """Run all test demonstrations."""
    print("Simple Interest Calculator - Test Demonstrations")

    # Test 1: Basic functionality with example from requirements
    run_test(
        "Basic calculation (1000, 5%, 2 years)",
        "1000\n5\n2\n",
        "Simple Interest: $100.00"
    )

    # Test 2: Decimal values
    run_test(
        "Decimal values (1500.50, 4.5%, 1.5 years)",
        "1500.50\n4.5\n1.5\n",
        "Simple Interest: $101.28"
    )

    # Test 3: Error handling - invalid input types
    run_test(
        "Error handling - invalid inputs then valid ones",
        "abc\n-5\n0\n1000\n5\n2\n"
    )

    # Test 4: Small values
    run_test(
        "Small values (100, 2%, 0.5 years)",
        "100\n2\n0.5\n",
        "Simple Interest: $1.00"
    )

    # Test 5: Large values
    run_test(
        "Large values (50000, 10%, 5 years)",
        "50000\n10\n5\n",
        "Simple Interest: $25000.00"
    )

    print(f"\n{'='*50}")
    print("All test demonstrations completed!")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()