#!/usr/bin/env python3
"""
Experiment Validation Script
Ensures experimental setup follows neutral protocols and catches bias
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Tuple

# Bias detection patterns
BIAS_PATTERNS = {
    'quality_bias': [
        r'\b(naive|simple|basic|primitive|crude)\b',
        r'\b(advanced|sophisticated|optimal|superior|better)\b',
        r'\b(poor|bad|worse|inferior|suboptimal)\b',
        r'\b(best|excellent|perfect|ideal)\b'
    ],
    'expectation_bias': [
        r'should\s+(be\s+)?(faster|slower|better|worse)',
        r'expected\s+to\s+(perform|work)\s+(better|worse)',
        r'(probably|likely)\s+(will|won\'t)\s+work',
        r'this\s+(will|should)\s+(obviously|clearly)'
    ],
    'methodology_bias': [
        r'proper\s+way',
        r'correct\s+approach',
        r'right\s+method',
        r'wrong\s+way'
    ]
}

REQUIRED_NEUTRAL_TERMS = {
    '1-immediate-implementation': 'immediate implementation',
    '2-specification-driven': 'specification-driven',
    '3-test-first-development': 'test-first development',
    '4-validated-test-development': 'validated test development'
}

class ExperimentValidator:
    def __init__(self, experiment_dir: str):
        self.exp_dir = Path(experiment_dir)
        self.errors = []
        self.warnings = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """Run complete validation suite"""
        print(f"🔍 Validating experiment: {self.exp_dir}")

        # Check directory structure
        self._check_directory_structure()

        # Check naming conventions
        self._check_naming_conventions()

        # Check for bias in content
        self._check_content_bias()

        # Check prompt accuracy
        self._check_prompt_accuracy()

        # Check metadata
        self._check_metadata()

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def _check_directory_structure(self):
        """Verify required directory structure exists"""
        required_dirs = [
            "1-immediate-implementation",
            "2-specification-driven",
            "3-test-first-development",
            "4-validated-test-development"
        ]

        for dir_name in required_dirs:
            dir_path = self.exp_dir / dir_name
            if not dir_path.exists():
                self.errors.append(f"Missing required directory: {dir_name}")
            else:
                # Check required files
                required_files = ["README.md", "PROMPT.md"]
                for file_name in required_files:
                    if not (dir_path / file_name).exists():
                        self.errors.append(f"Missing {file_name} in {dir_name}")

                # Check git initialization
                if not (dir_path / ".git").exists():
                    self.warnings.append(f"Git not initialized in {dir_name}")

    def _check_naming_conventions(self):
        """Verify neutral naming conventions"""
        for dir_name in self.exp_dir.iterdir():
            if dir_name.is_dir() and dir_name.name.startswith(('1-', '2-', '3-', '4-')):
                if dir_name.name not in REQUIRED_NEUTRAL_TERMS:
                    self.errors.append(f"Non-standard directory name: {dir_name.name}")

    def _check_content_bias(self):
        """Scan all text files for bias patterns"""
        text_files = []
        for pattern in ["**/*.md", "**/*.txt", "**/*.py"]:
            text_files.extend(self.exp_dir.glob(pattern))

        for file_path in text_files:
            try:
                content = file_path.read_text()
                self._scan_text_for_bias(content, str(file_path))
            except Exception as e:
                self.warnings.append(f"Could not read {file_path}: {e}")

    def _scan_text_for_bias(self, content: str, file_path: str):
        """Scan text content for bias patterns"""
        content_lower = content.lower()

        for bias_type, patterns in BIAS_PATTERNS.items():
            for pattern in patterns:
                matches = re.findall(pattern, content_lower, re.IGNORECASE)
                if matches:
                    self.errors.append(
                        f"Bias detected in {file_path}: {bias_type} - '{matches[0]}'"
                    )

        # Check for forbidden terms in method descriptions
        forbidden_terms = [
            'naive', 'simple', 'basic', 'advanced', 'sophisticated',
            'better', 'worse', 'optimal', 'suboptimal', 'proper', 'correct'
        ]
        for term in forbidden_terms:
            if re.search(rf'\b{term}\b', content_lower):
                self.errors.append(
                    f"Forbidden bias term '{term}' found in {file_path}"
                )

    def _check_prompt_accuracy(self):
        """Verify prompts match META_PROMPT_GENERATOR specifications"""
        # This would ideally compare against the actual META_PROMPT_GENERATOR
        # For now, check basic structure requirements
        method_dirs = [d for d in self.exp_dir.iterdir()
                      if d.is_dir() and d.name.startswith(('1-', '2-', '3-', '4-'))]

        for method_dir in method_dirs:
            prompt_file = method_dir / "PROMPT.md"
            if prompt_file.exists():
                content = prompt_file.read_text()

                # Check for required sections based on method type
                if "1-immediate" in method_dir.name:
                    if "Make it fully functional" not in content:
                        self.errors.append(f"Method 1 prompt missing key phrase in {method_dir.name}")

                elif "2-specification" in method_dir.name:
                    required_phrases = ["Phase 1 - Specifications", "Phase 2 - Implementation"]
                    for phrase in required_phrases:
                        if phrase not in content:
                            self.errors.append(f"Method 2 prompt missing '{phrase}' in {method_dir.name}")

                elif "3-test-first" in method_dir.name:
                    required_phrases = ["RED", "GREEN", "REFACTOR", "STRICT RULES"]
                    for phrase in required_phrases:
                        if phrase not in content:
                            self.errors.append(f"Method 3 prompt missing '{phrase}' in {method_dir.name}")

                elif "4-validated" in method_dir.name:
                    required_phrases = ["TEST VALIDATION", "Test the Tests", "QUALITY GATES"]
                    for phrase in required_phrases:
                        if phrase not in content:
                            self.errors.append(f"Method 4 prompt missing '{phrase}' in {method_dir.name}")

    def _check_metadata(self):
        """Verify experiment metadata is present and valid"""
        metadata_file = self.exp_dir / "experiment_metadata.json"
        if not metadata_file.exists():
            self.warnings.append("Missing experiment_metadata.json")
            return

        try:
            metadata = json.loads(metadata_file.read_text())
            required_fields = ["experiment_name", "tech_stack", "application_type", "setup_version"]
            for field in required_fields:
                if field not in metadata:
                    self.errors.append(f"Missing required metadata field: {field}")
        except json.JSONDecodeError:
            self.errors.append("Invalid JSON in experiment_metadata.json")

    def generate_report(self) -> str:
        """Generate validation report"""
        report = f"# Experiment Validation Report\n\n"
        report += f"**Experiment**: {self.exp_dir.name}\n\n"

        if not self.errors and not self.warnings:
            report += "✅ **PASSED**: Experiment setup meets all neutrality standards\n\n"
        else:
            if self.errors:
                report += f"❌ **FAILED**: {len(self.errors)} critical issues found\n\n"
                report += "## Errors (Must Fix)\n"
                for i, error in enumerate(self.errors, 1):
                    report += f"{i}. {error}\n"
                report += "\n"

            if self.warnings:
                report += f"⚠️  **WARNINGS**: {len(self.warnings)} potential issues\n\n"
                report += "## Warnings (Should Fix)\n"
                for i, warning in enumerate(self.warnings, 1):
                    report += f"{i}. {warning}\n"
                report += "\n"

        report += "## Validation Checklist\n"
        checklist_items = [
            ("Directory Structure", len([e for e in self.errors if "Missing required directory" in e]) == 0),
            ("Neutral Naming", len([e for e in self.errors if "Non-standard directory name" in e]) == 0),
            ("Bias-Free Content", len([e for e in self.errors if "Bias detected" in e or "Forbidden bias term" in e]) == 0),
            ("Prompt Accuracy", len([e for e in self.errors if "prompt missing" in e]) == 0),
            ("Metadata Present", len([e for e in self.errors if "metadata" in e]) == 0),
        ]

        for item, passed in checklist_items:
            status = "✅" if passed else "❌"
            report += f"- {status} {item}\n"

        return report


def main():
    """CLI interface for experiment validation"""
    import argparse

    parser = argparse.ArgumentParser(description="Validate TDD experiment for bias and standards compliance")
    parser.add_argument("experiment_dir", help="Path to experiment directory")
    parser.add_argument("--report", "-r", help="Output validation report to file")

    args = parser.parse_args()

    validator = ExperimentValidator(args.experiment_dir)
    is_valid, errors, warnings = validator.validate()

    # Print summary
    if is_valid:
        print("✅ Validation PASSED - Experiment meets neutrality standards")
    else:
        print(f"❌ Validation FAILED - {len(errors)} critical issues found")
        for error in errors:
            print(f"  • {error}")

    if warnings:
        print(f"⚠️  {len(warnings)} warnings:")
        for warning in warnings:
            print(f"  • {warning}")

    # Generate report if requested
    if args.report:
        report = validator.generate_report()
        Path(args.report).write_text(report)
        print(f"📋 Validation report saved to {args.report}")

    return 0 if is_valid else 1


if __name__ == "__main__":
    exit(main())