"""
B4: Volume Correlation
Matches entry and exit node connections based on data volume similarity
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

class VolumeCorrelation:
    def __init__(self, entries, exits):
        """
        entries: list of entry node connections with 'volume' keys (e.g., bytes transferred)
        exits: list of exit node connections with 'volume' keys
        """
        self.entries = entries
        self.exits = exits
        self.volume_tolerance = config['VOLUME_TOLERANCE']
    
    def correlate(self):
        correlations = []
        for entry in self.entries:
            entry_volume = entry.get('volume', 0)
            for exit in self.exits:
                exit_volume = exit.get('volume', 0)
                if entry_volume == 0 or exit_volume == 0:
                    continue
                # Calculate relative difference
                diff = abs(entry_volume - exit_volume) / max(entry_volume, exit_volume)
                if diff <= self.volume_tolerance:
                    logger.info(f"Volume match found: Entry volume {entry_volume} and Exit volume {exit_volume} with diff {diff:.2f}")
                    correlations.append({
                        'entry': entry,
                        'exit': exit,
                        'volume_difference': diff
                    })
        return correlations

def main():
    # Example test data, replace with real volume info
    entries = [
        {
            'entry_node': {'ip_address': '83.108.59.221', 'country': 'Norway'},
            'timestamp': '2025-11-11T20:11:59.108212',
            'user_ip': '192.168.1.100',
            'volume': 1024000  # bytes
        }
    ]
    exits = [
        {
            'exit_node': {'ip_address': '204.137.14.106', 'country': 'United States of America'},
            'timestamp': '2025-11-11T20:12:18.227362',
            'destination': '172.217.14.206',
            'volume': 1000000  # bytes
        }
    ]
    
    correlator = VolumeCorrelation(entries, exits)
    correlated_paths = correlator.correlate()
    
    print(f"\nVolume Correlation Results: {len(correlated_paths)} matches found.\n")
    for i, c in enumerate(correlated_paths, 1):
        print(f"Match {i}:")
        print(f"  Entry Node IP: {c['entry']['entry_node']['ip_address']} ({c['entry']['entry_node']['country']})")
        print(f"  Exit Node IP: {c['exit']['exit_node']['ip_address']} ({c['exit']['exit_node']['country']})")
        print(f"  Volume Difference: {c['volume_difference']:.2f}\n")

if __name__ == "__main__":
    main()
