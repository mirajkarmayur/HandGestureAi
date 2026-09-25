
# =========================================================
# HAND AI CONFIGURATION
# =========================================================

# Gesture stabilization
HISTORY_SIZE = 7
STABLE_FRAMES = 4


# Landmark smoothing
SMOOTHING_FACTOR = 0.6


# Camera
CAMERA_INDEX = 0
CAMERA_BUFFER_SIZE = 1


# Volume
VOLUME_STEP = 5
MIN_VOLUME = 0
MAX_VOLUME = 100


# MediaPipe model
MODEL_PATH = "hand_landmarker.task"
