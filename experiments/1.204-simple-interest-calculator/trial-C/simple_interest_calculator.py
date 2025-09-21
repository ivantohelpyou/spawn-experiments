#!/usr/bin/env python3
"""
Simple Interest Calculator

Calculates simple interest using the formula: Simple Interest = Principal × Rate × Time
"""

def get_positive_float(prompt):
    """Get a positive float input from the user with validation."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Error: Please enter a positive number greater than 0.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid number.")

def calculate_simple_interest(principal, rate, time):
    """
    Calculate simple interest.

    Args:
        principal (float): Principal amount in dollars
        rate (float): Interest rate as percentage
        time (float): Time period in years

    Returns:
        float: Simple interest amount
    """
    return (principal * rate * time) / 100

def main():
    """Main function to run the simple interest calculator."""
    print("Simple Interest Calculator")
    print("-" * 25)

    # Get inputs from user
    principal = get_positive_float("Enter principal amount: $")
    rate = get_positive_float("Enter interest rate (%): ")
    time = get_positive_float("Enter time period (years): ")

    # Calculate simple interest
    interest = calculate_simple_interest(principal, rate, time)

    # Display result
    print(f"\nSimple Interest: ${interest:.2f}")

if __name__ == "__main__":
    main()