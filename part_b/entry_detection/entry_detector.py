"""
B1: Entry Node Detection
Identifies which TOR entry node (guard) the user connected to
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from part_a.tor_database.fetch_nodes import TORDatabase
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EntryNodeDetector:
    """Detects entry nodes (guards) in captured traffic"""
    
    def __init__(self):
        self.tor_db = TORDatabase()
        self.tor_db.load_from_file()
        self.guard_nodes = self.tor_db.get_guard_nodes()
        logger.info(f"Loaded {len(self.guard_nodes)} guard nodes")
    
    def identify_entry_node(self, packet_info):
        """
        Identify if packet is connecting to a TOR entry node
        
        Args:
            packet_info: {
                'src_ip': source IP (user),
                'dst_ip': destination IP (possibly TOR node),
                'timestamp': when connection made,
                'src_port': source port,
                'dst_port': destination port
            }
        
        Returns:
            {
                'is_entry': True/False,
                'entry_node': node info if found,
                'user_ip': original user IP,
                'timestamp': connection time
            }
        """
        dst_ip = packet_info.get('dst_ip')
        
        # Check if destination is a known guard node
        for node in self.guard_nodes:
            if node['ip_address'] == dst_ip and node['running']:
                logger.info(f"✓ Entry node detected: {dst_ip} ({node['country']})")
                
                return {
                    'is_entry': True,
                    'entry_node': node,
                    'user_ip': packet_info.get('src_ip'),
                    'timestamp': packet_info.get('timestamp'),
                    'connection': {
                        'src_port': packet_info.get('src_port'),
                        'dst_port': packet_info.get('dst_port')
                    }
                }
        
        return {
            'is_entry': False,
            'entry_node': None
        }
    
    def find_all_entries(self, captured_packets):
        """
        Find all entry node connections in captured traffic
        
        Args:
            captured_packets: List of packet info dictionaries
        
        Returns:
            List of entry node detections
        """
        entries = []
        
        for packet in captured_packets:
            result = self.identify_entry_node(packet)
            if result['is_entry']:
                entries.append(result)
        
        logger.info(f"Found {len(entries)} entry node connections")
        return entries


def main():
    """Test entry node detection"""
    print("="*70)
    print("PART B - B1: Entry Node Detection")
    print("="*70)
    
    detector = EntryNodeDetector()
    
    # Test with sample packets
    test_packets = [
        {
            'src_ip': '192.168.1.100',
            'dst_ip': detector.guard_nodes[0]['ip_address'] if detector.guard_nodes else '1.2.3.4',
            'src_port': 50000,
            'dst_port': 9001,
            'timestamp': datetime.now().isoformat()
        },
        {
            'src_ip': '192.168.1.100',
            'dst_ip': '8.8.8.8',  # Not TOR
            'src_port': 50001,
            'dst_port': 443,
            'timestamp': datetime.now().isoformat()
        }
    ]
    
    print(f"\nTesting with {len(test_packets)} packets...")
    entries = detector.find_all_entries(test_packets)
    
    print(f"\n{'='*70}")
    print(f"RESULTS: {len(entries)} entry nodes detected")
    print(f"{'='*70}")
    
    for i, entry in enumerate(entries, 1):
        print(f"\nEntry {i}:")
        print(f"  User IP: {entry['user_ip']}")
        print(f"  Entry Node: {entry['entry_node']['ip_address']}")
        print(f"  Country: {entry['entry_node']['country_name']}")
        print(f"  Timestamp: {entry['timestamp']}")


if __name__ == "__main__":
    main()

import json

def save_entry_timestamps(entries):
    timestamps = [entry['timestamp'] for entry in entries]
    with open("part_b/logs/entry_timestamps.json", "w") as f:
        json.dump(timestamps, f, indent=4)

# After entries are found in find_all_entries(), add:
# save_entry_timestamps(entries)

# Add this call inside the main() after find_all_entries test like:

if __name__ == "__main__":
    main()
    # Save timestamps from test entries run:
    detector = EntryNodeDetector()
    test_packets = [
        {
            'src_ip': '192.168.1.100',
            'dst_ip': detector.guard_nodes[0]['ip_address'] if detector.guard_nodes else '1.2.3.4',
            'src_port': 50000,
            'dst_port': 9001,
            'timestamp': datetime.now().isoformat()
        },
        {
            'src_ip': '192.168.1.100',
            'dst_ip': '8.8.8.8',  # Not TOR
            'src_port': 50001,
            'dst_port': 443,
            'timestamp': datetime.now().isoformat()
        }
    ]
    entries = detector.find_all_entries(test_packets)
    save_entry_timestamps(entries)
