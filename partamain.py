import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import sys
import os
import logging
from datetime import datetime

# Add the project directories to the system path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config.settings import CAPTURE_INTERFACE, CAPTURE_FILTER, CAPTURE_DURATION  # Your config values
from part_a.network_capture.capture import NetworkCapture
from tordatabase.fetchnodes import TORDatabase
from tordetection.detector import TORDetector
from alerting.alertsystem import AlertSystem

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

class TORAnalysisSystem:
    def __init__(self):
        logging.info("Initializing TOR Analysis System...")
        self.capture = NetworkCapture(interface=CAPTURE_INTERFACE, capture_filter=CAPTURE_FILTER)
        self.database = TORDatabase()
        self.detector = TORDetector()
        self.alerts = AlertSystem()

    def setup_database(self):
        logging.info("Loading or fetching TOR node database...")
        loaded = self.database.loadfromfile()
        if not loaded:
            logging.info("No existing database found, fetching fresh nodes...")
            nodes = self.database.fetchtornodes()
            if nodes:
                self.database.savetofile()
                logging.info(f"Fetched and saved {len(nodes)} TOR nodes.")
            else:
                logging.warning("Failed to fetch TOR nodes!")
                return False
        else:
            stats = self.database.getstatistics()
            logging.info(f"Loaded database with {stats['totalnodes']} TOR nodes.")
        return True

    def start_capture(self, duration=CAPTURE_DURATION):
        logging.info(f"Starting network capture for {duration} seconds...")
        packets = self.capture.startcapture(timeout=duration)
        logging.info(f"Captured {len(packets)} packets.")
        return packets

    def analyze_traffic(self, packets):
        logging.info("Analyzing captured traffic for TOR indicators...")
        detections = self.detector.analyzetraffic(packets)
        logging.info(f"Detected {len(detections)} TOR traffic events.")
        return detections

    def generate_alerts(self, detections):
        logging.info("Generating alerts for detected TOR traffic...")
        for detection in detections:
            self.alerts.generatealert(detection)

    def run(self):
        if not self.setup_database():
            logging.error("Database setup failed. Exiting.")
            return
        packets = self.start_capture()
        if not packets:
            logging.warning("No packets captured. Exiting.")
            return
        detections = self.analyze_traffic(packets)
        if detections:
            self.generate_alerts(detections)
            summary = self.detector.getsummary()
            logging.info(f"Summary: Total Detections: {summary['totaldetections']}, Average Confidence: {summary['avgconfidence']:.2f}")
        else:
            logging.info("No TOR traffic detected.")

if __name__ == "__main__":
    system = TORAnalysisSystem()
    system.run()
