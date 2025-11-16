"""
B5: Path Reconstruction
Builds the complete TOR path from correlated entry and exit connections
"""

import logging
import os

# Load configuration
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.py"))
config = {}
with open(config_path) as f:
    exec(f.read(), config)

logging.basicConfig(filename=config['LOG_FILE'], level=getattr(logging, config['LOG_LEVEL']))
logger = logging.getLogger(__name__)

class PathReconstruction:
    def __init__(self, timing_matches, volume_matches):
        """
        timing_matches: list of dicts with 'entry', 'exit', 'time_difference'
        volume_matches: list of dicts with 'entry', 'exit', 'volume_difference'
        """
        self.timing_matches = timing_matches
        self.volume_matches = volume_matches
        self.min_confidence = config['MIN_CONFIDENCE_FOR_PATH']
        self.max_relay_hops = config['MAX_RELAY_HOPS']
    
    def calculate_confidence(self, timing_diff, volume_diff):
        # Weighted confidence calculation based on config weights
        timing_score = max(0, 1 - timing_diff / config['TIMING_WINDOW']) * config['TIMING_WEIGHT']
        volume_score = max(0, 1 - volume_diff / config['VOLUME_TOLERANCE']) * config['VOLUME_WEIGHT']
        # Simple addition for confident score; can be expanded with other factors
        confidence = timing_score + volume_score
        return confidence
    
    def reconstruct_paths(self):
        paths = []
        for t_match in self.timing_matches:
            for v_match in self.volume_matches:
                if (t_match['entry'] == v_match['entry'] and 
                    t_match['exit'] == v_match['exit']):
                    
                    confidence = self.calculate_confidence(t_match['time_difference'], v_match['volume_difference'])
                    logger.info(f"Reconstructed path with confidence {confidence:.2f}")
                    
                    if confidence >= self.min_confidence:
                        # Simulate path including middle relays (can be extended to real data)
                        path = {
                            'entry_node': t_match['entry']['entry_node'],
                            'exit_node': t_match['exit']['exit_node'],
                            'middle_relays': ['Unknown Relay 1', 'Unknown Relay 2'],  # Placeholder
                            'confidence': confidence,
                            'user_ip': t_match['entry']['user_ip'],
                            'destination': t_match['exit'].get('destination', 'Unknown')
                        }
                        paths.append(path)
        return paths

def main():
    # Demo data - replace with real correlated matches
    timing_matches = [
        {
            'entry': {
                'entry_node': {'ip_address': '83.108.59.221', 'country': 'Norway'},
                'timestamp': '2025-11-11T20:11:59.108212',
                'user_ip': '192.168.1.100'
            },
            'exit': {
                'exit_node': {'ip_address': '204.137.14.106', 'country': 'United States of America'},
                'timestamp': '2025-11-11T20:12:18.227362',
                'destination': '172.217.14.206'
            },
            'time_difference': 19.12
        }
    ]
    volume_matches = [
        {
            'entry': {
                'entry_node': {'ip_address': '83.108.59.221', 'country': 'Norway'},
                'timestamp': '2025-11-11T20:11:59.108212',
                'user_ip': '192.168.1.100',
                'volume': 1024000
            },
            'exit': {
                'exit_node': {'ip_address': '204.137.14.106', 'country': 'United States of America'},
                'timestamp': '2025-11-11T20:12:18.227362',
                'destination': '172.217.14.206',
                'volume': 1000000
            },
            'volume_difference': 0.02
        }
    ]
    
    reconstructor = PathReconstruction(timing_matches, volume_matches)
    paths = reconstructor.reconstruct_paths()
    
    print(f"\nPath Reconstruction Results: {len(paths)} paths found.\n")
    for i, path in enumerate(paths, 1):
        print(f"Path {i}:")
        print(f"  Entry Node: {path['entry_node']['ip_address']} ({path['entry_node']['country']})")
        print(f"  Middle Relays: {', '.join(path['middle_relays'])}")
        print(f"  Exit Node: {path['exit_node']['ip_address']} ({path['exit_node']['country']})")
        print(f"  User IP: {path['user_ip']}")
        print(f"  Destination: {path['destination']}")
        print(f"  Confidence: {path['confidence']:.2f}\n")

if __name__ == "__main__":
    main()
