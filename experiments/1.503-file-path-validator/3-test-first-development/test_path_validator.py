import unittest
from path_validator import PathValidator


class TestPathValidator(unittest.TestCase):

    def setUp(self):
        self.validator = PathValidator()

    def test_valid_string_path(self):
        """Test that a simple string path is considered valid."""
        result = self.validator.is_valid("/home/user/document.txt")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()