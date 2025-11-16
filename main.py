from config.settings import CAPTURE_INTERFACE, TIMEOUT
import logging
import subprocess
import sys
import os
import json
from datetime import datetime
from config.settings import TIMEOUT  # Make sure this exists in your settings.py and matches capture.py

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

# --- Added for reporting functionality ---
from part_d.reports.report_generator import ReportGenerator
# ----------------------------------------

def run_command(command_list, timeout=60):
    logging.info(f"Running: {' '.join(command_list)}")
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            logging.error(f"Error running command: {' '.join(command_list)}\n{result.stderr}")
            sys.exit(1)
        logging.info(result.stdout)
        return result.stdout
    except subprocess.TimeoutExpired:
        logging.error(f"Timeout expired for command: {' '.join(command_list)}")
        sys.exit(1)

def save_entry_timestamps(entries):
    os.makedirs("part_b/logs", exist_ok=True)
    with open("part_b/logs/entry_timestamps.json", "w") as f:
        json.dump(entries, f, indent=4)
    logging.info(f"Saved {len(entries)} entry timestamps.")

def save_exit_timestamps(exits):
    os.makedirs("part_b/logs", exist_ok=True)
    with open("part_b/logs/exit_timestamps.json", "w") as f:
        json.dump(exits, f, indent=4)
    logging.info(f"Saved {len(exits)} exit timestamps.")

def run_part_c(entry_packets, exit_packets, timing_data, volume_data, behavior_data=None):
    pattern_analyzer = PatternAnalyzer()
    confidence_scorer = ConfidenceScorer()
    pattern_results = pattern_analyzer.analyze_traffic(entry_packets, exit_packets)
    pattern_data = {
        "similarity": pattern_results["correlation"].get("pattern_similarity", 0),
        "cell_match": pattern_results["entry_analysis"]["tor_cells"].get("is_tor_pattern", False),
        "burst_match": pattern_results["entry_analysis"]["bursts"].get("has_bursts", False)
    }
    final_confidence = confidence_scorer.calculate_final_confidence(
        timing_data=timing_data,
        volume_data=volume_data,
        pattern_data=pattern_data,
        behavior_data=behavior_data
    )
    logging.info(f"\n{'='*70}")
    logging.info("CONFIDENCE BREAKDOWN")
    logging.info(f"{'='*70}")
    logging.info(f"Timing Score:    {final_confidence['breakdown']['timing']:.1f}/100 (weight: 40%)")
    logging.info(f"Volume Score:    {final_confidence['breakdown']['volume']:.1f}/100 (weight: 30%)")
    logging.info(f"Pattern Score:   {final_confidence['breakdown']['pattern']:.1f}/100 (weight: 20%)")
    logging.info(f"Behavior Score:  {final_confidence['breakdown']['behavior']:.1f}/100 (weight: 10%)")
    logging.info(f"\nFINAL CONFIDENCE: {final_confidence['final_score']:.1f}% ({final_confidence['level'].upper()})")
    logging.info(f"{'='*70}\n")
    return final_confidence

def main():
    print("\n" + "="*70)
    print("PART A: TOR DETECTION")
    print("="*70 + "\n")
    
    run_command([sys.executable, "part_a/tor_database/fetch_nodes.py"], timeout=300)
    run_command([sys.executable, "part_a/network_capture/capture.py"], timeout=TIMEOUT + 20)  # <-- MAKE SURE THIS IS GREATER than TIMEOUT in capture.py
    run_command([sys.executable, "-m", "part_a.tor_detection.detector"], timeout=60)

    # --- Add this block to generate report.json every run --- #
    # You MUST collect/construct analysis_data dict with actual results!
    # Dummy template (replace these fields with your real results as available):

    analysis_data = {
        "case_id": f"TOR-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "investigator": "TOR Analysis System",
        "summary": {
            "total_packets": 0,         # Replace with actual values
            "tor_packets": 0,           # Replace with actual values
            "connections": 0,
            "paths": 0,
            "avg_confidence": 0
        },
        "detections": [
            # Fill with your detection dicts
        ],
        "paths": [
            # Fill with your reconstructed path dicts
        ],
        "statistics": {
            "detection_rate": 0,
            "high_confidence": 0,
            "medium_confidence": 0,
            "low_confidence": 0,
            "countries": 0,
            "unique_entries": 0,
            "unique_exits": 0
        }
    }

    generator = ReportGenerator()
    generator.generate_json_export(analysis_data)
    # -------------------------------------------------------- #

    # ... rest of your main() stays as before, unchanged ...
    # (If you already gather results in a different structure, just adjust the
    # `analysis_data` dict above to match your real result data.)

if __name__ == "__main__":
    main()
