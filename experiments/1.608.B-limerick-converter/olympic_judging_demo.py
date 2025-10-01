#!/usr/bin/env python3
"""
Olympic Judging Demo for Experiment 1.608.B - Limerick Converter

Tests all 4 method implementations with a sample story and has 3 LLM judges
score each limerick for aesthetic quality. Uses Olympic scoring: drop highest
and lowest scores, average the remaining scores.

Judges:
- llama3.2 (Judge 1)
- phi3:mini (Judge 2)
- gemma2:2b (Judge 3)
"""

import sys
import os
import json
import subprocess
import time
from pathlib import Path


# Sample test story
TEST_STORY = """
In a small village, a clever fox outsmarted the local hunters
by using their own traps against them. The fox would trigger
the traps from a distance, then feast on the bait while the
hunters reset their devices in frustration.
"""


def call_ollama_judge(model: str, limerick: str, method_name: str) -> float:
    """
    Have an LLM judge score a limerick's aesthetic quality.

    Returns a score from 1-10.
    """
    prompt = f"""You are an expert poetry judge evaluating limericks for aesthetic quality.

Rate this limerick on a scale of 1-10 based on:
- Rhythm and meter (anapestic flow)
- Rhyme quality (how well does AABBA work?)
- Cleverness and humor
- Captures story essence
- Overall aesthetic appeal

LIMERICK:
{limerick}

METHOD: {method_name}

Return ONLY a single number from 1-10, nothing else. Be critical and differentiate between methods.
Your score (1-10):"""

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"  Warning: {model} failed: {result.stderr}")
            return 5.0  # Default score

        # Extract number from response
        response = result.stdout.strip()
        # Try to find a number in the response
        import re
        numbers = re.findall(r'\d+\.?\d*', response)
        if numbers:
            score = float(numbers[0])
            # Clamp to 1-10 range
            return max(1.0, min(10.0, score))
        else:
            print(f"  Warning: {model} didn't return a number: {response[:50]}")
            return 5.0

    except subprocess.TimeoutExpired:
        print(f"  Warning: {model} timed out")
        return 5.0
    except Exception as e:
        print(f"  Warning: {model} error: {e}")
        return 5.0


def generate_limerick_method1(story: str) -> dict:
    """Generate limerick using Method 1: Immediate Implementation."""
    sys.path.insert(0, str(Path(__file__).parent / "1-immediate-implementation"))
    from limerick_converter import LimerickConverter

    converter = LimerickConverter()
    result = converter.convert(story, validate=True)

    return {
        "limerick": result["limerick"],
        "lines": result["lines"],
        "validation": result.get("validation")
    }


def generate_limerick_method2(story: str) -> dict:
    """Generate limerick using Method 2: Specification-Driven."""
    sys.path.insert(0, str(Path(__file__).parent / "2-specification-driven"))

    # Import the module
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "limerick_converter_m2",
        Path(__file__).parent / "2-specification-driven" / "limerick_converter.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    converter = module.LimerickConverter()
    result = converter.convert(story)

    return {
        "limerick": result["limerick"],
        "lines": result["lines"].split('\n') if isinstance(result["lines"], str) else result["lines"],
        "validation": result.get("validation")
    }


def generate_limerick_method3(story: str) -> dict:
    """Generate limerick using Method 3: Pure TDD."""
    sys.path.insert(0, str(Path(__file__).parent / "3-test-first-development"))

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "limerick_converter_m3",
        Path(__file__).parent / "3-test-first-development" / "limerick_converter.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    result = module.generate_limerick(story)

    return {
        "limerick": result["limerick"],
        "lines": result["lines"],
        "validation": result.get("validation")
    }


def generate_limerick_method4(story: str) -> dict:
    """Generate limerick using Method 4: Adaptive/Validated TDD."""
    sys.path.insert(0, str(Path(__file__).parent / "4-adaptive-tdd"))

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "limerick_converter_m4",
        Path(__file__).parent / "4-adaptive-tdd" / "limerick_converter.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    converter = module.LimerickConverter()
    result = converter.convert(story)

    return {
        "limerick": result["limerick"],
        "lines": result["lines"],
        "validation": result.get("validation")
    }


def olympic_scoring(scores: list) -> float:
    """
    Olympic scoring: drop highest and lowest, average the rest.
    If only 3 scores, drop high and low, return middle.
    """
    if len(scores) < 3:
        return sum(scores) / len(scores)

    sorted_scores = sorted(scores)
    # Drop first (lowest) and last (highest)
    middle_scores = sorted_scores[1:-1]

    return sum(middle_scores) / len(middle_scores) if middle_scores else sorted_scores[1]


def main():
    print("=" * 80)
    print("OLYMPIC JUDGING DEMO: Experiment 1.608.B - Limerick Converter")
    print("=" * 80)
    print()

    print("TEST STORY:")
    print("-" * 80)
    print(TEST_STORY.strip())
    print("-" * 80)
    print()

    methods = [
        ("Method 1: Immediate Implementation", generate_limerick_method1),
        ("Method 2: Specification-Driven", generate_limerick_method2),
        ("Method 3: Pure TDD", generate_limerick_method3),
        ("Method 4: Adaptive/Validated TDD", generate_limerick_method4),
    ]

    results = {}

    print("GENERATING LIMERICKS FROM ALL 4 METHODS...")
    print()

    for method_name, generator in methods:
        print(f"⏳ {method_name}...")
        try:
            start_time = time.time()
            result = generator(TEST_STORY)
            gen_time = time.time() - start_time

            results[method_name] = {
                "limerick": result["limerick"],
                "lines": result["lines"],
                "validation": result.get("validation"),
                "generation_time": round(gen_time, 2)
            }
            print(f"   ✓ Generated in {gen_time:.2f}s")
        except Exception as e:
            print(f"   ✗ Error: {e}")
            results[method_name] = None

    print()
    print("=" * 80)
    print("GENERATED LIMERICKS")
    print("=" * 80)
    print()

    for method_name, result in results.items():
        if result:
            print(f"**{method_name}**")
            print(result["limerick"])
            if result.get("validation"):
                val = result["validation"]
                print(f"  Valid: {val.get('valid', 'N/A')}")
                if val.get('syllable_counts'):
                    print(f"  Syllables: {val['syllable_counts']}")
            print()

    print("=" * 80)
    print("OLYMPIC JUDGING (3 LLM Judges)")
    print("=" * 80)
    print()

    judges = [
        ("llama3.2", "Judge 1"),
        ("phi3:mini", "Judge 2"),
        ("gemma2:2b", "Judge 3"),
    ]

    judge_scores = {method: [] for method in results.keys() if results[method]}

    for model, judge_name in judges:
        print(f"🧑‍⚖️  {judge_name} ({model}) scoring...")
        for method_name in results.keys():
            if results[method_name]:
                limerick = results[method_name]["limerick"]
                print(f"   Scoring {method_name}...", end=" ")
                score = call_ollama_judge(model, limerick, method_name)
                judge_scores[method_name].append(score)
                print(f"{score}/10")
        print()

    print("=" * 80)
    print("OLYMPIC SCORES (Drop High/Low, Average Middle)")
    print("=" * 80)
    print()

    final_scores = {}
    for method_name, scores in judge_scores.items():
        if scores:
            olympic_score = olympic_scoring(scores)
            final_scores[method_name] = olympic_score

            print(f"**{method_name}**")
            print(f"  Judge Scores: {scores}")
            print(f"  Olympic Score: {olympic_score:.2f}/10")
            print()

    # Rank methods
    ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    print("=" * 80)
    print("FINAL RANKINGS")
    print("=" * 80)
    print()

    medals = ["🥇", "🥈", "🥉", "4️⃣"]
    for i, (method_name, score) in enumerate(ranked):
        medal = medals[i] if i < len(medals) else f"{i+1}."
        print(f"{medal} {method_name}: {score:.2f}/10")

    print()
    print("=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)

    # Save results to file
    output_file = Path(__file__).parent / "OLYMPIC_JUDGING_RESULTS.txt"
    with open(output_file, 'w') as f:
        f.write("OLYMPIC JUDGING RESULTS\n")
        f.write("Experiment 1.608.B - Limerick Converter\n")
        f.write("=" * 80 + "\n\n")

        f.write("TEST STORY:\n")
        f.write(TEST_STORY.strip() + "\n\n")

        f.write("LIMERICKS:\n\n")
        for method_name, result in results.items():
            if result:
                f.write(f"{method_name}:\n")
                f.write(result["limerick"] + "\n\n")

        f.write("SCORES:\n\n")
        for method_name, scores in judge_scores.items():
            f.write(f"{method_name}: {scores} → {final_scores[method_name]:.2f}/10\n")

        f.write("\nFINAL RANKINGS:\n\n")
        for i, (method_name, score) in enumerate(ranked):
            medal = medals[i] if i < len(medals) else f"{i+1}."
            f.write(f"{medal} {method_name}: {score:.2f}/10\n")

    print(f"\n✓ Results saved to {output_file}")


if __name__ == "__main__":
    main()
