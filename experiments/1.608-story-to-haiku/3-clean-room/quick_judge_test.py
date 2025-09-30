#!/usr/bin/env python3
"""Quick test - single judge"""

import json
import ollama

haiku_texts = [
    "gentle woman\ntalking greens thrive\nnature's love",
    "Garden tales told\nSeasons shared with plants\nFriendship in green",
    "Garden whispers\nStories shared with green\nNature's gentle soul",
    "Misty village\nSharing stories\nGarden's gentle hush"
]

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

print("Testing llama3.2 judge...")
response = ollama.generate(model='llama3.2', prompt=prompt)
print("\nRaw response:")
print(response['response'])
print("\n" + "="*70)

try:
    judgment = json.loads(response['response'].strip())
    print("\nParsed successfully:")
    print(json.dumps(judgment, indent=2))
except Exception as e:
    print(f"\nFailed to parse: {e}")
