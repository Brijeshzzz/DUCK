import os
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "fetch_nodes.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
import logging
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
"""
A2: TOR Node Database Module
Fetches and stores TOR relay information
"""

import requests
import json
import logging
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import *

# Setup logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TORDatabase:
    """Manages TOR node database"""
    
    def __init__(self):
        self.nodes = []
        self.last_update = None
        logger.info("TOR Database initialized")
    
    def fetch_tor_nodes(self):
        """
        Fetch current TOR relay list from official directory
        """
        logger.info(f"Fetching TOR nodes from {TOR_DIRECTORY_URL}")
        
        try:
            response = requests.get(TOR_DIRECTORY_URL, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            relays = data.get('relays', [])
            
            logger.info(f"Successfully fetched {len(relays)} TOR relays")
            
            # Process each relay
            processed_nodes = []
            for relay in relays:
                node = {
                    'fingerprint': relay.get('fingerprint'),
                    'nickname': relay.get('nickname'),
                    'ip_address': relay.get('or_addresses', [''])[0].split(':')[0] if relay.get('or_addresses') else '',
                    'or_port': relay.get('or_addresses', [''])[0].split(':')[1] if relay.get('or_addresses') and ':' in relay.get('or_addresses', [''])[0] else None,
                    'country': relay.get('country'),
                    'country_name': relay.get('country_name'),
                    'as_number': relay.get('as_number'),
                    'as_name': relay.get('as_name'),
                    'bandwidth': relay.get('observed_bandwidth', 0),
                    'flags': relay.get('flags', []),
                    'first_seen': relay.get('first_seen'),
                    'last_seen': relay.get('last_seen'),
                    'running': relay.get('running', False),
                    'is_guard': 'Guard' in relay.get('flags', []),
                    'is_exit': 'Exit' in relay.get('flags', []),
                    'is_fast': 'Fast' in relay.get('flags', []),
                    'is_stable': 'Stable' in relay.get('flags', [])
                }
                processed_nodes.append(node)
            
            self.nodes = processed_nodes
            self.last_update = datetime.now().isoformat()
            
            return processed_nodes
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch TOR nodes: {e}")
            return []
        except Exception as e:
            logger.error(f"Error processing TOR nodes: {e}")
            return []
    
    def save_to_file(self, filename=None):
        """
        Save TOR nodes to JSON file
        """
        filename = filename or DATABASE_FILE
        
        # Create directory if doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        data = {
            'last_update': self.last_update,
            'total_nodes': len(self.nodes),
            'nodes': self.nodes
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved {len(self.nodes)} nodes to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save database: {e}")
            return False
    
    def load_from_file(self, filename=None):
        """
        Load TOR nodes from JSON file
        """
        filename = filename or DATABASE_FILE
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.nodes = data.get('nodes', [])
            self.last_update = data.get('last_update')
            
            logger.info(f"Loaded {len(self.nodes)} nodes from {filename}")
            return True
            
        except FileNotFoundError:
            logger.warning(f"Database file not found: {filename}")
            return False
        except Exception as e:
            logger.error(f"Failed to load database: {e}")
            return False
    
    def get_node_by_ip(self, ip_address):
        """
        Check if IP address is a TOR node
        """
        for node in self.nodes:
            if node['ip_address'] == ip_address:
                return node
        return None
    
    def get_guard_nodes(self):
        """Get all guard (entry) nodes"""
        return [node for node in self.nodes if node['is_guard']]
    
    def get_exit_nodes(self):
        """Get all exit nodes"""
        return [node for node in self.nodes if node['is_exit']]
    
    def get_statistics(self):
        """Get database statistics"""
        total = len(self.nodes)
        running = sum(1 for node in self.nodes if node['running'])
        guards = sum(1 for node in self.nodes if node['is_guard'])
        exits = sum(1 for node in self.nodes if node['is_exit'])
        
        countries = {}
        for node in self.nodes:
            country = node.get('country', 'Unknown')
            countries[country] = countries.get(country, 0) + 1
        
        return {
            'total_nodes': total,
            'running_nodes': running,
            'guard_nodes': guards,
            'exit_nodes': exits,
            'countries': len(countries),
            'top_countries': sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10]
        }


def main():
    """Main function for testing"""
    print("=" * 60)
    print("TOR ANALYSIS SYSTEM - PART A")
    print("A2: TOR Node Database")
    print("=" * 60)
    
    # Create database instance
    db = TORDatabase()
    
    print("\nFetching TOR nodes from directory...")
    nodes = db.fetch_tor_nodes()
    
    if nodes:
        print(f"✓ Successfully fetched {len(nodes)} TOR nodes")
        
        # Save to file
        print(f"\nSaving to {DATABASE_FILE}...")
        db.save_to_file()
        print("✓ Database saved")
        
        # Show statistics
        stats = db.get_statistics()
        print(f"\n{'='*60}")
        print("DATABASE STATISTICS")
        print(f"{'='*60}")
        print(f"Total Nodes: {stats['total_nodes']}")
        print(f"Running Nodes: {stats['running_nodes']}")
        print(f"Guard Nodes: {stats['guard_nodes']}")
        print(f"Exit Nodes: {stats['exit_nodes']}")
        print(f"Countries: {stats['countries']}")
        
        print(f"\nTop 10 Countries:")
        for country, count in stats['top_countries']:
            print(f"  {country}: {count} nodes")
        
        # Show sample nodes
        print(f"\n{'='*60}")
        print("SAMPLE NODES (First 5)")
        print(f"{'='*60}")
        for i, node in enumerate(nodes[:5], 1):
            print(f"\n  Node {i}:")
            print(f"    Nickname: {node['nickname']}")
            print(f"    IP: {node['ip_address']}")
            print(f"    Country: {node['country_name']} ({node['country']})")
            print(f"    Flags: {', '.join(node['flags'])}")
            print(f"    Running: {'Yes' if node['running'] else 'No'}")
        
    else:
        print("✗ Failed to fetch TOR nodes")


if __name__ == "__main__":
    main()
