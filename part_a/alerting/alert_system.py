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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

"""
A4: Alert System Module
Generates alerts on TOR traffic detection
"""

import logging
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import *

# Setup logging
os.makedirs(os.path.dirname(ALERT_LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=ALERT_LOG_FILE,
    level=LOG_LEVEL,
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

def send_alert(message, level="INFO"):
    if ENABLE_CONSOLE_ALERTS:
        print(f"ALERT [{level}]: {message}")
    if ENABLE_FILE_ALERTS:
        if level == "INFO":
            logger.info(message)
        elif level == "WARNING":
            logger.warning(message)
        elif level == "ERROR":
            logger.error(message)
        else:
            logger.debug(message)

def main():
    # Parse detected IPs passed as arguments
    detected_ips = sys.argv[1:] if len(sys.argv) > 1 else []

    if detected_ips:
        message = f"TOR traffic detected involving {len(detected_ips)} TOR node(s): {', '.join(detected_ips)}"
        send_alert(message, "INFO")
    else:
        # No alert for empty list
        print("No TOR traffic detected - no alerts sent.")

if __name__ == "__main__":
    main()
