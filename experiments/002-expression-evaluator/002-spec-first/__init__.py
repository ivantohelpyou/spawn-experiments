"""
Expression Evaluator - Specification-First Implementation

A comprehensive mathematical expression parsing and evaluation system
built according to detailed specifications.
"""

__version__ = "1.0.0"
__author__ = "Expression Evaluator Team"
__description__ = "Mathematical expression parser and evaluator"

from .expression_manager import ExpressionManager
from .models import EvaluationResult, ValidationResult
from .exceptions import ExpressionError, SyntaxError, EvaluationError

__all__ = [
    'ExpressionManager',
    'EvaluationResult',
    'ValidationResult',
    'ExpressionError',
    'SyntaxError',
    'EvaluationError'
]