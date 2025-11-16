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
Configuration settings for TOR Analysis System - Part A
"""

# Network Capture Settings
CAPTURE_INTERFACE = "wlan0"
CAPTURE_FILTER = ""  # BPF filter
PACKET_COUNT = 0  # 0 = unlimited, or set specific number
TIMEOUT = 120

# TOR Database Settings
TOR_DIRECTORY_URL = "https://onionoo.torproject.org/details"
DATABASE_UPDATE_INTERVAL = 3600  # Update every 1 hour (in seconds)
DATABASE_FILE = "part_a/tor_database/tor_nodes.json"

# TOR Detection Settings
TOR_PORTS = [9001, 9030, 9050, 9051, 443, 80]  # Common TOR ports
DETECTION_CONFIDENCE_THRESHOLD = 70  # Minimum confidence % to flag as TOR

# Alerting Settings
ALERT_LOG_FILE = "part_a/logs/alerts.log"
ENABLE_CONSOLE_ALERTS = True
ENABLE_FILE_ALERTS = True

# Logging Settings
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "part_a/logs/system.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Performance Settings
MAX_PACKETS_IN_MEMORY = 10000
CLEANUP_INTERVAL = 300  # Clean old data every 5 minutes
