"""
Best-of-breed validation components from Tier 1 experiments.

These validators represent the most efficient implementations from experiments 1.501-1.504:
- email_validator: Method 3 TDD from 1.501 (112 lines, robust)
- url_validator: Method 3 TDD from 1.502 (187 lines, clean)
- file_path_validator: Constrained injection from 1.503 (687 lines, rescued from over-engineering)
- date_validator: Method 4 V4.1 from 1.504 (98 lines, optimal)

Available for reuse in Tier 2+ experiments to study component discovery and integration patterns.
"""

from .email_validator import is_valid_email
from .url_validator import URLValidator
from .file_path_validator import is_valid_path
from .date_validator import validate_date

# Create convenience functions with consistent naming
def validate_email(email):
    return is_valid_email(email)

def validate_url(url):
    validator = URLValidator()
    return validator.is_valid(url)

def validate_file_path(path):
    return is_valid_path(path)

__all__ = [
    'validate_email',
    'validate_url',
    'validate_file_path',
    'validate_date',
    'is_valid_email',
    'URLValidator',
    'is_valid_path'
]