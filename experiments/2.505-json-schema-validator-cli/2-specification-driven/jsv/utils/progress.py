"""Progress tracking utilities for batch operations."""

from typing import Optional, Any

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    # Create a simple fallback class
    class tqdm:
        def __init__(self, total=None, desc="", unit="", unit_scale=True, leave=True):
            self.total = total
            self.desc = desc
            self.current = 0

        def update(self, n=1):
            self.current += n
            if self.total:
                print(f"\r{self.desc}: {self.current}/{self.total}", end="", flush=True)

        def set_description(self, desc):
            self.desc = desc

        def set_postfix(self, **kwargs):
            pass

        def close(self):
            if self.total:
                print()  # New line


class ProgressTracker:
    """Manages progress indicators for batch operations."""

    def __init__(self, total: int, description: str = "Processing", show_progress: bool = True):
        """Initialize progress tracker.

        Args:
            total: Total number of items to process
            description: Description to show with progress bar
            show_progress: Whether to show progress bar
        """
        self.total = total
        self.description = description
        self.show_progress = show_progress
        self._progress_bar: Optional[tqdm] = None

    def __enter__(self) -> 'ProgressTracker':
        """Enter context manager."""
        if self.show_progress and self.total > 1:
            self._progress_bar = tqdm(
                total=self.total,
                desc=self.description,
                unit="file",
                unit_scale=True,
                leave=True
            )
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager."""
        if self._progress_bar:
            self._progress_bar.close()

    def update(self, count: int = 1, description: Optional[str] = None) -> None:
        """Update progress.

        Args:
            count: Number of items completed
            description: Optional description update
        """
        if self._progress_bar:
            if description:
                self._progress_bar.set_description(description)
            self._progress_bar.update(count)

    def set_postfix(self, **kwargs: Any) -> None:
        """Set postfix information.

        Args:
            **kwargs: Key-value pairs to display
        """
        if self._progress_bar:
            self._progress_bar.set_postfix(**kwargs)