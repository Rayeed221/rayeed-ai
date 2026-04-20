from google.genai import types

# ─────────────────────────────────────────────────────────────────────────────
# Gemini Function Declarations
#
# Compact LLM-facing surface: 7 intent-based tools. The LLM does NOT see
# primitives (set_mode, arm, wait_*, etc.); those live in tool_registry.py
# and are composed internally by workflows.
#
# Routing (see app.py._route_tool_call):
#   emergency_stop                                → planner.trigger_failsafe
#   takeoff / goto_position / land /
#   return_to_launch / hold_position              → workflows (registry.py)
#   get_status                                    → adapter.snapshot()
# ─────────────────────────────────────────────────────────────────────────────

FUNCTION_DECLARATIONS = [
    # ── Telemetry (single unified snapshot) ───────────────────────────────────
    types.FunctionDeclaration(
        name="get_status",
        description=(
            "Return a unified live snapshot of the drone: mode, armed flag, "
            "altitude, battery percentage, GPS position (lat/lon), heading, "
            "groundspeed, EKF health, landed state, and home position. Prefer "
            "this one call over multiple individual queries."
        ),
        parameters=types.Schema(type=types.Type.OBJECT, properties={}, required=[]),
    ),

    # ── Intent verbs (run full workflows) ─────────────────────────────────────
    types.FunctionDeclaration(
        name="takeoff",
        description=(
            "Take off to a specified altitude in meters. Automatically switches "
            "to GUIDED mode, arms the motors, and waits until the target "
            "altitude is reached. Use when starting a mission from the ground."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "altitude": types.Schema(
                    type=types.Type.NUMBER,
                    description="Target altitude in meters (max 120 m)",
                ),
            },
            required=["altitude"],
        ),
    ),
    types.FunctionDeclaration(
        name="goto_position",
        description=(
            "Fly the drone to a GPS coordinate at a given altitude. Optionally "
            "override cruise speed and yaw heading. The drone must already be "
            "airborne — call takeoff first if it is on the ground."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "lat":      types.Schema(type=types.Type.NUMBER, description="Target latitude"),
                "lon":      types.Schema(type=types.Type.NUMBER, description="Target longitude"),
                "alt":      types.Schema(type=types.Type.NUMBER, description="Target altitude in meters"),
                "speed_ms": types.Schema(type=types.Type.NUMBER, description="Optional cruise speed m/s (default 5, max 15)"),
                "yaw_deg":  types.Schema(type=types.Type.NUMBER, description="Optional yaw heading 0–360°"),
            },
            required=["lat", "lon", "alt"],
        ),
    ),
    types.FunctionDeclaration(
        name="land",
        description=(
            "Land the drone at its current position. Waits for ground contact "
            "then disarms the motors."
        ),
        parameters=types.Schema(type=types.Type.OBJECT, properties={}, required=[]),
    ),
    types.FunctionDeclaration(
        name="return_to_launch",
        description=(
            "Return the drone to its home/launch point and land. Waits for "
            "arrival at home then lands and disarms."
        ),
        parameters=types.Schema(type=types.Type.OBJECT, properties={}, required=[]),
    ),
    types.FunctionDeclaration(
        name="hold_position",
        description=(
            "Hold current position for a given number of seconds — used for "
            "inspection or photography. Optionally orient to a yaw angle."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "seconds": types.Schema(type=types.Type.NUMBER, description="Hold duration in seconds"),
                "yaw_deg": types.Schema(type=types.Type.NUMBER, description="Optional yaw orientation 0–360°"),
            },
            required=["seconds"],
        ),
    ),
    types.FunctionDeclaration(
        name="emergency_stop",
        description=(
            "Immediately trigger the drone's failsafe: set RTL mode, attempt "
            "to land, and disarm. Use only when the user commands an emergency "
            "or a safety-critical situation arises mid-mission."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "reason": types.Schema(
                    type=types.Type.STRING,
                    description="Short reason string for logging",
                ),
            },
            required=[],
        ),
    ),
]
