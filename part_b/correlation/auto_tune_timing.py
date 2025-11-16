import numpy as np
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

class TimingTuner:
    def __init__(self, entries, exits):
        self.entries = entries
        self.exits = exits
    
    def parse_time(self, ts):
        return datetime.fromisoformat(ts)
    
    def time_diff_seconds(self, t1, t2):
        return abs((t1 - t2).total_seconds())
    
    def score_with_params(self, window, tolerance):
        matches = 0
        total_diffs = []
        for entry in self.entries:
            et = self.parse_time(entry['timestamp'])
            for exit in self.exits:
                xt = self.parse_time(exit['timestamp'])
                diff = self.time_diff_seconds(et, xt)
                if diff <= window + tolerance:
                    matches += 1
                    total_diffs.append(diff)
        avg_diff = np.mean(total_diffs) if total_diffs else float('inf')
        return matches, avg_diff

    def tune(self, max_window=60, max_tolerance=10, window_step=1, tol_step=0.5):
        best_params = None
        best_score = -1
        for w in np.arange(1, max_window+1, window_step):
            for t in np.arange(0, max_tolerance+1, tol_step):
                matches, avg_diff = self.score_with_params(w, t)
                score = matches - avg_diff/10  # Simple scoring heuristic
                if score > best_score:
                    best_score = score
                    best_params = (w, t, matches, avg_diff)
        return best_params

def main():
    # Replace these with your real entry and exit timestamp data lists
    entries = [
        {'timestamp': '2025-11-11T20:28:44.797213'},
        {'timestamp': '2025-11-11T20:25:00.100000'}
    ]
    exits = [
        {'timestamp': '2025-11-11T20:28:44.934317'},
        {'timestamp': '2025-11-11T20:27:00.100000'}
    ]

    tuner = TimingTuner(entries, exits)
    best_w, best_t, matches, avg_diff = tuner.tune()
    logger.info(f"Best timing window: {best_w} seconds")
    logger.info(f"Best timing tolerance: {best_t} seconds")
    logger.info(f"Matches found: {matches}")
    logger.info(f"Average time difference for matches: {avg_diff:.2f} seconds")

if __name__ == "__main__":
    main()
