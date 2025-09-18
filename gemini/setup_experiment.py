#!/usr/bin/env python3
"""
Automated TDD Experiment Setup Script
Ensures consistent, unbiased experimental setup following META_PROMPT_GENERATOR protocols
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, List

# Standardized neutral naming - no bias indicators
METHOD_CONFIGS = {
    "method_a": {
        "dir_name": "1-immediate-implementation",
        "display_name": "Immediate Implementation",
        "description": "Implementation begins directly with coding",
        "template": "method_1_template.md"
    },
    "method_b": {
        "dir_name": "2-specification-driven",
        "display_name": "Specification-Driven Development",
        "description": "Two-phase approach with specification then implementation",
        "template": "method_2_template.md"
    },
    "method_c": {
        "dir_name": "3-test-first-development",
        "display_name": "Test-First Development",
        "description": "Test-driven development with Red-Green-Refactor cycles",
        "template": "method_3_template.md"
    },
    "method_d": {
        "dir_name": "4-validated-test-development",
        "display_name": "Validated Test Development",
        "description": "Test-driven development with comprehensive test validation",
        "template": "method_4_template.md"
    }
}

class ExperimentSetup:
    def __init__(self, base_dir: str = "experiments"):
        self.base_dir = Path(base_dir)

    def get_next_experiment_number(self) -> str:
        """Get next sequential experiment number"""
        if not self.base_dir.exists():
            self.base_dir.mkdir(parents=True, exist_ok=True)
            return "001"

        existing = [d for d in self.base_dir.iterdir() if d.is_dir() and d.name[:3].isdigit()]
        if not existing:
            return "001"

        numbers = [int(d.name[:3]) for d in existing]
        return f"{max(numbers) + 1:03d}"

    def create_experiment(self, experiment_name: str, tech_stack: str,
                         application_type: str) -> str:
        """Create new experiment with standardized structure"""
        exp_number = self.get_next_experiment_number()
        exp_dir = self.base_dir / f"{exp_number}-{experiment_name}"

        print(f"Creating experiment {exp_number}: {experiment_name}")
        exp_dir.mkdir(parents=True, exist_ok=True)

        # Create method directories with neutral names
        method_dirs = []
        for method_id, config in METHOD_CONFIGS.items():
            method_dir = exp_dir / config["dir_name"]
            method_dir.mkdir(exist_ok=True)
            method_dirs.append(method_dir)

            # Initialize git repo
            subprocess.run(["git", "init"], cwd=method_dir, capture_output=True)

            # Create README with neutral language
            self._create_method_readme(method_dir, config, tech_stack, application_type)

            # Create prompt file for agent execution
            self._create_prompt_file(method_dir, config, tech_stack, application_type)

        # Create experiment metadata
        self._create_experiment_metadata(exp_dir, experiment_name, tech_stack, application_type)

        return str(exp_dir)

    def _create_method_readme(self, method_dir: Path, config: Dict,
                             tech_stack: str, application_type: str):
        """Create neutral README for method"""
        readme_content = f"""# {config['display_name']}

## Description
{config['description']}

## Approach
- See PROMPT.md for detailed methodology
- Technology Stack: {tech_stack}
- Target Application: {application_type}

## Success Criteria
- Functional implementation
- Development time metrics
- Code quality assessment
- Implementation completeness
- Test coverage (where applicable)
- Adherence to methodology

## Execution
```bash
# Follow instructions in PROMPT.md
# Record timing in TIMING_LOG.txt
# Commit frequently for process analysis
```
"""
        (method_dir / "README.md").write_text(readme_content)

    def _create_prompt_file(self, method_dir: Path, config: Dict,
                           tech_stack: str, application_type: str):
        """Create standardized prompt file"""
        prompts = self._generate_prompts(tech_stack, application_type)
        method_key = [k for k, v in METHOD_CONFIGS.items() if v == config][0]

        prompt_content = f"""# Agent Execution Prompt

## Method: {config['display_name']}

Execute the following prompt exactly as specified:

---

{prompts[method_key]}

---

## Timing Instructions
- Automatic timing will be captured by the controlling system
- Optional manual backup: Add timestamps to TIMING_LOG.txt
- Record major milestones and phase transitions

## Commit Strategy
- Commit frequently to show development progression
- Use descriptive commit messages
- Tag major milestones (e.g., "RED phase complete", "GREEN phase complete")
"""
        (method_dir / "PROMPT.md").write_text(prompt_content)

    def _generate_prompts(self, tech_stack: str, application_type: str) -> Dict[str, str]:
        """Generate the four standardized prompts"""
        return {
            "method_a": f"""Build a {application_type} using {tech_stack}.

Make it fully functional with all the features you think it should have. Include a user interface and all necessary functionality.""",

            "method_b": f"""First, write comprehensive specifications for a {application_type}, then build the complete application.

Phase 1 - Specifications:
- List all features and requirements
- Define user stories and use cases
- Outline the technical architecture
- Specify data models and relationships
- Document business rules and constraints

Phase 2 - Implementation:
- Build the application according to the specifications
- Include all specified features
- Use {tech_stack} as the technology stack
- Ensure the final product matches the specifications

Provide both the specifications document and the complete implementation.""",

            "method_c": f"""Create a {application_type} using Test-Driven Development principles. Follow this exact process:

PHASE 1 - SPECIFICATIONS:
Write detailed specifications including:
1. Core functional requirements
2. User stories with acceptance criteria
3. Technical architecture overview
4. Data models and relationships
5. API design (if applicable)
6. Business rules and validation requirements
7. Error handling and edge cases

PHASE 2 - TDD IMPLEMENTATION:
Using the specifications above, implement using strict TDD:

FOR EACH FEATURE:
1. **RED**: Write failing tests first
   - Unit tests for individual components
   - Integration tests for component interactions
   - Edge case and error condition tests
   - Tests should describe expected behavior clearly

2. **GREEN**: Write minimal implementation code
   - Only enough code to make tests pass
   - No additional functionality beyond what tests require

3. **REFACTOR**: Clean up code while keeping tests green
   - Improve structure and readability
   - Remove duplication
   - Maintain test coverage

STRICT RULES:
- NO implementation code before tests
- Tests must fail before writing implementation
- Each commit should follow Red-Green-Refactor cycle
- Start with simplest features first

Technology: {tech_stack}
Show your work: display tests, show them failing, then show implementation.""",

            "method_d": f"""Create a {application_type} using Test-Driven Development with comprehensive test validation. Follow this rigorous process:

PHASE 1 - SPECIFICATIONS:
Write detailed specifications including:
1. Core functional requirements
2. User stories with acceptance criteria
3. Technical architecture overview
4. Data models and relationships
5. API design (if applicable)
6. Business rules and validation requirements
7. Error handling and edge cases

PHASE 2 - TEST-DRIVEN DEVELOPMENT WITH VALIDATION:

FOR EACH FEATURE, FOLLOW THIS COMPREHENSIVE CYCLE:

1. **RED**: Write failing tests
   - Write comprehensive test cases first
   - Include unit, integration, and edge case tests
   - Make tests descriptive and behavior-focused

2. **TEST VALIDATION** (Critical Step):
   Before writing implementation, validate your tests:

   a) **Explain Each Test**:
      - What specific behavior does this test verify?
      - What would happen if the implementation was wrong?
      - Does this test actually test what it claims to test?

   b) **Test the Tests**:
      - Write obviously incorrect implementation that should fail
      - Verify tests catch common mistakes in this domain
      - Ensure tests fail for the RIGHT reasons
      - Example: If testing addition, ensure test fails when function does subtraction

   c) **Test Quality Checklist**:
      - Are assertions specific and meaningful?
      - Do tests cover positive AND negative scenarios?
      - Would these tests catch realistic bugs?
      - Are there obvious ways tests could pass incorrectly?

3. **GREEN**: Write correct implementation
   - Only after test validation passes
   - Write minimal code to make tests pass
   - Verify all tests pass for correct reasons

4. **REFACTOR**: Improve code quality
   - Clean up implementation while tests stay green
   - Ensure test suite remains robust

5. **QUALITY GATES**: Before moving to next feature
   - Run full test suite
   - Verify test coverage is appropriate
   - Confirm error handling works correctly
   - Validate integration points function properly

ENHANCED RULES:
- NEVER write implementation before test validation
- Always demonstrate test validation step
- Show incorrect implementation failing tests
- Explain why each test matters
- Start with absolute simplest feature

Technology: {tech_stack}
Show all work: failing tests, test validation, correct implementation, passing tests."""
        }

    def _create_experiment_metadata(self, exp_dir: Path, experiment_name: str,
                                  tech_stack: str, application_type: str):
        """Create experiment metadata and documentation"""
        metadata = {
            "experiment_name": experiment_name,
            "tech_stack": tech_stack,
            "application_type": application_type,
            "methods": METHOD_CONFIGS,
            "created_at": subprocess.check_output(["date", "-u"]).decode().strip(),
            "setup_version": "2.0"
        }

        (exp_dir / "experiment_metadata.json").write_text(json.dumps(metadata, indent=2))

        # Create experiment overview
        overview = f"""# Experiment: {experiment_name}

## Configuration
- **Application Type**: {application_type}
- **Technology Stack**: {tech_stack}
- **Setup Version**: 2.0 (Neutral Protocol)

## Methods
{self._format_methods_table()}

## Execution Protocol
1. Each method directory contains PROMPT.md with exact instructions
2. Execute methods independently (parallel or sequential)
3. Follow timing and commit protocols in each README.md
4. Analyze results objectively without bias toward any method

## Bias Prevention
- Neutral naming conventions used throughout
- No quality expectations embedded in method names
- Identical success criteria across methods
- Standardized evaluation metrics

## Analysis Guidelines
- Document unexpected outcomes
- Measure actual performance vs. assumptions
- Consider context-dependent effectiveness
- Remain open to results that challenge preconceptions
"""
        (exp_dir / "EXPERIMENT_OVERVIEW.md").write_text(overview)

    def _format_methods_table(self) -> str:
        """Format methods as markdown table"""
        table = "| Method | Directory | Description |\n|--------|-----------|-------------|\n"
        for config in METHOD_CONFIGS.values():
            table += f"| {config['display_name']} | {config['dir_name']} | {config['description']} |\n"
        return table


def main():
    """CLI interface for experiment setup"""
    import argparse

    parser = argparse.ArgumentParser(description="Setup TDD experiment with neutral protocols")
    parser.add_argument("experiment_name", help="Name for the experiment (e.g., 'lru-cache-ttl')")
    parser.add_argument("--tech-stack", default="Python", help="Technology stack (default: Python)")
    parser.add_argument("--app-type", required=True, help="Application type (e.g., 'LRU Cache with TTL')")

    args = parser.parse_args()

    setup = ExperimentSetup()
    exp_dir = setup.create_experiment(args.experiment_name, args.tech_stack, args.app_type)

    print(f"✅ Experiment created: {exp_dir}")
    print(f"📁 Method directories created with neutral naming")
    print(f"📋 Prompts generated and saved to PROMPT.md files")
    print(f"🔬 Ready for unbiased experimental execution")


if __name__ == "__main__":
    main()