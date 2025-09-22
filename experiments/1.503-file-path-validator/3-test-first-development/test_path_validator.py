import unittest
from path_validator import PathValidator


class TestPathValidator(unittest.TestCase):

    def setUp(self):
        self.validator = PathValidator()

    def test_valid_string_path(self):
        """Test that a simple string path is considered valid."""
        result = self.validator.is_valid("/home/user/document.txt")
        self.assertTrue(result)

    def test_invalid_path_returns_false(self):
        """Test that invalid paths return False."""
        result = self.validator.is_valid("")
        self.assertFalse(result)

        result = self.validator.is_valid(None)
        self.assertFalse(result)

    def test_is_absolute_path(self):
        """Test that absolute paths are correctly identified."""
        result = self.validator.is_absolute("/home/user/file.txt")
        self.assertTrue(result)

        result = self.validator.is_absolute("relative/path.txt")
        self.assertFalse(result)

    def test_is_relative_path(self):
        """Test that relative paths are correctly identified."""
        result = self.validator.is_relative("relative/path.txt")
        self.assertTrue(result)

        result = self.validator.is_relative("/absolute/path.txt")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()