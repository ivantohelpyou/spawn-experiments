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

    def test_normalize_path(self):
        """Test that paths are correctly normalized."""
        # Test path with redundant separators
        result = self.validator.normalize("./test/../test_path_validator.py")
        self.assertEqual(result, "test_path_validator.py")

        # Test path with double dots
        result = self.validator.normalize("/home/user/../user/file.txt")
        self.assertEqual(result, "/home/user/file.txt")

    def test_pathlib_integration(self):
        """Test that pathlib.Path objects are handled correctly."""
        from pathlib import Path

        # Test with pathlib.Path object
        path_obj = Path("test_path_validator.py")
        result = self.validator.is_valid_pathlib(path_obj)
        self.assertTrue(result)

        # Test pathlib-based existence check
        result = self.validator.exists_pathlib(path_obj)
        self.assertTrue(result)

    def test_get_parent_directory(self):
        """Test getting parent directory using pathlib."""
        result = self.validator.get_parent("/home/user/documents/file.txt")
        self.assertEqual(result, "/home/user/documents")

    def test_get_file_extension(self):
        """Test getting file extension using pathlib."""
        result = self.validator.get_extension("test_file.py")
        self.assertEqual(result, ".py")

        result = self.validator.get_extension("file_without_extension")
        self.assertEqual(result, "")


if __name__ == '__main__':
    unittest.main()