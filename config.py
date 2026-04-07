import os

# ─── API ────────────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyCCIKOChwt4ywQPOdTf1iRbrh_547Ir1Mo")
MODEL = "models/gemini-3.1-flash-live-preview"

# ─── Audio ──────────────────────────────────────────────────────────────────
SEND_SAMPLE_RATE    = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE          = 512
CHANNELS            = 1

# ─── Backend ────────────────────────────────────────────────────────────────
# Options: "sim" | "mavlink"
BACKEND     = os.environ.get("DRONE_BACKEND", "sim")
MAVLINK_URI = os.environ.get("MAVLINK_URI", "udp:127.0.0.1:14550")

# ─── Safety Thresholds ──────────────────────────────────────────────────────
BATTERY_CRITICAL_PCT  = 15        # % → trigger emergency
BATTERY_LOW_PCT       = 25        # % → warn + restrict
ALTITUDE_CEILING_M    = 120.0     # meters AGL — hard ceiling
MAX_SPEED_MS          = 15.0      # m/s — hard limit
TELEMETRY_STALE_SEC   = 5.0       # seconds → planner wait
EMERGENCY_STALE_SEC   = 10.0      # seconds → failsafe
MAX_RETRY_COUNT       = 3         # before abort

# ─── Planner ────────────────────────────────────────────────────────────────
WAIT_POLL_INTERVAL   = 0.2        # seconds between wait checks
PLANNER_LOOP_INTERVAL = 0.1       # seconds between planner ticks

# ─── State Persistence ──────────────────────────────────────────────────────
STATE_FILE  = "mission_state.json"
MEMORY_DIR  = "memory_store"

# ─── Voice ──────────────────────────────────────────────────────────────────
VOICE_NAME              = "Sadachbia"
CONTEXT_TRIGGER_TOKENS  = 104857
CONTEXT_TARGET_TOKENS   = 52428

# ─── Vision (OAK-D Lite / DepthAI v3) ───────────────────────────────────────
# Set VISION_ENABLED=0 to disable all vision tools (e.g. headless CI runs)
VISION_ENABLED      = os.environ.get("VISION_ENABLED", "1") == "1"
VISION_FPS          = int(os.environ.get("VISION_FPS", "15"))
VISION_DEPTH_MIN_MM = int(os.environ.get("VISION_DEPTH_MIN_MM", "200"))   # 20 cm
VISION_DEPTH_MAX_MM = int(os.environ.get("VISION_DEPTH_MAX_MM", "8000"))  # 8 m
# YOLO blob from Luxonis model zoo (auto-downloaded by blobconverter)
VISION_BLOB_NAME    = os.environ.get("VISION_BLOB_NAME", "yolov6n_coco_416x416")
VISION_BLOB_SHAVES  = int(os.environ.get("VISION_BLOB_SHAVES", "6"))
