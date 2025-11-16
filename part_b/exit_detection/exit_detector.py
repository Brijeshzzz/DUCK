"""
B2: Exit Node Detection
Identifies which TOR exit node accessed the destination
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from part_a.tor_database.fetch_nodes import TORDatabase
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExitNodeDetector:
    """Detects exit nodes in captured traffic"""
    
    def __init__(self):
        self.tor_db = TORDatabase()
        self.tor_db.load_from_file()
        self.exit_nodes = self.tor_db.get_exit_nodes()
        logger.info(f"Loaded {len(self.exit_nodes)} exit nodes")
    
    def identify_exit_node(self, packet_info):
        """
        Identify if packet is coming from a TOR exit node
        
        Args:
            packet_info: {
                'src_ip': source IP (possibly TOR exit),
                'dst_ip': destination IP (target server),
                'timestamp': when connection made
            }
        
        Returns:
            {
                'is_exit': True/False,
                'exit_node': node info if found,
                'destination': target server IP,
                'timestamp': connection time
            }
        """
        src_ip = packet_info.get('src_ip')
        
        # Check if source is a known exit node
        for node in self.exit_nodes:
            if node['ip_address'] == src_ip and node['running']:
                logger.info(f"✓ Exit node detected: {src_ip} ({node['country']})")
                
                return {
                    'is_exit': True,
                    'exit_node': node,
                    'destination': packet_info.get('dst_ip'),
                    'timestamp': packet_info.get('timestamp'),
                    'connection': {
                        'src_port': packet_info.get('src_port'),
                        'dst_port': packet_info.get('dst_port')
                    }
                }
        
        return {
            'is_exit': False,
            'exit_node': None
        }
    
    def find_all_exits(self, captured_packets):
        """
        Find all exit node connections in captured traffic
        
        Args:
            captured_packets: List of packet info dictionaries
        
        Returns:
            List of exit node detections
        """
        exits = []
        
        for packet in captured_packets:
            result = self.identify_exit_node(packet)
            if result['is_exit']:
                exits.append(result)
        
        logger.info(f"Found {len(exits)} exit node connections")
        return exits


def main():
    """Test exit node detection"""
    print("="*70)
    print("PART B - B2: Exit Node Detection")
    print("="*70)
    
    detector = ExitNodeDetector()
    
    # Test with sample packets
    test_packets = [
        {
            'src_ip': detector.exit_nodes[0]['ip_address'] if detector.exit_nodes else '1.2.3.4',
            'dst_ip': '172.217.14.206',  # Example destination
            'src_port': 9001,
            'dst_port': 443,
            'timestamp': datetime.now().isoformat()
        },
        {
            'src_ip': '8.8.8.8',  # Not TOR
            'dst_ip': '1.1.1.1',
            'src_port': 443,
            'dst_port': 50001,
            'timestamp': datetime.now().isoformat()
        }
    ]
    
    print(f"\nTesting with {len(test_packets)} packets...")
    exits = detector.find_all_exits(test_packets)
    
    print(f"\n{'='*70}")
    print(f"RESULTS: {len(exits)} exit nodes detected")
    print(f"{'='*70}")
    
    for i, exit_node in enumerate(exits, 1):
        print(f"\nExit {i}:")
        print(f"  Exit Node: {exit_node['exit_node']['ip_address']}")
        print(f"  Country: {exit_node['exit_node']['country_name']}")
        print(f"  Destination: {exit_node['destination']}")
        print(f"  Timestamp: {exit_node['timestamp']}")


if __name__ == "__main__":
    main()

import json

def save_exit_timestamps(exits):
    timestamps = [exit['timestamp'] for exit in exits]
    with open("part_b/logs/exit_timestamps.json", "w") as f:
        json.dump(timestamps, f, indent=4)

# After exits are found in find_all_exits(), add:
# save_exit_timestamps(exits)

# Add this call inside the main() after find_all_exits test like:

if __name__ == "__main__":
    main()
    # Save timestamps from test exits run:
    detector = ExitNodeDetector()
    test_packets = [
        {
            'src_ip': detector.exit_nodes[0]['ip_address'] if detector.exit_nodes else '1.2.3.4',
            'dst_ip': '172.217.14.206',  # Example destination
            'src_port': 9001,
            'dst_port': 443,
            'timestamp': datetime.now().isoformat()
        },
        {
            'src_ip': '8.8.8.8',  # Not TOR
            'dst_ip': '1.1.1.1',
            'src_port': 443,
            'dst_port': 50001,
            'timestamp': datetime.now().isoformat()
        }
    ]
    exits = detector.find_all_exits(test_packets)
    save_exit_timestamps(exits)
