#!/usr/bin/env python3
"""
Simple Interest Calculator

A command-line application that calculates simple interest using the formula:
Simple Interest = Principal × Rate × Time

Author: Senior Software Engineer
"""


def validate_positive_number(value: str) -> tuple[bool, float]:
    """
    Validate that input string is a positive number.

    Args:
        value (str): String input to validate

    Returns:
        tuple[bool, float]: (is_valid, parsed_value)
    """
    try:
        # Remove any whitespace
        value = value.strip()

        # Check for empty input
        if not value:
            return False, 0.0

        # Convert to float
        parsed_value = float(value)

        # Check if positive
        if parsed_value <= 0:
            return False, parsed_value

        return True, parsed_value

    except ValueError:
        # Not a valid number
        return False, 0.0


def get_user_input(prompt: str) -> float:
    """
    Get and validate numeric input from user.

    Args:
        prompt (str): The message to display to the user

    Returns:
        float: Valid positive number entered by user
    """
    while True:
        user_input = input(prompt)
        is_valid, value = validate_positive_number(user_input)

        if is_valid:
            return value
        else:
            if not user_input.strip():
                print("Error: Please enter a value.")
            else:
                try:
                    float(user_input)
                    print("Error: Value must be greater than 0.")
                except ValueError:
                    print("Error: Please enter a valid number.")


def calculate_simple_interest(principal: float, rate: float, time: float) -> float:
    """
    Calculate simple interest using the standard formula.

    Args:
        principal (float): Principal amount in dollars
        rate (float): Interest rate as percentage
        time (float): Time period in years

    Returns:
        float: Calculated simple interest amount
    """
    # Convert rate from percentage to decimal
    rate_decimal = rate / 100.0

    # Apply simple interest formula: SI = P × R × T
    simple_interest = principal * rate_decimal * time

    return simple_interest


def format_currency(amount: float) -> str:
    """
    Format numeric amount as currency string.

    Args:
        amount (float): Numeric amount to format

    Returns:
        str: Formatted currency string (e.g., "$123.45")
    """
    return f"${amount:.2f}"


def display_result(interest: float) -> None:
    """
    Display the calculated result to user.

    Args:
        interest (float): Calculated simple interest amount
    """
    formatted_interest = format_currency(interest)
    print(f"Simple Interest: {formatted_interest}")


def main() -> None:
    """
    Main application entry point and controller.

    Orchestrates the complete user interaction flow:
    1. Get principal amount from user
    2. Get interest rate from user
    3. Get time period from user
    4. Calculate simple interest
    5. Display formatted result
    """
    try:
        # Get input from user
        principal = get_user_input("Enter principal amount: ")
        rate = get_user_input("Enter interest rate (%): ")
        time = get_user_input("Enter time period (years): ")

        # Calculate simple interest
        interest = calculate_simple_interest(principal, rate, time)

        # Display result
        display_result(interest)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        # Handle any unexpected errors
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()