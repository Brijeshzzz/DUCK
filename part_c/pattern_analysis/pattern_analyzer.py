"""
C1: Packet Pattern Analysis
Analyzes packet size sequences and timing patterns
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import logging
from collections import Counter
import statistics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PatternAnalyzer:
    """Analyzes traffic patterns for fingerprinting"""
    
    def __init__(self):
        self.patterns = []
        logger.info("Pattern Analyzer initialized")
    
    def extract_packet_sizes(self, packets):
        """Extract packet size sequence"""
        return [p.get('size', 0) for p in packets]
    
    def extract_timing_pattern(self, packets):
        """Extract inter-packet arrival times"""
        if len(packets) < 2:
            return []
        
        times = [self._parse_timestamp(p.get('timestamp')) for p in packets]
        times.sort()
        
        # Calculate differences
        intervals = []
        for i in range(1, len(times)):
            diff = (times[i] - times[0]).total_seconds()
            intervals.append(diff)
        
        return intervals
    
    def _parse_timestamp(self, timestamp_str):
        from datetime import datetime
        try:
            return datetime.fromisoformat(timestamp_str)
        except:
            return datetime.now()
    
    def detect_tor_cells(self, packet_sizes):
        """
        Detect TOR's fixed 512-byte cells
        TOR uses 512-byte cells, creating distinctive patterns
        """
        cell_size = 512
        cell_multiples = 0
        
        for size in packet_sizes:
            if size == cell_size or size % cell_size == 0:
                cell_multiples += 1
        
        cell_ratio = cell_multiples / len(packet_sizes) if packet_sizes else 0
        
        logger.info(f"TOR cell pattern: {cell_ratio*100:.1f}% packets match 512-byte cells")
        
        return {
            'cell_matches': cell_multiples,
            'total_packets': len(packet_sizes),
            'cell_ratio': cell_ratio,
            'is_tor_pattern': cell_ratio > 0.3  # >30% match = likely TOR
        }
    
    def analyze_burst_pattern(self, timing_intervals):
        """
        Analyze traffic bursts
        TOR has distinctive burst patterns
        """
        if len(timing_intervals) < 3:
            return {'has_bursts': False}
        
        # Find clusters of packets (bursts)
        burst_threshold = 0.1  # 100ms
        bursts = []
        current_burst = []
        
        for interval in timing_intervals:
            if interval < burst_threshold:
                current_burst.append(interval)
            else:
                if current_burst:
                    bursts.append(len(current_burst))
                current_burst = []
        
        if current_burst:
            bursts.append(len(current_burst))
        
        logger.info(f"Detected {len(bursts)} traffic bursts")
        
        return {
            'has_bursts': len(bursts) > 0,
            'burst_count': len(bursts),
            'avg_burst_size': statistics.mean(bursts) if bursts else 0
        }
    
    def compare_patterns(self, pattern1, pattern2):
        """
        Compare two packet patterns for similarity
        Returns similarity score 0-100
        """
        if not pattern1 or not pattern2:
            return 0
        
        # Simple comparison: how many packets match
        min_len = min(len(pattern1), len(pattern2))
        matches = sum(1 for i in range(min_len) 
                     if abs(pattern1[i] - pattern2[i]) < 50)  # 50 byte tolerance
        
        similarity = (matches / min_len) * 100 if min_len > 0 else 0
        
        return round(similarity, 2)
    
    def analyze_traffic(self, entry_packets, exit_packets):
        """
        Complete pattern analysis of entry and exit traffic
        """
        results = {
            'entry_analysis': {},
            'exit_analysis': {},
            'correlation': {}
        }
        
        # Analyze entry traffic
        entry_sizes = self.extract_packet_sizes(entry_packets)
        entry_timing = self.extract_timing_pattern(entry_packets)
        
        results['entry_analysis'] = {
            'packet_count': len(entry_packets),
            'size_pattern': entry_sizes[:10],  # First 10 packets
            'tor_cells': self.detect_tor_cells(entry_sizes),
            'bursts': self.analyze_burst_pattern(entry_timing)
        }
        
        # Analyze exit traffic
        exit_sizes = self.extract_packet_sizes(exit_packets)
        exit_timing = self.extract_timing_pattern(exit_packets)
        
        results['exit_analysis'] = {
            'packet_count': len(exit_packets),
            'size_pattern': exit_sizes[:10],
            'tor_cells': self.detect_tor_cells(exit_sizes),
            'bursts': self.analyze_burst_pattern(exit_timing)
        }
        
        # Compare patterns
        pattern_similarity = self.compare_patterns(entry_sizes, exit_sizes)
        
        results['correlation'] = {
            'pattern_similarity': pattern_similarity,
            'likely_correlated': pattern_similarity > 60
        }
        
        logger.info(f"Pattern analysis complete - Similarity: {pattern_similarity}%")
        
        return results


def main():
    """Test pattern analysis"""
    print("="*70)
    print("PART C - C1: Packet Pattern Analysis")
    print("="*70)
    
    analyzer = PatternAnalyzer()
    
    # Test with sample traffic
    entry_packets = [
        {'size': 512, 'timestamp': '2025-11-11T10:00:00.000'},
        {'size': 512, 'timestamp': '2025-11-11T10:00:00.100'},
        {'size': 200, 'timestamp': '2025-11-11T10:00:00.200'},
        {'size': 512, 'timestamp': '2025-11-11T10:00:00.300'},
    ]
    
    exit_packets = [
        {'size': 512, 'timestamp': '2025-11-11T10:00:02.000'},
        {'size': 512, 'timestamp': '2025-11-11T10:00:02.100'},
        {'size': 200, 'timestamp': '2025-11-11T10:00:02.200'},
        {'size': 512, 'timestamp': '2025-11-11T10:00:02.300'},
    ]
    
    print("\nAnalyzing traffic patterns...")
    results = analyzer.analyze_traffic(entry_packets, exit_packets)
    
    print(f"\n{'='*70}")
    print("ENTRY TRAFFIC ANALYSIS")
    print(f"{'='*70}")
    print(f"Packets: {results['entry_analysis']['packet_count']}")
    print(f"TOR Cell Ratio: {results['entry_analysis']['tor_cells']['cell_ratio']*100:.1f}%")
    print(f"TOR Pattern Detected: {results['entry_analysis']['tor_cells']['is_tor_pattern']}")
    
    print(f"\n{'='*70}")
    print("EXIT TRAFFIC ANALYSIS")
    print(f"{'='*70}")
    print(f"Packets: {results['exit_analysis']['packet_count']}")
    print(f"TOR Cell Ratio: {results['exit_analysis']['tor_cells']['cell_ratio']*100:.1f}%")
    
    print(f"\n{'='*70}")
    print("PATTERN CORRELATION")
    print(f"{'='*70}")
    print(f"Similarity: {results['correlation']['pattern_similarity']}%")
    print(f"Likely Correlated: {results['correlation']['likely_correlated']}")


if __name__ == "__main__":
    main()
