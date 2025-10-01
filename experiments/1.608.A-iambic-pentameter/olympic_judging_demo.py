#!/usr/bin/env python3
"""
Olympic Judging System for Iambic Pentameter Converter
Uses 3 LLM judges to score outputs, drops high/low, averages remaining scores

Judge models: llama3.2 (Meta), phi3:mini (Microsoft), gemma2:2b (Google)
"""

import sys
import subprocess
import json
import argparse
from pathlib import Path


class OlympicJudge:
    """Single LLM judge for scoring iambic pentameter quality"""

    def __init__(self, judge_id, model):
        self.judge_id = judge_id
        self.model = model

    def score(self, original_prose, iambic_output):
        """Score the iambic pentameter conversion (0-10)"""
        prompt = f"""You are Judge #{self.judge_id} in an Olympic-style poetry competition.

Score this iambic pentameter conversion from 0-10 based on:
- Syllable accuracy (10 syllables per line)
- Iambic meter (da-DUM pattern)
- Meaning preservation
- Poetic quality

ORIGINAL PROSE:
{original_prose}

IAMBIC PENTAMETER OUTPUT:
{iambic_output}

Provide ONLY a score from 0-10 (one number). No explanation."""

        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60  # Increased for slower models (phi3, gemma2)
            )

            # Extract number from output
            score_text = result.stdout.strip()
            # Try to find a number in the output
            import re
            numbers = re.findall(r'\d+\.?\d*', score_text)
            if numbers:
                score = float(numbers[0])
                return min(max(score, 0), 10)  # Clamp to 0-10
            return 5.0  # Default if parsing fails

        except Exception as e:
            print(f"Judge {self.judge_id} error: {e}")
            return 5.0


class OlympicJudgingSystem:
    """Olympic-style judging with 3 judges, drop high/low, average middle"""

    def __init__(self, judge_models=['llama3.2', 'phi3:mini', 'gemma2:2b']):
        """
        Initialize with diverse judge models to reduce bias.

        Args:
            judge_models: List of model names for judges (default: Meta, Microsoft, Google)
        """
        self.judges = [OlympicJudge(i+1, model) for i, model in enumerate(judge_models)]

    def judge(self, original_prose, iambic_output, method_name):
        """Get Olympic score for an output"""
        print(f"\n🏅 Judging {method_name}...")

        scores = []
        for judge in self.judges:
            score = judge.score(original_prose, iambic_output)
            scores.append(score)
            print(f"  Judge {judge.judge_id} ({judge.model}): {score:.1f}")

        # Drop high and low
        sorted_scores = sorted(scores)
        if len(sorted_scores) >= 3:
            middle_scores = sorted_scores[1:-1]
        else:
            middle_scores = sorted_scores

        final_score = sum(middle_scores) / len(middle_scores)

        print(f"  Dropped: {min(scores):.1f} (low), {max(scores):.1f} (high)")
        print(f"  Final Score: {final_score:.2f}/10")

        return {
            'method': method_name,
            'all_scores': scores,
            'dropped_low': min(scores),
            'dropped_high': max(scores),
            'final_score': final_score
        }


def load_implementation(method_dir):
    """Load a method implementation"""
    impl_path = Path(method_dir) / "iambic_converter.py"
    if not impl_path.exists():
        return None

    # Import the module dynamically
    import importlib.util
    spec = importlib.util.spec_from_file_location("iambic_converter", impl_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def run_conversion(method_dir, prose):
    """Run conversion using a specific method"""
    module = load_implementation(method_dir)
    if not module:
        return None

    try:
        # Try different class/function names used by different methods
        if hasattr(module, 'IambicConverter'):
            converter = module.IambicConverter()
            return converter.convert(prose)
        elif hasattr(module, 'convert_story_to_iambic'):
            return module.convert_story_to_iambic(prose)
        elif hasattr(module, 'convert_prose_to_iambic'):
            return module.convert_prose_to_iambic(prose)
        else:
            return None
    except Exception as e:
        print(f"Error running conversion: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Olympic Judging System for Iambic Pentameter')
    parser.add_argument('--run', type=int, default=1, help='Run number (default: 1)')
    parser.add_argument('--methods', type=int, default=4, help='Number of methods to judge (default: 4)')
    parser.add_argument('--prose', type=str, help='Custom prose to convert')
    args = parser.parse_args()

    # Default test prose
    test_prose = args.prose or "The cat sat on the mat and watched the birds fly overhead."

    # Experiment directory
    exp_dir = Path(__file__).parent

    # Method directories
    methods = [
        ('1-immediate-implementation', 'Method 1: Immediate Implementation'),
        ('2-specification-driven', 'Method 2: Specification-Driven'),
        ('3-test-first-development', 'Method 3: Pure TDD'),
        ('4-adaptive-tdd', 'Method 4: Adaptive TDD')
    ][:args.methods]

    print("="*80)
    print("🏆 OLYMPIC JUDGING SYSTEM - Iambic Pentameter Converter")
    print("="*80)
    print(f"\nOriginal Prose: {test_prose}")
    print(f"Judges: llama3.2 (Meta), phi3:mini (Microsoft), gemma2:2b (Google)")
    print(f"Scoring: Drop high/low, average remaining")
    print(f"Methods to judge: {len(methods)}\n")

    # Run conversions and collect outputs
    outputs = []
    for method_dir, method_name in methods:
        full_path = exp_dir / method_dir
        print(f"\n🔧 Running {method_name}...")
        output = run_conversion(full_path, test_prose)

        if output:
            print(f"Output preview: {output[:100]}...")
            outputs.append((method_name, output))
        else:
            print(f"⚠️  Skipped (implementation error)")

    if not outputs:
        print("\n❌ No methods produced output!")
        return 1

    # Judge all outputs
    print("\n" + "="*80)
    print("📊 JUDGING RESULTS")
    print("="*80)

    judging_system = OlympicJudgingSystem()
    results = []

    for method_name, output in outputs:
        result = judging_system.judge(test_prose, output, method_name)
        results.append(result)

    # Rank and display final results
    results.sort(key=lambda x: x['final_score'], reverse=True)

    print("\n" + "="*80)
    print("🏅 FINAL RANKINGS")
    print("="*80)

    medals = ['🥇', '🥈', '🥉']
    for i, result in enumerate(results):
        medal = medals[i] if i < len(medals) else '  '
        print(f"{medal} {i+1}. {result['method']}: {result['final_score']:.2f}/10")

    print("\n" + "="*80)

    return 0


if __name__ == '__main__':
    sys.exit(main())
