#!/usr/bin/env python3
"""
Story to Iambic Pentameter Converter
Converts prose text into Shakespearean verse using llama3.2 via Ollama
"""

import json
import subprocess
import sys
from typing import List


class IambicConverter:
    """Converts prose text to iambic pentameter using Ollama."""

    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def convert_to_iambic(self, prose: str) -> str:
        """
        Convert prose text to iambic pentameter.

        Args:
            prose: Input prose text

        Returns:
            Text formatted in iambic pentameter
        """
        prompt = self._create_prompt(prose)
        response = self._call_ollama(prompt)
        return response

    def _create_prompt(self, prose: str) -> str:
        """Create the prompt for Ollama."""
        return f"""Convert the following prose text into iambic pentameter (Shakespearean verse).

Rules for iambic pentameter:
- Each line must have exactly 10 syllables
- Syllables alternate between unstressed and stressed (da-DUM da-DUM da-DUM da-DUM da-DUM)
- Preserve the meaning and story of the original text
- Use poetic language suitable for Shakespeare

Original prose:
{prose}

Convert this to iambic pentameter verse. Return only the verse, no explanations:"""

    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API using subprocess."""
        try:
            # Use ollama run command
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                raise RuntimeError(f"Ollama error: {result.stderr}")

            return result.stdout.strip()

        except FileNotFoundError:
            raise RuntimeError("Ollama not found. Please install Ollama first.")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Ollama request timed out")

    def convert_paragraph(self, paragraph: str) -> str:
        """Convert a single paragraph to iambic pentameter."""
        return self.convert_to_iambic(paragraph)

    def convert_story(self, story: str, preserve_paragraphs: bool = True) -> str:
        """
        Convert an entire story to iambic pentameter.

        Args:
            story: The full story text
            preserve_paragraphs: If True, convert each paragraph separately

        Returns:
            Story converted to iambic pentameter
        """
        if not preserve_paragraphs:
            return self.convert_to_iambic(story)

        # Split into paragraphs and convert each
        paragraphs = [p.strip() for p in story.split('\n\n') if p.strip()]
        converted = []

        for para in paragraphs:
            converted_para = self.convert_paragraph(para)
            converted.append(converted_para)

        return '\n\n'.join(converted)


def main():
    """CLI interface for the converter."""
    if len(sys.argv) < 2:
        print("Usage: python iambic_converter.py <text>")
        print("   or: python iambic_converter.py -f <file>")
        sys.exit(1)

    converter = IambicConverter()

    # Check if reading from file
    if sys.argv[1] == '-f':
        if len(sys.argv) < 3:
            print("Error: Please specify a file path")
            sys.exit(1)

        with open(sys.argv[2], 'r') as f:
            text = f.read()
    else:
        # Join all arguments as the input text
        text = ' '.join(sys.argv[1:])

    print("Converting to iambic pentameter...")
    result = converter.convert_story(text)
    print("\n" + "="*50)
    print("IAMBIC PENTAMETER VERSE:")
    print("="*50)
    print(result)


if __name__ == "__main__":
    main()
