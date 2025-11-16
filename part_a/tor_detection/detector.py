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
A3: TOR Detection Module
Detects TOR circuit usage in captured packets
"""

import json
import logging
import os
import glob
import sys
from scapy.all import rdpcap, IP

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import *
import subprocess

# Setup logging
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=LOG_LEVEL,
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

def load_tor_node_ips():
    try:
        with open(DATABASE_FILE, 'r') as f:
            data = json.load(f)
            nodes = data.get('nodes', [])
            return set(node['ip_address'] for node in nodes if node['ip_address'])
    except Exception as e:
        logger.error(f"Failed to load TOR nodes: {e}")
        return set()

def get_latest_pcap_file():
    files = glob.glob('part_a/logs/packets_*.pcap')
    if not files:
        return None
    return max(files, key=os.path.getctime)

def detect_tor_in_pcap(tor_ips, pcap_file):
    packets = rdpcap(pcap_file)
    detected_ips = set()
    for pkt in packets:
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            if src_ip in tor_ips or dst_ip in tor_ips:
                detected_ips.add(src_ip if src_ip in tor_ips else dst_ip)
    return detected_ips

def main():
    logger.info("Starting TOR traffic detection")

    tor_ips = load_tor_node_ips()
    if not tor_ips:
        print("No TOR IPs loaded. Exiting detection.")
        return

    pcap_file = get_latest_pcap_file()
    if not pcap_file:
        print("No capture pcap files found in logs. Run capture first.")
        return

    logger.info(f"Detecting TOR usage in pcap: {pcap_file}")
    detected_ips = detect_tor_in_pcap(tor_ips, pcap_file)

    if detected_ips:
        print(f"TOR traffic detected involving {len(detected_ips)} TOR node(s):")
        for ip in detected_ips:
            print(f"- {ip}")
        logger.info(f"TOR traffic detected: {detected_ips}")

        # Call alert system passing detected IPs
        ips_str = " ".join(detected_ips)
        subprocess.run([sys.executable, "part_a/alerting/alert_system.py", ips_str])
    else:
        print("No TOR traffic detected in the capture.")
        logger.info("No TOR traffic detected.")
        # Call alert system with empty list to suppress alerts
        subprocess.run([sys.executable, "part_a/alerting/alert_system.py"])

if __name__ == "__main__":
    main()
