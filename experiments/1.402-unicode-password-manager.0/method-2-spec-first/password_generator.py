"""
Secure password generator with Unicode support
Implements SPEC-4.2 and related requirements
"""

import secrets
import string
from enum import Enum
from typing import Set
import unicodedata

class CharacterSet(Enum):
    """Character set options for password generation"""
    ASCII_BASIC = "ascii_basic"
    ASCII_EXTENDED = "ascii_extended"
    UNICODE_SYMBOLS = "unicode_symbols"
    UNICODE_MIXED = "unicode_mixed"
    EMOJI_ONLY = "emoji_only"

class PasswordGenerator:
    """
    Cryptographically secure password generator with Unicode support
    Follows SPEC requirements for password generation
    """

    def __init__(self):
        self._character_sets = {
            CharacterSet.ASCII_BASIC: self._get_ascii_basic(),
            CharacterSet.ASCII_EXTENDED: self._get_ascii_extended(),
            CharacterSet.UNICODE_SYMBOLS: self._get_unicode_symbols(),
            CharacterSet.UNICODE_MIXED: self._get_unicode_mixed(),
            CharacterSet.EMOJI_ONLY: self._get_emoji_set()
        }

    def _get_ascii_basic(self) -> str:
        """Basic ASCII: letters and numbers only"""
        return string.ascii_letters + string.digits

    def _get_ascii_extended(self) -> str:
        """Extended ASCII: letters, numbers, and symbols"""
        return string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def _get_unicode_symbols(self) -> str:
        """Unicode symbols for enhanced security"""
        symbols = [
            # Mathematical symbols
            "∀∂∃∄∅∆∇∈∉∋∌∍∎∏∐∑−∓∔∕∖∗∘∙√∛∜∝∞∟∠∡∢∣∤∥∦∧∨∩∪∫∬∭∮∯∰∱∲∳∴∵∶∷∸∹∺∻∼∽∾∿",

            # Currency symbols
            "₠₡₢₣₤₥₦₧₨₩₪₫€₭₮₯₰₱₲₳₴₵₶₷₸₹₺₻₼₽₾₿",

            # Geometric shapes
            "■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯▰▱▲△▴▵▶▷▸▹►▻▼▽▾▿◀◁◂◃◄◅◆◇◈◉◊○◌◍◎●◐◑◒◓◔◕◖◗◘◙◚◛◜◝◞◟◠◡◢◣◤◥◦◧◨◩◪◫◬◭◮◯",

            # Box drawing
            "─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╌╍╎╏═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╭╮╯╰╱╲╳╴╵╶╷╸╹╺╻╼╽╾╿",
        ]
        return "".join(symbols)

    def _get_unicode_mixed(self) -> str:
        """Mixed ASCII and Unicode for balanced security"""
        return (self._get_ascii_extended() +
                "αβγδεζηθικλμνξοπρστυφχψω" +
                "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ" +
                "àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ" +
                "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸ" +
                "🔐🗝️🔒🔓🔑⚡💪🎯🛡️⚔️🏆✨💎🔥")

    def _get_emoji_set(self) -> str:
        """Emoji-only passwords for fun"""
        return ("🔐🗝️🔒🔓🔑⚡💪🎯🛡️⚔️🏆✨💎🔥" +
                "😀😃😄😁😆😅😂🤣😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🤩🥳😏😒😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🤭🤫🤥😶😐😑😬🙄😯😦😧😮😲🥱😴🤤😪😵🤐🥴🤢🤮🤧😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀☠️👽👾🤖🎃😺😸😹😻😼😽🙀😿😾")

    def generate_password(
        self,
        length: int = 16,
        charset: CharacterSet = CharacterSet.UNICODE_MIXED,
        exclude_similar: bool = True
    ) -> str:
        """
        Generate cryptographically secure password
        Implements SPEC-4.2
        """
        # Validate length (RULE extends to 8-128 characters)
        if not (8 <= length <= 128):
            raise ValueError("Password length must be between 8 and 128 characters")

        # Get character set
        chars = self._character_sets[charset]

        # Exclude visually similar characters if requested
        if exclude_similar:
            chars = self._exclude_similar_characters(chars)

        if not chars:
            raise ValueError("Character set is empty after filtering")

        # Generate password using cryptographically secure random
        # SPEC-1.3.1: cryptographically secure
        password = ""

        # For emoji passwords, we need special handling
        if charset == CharacterSet.EMOJI_ONLY:
            # Emoji can be multi-byte, so we need to handle them specially
            emoji_list = list(chars)
            for _ in range(length):
                password += secrets.choice(emoji_list)
        else:
            # For other character sets, use standard approach
            for _ in range(length):
                password += secrets.choice(chars)

        # Validate that we got the requested visual length
        # This is approximate for complex Unicode
        visual_length = self._get_visual_length(password)
        if abs(visual_length - length) > length * 0.1:  # Allow 10% variance
            # If length is significantly off, regenerate
            return self.generate_password(length, charset, exclude_similar)

        return password

    def _exclude_similar_characters(self, chars: str) -> str:
        """
        Remove visually similar characters to prevent confusion
        Examples: 0/O, 1/l/I, etc.
        """
        similar_groups = [
            "0O",  # Zero and capital O
            "1lI|",  # One, lowercase L, capital I, pipe
            "2Z",  # Two and Z in some fonts
            "5S",  # Five and S
            "6G",  # Six and G
            "8B",  # Eight and B
            "9g",  # Nine and g
        ]

        filtered_chars = ""
        for char in chars:
            # Keep character if it's not in any similar group
            # (or keep only the first character from each group)
            should_keep = True
            for group in similar_groups:
                if char in group and group.index(char) > 0:
                    should_keep = False
                    break
            if should_keep:
                filtered_chars += char

        return filtered_chars

    def _get_visual_length(self, text: str) -> int:
        """
        Approximate visual character count
        This is simplified - production would use proper grapheme counting
        """
        # Remove combining characters
        without_combining = ''.join(c for c in text
                                  if unicodedata.category(c) != 'Mn')
        return len(without_combining)

    def get_password_strength_indicator(self, password: str) -> str:
        """
        Return Unicode visual strength indicator
        Implements UI-9.1.2
        """
        if len(password) < 8:
            return "🔴 Weak"
        elif len(password) < 12:
            return "🟡 Medium"
        elif len(password) < 16:
            return "🟢 Strong"
        else:
            return "🟢 Very Strong"

    def analyze_password_entropy(self, password: str) -> float:
        """Calculate approximate password entropy"""
        if not password:
            return 0.0

        # Count unique characters
        unique_chars = len(set(password))

        # Estimate charset size based on characters used
        charset_size = 0
        if any(c in string.ascii_lowercase for c in password):
            charset_size += 26
        if any(c in string.ascii_uppercase for c in password):
            charset_size += 26
        if any(c in string.digits for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += len(string.punctuation)

        # For Unicode characters, estimate larger charset
        if any(ord(c) > 127 for c in password):
            charset_size += 1000  # Rough estimate for Unicode

        # Entropy = log2(charset_size^length)
        import math
        if charset_size > 0:
            return len(password) * math.log2(charset_size)
        return 0.0