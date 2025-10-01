"""Story-to-Limerick Converter using Test-Driven Development."""


class LimerickConverter:
    """Converts stories to limericks with proper AABBA rhyme scheme."""

    def validate_limerick_structure(self, limerick_lines):
        """
        Validate that a limerick has the correct structure.

        Args:
            limerick_lines: List of strings, each representing a line

        Returns:
            Dict with:
                - valid: bool indicating if structure is valid
                - line_count: int number of lines
                - issues: list of validation issues found
        """
        issues = []
        line_count = len(limerick_lines)

        if line_count != 5:
            issues.append(f'Must have exactly 5 lines, got {line_count}')

        return {
            'valid': len(issues) == 0,
            'line_count': line_count,
            'issues': issues
        }
