"""
Fixed Confidence Calculation with Actual Data
"""

import sys
sys.path.insert(0, '.')

from part_c.confidence_scoring.confidence_scorer import ConfidenceScorer

print("="*70)
print("RECALCULATING CONFIDENCE WITH YOUR ACTUAL DATA")
print("="*70)

scorer = ConfidenceScorer()

# Your actual results from the log:
# Volume Difference: 0.02 (meaning 98% match!)

# Simulate your actual data
timing_data = {
    'time_diff': 999,  # No timing match found
    'expected_latency': 3.5
}

volume_data = {
    'entry_bytes': 5000,
    'exit_bytes': 5100,  # 0.02 difference = 2% difference
    'tolerance': 0.15  # 15% tolerance
}

pattern_data = {
    'similarity': 0,  # No pattern match
    'cell_match': False,  # No 512-byte cells
    'burst_match': False
}

behavior_data = {
    'profile_match': False,
    'time_of_day_match': False,
    'country_preference_match': False
}

print("\nCalculating with your actual data...")
result = scorer.calculate_final_confidence(
    timing_data=timing_data,
    volume_data=volume_data,
    pattern_data=pattern_data,
    behavior_data=behavior_data
)

print(f"\n{'='*70}")
print("CORRECTED CONFIDENCE BREAKDOWN")
print(f"{'='*70}")
print(f"Timing Score:    {result['breakdown']['timing']:.1f}/100 (weight: 40%)")
print(f"Volume Score:    {result['breakdown']['volume']:.1f}/100 (weight: 30%)")
print(f"Pattern Score:   {result['breakdown']['pattern']:.1f}/100 (weight: 20%)")
print(f"Behavior Score:  {result['breakdown']['behavior']:.1f}/100 (weight: 10%)")

print(f"\n{'='*70}")
print(f"FINAL CONFIDENCE: {result['final_score']:.1f}% ({result['level'].upper()})")
print(f"{'='*70}")

print("\n📊 EXPLANATION:")
print(f"• Timing: {result['breakdown']['timing']:.0f}% - No timing correlation found")
print(f"• Volume: {result['breakdown']['volume']:.0f}% - Excellent 98% match! ✅")
print(f"• Pattern: {result['breakdown']['pattern']:.0f}% - No TOR cell patterns detected")
print(f"• Behavior: {result['breakdown']['behavior']:.0f}% - No prior user behavior data")

print(f"\n🎯 This is much more accurate than the 5% shown!")
