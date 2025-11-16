import logging
import sys
import os
import pyshark
from datetime import datetime

# Fix sys.path to import config from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from config.settings import CAPTURE_INTERFACE, TIMEOUT

LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = 'logs/capture.log'

# Setup logging
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

def capture_packets(interface, duration_sec):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"part_a/logs/packets_{timestamp}_pyshark.pcap"
    logger.info(f"Starting capture on {interface} for {duration_sec} seconds")
    capture = pyshark.LiveCapture(interface=interface, output_file=filename)
    capture.sniff(timeout=duration_sec)
    logger.info(f"Capture completed, saved to {filename}")
    print(f"Capture completed, saved to {filename}")

if __name__ == "__main__":
    capture_packets(CAPTURE_INTERFACE, TIMEOUT)
