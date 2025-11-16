"""
B3: Timing Correlation
Matches entry and exit node connections based on timing proximity
"""

from datetime import datetime, timedelta
import logging
import os

# Load configuration
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.py"))
config = {}
with open(config_path) as f:
    exec(f.read(), config)

logging.basicConfig(filename=config['LOG_FILE'], level=getattr(logging, config['LOG_LEVEL']))
logger = logging.getLogger(__name__)

class TimingCorrelation:
    def __init__(self, entries, exits):
        """
        entries: list of entry node connection dicts with 'timestamp' keys
        exits: list of exit node connection dicts with 'timestamp' keys
        """
        self.entries = entries
        self.exits = exits
        self.timing_window = config['TIMING_WINDOW']
        self.timing_tolerance = config['TIMING_TOLERANCE']
    
    def correlate(self):
        correlations = []
        for entry in self.entries:
            entry_time = datetime.fromisoformat(entry['timestamp'])
            for exit in self.exits:
                exit_time = datetime.fromisoformat(exit['timestamp'])
                delta = abs((exit_time - entry_time).total_seconds())
                
                if delta <= self.timing_window + self.timing_tolerance:
                    logger.info(f"Timing match found: Entry {entry['entry_node']['ip_address']} and Exit {exit['exit_node']['ip_address']} with delta {delta:.2f} seconds")
                    correlations.append({
                        'entry': entry,
                        'exit': exit,
                        'time_difference': delta
                    })
        return correlations

def main():
    # Example test entries and exits, replace these with real detections
    entries = [
        {
            'entry_node': {'ip_address': '83.108.59.221', 'country': 'Norway'},
            'timestamp': '2025-11-11T20:11:59.108212',
            'user_ip': '192.168.1.100'
        }
    ]
    exits = [
        {
            'exit_node': {'ip_address': '204.137.14.106', 'country': 'United States of America'},
            'timestamp': '2025-11-11T20:12:18.227362',
            'destination': '172.217.14.206'
        }
    ]
    
    correlator = TimingCorrelation(entries, exits)
    correlated_paths = correlator.correlate()
    
    print(f"\nTiming Correlation Results: {len(correlated_paths)} matches found.\n")
    for i, c in enumerate(correlated_paths, 1):
        print(f"Match {i}:")
        print(f"  Entry Node IP: {c['entry']['entry_node']['ip_address']} ({c['entry']['entry_node']['country']})")
        print(f"  Exit Node IP: {c['exit']['exit_node']['ip_address']} ({c['exit']['exit_node']['country']})")
        print(f"  Time Difference (s): {c['time_difference']:.2f}\n")

if __name__ == "__main__":
    main()
