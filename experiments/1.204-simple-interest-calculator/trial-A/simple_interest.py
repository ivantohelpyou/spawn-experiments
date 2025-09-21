def calculate_simple_interest(principal, rate, time):
    """Calculate simple interest using the formula: SI = Principal × Rate × Time"""
    # Input validation: all values must be positive (> 0)
    if principal <= 0:
        raise ValueError("Principal must be greater than 0")
    if rate <= 0:
        raise ValueError("Rate must be greater than 0")
    if time <= 0:
        raise ValueError("Time must be greater than 0")

    return principal * (rate / 100) * time


def main():
    """Main function for command-line interface"""
    try:
        # Get user inputs with clear prompts
        print("Enter principal amount:", end=" ")
        principal = float(input())
        print("Enter interest rate (%):", end=" ")
        rate = float(input())
        print("Enter time period (years):", end=" ")
        time = float(input())

        # Calculate simple interest
        interest = calculate_simple_interest(principal, rate, time)

        # Display result with proper formatting
        print(f"Simple Interest: ${interest:.2f}")

    except ValueError as e:
        if "could not convert string to float" in str(e):
            print("Invalid input. Please enter numeric values only.")
        else:
            print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()