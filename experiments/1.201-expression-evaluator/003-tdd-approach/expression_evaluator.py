"""
Expression Evaluator - Minimal Implementation for TDD Cycle 1

This is the minimal implementation to make the basic arithmetic tests pass.
Following TDD: Only implement what's needed to make tests green.
"""

import re
from enum import Enum
from dataclasses import dataclass
from typing import List


class TokenType(Enum):
    """Token types for the expression evaluator."""
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    EOF = "EOF"


@dataclass
class Token:
    """Represents a token in the expression."""
    type: TokenType
    value: str
    position: int = 0


class ExpressionEvaluator:
    """
    Simple expression evaluator using TDD approach.

    Currently supports basic arithmetic operations with minimal implementation.
    """

    def __init__(self):
        self.tokens = []
        self.current_token_index = 0
        self.current_token = None

    def evaluate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression string.

        Args:
            expression: String containing mathematical expression

        Returns:
            float: Numeric result of the expression

        Raises:
            ValueError: If expression has invalid syntax
            ZeroDivisionError: If expression contains division by zero
        """
        # Validate input
        if not expression or not expression.strip():
            raise ValueError("Empty expression")

        # Tokenize the expression
        self.tokens = self._tokenize(expression.strip())
        self.current_token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None

        # Parse and evaluate
        result = self._parse_expression()

        # Check for remaining tokens (indicates syntax error)
        if self.current_token.type != TokenType.EOF:
            raise ValueError(f"Unexpected token: {self.current_token.value}")

        return float(result)

    def _tokenize(self, expression: str) -> List[Token]:
        """
        Convert expression string into tokens.

        Args:
            expression: Input expression string

        Returns:
            List of tokens
        """
        tokens = []
        i = 0

        while i < len(expression):
            char = expression[i]

            # Skip whitespace
            if char.isspace():
                i += 1
                continue

            # Handle numbers (including negative and floating point)
            if char.isdigit() or char == '.' or (char == '-' and i + 1 < len(expression) and
                                               (expression[i + 1].isdigit() or expression[i + 1] == '.')):
                # Check if this is a negative number (not an operator)
                if char == '-':
                    # It's a negative number if it's at the start or after an operator
                    if i == 0 or tokens[-1].type in [TokenType.PLUS, TokenType.MINUS,
                                                    TokenType.MULTIPLY, TokenType.DIVIDE]:
                        number_start = i
                        i += 1  # Skip the minus sign
                    else:
                        # It's a minus operator
                        tokens.append(Token(TokenType.MINUS, char, i))
                        i += 1
                        continue
                else:
                    number_start = i

                # Collect the rest of the number (including scientific notation)
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1

                # Check for scientific notation (e or E)
                if i < len(expression) and expression[i].lower() == 'e':
                    i += 1  # consume 'e' or 'E'
                    # Check for optional + or - after e
                    if i < len(expression) and expression[i] in '+-':
                        i += 1
                    # Collect exponent digits
                    if i < len(expression) and expression[i].isdigit():
                        while i < len(expression) and expression[i].isdigit():
                            i += 1
                    else:
                        # Invalid scientific notation
                        raise ValueError(f"Invalid scientific notation at position {number_start}")

                number_str = expression[number_start:i]
                tokens.append(Token(TokenType.NUMBER, number_str, number_start))
                continue

            # Handle operators and parentheses
            if char == '+':
                tokens.append(Token(TokenType.PLUS, char, i))
            elif char == '-':
                tokens.append(Token(TokenType.MINUS, char, i))
            elif char == '*':
                tokens.append(Token(TokenType.MULTIPLY, char, i))
            elif char == '/':
                tokens.append(Token(TokenType.DIVIDE, char, i))
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char, i))
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char, i))
            else:
                # Invalid character
                raise ValueError(f"Invalid character '{char}' at position {i}")

            i += 1

        # Add EOF token
        tokens.append(Token(TokenType.EOF, "", len(expression)))
        return tokens

    def _parse_expression(self) -> float:
        """
        Parse and evaluate expression with proper precedence.

        Grammar:
        expression -> term (('+' | '-') term)*
        term -> factor (('*' | '/') factor)*
        factor -> number | '(' expression ')'
        """
        return self._parse_term_level()

    def _parse_term_level(self) -> float:
        """Parse addition and subtraction (lowest precedence)."""
        result = self._parse_factor_level()

        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            operator = self.current_token
            self._consume_token()
            right = self._parse_factor_level()
            result = self._apply_operation(result, operator.type, right)

        return result

    def _parse_factor_level(self) -> float:
        """Parse multiplication and division (higher precedence)."""
        result = self._parse_primary()

        while self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            operator = self.current_token
            self._consume_token()
            right = self._parse_primary()
            result = self._apply_operation(result, operator.type, right)

        return result

    def _parse_primary(self) -> float:
        """Parse primary expressions: numbers, parenthesized expressions, and unary minus."""
        if self.current_token.type == TokenType.NUMBER:
            value = float(self.current_token.value)
            self._consume_token()
            return value
        elif self.current_token.type == TokenType.LEFT_PAREN:
            self._consume_token()  # consume '('
            result = self._parse_term_level()  # parse the expression inside parentheses
            if self.current_token.type != TokenType.RIGHT_PAREN:
                raise ValueError("Expected closing parenthesis")
            self._consume_token()  # consume ')'
            return result
        elif self.current_token.type == TokenType.MINUS:
            # Handle unary minus
            self._consume_token()  # consume '-'
            return -self._parse_primary()  # recursively parse the negated expression
        else:
            raise ValueError(f"Expected number, '(', or '-', got {self.current_token.type}")

    def _is_operator(self, token_type: TokenType) -> bool:
        """Check if token type is an operator."""
        return token_type in [TokenType.PLUS, TokenType.MINUS,
                             TokenType.MULTIPLY, TokenType.DIVIDE]

    def _apply_operation(self, left: float, operator: TokenType, right: float) -> float:
        """Apply the specified operation to two operands."""
        if operator == TokenType.PLUS:
            return left + right
        elif operator == TokenType.MINUS:
            return left - right
        elif operator == TokenType.MULTIPLY:
            return left * right
        elif operator == TokenType.DIVIDE:
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def _consume_token(self):
        """Move to the next token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = Token(TokenType.EOF, "", -1)