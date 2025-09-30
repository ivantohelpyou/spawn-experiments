#!/usr/bin/env python3
"""
Live Demo Script - Story-to-Haiku Converter
Experiment 1.608

Demonstrates all 4 implementations working with REAL Ollama.
Perfect for live demo - shows actual AI-generated haiku outputs.

Usage: python live_demo.py [--story N]
"""

import sys
import time
from pathlib import Path

# Ensure we can import the implementations
sys.path.insert(0, str(Path(__file__).parent))

# Import all method implementations
from importlib import import_module
import importlib.util

def load_method(method_num):
    """Load a method's haiku_converter module."""
    method_dirs = {
        1: "1-immediate-implementation",
        2: "2-specification-driven",
        3: "3-test-first-development",
        4: "4-adaptive-tdd"
    }

    method_dir = Path(__file__).parent / method_dirs[method_num]
    module_path = method_dir / "haiku_converter.py"

    spec = importlib.util.spec_from_file_location(f"method{method_num}", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

# Demo story
DEMO_STORY = """In a small village nestled between mountains, an old woman
tended her garden every morning. She spoke to each plant as if they
were old friends, sharing stories of seasons past."""

def demo_method(method_num, story=DEMO_STORY):
    """Demo a single method with real Ollama."""

    method_names = {
        1: "Immediate Implementation",
        2: "Specification-Driven",
        3: "Test-First Development",
        4: "Adaptive TDD"
    }

    print(f"\n{'='*70}")
    print(f"METHOD {method_num}: {method_names[method_num]}")
    print(f"{'='*70}\n")

    try:
        # Load the implementation
        module = load_method(method_num)

        print("📖 Input Story:")
        print(f"   {story[:80]}...")
        print()

        # Time the real Ollama call
        print("🤖 Calling Ollama (llama3.2)...")
        start = time.time()

        # Real Ollama call - no mock!
        result = module.story_to_haiku(story)

        elapsed = time.time() - start

        # Display results
        print(f"✓  Generated in {elapsed:.1f}s\n")
        print("🎋 Haiku:")
        for i, line in enumerate(result['lines'], 1):
            syllables = result['syllable_counts'][i-1]
            target = [5, 7, 5][i-1]
            check = "✓" if syllables == target else f"({syllables})"
            print(f"   {line:40} {check}")

        print(f"\n   Syllable pattern: {result['syllable_counts']}")

        if 'essence' in result:
            print(f"   Captured essence: {result['essence'][:60]}...")

        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run live demo."""
    import argparse

    parser = argparse.ArgumentParser(description='Live demo with real Ollama')
    parser.add_argument('--method', type=int, choices=[1,2,3,4],
                       help='Demo specific method only')
    parser.add_argument('--story', type=str,
                       help='Custom story text')
    parser.add_argument('--quick', action='store_true',
                       help='Quick demo - only show Methods 1 and 4')

    args = parser.parse_args()

    # Header
    print("\n" + "="*70)
    print("STORY-TO-HAIKU LIVE DEMO")
    print("Experiment 1.608 - Ollama Integration")
    print("="*70)

    story = args.story if args.story else DEMO_STORY

    if args.method:
        # Single method
        success = demo_method(args.method, story)

    elif args.quick:
        # Quick demo - show fastest (Method 1) and best (Method 4)
        print("\n🚀 Quick Demo - Showing Methods 1 and 4")
        demo_method(1, story)
        demo_method(4, story)

    else:
        # All methods
        print("\n🎬 Full Demo - All 4 Methodologies\n")
        successes = 0

        for method_num in [1, 2, 3, 4]:
            if demo_method(method_num, story):
                successes += 1

            # Brief pause between methods
            if method_num < 4:
                time.sleep(0.5)

        # Summary
        print(f"\n{'='*70}")
        print(f"DEMO COMPLETE: {successes}/4 methods successful")
        print(f"{'='*70}\n")

    print("✨ Live demo finished!\n")

if __name__ == "__main__":
    main()