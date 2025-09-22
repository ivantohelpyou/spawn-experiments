from urllib.parse import urlparse
import requests


class URLValidator:
    """A URL validator that checks format and accessibility using urllib.parse and requests."""

    # Allowed URL schemes
    ALLOWED_SCHEMES = {'http', 'https'}

    # Default timeout for accessibility checks
    DEFAULT_TIMEOUT = 5

    def is_valid(self, url):
        """
        Check if a URL has valid format.

        Args:
            url (str): The URL to validate

        Returns:
            bool: True if URL has valid format, False otherwise
        """
        try:
            parsed = urlparse(url)
            # URL must have an allowed scheme and a network location
            return (parsed.scheme in self.ALLOWED_SCHEMES and
                   bool(parsed.netloc))
        except Exception:
            return False

    def is_accessible(self, url):
        """
        Check if a URL is accessible via HTTP request.

        Args:
            url (str): The URL to check accessibility

        Returns:
            bool: True if URL is accessible (status < 400), False otherwise
        """
        try:
            response = requests.head(url, timeout=self.DEFAULT_TIMEOUT)
            return response.status_code < 400
        except Exception:
            return False

    def validate_completely(self, url):
        """
        Perform both format validation and accessibility check.

        Args:
            url (str): The URL to validate completely

        Returns:
            dict: Dictionary with 'valid' and 'accessible' boolean keys
        """
        valid = self.is_valid(url)
        accessible = self.is_accessible(url) if valid else False

        return {
            'valid': valid,
            'accessible': accessible
        }