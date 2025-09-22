"""
Progress indicators and colored output utilities.
Provides visual feedback for long-running operations.
"""

import sys
import time
from typing import Optional


class ProgressBar:
    """Simple progress bar for batch operations."""

    def __init__(self, total: int, width: int = 50, show_percentage: bool = True):
        self.total = total
        self.width = width
        self.show_percentage = show_percentage
        self.current = 0
        self.start_time = time.time()

    def update(self, increment: int = 1):
        """Update progress bar."""
        self.current += increment
        self._draw()

    def set_progress(self, current: int):
        """Set absolute progress."""
        self.current = current
        self._draw()

    def _draw(self):
        """Draw the progress bar."""
        if self.total == 0:
            return

        percentage = min(100, (self.current / self.total) * 100)
        filled_width = int((self.current / self.total) * self.width)
        bar = '█' * filled_width + '░' * (self.width - filled_width)

        elapsed = time.time() - self.start_time
        rate = self.current / max(elapsed, 0.001)  # Avoid division by zero

        if self.show_percentage:
            sys.stdout.write(f'\rProgress: [{bar}] {percentage:.1f}% ({self.current}/{self.total}) - {elapsed:.1f}s')
        else:
            sys.stdout.write(f'\rProgress: [{bar}] ({self.current}/{self.total}) - {elapsed:.1f}s')

        sys.stdout.flush()

        if self.current >= self.total:
            sys.stdout.write('\n')

    def finish(self):
        """Complete the progress bar."""
        self.current = self.total
        self._draw()


class ColoredOutput:
    """Utility for colored terminal output."""

    COLORS = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'reset': '\033[0m'
    }

    STYLES = {
        'bold': '\033[1m',
        'dim': '\033[2m',
        'underline': '\033[4m',
        'reset': '\033[0m'
    }

    def __init__(self, use_colors: bool = None):
        """
        Initialize colored output.

        Args:
            use_colors: Whether to use colors. If None, auto-detect based on terminal.
        """
        if use_colors is None:
            # Auto-detect color support
            self.use_colors = self._supports_color()
        else:
            self.use_colors = use_colors

    def _supports_color(self) -> bool:
        """Detect if the terminal supports color."""
        # Check if we're in a TTY and not redirected
        if not sys.stdout.isatty():
            return False

        # Check common environment variables
        term = sys.platform
        if term == 'win32':
            # Windows 10+ supports ANSI colors
            return True

        # Unix-like systems generally support colors
        return True

    def colorize(self, text: str, color: Optional[str] = None, style: Optional[str] = None) -> str:
        """
        Apply color and style to text.

        Args:
            text: Text to colorize
            color: Color name
            style: Style name (bold, dim, underline)

        Returns:
            Colored text string
        """
        if not self.use_colors:
            return text

        codes = []

        if color and color in self.COLORS:
            codes.append(self.COLORS[color])

        if style and style in self.STYLES:
            codes.append(self.STYLES[style])

        if codes:
            return f"{''.join(codes)}{text}{self.COLORS['reset']}"

        return text

    def success(self, text: str) -> str:
        """Format text as success (green)."""
        return self.colorize(text, 'bright_green')

    def error(self, text: str) -> str:
        """Format text as error (red)."""
        return self.colorize(text, 'bright_red')

    def warning(self, text: str) -> str:
        """Format text as warning (yellow)."""
        return self.colorize(text, 'bright_yellow')

    def info(self, text: str) -> str:
        """Format text as info (cyan)."""
        return self.colorize(text, 'bright_cyan')

    def bold(self, text: str) -> str:
        """Format text as bold."""
        return self.colorize(text, style='bold')

    def print_success(self, text: str):
        """Print success message."""
        print(self.success(text))

    def print_error(self, text: str):
        """Print error message."""
        print(self.error(text))

    def print_warning(self, text: str):
        """Print warning message."""
        print(self.warning(text))

    def print_info(self, text: str):
        """Print info message."""
        print(self.info(text))


# Global instances for convenience
colored = ColoredOutput()


def create_progress_bar(total: int, **kwargs) -> ProgressBar:
    """Create a progress bar instance."""
    return ProgressBar(total, **kwargs)


def disable_colors():
    """Disable colored output globally."""
    global colored
    colored.use_colors = False


def enable_colors():
    """Enable colored output globally."""
    global colored
    colored.use_colors = True