"""
Tokenizer service for the Expression Evaluator system.

This module handles lexical analysis of mathematical expressions,
converting input strings into streams of tokens.
"""

import re
from typing import List, Iterator, Optional
try:
    from .models import Token, TokenType
    from .exceptions import SyntaxError
except ImportError:
    from models import Token, TokenType
    from exceptions import SyntaxError


class Tokenizer:
    """
    Converts mathematical expressions into token streams.

    The tokenizer performs lexical analysis, identifying numbers, operators,
    functions, variables, and other elements of mathematical expressions.
    """

    # Regular expressions for token patterns
    PATTERNS = {
        TokenType.NUMBER: r'\d+\.?\d*([eE][+-]?\d+)?',
        TokenType.FUNCTION: r'[a-zA-Z_][a-zA-Z0-9_]*(?=\s*\()',
        TokenType.VARIABLE: r'[a-zA-Z_][a-zA-Z0-9_]*',
        TokenType.OPERATOR: r'\*\*|//|[+\-*/()%^]',
        TokenType.LEFT_PAREN: r'\(',
        TokenType.RIGHT_PAREN: r'\)',
        TokenType.COMMA: r',',
    }

    # Operator precedence and associativity
    OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'left'},
        '-': {'precedence': 1, 'associativity': 'left'},
        '*': {'precedence': 2, 'associativity': 'left'},
        '/': {'precedence': 2, 'associativity': 'left'},
        '//': {'precedence': 2, 'associativity': 'left'},
        '%': {'precedence': 2, 'associativity': 'left'},
        '**': {'precedence': 3, 'associativity': 'right'},
        '^': {'precedence': 3, 'associativity': 'right'},
    }

    # Mathematical constants
    CONSTANTS = {'pi', 'e', 'tau', 'inf'}

    def __init__(self):
        """Initialize the tokenizer."""
        self.expression = ""
        self.position = 0
        self.tokens = []

    def tokenize(self, expression: str) -> List[Token]:
        """
        Tokenize a mathematical expression.

        Args:
            expression: The mathematical expression to tokenize

        Returns:
            List of tokens representing the expression

        Raises:
            SyntaxError: If the expression contains invalid syntax
        """
        self.expression = expression.strip()
        self.position = 0
        self.tokens = []

        if not self.expression:
            return [Token(TokenType.EOF, "", 0)]

        while self.position < len(self.expression):
            if self._skip_whitespace():
                continue

            token = self._next_token()
            if token is None:
                raise SyntaxError(
                    f"Invalid character '{self.expression[self.position]}'",
                    position=self.position,
                    suggestion="Check for unsupported characters or typos"
                )

            self.tokens.append(token)

        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.position))
        return self.tokens

    def _skip_whitespace(self) -> bool:
        """Skip whitespace characters."""
        start_pos = self.position
        while self.position < len(self.expression) and self.expression[self.position].isspace():
            self.position += 1
        return self.position > start_pos

    def _next_token(self) -> Optional[Token]:
        """Get the next token from the expression."""
        if self.position >= len(self.expression):
            return None

        # Try to match each token type
        for token_type, pattern in self.PATTERNS.items():
            regex = re.compile(pattern)
            match = regex.match(self.expression, self.position)

            if match:
                value = match.group(0)
                token_position = self.position
                self.position = match.end()

                # Special handling for different token types
                if token_type == TokenType.VARIABLE:
                    # Check if it's actually a constant
                    if value in self.CONSTANTS:
                        return Token(TokenType.CONSTANT, value, token_position)
                    # Check if it's actually a function (this shouldn't happen due to regex)
                    return Token(TokenType.VARIABLE, value, token_position)
                elif token_type == TokenType.OPERATOR:
                    # Handle special cases for operators
                    if value in ('(', ')'):
                        if value == '(':
                            return Token(TokenType.LEFT_PAREN, value, token_position)
                        else:
                            return Token(TokenType.RIGHT_PAREN, value, token_position)
                    return Token(TokenType.OPERATOR, value, token_position)
                else:
                    return Token(token_type, value, token_position)

        return None

    def get_operator_precedence(self, operator: str) -> int:
        """Get the precedence of an operator."""
        return self.OPERATORS.get(operator, {}).get('precedence', 0)

    def get_operator_associativity(self, operator: str) -> str:
        """Get the associativity of an operator."""
        return self.OPERATORS.get(operator, {}).get('associativity', 'left')

    def is_right_associative(self, operator: str) -> bool:
        """Check if an operator is right associative."""
        return self.get_operator_associativity(operator) == 'right'

    def is_operator(self, token: Token) -> bool:
        """Check if a token is an operator."""
        return token.type == TokenType.OPERATOR

    def is_function(self, token: Token) -> bool:
        """Check if a token is a function."""
        return token.type == TokenType.FUNCTION

    def is_number(self, token: Token) -> bool:
        """Check if a token is a number."""
        return token.type == TokenType.NUMBER

    def is_variable(self, token: Token) -> bool:
        """Check if a token is a variable."""
        return token.type == TokenType.VARIABLE

    def is_constant(self, token: Token) -> bool:
        """Check if a token is a constant."""
        return token.type == TokenType.CONSTANT

    def validate_tokens(self, tokens: List[Token]) -> None:
        """
        Validate a token stream for basic syntax errors.

        Args:
            tokens: List of tokens to validate

        Raises:
            SyntaxError: If the token stream contains syntax errors
        """
        if not tokens or tokens[-1].type != TokenType.EOF:
            raise SyntaxError("Invalid token stream")

        paren_count = 0
        prev_token = None

        for token in tokens[:-1]:  # Exclude EOF token
            # Check parentheses balance
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise SyntaxError(
                        "Unmatched closing parenthesis",
                        position=token.position,
                        suggestion="Check parentheses balance"
                    )

            # Check for invalid token sequences
            if prev_token:
                self._validate_token_sequence(prev_token, token)

            prev_token = token

        # Check final parentheses balance
        if paren_count != 0:
            raise SyntaxError(
                "Unmatched opening parenthesis",
                suggestion="Check parentheses balance"
            )

    def _validate_token_sequence(self, prev_token: Token, current_token: Token) -> None:
        """Validate sequence of two consecutive tokens."""
        # Two numbers in a row (missing operator)
        if (prev_token.type == TokenType.NUMBER and
            current_token.type == TokenType.NUMBER):
            raise SyntaxError(
                "Missing operator between numbers",
                position=current_token.position,
                suggestion="Add an operator between the numbers"
            )

        # Two operators in a row (except unary minus)
        if (prev_token.type == TokenType.OPERATOR and
            current_token.type == TokenType.OPERATOR):
            if not (prev_token.value in ('(', ',') or current_token.value == '-'):
                raise SyntaxError(
                    "Invalid operator sequence",
                    position=current_token.position,
                    suggestion="Check operator placement"
                )

        # Function not followed by opening parenthesis
        if (prev_token.type == TokenType.FUNCTION and
            current_token.type != TokenType.LEFT_PAREN):
            raise SyntaxError(
                "Function must be followed by opening parenthesis",
                position=current_token.position,
                suggestion=f"Add '(' after function '{prev_token.value}'"
            )

    def __str__(self) -> str:
        """String representation of the tokenizer."""
        return f"Tokenizer(expression='{self.expression}', position={self.position})"