import unittest
from email_validator import validate_email


class TestEmailValidator(unittest.TestCase):

    def test_simple_valid_email(self):
        """Test the most basic valid email format"""
        result = validate_email("test@example.com")
        self.assertTrue(result)

    def test_email_without_at_symbol(self):
        """Test invalid email without @ symbol"""
        result = validate_email("testexample.com")
        self.assertFalse(result)

    def test_email_with_multiple_at_symbols(self):
        """Test invalid email with multiple @ symbols"""
        result = validate_email("test@@example.com")
        self.assertFalse(result)

    def test_empty_local_part(self):
        """Test invalid email with empty local part"""
        result = validate_email("@example.com")
        self.assertFalse(result)

    def test_empty_domain_part(self):
        """Test invalid email with empty domain part"""
        result = validate_email("test@")
        self.assertFalse(result)

    def test_domain_without_dot(self):
        """Test invalid domain without dot"""
        result = validate_email("test@example")
        self.assertFalse(result)

    def test_invalid_characters_in_local(self):
        """Test invalid characters in local part"""
        result = validate_email("test$@example.com")
        self.assertFalse(result)

    def test_local_starts_with_dot(self):
        """Test invalid local part starting with dot"""
        result = validate_email(".test@example.com")
        self.assertFalse(result)

    def test_local_ends_with_dot(self):
        """Test invalid local part ending with dot"""
        result = validate_email("test.@example.com")
        self.assertFalse(result)

    def test_local_consecutive_dots(self):
        """Test invalid local part with consecutive dots"""
        result = validate_email("te..st@example.com")
        self.assertFalse(result)

    def test_invalid_domain_characters(self):
        """Test invalid characters in domain"""
        result = validate_email("test@exam_ple.com")
        self.assertFalse(result)

    def test_domain_label_too_short(self):
        """Test domain with too short TLD"""
        result = validate_email("test@example.c")
        self.assertFalse(result)

    def test_email_too_long(self):
        """Test email that exceeds 254 character limit"""
        long_local = 'a' * 250
        result = validate_email(f"{long_local}@example.com")
        self.assertFalse(result)

    def test_local_part_too_long(self):
        """Test local part exceeds 64 character limit"""
        long_local = 'a' * 65
        result = validate_email(f"{long_local}@example.com")
        self.assertFalse(result)

    def test_valid_email_with_numbers(self):
        """Test valid email with numbers"""
        result = validate_email("user123@example.com")
        self.assertTrue(result)

    def test_valid_email_with_dots(self):
        """Test valid email with dots in local part"""
        result = validate_email("user.name@example.com")
        self.assertTrue(result)

    def test_valid_email_with_plus(self):
        """Test valid email with plus in local part"""
        result = validate_email("user+tag@example.com")
        self.assertTrue(result)

    def test_valid_email_with_hyphen_in_domain(self):
        """Test valid email with hyphen in domain"""
        result = validate_email("user@sub-domain.example.com")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()