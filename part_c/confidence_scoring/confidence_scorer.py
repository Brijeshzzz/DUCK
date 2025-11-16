"""
C5: Confidence Score Calculator
Calculates final confidence scores for TOR path correlations
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfidenceScorer:
    """Calculates confidence scores for correlations"""
    
    # Scoring weights (must add up to 100)
    WEIGHTS = {
        'timing': 40,      # Timing correlation weight
        'volume': 30,      # Volume correlation weight
        'pattern': 20,     # Pattern matching weight
        'behavior': 10     # Behavioral analysis weight
    }
    
    def __init__(self):
        logger.info("Confidence Scorer initialized")
    
    def calculate_timing_score(self, timing_data):
        """
        Score based on timing correlation
        
        Args:
            timing_data: {
                'time_diff': seconds between entry and exit,
                'expected_latency': expected TOR latency (2-5 seconds)
            }
        """
        time_diff = timing_data.get('time_diff', 999)
        expected = timing_data.get('expected_latency', 3.5)
        
        # Perfect score if within expected range (2-5 seconds)
        if 2 <= time_diff <= 5:
            score = 100
        elif 1 <= time_diff <= 10:
            # Partial score if close
            deviation = abs(time_diff - expected)
            score = max(0, 100 - (deviation * 20))
        else:
            score = 0
        
        return min(100, score)
    
    def calculate_volume_score(self, volume_data):
        """
        Score based on volume correlation
        
        Args:
            volume_data: {
                'entry_bytes': bytes sent through entry,
                'exit_bytes': bytes from exit,
                'tolerance': acceptable difference (0.15 = 15%)
            }
        """
        entry_bytes = volume_data.get('entry_bytes', 0)
        exit_bytes = volume_data.get('exit_bytes', 0)
        tolerance = volume_data.get('tolerance', 0.15)
        
        if entry_bytes == 0 or exit_bytes == 0:
            return 0
        
        # Calculate percentage difference
        diff = abs(entry_bytes - exit_bytes)
        percent_diff = diff / max(entry_bytes, exit_bytes)
        
        if percent_diff <= tolerance:
            # Within tolerance = high score
            score = 100 - (percent_diff / tolerance * 20)
        else:
            # Beyond tolerance = low score
            score = max(0, 100 - (percent_diff * 100))
        
        return min(100, score)
    
    def calculate_pattern_score(self, pattern_data):
        """
        Score based on pattern matching
        
        Args:
            pattern_data: {
                'similarity': 0-100 similarity percentage,
                'cell_match': True if TOR cells detected,
                'burst_match': True if burst patterns match
            }
        """
        similarity = pattern_data.get('similarity', 0)
        cell_match = pattern_data.get('cell_match', False)
        burst_match = pattern_data.get('burst_match', False)
        
        score = similarity * 0.6  # 60% weight on similarity
        
        if cell_match:
            score += 20  # Bonus for TOR cell detection
        
        if burst_match:
            score += 20  # Bonus for burst pattern match
        
        return min(100, score)
    
    def calculate_behavior_score(self, behavior_data):
        """
        Score based on behavioral analysis
        
        Args:
            behavior_data: {
                'profile_match': True if matches user's typical behavior,
                'time_of_day_match': True if typical usage time,
                'country_preference_match': True if typical exit country
            }
        """
        score = 50  # Base score
        
        if behavior_data.get('profile_match'):
            score += 20
        
        if behavior_data.get('time_of_day_match'):
            score += 15
        
        if behavior_data.get('country_preference_match'):
            score += 15
        
        return min(100, score)
    
    def calculate_final_confidence(self, timing_data=None, volume_data=None, 
                                   pattern_data=None, behavior_data=None):
        """
        Calculate weighted final confidence score
        
        Returns:
            {
                'final_score': 0-100,
                'level': 'high'/'medium'/'low',
                'breakdown': individual scores
            }
        """
        scores = {}
        
        # Calculate individual scores
        if timing_data:
            scores['timing'] = self.calculate_timing_score(timing_data)
        else:
            scores['timing'] = 0
        
        if volume_data:
            scores['volume'] = self.calculate_volume_score(volume_data)
        else:
            scores['volume'] = 0
        
        if pattern_data:
            scores['pattern'] = self.calculate_pattern_score(pattern_data)
        else:
            scores['pattern'] = 0
        
        if behavior_data:
            scores['behavior'] = self.calculate_behavior_score(behavior_data)
        else:
            scores['behavior'] = 50  # Neutral if no data
        
        # Calculate weighted final score
        final_score = (
            scores['timing'] * self.WEIGHTS['timing'] / 100 +
            scores['volume'] * self.WEIGHTS['volume'] / 100 +
            scores['pattern'] * self.WEIGHTS['pattern'] / 100 +
            scores['behavior'] * self.WEIGHTS['behavior'] / 100
        )
        
        # Determine confidence level
        if final_score >= 80:
            level = 'high'
        elif final_score >= 60:
            level = 'medium'
        else:
            level = 'low'
        
        logger.info(f"Final confidence: {final_score:.1f}% ({level})")
        
        return {
            'final_score': round(final_score, 2),
            'level': level,
            'breakdown': scores
        }


def main():
    """Test confidence scoring"""
    print("="*70)
    print("PART C - C5: Confidence Score Calculator")
    print("="*70)
    
    scorer = ConfidenceScorer()
    
    # Test with sample data
    timing_data = {'time_diff': 3.2, 'expected_latency': 3.5}
    volume_data = {'entry_bytes': 5000, 'exit_bytes': 5200, 'tolerance': 0.15}
    pattern_data = {'similarity': 75, 'cell_match': True, 'burst_match': True}
    behavior_data = {'profile_match': True, 'time_of_day_match': True, 'country_preference_match': False}
    
    print("\nCalculating confidence score...")
    result = scorer.calculate_final_confidence(
        timing_data=timing_data,
        volume_data=volume_data,
        pattern_data=pattern_data,
        behavior_data=behavior_data
    )
    
    print(f"\n{'='*70}")
    print("CONFIDENCE SCORE BREAKDOWN")
    print(f"{'='*70}")
    print(f"Timing Score:    {result['breakdown']['timing']:.1f}/100 (weight: {scorer.WEIGHTS['timing']}%)")
    print(f"Volume Score:    {result['breakdown']['volume']:.1f}/100 (weight: {scorer.WEIGHTS['volume']}%)")
    print(f"Pattern Score:   {result['breakdown']['pattern']:.1f}/100 (weight: {scorer.WEIGHTS['pattern']}%)")
    print(f"Behavior Score:  {result['breakdown']['behavior']:.1f}/100 (weight: {scorer.WEIGHTS['behavior']}%)")
    
    print(f"\n{'='*70}")
    print(f"FINAL CONFIDENCE: {result['final_score']}% ({result['level'].upper()})")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
