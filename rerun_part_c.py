"""
Re-run Part C with volume data to get correct confidence
"""

import sys
import json
sys.path.insert(0, '.')

from part_c.pattern_analysis.pattern_analyzer import PatternAnalyzer
from part_c.confidence_scoring.confidence_scorer import ConfidenceScorer

print("="*70)
print("RE-CALCULATING CONFIDENCE WITH VOLUME DATA")
print("="*70)

# Load volume correlation
try:
    with open('part_b/logs/volume_correlations.json', 'r') as f:
        volume_results = json.load(f)
    
    volume_diff = volume_results[0]['volume_difference']
    print(f"\n✓ Volume correlation loaded: {volume_diff}")
    
    volume_data = {
        'entry_bytes': 5000,
        'exit_bytes': int(5000 * (1 + volume_diff)),
        'tolerance': 0.15
    }
except:
    print("\n✗ Volume correlation file not found")
    volume_data = None

# Prepare other data
timing_data = {'time_diff': 999, 'expected_latency': 3.5}

pattern_data = {
    'similarity': 100,  # You had 100% pattern match!
    'cell_match': True,  # 100% TOR cells detected
    'burst_match': True
}

behavior_data = {
    'profile_match': False,
    'time_of_day_match': False,
    'country_preference_match': False
}

# Calculate confidence
scorer = ConfidenceScorer()
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

print("\n📊 WHAT CHANGED:")
print(f"  Before: 21% (Volume score = 0)")
print(f"  After:  {result['final_score']:.1f}% (Volume score = {result['breakdown']['volume']:.1f})")
