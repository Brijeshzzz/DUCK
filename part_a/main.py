import logging
import subprocess
import sys
import os

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def run_command(command_list):
    logging.info(f"Running: {' '.join(command_list)}")
    result = subprocess.run(command_list, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"Error running command: {' '.join(command_list)}\n{result.stderr}")
        sys.exit(1)
    logging.info(result.stdout)

def main():
    # 1. Fetch TOR nodes
    run_command([sys.executable, "part_a/tor_database/fetch_nodes.py"])

    # 2. Capture packets
    # Make sure python has permissions (setcap or run with sudo externally)
    run_command([sys.executable, "part_a/network_capture/capture.py"])

    # 3. Run TOR detection
    run_command([sys.executable, "-m", "part_a.tor_detection.detector"])
    
    # Add any alerting or logging you want here
    
    logging.info("Full pipeline completed successfully.")

if __name__ == "__main__":
    main()
