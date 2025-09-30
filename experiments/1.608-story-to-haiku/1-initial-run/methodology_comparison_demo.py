#!/usr/bin/env python3
"""
Methodology Comparison Demo - Story-to-Haiku Converter
Experiment 1.608

This script runs ALL 4 methodology implementations with REAL Ollama calls
to demonstrate the actual differences in output and behavior.

WARNING: This uses real Ollama and will take ~2-3 minutes to complete.
Each haiku generation takes ~20-30 seconds on typical hardware.
"""

import sys
import time
import importlib.util
from pathlib import Path

# Test stories for comparison
TEST_STORIES = [
    {
        "title": "The Mountain Garden",
        "text": """In a small village nestled between mountains, an old woman
        tended her garden every morning. She spoke to each plant as if they
        were old friends, sharing stories of seasons past."""
    },
    {
        "title": "The Midnight Coder",
        "text": """A young programmer sat late at night, debugging code that
        refused to work. Hours passed. Then suddenly, in a moment of clarity,
        the solution appeared. The computer hummed softly as tests turned green."""
    },
    {
        "title": "Ocean's Memory",
        "text": """The ocean waves crashed against ancient cliffs, carved by
        millennia of patient erosion. Each wave whispered secrets of storms
        long forgotten, of ships that sailed and never returned."""
    }
]

def load_method_module(method_num):
    """Dynamically load a method's implementation module."""
    method_dirs = {
        1: "1-immediate-implementation",
        2: "2-specification-driven",
        3: "3-test-first-development",
        4: "4-adaptive-tdd"
    }

    method_dir = Path(__file__).parent / method_dirs[method_num]
    module_path = method_dir / "haiku_converter.py"

    if not module_path.exists():
        raise FileNotFoundError(f"Method {method_num} not found at {module_path}")

    spec = importlib.util.spec_from_file_location(f"method{method_num}", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

def format_result(result):
    """Format a haiku result for display."""
    output = []
    output.append(f"  {result['haiku']}")
    output.append(f"  Syllables: {result['syllable_counts']}")
    if 'essence' in result:
        output.append(f"  Essence: {result['essence']}")
    return "\n".join(output)

def run_single_comparison(story, method_num):
    """Run a single method on a single story."""
    print(f"\n{'='*70}")
    print(f"METHOD {method_num}")
    print(f"{'='*70}")

    try:
        # Load method implementation
        module = load_method_module(method_num)

        # Time the execution
        start_time = time.time()
        result = module.story_to_haiku(story['text'])  # Real Ollama call!
        elapsed = time.time() - start_time

        # Display results
        print(f"\n📖 Story: {story['title']}")
        print(f"\n🎋 Haiku:")
        print(format_result(result))
        print(f"\n⏱️  Generation Time: {elapsed:.1f}s")

        return {
            'method': method_num,
            'success': True,
            'result': result,
            'time': elapsed
        }

    except Exception as e:
        print(f"\n❌ ERROR in Method {method_num}: {e}")
        return {
            'method': method_num,
            'success': False,
            'error': str(e),
            'time': 0
        }

def run_comparison(story_index=0):
    """Run comparison for a single story across all methods."""
    story = TEST_STORIES[story_index]

    print("\n" + "="*70)
    print(f"STORY-TO-HAIKU METHODOLOGY COMPARISON")
    print(f"Experiment 1.608 - Using Real Ollama (llama3.2)")
    print("="*70)
    print(f"\n📖 Test Story: {story['title']}")
    print(f"\n{story['text'][:150]}...")
    print("\n" + "="*70)

    results = []

    # Run each method sequentially (required - single Ollama instance)
    for method_num in [1, 2, 3, 4]:
        result = run_single_comparison(story, method_num)
        results.append(result)

        # Small pause between methods
        if method_num < 4:
            time.sleep(1)

    return results

def print_summary(results):
    """Print summary comparison of all methods."""
    print("\n" + "="*70)
    print("SUMMARY COMPARISON")
    print("="*70)

    successful_results = [r for r in results if r['success']]

    if not successful_results:
        print("\n❌ No methods completed successfully")
        return

    # Timing comparison
    print("\n⏱️  Generation Times:")
    for r in successful_results:
        print(f"  Method {r['method']}: {r['time']:.1f}s")

    avg_time = sum(r['time'] for r in successful_results) / len(successful_results)
    print(f"\n  Average: {avg_time:.1f}s")

    # Haiku comparison
    print("\n🎋 Haiku Outputs:")
    for r in successful_results:
        print(f"\n  Method {r['method']}:")
        for line in r['result']['haiku'].split('\n'):
            print(f"    {line}")

    # Syllable accuracy
    print("\n📊 Syllable Counts (target: [5, 7, 5]):")
    for r in successful_results:
        counts = r['result']['syllable_counts']
        match = "✓" if counts == [5, 7, 5] else "✗"
        print(f"  Method {r['method']}: {counts} {match}")

def print_methodology_notes():
    """Print notes about each methodology."""
    print("\n" + "="*70)
    print("METHODOLOGY NOTES")
    print("="*70)

    notes = {
        1: "Immediate Implementation - Fast coding, minimal planning",
        2: "Specification-Driven - Comprehensive design before implementation",
        3: "Test-First Development - Strict TDD (Red-Green-Refactor)",
        4: "Adaptive TDD - Strategic testing, pragmatic approach"
    }

    print("\n")
    for method, note in notes.items():
        print(f"  Method {method}: {note}")

    print("\n" + "="*70)

def main():
    """Main comparison script."""
    import argparse

    parser = argparse.ArgumentParser(description='Compare methodology implementations with real Ollama')
    parser.add_argument('--story', type=int, default=0, choices=[0, 1, 2],
                       help='Which test story to use (0-2)')
    parser.add_argument('--method', type=int, choices=[1, 2, 3, 4],
                       help='Run only a specific method (default: all)')
    parser.add_argument('--all-stories', action='store_true',
                       help='Run all stories (WARNING: takes 10+ minutes)')

    args = parser.parse_args()

    print_methodology_notes()

    if args.all_stories:
        print("\n⚠️  Running ALL stories - this will take 10+ minutes...")
        all_results = []
        for i in range(len(TEST_STORIES)):
            story_results = run_comparison(story_index=i)
            all_results.extend(story_results)
            print("\n" + "="*70 + "\n")

        print("\n🏁 ALL STORIES COMPLETE")

    elif args.method:
        # Single method
        story = TEST_STORIES[args.story]
        print(f"\n📖 Story: {story['title']}")
        result = run_single_comparison(story, args.method)
        print_summary([result])

    else:
        # Single story, all methods (default - good for demo)
        results = run_comparison(story_index=args.story)
        print_summary(results)

    print("\n✨ Comparison complete!\n")

if __name__ == "__main__":
    main()