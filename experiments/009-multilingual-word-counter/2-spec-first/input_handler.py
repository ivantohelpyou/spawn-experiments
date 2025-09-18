"""
Input handling module for the Multilingual Word Counter.
Handles various input sources: files, URLs, stdin.
"""

import sys
import os
import requests
from typing import Optional, Dict, Any
from urllib.parse import urlparse

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


class InputHandler:
    """Handles various input sources for text processing."""

    def __init__(self, timeout: int = 30):
        """Initialize the input handler."""
        self.timeout = timeout

    def read_file(self, file_path: str) -> str:
        """
        Read text from a file.

        Args:
            file_path: Path to the file

        Returns:
            Text content of the file

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
            ValueError: If file type is not supported
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_extension = os.path.splitext(file_path)[1].lower()

        try:
            if file_extension == '.txt':
                return self._read_text_file(file_path)
            elif file_extension == '.docx':
                return self._read_docx_file(file_path)
            elif file_extension == '.pdf':
                return self._read_pdf_file(file_path)
            elif file_extension in ['.md', '.markdown']:
                return self._read_text_file(file_path)
            elif file_extension in ['.py', '.js', '.html', '.css', '.json', '.xml']:
                return self._read_text_file(file_path)
            else:
                # Try to read as text file
                return self._read_text_file(file_path)
        except Exception as e:
            raise IOError(f"Error reading file {file_path}: {str(e)}")

    def fetch_url(self, url: str) -> str:
        """
        Fetch text content from a URL.

        Args:
            url: URL to fetch

        Returns:
            Text content from the URL

        Raises:
            ValueError: If URL is invalid
            requests.RequestException: If request fails
        """
        # Validate URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL: {url}")

        try:
            # Make request with timeout
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            # Determine content type
            content_type = response.headers.get('content-type', '').lower()

            if 'html' in content_type:
                return self._extract_text_from_html(response.text)
            elif 'json' in content_type:
                return response.text
            else:
                return response.text

        except requests.RequestException as e:
            raise requests.RequestException(f"Error fetching URL {url}: {str(e)}")

    def read_stdin(self) -> str:
        """
        Read text from standard input.

        Returns:
            Text content from stdin
        """
        try:
            # Read all input from stdin
            text = sys.stdin.read()
            return text
        except Exception as e:
            raise IOError(f"Error reading from stdin: {str(e)}")

    def get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Get metadata about a file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with file metadata
        """
        if not os.path.exists(file_path):
            return {}

        try:
            stat = os.stat(file_path)
            return {
                'file_path': os.path.abspath(file_path),
                'file_name': os.path.basename(file_path),
                'file_size': stat.st_size,
                'file_extension': os.path.splitext(file_path)[1].lower(),
                'modified_time': stat.st_mtime,
                'created_time': stat.st_ctime
            }
        except Exception:
            return {'file_path': file_path}

    def _read_text_file(self, file_path: str) -> str:
        """Read a plain text file."""
        encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                raise IOError(f"Error reading text file: {str(e)}")

        raise IOError(f"Could not decode file {file_path} with any supported encoding")

    def _read_docx_file(self, file_path: str) -> str:
        """Read a Microsoft Word document."""
        if not DOCX_AVAILABLE:
            raise ValueError("python-docx library not available. Install with: pip install python-docx")

        try:
            doc = Document(file_path)
            paragraphs = [paragraph.text for paragraph in doc.paragraphs]
            return '\\n'.join(paragraphs)
        except Exception as e:
            raise IOError(f"Error reading DOCX file: {str(e)}")

    def _read_pdf_file(self, file_path: str) -> str:
        """Read a PDF document."""
        if not PDF_AVAILABLE:
            raise ValueError("PyPDF2 library not available. Install with: pip install PyPDF2")

        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\\n"
            return text
        except Exception as e:
            raise IOError(f"Error reading PDF file: {str(e)}")

    def _extract_text_from_html(self, html: str) -> str:
        """Extract text content from HTML."""
        if not BS4_AVAILABLE:
            # Fallback: simple regex-based HTML tag removal
            import re
            text = re.sub(r'<[^>]+>', '', html)
            # Clean up whitespace
            text = re.sub(r'\\s+', ' ', text)
            return text.strip()

        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text content
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\\n'.join(chunk for chunk in chunks if chunk)

            return text
        except Exception as e:
            # Fallback to regex method
            import re
            text = re.sub(r'<[^>]+>', '', html)
            text = re.sub(r'\\s+', ' ', text)
            return text.strip()

    def detect_input_type(self, input_source: str) -> str:
        """
        Detect the type of input source.

        Args:
            input_source: Input source string

        Returns:
            Type of input: 'file', 'url', 'text'
        """
        # Check if it's a URL
        if input_source.startswith(('http://', 'https://')):
            return 'url'

        # Check if it's a file path
        if os.path.exists(input_source) or (os.path.sep in input_source):
            return 'file'

        # Otherwise, treat as direct text
        return 'text'

    def process_input(self, input_source: str, input_type: Optional[str] = None) -> tuple[str, Dict[str, Any]]:
        """
        Process input from various sources.

        Args:
            input_source: Input source (file path, URL, or text)
            input_type: Optional type hint ('file', 'url', 'text', 'stdin')

        Returns:
            Tuple of (text_content, metadata)
        """
        if input_type is None:
            input_type = self.detect_input_type(input_source)

        metadata = {'input_type': input_type, 'input_source': input_source}

        try:
            if input_type == 'file':
                text = self.read_file(input_source)
                metadata.update(self.get_file_metadata(input_source))
            elif input_type == 'url':
                text = self.fetch_url(input_source)
                metadata.update({'url': input_source})
            elif input_type == 'stdin':
                text = self.read_stdin()
            else:  # text
                text = input_source

            return text, metadata

        except Exception as e:
            # Return error information in metadata
            metadata['error'] = str(e)
            return "", metadata