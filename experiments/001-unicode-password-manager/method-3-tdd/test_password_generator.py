"""
TDD Cycle 5: Password Generation
RED phase - write failing tests for password generation
"""

import unittest

class TestPasswordGenerator(unittest.TestCase):
    """TDD Cycle 5: Secure password generation with Unicode"""

    def test_generate_basic_password(self):
        """RED: Generate a basic password of specified length"""
        from password_generator import PasswordGenerator

        generator = PasswordGenerator()
        password = generator.generate(12)

        self.assertEqual(len(password), 12)
        self.assertIsInstance(password, str)

    def test_generate_unicode_password(self):
        """RED: Generate password with Unicode characters"""
        from password_generator import PasswordGenerator

        generator = PasswordGenerator()
        password = generator.generate(10, include_unicode=True)

        self.assertEqual(len(password), 10)
        # Should contain at least one Unicode character (> ASCII 127)
        self.assertTrue(any(ord(c) > 127 for c in password))

    def test_generate_emoji_password(self):
        """RED: Generate password with emoji characters"""
        from password_generator import PasswordGenerator

        generator = PasswordGenerator()
        password = generator.generate_emoji(8)

        self.assertEqual(len(password), 8)
        # Should contain emoji characters
        self.assertTrue(any(ord(c) > 1000 for c in password))

    def test_password_entropy(self):
        """RED: Calculate password entropy"""
        from password_generator import PasswordGenerator

        generator = PasswordGenerator()
        password = "abc123"
        entropy = generator.calculate_entropy(password)

        self.assertGreater(entropy, 0)
        self.assertIsInstance(entropy, float)

    def test_password_strength_unicode(self):
        """RED: Password strength should account for Unicode"""
        from password_generator import PasswordGenerator

        generator = PasswordGenerator()

        weak_password = "abc123"
        strong_password = "café🔐αβγ123"

        weak_strength = generator.get_strength(weak_password)
        strong_strength = generator.get_strength(strong_password)

        # Unicode password should be stronger
        self.assertGreater(strong_strength, weak_strength)

if __name__ == '__main__':
    unittest.main()