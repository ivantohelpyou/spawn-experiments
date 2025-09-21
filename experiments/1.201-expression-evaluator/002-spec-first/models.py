"""
Data models and enums for the Expression Evaluator system.

This module contains all the data structures used throughout the system
including tokens, AST nodes, and result objects.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union, List, Dict, Callable, Any
import time


class TokenType(Enum):
    """Enumeration of token types for lexical analysis."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    FUNCTION = "FUNCTION"
    VARIABLE = "VARIABLE"
    CONSTANT = "CONSTANT"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    COMMA = "COMMA"
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"


class NodeType(Enum):
    """Enumeration of AST node types."""
    NUMBER = "NUMBER"
    VARIABLE = "VARIABLE"
    CONSTANT = "CONSTANT"
    BINARY_OP = "BINARY_OP"
    UNARY_OP = "UNARY_OP"
    FUNCTION_CALL = "FUNCTION_CALL"


class OperatorType(Enum):
    """Enumeration of supported operators."""
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    POWER = "**"
    MODULO = "%"
    FLOOR_DIVIDE = "//"


@dataclass
class Token:
    """Represents a token in the expression."""
    type: TokenType
    value: str
    position: int

    def __str__(self) -> str:
        return f"Token({self.type.value}, '{self.value}', {self.position})"


@dataclass
class ExpressionNode:
    """Represents a node in the Abstract Syntax Tree."""
    node_type: NodeType
    value: Optional[Union[float, str]] = None
    left: Optional['ExpressionNode'] = None
    right: Optional['ExpressionNode'] = None
    children: Optional[List['ExpressionNode']] = None
    operator: Optional[str] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []

    def __str__(self) -> str:
        if self.node_type == NodeType.NUMBER:
            return f"Num({self.value})"
        elif self.node_type == NodeType.VARIABLE:
            return f"Var({self.value})"
        elif self.node_type == NodeType.CONSTANT:
            return f"Const({self.value})"
        elif self.node_type == NodeType.BINARY_OP:
            return f"BinOp({self.left} {self.operator} {self.right})"
        elif self.node_type == NodeType.UNARY_OP:
            return f"UnaryOp({self.operator} {self.right})"
        elif self.node_type == NodeType.FUNCTION_CALL:
            args = ", ".join(str(child) for child in self.children)
            return f"Func({self.value}({args}))"
        return f"Node({self.node_type})"


@dataclass
class VariableContext:
    """Context for variables, constants, and functions."""
    variables: Dict[str, float]
    constants: Dict[str, float]
    functions: Dict[str, Callable]

    def __init__(self):
        self.variables = {}
        self.constants = self._get_default_constants()
        self.functions = self._get_default_functions()

    def _get_default_constants(self) -> Dict[str, float]:
        """Get default mathematical constants."""
        import math
        return {
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau,
            'inf': math.inf,
        }

    def _get_default_functions(self) -> Dict[str, Callable]:
        """Get default mathematical functions."""
        import math
        return {
            # Basic functions
            'abs': abs,
            'round': round,
            'int': int,
            'float': float,

            # Trigonometric functions
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'atan2': math.atan2,
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,

            # Logarithmic functions
            'log': math.log,
            'log10': math.log10,
            'log2': math.log2,
            'ln': math.log,

            # Exponential and power functions
            'exp': math.exp,
            'sqrt': math.sqrt,
            'pow': pow,

            # Other mathematical functions
            'ceil': math.ceil,
            'floor': math.floor,
            'factorial': math.factorial,
            'degrees': math.degrees,
            'radians': math.radians,

            # Statistical functions
            'min': min,
            'max': max,
            'sum': sum,
        }

    def get_variable(self, name: str) -> float:
        """Get variable value."""
        if name in self.variables:
            return self.variables[name]
        elif name in self.constants:
            return self.constants[name]
        else:
            from .exceptions import VariableError
            raise VariableError(f"Undefined variable: {name}")

    def set_variable(self, name: str, value: float) -> None:
        """Set variable value."""
        self.variables[name] = value

    def get_function(self, name: str) -> Callable:
        """Get function by name."""
        if name in self.functions:
            return self.functions[name]
        else:
            from .exceptions import FunctionError
            raise FunctionError(f"Unknown function: {name}")


@dataclass
class EvaluationResult:
    """Result of expression evaluation."""
    value: Optional[float] = None
    success: bool = False
    error_message: Optional[str] = None
    execution_time: float = 0.0
    position: Optional[int] = None

    @classmethod
    def success_result(cls, value: float, execution_time: float = 0.0) -> 'EvaluationResult':
        """Create a successful evaluation result."""
        return cls(value=value, success=True, execution_time=execution_time)

    @classmethod
    def error_result(cls, error_message: str, position: Optional[int] = None, execution_time: float = 0.0) -> 'EvaluationResult':
        """Create an error evaluation result."""
        return cls(error_message=error_message, success=False, position=position, execution_time=execution_time)

    def __str__(self) -> str:
        if self.success:
            return f"Success: {self.value} (took {self.execution_time:.3f}s)"
        else:
            return f"Error: {self.error_message}"


@dataclass
class ValidationResult:
    """Result of expression validation."""
    valid: bool = False
    errors: List[str] = None
    warnings: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []

    @classmethod
    def valid_result(cls) -> 'ValidationResult':
        """Create a valid validation result."""
        return cls(valid=True)

    @classmethod
    def invalid_result(cls, errors: List[str], warnings: Optional[List[str]] = None) -> 'ValidationResult':
        """Create an invalid validation result."""
        return cls(valid=False, errors=errors, warnings=warnings or [])

    def __str__(self) -> str:
        if self.valid:
            return "Valid expression"
        else:
            result = f"Invalid expression: {'; '.join(self.errors)}"
            if self.warnings:
                result += f" (Warnings: {'; '.join(self.warnings)})"
            return result


@dataclass
class ErrorInfo:
    """Detailed error information."""
    code: str
    message: str
    position: Optional[int] = None
    suggestion: Optional[str] = None

    def __str__(self) -> str:
        result = f"{self.code}: {self.message}"
        if self.position is not None:
            result += f" at position {self.position}"
        if self.suggestion:
            result += f". Suggestion: {self.suggestion}"
        return result