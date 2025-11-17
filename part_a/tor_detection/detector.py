import sys
import os
import json
import logging
import glob
from datetime import datetime
from scapy.all import rdpcap, IP
import requests
import ipaddress # <--- Needed for public IP check

# Add necessary paths and config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
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

def is_public_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_global
    except Exception:
        return False

def get_ip_geolocation(ip):
    if not is_public_ip(ip):
        return {"lat": None, "lon": None, "country": "-"}
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}?fields=status,lat,lon,country")
        data = resp.json()
        if data["status"] == "success":
            return {"lat": data["lat"], "lon": data["lon"], "country": data["country"]}
    except Exception:
        pass
    return {"lat": None, "lon": None, "country": "-"}

def load_tor_node_ips():
    try:
        with open(DATABASE_FILE, 'r') as f:
            data = json.load(f)
            nodes = data.get('nodes', [])
            node_map = {}
            for node in nodes:
                ip = node.get('ip_address')
                country = node.get('country', '')
                if ip:
                    node_map[ip] = country
            return node_map
    except Exception as e:
        logger.error(f"Failed to load TOR nodes: {e}")
        return {}

def get_latest_pcap_file():
    files = glob.glob('part_a/logs/packets_*.pcap')
    if not files:
        return None
    return max(files, key=os.path.getctime)

def detect_tor_in_pcap(tor_nodes, pcap_file):
    packets = rdpcap(pcap_file)
    detections = []
    for pkt in packets:
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            # entry_node (user->tor), exit_node (tor->user) logic
            if src_ip in tor_nodes:
                geo = get_ip_geolocation(src_ip)
                entry = {
                    "ip": src_ip,
                    "country": geo["country"],
                    "lat": geo["lat"],
                    "lon": geo["lon"]
                }
                detections.append({
                    "user_ip": dst_ip,
                    "entry_node": entry,
                    "exit_node": None,
                    "confidence": 100,
                    "timestamp": datetime.now().isoformat()
                })
            elif dst_ip in tor_nodes:
                geo = get_ip_geolocation(dst_ip)
                exit = {
                    "ip": dst_ip,
                    "country": geo["country"],
                    "lat": geo["lat"],
                    "lon": geo["lon"]
                }
                detections.append({
                    "user_ip": src_ip,
                    "entry_node": None,
                    "exit_node": exit,
                    "confidence": 100,
                    "timestamp": datetime.now().isoformat()
                })
    return detections, len(packets)

def main():
    logger.info("Starting TOR traffic detection")
    tor_nodes = load_tor_node_ips()
    if not tor_nodes:
        print("No TOR IPs loaded. Exiting detection.")
        return

    pcap_file = get_latest_pcap_file()
    if not pcap_file:
        print("No capture pcap files found in logs. Run capture first.")
        return

    logger.info(f"Detecting TOR usage in pcap: {pcap_file}")
    detections, total_packet_count = detect_tor_in_pcap(tor_nodes, pcap_file)

    if detections:
        print(f"TOR traffic detected involving {len(detections)} TOR node(s):")
        for det in detections:
            if det["entry_node"]:
                print(f"- ENTRY {det['entry_node']['ip']} (User: {det['user_ip']})")
            if det["exit_node"]:
                print(f"- EXIT {det['exit_node']['ip']} (User: {det['user_ip']})")
        logger.info(f"TOR traffic detected: {detections}")
        ips_str = " ".join([det["user_ip"] for det in detections])
        subprocess.run([sys.executable, "part_a/alerting/alert_system.py", ips_str])
    else:
        print("No TOR traffic detected in the capture.")
        logger.info("No TOR traffic detected.")
        subprocess.run([sys.executable, "part_a/alerting/alert_system.py"])

    # --- Save detection results to JSON ---
    output = {
        "case_id": f"TOR-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "investigator": "TOR Analysis System",
        "summary": {
            "total_packets": total_packet_count,
            "tor_packets": len(detections),
            "connections": len(detections),
            "paths": 0,
            "avg_confidence": 100 if detections else 0
        },
        "detections": detections,
        "paths": [],
        "statistics": {
            "detection_rate": (len(detections)/total_packet_count*100) if total_packet_count else 0,
            "high_confidence": len(detections),
            "medium_confidence": 0,
            "low_confidence": 0,
            "countries": len({(det['entry_node'] or det['exit_node'] or {}).get('country') for det in detections if (det['entry_node'] or det['exit_node'])}),
            "unique_entries": len({det['entry_node']['ip'] for det in detections if det['entry_node']}),
            "unique_exits": len({det['exit_node']['ip'] for det in detections if det['exit_node']})
        }
    }
    json_path = "part_a/tor_detection/detection_results.json"
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"[INFO] Detection results written to {json_path}")

if __name__ == "__main__":
    main()
