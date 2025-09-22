"""
Test type checking for email validator.
"""

import unittest
from email_validator import is_valid_email


class TestTypeChecking(unittest.TestCase):
    """Test that the validator properly handles non-string inputs."""

    def test_non_string_input_raises_type_error(self):
        """Test that non-string inputs raise TypeError."""
        non_string_inputs = [
            123,
            None,
            [],
            {},
            True,
            False,
            12.34
        ]

        for input_value in non_string_inputs:
            with self.subTest(input_value=input_value):
                with self.assertRaises(TypeError):
                    is_valid_email(input_value)


if __name__ == "__main__":
    unittest.main()