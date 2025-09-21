class SimpleInterestCalculator:

    def calculate(self, principal, rate, time):
        """Calculate simple interest using the formula: SI = P × R × T / 100"""
        if principal <= 0:
            raise ValueError("Principal must be positive")
        if rate <= 0:
            raise ValueError("Rate must be positive")
        if time <= 0:
            raise ValueError("Time must be positive")

        return principal * rate * time / 100


class SimpleInterestApp:

    def __init__(self):
        self.calculator = SimpleInterestCalculator()

    def _get_positive_number(self, prompt, validation_keyword):
        """Helper method to get a positive number from user input with validation"""
        while True:
            try:
                value = float(input(prompt))
                # Validate by checking if it's positive
                if value <= 0:
                    raise ValueError(f"{validation_keyword} must be positive")
                return value
            except ValueError as e:
                if validation_keyword.lower() in str(e).lower():
                    print(f"Error: {e}")
                else:
                    print("Error: Please enter a valid number")

    def run(self):
        """Run the command-line interface for the simple interest calculator"""
        principal = self._get_positive_number("Enter principal amount: ", "Principal")
        rate = self._get_positive_number("Enter interest rate (%): ", "Rate")
        time = self._get_positive_number("Enter time period (years): ", "Time")

        result = self.calculator.calculate(principal, rate, time)
        print(f"Simple Interest: ${result:.2f}")


if __name__ == "__main__":
    app = SimpleInterestApp()
    app.run()