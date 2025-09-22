import unittest
from date_validator import validate_date


class TestDateValidator(unittest.TestCase):

    def test_validate_date_function_exists(self):
        """Test that validate_date function exists and can be called"""
        result = validate_date("01/01/2000")
        self.assertIsInstance(result, bool)


if __name__ == '__main__':
    unittest.main()