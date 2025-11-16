"""
Part B Configuration
"""

# Correlation Settings
TIMING_WINDOW = 5  # seconds - max time between entry and exit
TIMING_TOLERANCE = 0.5  # seconds - acceptable variance
VOLUME_TOLERANCE = 0.15  # 15% difference allowed in packet sizes

# Confidence Scoring Weights
TIMING_WEIGHT = 40  # 40% of confidence score
VOLUME_WEIGHT = 30  # 30% of confidence score
PATTERN_WEIGHT = 20  # 20% of confidence score
BEHAVIOR_WEIGHT = 10  # 10% of confidence score

# Path Reconstruction
MAX_RELAY_HOPS = 3  # TOR uses 3 hops typically
MIN_CONFIDENCE_FOR_PATH = 70  # Only show paths with 70%+ confidence

# Logging
LOG_FILE = "part_b/logs/correlation.log"
LOG_LEVEL = "INFO"
