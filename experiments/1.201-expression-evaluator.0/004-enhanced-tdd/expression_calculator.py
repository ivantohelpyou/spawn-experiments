class ExpressionCalculator:
    """Calculator for evaluating mathematical expressions.

    This implementation follows TDD principles and will be extended
    incrementally to support more complex expressions.
    """

    def evaluate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression string.

        Current implementation handles single numbers and basic addition.
        Will be extended to support more operations in future iterations.

        Args:
            expression: String containing a mathematical expression

        Returns:
            float: The numeric value of the expression

        Raises:
            ValueError: If the expression cannot be evaluated
        """
        if not isinstance(expression, str):
            raise ValueError("Expression must be a string")

        # Remove leading and trailing whitespace
        cleaned = expression.strip()

        if not cleaned:
            raise ValueError("Expression cannot be empty")

        # Check for any operators and parse with precedence
        if any(op in cleaned for op in ['+', '-', '*', '/']):
            return self._parse_expression(cleaned)

        try:
            # Convert to float (handles single numbers)
            return float(cleaned)
        except ValueError as e:
            raise ValueError(f"Invalid number format: '{cleaned}'") from e

    def _evaluate_addition(self, expression: str) -> float:
        """
        Evaluate a simple addition expression.

        Handles expressions like "2 + 3", "2.5 + 1.5", "-2 + 5", "3 + (-7)"
        """
        # Find the + operator (not at the start of the expression)
        # This ensures we don't mistake unary minus for addition
        plus_pos = -1
        for i in range(1, len(expression)):  # Start from 1 to skip potential unary minus
            if expression[i] == '+':
                plus_pos = i
                break

        if plus_pos == -1:
            raise ValueError("No addition operator found")

        left_part = expression[:plus_pos].strip()
        right_part = expression[plus_pos + 1:].strip()

        # Handle parentheses around operands
        if right_part.startswith('(') and right_part.endswith(')'):
            right_part = right_part[1:-1].strip()

        if left_part.startswith('(') and left_part.endswith(')'):
            left_part = left_part[1:-1].strip()

        try:
            left_value = float(left_part)
            right_value = float(right_part)
            return left_value + right_value
        except ValueError as e:
            raise ValueError(f"Invalid operand in addition: '{left_part}' + '{right_part}'") from e

    def _parse_expression(self, expression: str) -> float:
        """
        Parse and evaluate expression with proper operator precedence.

        Grammar:
        expression: term (('+' | '-') term)*
        term: factor (('*' | '/') factor)*
        factor: number | '(' expression ')'
        """
        self.tokens = self._tokenize(expression)
        self.pos = 0
        return self._parse_expression_level()

    def _tokenize(self, expression: str) -> list:
        """Tokenize the expression into numbers and operators."""
        import re
        # Handle negative numbers properly
        expression = expression.replace(' ', '')
        tokens = []
        i = 0
        while i < len(expression):
            if expression[i].isdigit() or expression[i] == '.':
                # Parse number
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(float(expression[i:j]))
                i = j
            elif expression[i] == '-' and (i == 0 or expression[i-1] in '(+*/-'):
                # Negative number
                j = i + 1
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(float(expression[i:j]))
                i = j
            elif expression[i] in '+-*/()':
                tokens.append(expression[i])
                i += 1
            else:
                i += 1
        return tokens

    def _parse_expression_level(self) -> float:
        """Parse addition and subtraction (lowest precedence)."""
        result = self._parse_term_level()

        while self.pos < len(self.tokens) and self.tokens[self.pos] in ['+', '-']:
            op = self.tokens[self.pos]
            self.pos += 1
            right = self._parse_term_level()
            if op == '+':
                result = result + right
            else:  # op == '-'
                result = result - right

        return result

    def _parse_term_level(self) -> float:
        """Parse multiplication and division (higher precedence)."""
        result = self._parse_factor()

        while self.pos < len(self.tokens) and self.tokens[self.pos] in ['*', '/']:
            op = self.tokens[self.pos]
            self.pos += 1
            right = self._parse_factor()
            if op == '*':
                result = result * right
            else:  # op == '/'
                if right == 0:
                    raise ValueError("Division by zero")
                result = result / right

        return result

    def _parse_factor(self) -> float:
        """Parse numbers and parenthesized expressions."""
        if self.pos >= len(self.tokens):
            raise ValueError("Unexpected end of expression")

        token = self.tokens[self.pos]

        if isinstance(token, float):
            self.pos += 1
            return token
        elif token == '(':
            self.pos += 1
            result = self._parse_expression_level()
            if self.pos >= len(self.tokens) or self.tokens[self.pos] != ')':
                raise ValueError("Missing closing parenthesis")
            self.pos += 1
            return result
        else:
            raise ValueError(f"Unexpected token: {token}")