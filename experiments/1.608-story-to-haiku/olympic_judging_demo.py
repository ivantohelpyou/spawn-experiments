#!/usr/bin/env python3
"""
Olympic Judging Demo - Story-to-Haiku Converter
Experiment 1.608

This script:
1. Runs all methodology implementations with REAL Ollama for a specific run
2. Collects the haiku outputs
3. Has 3 judge models evaluate them (Olympic style)
4. Drops highest/lowest scores and averages
5. Declares a winner

Judge models: llama3.2, phi3:mini, gemma2:2b

Usage:
    python olympic_judging_demo.py --run 3
    python olympic_judging_demo.py --run 3 --methods 5  # For runs with 5 methods
"""

import sys
import time
import json
from pathlib import Path
import importlib.util

# Test story for comparison
DEMO_STORY = """In a small village nestled between mountains, an old woman
tended her garden every morning. She spoke to each plant as if they
were old friends, sharing stories of seasons past."""

def load_method(method_num, run_dir):
    """Load a method's haiku_converter module from specified run directory."""
    method_dirs = {
        1: "1-immediate-implementation",
        2: "2-specification-driven",
        3: "3-test-first-development",
        4: "4-selective-tdd",  # Updated name after methodology correction
        5: "5-adaptive-tdd"    # Correct Adaptive/Validated TDD
    }

    # Look in specified run directory
    method_dir = run_dir / method_dirs[method_num]
    module_path = method_dir / "haiku_converter.py"

    if not module_path.exists():
        raise FileNotFoundError(f"Method {method_num} not found at {module_path}")

    spec = importlib.util.spec_from_file_location(f"method{method_num}", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

def warmup_models(warmup_story="The sun rises over the mountains.", judge_models=['llama3.2', 'phi3:mini', 'gemma2:2b']):
    """
    Warm up ALL Ollama models (generator + judges) to eliminate cold-start bias.
    This ensures fair timing comparisons across all methods and judges.
    """
    import ollama

    print("="*70)
    print("MODEL WARM-UP (Trial 0 - Not Scored)")
    print("="*70)
    print(f"\n🔥 Warming up Ollama models...\n")

    # Warm up generator (llama3.2)
    print("Generator (llama3.2): ", end="", flush=True)
    try:
        module = load_method(1)
        start = time.time()
        result = module.story_to_haiku(warmup_story)
        elapsed = time.time() - start
        print(f"✓ ({elapsed:.1f}s)")
    except Exception as e:
        print(f"✗ {e}")

    # Warm up judge models
    for judge_model in judge_models:
        print(f"Judge ({judge_model}): ", end="", flush=True)
        try:
            start = time.time()
            response = ollama.generate(
                model=judge_model,
                prompt="Rate this haiku 1-10: Cherry blossoms fall / Softly on the quiet pond / Spring whispers arrive. Return JSON: {\"score\": 8}"
            )
            elapsed = time.time() - start
            print(f"✓ ({elapsed:.1f}s)")
        except Exception as e:
            print(f"✗ {e}")

    print(f"\n✅ All models warmed up and ready for timed trials.\n")

def generate_all_haiku(story, run_dir, num_methods=4, skip_warmup=False, delay_between_runs=2.0):
    """
    Generate haiku from all methods in specified run.

    Args:
        story: The story to convert to haiku
        run_dir: Path to the run directory (e.g., 3-clean-room)
        num_methods: Number of methods to test (4 or 5)
        skip_warmup: If True, skip model warm-up
        delay_between_runs: Seconds to wait between method calls (default 2.0)
    """

    # Warm up models first (unless skipped)
    if not skip_warmup:
        warmup_models()

    print("="*70)
    print(f"GENERATING HAIKU FROM ALL {num_methods} METHODOLOGIES")
    print("="*70)
    print(f"\n📖 Story: {story[:80]}...\n")
    if delay_between_runs > 0:
        print(f"⏱️  Delay between runs: {delay_between_runs}s (prevents Ollama serial call issues)\n")

    results = []

    for method_num in range(1, num_methods + 1):
        print(f"Method {method_num}: ", end="", flush=True)

        try:
            module = load_method(method_num, run_dir)
            start = time.time()
            result = module.story_to_haiku(story)
            elapsed = time.time() - start

            # Display haiku
            print(f"✓ ({elapsed:.1f}s)")
            for line in result['lines']:
                print(f"  {line}")
            print(f"  Syllables: {result['syllables']} {'✓' if result['valid'] else '✗'}")
            print()

            results.append({
                'method': method_num,
                'result': result,
                'time': elapsed
            })

        except Exception as e:
            print(f"✗ ERROR: {e}")
            results.append({
                'method': method_num,
                'error': str(e)
            })

        # Add delay between runs (except after last run)
        if delay_between_runs > 0 and method_num < num_methods:
            print(f"   Waiting {delay_between_runs}s before next run...\n")
            time.sleep(delay_between_runs)

    return results

def judge_haiku(story, all_results, judge_model='phi3:mini'):
    """
    Have a judge model rate all 4 haiku.

    Returns dict with scores and reasoning.
    """
    import ollama

    # Prepare haiku for judging
    haiku_texts = []
    for r in all_results:
        if 'error' in r:
            haiku_texts.append("[ERROR - No haiku generated]")
        else:
            haiku_texts.append(r['result']['haiku'])

    num_haiku = len(haiku_texts)

    prompt = f"""You are a distinguished poetry critic judging {num_haiku} haiku poems.

CRITICAL REQUIREMENT: Your scores MUST be differentiated. Look carefully for subtle differences in:
- Adherence to 5-7-5 syllable structure (worth 3 points)
- Poetic quality and imagery (worth 4 points)
- Emotional resonance and depth (worth 3 points)

The scores should vary - not all haiku are equally good. Be discerning and critical.

Haiku 1:
{haiku_texts[0]}

Haiku 2:
{haiku_texts[1]}

Haiku 3:
{haiku_texts[2]}

{chr(10).join(f"Haiku {i+1}:{chr(10)}{haiku}" for i, haiku in enumerate(haiku_texts))}

Return ONLY valid JSON in this format:
{{
  "scores": [{', '.join(f'score{i+1}' for i in range(num_haiku))}],
  "winner": N,
  "reasoning": "why this haiku is best"
}}
"""

    try:
        response = ollama.generate(model=judge_model, prompt=prompt)
        judgment = json.loads(response['response'].strip())
        return judgment
    except Exception as e:
        # Fallback: equal scores for all haiku
        num_haiku = len(haiku_texts)
        return {
            'scores': [5] * num_haiku,
            'winner': 1,
            'reasoning': f'Error in judging: {e}'
        }

def olympic_judging(story, all_results):
    """
    Olympic-style judging: 3 judges, drop highest/lowest, average.
    """
    print("\n" + "="*70)
    print("OLYMPIC JUDGING PHASE")
    print("="*70)

    judges = [
        ('llama3.2', 'Original generator - can it judge fairly?'),
        ('phi3:mini', 'Lightweight model - fresh perspective'),
        ('gemma2:2b', 'Google model - different training')
    ]

    all_judgments = []

    for judge_model, description in judges:
        print(f"\n🏅 Judge: {judge_model}")
        print(f"   {description}")
        print("   Judging", end="", flush=True)

        start = time.time()
        judgment = judge_haiku(story, all_results, judge_model)
        elapsed = time.time() - start

        print(f" ... done ({elapsed:.1f}s)")
        print(f"   Scores: {judgment['scores']}")
        print(f"   Prefers: Method {judgment['winner']}")

        all_judgments.append(judgment)

    return all_judgments

def calculate_final_scores(all_judgments, num_methods):
    """
    Olympic scoring: for each method, drop highest/lowest judge score, average the rest.
    """
    print("\n" + "="*70)
    print("FINAL SCORING (Olympic Style)")
    print("="*70)

    final_scores = []

    for method_idx in range(num_methods):
        method_num = method_idx + 1

        # Get this method's scores from all judges
        method_scores = [j['scores'][method_idx] for j in all_judgments]

        # Sort to find highest/lowest
        sorted_scores = sorted(method_scores)

        # Drop highest and lowest (Olympic style)
        if len(sorted_scores) > 2:
            middle_scores = sorted_scores[1:-1]
        else:
            middle_scores = sorted_scores

        # Average the middle scores
        final_score = sum(middle_scores) / len(middle_scores) if middle_scores else 0

        final_scores.append(final_score)

        print(f"\nMethod {method_num}:")
        print(f"  Judge scores: {method_scores}")
        print(f"  Dropped: {min(method_scores)}, {max(method_scores)}")
        print(f"  Final score: {final_score:.2f}")

    return final_scores

def announce_winner(all_results, final_scores):
    """Announce the winning haiku."""
    print("\n" + "="*70)
    print("🏆 WINNER ANNOUNCEMENT")
    print("="*70)

    winner_idx = final_scores.index(max(final_scores))
    winner_method = winner_idx + 1
    winner_score = final_scores[winner_idx]

    print(f"\n🥇 WINNER: Method {winner_method} with score {winner_score:.2f}/10")
    print(f"\n🎋 Winning Haiku:")

    winner_result = all_results[winner_idx]
    if 'error' not in winner_result:
        for line in winner_result['result']['lines']:
            print(f"   {line}")
        print(f"\n   Syllables: {winner_result['result']['syllables']}")
        print(f"   Essence: {winner_result['result']['essence']}")
        print(f"   Generation time: {winner_result['time']:.1f}s")

    # Show all scores for comparison
    print(f"\n📊 All Scores:")
    for i, score in enumerate(final_scores, 1):
        medal = "🥇" if i == winner_method else ("🥈" if score == sorted(final_scores)[-2] else ("🥉" if score == sorted(final_scores)[-3] else "  "))
        print(f"   {medal} Method {i}: {score:.2f}/10")

def main():
    """Run the complete olympic judging demo."""
    import argparse

    parser = argparse.ArgumentParser(description='Olympic judging demo for haiku quality')
    parser.add_argument('--run', type=int, required=True,
                       help='Run number to judge (e.g., 3 for 3-clean-room)')
    parser.add_argument('--methods', type=int, default=4, choices=[4, 5],
                       help='Number of methods to judge (4 or 5)')
    parser.add_argument('--story', type=str, help='Custom story text')
    parser.add_argument('--no-judging', action='store_true',
                       help='Generate haiku only, skip judging')
    parser.add_argument('--skip-warmup', action='store_true',
                       help='Skip model warm-up (Trial 0) - useful if model already warm')
    parser.add_argument('--delay', type=float, default=2.0,
                       help='Seconds to wait between method runs (default: 2.0, use 0 for no delay)')

    args = parser.parse_args()

    # Determine run directory
    run_dirs = {
        1: "1-initial-run",
        2: "2-structured-output",
        3: "3-clean-room",
        4: "4-next-run"  # Add as needed
    }

    if args.run not in run_dirs:
        print(f"❌ Error: Run {args.run} not found. Available runs: {list(run_dirs.keys())}")
        return

    run_dir = Path(__file__).parent / run_dirs[args.run]

    if not run_dir.exists():
        print(f"❌ Error: Run directory not found: {run_dir}")
        return

    story = args.story if args.story else DEMO_STORY

    print("\n" + "="*70)
    print("STORY-TO-HAIKU: OLYMPIC JUDGING DEMO")
    print(f"Experiment 1.608 - Run {args.run} ({run_dirs[args.run]})")
    print(f"Methods: {args.methods}")
    print("="*70)

    # Phase 1: Generate all haiku
    start_total = time.time()
    all_results = generate_all_haiku(story, run_dir, num_methods=args.methods,
                                     skip_warmup=args.skip_warmup,
                                     delay_between_runs=args.delay)

    # Check if any succeeded
    successful = [r for r in all_results if 'error' not in r]
    if not successful:
        print("\n❌ No methods succeeded - cannot proceed with judging")
        return

    if args.no_judging:
        print("\n✅ Generation complete (judging skipped)")
        return

    # Phase 2: Olympic judging
    all_judgments = olympic_judging(story, all_results)

    # Phase 3: Calculate final scores
    final_scores = calculate_final_scores(all_judgments, args.methods)

    # Phase 4: Announce winner
    announce_winner(all_results, final_scores)

    elapsed_total = time.time() - start_total
    print(f"\n⏱️  Total time: {elapsed_total:.1f}s")
    print("\n✨ Demo complete!\n")

if __name__ == "__main__":
    main()
