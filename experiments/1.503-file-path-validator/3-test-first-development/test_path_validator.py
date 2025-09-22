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

    def test_file_exists(self):
        """Test that file existence is correctly checked."""
        # Test with an existing file (the test file itself)
        result = self.validator.exists("test_path_validator.py")
        self.assertTrue(result)

        # Test with a non-existing file
        result = self.validator.exists("non_existent_file.txt")
        self.assertFalse(result)

    def test_is_file(self):
        """Test that files are correctly identified."""
        # Test with an existing file
        result = self.validator.is_file("test_path_validator.py")
        self.assertTrue(result)

        # Test with a directory (current directory)
        result = self.validator.is_file(".")
        self.assertFalse(result)

    def test_is_directory(self):
        """Test that directories are correctly identified."""
        # Test with current directory
        result = self.validator.is_directory(".")
        self.assertTrue(result)

        # Test with a file
        result = self.validator.is_directory("test_path_validator.py")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()