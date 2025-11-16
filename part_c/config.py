"""
Part C Configuration - Advanced Analysis
"""

# Machine Learning Settings
ML_MODEL_PATH = "part_c/models/tor_classifier.pkl"
FEATURE_COUNT = 10  # Number of features for ML
TRAINING_DATA_SIZE = 1000  # Minimum samples for training

# Behavioral Profiling
BEHAVIOR_WINDOW_DAYS = 7  # Track user behavior for 7 days
MIN_SESSIONS_FOR_PROFILE = 5  # Need 5+ sessions to build profile
BEHAVIOR_DATABASE = "part_c/behavioral_profiling/user_profiles.json"

# Confidence Scoring
CONFIDENCE_THRESHOLDS = {
    'high': 80,      # 80-100% = High confidence
    'medium': 60,    # 60-79% = Medium confidence
    'low': 40        # 40-59% = Low confidence
}

# Pattern Analysis
PACKET_SIZE_TOLERANCE = 50  # bytes
BURST_DETECTION_WINDOW = 1.0  # seconds
MIN_PATTERN_LENGTH = 5  # minimum packets to detect pattern

# Logging
LOG_FILE = "part_c/logs/analysis.log"
LOG_LEVEL = "INFO"
