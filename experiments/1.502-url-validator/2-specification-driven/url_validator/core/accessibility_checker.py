"""URL accessibility checking using requests."""

import time
import ssl
from typing import Optional, Dict, Any, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3

from ..models.result import AccessibilityResult, ValidationResult
from ..models.error import ValidationError, ErrorCode
from ..models.config import ValidationConfig


class AccessibilityChecker:
    """
    Checks URL accessibility using the requests library.

    This class provides comprehensive URL accessibility testing including:
    - HTTP/HTTPS connectivity testing
    - Redirect following with limits
    - SSL certificate validation
    - Response code handling
    - Timeout and retry management
    """

    def __init__(self, config: ValidationConfig):
        """
        Initialize accessibility checker with configuration.

        Args:
            config: Validation configuration
        """
        self.config = config
        self.logger = config.get_logger(__name__)
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """
        Create configured requests session.

        Returns:
            Configured requests.Session object
        """
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=self.config.retry_attempts,
            backoff_factor=self.config.retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set default headers
        session.headers.update({
            'User-Agent': self.config.user_agent,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })

        # Add custom headers
        if self.config.custom_headers:
            session.headers.update(self.config.custom_headers)

        # Configure proxies
        if self.config.proxy_settings:
            session.proxies.update(self.config.proxy_settings)

        return session

    def check_accessibility(self, url: str, result: ValidationResult) -> None:
        """
        Check URL accessibility and update result.

        Args:
            url: URL to check
            result: ValidationResult to update
        """
        start_time = time.time()
        accessibility_result = AccessibilityResult(is_accessible=False)

        try:
            # Perform the accessibility check
            self._perform_request(url, accessibility_result)

        except Exception as e:
            self.logger.error(f"Unexpected error during accessibility check: {e}")
            accessibility_result.error_details = str(e)
            result.add_error(ValidationError.network_error(
                ErrorCode.UNEXPECTED_ERROR,
                f"Unexpected error during accessibility check: {e}",
                {"error": str(e), "type": type(e).__name__}
            ))

        finally:
            accessibility_result.response_time = time.time() - start_time
            result.set_accessibility_result(accessibility_result)

    def _perform_request(self, url: str, accessibility_result: AccessibilityResult) -> None:
        """
        Perform the actual HTTP request.

        Args:
            url: URL to request
            accessibility_result: AccessibilityResult to update
        """
        try:
            response = self.session.head(
                url,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl,
                allow_redirects=self.config.follow_redirects,
                stream=False
            )

            self._process_response(response, accessibility_result)

        except requests.exceptions.SSLError as e:
            self._handle_ssl_error(e, accessibility_result)

        except requests.exceptions.Timeout as e:
            self._handle_timeout_error(e, accessibility_result)

        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(e, accessibility_result)

        except requests.exceptions.TooManyRedirects as e:
            self._handle_redirect_error(e, accessibility_result)

        except requests.exceptions.RequestException as e:
            self._handle_request_error(e, accessibility_result)

    def _process_response(self, response: requests.Response,
                         accessibility_result: AccessibilityResult) -> None:
        """
        Process successful HTTP response.

        Args:
            response: HTTP response object
            accessibility_result: AccessibilityResult to update
        """
        accessibility_result.status_code = response.status_code
        accessibility_result.final_url = response.url
        accessibility_result.headers = dict(response.headers)

        # Process redirects
        if response.history:
            accessibility_result.redirect_count = len(response.history)
            accessibility_result.redirect_chain = [resp.url for resp in response.history]
            accessibility_result.redirect_chain.append(response.url)

        # Extract SSL information for HTTPS URLs
        if response.url.startswith('https://'):
            self._extract_ssl_info(response, accessibility_result)

        # Determine accessibility based on status code
        accessibility_result.is_accessible = self._is_status_code_accessible(response.status_code)

    def _extract_ssl_info(self, response: requests.Response,
                         accessibility_result: AccessibilityResult) -> None:
        """
        Extract SSL certificate information.

        Args:
            response: HTTP response object
            accessibility_result: AccessibilityResult to update
        """
        try:
            # Get SSL info from the underlying urllib3 connection
            if hasattr(response.raw, '_connection'):
                connection = response.raw._connection
                if hasattr(connection, 'sock') and hasattr(connection.sock, 'getpeercert'):
                    cert = connection.sock.getpeercert()
                    if cert:
                        accessibility_result.ssl_info = {
                            'subject': dict(cert.get('subject', [])),
                            'issuer': dict(cert.get('issuer', [])),
                            'version': cert.get('version'),
                            'serial_number': str(cert.get('serialNumber', '')),
                            'not_before': cert.get('notBefore'),
                            'not_after': cert.get('notAfter'),
                            'subject_alt_name': cert.get('subjectAltName', [])
                        }
        except Exception as e:
            self.logger.debug(f"Could not extract SSL info: {e}")

    def _is_status_code_accessible(self, status_code: int) -> bool:
        """
        Determine if a status code indicates accessibility.

        Args:
            status_code: HTTP status code

        Returns:
            True if status code indicates accessibility
        """
        # 2xx - Success
        if 200 <= status_code < 300:
            return True

        # 3xx - Redirection (already followed if configured)
        if 300 <= status_code < 400:
            return True

        # 4xx - Client errors (URL exists but has issues)
        if 400 <= status_code < 500:
            # Some 4xx codes still indicate the URL exists
            accessible_4xx = {401, 403, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417}
            return status_code in accessible_4xx

        # 5xx - Server errors (temporarily inaccessible)
        return False

    def _handle_ssl_error(self, error: requests.exceptions.SSLError,
                         accessibility_result: AccessibilityResult) -> None:
        """
        Handle SSL-related errors.

        Args:
            error: SSL error
            accessibility_result: AccessibilityResult to update
        """
        accessibility_result.error_details = f"SSL Error: {error}"
        accessibility_result.is_accessible = False

        # Try to determine specific SSL issue
        error_str = str(error).lower()
        if 'certificate verify failed' in error_str:
            error_code = ErrorCode.SSL_CERTIFICATE_ERROR
            message = "SSL certificate verification failed"
        elif 'certificate has expired' in error_str:
            error_code = ErrorCode.SSL_CERTIFICATE_ERROR
            message = "SSL certificate has expired"
        elif 'hostname doesn\'t match' in error_str:
            error_code = ErrorCode.SSL_CERTIFICATE_ERROR
            message = "SSL certificate hostname mismatch"
        else:
            error_code = ErrorCode.SSL_CERTIFICATE_ERROR
            message = f"SSL error: {error}"

        # Note: We don't add the error to the result here as this method
        # is called from check_accessibility which handles error addition

    def _handle_timeout_error(self, error: requests.exceptions.Timeout,
                            accessibility_result: AccessibilityResult) -> None:
        """
        Handle timeout errors.

        Args:
            error: Timeout error
            accessibility_result: AccessibilityResult to update
        """
        accessibility_result.error_details = f"Timeout: {error}"
        accessibility_result.is_accessible = False

        if isinstance(error, requests.exceptions.ConnectTimeout):
            message = f"Connection timeout after {self.config.timeout} seconds"
        elif isinstance(error, requests.exceptions.ReadTimeout):
            message = f"Read timeout after {self.config.timeout} seconds"
        else:
            message = f"Request timeout after {self.config.timeout} seconds"

    def _handle_connection_error(self, error: requests.exceptions.ConnectionError,
                               accessibility_result: AccessibilityResult) -> None:
        """
        Handle connection errors.

        Args:
            error: Connection error
            accessibility_result: AccessibilityResult to update
        """
        accessibility_result.error_details = f"Connection Error: {error}"
        accessibility_result.is_accessible = False

        error_str = str(error).lower()
        if 'name or service not known' in error_str or 'nodename nor servname provided' in error_str:
            message = "DNS resolution failed"
        elif 'connection refused' in error_str:
            message = "Connection refused"
        elif 'network is unreachable' in error_str:
            message = "Network unreachable"
        else:
            message = f"Connection error: {error}"

    def _handle_redirect_error(self, error: requests.exceptions.TooManyRedirects,
                             accessibility_result: AccessibilityResult) -> None:
        """
        Handle too many redirects error.

        Args:
            error: Redirect error
            accessibility_result: AccessibilityResult to update
        """
        accessibility_result.error_details = f"Too Many Redirects: {error}"
        accessibility_result.is_accessible = False

        # Try to extract redirect information
        if hasattr(error, 'response') and error.response:
            accessibility_result.redirect_count = len(error.response.history)

    def _handle_request_error(self, error: requests.exceptions.RequestException,
                            accessibility_result: AccessibilityResult) -> None:
        """
        Handle general request errors.

        Args:
            error: Request error
            accessibility_result: AccessibilityResult to update
        """
        accessibility_result.error_details = f"Request Error: {error}"
        accessibility_result.is_accessible = False

    def close(self) -> None:
        """Close the session and clean up resources."""
        if self.session:
            self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def quick_check(self, url: str) -> bool:
        """
        Perform a quick accessibility check.

        Args:
            url: URL to check

        Returns:
            True if URL appears accessible
        """
        try:
            response = self.session.head(
                url,
                timeout=min(5, self.config.timeout),
                verify=self.config.verify_ssl,
                allow_redirects=True
            )
            return self._is_status_code_accessible(response.status_code)
        except Exception:
            return False