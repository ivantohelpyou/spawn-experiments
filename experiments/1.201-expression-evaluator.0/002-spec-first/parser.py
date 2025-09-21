"""
Parser service for the Expression Evaluator system.

This module handles syntax analysis of mathematical expressions,
converting token streams into Abstract Syntax Trees (AST).
"""

from typing import List, Optional
try:
    from .models import Token, TokenType, ExpressionNode, NodeType
    from .tokenizer import Tokenizer
    from .exceptions import SyntaxError
except ImportError:
    from models import Token, TokenType, ExpressionNode, NodeType
    from tokenizer import Tokenizer
    from exceptions import SyntaxError


class Parser:
    """
    Converts token streams into Abstract Syntax Trees.

    The parser implements a recursive descent parser with operator precedence
    to handle mathematical expressions correctly according to standard
    mathematical precedence rules.
    """

    def __init__(self, tokenizer: Optional[Tokenizer] = None):
        """
        Initialize the parser.

        Args:
            tokenizer: Optional tokenizer instance (creates one if not provided)
        """
        self.tokenizer = tokenizer or Tokenizer()
        self.tokens = []
        self.position = 0
        self.current_token = None

    def parse(self, expression: str) -> ExpressionNode:
        """
        Parse a mathematical expression into an AST.

        Args:
            expression: The mathematical expression to parse

        Returns:
            Root node of the expression AST

        Raises:
            SyntaxError: If the expression has syntax errors
        """
        # Tokenize the expression
        self.tokens = self.tokenizer.tokenize(expression)
        self.tokenizer.validate_tokens(self.tokens)

        # Initialize parser state
        self.position = 0
        self.current_token = self.tokens[0] if self.tokens else None

        # Parse the expression
        if not self.tokens or self.tokens[0].type == TokenType.EOF:
            raise SyntaxError("Empty expression")

        ast = self._parse_expression()

        # Check for unexpected tokens at the end
        if self.current_token and self.current_token.type != TokenType.EOF:
            raise SyntaxError(
                f"Unexpected token: {self.current_token.value}",
                position=self.current_token.position,
                suggestion="Check for extra characters at the end of expression"
            )

        return ast

    def _advance(self) -> None:
        """Move to the next token."""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None

    def _peek_token(self, offset: int = 1) -> Optional[Token]:
        """Peek at a future token without advancing."""
        peek_pos = self.position + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None

    def _expect_token(self, token_type: TokenType) -> Token:
        """
        Expect a specific token type and advance.

        Args:
            token_type: Expected token type

        Returns:
            The current token

        Raises:
            SyntaxError: If the current token doesn't match expected type
        """
        if not self.current_token or self.current_token.type != token_type:
            expected = token_type.value
            actual = self.current_token.type.value if self.current_token else "EOF"
            raise SyntaxError(
                f"Expected {expected}, got {actual}",
                position=self.current_token.position if self.current_token else len(self.tokens),
                suggestion=f"Add missing {expected.lower()}"
            )

        token = self.current_token
        self._advance()
        return token

    def _parse_expression(self) -> ExpressionNode:
        """Parse a complete expression (lowest precedence level)."""
        return self._parse_additive()

    def _parse_additive(self) -> ExpressionNode:
        """Parse addition and subtraction (precedence level 1)."""
        left = self._parse_multiplicative()

        while (self.current_token and
               self.current_token.type == TokenType.OPERATOR and
               self.current_token.value in ('+', '-')):

            operator = self.current_token.value
            operator_token = self.current_token
            self._advance()
            right = self._parse_multiplicative()

            left = ExpressionNode(
                node_type=NodeType.BINARY_OP,
                operator=operator,
                left=left,
                right=right
            )

        return left

    def _parse_multiplicative(self) -> ExpressionNode:
        """Parse multiplication, division, and modulo (precedence level 2)."""
        left = self._parse_power()

        while (self.current_token and
               self.current_token.type == TokenType.OPERATOR and
               self.current_token.value in ('*', '/', '//', '%')):

            operator = self.current_token.value
            self._advance()
            right = self._parse_power()

            left = ExpressionNode(
                node_type=NodeType.BINARY_OP,
                operator=operator,
                left=left,
                right=right
            )

        return left

    def _parse_power(self) -> ExpressionNode:
        """Parse exponentiation (precedence level 3, right-associative)."""
        left = self._parse_unary()

        if (self.current_token and
            self.current_token.type == TokenType.OPERATOR and
            self.current_token.value in ('**', '^')):

            operator = self.current_token.value
            self._advance()
            # Right associative: parse power, not unary
            right = self._parse_power()

            return ExpressionNode(
                node_type=NodeType.BINARY_OP,
                operator=operator,
                left=left,
                right=right
            )

        return left

    def _parse_unary(self) -> ExpressionNode:
        """Parse unary operators (highest precedence)."""
        if (self.current_token and
            self.current_token.type == TokenType.OPERATOR and
            self.current_token.value in ('+', '-')):

            operator = self.current_token.value
            self._advance()
            operand = self._parse_unary()

            return ExpressionNode(
                node_type=NodeType.UNARY_OP,
                operator=operator,
                right=operand
            )

        return self._parse_primary()

    def _parse_primary(self) -> ExpressionNode:
        """Parse primary expressions (numbers, variables, functions, parentheses)."""
        if not self.current_token:
            raise SyntaxError("Unexpected end of expression")

        # Numbers
        if self.current_token.type == TokenType.NUMBER:
            value = float(self.current_token.value)
            self._advance()
            return ExpressionNode(node_type=NodeType.NUMBER, value=value)

        # Constants
        if self.current_token.type == TokenType.CONSTANT:
            name = self.current_token.value
            self._advance()
            return ExpressionNode(node_type=NodeType.CONSTANT, value=name)

        # Variables
        if self.current_token.type == TokenType.VARIABLE:
            name = self.current_token.value
            self._advance()
            return ExpressionNode(node_type=NodeType.VARIABLE, value=name)

        # Functions
        if self.current_token.type == TokenType.FUNCTION:
            return self._parse_function_call()

        # Parentheses
        if self.current_token.type == TokenType.LEFT_PAREN:
            self._advance()  # consume '('
            expr = self._parse_expression()
            self._expect_token(TokenType.RIGHT_PAREN)  # consume ')'
            return expr

        # If we get here, it's an unexpected token
        raise SyntaxError(
            f"Unexpected token: {self.current_token.value}",
            position=self.current_token.position,
            suggestion="Check for typos or missing operators"
        )

    def _parse_function_call(self) -> ExpressionNode:
        """Parse function calls with arguments."""
        function_name = self.current_token.value
        self._advance()  # consume function name

        self._expect_token(TokenType.LEFT_PAREN)  # consume '('

        # Parse arguments
        arguments = []
        if self.current_token and self.current_token.type != TokenType.RIGHT_PAREN:
            arguments.append(self._parse_expression())

            while (self.current_token and
                   self.current_token.type == TokenType.COMMA):
                self._advance()  # consume ','
                arguments.append(self._parse_expression())

        self._expect_token(TokenType.RIGHT_PAREN)  # consume ')'

        return ExpressionNode(
            node_type=NodeType.FUNCTION_CALL,
            value=function_name,
            children=arguments
        )

    def validate_ast(self, node: ExpressionNode) -> None:
        """
        Validate an AST for semantic correctness.

        Args:
            node: Root node of the AST to validate

        Raises:
            SyntaxError: If the AST contains semantic errors
        """
        if node is None:
            raise SyntaxError("Empty AST node")

        if node.node_type == NodeType.BINARY_OP:
            if not node.left or not node.right:
                raise SyntaxError(f"Binary operator '{node.operator}' missing operand(s)")
            if not node.operator:
                raise SyntaxError("Binary operator missing operator")

            # Recursively validate children
            self.validate_ast(node.left)
            self.validate_ast(node.right)

        elif node.node_type == NodeType.UNARY_OP:
            if not node.right:
                raise SyntaxError(f"Unary operator '{node.operator}' missing operand")
            if not node.operator:
                raise SyntaxError("Unary operator missing operator")

            # Recursively validate child
            self.validate_ast(node.right)

        elif node.node_type == NodeType.FUNCTION_CALL:
            if not node.value:
                raise SyntaxError("Function call missing function name")
            if node.children is None:
                node.children = []

            # Validate function arguments
            for arg in node.children:
                self.validate_ast(arg)

        elif node.node_type in (NodeType.NUMBER, NodeType.VARIABLE, NodeType.CONSTANT):
            if node.value is None:
                raise SyntaxError(f"{node.node_type.value} node missing value")

    def ast_to_string(self, node: ExpressionNode, indent: int = 0) -> str:
        """
        Convert AST to a readable string representation.

        Args:
            node: Root node of the AST
            indent: Current indentation level

        Returns:
            String representation of the AST
        """
        if node is None:
            return "None"

        spaces = "  " * indent
        result = f"{spaces}{node.node_type.value}"

        if node.value is not None:
            result += f": {node.value}"

        if node.operator:
            result += f" ({node.operator})"

        result += "\n"

        # Add children
        if node.left:
            result += f"{spaces}├─ Left:\n{self.ast_to_string(node.left, indent + 1)}"

        if node.right:
            result += f"{spaces}├─ Right:\n{self.ast_to_string(node.right, indent + 1)}"

        if node.children:
            result += f"{spaces}├─ Children:\n"
            for i, child in enumerate(node.children):
                prefix = "└─" if i == len(node.children) - 1 else "├─"
                result += f"{spaces}  {prefix} Arg {i}:\n{self.ast_to_string(child, indent + 2)}"

        return result

    def __str__(self) -> str:
        """String representation of the parser."""
        return f"Parser(position={self.position}, current_token={self.current_token})"