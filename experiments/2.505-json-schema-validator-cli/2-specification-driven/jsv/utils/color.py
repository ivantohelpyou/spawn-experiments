"""Terminal color formatting utilities."""

import sys
from typing import Optional
from colorama import init, Fore, Back, Style


class ColorFormatter:
    """Handles colored terminal output with fallback for non-color terminals."""

    def __init__(self, use_color: Optional[bool] = None):
        """Initialize color formatter.

        Args:
            use_color: Whether to use colors. If None, auto-detect based on terminal.
        """
        # Initialize colorama for cross-platform support
        init(autoreset=True)

        if use_color is None:
            # Auto-detect color support
            self.use_color = self._supports_color()
        else:
            self.use_color = use_color

    def _supports_color(self) -> bool:
        """Check if terminal supports color output."""
        # Check if stdout is a TTY and not redirected
        if not sys.stdout.isatty():
            return False

        # Check for common environment variables that indicate color support
        term = sys.platform
        if term.startswith('win'):
            # Windows with colorama support
            return True

        # Unix-like systems
        import os
        term_env = os.environ.get('TERM', '').lower()
        return 'color' in term_env or term_env in ['xterm', 'xterm-256color', 'screen']

    def success(self, text: str) -> str:
        """Format text as success (green)."""
        if self.use_color:
            return f"{Fore.GREEN}{text}{Style.RESET_ALL}"
        return text

    def error(self, text: str) -> str:
        """Format text as error (red)."""
        if self.use_color:
            return f"{Fore.RED}{text}{Style.RESET_ALL}"
        return text

    def warning(self, text: str) -> str:
        """Format text as warning (yellow)."""
        if self.use_color:
            return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"
        return text

    def info(self, text: str) -> str:
        """Format text as info (blue)."""
        if self.use_color:
            return f"{Fore.BLUE}{text}{Style.RESET_ALL}"
        return text

    def bold(self, text: str) -> str:
        """Format text as bold."""
        if self.use_color:
            return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"
        return text

    def dim(self, text: str) -> str:
        """Format text as dim/faded."""
        if self.use_color:
            return f"{Style.DIM}{text}{Style.RESET_ALL}"
        return text

    def highlight(self, text: str) -> str:
        """Format text with background highlight."""
        if self.use_color:
            return f"{Back.YELLOW}{Fore.BLACK}{text}{Style.RESET_ALL}"
        return f"[{text}]"