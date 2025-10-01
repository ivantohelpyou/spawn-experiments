import unittest
import json
from limerick_converter import LimerickConverter


class TestLimerickConverter(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.converter = LimerickConverter()

    def test_validate_limerick_structure_correct(self):
        """Test that a valid limerick structure passes validation."""
        valid_limerick = [
            "A programmer stayed up at night,",
            "Debugging code was their fight,",
            "Found one missing mark,",
            "A semicolon stark,",
            "Then slept with relief and delight."
        ]

        result = self.converter.validate_limerick_structure(valid_limerick)
        self.assertTrue(result['valid'])
        self.assertEqual(result['line_count'], 5)
        self.assertEqual(len(result['issues']), 0)

    def test_validate_limerick_structure_wrong_line_count(self):
        """Test that wrong line count fails validation."""
        invalid_limerick = [
            "A programmer stayed up at night,",
            "Debugging code was their fight,",
            "Found one missing mark,"
        ]

        result = self.converter.validate_limerick_structure(invalid_limerick)
        self.assertFalse(result['valid'])
        self.assertIn('Must have exactly 5 lines', str(result['issues']))


if __name__ == '__main__':
    unittest.main()
