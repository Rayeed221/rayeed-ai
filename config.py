import os
from dotenv import load_dotenv

load_dotenv()

# ─── API ────────────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY   = os.environ.get("GROQ_API_KEY")
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY")

MODEL = "models/gemini-3.1-flash-live-preview"

# ─── Ollama ──────────────────────────────────────────────────────────────────
OLLAMA_BASE_URL   = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL      = os.environ.get("OLLAMA_MODEL", "qwen3:latest")

# ─── Groq ────────────────────────────────────────────────────────────────────
GROQ_MODEL        = os.environ.get("GROQ_MODEL", "qwen/qwen3-32b")

# ─── Audio ──────────────────────────────────────────────────────────────────
SEND_SAMPLE_RATE    = int(os.environ.get("SEND_SAMPLE_RATE", "16000"))
RECEIVE_SAMPLE_RATE = int(os.environ.get("RECEIVE_SAMPLE_RATE", "24000"))
CHUNK_SIZE          = int(os.environ.get("CHUNK_SIZE", "512"))
CHANNELS            = int(os.environ.get("CHANNELS", "1"))
AUDIO_DEVICE_ID     = os.environ.get("AUDIO_DEVICE_ID")  # None = default; set to device index for specific mic

# ─── Backend ────────────────────────────────────────────────────────────────
# Options: "sim" | "mavlink"
# BACKEND     = os.environ.get("DRONE_BACKEND", "sim")
BACKEND     = os.environ.get("DRONE_BACKEND", "mavlink")

MAVLINK_URI = os.environ.get("MAVLINK_URI", "tcp:127.0.0.1:5763")

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

# ─── Avoidance (DroNet) ─────────────────────────────────────────────────────
DRONET_MODEL_PATH       = os.environ.get(
    "DRONET_MODEL_PATH",
    "vision/avoidance/dronet_tiny_openvino_2022.1_5shave.blob",
)
AVOIDANCE_COLLISION_THR = float(os.environ.get("AVOIDANCE_COLLISION_THR", "0.7"))
AVOIDANCE_STALE_SEC     = float(os.environ.get("AVOIDANCE_STALE_SEC",     "0.5"))

# ─── VIO / SLAM staleness (read early by PoseCache) ─────────────────────────
# PoseCache.get() consults this to decide whether the VIO-derived heading is
# fresh enough to override the telemetry heading.  Hoisted above the Vision
# section because pose_cache.py imports it; rest of the block is below.
VIOSLAM_STALE_SEC       = float(os.environ.get("VIOSLAM_STALE_SEC", "0.5"))

# ─── Vision (OAK-D Lite / DepthAI v3) ───────────────────────────────────────
# Set VISION_ENABLED=0 to disable all vision tools (e.g. headless CI runs)
VISION_ENABLED      = os.environ.get("VISION_ENABLED", "1") == "1"
VISION_FPS          = int(os.environ.get("VISION_FPS", "15"))
VISION_DEPTH_MIN_MM = int(os.environ.get("VISION_DEPTH_MIN_MM", "200"))   # 20 cm
VISION_DEPTH_MAX_MM = int(os.environ.get("VISION_DEPTH_MAX_MM", "8000"))  # 8 m
# YOLO blob from Luxonis model zoo (auto-downloaded by blobconverter)
VISION_BLOB_NAME    = os.environ.get("VISION_BLOB_NAME", "yolov6n_coco_416x416")
VISION_BLOB_SHAVES  = int(os.environ.get("VISION_BLOB_SHAVES", "6"))

# YOLO blob local caching — save to codebase instead of system cache
YOLO_BLOB_DIR       = os.environ.get("YOLO_BLOB_DIR", "vision/models")
YOLO_AUTO_DOWNLOAD  = os.environ.get("YOLO_AUTO_DOWNLOAD", "1") == "1"

# Camera mounting relative to drone body (FRD axes).
# Adjust these when the OAK-D Lite is not mounted level and forward-facing.
VISION_CAMERA_PITCH_DEG  = float(os.environ.get("VISION_CAMERA_PITCH_DEG",  "0.0"))
VISION_CAMERA_YAW_DEG    = float(os.environ.get("VISION_CAMERA_YAW_DEG",    "0.0"))
VISION_CAMERA_OFFSET_F_M = float(os.environ.get("VISION_CAMERA_OFFSET_F_M", "0.0"))
VISION_CAMERA_OFFSET_R_M = float(os.environ.get("VISION_CAMERA_OFFSET_R_M", "0.0"))
VISION_CAMERA_OFFSET_D_M = float(os.environ.get("VISION_CAMERA_OFFSET_D_M", "0.0"))
# OAK-D Lite RGB camera horizontal field of view (degrees)
VISION_CAMERA_HFOV_DEG   = float(os.environ.get("VISION_CAMERA_HFOV_DEG",   "73.0"))

# ─── VIO / SLAM (OAK-D Lite + RTABMap on Myriad X) ──────────────────────────
# HARDWARE CONSTRAINT: cannot run alongside the regular vision tools on the
# SAME OAK-D unit (Myriad X cannot host RTABMapSLAM + YOLO + SLC concurrently).
# Set only one of {VISION_ENABLED, VIOSLAM_ENABLED} to "1" per device.
# (VIOSLAM_STALE_SEC is hoisted earlier — see the section above.)
VIOSLAM_ENABLED         = os.environ.get("VIOSLAM_ENABLED", "0") == "1"
VIOSLAM_FPS             = int(os.environ.get("VIOSLAM_FPS", "30"))
VIOSLAM_SLAM_HZ         = float(os.environ.get("VIOSLAM_SLAM_HZ", "2.0"))
VIOSLAM_DB_PATH         = os.environ.get("VIOSLAM_DB_PATH", "map.db")
VIOSLAM_LOAD_DB         = os.environ.get("VIOSLAM_LOAD_DB", "0") == "1"
VIOSLAM_OCC_CELL_SIZE   = float(os.environ.get("VIOSLAM_OCC_CELL_SIZE", "0.05"))   # MUST equal SLAM_PARAMS["Grid/CellSize"]
VIOSLAM_PROXIMITY_THR_M = float(os.environ.get("VIOSLAM_PROXIMITY_THR_M", "1.5"))
