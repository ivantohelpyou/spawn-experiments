#!/usr/bin/env python3
"""Test script to see what judges actually returned"""

import json

# The 4 haiku that were generated
haiku_texts = [
    """gentle woman
talking greens thrive
nature's love""",
    """Garden tales told
Seasons shared with plants
Friendship in green""",
    """Garden whispers
Stories shared with green
Nature's gentle soul""",
    """Misty village
Sharing stories
Garden's gentle hush"""
]

story = """In a small village nestled between mountains, an old woman
tended her garden every morning. She spoke to each plant as if they
were old friends, sharing stories of seasons past."""

def test_judge(judge_model):
    """Test what a judge actually returns"""
    import ollama

    prompt = f"""You are a distinguished poetry critic judging 4 haiku poems.

Rate each haiku with a score from 1-10 based on:
- Adherence to 5-7-5 syllable structure (worth 3 points)
- Poetic quality and imagery (worth 4 points)
- Emotional resonance and depth (worth 3 points)

Haiku 1:
{haiku_texts[0]}

Haiku 2:
{haiku_texts[1]}

Haiku 3:
{haiku_texts[2]}

Haiku 4:
{haiku_texts[3]}

Return ONLY valid JSON in this format:
{{
  "scores": [score1, score2, score3, score4],
  "winner": N,
  "reasoning": "why this haiku is best"
}}
"""

    print(f"\n{'='*70}")
    print(f"Testing Judge: {judge_model}")
    print(f"{'='*70}")

    try:
        response = ollama.generate(model=judge_model, prompt=prompt)
        print(f"\nRaw response:\n{response['response']}")
        print(f"\n{'-'*70}")

        judgment = json.loads(response['response'].strip())
        print(f"\nParsed JSON:")
        print(json.dumps(judgment, indent=2))

        return judgment
    except Exception as e:
        print(f"\nError: {e}")
        return None

if __name__ == "__main__":
    judges = ['llama3.2', 'phi3:mini', 'gemma2:2b']

    all_judgments = []
    for judge in judges:
        judgment = test_judge(judge)
        if judgment:
            all_judgments.append(judgment)

    print(f"\n\n{'='*70}")
    print("SUMMARY OF ALL JUDGMENTS")
    print(f"{'='*70}")
    for i, judge in enumerate(judges[:len(all_judgments)]):
        print(f"\n{judge}:")
        print(f"  Scores: {all_judgments[i]['scores']}")
        print(f"  Winner: Method {all_judgments[i]['winner']}")
        print(f"  Reasoning: {all_judgments[i]['reasoning']}")
