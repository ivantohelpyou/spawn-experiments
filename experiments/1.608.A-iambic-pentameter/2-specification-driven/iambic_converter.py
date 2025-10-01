"""
Story-to-Iambic-Pentameter Converter
Specification-Driven Implementation
"""

import re
import subprocess
from typing import Dict, Tuple


class SyllableCounter:
    """Count syllables in English words."""

    EXCEPTIONS = {
        'the': 1, 'a': 1, 'to': 1, 'of': 1, 'and': 1, 'said': 1,
        'love': 1, 'come': 1, 'some': 1, 'fire': 1, 'hour': 1,
        'power': 2, 'flower': 2, 'special': 2, 'people': 2,
        'every': 3, 'family': 3,
    }

    def count_syllables(self, word: str) -> int:
        """Count syllables in a word."""
        clean_word = re.sub(r'[^a-zA-Z]', '', word).lower()
        if not clean_word:
            return 0
        if clean_word in self.EXCEPTIONS:
            return self.EXCEPTIONS[clean_word]

        count = 0
        previous_was_vowel = False
        for char in clean_word:
            is_vowel = char in 'aeiouy'
            if is_vowel and not previous_was_vowel:
                count += 1
            previous_was_vowel = is_vowel

        if clean_word.endswith('e') and not clean_word.endswith('le'):
            count -= 1

        return max(count, 1)

    def count_line_syllables(self, line: str) -> int:
        """Count syllables in a line."""
        return sum(self.count_syllables(word) for word in line.split())


class MeterValidator:
    """Validate iambic pentameter."""

    def __init__(self, strict: bool = False):
        self.strict = strict
        self.counter = SyllableCounter()

    def is_valid_line(self, line: str) -> Tuple[bool, int]:
        """Check if line is valid iambic pentameter."""
        syllables = self.counter.count_line_syllables(line)
        if self.strict:
            return syllables == 10, syllables
        return 9 <= syllables <= 11, syllables

    def validate_poem(self, text: str) -> Dict:
        """Validate entire poem."""
        lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
        details = []
        valid_count = 0

        for line in lines:
            is_valid, syllables = self.is_valid_line(line)
            details.append({'line': line, 'syllables': syllables, 'valid': is_valid})
            if is_valid:
                valid_count += 1

        total = len(lines)
        accuracy = (valid_count / total * 100) if total > 0 else 0

        return {
            'valid': valid_count == total,
            'total_lines': total,
            'valid_lines': valid_count,
            'accuracy': accuracy,
            'details': details
        }


class OllamaClient:
    """Handle Ollama communication."""

    def __init__(self, model: str = "llama3.2", timeout: int = 60):
        self.model = model
        self.timeout = timeout

    def is_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
            return result.returncode == 0 and self.model in result.stdout
        except:
            return False

    def generate(self, prompt: str) -> str:
        """Generate text."""
        if not self.is_available():
            raise ConnectionError(f"Ollama not available or model '{self.model}' not found")

        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            if result.returncode != 0:
                raise RuntimeError(f"Generation failed: {result.stderr}")
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Generation timed out after {self.timeout}s")


class IambicConverter:
    """Convert prose to iambic pentameter."""

    def __init__(self, model: str = "llama3.2", strict: bool = False):
        self.ollama = OllamaClient(model=model)
        self.validator = MeterValidator(strict=strict)
        self.max_attempts = 3

    def convert(self, text: str) -> str:
        """Convert prose to iambic pentameter."""
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")
        if len(text) > 5000:
            raise ValueError("Input text too long (max 5000 characters)")

        best_result = None
        best_accuracy = 0

        for attempt in range(1, self.max_attempts + 1):
            try:
                prompt = self._build_prompt(text) if attempt == 1 else self._build_refinement_prompt(text, best_result)
                poem = self.ollama.generate(prompt)
                validation = self.validator.validate_poem(poem)

                if validation['accuracy'] > best_accuracy:
                    best_accuracy = validation['accuracy']
                    best_result = {'poem': poem, 'validation': validation}

                if validation['valid'] or validation['accuracy'] >= 80:
                    return self._format_output(poem, validation)

            except (ConnectionError, TimeoutError):
                raise
            except Exception as e:
                if attempt == self.max_attempts:
                    raise RuntimeError(f"Conversion failed: {e}")

        if best_result:
            return self._format_output(best_result['poem'], best_result['validation'])
        raise RuntimeError("Failed to generate valid iambic pentameter")

    def _build_prompt(self, text: str) -> str:
        """Build initial prompt."""
        return f"""You are a Shakespearean poetry expert. Convert the following prose into iambic pentameter.

RULES:
- Each line must have exactly 10 syllables
- Follow iambic meter: da-DUM da-DUM da-DUM da-DUM da-DUM
- Maintain the original meaning
- Use poetic language
- Output only the poem, no explanations

PROSE:
{text}

IAMBIC PENTAMETER:"""

    def _build_refinement_prompt(self, text: str, previous_result: Dict) -> str:
        """Build refinement prompt."""
        validation = previous_result['validation']
        problems = [f"Line {i+1}: {d['line']} ({d['syllables']} syllables)"
                   for i, d in enumerate(validation['details']) if not d['valid']][:5]

        return f"""The previous attempt had incorrect syllable counts.

PROBLEMS:
{chr(10).join(problems)}

Revise to ensure EVERY line has exactly 10 syllables. Use contractions (I'm, don't, 'tis).

ORIGINAL PROSE:
{text}

REVISED IAMBIC PENTAMETER:"""

    def _format_output(self, poem: str, validation: Dict) -> str:
        """Format output."""
        lines = [l.strip() for l in poem.strip().split('\n') if l.strip()]
        formatted = '\n'.join(lines)

        if not validation['valid']:
            acc = validation['accuracy']
            formatted += f"\n\n[Note: {acc:.1f}% accuracy ({validation['valid_lines']}/{validation['total_lines']} lines correct)]"

        return formatted


def main():
    """Example usage."""
    converter = IambicConverter()
    prose = "The cat sat on the mat and looked at the bird."

    print("Story-to-Iambic-Pentameter Converter")
    print("="*50)
    print(f"Prose: {prose}\n")

    try:
        poem = converter.convert(prose)
        print("Iambic Pentameter:")
        print(poem)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
