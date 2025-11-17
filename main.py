from config.settings import CAPTURE_INTERFACE, TIMEOUT
import logging
import subprocess
import sys
import os
import json
from datetime import datetime
from config.settings import TIMEOUT
import geoip2.database 
import requests 
import time 

# Configuration for GeoLite2 Database (!!! UPDATE THIS PATH !!!)
GEOIP_DB_PATH = os.path.join(os.path.dirname(__file__), "config", "GeoLite2-City.mmdb")

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "part_b", "entry_detection")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "part_b", "exit_detection")))
from entry_detector import EntryNodeDetector
from exit_detector import ExitNodeDetector

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "part_c", "pattern_analysis")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "part_c", "confidence_scoring")))
from pattern_analyzer import PatternAnalyzer
from confidence_scorer import ConfidenceScorer

from part_d.reports.report_generator import ReportGenerator

# =========================================================
# GEO LOCATION ENRICHMENT HELPERS
# =========================================================
def get_ip_geolocation(ip, reader):
    """Fetches geolocation (lat/lon) for a given IP address."""
    if not ip or ip.startswith(('192.168.', '10.', '172.16.')):
        return None, None, None 
    
    try:
        response = reader.city(ip)
        lat = response.location.latitude
        lon = response.location.longitude
        country = response.country.name
        logging.debug(f"GeoIP success for {ip} via DB.")
        return lat, lon, country
    except geoip2.errors.AddressNotFoundError:
        try:
            time.sleep(0.5) 
            url = f"http://ip-api.com/json/{ip}"
            res = requests.get(url, timeout=5)
            data = res.json()
            if data['status'] == 'success':
                lat = data['lat']
                lon = data['lon']
                country = data['country']
                logging.warning(f"GeoIP success for {ip} via API fallback.")
                return lat, lon, country
        except (requests.exceptions.RequestException, KeyError):
            logging.error(f"Failed to get geolocation for IP: {ip}")
    except Exception as e:
        logging.error(f"General GeoIP error for {ip}: {e}")

    return None, None, None

def enrich_detections_with_geolocation(detections):
    """Iterates through detections and adds 'lat', 'lon', and 'country' fields."""
    if not os.path.exists(GEOIP_DB_PATH):
        logging.critical(f"GeoIP Database not found at {GEOIP_DB_PATH}. Skipping geolocation.")
        return detections

    try:
        reader = geoip2.database.Reader(GEOIP_DB_PATH)
    except Exception as e:
        logging.critical(f"Error initializing GeoIP reader: {e}. Skipping geolocation.")
        return detections

    final_enriched_detections = []
    
    for det in detections:
        # <<< CRITICAL DEFENSIVE FIX: Ensure 'det' is a dictionary >>>
        if not isinstance(det, dict):
            logging.warning("Skipping non-dictionary detection entry (possible corruption).")
            continue
            
        entry_node = det.get('entry_node')
        exit_node = det.get('exit_node')

        # Enrich Entry Node
        if entry_node and isinstance(entry_node, dict) and entry_node.get('ip'):
            ip = entry_node['ip']
            lat, lon, country = get_ip_geolocation(ip, reader)
            if lat and lon:
                det['entry_node']['lat'] = lat
                det['entry_node']['lon'] = lon
                det['entry_node']['country'] = country
        
        # Enrich Exit Node
        if exit_node and isinstance(exit_node, dict) and exit_node.get('ip'):
            ip = exit_node['ip']
            lat, lon, country = get_ip_geolocation(ip, reader)
            if lat and lon:
                det['exit_node']['lat'] = lat
                det['exit_node']['lon'] = lon
                det['exit_node']['country'] = country
        
        final_enriched_detections.append(det)


    reader.close()
    logging.info(f"Successfully enriched {len(final_enriched_detections)} detection entries.")
    return final_enriched_detections
# =========================================================

def run_command(command_list, timeout=60):
    logging.info(f"Running: {' '.join(command_list)}")
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            logging.error(f"Error running command: {' '.join(command_list)}\n{result.stderr}")
            return "" 
        logging.info(result.stdout)
        return result.stdout
    except subprocess.TimeoutExpired:
        logging.error(f"Timeout expired for command: {' '.join(command_list)}")
        return "" 

def get_latest_detection_results():
    """Reads the raw detection results from the file generated by detector.py."""
    filepath = "part_a/tor_detection/detection_results.json"
    if not os.path.exists(filepath):
        logging.warning(f"{filepath} not found.")
        return []
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            # Safely return the detections list, assuming the file structure is correct.
            if isinstance(data, dict) and 'detections' in data:
                return data['detections']
            if isinstance(data, list):
                return data # Accept raw list if file is not wrapped in dict
            return []
    except json.JSONDecodeError:
        logging.error(f"Could not decode JSON from {filepath}")
        return []

def main():
    print("\n" + "="*70)
    print("PART A: TOR DETECTION")
    print("="*70 + "\n")
    
    # 1. Run core detection pipeline
    run_command([sys.executable, "part_a/tor_database/fetch_nodes.py"], timeout=300)
    run_command([sys.executable, "part_a/network_capture/capture.py"], timeout=TIMEOUT + 20)
    
    # NOTE: Timeout is 180 seconds now due to the previous 'sed' command.
    run_command([sys.executable, "-m", "part_a.tor_detection.detector"], timeout=180)

    # 2. Get the RAW detection results 
    raw_detections = get_latest_detection_results()
    
    # 3. ENRICH DETECTIONS WITH GEO LOCATION
    if raw_detections:
        print("\n" + "="*70)
        print("PART B: GEO-LOCATION ENRICHMENT")
        print("="*70 + "\n")
        
        enriched_detections = enrich_detections_with_geolocation(raw_detections)
    else:
        enriched_detections = []
        logging.info("No raw detections found to enrich.")
        
    # 4. Construct final analysis data structure
    analysis_data = {
        "case_id": f"TOR-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "investigator": "TOR Analysis System",
        "summary": {
            "total_packets": 0,         
            "tor_packets": 0,           
            "connections": len(enriched_detections),
            "paths": len(enriched_detections),
            "avg_confidence": 0 
        },
        "detections": enriched_detections, 
        "paths": [],
        "statistics": {
            "detection_rate": 0,
            "high_confidence": 0,
            "medium_confidence": 0,
            "low_confidence": 0,
            "countries": 0,
            "unique_entries": len(set(d['entry_node']['ip'] for d in enriched_detections if d.get('entry_node') and d['entry_node'].get('ip'))),
            "unique_exits": len(set(d['exit_node']['ip'] for d in enriched_detections if d.get('exit_node') and d['exit_node'].get('ip')))
        }
    }

    # 5. Generate the final report (which the frontend reads)
    generator = ReportGenerator()
    generator.generate_json_export(analysis_data)
    print("[INFO] Report files updated with geolocation data.")
    
    print("\n" + "="*70)
    print("Pipeline Complete: Front-end map should now display nodes.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()