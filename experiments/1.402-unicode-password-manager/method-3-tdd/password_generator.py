"""
Password generator implementation - TDD Cycle 5 GREEN phase
Minimal implementation to make tests pass
"""

import secrets
import string
import math

class PasswordGenerator:
    """Secure password generator with Unicode support (TDD Cycle 5)"""

    def __init__(self):
        # Basic character sets
        self.ascii_chars = string.ascii_letters + string.digits + "!@#$%^&*"

        # Unicode character sets
        self.unicode_symbols = "αβγδεζηθικλμνξοπρστυφχψω"  # Greek
        self.unicode_symbols += "àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ"  # Accented
        self.unicode_symbols += "∀∂∃∄∅∆∇∈∉∋∌∍∎∏∐∑−∓∔∕∖∗"  # Math symbols

        self.emoji_chars = "🔐🗝️🔒🔓🔑⚡💪🎯🛡️⚔️🏆✨💎🔥"

    def generate(self, length: int, include_unicode: bool = False) -> str:
        """Generate password of specified length"""
        if include_unicode:
            charset = self.ascii_chars + self.unicode_symbols
        else:
            charset = self.ascii_chars

        return ''.join(secrets.choice(charset) for _ in range(length))

    def generate_emoji(self, length: int) -> str:
        """Generate password using emoji characters"""
        return ''.join(secrets.choice(self.emoji_chars) for _ in range(length))

    def calculate_entropy(self, password: str) -> float:
        """Calculate password entropy in bits"""
        if not password:
            return 0.0

        # Estimate character set size based on characters used
        charset_size = 0

        if any(c in string.ascii_lowercase for c in password):
            charset_size += 26
        if any(c in string.ascii_uppercase for c in password):
            charset_size += 26
        if any(c in string.digits for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += len(string.punctuation)

        # Check for Unicode characters
        if any(ord(c) > 127 for c in password):
            charset_size += 1000  # Rough estimate for Unicode

        if charset_size == 0:
            return 0.0

        # Entropy = log2(charset_size^length)
        return len(password) * math.log2(charset_size)

    def get_strength(self, password: str) -> float:
        """Get password strength score (0-100)"""
        if not password:
            return 0.0

        score = 0

        # Length component
        score += min(len(password) * 4, 40)  # Max 40 points for length

        # Character diversity
        if any(c in string.ascii_lowercase for c in password):
            score += 10
        if any(c in string.ascii_uppercase for c in password):
            score += 10
        if any(c in string.digits for c in password):
            score += 10
        if any(c in string.punctuation for c in password):
            score += 10

        # Unicode bonus
        if any(ord(c) > 127 for c in password):
            score += 20  # Bonus for Unicode

        return min(score, 100)  # Cap at 100