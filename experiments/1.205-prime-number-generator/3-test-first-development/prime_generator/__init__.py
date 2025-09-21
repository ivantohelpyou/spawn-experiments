"""Prime Number Generator Package

A library for generating and validating prime numbers using Test-Driven Development.
"""

__version__ = "1.0.0"
__author__ = "TDD Prime Generator"

from .core import PrimeChecker
from .generator import PrimeGenerator
from .exceptions import PrimeGeneratorError, InvalidInputError, ComputationError

__all__ = [
    'PrimeChecker',
    'PrimeGenerator',
    'PrimeGeneratorError',
    'InvalidInputError',
    'ComputationError'
]