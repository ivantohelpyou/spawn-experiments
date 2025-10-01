#!/usr/bin/env python3
"""
End-to-end test for limerick converter.
"""
import json
from limerick_converter import LimerickConverter

def main():
    print("=" * 60)
    print("LIMERICK CONVERTER - END-TO-END TEST")
    print("=" * 60)
    
    converter = LimerickConverter()
    
    story = """
    A programmer stayed up all night debugging their code.
    They searched through thousands of lines, checking every function.
    Finally, at 3 AM, they found it - a missing semicolon.
    Exhausted but relieved, they fixed it and went to sleep.
    """
    
    print("\nINPUT STORY:")
    print(story.strip())
    print("\n" + "=" * 60)
    print("CONVERTING TO LIMERICK...")
    print("=" * 60 + "\n")
    
    try:
        result_json = converter.convert(story)
        result = json.loads(result_json)
        
        print("GENERATED LIMERICK:")
        print("-" * 60)
        print(result["limerick"]["text"])
        print("-" * 60)
        
        print("\nVALIDATION RESULTS:")
        validation = result["validation"]
        print(f"  Valid: {validation['valid']}")
        print(f"  Syllable counts: {validation['syllable_counts']}")
        if validation['errors']:
            print("  Errors:")
            for error in validation['errors']:
                print(f"    - {error}")
        else:
            print("  ✓ No validation errors!")
        
        print("\n" + "=" * 60)
        print("TEST COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
